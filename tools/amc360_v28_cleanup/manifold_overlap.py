import bpy, bmesh, sys
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]
res={}
for path in a:
    bpy.ops.wm.open_mainfile(filepath=path, load_ui=False, use_scripts=False)
    dg=bpy.context.evaluated_depsgraph_get()
    def bvh(o):
        ev=o.evaluated_get(dg); me=ev.to_mesh(); bm=bmesh.new(); bm.from_mesh(me); bm.transform(o.matrix_world); ev.to_mesh_clear(); t=BVHTree.FromBMesh(bm); bm.free(); return t
    obs=[o for o in bpy.data.objects if o.type=='MESH']
    T={o.name:bvh(o) for o in obs}
    hits={}
    for n in ('ExhaustManifold_Left_CompleteCast','ExhaustManifold_Right_CompleteCast'):
        for o in obs:
            if o.name==n: continue
            k=len(T[n].overlap(T[o.name]))
            if k: hits[f'{n} x {o.name}']=k
    res[path.split('/')[-1]]=hits
for k,v in res.items():
    print(k); [print('  ',a,b) for a,b in sorted(v.items())]
