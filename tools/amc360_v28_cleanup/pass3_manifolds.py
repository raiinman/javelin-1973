"""Pass 3: rebuild ExhaustManifold_{Left,Right}_CompleteCast mesh data in place as a clean cast log
manifold. Same objects, transforms, parents, materials; outlet ends on the existing OutletThroat."""
import bpy, bmesh, sys, math, json
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
src, dst, log = a[0], a[1], a[2]
bpy.ops.wm.open_mainfile(filepath=src, load_ui=False, use_scripts=False)
dg = bpy.context.evaluated_depsgraph_get()

def world_bvh(o):
    ev = o.evaluated_get(dg); me = ev.to_mesh()
    bm = bmesh.new(); bm.from_mesh(me); bm.transform(o.matrix_world); ev.to_mesh_clear()
    t = BVHTree.FromBMesh(bm); bm.free(); return t

def catmull(pts, per):
    out = []
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        for k in range(per):
            t = k / per
            out.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                             + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-1]); return out

def sweep(bm, path, radius, segs=12, scales=None, cap0=True, cap1=True, ovals=(1, 1)):
    path = [Vector(p) for p in path]; n = len(path)
    tans = [(path[min(i + 1, n - 1)] - path[max(i - 1, 0)]).normalized() for i in range(n)]
    ref = Vector((0, 0, 1)) if abs(tans[0].z) < .9 else Vector((1, 0, 0))
    nrm = (ref - tans[0] * ref.dot(tans[0])).normalized(); rings = []
    for i in range(n):
        if i: nrm = (nrm - tans[i] * nrm.dot(tans[i])).normalized()
        b = tans[i].cross(nrm); k = (scales[i] if scales else 1) * radius
        rings.append([bm.verts.new(path[i] + (nrm * math.cos(2 * math.pi * j / segs) * ovals[0]
                                               + b * math.sin(2 * math.pi * j / segs) * ovals[1]) * k)
                      for j in range(segs)])
    for r0, r1 in zip(rings, rings[1:]):
        for j in range(segs):
            bm.faces.new([r0[j], r0[(j + 1) % segs], r1[(j + 1) % segs], r1[j]])
    if cap0: bm.faces.new(list(reversed(rings[0])))
    if cap1: bm.faces.new(rings[-1])

def lathe(bm, prof, segs, origin, axis):
    z = Vector(axis).normalized(); h = Vector((1, 0, 0)) if abs(z.x) < .9 else Vector((0, 1, 0))
    x = h.cross(z).normalized(); y = z.cross(x); rings = []
    for r, hh in prof:
        c = Vector(origin) + z * hh
        rings.append([bm.verts.new(c)] if r < 1e-6 else
                     [bm.verts.new(c + (x * math.cos(2 * math.pi * j / segs) + y * math.sin(2 * math.pi * j / segs)) * r) for j in range(segs)])
    for a_, b_ in zip(rings, rings[1:]):
        if len(a_) == 1 or len(b_) == 1:
            pole, ring = (a_[0], b_) if len(a_) == 1 else (b_[0], a_)
            for j in range(segs):
                bm.faces.new([pole, ring[j], ring[(j + 1) % segs]] if len(a_) == 1 else [ring[j], ring[(j + 1) % segs], pole])
        else:
            for j in range(segs):
                bm.faces.new([a_[j], a_[(j + 1) % segs], b_[(j + 1) % segs], b_[j]])

