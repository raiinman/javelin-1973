import bpy, sys, os
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.open_mainfile(filepath=a[0], load_ui=False, use_scripts=False)
out=a[1]; tag=a[2]
sc=bpy.context.scene
for n in ('ExhaustManifold_Left_CompleteCast','ExhaustManifold_Right_CompleteCast','ExhaustManifold_Left_OutletThroat','CylinderHead_Left','SparkPlugBoot_-1_1'):
    o=bpy.data.objects[n]; bb=[o.matrix_world@Vector(c) for c in o.bound_box]
    print(n,'parent',o.parent and o.parent.name,'min',[round(min(v[i] for v in bb),3) for i in range(3)],'max',[round(max(v[i] for v in bb),3) for i in range(3)],'verts',len(o.data.vertices),'faces',len(o.data.polygons), 'mods',[m.type for m in o.modifiers])
sc.render.engine='CYCLES'; sc.cycles.samples=48; sc.cycles.use_denoising=True
sc.render.resolution_x, sc.render.resolution_y = 1400, 1000; sc.render.resolution_percentage=70
def cam(name, loc, target, lens):
    cd=bpy.data.cameras.new(name); cd.lens=lens; ob=bpy.data.objects.new(name,cd); sc.collection.objects.link(ob)
    ob.location=loc; ob.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler(); return ob
for n,(loc,tgt) in {'manifold_right':((1.25,.35,.15),(.30,0,0)),'manifold_left':((-1.25,.35,.15),(-.30,0,0)),
                   'manifold_right_low':((.95,-.6,-.25),(.32,-.05,-.02))}.items():
    sc.camera=cam(n,loc,tgt,45); sc.render.filepath=os.path.join(out,f'{tag}_{n}.png'); bpy.ops.render.render(write_still=True)
