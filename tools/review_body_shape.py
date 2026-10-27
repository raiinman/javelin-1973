"""Capture fixed-camera body-shape evidence from a saved original Blender file."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--blend',type=Path,default=ROOT/'assets/Javelin73PC.blend')
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
args.out=args.out.resolve()
args.blend=args.blend.resolve()
args.out.mkdir(parents=True,exist_ok=False)
bpy.ops.wm.open_mainfile(filepath=str(args.blend.resolve()))
scene=bpy.context.scene
scene.frame_set(1)
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1100
scene.render.resolution_y=800
scene.render.resolution_percentage=100
for material in bpy.data.materials:
    material.use_backface_culling=True
clay=bpy.data.materials.new('ReviewClay')
clay.diffuse_color=(.38,.38,.38,1)
clay.use_nodes=True
bsdf=clay.node_tree.nodes.get('Principled BSDF')
bsdf.inputs['Base Color'].default_value=(.38,.38,.38,1)
bsdf.inputs['Roughness'].default_value=.36
views={
    'front-quarter':((-4,7,2.2),(0,.30,.05),5.8),
    'front-quarter-opposite':((4,7,2.2),(0,.30,.05),5.8),
    'rear-quarter':((-4,-7,2.8),(0,-.30,.10),5.8),
    'side':((-8,0,.5),(0,0,0),5.8),
    'top':((0,0,9),(0,0,0),7.1),
    'fender-close':((-3,4.4,2.1),(0,1.15,.20),3.1),
    'sail-close':((-4,-3,2.5),(0,-.90,.38),3.0)
}
captures=[]
for name,(position,target,scale) in views.items():
    camera=scene.camera
    camera.data.type='ORTHO'
    camera.data.ortho_scale=scale
    camera.location=position
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    for mode in ('paint','clay'):
        scene.view_layers[0].material_override=clay if mode=='clay' else None
        scene.render.filepath=str(args.out/f'{name}-{mode}.png')
        bpy.ops.render.render(write_still=True)
    captures.append({'view':name,'position':position,'target':target,'orthoScale':scale})
for name,position,target in (
        ('target-frame2-estimate',(1.30,6.00,1.35),(0,.55,.02)),
        ('target-frame30-estimate',(.95,6.15,1.20),(0,.50,.01)),
        ('target-wide-estimate',(1.30,4.80,1.15),(0,.55,.02))):
    camera=scene.camera
    camera.data.type='PERSP'
    camera.data.lens=40 if name=='target-wide-estimate' else 50
    camera.data.sensor_width=36
    camera.data.sensor_fit='HORIZONTAL'
    camera.location=position
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.resolution_x=914
    scene.render.resolution_y=523
    for mode in ('paint','clay'):
        scene.view_layers[0].material_override=clay if mode=='clay' else None
        scene.render.filepath=str(args.out/f'{name}-{mode}.png')
        bpy.ops.render.render(write_still=True)
    captures.append({'view':name,'position':position,'target':target,'lens':camera.data.lens,'sensorWidth':36,
                     'resolution':[914,523],'calibrated':False})
payload={'blend':str(args.blend),'sha256':hashlib.sha256(args.blend.read_bytes()).hexdigest(),
         'blender':bpy.app.version_string,'frame':1,'views':captures,
         'limits':'Fixed diagnostic cameras; not calibrated photo projections. Clay glass is opaque.',
         'triangles':sum(len(p.vertices)-2 for o in bpy.data.objects if o.name.startswith('J73Mesh_') for p in o.data.polygons)}
(args.out/'report.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print('BODY_SHAPE_REVIEW_COMPLETE',len(captures)*2)