def pad(bm, centre, normal, w=.048, h=.044, t=.011, r=.010):
    n = normal.normalized(); up = Vector((0, 0, 1)); u = (up - n * up.dot(n)).normalized(); v = n.cross(u)
    ring = []
    for cx, cz, a0 in ((w / 2 - r, h / 2 - r, 0), (-(w / 2 - r), h / 2 - r, 90), (-(w / 2 - r), -(h / 2 - r), 180), (w / 2 - r, -(h / 2 - r), 270)):
        for k in range(4):
            ang = math.radians(a0 + 90 * k / 3)
            ring.append((cx + r * math.cos(ang), cz + r * math.sin(ang)))
    back = [bm.verts.new(centre - n * .002 + v * px + u * pz) for px, pz in ring]
    front = [bm.verts.new(centre + n * t + v * px * .94 + u * pz * .94) for px, pz in ring]
    m = len(ring)
    for j in range(m):
        bm.faces.new([back[j], back[(j + 1) % m], front[(j + 1) % m], front[j]])
    bm.faces.new(list(reversed(back))); bm.faces.new(front)

report = {}
for side, name in ((1, 'Right'), (-1, 'Left')):
    o = bpy.data.objects[f'ExhaustManifold_{name}_CompleteCast']
    throat = bpy.data.objects[f'ExhaustManifold_{name}_OutletThroat']
    head = bpy.data.objects[f'CylinderHead_{name}']
    hb = world_bvh(head)
    # Port centres from the original pad clusters (vertices touching the head face).
    W = [o.matrix_world @ v.co for v in o.data.vertices]
    xmin = min(abs(p.x) for p in W)
    near = sorted([p for p in W if abs(p.x) < xmin + .010], key=lambda p: p.y)
    groups = []
    for p in near:
        if groups and p.y - groups[-1][-1].y < .06: groups[-1].append(p)
        else: groups.append([p])
    ports = [sum(g, Vector()) / len(g) for g in groups]
    assert len(ports) == 4, len(ports)
    seats = []
    for pc in ports:
        hit = hb.ray_cast(Vector((side * .6, pc.y, pc.z)), Vector((-side, 0, 0)))
        loc, nrm = hit[0], hit[1]
        if nrm.x * side < 0: nrm = -nrm
        seats.append((loc, nrm))
    tc = sum((throat.matrix_world @ v.co for v in throat.data.vertices), Vector()) / len(throat.data.vertices)
    x_log = side * .338
    z_log = .068
    # Stay clear of accessories ahead of the bank (the passenger alternator), measured from the model.
    ylim = 9.0
    for q in bpy.data.objects:
        if q.type == 'MESH' and q.name.startswith('Alternator_'):
            ev = q.evaluated_get(dg); qm = ev.to_mesh()
            for v in qm.vertices:
                w = q.matrix_world @ v.co
                if w.x * side > .20 and -.05 < w.z < .16:
                    ylim = min(ylim, w.y)
            ev.to_mesh_clear()
    LEAN = .035   # every primary sweeps rearward toward the outlet by the same amount
    y_front = min(max(p.y for p in ports) - LEAN + .024, ylim - .034)
    y_end = tc.y - .034
    parts, pads = [], bmesh.new()
    def part():
        b = bmesh.new(); parts.append(b); return b
    # Log runner: grows toward the outlet, slightly oval, closed domed ends.
    lp = [Vector((x_log, y_front - (y_front - y_end) * k / 14, z_log - .006 * k / 14)) for k in range(15)]
    sweep(part(), lp, .025, 14, scales=[.92 + .26 * k / 14 for k in range(15)], ovals=(1.0, 1.12))
    for end, prev, g in ((lp[0], lp[1], .92), (lp[-1], lp[-2], 1.18)):
        d = (end - prev).normalized()
        lathe(part(), [(0, -.004), (.025 * g, -.004), (.025 * g, .004), (.021 * g, .014), (.011 * g, .021), (0, .023 * g)], 14, end, d)
    # Primaries: pad, short outward run, then a smooth rearward bend landing on the log body.
    for (loc, nrm), pc in zip(seats, ports):
        pad(pads, loc, nrm)
        path = catmull([loc + nrm * .006, loc + nrm * .026 + Vector((0, 0, -.004)),
                        Vector((x_log - side * .010, pc.y - .015, z_log + .040)),
                        Vector((x_log, pc.y - LEAN, z_log + .004))], 4)
        n = len(path)
        sweep(part(), path, .019, 12, scales=[1 + .38 * (i / (n - 1)) ** 2 for i in range(n)], ovals=(1.0, 1.15))
    # Outlet leaves the underside of the log and drops onto the existing throat.
    out_top = tc + Vector((0, 0, .013))
    elbow = catmull([Vector((x_log, tc.y, z_log + .004)), Vector((x_log, tc.y, z_log - .030)),
                     Vector(((x_log + tc.x) / 2, tc.y, z_log - .085)), out_top + Vector((0, 0, .030)), out_top], 4)
    sweep(part(), elbow, .030, 14, scales=[1.0 + .10 * i / (len(elbow) - 1) for i in range(len(elbow))])
    # Flange ring; the capped elbow end sits 12.5 mm up inside it, leaving an open bore.
    lathe(part(), [(.0335, .0), (.048, .0), (.048, -.0125), (.0335, -.0125), (.0335, .0)], 16, out_top, Vector((0, 0, 1)))
    # Fuse everything into one cast shell with exact boolean unions.
    temps = []
    for k, b in enumerate(parts):
        bmesh.ops.remove_doubles(b, verts=b.verts, dist=1e-6)
        bmesh.ops.recalc_face_normals(b, faces=b.faces)
        me_t = bpy.data.meshes.new(f'_tmp{k}'); b.to_mesh(me_t); b.free()
        ob_t = bpy.data.objects.new(f'_tmp{k}', me_t); bpy.context.scene.collection.objects.link(ob_t); temps.append(ob_t)
    base = temps[0]
    for ob_t in temps[1:]:
        md = base.modifiers.new('u', 'BOOLEAN'); md.operation = 'UNION'; md.solver = 'EXACT'; md.object = ob_t
        ob_t.hide_set(True)
    dgu = bpy.context.evaluated_depsgraph_get()
    ev = base.evaluated_get(dgu); fused = ev.to_mesh()
    bm = bmesh.new(); bm.from_mesh(fused); ev.to_mesh_clear()
    for ob_t in temps:
        m_ = ob_t.data; bpy.data.objects.remove(ob_t); bpy.data.meshes.remove(m_)
    # Cast fillets at the primary/log and elbow/log junctions (not at pads or flange).
    bmesh.ops.dissolve_degenerate(bm, dist=1e-6, edges=bm.edges)
    seam = []
    for e in bm.edges:
        if len(e.link_faces) != 2:
            continue
        mid = (e.verts[0].co + e.verts[1].co) / 2
        if abs(mid.x) < .303 or mid.z < tc.z + .024:
            continue
        if e.calc_face_angle(0) > math.radians(32):
            seam.append(e)
    if seam:
        bmesh.ops.bevel(bm, geom=seam, offset=.0045, segments=2, profile=.5, affect='EDGES', clamp_overlap=True)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # Port pads stay separate seated shells on the head face (a crisp cast seam to each primary).
    bmesh.ops.recalc_face_normals(pads, faces=pads.faces)
    tmp = bpy.data.meshes.new('_pads'); pads.to_mesh(tmp); pads.free(); bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)
    inv = o.matrix_world.inverted(); bm.transform(inv)
    me = o.data; mats = list(me.materials)
    bm.to_mesh(me); bm.free()
    me.materials.clear()
    for m in mats: me.materials.append(m)
    me.shade_smooth(); me.set_sharp_from_angle(angle=math.radians(55))
    report[o.name] = dict(fillet_edges=len(seam), accessory_limit_y=round(ylim, 4) if ylim < 9 else None, ports=[[round(c, 4) for c in s[0]] for s in seats], log_x=x_log, outlet=[round(c, 4) for c in tc],
                          vertices=len(me.vertices), faces=len(me.polygons))
bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True)
json.dump(report, open(log, 'w'), indent=1)
print('saved', json.dumps(report))
