import bpy, sys
out={}
for path in sys.argv[sys.argv.index('--')+1:]:
    bpy.ops.wm.open_mainfile(filepath=path, load_ui=False, use_scripts=False)
    out[path]={o.name:(tuple(round(x,9) for r in o.matrix_world for x in r), o.parent.name if o.parent else None, o.parent_type, tuple(o.scale), [s.material.name for s in o.material_slots if s.material]) for o in bpy.data.objects}
a,b=list(out.values())
print('objects',len(a),len(b),'transform/parent/scale/material-slot diffs:',[k for k in a if a[k]!=b.get(k)])
