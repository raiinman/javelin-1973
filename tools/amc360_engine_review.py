"""Verification, renders and car bay fit for the AMC 360-style engine.

  python tools/amc360_engine_review.py check  --engine E.blend --report R.json
  python tools/amc360_engine_review.py render --engine E.blend --outdir DIR
  python tools/amc360_engine_review.py fit    --engine E.blend --car CAR.blend --out FIT.blend
        --report R.json --renders DIR [--root X Y Z]

Runs inside Blender 5.2 (blender -b --python ... -- ARGS) or with the bpy module.
The car file is opened read-only and never saved over; fit saves a separate copy.
"""
import argparse
import hashlib
import json
import math
import os
import sys
from itertools import combinations

import bpy  # must precede bmesh when run as the bpy module
import bmesh
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

# Pairs that are meant to seat into one another (bolted spigots, leads entering
# boots/towers, combs gripping leads). Everything else must not interpenetrate.
SEATED = {
    frozenset(('ENG_IgnitionLeads', 'ENG_PlugBoots')): 'lead ends enter boot tips',
    frozenset(('ENG_IgnitionLeads', 'ENG_DistributorCap')): 'lead ends enter cap towers',
    frozenset(('ENG_IgnitionLeads', 'ENG_WireLoom_L')): 'loom comb grips leads',
    frozenset(('ENG_IgnitionLeads', 'ENG_WireLoom_R')): 'loom comb grips leads',
    frozenset(('ENG_PlugBoots', 'ENG_Head_L')): 'plug threads enter head bosses',
    frozenset(('ENG_PlugBoots', 'ENG_Head_R')): 'plug threads enter head bosses',
    frozenset(('ENG_Distributor', 'ENG_TimingCover')): 'distributor shank in cover boss',
    frozenset(('ENG_Distributor', 'ENG_DistributorCap')): 'cap seats on housing lip',
    frozenset(('ENG_OilFilter', 'ENG_TimingCover')): 'filter spins onto adapter',
    frozenset(('ENG_OilFillerCap', 'ENG_TimingCover')): 'cap on filler tube',
    frozenset(('ENG_WaterPump', 'ENG_FanPulley')): 'pulley on pump hub',
    frozenset(('ENG_Fan', 'ENG_FanPulley')): 'fan bolted to spacer',
    frozenset(('ENG_AlternatorBracket', 'ENG_Alternator')): 'pivot and adjuster bolts',
    frozenset(('ENG_Carburettor', 'ENG_AirCleaner')): 'cleaner neck seats on air horn',
    frozenset(('ENG_WaterPump', 'ENG_TimingCover')): 'pump flange bolted to cover',
    frozenset(('ENG_CrankDamper', 'ENG_TimingCover')): 'damper hub in seal boss',
    frozenset(('ENG_ExhaustManifold_L', 'ENG_Head_L')): 'port flanges on head face',
    frozenset(('ENG_ExhaustManifold_R', 'ENG_Head_R')): 'port flanges on head face',
}


def args_after_dashes():
    return sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def engine_objects():
    return sorted([o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('ENG_')],
                  key=lambda o: o.name)


def eval_bmesh(ob, dg):
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.transform(ob.matrix_world)
    ev.to_mesh_clear()
    return bm


def tri_count(ob, dg):
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    me.calc_loop_triangles()
    n = len(me.loop_triangles)
    ev.to_mesh_clear()
    return n


def topology(ob, dg):
    bm = eval_bmesh(ob, dg)
    bm.faces.ensure_lookup_table()
    degenerate = sum(1 for f in bm.faces if f.calc_area() < 1e-9)
    zero_edges = sum(1 for e in bm.edges if e.calc_length() < 1e-7)
    boundary = sum(1 for e in bm.edges if len(e.link_faces) == 1)
    nonmanifold = sum(1 for e in bm.edges if len(e.link_faces) > 2)
    loose = sum(1 for v in bm.verts if not v.link_faces)
    inconsistent = sum(1 for e in bm.edges if len(e.link_faces) == 2 and not e.is_contiguous)
    # Signed volume per connected shell: positive = outward normals.
    seen, shells, inward = set(), 0, 0
    for f in bm.faces:
        if f.index in seen:
            continue
        stack, comp = [f], []
        seen.add(f.index)
        while stack:
            g = stack.pop()
            comp.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index)
                        stack.append(h)
        closed = all(len(e.link_faces) == 2 for g in comp for e in g.edges)
        if not closed:
            continue
        shells += 1
        vol = 0.0
        for g in comp:
            vs = [v.co for v in g.verts]
            for i in range(1, len(vs) - 1):
                vol += vs[0].dot(vs[i].cross(vs[i + 1])) / 6
        if vol <= 0:
            inward += 1
    bm.free()
    return dict(degenerate_faces=degenerate, zero_length_edges=zero_edges, boundary_edges=boundary,
                nonmanifold_edges=nonmanifold, loose_verts=loose, inconsistent_winding_edges=inconsistent,
                closed_shells=shells, inward_shells=inward)


