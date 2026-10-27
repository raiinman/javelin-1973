"""Original AMC 360-style V8 exterior engine for the Javelin project.

Deterministic, fully procedural. No imported meshes, textures, fonts or logos.
Engine frame: metres, +Y forward, +Z up, driver side -X, origin on the crank
axis at the block front face. ENG_Root carries the car fit transform.

Run with Blender 5.2 (or the matching bpy module):
  blender -b --factory-startup --python tools/amc360_engine.py -- --out OUT.blend
"""
import argparse
import math
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

S45 = math.sqrt(.5)
DECK = .234            # crank axis to deck, along the bank axis (9.21 in tall deck)
BORE_PITCH = .12065    # 4.75 in bore spacing
BANK_OFFSET = .022     # driver bank sits forward of the passenger bank
HEAD_H = .098          # head deck to valve-cover rail
HEAD_HALF = .100
BLOCK_REAR = -.575
CYL_Y = {-1: [-.075 - i * BORE_PITCH for i in range(4)],
         1: [-.075 - BANK_OFFSET - i * BORE_PITCH for i in range(4)]}
HEAD_Y = {-1: (-.008, -.545), 1: (-.030, -.567)}
INTAKE_Y = (-.020, -.530)
CARB_Y = -.275
CARB_PAD_Z = .335
CLEANER_Z = .426
PUMP_C = (0.0, .190)
ALT_C = (.260, .300)
BELT_Y = .125

# Distributor: boss on the passenger-side timing cover, leaning out and slightly back.
DIST_BASE = Vector((.118, .035, .100))
DIST_AXIS = Vector((.25, -.15, .95)).normalized()

PAINT = {
    # Unverified colour choices; see docs/amc360-engine.md before matching the target.
    'ENG_Paint_Cast': ((.10, .25, .48), 0.0, .55),
    'ENG_Paint_Pressed': ((.11, .27, .52), 0.0, .35),
    'ENG_Black_Satin': ((.025, .025, .028), 0.0, .45),
    'ENG_Cast_Iron': ((.16, .15, .14), .6, .75),
    'ENG_Aluminium': ((.62, .62, .60), 1.0, .45),
    'ENG_Zinc_Plate': ((.72, .62, .38), 1.0, .35),
    'ENG_Rubber': ((.03, .03, .03), 0.0, .8),
    'ENG_Bakelite_Cap': ((.04, .035, .03), 0.0, .3),
    'ENG_Steel_Bright': ((.75, .75, .74), 1.0, .25),
    'ENG_Decal_Silver': ((.80, .80, .78), .6, .35),
}


def bank_point(side, u, v):
    """Bank frame: u along the cylinder axis from the crank, v toward the exhaust side."""
    x = side * (u + v) * S45
    z = (u - v) * S45
    return x, z


def bank_matrix(side, u0=0.0):
    """Local x = v (outward), y = engine Y, z = bank axis; origin at axis distance u0."""
    a = Vector((side * S45, 0, S45))
    n = Vector((side * S45, 0, -S45))
    m = Matrix.Identity(4)
    m.col[0][:3] = n
    m.col[1][:3] = (0, 1, 0)
    m.col[2][:3] = a
    m.col[3][:3] = a * u0
    return m


def axis_matrix(origin, axis, hint=Vector((0, 0, 1))):
    z = Vector(axis).normalized()
    if abs(z.dot(hint)) > .95:
        hint = Vector((1, 0, 0))
    x = hint.cross(z).normalized()
    y = z.cross(x)
    m = Matrix.Identity(4)
    m.col[0][:3] = x
    m.col[1][:3] = y
    m.col[2][:3] = z
    m.col[3][:3] = origin
    return m


