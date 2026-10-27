"""Read-only saved-mesh attachment and wheel-clearance checks, called by pose gate."""
import re


def check_panel_clearance():
    """Read evaluated moving surfaces at ten actual hinge fractions."""
    import bpy
    import math
    from mathutils.bvhtree import BVHTree
    rig=bpy.data.objects['J73_Skeleton']
    rig.animation_data.action=None
    def tree(name):
        obj=bpy.data.objects['J73Mesh_'+name].evaluated_get(bpy.context.evaluated_depsgraph_get())
        mesh=obj.to_mesh()
        result=BVHTree.FromPolygons([obj.matrix_world@v.co for v in mesh.vertices],
                                   [tuple(p.vertices) for p in mesh.polygons])
        obj.to_mesh_clear()
        return result
    fixed={name:tree(name) for name in ('Body','Interior','Windshield','RearGlass')}
    for fraction in (0,.025,.05,.1,.2,.35,.5,.65,.8,1):
        for bone in rig.pose.bones:
            bone.rotation_euler=(0,0,0)
            bone.location=(0,0,0)
        for name,angles in {'Hood':(57*fraction,0,0),'Trunk':(-47*fraction,0,0),
                            'DoorLeft':(0,-66*fraction,0),'DoorRight':(0,66*fraction,0)}.items():
            rig.pose.bones[name].rotation_euler=tuple(math.radians(v) for v in angles)
        bpy.context.view_layer.update()
        moving={name:tree(name) for name in ('Hood','Trunk','DoorLeft','DoorRight','WindowLeft','WindowRight')}
        pairs=[('Hood','Body'),('Hood','Windshield'),('Hood','Interior'),
               ('Trunk','Body'),('Trunk','RearGlass'),('Trunk','Interior'),
               ('DoorLeft','Body'),('DoorRight','Body'),
               ('DoorLeft','Interior'),('DoorRight','Interior')]
        # Closed glass seats in its fixed chrome seal. Raised glass must clear
        # that seal once the doors begin opening. Parent-door pockets are intentional.
        if fraction:
            pairs += [('WindowLeft','Body'),('WindowRight','Body')]
        for panel,obstacle in pairs:
            contacts=moving[panel].overlap(fixed[obstacle])
            assert not contacts, f'{panel}/{obstacle} overlap at hinge fraction {fraction}: {len(contacts)} surface pairs'
    print('PASS ten hinge fractions: hood/trunk/doors clear fixed body/cabin/glass; raised windows clear opening seals')