def bvh_for(ob, dg):
    bm = eval_bmesh(ob, dg)
    t = BVHTree.FromBMesh(bm)
    bm.free()
    return t


def check(engine_path, report_path):
    bpy.ops.wm.open_mainfile(filepath=engine_path)
    dg = bpy.context.evaluated_depsgraph_get()
    obs = engine_objects()
    per = {}
    total = 0
    for ob in obs:
        n = tri_count(ob, dg)
        total += n
        gh = hashlib.sha256()
        for v in ob.data.vertices:
            gh.update(('%.6f %.6f %.6f;' % tuple(v.co)).encode())
        for f in ob.data.polygons:
            gh.update((' '.join(map(str, f.vertices)) + '|%d;' % f.material_index).encode())
        per[ob.name] = dict(triangles=n, geometry_sha256=gh.hexdigest(),
                            materials=[m.name for m in ob.data.materials],
                            pivot=[round(c, 4) for c in ob.matrix_world.translation],
                            **topology(ob, dg))
    trees = {ob.name: bvh_for(ob, dg) for ob in obs}
    hits, seated = {}, {}
    for a, b in combinations([o.name for o in obs], 2):
        pairs = trees[a].overlap(trees[b])
        if pairs:
            key = frozenset((a, b))
            (seated if key in SEATED else hits)[f'{a} x {b}'] = len(pairs)
    open_ok = {'ENG_AirCleanerLabel360'}
    problems = []
    for name, d in per.items():
        if d['degenerate_faces'] or d['zero_length_edges'] or d['nonmanifold_edges'] or d['loose_verts']:
            problems.append(f'{name}: degenerate/nonmanifold/loose geometry')
        if d['inconsistent_winding_edges']:
            problems.append(f'{name}: inconsistent winding')
        if d['inward_shells']:
            problems.append(f'{name}: {d["inward_shells"]} inward shells')
        if d['boundary_edges'] and name not in open_ok:
            problems.append(f'{name}: {d["boundary_edges"]} open boundary edges')
    for k, v in hits.items():
        a, b = k.split(' x ')
        i, j = trees[a].overlap(trees[b])[0]
        bm = eval_bmesh(bpy.data.objects[a], dg)
        bm.faces.ensure_lookup_table()
        at = [round(c, 3) for c in bm.faces[i].calc_center_median()]
        bm.free()
        problems.append(f'unintended intersection {k}: {v} triangle pairs, e.g. near {at}')
    rep = dict(engine=os.path.basename(engine_path), sha256=sha256(engine_path),
               blender=bpy.app.version_string, total_triangles=total, objects=per,
               seated_contacts={k: [v, SEATED[frozenset(k.split(' x '))]] for k, v in seated.items()},
               unintended_intersections=hits, problems=problems)
    with open(report_path, 'w') as f:
        json.dump(rep, f, indent=1)
    print(json.dumps(dict(total=total, problems=problems), indent=1))
    return rep


# ------------------------------------------------------------------ rendering

def setup_render(res=(1400, 1000), samples=int(os.environ.get('ENG_SAMPLES', 48))):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = int(os.environ.get('ENG_RES_PCT', 100))
    sc.render.film_transparent = False
    sc.view_settings.view_transform = 'AgX'
    world = bpy.data.worlds.get('ENG_ReviewWorld') or bpy.data.worlds.new('ENG_ReviewWorld')
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    bg.inputs[0].default_value = (.55, .57, .60, 1)
    bg.inputs[1].default_value = .55
    sc.world = world


def add_light(name, loc, rot, energy, size, kind='AREA'):
    ld = bpy.data.lights.new(name, kind)
    ld.energy = energy
    if kind == 'AREA':
        ld.size = size
    ob = bpy.data.objects.new(name, ld)
    ob.location, ob.rotation_euler = loc, rot
    bpy.context.scene.collection.objects.link(ob)
    return ob


