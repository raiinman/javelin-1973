"""Pass 2: rebuild each Fan_Blade_n mesh in place (same object, transform, origin, planform and pitch)."""
import bpy, bmesh, sys, math, json
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
src, dst, log = a[0], a[1], a[2]
bpy.ops.wm.open_mainfile(filepath=src, load_ui=False, use_scripts=False)

def catmull(pts, per):
    out = []
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        for k in range(per):
            t = k / per
            out.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                             + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-1])
    return out

report = {}
for o in sorted([o for o in bpy.data.objects if o.name.startswith('Fan_Blade_')], key=lambda o: o.name):
    vs = [v.co.copy() for v in o.data.vertices]
    assert len(vs) == 20, (o.name, len(vs))
    # Original layout: stations 0..4, leading=even, trailing=odd, back face = +10.
    L = [(vs[2 * i] + vs[10 + 2 * i]) / 2 for i in range(5)]
    T = [(vs[2 * i + 1] + vs[11 + 2 * i]) / 2 for i in range(5)]
    half = (vs[10] - vs[0]).length / 2
    Ls, Ts = catmull(L, 2), catmull(T, 2)
    ns = len(Ls)
    # Soften the tip: the last station narrows toward its chord midpoint.
    for k, f in ((ns - 1, .55), (ns - 2, .90)):
        mid = (Ls[k] + Ts[k]) / 2
        Ls[k], Ts[k] = mid + (Ls[k] - mid) * f, mid + (Ts[k] - mid) * f
    nc = 4
    top, bot = [], []
    for i in range(ns):
        span = (Ls[min(i + 1, ns - 1)] - Ls[max(i - 1, 0)]).normalized()
        chord = Ts[i] - Ls[i]
        n = chord.normalized().cross(span).normalized()
        if n.dot(vs[10] - vs[0]) < 0:
            n = -n
        rt, rb = [], []
        for j in range(nc + 1):
            t = j / nc
            camber = .0035 * math.sin(math.pi * t) * chord.length / .05
            p = Ls[i] + chord * t - n * camber
            rt.append(p + n * half)
            rb.append(p - n * half)
        top.append(rt)
        bot.append(rb)
    bm = bmesh.new()
    T_ = [[bm.verts.new(p) for p in r] for r in top]
    B_ = [[bm.verts.new(p) for p in r] for r in bot]
    for i in range(ns - 1):
        for j in range(nc):
            bm.faces.new([T_[i][j], T_[i][j + 1], T_[i + 1][j + 1], T_[i + 1][j]])
            bm.faces.new([B_[i][j], B_[i + 1][j], B_[i + 1][j + 1], B_[i][j + 1]])
    for i in range(ns - 1):  # leading and trailing edge walls
        bm.faces.new([T_[i][0], T_[i + 1][0], B_[i + 1][0], B_[i][0]])
        bm.faces.new([T_[i][nc], B_[i][nc], B_[i + 1][nc], T_[i + 1][nc]])
    for i in (0, ns - 1):  # root and tip walls
        for j in range(nc):
            f = [T_[i][j], B_[i][j], B_[i][j + 1], T_[i][j + 1]]
            bm.faces.new(f if i == 0 else list(reversed(f)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = o.data
    mats = list(me.materials)
    bm.to_mesh(me)
    bm.free()
    me.materials.clear()
    for m in mats:
        me.materials.append(m)
    me.shade_smooth()
    me.set_sharp_from_angle(angle=math.radians(30))
    report[o.name] = dict(old_vertices=20, new_vertices=len(me.vertices), new_faces=len(me.polygons))
bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True)
json.dump(report, open(log, 'w'), indent=1)
print('saved', dst, report)