class Part:
    def __init__(self, name, mats, pivot=(0, 0, 0)):
        self.name, self.mats, self.pivot = name, list(mats), Vector(pivot)
        self.bm = bmesh.new()

    def mi(self, mat):
        return self.mats.index(mat)

    def face(self, pts, mat, xf=None):
        vs = [self.bm.verts.new(xf @ Vector(p) if xf else Vector(p)) for p in pts]
        f = self.bm.faces.new(vs)
        f.material_index = self.mi(mat)
        return f

    def grid(self, rings, mat, closed=True, cap0=False, cap1=False, xf=None):
        """Connect equal-length point rings; ring entries may be a single pole point."""
        bm = self.bm
        vr = []
        for ring in rings:
            pts = [xf @ Vector(p) if xf else Vector(p) for p in ring]
            vr.append([bm.verts.new(p) for p in pts])
        idx = self.mi(mat)
        for a, b in zip(vr, vr[1:]):
            if len(a) == 1 or len(b) == 1:
                pole, ring = (a[0], b) if len(a) == 1 else (b[0], a)
                n = len(ring)
                for i in range(n if closed else n - 1):
                    j = (i + 1) % n
                    tri = [pole, ring[i], ring[j]] if len(a) == 1 else [ring[i], ring[j], pole]
                    bm.faces.new(tri).material_index = idx
                continue
            n = len(a)
            for i in range(n if closed else n - 1):
                j = (i + 1) % n
                bm.faces.new([a[i], a[j], b[j], b[i]]).material_index = idx
        if cap0 and len(vr[0]) > 2:
            bm.faces.new(list(reversed(vr[0]))).material_index = idx
        if cap1 and len(vr[-1]) > 2:
            bm.faces.new(vr[-1]).material_index = idx
        return vr

    def lathe(self, profile, segs, mat, xf, mats=None):
        """Profile of (radius, height) about local Z. Zero radius collapses to a pole.
        Open ends are capped. Optional per-span materials."""
        rings = []
        for r, h in profile:
            if r < 1e-6:
                rings.append([(0, 0, h)])
            else:
                rings.append([(r * math.cos(2 * math.pi * i / segs),
                               r * math.sin(2 * math.pi * i / segs), h) for i in range(segs)])
        if mats is None:
            self.grid(rings, mat, cap0=len(rings[0]) > 1, cap1=len(rings[-1]) > 1, xf=xf)
        else:
            for k in range(len(rings) - 1):
                self.grid(rings[k:k + 2], mats[k], cap0=(k == 0 and len(rings[0]) > 1),
                          cap1=(k == len(rings) - 2 and len(rings[-1]) > 1), xf=xf)

    def cyl(self, a, b, r, segs, mat, cap=True):
        a, b = Vector(a), Vector(b)
        xf = axis_matrix(a, b - a)
        h = (b - a).length
        self.lathe([(r, 0), (r, h)], segs, mat, xf)

    def rbox(self, center, size, radius, mat, xf=None, segs=2):
        bm = bmesh.new()
        res = bmesh.ops.create_cube(bm, size=1.0)
        for v in res['verts']:
            v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
        if radius > 0:
            bmesh.ops.bevel(bm, geom=list(bm.edges), offset=radius, segments=segs,
                            profile=.5, affect='EDGES', clamp_overlap=True)
        m = Matrix.Translation(center)
        if xf:
            m = xf @ m
        self.absorb(bm, mat, m)

    def extrude(self, poly, y0, y1, mat, bevel=0.0, xf=None):
        """Polygon in XZ extruded along Y (or the local Y of xf)."""
        bm = bmesh.new()
        f0 = bm.faces.new([bm.verts.new((x, y0, z)) for x, z in poly])
        f1 = bm.faces.new([bm.verts.new((x, y1, z)) for x, z in reversed(poly)])
        a, b = f0.verts, list(reversed(f1.verts))
        n = len(a)
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new([a[i], a[j], b[j], b[i]])
        if bevel > 0:
            cap_edges = [e for e in bm.edges if all(abs(v.co.y - y0) < 1e-7 for v in e.verts)
                         or all(abs(v.co.y - y1) < 1e-7 for v in e.verts)]
            bmesh.ops.bevel(bm, geom=cap_edges, offset=bevel, segments=2, profile=.5,
                            affect='EDGES', clamp_overlap=True)
        self.absorb(bm, mat, xf or Matrix.Identity(4))

    def sweep(self, path, section, mat, closed=False, cap=True):
        """Sweep a 2D section (in path normal/binormal) along points, parallel transport."""
        path = [Vector(p) for p in path]
        n = len(path)
        tans = []
        for i in range(n):
            if closed:
                t = path[(i + 1) % n] - path[i - 1]
            else:
                t = path[min(i + 1, n - 1)] - path[max(i - 1, 0)]
            tans.append(t.normalized())
        ref = Vector((0, 0, 1)) if abs(tans[0].z) < .9 else Vector((1, 0, 0))
        nrm = (ref - tans[0] * ref.dot(tans[0])).normalized()
        rings = []
        for i in range(n):
            if i:
                nrm = (nrm - tans[i] * nrm.dot(tans[i])).normalized()
            bin_ = tans[i].cross(nrm)
            rings.append([path[i] + nrm * sx + bin_ * sy for sx, sy in section])
        if closed:
            rings.append(rings[0])
            vr = self.grid(rings[:-1], mat, cap0=False, cap1=False)
            idx = self.mi(mat)
            a, b = vr[-1], vr[0]
            m = len(a)
            for i in range(m):
                j = (i + 1) % m
                self.bm.faces.new([a[i], a[j], b[j], b[i]]).material_index = idx
        else:
            self.grid(rings, mat, cap0=cap, cap1=cap)

    def absorb(self, bm, mat, xf):
        bm.transform(xf)
        me = bpy.data.meshes.new('tmp')
        bm.to_mesh(me)
        bm.free()
        start = len(self.bm.faces)
        self.bm.from_mesh(me)
        bpy.data.meshes.remove(me)
        self.bm.faces.ensure_lookup_table()
        for f in self.bm.faces[start:]:
            f.material_index = self.mi(mat)

    def build(self, parent, materials, recalc=True, sharp=math.radians(34)):
        bm = self.bm
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
        if recalc:
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.transform(Matrix.Translation(-self.pivot))
        me = bpy.data.meshes.new(self.name)
        bm.to_mesh(me)
        bm.free()
        for m in self.mats:
            me.materials.append(materials[m])
        me.shade_smooth()
        me.set_sharp_from_angle(angle=sharp)
        ob = bpy.data.objects.new(self.name, me)
        ob.location = self.pivot
        ob.parent = parent
        return ob


def catmull(points, per=8):
    pts = [Vector(p) for p in points]
    out = []
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        for k in range(per):
            t = k / per
            t2, t3 = t * t, t * t * t
            out.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                             + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(pts[-1])
    return out