def look_camera(name, loc, target, lens=50, ortho=None):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.clip_start = .01
    if ortho:
        cd.type = 'ORTHO'
        cd.ortho_scale = ortho
    ob = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob


def render_to(cam, path):
    sc = bpy.context.scene
    sc.camera = cam
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print('render', path)


def studio(center):
    c = Vector(center)
    add_light('ENG_Key', c + Vector((1.6, 1.8, 2.0)), (math.radians(-40), math.radians(35), math.radians(140)), 650, 1.6)
    add_light('ENG_Fill', c + Vector((-2.0, .6, 1.0)), (math.radians(70), 0, math.radians(-110)), 260, 2.5)
    add_light('ENG_Rim', c + Vector((0, -2.2, 1.6)), (math.radians(-55), 0, 0), 300, 2.0)
    fd = bpy.data.meshes.new('ENG_Floor')
    s = 6
    fd.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    fm = bpy.data.materials.new('ENG_FloorMat')
    fm.use_nodes = True
    fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (.35, .35, .36, 1)
    fm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = .8
    fd.materials.append(fm)
    fl = bpy.data.objects.new('ENG_Floor', fd)
    fl.location = (0, 0, -.235)
    bpy.context.scene.collection.objects.link(fl)


def render_engine(engine_path, outdir):
    bpy.ops.wm.open_mainfile(filepath=engine_path)
    os.makedirs(outdir, exist_ok=True)
    setup_render()
    c = Vector((0, -.22, .17))
    studio(c)
    views = {
        'front_quarter': ((1.25, 1.35, .95), 40),
        'rear_quarter': ((-1.30, -1.75, .95), 40),
        'side': ((-2.2, -.22, .20), 50),
        'front': ((0, 2.2, .25), 50),
    }
    for name, (loc, lens) in views.items():
        render_to(look_camera('CAM_' + name, c + Vector(loc) - Vector((0, 0, 0)), c, lens),
                  os.path.join(outdir, f'amc360_{name}.png'))
    top = look_camera('CAM_top', (0, -.22, 2.5), (0, -.22, .1), ortho=1.25)
    render_to(top, os.path.join(outdir, 'amc360_top.png'))
    # Label legibility close-up, from ahead of the engine where a person stands at the bay.
    render_to(look_camera('CAM_label', (0, .32, .95), (0, -.20, .52), 50),
              os.path.join(outdir, 'amc360_label_closeup.png'))
    # Component isolation: each part pulled apart along its own mounting direction.
    up, fwd = Vector((0, 0, 1)), Vector((0, 1, 0))
    offsets = {
        'ENG_AirCleaner': up * .55, 'ENG_AirCleanerLabel360': up * .55, 'ENG_Carburettor': up * .36,
        'ENG_Intake': up * .20,
        'ENG_ValveCover_L': Vector((-.16, 0, .16)), 'ENG_ValveCover_R': Vector((.16, 0, .16)),
        'ENG_ExhaustManifold_L': Vector((-.24, 0, -.04)), 'ENG_ExhaustManifold_R': Vector((.24, 0, -.04)),
        'ENG_OilPan': up * -.28,
        'ENG_TimingCover': fwd * .22, 'ENG_WaterPump': fwd * .34, 'ENG_OilFilter': fwd * .30 + Vector((.10, 0, -.06)),
        'ENG_OilFillerCap': fwd * .26 + up * .10, 'ENG_CrankDamper': fwd * .46, 'ENG_FanPulley': fwd * .50,
        'ENG_DriveBelt': fwd * .58, 'ENG_Fan': fwd * .80,
        'ENG_Alternator': fwd * .42 + Vector((.18, 0, .06)), 'ENG_AlternatorBracket': fwd * .20 + Vector((.18, 0, .06)),
        'ENG_Distributor': fwd * .30 + Vector((.10, 0, .18)), 'ENG_DistributorCap': fwd * .30 + Vector((.10, 0, .30)),
        'ENG_IgnitionLeads': up * .38 + Vector((0, 0, 0)), 'ENG_PlugBoots': up * .38,
        'ENG_WireLoom_L': up * .38, 'ENG_WireLoom_R': up * .38,
    }
    for n, d in offsets.items():
        ob = bpy.data.objects[n]
        ob.location = ob.location + d
    bpy.data.objects['ENG_Floor'].location.z = -.56
    cam = look_camera('CAM_exploded', c + Vector((1.9, 2.25, 1.25)), c + Vector((.04, .30, .20)), 36)
    render_to(cam, os.path.join(outdir, 'amc360_components.png'))


