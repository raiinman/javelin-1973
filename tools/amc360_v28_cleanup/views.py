"""Render a fixed view set of an engine blend (scripts disabled) and print geometry fingerprints."""
import bpy, sys, os, json, hashlib
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
src, outdir, tag = a[0], a[1], a[2]
bpy.ops.wm.open_mainfile(filepath=src, load_ui=False, use_scripts=False)
os.makedirs(outdir, exist_ok=True)
sc = bpy.context.scene
# Fingerprints: vertex coordinates, polygons and world matrices of every mesh/font object.
fp = {}
for o in bpy.data.objects:
    h = hashlib.sha256()
    h.update(repr([round(x, 7) for r in o.matrix_world for x in r]).encode())
    if o.type == 'MESH':
        for v in o.data.vertices: h.update(('%.7f %.7f %.7f;' % tuple(v.co)).encode())
        for p in o.data.polygons: h.update((' '.join(map(str, p.vertices)) + ';').encode())
    fp[o.name] = h.hexdigest()
json.dump(fp, open(os.path.join(outdir, f'fingerprint_{tag}.json'), 'w'), indent=0)
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(os.environ.get('SAMPLES', 64))
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1400, 1100
sc.render.resolution_percentage = int(os.environ.get('PCT', 70))
def cam(name, loc, target, lens):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_start = .01
    ob = bpy.data.objects.new(name, cd); sc.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return ob
views = {'review_camera': bpy.data.objects.get('Engine_Review_Camera'),
         'front': cam('C_front', (0, 2.1, .25), (0, 0, .12), 50),
         'front_closeup': cam('C_fc', (.35, 1.25, .35), (0, .35, .10), 45),
         'front_quarter': cam('C_fq', (1.25, 1.55, .9), (0, .05, .1), 40),
         'rear_quarter': cam('C_rq', (-1.3, -1.6, .9), (0, -.05, .1), 40)}
for n, c in views.items():
    sc.camera = c
    sc.render.filepath = os.path.join(outdir, f'{tag}_{n}.png')
    bpy.ops.render.render(write_still=True)
    print('render', n)