def circle_section(r, n):
    return [(r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def rounded_rect(hl, hw, r, corner=4, side=0):
    """Plan ring (l, w), counter-clockwise, optional extra points along long sides."""
    pts = []
    centers = [(hl - r, hw - r, 0), (-(hl - r), hw - r, 90), (-(hl - r), -(hw - r), 180),
               (hl - r, -(hw - r), 270)]
    for k, (cx, cy, a0) in enumerate(centers):
        for i in range(corner + 1):
            a = math.radians(a0 + 90 * i / corner)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        if side and k in (0, 2):
            x0, x1 = (cx, -cx)
            y = hw if k == 0 else -hw
            for i in range(1, side + 1):
                pts.append((x0 + (x1 - x0) * i / (side + 1), y))
    return pts


# ---------------------------------------------------------------- components

def block_profile():
    right = [(0.0, -.018), (.180, -.018), (.180, -.004), (.165, -.004), (.165, .020),
             bank_point(1, DECK - .085, .0925), bank_point(1, DECK, .0925),
             bank_point(1, DECK, -.0925), bank_point(1, DECK - .075, -.0925)]
    left = [(-x, z) for x, z in reversed(right[1:])]
    return right + [(0.0, .165)] + left


def build_block(P):
    p = Part('ENG_Block', ['ENG_Paint_Cast'])
    prof = block_profile()
    # remove duplicate bottom-centre point produced by mirroring
    prof = [q for i, q in enumerate(prof) if i == 0 or (abs(q[0] - prof[i - 1][0]) + abs(q[1] - prof[i - 1][1])) > 1e-6]
    if abs(prof[0][0] - prof[-1][0]) < 1e-6 and abs(prof[0][1] - prof[-1][1]) < 1e-6:
        prof = prof[:-1]
    p.extrude(prof, BLOCK_REAR, 0.0, 'ENG_Paint_Cast', bevel=.006)
    # Rear bellhousing flange: a broader cast plate behind the block.
    flange = [(x * 1.07, (z - .08) * 1.07 + .08) for x, z in prof]
    p.extrude(flange, BLOCK_REAR - .012, BLOCK_REAR + .0005, 'ENG_Paint_Cast', bevel=.003)
    # Core plugs on the outer bank walls, three per side between cylinders.
    for side in (-1, 1):
        for i in range(3):
            y = (CYL_Y[side][i] + CYL_Y[side][i + 1]) / 2
            x, z = bank_point(side, DECK - .045, .0925)
            n = Vector((side * S45, 0, -S45))
            base = Vector((x, y, z)) - n * .002
            p.lathe([(0, 0), (.019, 0), (.019, .004), (.016, .006), (0, .005)], 14,
                    'ENG_Paint_Cast', axis_matrix(base, n))
        # Cast engine-mount bosses on the skirt.
        p.rbox((side * .170, -.165, .045), (.026, .085, .055), .006, 'ENG_Paint_Cast')
    return p


def build_head(side):
    p = Part('ENG_Head_' + ('L' if side < 0 else 'R'), ['ENG_Paint_Cast'])
    sec_uv = [(.0005, -.095), (.018, -HEAD_HALF), (.080, -HEAD_HALF), (HEAD_H, -.088),
              (HEAD_H, .088), (.080, HEAD_HALF), (.018, HEAD_HALF), (.0005, .095)]
    poly = [bank_point(side, DECK + u, v) for u, v in sec_uv]
    if side < 0:
        poly = list(reversed(poly))
    y0, y1 = HEAD_Y[side]
    p.extrude(poly, y1, y0, 'ENG_Paint_Cast', bevel=.005)
    # Spark-plug bosses between the exhaust ports.
    m = bank_matrix(side, DECK)
    for y in CYL_Y[side]:
        c = m @ Vector((HEAD_HALF - .002, y - .022, .074))
        p.lathe([(0, 0), (.014, 0), (.014, .006), (0, .006)], 12, 'ENG_Paint_Cast',
                axis_matrix(c, plug_dir(side)))
    x, z = bank_point(side, DECK + HEAD_H * .5, 0)
    p.pivot = Vector((x, (y0 + y1) / 2, z))
    return p


def plug_dir(side):
    n = Vector((side * S45, 0, -S45))
    a = Vector((side * S45, 0, S45))
    return (n * math.cos(math.radians(32)) + a * math.sin(math.radians(32))).normalized()


def plug_tip(side, y):
    m = bank_matrix(side, DECK)
    base = m @ Vector((HEAD_HALF + .004, y - .022, .074))
    return base, plug_dir(side)


def build_valve_cover(side):
    name = 'ENG_ValveCover_' + ('L' if side < 0 else 'R')
    y0, y1 = HEAD_Y[side]
    yc = (y0 + y1) / 2
    hl = (y0 - y1) / 2 - .008
    m = bank_matrix(side, DECK + HEAD_H + .0005) @ Matrix.Translation((0, yc, 0))
    pivot = m @ Vector((0, 0, 0))
    p = Part(name, ['ENG_Paint_Pressed', 'ENG_Steel_Bright', 'ENG_Rubber'], pivot=pivot)
    # (height, half-length, half-width, corner radius) from flange to crown.
    levels = [(0.0, hl + .006, .094, .026), (.004, hl + .006, .094, .026), (.004, hl - .002, .086, .020),
              (.030, hl - .004, .084, .019), (.050, hl - .007, .080, .017), (.060, hl - .013, .072, .014),
              (.066, hl - .022, .060, .012), (.068, hl - .032, .046, .010)]
    rings = []
    for h, l, w, r in levels:
        rings.append([(wv, ll, h) for ll, wv in rounded_rect(l, w, r, corner=3, side=5)])
    p.grid(rings, 'ENG_Paint_Pressed', cap0=True, xf=m)
    # Pressed raised centre panel.
    top = rings[-1]
    inner = [(wv * .86, ll * .97, .068) for wv, ll, _ in top]
    crown = [(wv * .82, ll * .955, .0715) for wv, ll, _ in top]
    p.grid([top, inner, crown], 'ENG_Paint_Pressed', cap1=True, xf=m)
    # Flange bolts, both long sides.
    for k in range(4):
        ly = -hl + .05 + k * (2 * hl - .10) / 3
        for wv in (-.090, .090):
            p.lathe([(.0075, 0), (.0075, .006), (.006, .0075), (0, .0078)], 6,
                    'ENG_Steel_Bright', m @ Matrix.Translation((wv, ly, .004)))
    # Breather on the driver cover, PCV grommet/valve on the passenger cover.
    if side < 0:
        p.lathe([(.020, 0), (.022, .006), (.022, .030), (.018, .036), (0, .038)], 16,
                'ENG_Steel_Bright', m @ Matrix.Translation((-.010, hl - .085, .070)))
    else:
        p.lathe([(.014, 0), (.014, .006), (.010, .008), (.010, .028), (0, .030)], 12,
                'ENG_Rubber', m @ Matrix.Translation((-.010, hl - .080, .070)))
    return p


def build_wire_clips(side):
    """Loom combs on the outer flange; the leads pass through them."""
    name = 'ENG_WireLoom_' + ('L' if side < 0 else 'R')
    m = bank_matrix(side, DECK)
    p = Part(name, ['ENG_Black_Satin'])
    for y in loom_clip_y(side):
        p.rbox((HEAD_HALF + .009, y, .135), (.020, .012, .060), .003, 'ENG_Black_Satin', xf=m)
    p.pivot = m @ Vector((HEAD_HALF + .009, loom_clip_y(side)[0], .135))
    return p


def loom_clip_y(side):
    c = CYL_Y[side]
    return [(c[0] + c[1]) / 2 + .01, (c[2] + c[3]) / 2 + .01]


def intake_top(x, y, half):
    t = abs(x) / half
    z = .293 + .012 * (1 - t * t)
    # Runner humps from each port toward the plenum.
    for side in (-1, 1):
        for i, cy in enumerate(CYL_Y[side]):
            py = cy + .004
            ey = CARB_Y + (.045 if i < 2 else -.045)
            # runner centreline: from (side*half, py) to (side*.045, ey)
            sx = side * half
            ex = side * .045
            dx, dy = ex - sx, ey - py
            L2 = dx * dx + dy * dy
            s = max(0, min(1, ((x - sx) * dx + (y - py) * dy) / L2))
            qx, qy = sx + s * dx, py + s * dy
            d = math.hypot(x - qx, y - qy)
            f = max(0.0, 1 - (d / .030) ** 2)
            z = max(z, .300 + .022 * f * f * (1 - .25 * s))
    # Plenum and carburettor pad.
    px = abs(x) / .090
    py = abs(y - CARB_Y) / .088
    rr = (px ** 4 + py ** 4) ** .25
    if rr < 1:
        z = max(z, CARB_PAD_Z if rr < .78 else CARB_PAD_Z - (rr - .78) / .22 * .035)
    return z


def build_intake():
    p = Part('ENG_Intake', ['ENG_Paint_Cast'], pivot=(0, CARB_Y, CARB_PAD_Z))
    vlo = -.1005
    lt = bank_point(-1, DECK + .080, vlo)
    lb = bank_point(-1, DECK + .020, vlo)
    half = -lt[0]
    nx = 22
    ys = [INTAKE_Y[0] - (INTAKE_Y[0] - INTAKE_Y[1]) * k / 47 for k in range(48)]
    rings = []
    for y in ys:
        sec = [(-.060, y, .200), (lb[0], y, lb[1])]
        for k in range(1, 5):
            t = k / 5
            sec.append((lb[0] + (lt[0] - lb[0]) * t, y, lb[1] + (lt[1] - lb[1]) * t))
        for k in range(nx + 1):
            x = -half + 2 * half * k / nx
            sec.append((x, y, intake_top(x, y, half)))
        for k in range(1, 5):
            t = k / 5
            sec.append((-(lt[0] + (lb[0] - lt[0]) * t), y, lt[1] + (lb[1] - lt[1]) * t))
        sec.append((-lb[0], y, lb[1]))
        sec.append((.060, y, .200))
        rings.append(sec)
    p.grid(rings, 'ENG_Paint_Cast', cap0=True, cap1=True)
    # Thermostat housing with upper-hose neck on the front face.
    base = Vector((-.060, INTAKE_Y[0] + .002, .268))
    p.lathe([(0, 0), (.032, 0), (.032, .018), (.024, .022), (.022, .060), (.025, .064),
             (.025, .070), (.019, .072), (0, .072)], 16, 'ENG_Paint_Cast',
            axis_matrix(base, Vector((0, 1, .18))))
    return p


def build_heads_ports_exhaust(side):
    name = 'ENG_ExhaustManifold_' + ('L' if side < 0 else 'R')
    m = bank_matrix(side, DECK)
    p = Part(name, ['ENG_Cast_Iron'])
    log_u, log_v = .008, .158
    ys = [y + .015 for y in CYL_Y[side]]
    for y in ys:
        p.rbox((HEAD_HALF + .0065, y, .040), (.012, .046, .040), .004, 'ENG_Cast_Iron', xf=m)
        path = catmull([(HEAD_HALF + .010, y, .040), (HEAD_HALF + .035, y, .036),
                        (log_v - .006, y, log_u + .006)], per=4)
        p.sweep([m @ q for q in path], circle_section(.019, 10), 'ENG_Cast_Iron')
    yf, yr = ys[0] + .035, ys[-1] - .060
    lp = [m @ Vector((log_v, yf - k * (yf - yr) / 12, log_u)) for k in range(13)]
    sec = [(.030 * math.cos(2 * math.pi * i / 14), .026 * math.sin(2 * math.pi * i / 14)) for i in range(14)]
    p.sweep(lp, sec, 'ENG_Cast_Iron')
    p.lathe([(0, 0), (.030, 0), (.026, -.004), (0, -.004)], 14, 'ENG_Cast_Iron',
            axis_matrix(lp[0], lp[0] - lp[1]))
    p.lathe([(0, 0), (.030, 0), (.026, -.004), (0, -.004)], 14, 'ENG_Cast_Iron',
            axis_matrix(lp[-1], lp[-1] - lp[-2]))
    # Downturned outlet with a three-bolt flange near the rear.
    oc = m @ Vector((log_v, ys[-1] - .020, log_u))
    p.lathe([(.026, 0), (.026, -.070), (.042, -.070), (.042, -.082), (.022, -.082)], 14,
            'ENG_Cast_Iron', axis_matrix(oc, Vector((0, 0, 1))))
    p.pivot = m @ Vector((log_v, (yf + yr) / 2, log_u))
    return p


def build_oil_pan():
    p = Part('ENG_OilPan', ['ENG_Paint_Pressed'], pivot=(0, -.26, -.018))

    def depth(y):
        t = max(0.0, min(1.0, (-.245 - y) / .060))
        t = t * t * (3 - 2 * t)
        return -.095 + (-.215 + .095) * t

    def section(y):
        zb = depth(y)
        sump = (zb + .095) / -.120
        hb = .165 - .015 * sump
        pts = [(-.190, -.0185), (.190, -.0185), (.190, -.0235), (.176, -.0235)]
        r = .030
        wall = [(.172, -.040), (hb + .004, zb + r)]
        for i in range(5):
            a = -math.pi / 2 * i / 4
            pts_r = (hb - r + r * math.cos(a), zb + r + r * math.sin(a))
            wall.append(pts_r)
        pts += wall
        mirror = [(-x, z) for x, z in reversed(wall)]
        pts += mirror + [(-.176, -.0235), (-.190, -.0235)]
        return [(x, y, z) for x, z in pts]

    ys = [.055 - k * (.630) / 27 for k in range(28)]
    p.grid([section(y) for y in ys], 'ENG_Paint_Pressed', cap0=True, cap1=True)
    p.lathe([(.016, 0), (.016, -.008), (.011, -.012), (0, -.012)], 6, 'ENG_Steel_Bright',
            axis_matrix(Vector((.06, -.47, -.215)), Vector((0, 0, 1))))
    return p


def timing_outline():
    return [(-.150, -.018), (.150, -.018), (.162, .015), (.160, .060), (.150, .095),
            (.120, .118), (.090, .128), (.075, .165), (.070, .225), (.045, .258), (0.0, .266),
            (-.045, .258), (-.070, .225), (-.085, .170), (-.130, .140), (-.158, .080), (-.162, .015)]


def build_timing_cover():
    p = Part('ENG_TimingCover', ['ENG_Paint_Cast', 'ENG_Steel_Bright'], pivot=(0, .03, .1))
    p.extrude(timing_outline(), .0005, .055, 'ENG_Paint_Cast', bevel=.008)
    # Crank seal boss.
    p.lathe([(.058, 0), (.058, .010), (.050, .014), (.040, .014)], 24, 'ENG_Paint_Cast',
            Matrix.Translation((0, .052, 0)) @ Matrix.Rotation(-math.pi / 2, 4, 'X'))
    # Distributor boss.
    p.lathe([(0, -.050), (.030, -.050), (.030, 0), (.024, .004), (0, .004)], 16, 'ENG_Paint_Cast',
            axis_matrix(DIST_BASE, DIST_AXIS))
    # Oil-filter adapter, lower passenger side, pointing down and outward.
    fa, fd = filter_frame()
    p.lathe([(0, -.040), (.034, -.040), (.034, 0), (.026, .004), (0, .004)], 16, 'ENG_Paint_Cast',
            axis_matrix(fa, fd))
    # Front oil-filler tube, driver side.
    tube = catmull([(-.105, .040, .112), (-.106, .062, .130), (-.110, .080, .168)], per=5)
    p.sweep(tube, circle_section(.016, 12), 'ENG_Paint_Cast')
    return p


def filter_frame():
    d = Vector((.50, .0, -.866)).normalized()
    a = Vector((.168, .112, -.040))
    return a, d


def build_oil_filter():
    a, d = filter_frame()
    p = Part('ENG_OilFilter', ['ENG_Black_Satin', 'ENG_Steel_Bright'], pivot=a)
    base = a + d * .004
    p.lathe([(0, 0), (.040, 0), (.047, .006), (.047, .112), (.043, .120), (.020, .123), (0, .123)],
            24, 'ENG_Black_Satin', axis_matrix(base, d))
    return p


def build_oil_filler_cap():
    top = Vector((-.110, .080, .168))
    p = Part('ENG_OilFillerCap', ['ENG_Black_Satin'], pivot=top)
    ax = Vector((-.02, .40, 1)).normalized()
    p.lathe([(0, 0), (.019, 0), (.027, .004), (.027, .016), (.022, .022), (0, .024)], 18,
            'ENG_Black_Satin', axis_matrix(top, ax))
    return p


def build_water_pump():
    c = Vector((PUMP_C[0], .055, PUMP_C[1]))
    p = Part('ENG_WaterPump', ['ENG_Paint_Cast', 'ENG_Steel_Bright'], pivot=c)
    xf = axis_matrix(c, Vector((0, 1, 0)))
    p.lathe([(0, .0005), (.072, .0005), (.072, .012), (.060, .015), (.058, .028), (.034, .032),
             (.032, .052), (.022, .054), (.020, .060), (0, .060)], 24, 'ENG_Paint_Cast', xf)
    # Lower-hose inlet and heater nipple.
    for start, direction, r, ln in (((-.045, .072, .150), (-.55, .55, -.2), .021, .060),
                                    ((.040, .070, .235), (.35, .55, .55), .010, .040)):
        s = Vector(start)
        dd = Vector(direction).normalized()
        p.lathe([(0, -.010), (r, -.010), (r, ln - .006), (r + .003, ln - .004), (r + .003, ln),
                 (r - .004, ln), (0, ln)], 12, 'ENG_Paint_Cast', axis_matrix(s, dd))
    return p


def groove_pulley(p, center_xz, y_mid, r, width, segs, mat, hub=True):
    c = Vector((center_xz[0], y_mid - width / 2, center_xz[1]))
    xf = axis_matrix(c, Vector((0, 1, 0)))
    w = width
    prof = [(0, 0), (r - .012, 0), (r, .0015), (r, .004), (r - .009, w * .38), (r - .009, w * .62),
            (r, w - .004), (r, w - .0015), (r - .012, w), (.022, w), (.022, w + .006), (0, w + .006)]
    p.lathe(prof, segs, mat, xf)


def build_crank_damper():
    p = Part('ENG_CrankDamper', ['ENG_Black_Satin', 'ENG_Rubber', 'ENG_Steel_Bright'], pivot=(0, .085, 0))
    xf = axis_matrix(Vector((0, .066, 0)), Vector((0, 1, 0)))
    p.lathe([(0, 0), (.030, 0), (.030, .008), (.070, .010), (.070, .012), (.090, .012), (.090, .030),
             (.072, .030), (.072, .033), (.090, .033), (.090, .046), (.035, .048), (0, .048)], 32,
            'ENG_Black_Satin', xf,
            mats=['ENG_Black_Satin'] * 6 + ['ENG_Rubber', 'ENG_Rubber'] + ['ENG_Black_Satin'] * 4)
    groove_pulley(p, (0, 0), BELT_Y, .088, .020, 32, 'ENG_Black_Satin')
    p.lathe([(.012, 0), (.012, .010), (.009, .013), (0, .013)], 6, 'ENG_Steel_Bright',
            axis_matrix(Vector((0, BELT_Y + .016, 0)), Vector((0, 1, 0))))
    return p


def build_pump_pulley_fan():
    p = Part('ENG_FanPulley', ['ENG_Black_Satin'], pivot=(PUMP_C[0], BELT_Y, PUMP_C[1]))
    groove_pulley(p, PUMP_C, BELT_Y, .078, .020, 32, 'ENG_Black_Satin')
    c = Vector((PUMP_C[0], BELT_Y + .016, PUMP_C[1]))
    p.lathe([(0, 0), (.032, 0), (.032, .034), (0, .034)], 16, 'ENG_Black_Satin',
            axis_matrix(c, Vector((0, 1, 0))))
    return p


def build_fan():
    hub = Vector((PUMP_C[0], .169, PUMP_C[1]))
    p = Part('ENG_Fan', ['ENG_Black_Satin'], pivot=hub)
    p.lathe([(0, 0), (.080, 0), (.084, .002), (.084, .005), (0, .005)], 24, 'ENG_Black_Satin',
            axis_matrix(hub, Vector((0, 1, 0))))
    pitch = math.radians(27)
    thick = .0028
    nr, nc = 7, 3
    for b in range(4):
        ang = math.pi / 4 + b * math.pi / 2
        top, bot = [], []
        for i in range(nr + 1):
            r = .060 + (.228 - .060) * i / nr
            chord = .040 + .030 * math.sin(math.pi * min(1, i / nr * 1.25)) - .010 * (i / nr)
            rt, rb = [], []
            for j in range(nc + 1):
                c = -chord / 2 + chord * j / nc
                camber = .006 * (1 - (2 * j / nc - 1) ** 2)
                # local: radial r, tangential c, axial along pitch
                tang = c * math.cos(pitch)
                axial = c * math.sin(pitch) + camber + .006
                for lst, off in ((rt, thick / 2), (rb, -thick / 2)):
                    t2 = tang - off * math.sin(pitch)
                    ax = axial + off * math.cos(pitch)
                    x = r * math.cos(ang) - t2 * math.sin(ang)
                    z = r * math.sin(ang) + t2 * math.cos(ang)
                    lst.append(hub + Vector((x, ax, z)))
            top.append(rt)
            bot.append(rb)
        rings = []
        for i in range(nr + 1):
            rings.append(top[i] + list(reversed(bot[i])))
        p.grid(rings, 'ENG_Black_Satin', cap0=True, cap1=True)
    return p


def build_belt():
    p = Part('ENG_DriveBelt', ['ENG_Rubber'], pivot=(0, BELT_Y, .12))
    circles = [((0.0, 0.0), .0835), (ALT_C, .0335), (PUMP_C, .0735)]   # CCW order
    pts = []
    tang = []
    n = len(circles)
    for i in range(n):
        (c1, r1), (c2, r2) = circles[i], circles[(i + 1) % n]
        d = Vector((c2[0] - c1[0], c2[1] - c1[1]))
        L = d.length
        dn = d / L
        # external tangent on the right-hand side of travel for a CCW loop
        cos_a = (r1 - r2) / L
        sin_a = math.sqrt(1 - cos_a * cos_a)
        nrm = Vector((dn.x * cos_a + dn.y * sin_a, -dn.x * sin_a + dn.y * cos_a))
        tang.append((Vector(c1) + nrm * r1, Vector(c2) + nrm * r2, nrm))
    for i in range(n):
        a0, a1, nrm = tang[i]
        prev_n = tang[i - 1][2]
        c, r = circles[i]
        th0 = math.atan2(prev_n.y, prev_n.x)
        th1 = math.atan2(nrm.y, nrm.x)
        while th1 > th0:
            th1 -= 2 * math.pi
        steps = max(3, int((th0 - th1) / math.radians(7)))
        for k in range(steps):
            th = th0 + (th1 - th0) * k / steps
            pts.append((c[0] + r * math.cos(th), c[1] + r * math.sin(th)))
        seg = (a1 - a0).length
        ns = max(2, int(seg / .03))
        for k in range(ns):
            q = a0 + (a1 - a0) * (k / ns)
            pts.append((q.x, q.y))
    path = [Vector((x, BELT_Y, z)) for x, z in pts]
    # Trapezoid V-belt: section in (normal, binormal). Normal points away from wrap.
    sec = [(-.0035, -.0045), (.0045, -.0065), (.0045, .0065), (-.0035, .0045)]
    # Build manually so the wide face is outward of the loop.
    ctr = Vector((.08, BELT_Y, .14))
    rings = []
    for i, q in enumerate(path):
        t = (path[(i + 1) % len(path)] - path[i - 1]).normalized()
        out = t.cross(Vector((0, 1, 0))).normalized()
        if out.dot(q - ctr) < 0:
            out = -out
        rings.append([q + out * (s0 + .0035) + Vector((0, s1, 0)) for s0, s1 in sec])
    vr = [[p.bm.verts.new(v) for v in ring] for ring in rings]
    for i in range(len(vr)):
        a, b = vr[i], vr[(i + 1) % len(vr)]
        for k in range(4):
            j = (k + 1) % 4
            p.bm.faces.new([a[k], a[j], b[j], b[k]])
    return p


def build_alternator():
    c = Vector((ALT_C[0], -.012, ALT_C[1]))
    pivot = Vector((ALT_C[0], .004, ALT_C[1] - .085))
    p = Part('ENG_Alternator', ['ENG_Aluminium', 'ENG_Black_Satin', 'ENG_Steel_Bright'], pivot=pivot)
    xf = axis_matrix(c, Vector((0, 1, 0)))
    p.lathe([(0, 0), (.050, 0), (.066, .006), (.072, .020), (.078, .030), (.078, .060), (.075, .062),
             (.078, .064), (.078, .094), (.068, .104), (.040, .108), (0, .108)], 28, 'ENG_Aluminium', xf)
    # Cooling fan and pulley.
    p.lathe([(0, 0), (.060, 0), (.060, .007), (0, .007)], 20, 'ENG_Black_Satin',
            axis_matrix(c + Vector((0, .108, 0)), Vector((0, 1, 0))))
    groove_pulley(p, ALT_C, BELT_Y, .0385, .018, 20, 'ENG_Black_Satin')
    # Mounting ears: lower pivot and upper adjuster.
    p.rbox(pivot + Vector((0, .010, .008)), (.030, .044, .030), .006, 'ENG_Aluminium')
    p.rbox(Vector((ALT_C[0] + .062, .004, ALT_C[1] + .062)), (.024, .030, .024), .006, 'ENG_Aluminium')
    # Output terminal.
    p.cyl(c + Vector((-.045, .004, .045)), c + Vector((-.045, -.012, .045)), .006, 8, 'ENG_Steel_Bright')
    return p


def build_alt_bracket():
    p = Part('ENG_AlternatorBracket', ['ENG_Black_Satin', 'ENG_Steel_Bright'],
             pivot=(ALT_C[0], -.025, ALT_C[1] - .085))
    plate = [(.165, .215), (.235, .145), (.285, .170), (.300, .232), (.330, .330), (.318, .345),
             (.276, .262), (.240, .238), (.200, .262)]
    p.extrude(plate, -.0295, -.0215, 'ENG_Black_Satin', bevel=.002)
    # Pivot and adjuster bolts bridging bracket to the alternator ears.
    for x, z in ((ALT_C[0], ALT_C[1] - .077), (ALT_C[0] + .062, ALT_C[1] + .062)):
        p.cyl((x, -.0215, z), (x, -.0005, z), .006, 8, 'ENG_Steel_Bright')
        p.lathe([(0, 0), (.011, 0), (.011, .006), (0, .006)], 6, 'ENG_Steel_Bright',
                axis_matrix(Vector((x, -.0005, z)), Vector((0, 1, 0))))
    return p


def build_carburettor():
    p = Part('ENG_Carburettor', ['ENG_Zinc_Plate', 'ENG_Steel_Bright', 'ENG_Black_Satin'],
             pivot=(0, CARB_Y, CARB_PAD_Z))
    z0 = CARB_PAD_Z + .0005
    p.rbox((0, CARB_Y, z0 + .006), (.160, .150, .012), .004, 'ENG_Zinc_Plate')
    p.rbox((0, CARB_Y, z0 + .012 + .028), (.142, .128, .056), .014, 'ENG_Zinc_Plate')
    p.rbox((0, CARB_Y + .070, z0 + .030), (.110, .022, .040), .009, 'ENG_Zinc_Plate')  # float bowl
    p.rbox((0, CARB_Y, z0 + .074), (.150, .136, .012), .006, 'ENG_Zinc_Plate')
    p.lathe([(0, 0), (.066, 0), (.066, CLEANER_Z - z0 - .080), (0, CLEANER_Z - z0 - .080)], 28,
            'ENG_Zinc_Plate', Matrix.Translation((0, CARB_Y, z0 + .080)))
    # Choke housing and throttle lever.
    p.cyl((-.071, CARB_Y - .020, z0 + .052), (-.092, CARB_Y - .020, z0 + .052), .022, 16, 'ENG_Black_Satin')
    p.rbox((.081, CARB_Y - .030, z0 + .020), (.006, .050, .016), .002, 'ENG_Steel_Bright')
    return p


CLEANER_PROFILE = [(0.0, .0005), (.068, .0005), (.072, .004), (.150, .010), (.172, .014), (.180, .020),
                   (.183, .026), (.180, .032), (.176, .034), (.176, .086), (.182, .090), (.183, .095),
                   (.178, .100), (.160, .106), (.110, .114), (.050, .119), (0.0, .120)]


def lid_height(r):
    prof = CLEANER_PROFILE[-6:]
    for (r0, h0), (r1, h1) in zip(prof, prof[1:]):
        if r1 <= r <= r0:
            t = (r - r1) / (r0 - r1)
            return h1 + (h0 - h1) * t
    return prof[-1][1]


def build_air_cleaner():
    base = Vector((0, CARB_Y, CLEANER_Z))
    p = Part('ENG_AirCleaner', ['ENG_Black_Satin', 'ENG_Steel_Bright'], pivot=base)
    p.lathe(CLEANER_PROFILE, 48, 'ENG_Black_Satin', Matrix.Translation(base))
    # Wing nut on the centre stud.
    top = base + Vector((0, 0, .1195))
    p.lathe([(0, 0), (.014, 0), (.014, .010), (.006, .016), (0, .017)], 10, 'ENG_Steel_Bright',
            Matrix.Translation(top))
    for s in (-1, 1):
        p.rbox(top + Vector((s * .020, 0, .010)), (.026, .005, .014), .002, 'ENG_Steel_Bright')
    # Forward snorkel blended into the housing wall.
    ring = []
    for i in range(16):
        a = 2 * math.pi * i / 16
        c, s = math.cos(a), math.sin(a)
        ring.append((.046 * math.copysign(abs(c) ** .5, c), .022 * math.copysign(abs(s) ** .5, s)))
    snork = []
    for k, (y, scale) in enumerate(((.150, 1.0), (.200, 1.0), (.262, 1.0), (.270, 1.08), (.274, 1.08))):
        snork.append([(base.x + sx * scale, base.y + y, base.z + .058 + sz * scale) for sx, sz in ring])
    p.grid(snork, 'ENG_Black_Satin', cap0=True, cap1=False)
    # Rolled mouth: inner return so the opening reads hollow.
    inner = [(base.x + sx * .9, base.y + .268, base.z + .058 + sz * .9) for sx, sz in ring]
    deep = [(base.x + sx * .9, base.y + .230, base.z + .058 + sz * .9) for sx, sz in ring]
    p.grid([snork[-1], inner, deep], 'ENG_Black_Satin', cap1=True)
    return p


DIGITS = {
    '3': [[(.12, 1.18), (.30, 1.36), (.62, 1.38), (.84, 1.20), (.82, .94), (.58, .76), (.40, .74)],
          [(.58, .76), (.86, .58), (.88, .26), (.66, .04), (.32, .03), (.10, .20)]],
    '6': [[(.82, 1.26), (.62, 1.39), (.34, 1.36), (.14, 1.10), (.10, .62), (.14, .26), (.36, .03),
           (.66, .04), (.88, .28), (.86, .58), (.64, .78), (.36, .78), (.14, .58)]],
    '0': [[(.50, 1.39), (.80, 1.24), (.90, .70), (.80, .16), (.50, .01), (.20, .16), (.10, .70),
           (.20, 1.24), (.50, 1.39)]],
}


def build_decal():
    """Small original-stroke '360' on the cleaner lid, readable from the front of the car."""
    base = Vector((0, CARB_Y, CLEANER_Z))
    p = Part('ENG_AirCleanerLabel360', ['ENG_Decal_Silver'], pivot=base + Vector((0, .072, .114)))
    unit = .028
    width = .12 * unit
    advance = 1.12 * unit
    start = 1.5 * advance - .06 * unit
    for k, ch in enumerate('360'):
        ox = start - k * advance
        for stroke in DIGITS[ch]:
            pts = catmull(stroke, per=4)
            # Viewer stands ahead of the car: character right = -X, character up = -Y.
            planar = [(ox - x * unit, .072 - (y - .70) * unit) for x, y in pts]
            left, right = [], []
            for i, (px, py) in enumerate(planar):
                a = planar[max(i - 1, 0)]
                b = planar[min(i + 1, len(planar) - 1)]
                tx, ty = b[0] - a[0], b[1] - a[1]
                L = math.hypot(tx, ty) or 1
                nx, ny = -ty / L * width / 2, tx / L * width / 2
                for lst, s in ((left, 1), (right, -1)):
                    qx, qy = px + s * nx, py + s * ny
                    r = math.hypot(qx, qy)
                    lst.append(Vector((base.x + qx, base.y + qy, base.z + lid_height(r) + .0009)))
            for i in range(len(planar) - 1):
                f = p.bm.faces.new([p.bm.verts.new(left[i]), p.bm.verts.new(right[i]),
                                    p.bm.verts.new(right[i + 1]), p.bm.verts.new(left[i + 1])])
                if f.normal.z < 0:
                    f.normal_flip()
    return p


def dist_point(h):
    return DIST_BASE + DIST_AXIS * h


def cap_towers():
    xf = axis_matrix(dist_point(.128), DIST_AXIS, hint=Vector((0, 1, 0)))
    towers = []
    for i in range(8):
        a = 2 * math.pi * (i + .5) / 8
        base = xf @ Vector((.031 * math.cos(a), .031 * math.sin(a), 0))
        tip = base + DIST_AXIS * .022
        towers.append((a, base, tip))
    return towers


def build_distributor():
    p = Part('ENG_Distributor', ['ENG_Paint_Cast', 'ENG_Steel_Bright'], pivot=DIST_BASE)
    xf = axis_matrix(DIST_BASE, DIST_AXIS)
    p.lathe([(0, .004), (.030, .004), (.030, .012), (.034, .016), (.035, .070), (.040, .074),
             (.040, .084), (0, .084)], 20, 'ENG_Paint_Cast', xf)
    # Vacuum advance canister.
    side = xf @ Vector((0, -.030, .055))
    p.lathe([(0, 0), (.022, 0), (.024, .010), (.024, .026), (.020, .034), (0, .034)], 14,
            'ENG_Steel_Bright', axis_matrix(side, (xf.to_3x3() @ Vector((0, -1, 0)))))
    # Hold-down clamp.
    p.rbox(DIST_BASE + Vector((-.030, .0, .006)), (.040, .016, .006), .002, 'ENG_Steel_Bright')
    return p


def build_distributor_cap():
    p = Part('ENG_DistributorCap', ['ENG_Bakelite_Cap', 'ENG_Rubber'], pivot=dist_point(.084))
    xf = axis_matrix(dist_point(.084), DIST_AXIS)
    p.lathe([(0, .0005), (.046, .0005), (.046, .010), (.044, .030), (.040, .040), (.022, .046),
             (0, .047)], 24, 'ENG_Bakelite_Cap', xf)
    for _a, base, tip in cap_towers():
        p.lathe([(0, -.006), (.0075, -.006), (.0075, .016), (.0060, .022), (0, .022)], 8,
                'ENG_Bakelite_Cap', axis_matrix(base, DIST_AXIS))
    p.lathe([(0, 0), (.009, 0), (.009, .020), (0, .020)], 8, 'ENG_Bakelite_Cap',
            axis_matrix(dist_point(.128), DIST_AXIS))
    return p


def lead_paths():
    """Return (side, cylinder index, polyline) for all eight leads."""
    towers = cap_towers()
    cap_c = dist_point(.128)
    right = sorted([t for t in towers if t[2].x > cap_c.x], key=lambda t: t[2].y, reverse=True)
    left = sorted([t for t in towers if t[2].x <= cap_c.x], key=lambda t: t[2].y, reverse=True)
    out = []
    for side, towers_s in ((1, right), (-1, left)):
        m = bank_matrix(side, DECK)
        for k, y in enumerate(CYL_Y[side]):
            plug, d = plug_tip(side, y)
            boot_end = plug + d * .050
            lu = .118 + .0085 * k
            lv = .112
            pts = [boot_end, boot_end + d * .012,
                   m @ Vector((lv + .010, y - .022, lu - .010)),
                   m @ Vector((lv, y - .040, lu))]
            yfront = HEAD_Y[side][0] - .020
            pts.append(m @ Vector((lv, yfront, lu)))
            _a, tb, tip = towers_s[k]
            stack = k * .0085
            if side > 0:
                pts += [Vector((.300 - stack * .4, .006 + stack * .3, .165 - stack * .5)),
                        Vector((.225, .022 + stack * .5, .168 + stack * .2)),
                        tip + DIST_AXIS * .030 + Vector((.012, 0, 0)), tip + DIST_AXIS * .010, tip]
            else:
                pts += [Vector((-.300, .022 + stack * .4, .232 + stack)),
                        Vector((-.170, .030 + stack * .4, .310 + stack)),
                        Vector((0.0, .033 + stack * .4, .328 + stack)),
                        Vector((.085, .036 + stack * .4, .312 + stack)),
                        tip + DIST_AXIS * .040 + Vector((-.010, 0, 0)), tip + DIST_AXIS * .010, tip]
            out.append((side, k, pts))
    return out


def build_leads():
    p = Part('ENG_IgnitionLeads', ['ENG_Rubber'], pivot=dist_point(.15))
    for side, k, pts in lead_paths():
        path = catmull(pts, per=6)
        p.sweep(path, circle_section(.0036, 6), 'ENG_Rubber')
    return p


def build_plug_boots():
    p = Part('ENG_PlugBoots', ['ENG_Rubber', 'ENG_Steel_Bright'], pivot=(0, -.27, .1))
    for side in (-1, 1):
        for y in CYL_Y[side]:
            plug, d = plug_tip(side, y)
            p.lathe([(0, -.004), (.0075, -.004), (.0075, .006), (.0055, .010)], 6,
                    'ENG_Steel_Bright', axis_matrix(plug, d))
            p.lathe([(.0055, .010), (.0090, .014), (.0090, .040), (.0060, .050), (0, .0505)], 10,
                    'ENG_Rubber', axis_matrix(plug, d))
    return p


BUILDERS = ['block', 'heads', 'covers', 'intake', 'exhaust', 'pan', 'front', 'carb', 'cleaner',
            'ignition', 'accessories']


def make_materials():
    mats = {}
    for name, (col, metal, rough) in PAINT.items():
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = (*col, 1)
        bsdf.inputs['Metallic'].default_value = metal
        bsdf.inputs['Roughness'].default_value = rough
        m.diffuse_color = (*col, 1)
        mats[name] = m
    return mats


GROUPS = {
    'ENG_Castings': ['ENG_Block', 'ENG_Head_L', 'ENG_Head_R', 'ENG_Intake', 'ENG_TimingCover',
                     'ENG_WaterPump', 'ENG_ExhaustManifold_L', 'ENG_ExhaustManifold_R'],
    'ENG_Pressings': ['ENG_ValveCover_L', 'ENG_ValveCover_R', 'ENG_OilPan', 'ENG_AirCleaner',
                      'ENG_AirCleanerLabel360'],
    'ENG_FuelIgnition': ['ENG_Carburettor', 'ENG_Distributor', 'ENG_DistributorCap',
                         'ENG_IgnitionLeads', 'ENG_PlugBoots', 'ENG_WireLoom_L', 'ENG_WireLoom_R'],
    'ENG_FrontDrive': ['ENG_CrankDamper', 'ENG_FanPulley', 'ENG_Fan', 'ENG_DriveBelt',
                       'ENG_Alternator', 'ENG_AlternatorBracket', 'ENG_OilFilter', 'ENG_OilFillerCap'],
}


def generate(scene=None, root_location=(0, 0, 0)):
    scene = scene or bpy.context.scene
    mats = make_materials()
    top = bpy.data.collections.new('AMC360_Engine')
    scene.collection.children.link(top)
    root = bpy.data.objects.new('ENG_Root', None)
    root.empty_display_type = 'ARROWS'
    root.empty_display_size = .15
    root.location = root_location
    root['frame'] = 'crank axis at block front face; +Y forward, +Z up, driver -X'
    top.objects.link(root)
    parts = [build_block(None)]
    for side in (-1, 1):
        parts += [build_head(side), build_valve_cover(side), build_heads_ports_exhaust(side),
                  build_wire_clips(side)]
    parts += [build_intake(), build_oil_pan(), build_timing_cover(), build_oil_filter(),
              build_oil_filler_cap(), build_water_pump(), build_crank_damper(),
              build_pump_pulley_fan(), build_fan(), build_belt(), build_alternator(),
              build_alt_bracket(), build_carburettor(), build_air_cleaner(), build_decal(),
              build_distributor(), build_distributor_cap(), build_leads(), build_plug_boots()]
    objs = {}
    for part in parts:
        ob = part.build(root, mats, recalc=part.name != 'ENG_AirCleanerLabel360')
        objs[ob.name] = ob
    for gname, names in GROUPS.items():
        col = bpy.data.collections.new(gname)
        top.children.link(col)
        for n in names:
            col.objects.link(objs[n])
    missing = set(objs) - {n for v in GROUPS.values() for n in v}
    assert not missing, missing
    return root, objs


def main():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args(argv)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    generate(scene)
    bpy.ops.wm.save_as_mainfile(filepath=args.out, compress=True)
    print('saved', args.out)


if __name__ == '__main__':
    main()