# ------------------------------------------------------------------ car fit

def link_engine(engine_path, root_loc):
    with bpy.data.libraries.load(engine_path, link=False) as (src, dst):
        dst.collections = [n for n in src.collections if n == 'AMC360_Engine']
    col = dst.collections[0]
    bpy.context.scene.collection.children.link(col)
    root = bpy.data.objects['ENG_Root']
    root.location = root_loc
    bpy.context.view_layer.update()
    return col


def car_mesh_objects():
    return [o for o in bpy.data.objects if o.type == 'MESH' and not o.name.startswith('ENG_')]


def visibility_snapshot():
    return {o.name: (o.hide_get() if o.name in bpy.context.view_layer.objects else None,
                     o.hide_viewport, o.hide_render, tuple(round(v, 6) for v in o.matrix_world.translation))
            for o in bpy.data.objects if not o.name.startswith(('ENG_', 'CAM_'))}


def find_hood():
    cands = [o for o in bpy.data.objects if 'hood' in o.name.lower() and o.type == 'MESH']
    return cands


def contact_faces(co, dg, eng_trees):
    """Every car face an engine triangle crosses, with its vertices and the engine parts."""
    ct = bvh_for(co, dg)
    hits = {}
    for n, t in eng_trees.items():
        for _i, k in t.overlap(ct):
            hits.setdefault(k, set()).add(n)
    if not hits:
        return []
    bm = eval_bmesh(co, dg)
    bm.faces.ensure_lookup_table()
    out = []
    for k in sorted(hits):
        f = bm.faces[k]
        out.append(dict(face=k, verts=[[round(c, 3) for c in v.co] for v in f.verts],
                        normal=[round(c, 2) for c in f.normal], engine_parts=sorted(hits[k])))
    bm.free()
    return out