def check_front_lamp_recess(atlas):
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    body=bpy.data.objects['J73Mesh_Body']
    mesh=body.data
    uv=mesh.uv_layers.active
    def semantic(face):
        coord=uv.data[face.loop_start].uv
        cell=int(coord.x*atlas['columns'])+int(coord.y*atlas['rows'])*atlas['columns']
        return atlas['zones'][cell//len(atlas['colours'])],atlas['colours'][cell%len(atlas['colours'])]
    field_faces=[tuple(face.vertices) for face in mesh.polygons
                 if semantic(face)[1]=='shadow' and all(mesh.vertices[i].co.y>2.34 for i in face.vertices)]
    assert field_faces,'Front fascia shadow field missing'
    field=BVHTree.FromPolygons([v.co for v in mesh.vertices],field_faces)
    gaps=[]
    for centre,zone in ((-.708,'headleft'),(.708,'headright')):
        for dx,dz in ((.013,.011),(-.013,.011),(.039,.033),(-.039,-.033)):
            origin=Vector((centre+dx,2.7,.641-.65+dz))
            direction=Vector((0,-1,0))
            hit,lens,normal,index=body.ray_cast(origin,direction)
            assert hit and semantic(mesh.polygons[index])==(zone,'headlamp'), \
                f'Front lamp aperture does not expose its semantic lens at {centre,dx,dz}'
            assert normal.y>.8,'Front lens faces inward'
            assert field.ray_cast(origin,direction,.4)[0] is None, \
                'Opaque front/back fascia spans the headlamp opening'
            neighbour=Vector((centre+dx,2.7,.641-.65+.132))
            adjacent,_,_,_=field.ray_cast(neighbour,direction,.4)
            assert adjacent is not None,'Adjacent front fascia surface missing'
            gap=adjacent.y-lens.y
            assert .008<gap<.025, \
                f'Headlamp must recess8..25mm behind adjacent actual fascia, got {gap*1000:.3f}mm'
            gaps.append(gap)
    print(f'PASS both front lamp apertures:8 saved rays, no spanning shadow caps, '
          f'lens recess {min(gaps)*1000:.3f}..{max(gaps)*1000:.3f}mm behind adjacent fascia')


def check_trunk_cup_backing(atlas):
    """Catch folded underside crossings hidden by closed-component checks."""
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    mesh=bpy.data.objects['J73Mesh_Trunk'].data
    uv=mesh.uv_layers.active
    def painted(face):
        coord=uv.data[face.loop_start].uv
        slot=int(coord.x*atlas['columns'])+int(coord.y*atlas['rows'])*atlas['columns']
        return atlas['colours'][slot%len(atlas['colours'])]=='red'
    skin=BVHTree.FromPolygons([v.co for v in mesh.vertices],
                             [tuple(f.vertices) for f in mesh.polygons if painted(f)])
    samples=0
    for column in range(-8,9):
        x=column*.009
        for z in (.846,.854,.862,.870,.878,.886):
            outer,on,_,_=skin.ray_cast(Vector((x,-3,z-.65)),Vector((0,1,0)),1.)
            inner,inn,_,_=skin.ray_cast(Vector((x,-2,z-.65)),Vector((0,-1,0)),1.)
            assert outer is not None and inner is not None, 'Open trunk cup backing'
            assert on.y<-.1 and inn.y>.1, 'Trunk cup backing crosses or inverts its exterior'
            assert .0035<inner.y-outer.y<.0065, 'Trunk cup backing needs positive thin metal thickness'
            samples+=1
    print(f'PASS trunk cup backing: {samples} two-sided rays, opposing normals and positive thickness')


def check_cargo_visibility(vehicle_script):
    """Require fixed cargo lining to occlude actual upper rear-wheel surfaces.

    Samples 28 positions just inside this model's trunk aperture and every
    upper/rear wheel triangle centre. Excludes the lid deliberately, so a
    closed lid cannot hide a missing fixed liner. Does not mutate the scene.
    Native rendering and untested camera rays remain separate gates.
    """
    import re
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree

    vertices = []
    faces = []
    for name in ('Body', 'Interior'):
        obj = bpy.data.objects['J73Mesh_' + name]
        offset = len(vertices)
        vertices.extend(obj.matrix_world @ vertex.co for vertex in obj.data.vertices)
        faces.extend(tuple(offset + index for index in face.vertices) for face in obj.data.polygons)
    fixed = BVHTree.FromPolygons(vertices, faces)
    wheel = bpy.data.objects['J73Mesh_Wheel']
    wheel.data.calc_loop_triangles()
    rear_wheels = [(name, tuple(map(float, values.split()))) for name, values in
                   re.findall(r'wheel (\w+)\s*\{[^}]*offset\s*=\s*([^,]+)', vehicle_script)
                   if name.startswith('Rear')]
    assert len(rear_wheels) == 2, 'Cargo visibility requires both native rear wheel placements'
    samples = 0
    leaks = 0
    backward = 0
    for name, (x, z, y) in rear_wheels:
        centre = Vector((-x, y, z))
        for triangle in wheel.data.loop_triangles:
            target = sum((wheel.data.vertices[index].co for index in triangle.vertices), Vector()) / 3 + centre
            if target.z <= z + .14 or target.y >= y + .14:
                continue
            for aperture_x in (-.68, -.51, -.34, 0, .34, .51, .68):
                for aperture_y in (-2.155, -2.08, -2.00, -1.92):
                    origin = Vector((aperture_x, aperture_y, .31))
                    direction = (target-origin).normalized()
                    distance = (target-origin).length
                    hit, normal, _, _ = fixed.ray_cast(origin, direction, distance-.0002)
                    samples += 1
                    if hit is None:
                        leaks += 1
                    elif normal.dot(direction) >= 0:
                        backward += 1
    assert samples > 100000, 'Cargo visibility requires the complete upper/rear wheel sample set'
    assert leaks == 0 and backward == 0, (
        f'Cargo lining exposes rear wheels: {leaks}/{samples} unblocked rays, '
        f'{backward} first hits face away from the opening')
    print(f'PASS cargo fixed lining: {samples} saved-mesh rays, zero tire leaks or backward first hits')


def check_backlight_support():
    """Audit the saved rounded backlight, exact support seams and exposed glass.

    No file writes or scene mutations. Tests the actual saved mesh rather than
    generator profile constants. Native appearance remains a separate gate.
    """
    import bpy
    import math
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    glass = bpy.data.objects['J73Mesh_RearGlass']
    body = bpy.data.objects['J73Mesh_Body']
    edge_use = {}
    for face in glass.data.polygons:
        for edge in face.edge_keys:
            edge = tuple(sorted(edge))
            edge_use[edge] = edge_use.get(edge, 0) + 1
    boundary = [edge for edge, count in edge_use.items() if count == 1]
    adjacency = {}
    for a, b in boundary:
        adjacency.setdefault(a, []).append(b)
        adjacency.setdefault(b, []).append(a)
    assert len(boundary) > 50 and all(len(v) == 2 for v in adjacency.values()), 'Backlight requires one continuous unbranched perimeter'
    start = min(adjacency)
    ordered = [start]
    previous = None
    current = start
    while True:
        following = next(v for v in adjacency[current] if v != previous)
        if following == start:
            break
        assert following not in ordered, 'Backlight boundary loops must not self-repeat'
        ordered.append(following)
        previous, current = current, following
    assert len(ordered) == len(adjacency), 'Backlight contains disconnected perimeter loops'
    points = [glass.matrix_world @ glass.data.vertices[index].co for index in ordered]
    turns = []
    for i, point in enumerate(points):
        a = (point-points[i-1]).normalized()
        b = (points[(i+1) % len(points)]-point).normalized()
        turns.append(math.degrees(math.acos(max(-1, min(1, a.dot(b))))))
    assert max(turns) < 35, f'Backlight retains an abrupt perimeter corner: {max(turns):.2f} degrees'
    body_tree = BVHTree.FromPolygons([body.matrix_world @ v.co for v in body.data.vertices],
                                     [tuple(p.vertices) for p in body.data.polygons])
    gaps = [body_tree.find_nearest(point)[3] for point in points]
    assert max(gaps) < .0001, f'Backlight perimeter lacks exact body support: {max(gaps)*1000:.3f}mm'
    outward = Vector((0, -.35, .94)).normalized()
    assert all(p.normal.dot(outward) > .75 for p in glass.data.polygons if p.area > 1e-8), 'Backlight has inward or steeply folded faces'
    glass.data.calc_loop_triangles()
    samples = 0
    for triangle in glass.data.loop_triangles:
        centre = sum((glass.matrix_world @ glass.data.vertices[i].co for i in triangle.vertices), Vector()) / 3
        if min((centre-p).length for p in points) <= .025:
            continue  # The narrow chrome perimeter is intentionally over the glass edge.
        normal = glass.data.polygons[triangle.polygon_index].normal
        hit, _, _, _ = body_tree.ray_cast(centre+normal*.025, -normal, .0248)
        assert hit is None, 'Paint/body geometry hides the actual backlight aperture'
        samples += 1
    assert samples > 1000, 'Need dense whole-aperture backlight visibility coverage'
    print(f'PASS backlight: {len(points)} supported perimeter points, max turn {max(turns):.2f}deg, max support gap {max(gaps)*1000:.4f}mm, {samples} visible glass rays')


def check_placement(atlas, vehicle_script):
    import bpy
    from mathutils import Matrix, Vector
    from mathutils.bvhtree import BVHTree

    check_front_lamp_recess(atlas)
    check_trunk_cup_backing(atlas)
    check_cargo_visibility(vehicle_script)
    check_backlight_support()
    body = bpy.data.objects['J73Mesh_Body']
    body_length = max(vertex.co.y for vertex in body.data.vertices)-min(vertex.co.y for vertex in body.data.vertices)
    body_width=max(vertex.co.x for vertex in body.data.vertices)-min(vertex.co.x for vertex in body.data.vertices)
    assert abs(body_length-4.88442)<.010, \
        f'Saved Body length {body_length:.5f}m differs from factory 192.3in beyond10mm'
    assert abs(body_width-1.91262)<.010, \
        f'Saved Body width {body_width:.5f}m differs from factory75.3in beyond10mm'

    def colour(obj, face):
        uv = obj.data.uv_layers.active.data[face.loop_start].uv
        slot = int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
        return atlas['colours'][slot % len(atlas['colours'])]

    interior = bpy.data.objects['J73Mesh_Interior']
    remaining = {face.index for face in interior.data.polygons if colour(interior, face) == 'seat'}
    boxes = []
    while remaining:
        vertices = set(interior.data.polygons[remaining.pop()].vertices)
        while True:
            linked = {index for index in remaining if vertices.intersection(interior.data.polygons[index].vertices)}
            if not linked:
                break
            for index in linked:
                vertices.update(interior.data.polygons[index].vertices)
            remaining -= linked
        points = [interior.data.vertices[index].co for index in vertices]
        low = Vector(tuple(min(point[axis] for point in points) for axis in range(3)))
        high = Vector(tuple(max(point[axis] for point in points) for axis in range(3)))
        boxes.append((low, high))
    # Upholstered headlining shares the fabric swatch, but is above the seats
    # and spans the cabin. Classify cushions/backrests by physical size/height.
    cushions = [(low, high) for low, high in boxes
                if high.z < .1 and .3 < high.x-low.x < 1.35
                and high.z-low.z < .25 and high.y-low.y > .3]
    backs = [(low, high) for low, high in boxes
             if high.z < .4 and .3 < high.x-low.x < 1.35
             and high.z-low.z > .4 and high.y-low.y < .2]
    assert len(cushions) == len(backs) == 3, 'Need two front buckets and one full-width rear bench'
    for group in (cushions,backs):
        front=[(a,b) for a,b in group if (a.y+b.y)/2>-.4]
        rear=[(a,b) for a,b in group if (a.y+b.y)/2<-.4]
        assert len(front)==2 and len(rear)==1, 'Incorrect bucket/bench row arrangement'
        assert all(.45<b.x-a.x<.55 for a,b in front), 'Front buckets lost individual padding'
        assert 1.15<rear[0][1].x-rear[0][0].x<1.30, 'Rear bench must span both rear occupants'
    check_cabin_sheets(interior, atlas, backs)
    passengers = re.findall(r'passenger (\w+)\s*\{.*?position inside\s*\{\s*offset\s*=\s*([^,]+)',
                            vehicle_script, re.S)
    assert len(passengers) == 4, 'Need four native passenger attachment positions'
    for name, values in passengers:
        x, z, y = map(float, values.split())
        point = Vector((-x, y, z))  # Native script X is mirrored by vehicle renderer.
        matches = [(low, high) for low, high in cushions
                   if low.x < point.x < high.x and low.y < point.y < high.y]
        assert len(matches) == 1, f'{name} attachment is outside its visible cushion'
        low, high = matches[0]
        assert -.02 < point.z-high.z < .12, f'{name} attachment height disagrees with seat top'
        center = (low+high)/2
        back = min(backs, key=lambda box: ((box[0]+box[1])/2-center).length)
        back_center = (back[0]+back[1])/2
        assert back_center.y < center.y-.1, f'{name} visible seat faces away from nose'
        assert ('Left' in name) == (point.x < 0), f'{name} attachment is on the wrong side'
        assert ('Front' in name) == (center.y > -.4), f'{name} attachment uses wrong seat row'
    print('PASS four native attachments match saved cushions, heights, sides and forward-facing backrests')
    steering = [face for face in interior.data.polygons if colour(interior, face) == 'chrome'
                and face.center.y > .18 and 0 < face.center.z < .45]
    assert steering, 'Missing visible steering wheel and column hub'
    steering_center = sum((face.center for face in steering), Vector())/len(steering)
    assert -.55 < steering_center.x < -.20 and .15 < steering_center.y < .45, \
        'Steering wheel must stay on the driver side, forward of front seat'
    rig = bpy.data.objects['J73_Skeleton']
    for side, direction in (('Left', -1), ('Right', 1)):
        door = bpy.data.objects['J73Mesh_Door'+side]
        skin = [door.data.vertices[index].co for face in door.data.polygons if colour(door, face) == 'red'
                for index in face.vertices]
        front = max(point.y for point in skin)
        outer = max(point.x*direction for point in skin if point.y > front-.02)
        hinge = rig.data.bones['Door'+side].head_local
        assert abs(hinge.y-front)<.03 and abs(hinge.x*direction-outer)<.03, \
            f'{side} door hinge must follow the front outer skin edge'
        handles = [face for face in door.data.polygons if colour(door, face) == 'chrome'
                   and face.center.y < -.2 and face.center.x*direction > .85]
        assert handles and all(face.center.y < hinge.y-.5 for face in handles), \
            f'{side} exterior door handle must stay aft of the front hinge'
    print('PASS driver-side steering wheel, front-edge door hinges and aft door handles')

    def tree(obj, transform=Matrix.Identity(4)):
        obj.data.calc_loop_triangles()
        return BVHTree.FromPolygons([transform@vertex.co for vertex in obj.data.vertices],
                                   [tuple(triangle.vertices) for triangle in obj.data.loop_triangles],
                                   all_triangles=True)

    fixed = {name: tree(bpy.data.objects['J73Mesh_'+name])
             for name in ('Body', 'Interior', 'DoorLeft', 'DoorRight')}
    wheel = bpy.data.objects['J73Mesh_Wheel']
    wheels = re.findall(r'wheel (\w+)\s*\{[^}]*offset\s*=\s*([^,]+)', vehicle_script)
    assert len(wheels) == 4, 'Need four native wheel placements'
    front_axle = [float(values.split()[2]) for name, values in wheels if name.startswith('Front')]
    rear_axle = [float(values.split()[2]) for name, values in wheels if name.startswith('Rear')]
    assert len(front_axle) == len(rear_axle) == 2, 'Need paired front and rear native axles'
    assert abs(front_axle[0]-front_axle[1])<.001 and abs(rear_axle[0]-rear_axle[1])<.001, \
        'Native axle wheel centres must agree left-to-right'
    axle_separation = sum(front_axle)/2-sum(rear_axle)/2
    assert abs(axle_separation-2.794)<.010, \
        f'Native axle separation {axle_separation:.5f}m differs from factory110in beyond10mm'
    print(f'PASS factory dimensions: saved Body length {body_length:.5f}m, width {body_width:.5f}m, native axle separation {axle_separation:.5f}m')
    for name, values in wheels:
        x, z, y = map(float, values.split())
        for angle in ((-.30, 0, .30) if name.startswith('Front') else (0,)):
            transform = Matrix.Translation(Vector((-x, y, z))) @ Matrix.Rotation(angle, 4, 'Z')
            placed_wheel = tree(wheel, transform)
            for part, obstacle in fixed.items():
                intersections = placed_wheel.overlap(obstacle)
                assert not intersections, f'{name} wheel intersects {part} at steering {angle:+.2f}, {len(intersections)} triangle pairs'
    print('PASS all four visible wheels clear body/cabin/doors at rest and front +/-0.30rad steering')


def check_cabin_sheets(interior, atlas, backs):
    """Identify intentional upholstery sheets independently of generator tags."""
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(interior.data)
    remaining = set(bm.verts)
    open_faces = set()
    while remaining:
        pending = [remaining.pop()]
        vertices = set(pending)
        while pending:
            vertex = pending.pop()
            for edge in vertex.link_edges:
                other = edge.other_vert(vertex)
                if other in remaining:
                    remaining.remove(other)
                    vertices.add(other)
                    pending.append(other)
        edges = {edge for vertex in vertices for edge in vertex.link_edges}
        if any(len(edge.link_faces) != 2 for edge in edges):
            open_faces.update(face.index for vertex in vertices for face in vertex.link_faces)
    bm.free()

    def colour(face):
        uv = interior.data.uv_layers.active.data[face.loop_start].uv
        slot = int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
        return atlas['colours'][slot % len(atlas['colours'])]

    sheets = [interior.data.polygons[index] for index in open_faces]
    # Read the actual curved cushion support, excluding coloured ribbon faces.
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    interior.data.calc_loop_triangles()
    base_ids={face.index for face in interior.data.polygons if colour(face)=='seat'}
    base=BVHTree.FromPolygons([v.co for v in interior.data.vertices],
         [tuple(t.vertices) for t in interior.data.loop_triangles if t.polygon_index in base_ids],
         all_triangles=True)
    cushion_ids={face.index for face in sheets if colour(face) in {'wine','pink','cream'}
                 and face.center.z<.05 and face.normal.z>.9}
    samples=0
    for triangle in interior.data.loop_triangles:
        if triangle.polygon_index not in cushion_ids:continue
        points=[interior.data.vertices[i].co for i in triangle.vertices]
        center=sum(points,Vector())/3
        for point in [center]+[p*.8+center*.2 for p in points]:
            hit,_,_,distance=base.ray_cast(point,Vector((0,0,-1)),.01)
            assert hit is not None and .00025<distance<.0025, \
                'Cushion ribbon is hidden, detached or unsupported by its actual curved padding'
            samples+=1
    assert samples>100, 'Missing curved cushion ribbon coverage'
    print(f'PASS curved cushion ribbons retain 0.25..2.5mm support over {samples} samples')
    white_ids={face.index for face in interior.data.polygons if colour(face)=='white'}
    ball=BVHTree.FromPolygons([v.co for v in interior.data.vertices],
         [tuple(t.vertices) for t in interior.data.loop_triangles if t.polygon_index in white_ids],
         all_triangles=True)
    marks=[face for face in sheets if colour(face)=='black'
           and abs(face.center.x+.035)<.02 and abs(face.center.y-.09)<.02
           and face.center.z>.085 and face.normal.z>.8]
    assert len(marks)>=20, 'White shifter ball needs a visible subdivided H marking'
    for face in marks:
        hit,_,_,distance=ball.ray_cast(face.center,Vector((0,0,-1)),.01)
        assert hit is not None and .00025<distance<.0025, \
            'Shifter marking is hidden by or detached from its rounded ball'
    print('PASS white spherical shifter and visible surface-following H marking')
    fabric = {'wine', 'pink', 'cream', 'black'}
    ribbon_count = 0
    back_samples=0
    for low, high in backs:
        ribbon = [face for face in sheets if colour(face) in fabric
                  and low.y-.005<=face.center.y<=high.y+.005
                  and face.center.z>low.z+.105
                  and all(low.x-.005 <= interior.data.vertices[index].co.x <= high.x+.005
                          and low.z-.005 <= interior.data.vertices[index].co.z <= high.z+.005
                          for index in face.vertices)]
        assert {'wine', 'pink', 'cream'} <= {colour(face) for face in ribbon}, \
            f'Backrest at {tuple(low)} lacks the three Cardin ribbon colours'
        assert all(face.normal.y>.8 for face in ribbon), \
            f'Open seat-back ribbon must face cabin-forward +Y near {tuple(low)}'
        light_points = [interior.data.vertices[index].co for face in ribbon
                        if colour(face)=='cream' for index in face.vertices]
        center_x = (low.x+high.x)/2
        assert max(point.z for point in light_points)-min(point.z for point in light_points)>.25, \
            'Seat-back U ribbon must extend vertically, not just form horizontal bars'
        for side in (-1, 1):
            assert any((point.x-center_x)*side>.07 and point.z>high.z-.08 for point in light_points), \
                'Seat-back U ribbon must reach both upper sides of its backrest'
        ribbon_ids={face.index for face in ribbon}
        for triangle in interior.data.loop_triangles:
            if triangle.polygon_index not in ribbon_ids:continue
            points=[interior.data.vertices[i].co for i in triangle.vertices]
            center=sum(points,Vector())/3
            for point in [center]+[p*.8+center*.2 for p in points]:
                hit,support_normal,_,distance=base.ray_cast(point,Vector((0,-1,0)),.01)
                assert hit is not None and .00025<distance<.0025, \
                    'Backrest ribbon is hidden, detached or unsupported by actual padding'
                assert interior.data.polygons[triangle.polygon_index].normal.dot(support_normal)>.99, (
                    'Backrest ribbon facing must follow its actual curved padding')
                back_samples+=1
        ribbon_count += len(ribbon)
    print(f'PASS curved backrest ribbons retain0.25..2.5mm support over {back_samples} samples')
    headliner = [face for face in sheets
                 if all(interior.data.vertices[index].co.z>.45 for index in face.vertices)]
    assert headliner and {'seat', 'wine', 'pink', 'cream'} <= {colour(face) for face in headliner}, \
        'Open cabin headliner must include its fabric base and Cardin ribbons'
    assert sum(face.area for face in headliner if colour(face)=='seat')>.5, \
        'Headliner fabric base must span the cabin roof'
    assert all(face.normal.z<-.8 for face in headliner), \
        'Open headliner base and ribbons must face downward into the cabin'
    check_headliner_clearance(interior.data, headliner, colour)
    print(f'PASS three forward-facing Cardin backrest borders ({ribbon_count} faces) and downward open headliner ({len(headliner)} faces)')


def check_headliner_clearance(mesh, headliner, colour):
    """Sample actual coloured sheets against only their underlying roof fabric."""
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree

    mesh.calc_loop_triangles()
    base_ids = {face.index for face in headliner if colour(face) == 'seat'}
    ribbon_ids = {face.index for face in headliner if colour(face) != 'seat'}
    base = BVHTree.FromPolygons(
        [vertex.co for vertex in mesh.vertices],
        [tuple(triangle.vertices) for triangle in mesh.loop_triangles
         if triangle.polygon_index in base_ids], all_triangles=True)
    direction = Vector((0, 0, 1))
    gaps = []
    for triangle in mesh.loop_triangles:
        if triangle.polygon_index not in ribbon_ids:
            continue
        points = [mesh.vertices[index].co for index in triangle.vertices]
        # Triangle centres and near-corner samples expose coarse-base clipping
        # without depending on a particular strip/grid tessellation.
        for weights in ((1/3, 1/3, 1/3), (.8, .1, .1), (.1, .8, .1), (.1, .1, .8)):
            sample = sum((point*weight for point, weight in zip(points, weights)), Vector())
            hit, _, _, distance = base.ray_cast(sample-direction*.02, direction, .04)
            assert hit is not None, \
                f'Headliner ribbon face {triangle.polygon_index} lacks fabric directly above it'
            gap = distance-.02
            assert .00025 <= gap <= .0025, \
                f'Headliner ribbon face {triangle.polygon_index} clearance {gap*1000:.3f}mm: must stay cabin-side of fabric within0.25..2.5mm'
            gaps.append(gap)
    assert gaps, 'Need sampled coloured headliner ribbon triangles'
    print(f'PASS headliner cabin-side ray clearance: {len(gaps)} samples, {min(gaps)*1000:.3f}..{max(gaps)*1000:.3f}mm')
