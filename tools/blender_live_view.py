"""Follow saved car builds in a separate Blender session, preserving dirty data.

Launch with Blender <assets/Javelin73PC.blend> --python <this-file>.
No input injection, network listener, startup installation or source saving.
"""
import json
import os
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parents[1]
TARGET=(ROOT/'assets/Javelin73PC.blend').resolve()
REPORT=ROOT/'build/blender-live-view.json'
REPORT.parent.mkdir(exist_ok=True)
loaded=TARGET.stat().st_mtime_ns
candidate=None
last_report=None


def report(state):
    global last_report
    meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('J73Mesh_')]
    payload={'state':state,'pid':os.getpid(),'file':bpy.data.filepath,'dirty':bpy.data.is_dirty,
             'loaded_mtime_ns':loaded,'parts':len(meshes),
             'triangles':sum(len(p.vertices)-2 for o in meshes for p in o.data.polygons)}
    if payload!=last_report:
        REPORT.write_text(json.dumps(payload,indent=2),encoding='utf-8')
        last_report=payload


def follow_build():
    global loaded,candidate
    try:
        if Path(bpy.data.filepath).resolve()!=TARGET:
            report('stopped, another document was opened')
            return None
        stat=TARGET.stat()
        current=(stat.st_mtime_ns,stat.st_size)
        if current[0]==loaded:
            candidate=None
            report('current')
        elif bpy.data.is_dirty:
            candidate=None
            report('refresh paused, unsaved edits')
        elif current!=candidate:
            candidate=current
            report('waiting for stable build file')
        else:
            bpy.ops.wm.open_mainfile(filepath=str(TARGET))
            loaded=current[0]
            candidate=None
            report('current')
    except (OSError,RuntimeError) as error:
        report('refresh pending: '+str(error))
    return 2.0


report('current')
bpy.app.timers.register(follow_build,first_interval=2.0,persistent=True)