def fit(engine_path, car_path, out_path, report_path, render_dir, root_loc):
    car_hash = sha256(car_path)
    bpy.ops.wm.open_mainfile(filepath=car_path)
    before = visibility_snapshot()
    scene = bpy.context.scene
    frame0 = scene.frame_current
    link_engine(engine_path, root_loc)
    dg = bpy.context.evaluated_depsgraph_get()
    eng = engine_objects()
    eng_trees = {o.name: bvh_for(o, dg) for o in eng}
    eng_bms = {o.name: eval_bmesh(o, dg) for o in eng}
    # Static clearance against every car mesh near the engine, visible or hidden.
    static = {}
    allv = [v.co for bm in eng_bms.values() for v in bm.verts]
    lo = Vector([min(c[i] for c in allv) - .06 for i in range(3)])
    hi = Vector([max(c[i] for c in allv) + .06 for i in range(3)])
    for co in car_mesh_objects():
        if co.data is None or not len(co.data.polygons):
            continue
        bb = [co.matrix_world @ Vector(b) for b in co.bound_box]
        if any(max(b[i] for b in bb) < lo[i] or min(b[i] for b in bb) > hi[i] for i in range(3)):
            continue
        t = bvh_for(co, dg)
        best = 9.0
        for bm in eng_bms.values():
            for v in bm.verts:
                r = t.find_nearest(v.co, best)
                if r[0] is not None and r[3] < best:
                    best = r[3]
        faces = contact_faces(co, dg, eng_trees)
        if best < .05 or faces:
            static[co.name] = dict(min_distance_m=round(best, 4), visible=co.visible_get(),
                                   contact_faces=faces)
    # Hood sweep at half-frame samples, frames 1..26.
    hoods = find_hood()
    sweep = {}
    for hood in hoods:
        rows = []
        for i in range(51):
            f = 1 + i * .5
            scene.frame_set(int(math.floor(f)), subframe=f - math.floor(f))
            dgx = bpy.context.evaluated_depsgraph_get()
            ht = bvh_for(hood, dgx)
            best, who, overl = 9.0, None, 0
            for n, bm in eng_bms.items():
                overl += len(eng_trees[n].overlap(ht))
                for v in bm.verts:
                    r = ht.find_nearest(v.co, best)
                    if r[0] is not None and r[3] < best:
                        best, who = r[3], n
            rows.append(dict(frame=f, min_clearance_m=round(best, 4), nearest_engine_part=who,
                             overlapping_tri_pairs=overl))
        sweep[hood.name] = rows
    scene.frame_set(frame0)
    animated = bool(bpy.data.actions) or any(o.animation_data for o in hoods)
    # Without hood animation, also sweep an explicitly assumed rear-edge hinge.
    # This is a diagnostic, not evidence of the real rig.
    assumed = {}
    for hood in hoods:
        hb = eval_bmesh(hood, bpy.context.evaluated_depsgraph_get())
        ymin = min(v.co.y for v in hb.verts)
        rear = [v.co for v in hb.verts if v.co.y < ymin + .02]
        pivot = Vector((0, ymin, sum(c.z for c in rear) / len(rear)))
        rows = []
        for i in range(51):
            ang = math.radians(55) * i / 50
            m = Matrix.Translation(pivot) @ Matrix.Rotation(ang, 4, 'X') @ Matrix.Translation(-pivot)
            hc = hb.copy()
            hc.transform(m)
            ht = BVHTree.FromBMesh(hc)
            hc.free()
            best, who, overl = 9.0, None, 0
            for n, bm in eng_bms.items():
                overl += len(eng_trees[n].overlap(ht))
                for v in bm.verts:
                    r = ht.find_nearest(v.co, best)
                    if r[0] is not None and r[3] < best:
                        best, who = r[3], n
            rows.append(dict(sample=i, open_deg=round(math.degrees(ang), 2), min_clearance_m=round(best, 4),
                             nearest_engine_part=who, overlapping_tri_pairs=overl))
        hb.free()
        assumed[hood.name] = dict(hinge_pivot=[round(c, 4) for c in pivot], max_open_deg=55, rows=rows)
    after = visibility_snapshot()
    changed = [k for k in before if before[k][:3] != after.get(k, (None,))[:3]]
    rep = dict(car=os.path.basename(car_path), car_sha256=car_hash, engine_sha256=sha256(engine_path),
               root_location=list(root_loc), car_objects=len(before), car_visibility_changed=changed,
               car_has_actions=bool(bpy.data.actions), hood_animated=animated,
               static_near_or_overlapping=static, hood_sweep=sweep, assumed_rear_hinge_sweep=assumed)
    with open(report_path, 'w') as f:
        json.dump(rep, f, indent=1)
    worst = {h: min(rows, key=lambda r: r['min_clearance_m']) for h, rows in sweep.items()}
    print(json.dumps(dict(hoods=[h.name for h in hoods], worst=worst, animated=animated,
                          contacts={k: len(v['contact_faces']) for k, v in static.items()}), indent=1))
    if render_dir:
        section_slices(os.path.join(render_dir, 'amc360_fit_sections.png'), root_loc)
        render_fit(render_dir, root_loc, hoods)
    save_diagnostic(engine_path, car_path, out_path, root_loc)


