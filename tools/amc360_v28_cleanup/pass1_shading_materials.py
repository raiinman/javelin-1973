"""Shading/material cleanup of the Astra V28 engine. Never moves vertices, objects, origins or parts."""
import bpy, sys, math, json
a = sys.argv[sys.argv.index('--') + 1:]
src, dst, log = a[0], a[1], a[2]
bpy.ops.wm.open_mainfile(filepath=src, load_ui=False, use_scripts=False)
changes = {'materials': {}, 'flat_shaded': [], 'sharp_by_angle': {}}

def setp(mat, **kw):
    b = bpy.data.materials[mat].node_tree.nodes['Principled BSDF']
    val = lambda x: [round(c, 3) for c in x] if hasattr(x, '__len__') else round(x, 3)
    before = {k: val(b.inputs[k].default_value) for k in kw}
    for k, v in kw.items():
        b.inputs[k].default_value = v
    changes['materials'][mat] = {'before': before, 'after': {k: val(v) for k, v in kw.items()}}

# Satin black enamel instead of a 35%-metallic, 0.27-roughness mirror black.
setp('Black_Enamel', **{'Metallic': 0.0, 'Roughness': 0.40, 'Base Color': (0.010, 0.012, 0.015, 1.0)})
# Bakelite cap and rubber read as moulded, not lacquered.
setp('Distributor_Dark_Bakelite', **{'Roughness': 0.5})

for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    me = o.data
    if o.name.startswith('Fan_Blade_'):
        # Stamped steel blades: flat shading removes the inflated, glossy blob read.
        for p in me.polygons:
            p.use_smooth = False
        changes['flat_shaded'].append(o.name)
        continue
    # Keep curved surfaces smooth but split shading at real edges (cast/pressed corners).
    if any(p.use_smooth for p in me.polygons):
        me.set_sharp_from_angle(angle=math.radians(36))
        sharp = me.attributes.get('sharp_edge')
        changes['sharp_by_angle'][o.name] = sum(1 for v in sharp.data if v.value) if sharp else 0
bpy.context.scene['claude_cleanup'] = 'Shading/material pass on Astra V28; geometry, transforms and parts unchanged.'
bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True)
json.dump(changes, open(log, 'w'), indent=1)
print('saved', dst, len(changes['flat_shaded']), len(changes['sharp_by_angle']))
