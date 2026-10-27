"""Evaluate the original Blender rig without rendering or saving the source."""
import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_surface_orientation(atlas):
    """Audit all original meshes, without treating intentional open sheets as solids."""
    import bpy
    import bmesh
    import math
    meshes = [obj for obj in bpy.data.objects if obj.name.startswith('J73Mesh_')]
    assert len(meshes) == 11, 'Surface audit requires all eleven vehicle meshes'
    solids = 0
    for obj in meshes:
        assert obj.matrix_world.determinant() > 0, f'{obj.name} has a mirrored object basis'
        assert all(math.isfinite(value) for vertex in obj.data.vertices for value in vertex.co)
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        remaining = set(bm.verts)
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
            if not all(len(edge.link_faces) == 2 for edge in edges):
                continue
            assert all(edge.is_contiguous for edge in edges), f'{obj.name} solid has inconsistent face winding'
            faces = {face for vertex in vertices for face in vertex.link_faces}
            volume = 0
            for face in faces:
                points = [vertex.co for vertex in face.verts]
                for index in range(1, len(points)-1):
                    volume += points[0].dot(points[index].cross(points[index+1]))/6
            assert volume > -1e-8, f'{obj.name} contains an inside-out closed component'
            solids += 1
        bm.free()
    body=bpy.data.objects['J73Mesh_Body']
    for side in (-1,1):
        for y in (-1.70,-1.50,-1.30,-1.10):
            for z in (.78,.84,.90):
                hit,point,normal,index=body.ray_cast((side*2,y,z-.65),(-side,0,0))
                assert hit and normal.x*side>0, f'Rear shoulder culls inward at {side,y,z}'
    print('PASS both rear shoulders face outward at 24 saved-surface ray samples')
    for side,suffix in ((-1,'Left'),(1,'Right')):
        door=bpy.data.objects['J73Mesh_Door'+suffix]
        faces=[]
        for face in door.data.polygons:
            uv=door.data.uv_layers.active.data[face.loop_start].uv
            slot=int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
            if atlas['colours'][slot%len(atlas['colours'])]=='silverLight' and abs(face.center.x)>.90 and face.center.z>.29:
                faces.append(face)
        assert len(faces)==48, f'{suffix} mirror requires its complete round reflective disk'
        assert all(face.normal.y<-.97 and face.normal.x*side<-.17 for face in faces), \
            f'{suffix} mirror must face rearward and slightly inward, not sideways or forward'
    print('PASS both round mirror disks face aft/inward on their moving doors')
    for side, direction in (('Left', -1), ('Right', 1)):
        door = bpy.data.objects['J73Mesh_Door'+side]
        def painted(face):
            uv = door.data.uv_layers.active.data[face.loop_start].uv
            slot = int(uv.x*atlas['columns']) + int(uv.y*atlas['rows'])*atlas['columns']
            return atlas['colours'][slot%len(atlas['colours'])] == 'red'
        # The upper return becomes larger than individual skin cells after
        # refinement. Select the exposed vertical skin spatially, not by area.
        exterior=[face for face in door.data.polygons if painted(face)
                  and abs(face.center.x)>.86 and face.center.z<.15
                  and -.434<face.center.y<.784]
        assert sum(face.area for face in exterior)>.4, f'{side} door skin coverage missing'
        assert all(face.normal.x*direction>.8 for face in exterior), f'{side} door skin faces inward'
    hood_obj=bpy.data.objects['J73Mesh_Hood']
    def hood_colour(face):
        uv=hood_obj.data.uv_layers.active.data[face.loop_start].uv
        slot=int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
        return atlas['colours'][slot%len(atlas['colours'])]
    hood_tops=[face for face in hood_obj.data.polygons if hood_colour(face)=='red']
    assert hood_tops and all(face.normal.z>.8 for face in hood_tops), \
        'Every painted hood top triangle must face upward'
    body = bpy.data.objects['J73Mesh_Body']
    for zone, direction, side in (('headleft',1,-1), ('headright',1,1),
                                  ('tailleft',-1,-1), ('tailright',-1,1),
                                  ('brakeleft',-1,-1), ('brakeright',-1,1)):
        faces = []
        for face in body.data.polygons:
            uv = body.data.uv_layers.active.data[face.loop_start].uv
            slot = int(uv.x*atlas['columns']) + int(uv.y*atlas['rows'])*atlas['columns']
            if atlas['zones'][slot//len(atlas['colours'])] == zone:
                faces.append(face)
        assert faces and all(face.center.y*direction > 2 and face.center.x*side > .2 for face in faces), \
            f'{zone} semantic lamp mask is on the wrong end or side'
        assert any(face.normal.y*direction > .9 for face in faces), f'{zone} lacks an outward lamp face'
    wheel = bpy.data.objects['J73Mesh_Wheel']
    for x in (-.67,-.43,.43,.67):
        hit,lens,_,index=body.ray_cast((x,-3,.720-.65),(0,1,0))
        paint_hit,paint,_,_=body.ray_cast((x,-3,.825-.65),(0,1,0))
        assert hit and paint_hit, 'Rear lamp or surrounding fascia is missing'
        face=body.data.polygons[index]
        uv=body.data.uv_layers.active.data[face.loop_start].uv
        slot=int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
        assert atlas['colours'][slot%len(atlas['colours'])] in {'tail','cream','brakeRed'}, \
            'Rear fascia occludes a recessed lens'
        assert .015<lens.y-paint.y<.045, 'Rear lens must sit inside the painted fascia aperture'
    print('PASS four rear lens rays enter real fascia apertures with 15..45mm recess')
    spans = [max(vertex.co[i] for vertex in wheel.data.vertices)-min(vertex.co[i] for vertex in wheel.data.vertices)
             for i in range(3)]
    assert spans[0] < spans[1]*.6 and abs(spans[1]-spans[2]) < .01, 'Wheel axle must follow X'
    assert abs(spans[1]/2-.33)<.015, 'Visible wheel radius must agree with the physical tire radius'
    print(f'PASS eleven mesh bases, {solids} closed component windings, exterior door/hood normals, six lamp zones and wheel axle/radius')


def check_pose(blend):
    import bpy
    from mathutils import Vector
    bpy.ops.wm.open_mainfile(filepath=str(blend.resolve()))
    rig = bpy.data.objects['J73_Skeleton']
    expected = {'J73_Panels', 'J73_WindowLeft', 'J73_WindowRight'}
    missing = expected - set(bpy.data.actions.keys())
    assert not missing, f'Saved original source is missing actions: {sorted(missing)}'
    trunk_mesh=bpy.data.objects['J73Mesh_Trunk'].data
    trunk_tops=[face for face in trunk_mesh.polygons
                if -2.14<face.center.y<-1.90 and .24<face.center.z<.31 and face.normal.z>0]
    assert len(trunk_tops)>=300 and all(face.normal.z>.9 for face in trunk_tops), \
        'Crowned trunk top must face upward for native backface culling'
    print('PASS trunk top faces outward for native backface culling')
    # Check every glass surface against its outward/upward viewing direction.
    # The revised fastback angle has a smaller Y component than the old glass.
    for name,outward in (('WindowLeft',(-1,0,.35)),('WindowRight',(1,0,.35)),
                         ('Windshield',(0,.6,.8)),('RearGlass',(0,-.35,.94))):
        direction=Vector(outward).normalized()
        sheets=[f for f in bpy.data.objects['J73Mesh_'+name].data.polygons
                if f.area>(1e-8 if name=='RearGlass' else .01)]
        assert sheets and all(f.normal.dot(direction)>.75 for f in sheets), \
            f'{name} glass must face outward for native culling'
    print('PASS four exterior glass sheet normals face outward')
    atlas = json.loads((blend.parent/'atlas-manifest.json').read_text())
    body_mesh=bpy.data.objects['J73Mesh_Body'].data
    def apron_paint(face):
        uv=body_mesh.uv_layers.active.data[face.loop_start].uv
        slot=int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
        return atlas['colours'][slot%len(atlas['colours'])]=='red'
    apron=[face for face in body_mesh.polygons
           if -1.72<face.center.y<-1.64 and face.center.z>.2
           and face.area>.00005 and face.normal.z>.7 and apron_paint(face)]
    assert len(apron)>=6, 'Curved backlight apron requires six outward top strips'
    edge_points=[body_mesh.vertices[i].co for face in apron for i in face.vertices]
    glass_mesh=bpy.data.objects['J73Mesh_RearGlass'].data
    glass_bottom=[v.co for v in glass_mesh.vertices if abs(v.co.y+1.64)<.0001]
    assert len(glass_bottom)>=7, 'Backlight requires seven lower-edge columns'
    assert all(min((point-edge).length for edge in edge_points)<.0001
               for point in glass_bottom), 'Painted apron must meet every lower-glass column'
    print('PASS outward backlight apron meets all seven curved lower-glass columns')
    body = bpy.data.objects['J73Mesh_Body']
    check_surface_orientation(atlas)
    sys.path.insert(0, str(ROOT/'tools'))
    from check_rear_corners import check_rear_corner_closure
    check_rear_corner_closure(atlas)
    from check_rear_haunch import check_rear_haunch_joins
    check_rear_haunch_joins(atlas)
    from check_door_crests import check_door_crests
    check_door_crests(atlas)
    from check_pedals import check_saved_pedals
    check_saved_pedals()
    from check_roof_hardware import check_saved_roof_hardware
    check_saved_roof_hardware(atlas)
    from check_front_nose_terminal import check_front_nose_terminal
    check_front_nose_terminal(atlas)
    from check_vehicle_placement import check_placement
    check_placement(atlas, (ROOT/'Javelin73PC/42/media/scripts/vehicle_Javelin73PC.txt').read_text())
    glass_index = atlas['colours'].index('glass')
    quarter_vertices = []
    for face in body.data.polygons:
        uv = body.data.uv_layers.active.data[face.loop_start].uv
        slot = int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
        if slot % len(atlas['colours']) == glass_index:
            quarter_vertices.extend(body.data.vertices[index].co for index in face.vertices)
    body_vertices = [vertex.co for vertex in body.data.vertices]
    from mathutils.bvhtree import BVHTree
    body_surface = BVHTree.FromPolygons(body_vertices, [tuple(face.vertices) for face in body.data.polygons])
    for direction in (-1,1):
        tip=min((point for point in quarter_vertices if point.x*direction>0),key=lambda point:point.y)
        indices={vertex.index for vertex in body.data.vertices if (vertex.co-tip).length<.0001}
        connected=sum(bool(indices.intersection(face.vertices)) for face in body.data.polygons)
        assert connected>=4, 'Quarter-glass aft tip must share the adjoining sail surfaces'
    rear_corners=[v.co for v in trunk_mesh.vertices if abs(abs(v.co.x)-.82)<.0001
                  and abs(v.co.y+2.18092)<.0001 and abs(v.co.z-.240)<.0001]
    assert len(rear_corners)==2, 'Both rear lid seam anchors must remain present'
    for point in rear_corners:
        distance=min((point-vertex).length for vertex in body_vertices)
        assert distance<.010, f'Trunk rear/fixed-body closure gap {distance:.4f}m exceeds10mm'
    print('PASS quarter-glass aft tips share sail surfaces and trunk rear joins fixed body within10mm')
    for side in ('Left','Right'):
        window = bpy.data.objects['J73Mesh_Window'+side]
        face = max(window.data.polygons,key=lambda polygon: polygon.area)
        corners = sorted((window.data.vertices[index].co for index in face.vertices),key=lambda point:point.z)
        door_vertices = [vertex.co for vertex in bpy.data.objects['J73Mesh_Door'+side].data.vertices]
        for point in corners[:2]:
            distance = min((point-vertex).length for vertex in door_vertices)
            assert distance < .020, f'{side} glass/door beltline gap {distance:.4f}m exceeds20mm'
        for point in corners:
            # A trim edge can pass through a face between its vertices. Measure
            # the actual surface gap, independent of frame tessellation.
            distance = body_surface.find_nearest(point)[3]
            assert distance < .020, f'{side} glass/aperture frame gap {distance:.4f}m exceeds20mm'
        for pair in (corners[:2],corners[2:]):
            rear_corner = min(pair,key=lambda point:point.y)
            distance = min((rear_corner-vertex).length for vertex in quarter_vertices)
            assert distance < .025, f'{side} main/quarter glass junction {distance:.4f}m exceeds25mm'
    print('PASS closed glass/door/frame junctions within20mm, quarter-glass divider within25mm')
    names = ('Hood', 'Trunk', 'DoorLeft', 'DoorRight', 'WindowLeft', 'WindowRight', 'Interior')

    def pose(clip, frame):
        rig.animation_data.action = bpy.data.actions[clip]
        suitable = rig.animation_data.action_suitable_slots
        if suitable:
            rig.animation_data.action_slot = suitable[0]
        bpy.context.scene.frame_set(frame)
        bpy.context.view_layer.update()
        graph = bpy.context.evaluated_depsgraph_get()
        result = {}
        for name in names:
            obj = bpy.data.objects['J73Mesh_' + name].evaluated_get(graph)
            vertices = obj.data.vertices
            result[name] = sum((obj.matrix_world @ vertex.co for vertex in vertices), Vector()) / len(vertices)
        return result

    closed = pose('J73_Panels', 1)
    panels = pose('J73_Panels', 31)
    for name in ('Hood', 'Trunk'):
        rise = panels[name].z - closed[name].z
        assert rise > .10, f'{name} must open upward, centroid rise={rise:.5f}'
        print(f'PASS {name} centroid rises {rise:.4f} metres')
    left = panels['DoorLeft'] - closed['DoorLeft']
    right = panels['DoorRight'] - closed['DoorRight']
    assert left.x < -.15 and right.x > .15, f'Doors must swing outward: {left.x}, {right.x}'
    assert abs(left.x + right.x) < .015, 'Door movement must mirror left to right'
    print(f'PASS doors swing outward left={left.x:.4f}, right={right.x:.4f} metres')
    for name in ('WindowLeft', 'WindowRight'):
        movement = panels[name] - closed[name]
        assert movement.xy.length > .15 and abs(movement.z) < .005, f'{name} must follow door swing'
    assert (panels['Interior'] - closed['Interior']).length < .0001, 'Interior must stay fixed'
    for side, other in (('Left', 'Right'), ('Right', 'Left')):
        first = pose('J73_Window' + side, 1)
        last = pose('J73_Window' + side, 31)
        window = 'Window' + side
        delta = last[window] - first[window]
        assert abs(delta.z + .45) < .005 and delta.xy.length < .005, f'{window} must lower vertically .45m, got {delta}'
        for fixed in ('Window' + other, 'DoorLeft', 'DoorRight', 'Hood', 'Trunk', 'Interior'):
            assert (last[fixed] - first[fixed]).length < .0001, f'{window} action moves unrelated {fixed}'
        print(f'PASS {window} lowers {delta.z:.4f} metres independently')
    from check_vehicle_placement import check_panel_clearance
    check_panel_clearance()
    print('PASS: evaluated Blender geometry poses; game animation playback remains separate')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blend', type=Path, default=ROOT / 'assets' / 'Javelin73PC.blend')
    parser.add_argument('--blender', type=Path, default=Path('C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'))
    in_blender = importlib.util.find_spec('bpy') is not None
    argv = sys.argv[sys.argv.index('--') + 1:] if in_blender and '--' in sys.argv else (sys.argv[1:] if not in_blender else [])
    args = parser.parse_args(argv)
    if in_blender:
        check_pose(args.blend)
        return 0
    if not args.blender.is_file() or not args.blend.is_file():
        parser.error('Requires Blender and the generated original source blend file')
    return subprocess.run([str(args.blender), '--background', '--factory-startup', '--python-exit-code', '1',
                           '--python', str(Path(__file__).resolve()), '--', '--blend', str(args.blend.resolve())]).returncode


if __name__ == '__main__':
    raise SystemExit(main())