def section_slices(path, root_loc):
    """Planar cuts of visible car meshes (red, closed hood included) and the engine (blue)."""
    from PIL import Image, ImageDraw
    dg = bpy.context.evaluated_depsgraph_get()
    carobs = [o for o in bpy.data.objects if o.type == 'MESH' and not o.name.startswith('ENG_')
              and o.visible_get()]
    engobs = engine_objects()
    ry = root_loc[1]

    def cut(obs, axis, val):
        no = Vector((1, 0, 0)) if axis == 'x' else Vector((0, 1, 0))
        co = no * val
        segs = []
        for o in obs:
            bm = eval_bmesh(o, dg)
            r = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
                                       plane_co=co, plane_no=no, dist=1e-6)
            segs += [[v.co.copy() for v in e.verts] for e in r['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
            bm.free()
        return segs
    panels = [('y', round(ry - .45, 3)), ('y', round(ry - .25, 3)), ('y', round(ry + .10, 3)),
              ('x', 0.0), ('x', .20), ('x', -.30)]
    W, H = 700, 460
    sheet = Image.new('RGB', (W * 3, H * 2), 'white')
    for k, (ax, val) in enumerate(panels):
        img = Image.new('RGB', (W, H), 'white')
        d = ImageDraw.Draw(img)
        if ax == 'y':
            u0, u1, v0, v1 = -.75, .75, -.55, .55
            U = lambda p: p.x
        else:
            u0, u1, v0, v1 = ry - 1.0, ry + .55, -.55, .55
            U = lambda p: p.y
        sc = min((W - 20) / (u1 - u0), (H - 30) / (v1 - v0))
        P = lambda p: (10 + (U(p) - u0) * sc, H - 10 - (p.z - v0) * sc)
        for g in range(-20, 30):
            gv = g / 10
            if u0 <= gv <= u1:
                d.line([P(Vector((gv, gv, v0))), P(Vector((gv, gv, v1)))], fill=(232, 232, 232))
        for g in range(-5, 6):
            gz = g / 10
            d.line([P(Vector((u0, u0, gz))), P(Vector((u1, u1, gz)))], fill=(232, 232, 232))
        for segs, col in ((cut(carobs, ax, val), (200, 30, 30)), (cut(engobs, ax, val), (30, 60, 200))):
            for a, b in segs:
                d.line([P(a), P(b)], fill=col, width=1)
        lab = 'section %s = %.3f m (%s)' % (ax.upper(), val, 'looking forward' if ax == 'y' else 'from +X')
        d.text((10, 6), lab + '   red: car (visible, closed hood)   blue: engine   grid 0.1 m', fill='black')
        sheet.paste(img, ((k % 3) * W, (k // 3) * H))
    sheet.save(path)
    print('sections', path)


def render_fit(outdir, root_loc, hoods):
    os.makedirs(outdir, exist_ok=True)
    setup_render((1400, 1000))
    c = Vector(root_loc) + Vector((0, -.2, .15))
    add_light('ENG_FitKey', c + Vector((1.5, 1.5, 2.5)), (math.radians(-35), math.radians(30), math.radians(140)), 900, 2)
    add_light('ENG_FitTop', c + Vector((0, 0, 2.5)), (0, 0, 0), 600, 2.5)
    # The supplied file has no hood animation, so the bay views hide the hood
    # in this session only; the car file itself is never written.
    for h in hoods:
        h.hide_render = True
    render_to(look_camera('CAM_fit_bay', c + Vector((1.3, 1.7, 1.3)), c, 30),
              os.path.join(outdir, 'amc360_fit_bay_hood_hidden.png'))
    render_to(look_camera('CAM_fit_bay_top', c + Vector((0, .1, 2.2)), c + Vector((0, .1, 0)), 35),
              os.path.join(outdir, 'amc360_fit_bay_top_hood_hidden.png'))
    for h in hoods:
        h.hide_render = False
    render_to(look_camera('CAM_fit_closed', c + Vector((2.6, 3.2, 1.0)), c + Vector((0, -.4, 0)), 40),
              os.path.join(outdir, 'amc360_fit_closed_hood.png'))


def save_diagnostic(engine_path, car_path, out_path, root_loc):
    """Small separate file: the car's scene is library-linked read-only as a background set,
    the engine collection is appended locally at the fit transform."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(car_path, link=True, relative=False) as (src, dst):
        dst.scenes = list(src.scenes)
    car_scene = dst.scenes[0]
    scene = bpy.context.scene
    scene.name = 'AMC360_BayFit_DIAGNOSTIC'
    scene.background_set = car_scene
    scene['diagnostic'] = ('Engine fit check only. Car is linked read-only from the historical '
                           'assets/current-stl snapshot; not an adopted car checkpoint.')
    link_engine(engine_path, root_loc)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out_path, compress=True, relative_remap=True)
    print('diagnostic', out_path)


def main():
    a = args_after_dashes()
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['check', 'render', 'fit'])
    ap.add_argument('--engine', required=True)
    ap.add_argument('--report')
    ap.add_argument('--outdir')
    ap.add_argument('--car')
    ap.add_argument('--out')
    ap.add_argument('--renders')
    ap.add_argument('--root', nargs=3, type=float, default=(0, 1.49, -.235))
    o = ap.parse_args(a)
    eng = os.path.abspath(o.engine)
    if o.mode == 'check':
        check(eng, os.path.abspath(o.report))
    elif o.mode == 'render':
        render_engine(eng, os.path.abspath(o.outdir))
    else:
        fit(eng, os.path.abspath(o.car), os.path.abspath(o.out), os.path.abspath(o.report),
            os.path.abspath(o.renders) if o.renders else None, tuple(o.root))


if __name__ == '__main__':
    main()
