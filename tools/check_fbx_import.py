"""Require exact mesh/clip imports through the installed game's native loader."""
import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from validate_mod import ROOT, MOD_ID


def check_output(output, nodes, clips):
    errors = []
    imported = re.search(r'IMPORTED meshes=(\d+) animations=(\d+)', output)
    if not imported or int(imported[1]) != len(nodes):
        errors.append(f'Expected exactly {len(nodes)} imported meshes, possible material split')
    if imported and int(imported[2]) != len(clips):
        errors.append(f'Expected exactly {len(clips)} imported animation clips')
    resolved = set(re.findall(r'^RESOLVED (\S+)', output, re.M))
    for node in nodes:
        if node not in resolved:
            errors.append(f'Native mesh resolver failed: {node}')
    actual_clips = set(re.findall(r'^ANIMATION .*? clip=(\S+)', output, re.M))
    if actual_clips != set(clips):
        errors.append(f'Expected clips {sorted(clips)}, got {sorted(actual_clips)}')
    # The actual game imports left-handed coordinates. These asymmetric anchors
    # distinguish a reversed basis that symmetric overall bounds would conceal.
    orientations = {'J73Mesh_Hood': (2, 1), 'J73Mesh_Trunk': (2, -1),
                    'J73Mesh_DoorLeft': (0, -1), 'J73Mesh_DoorRight': (0, 1)}
    bounds = {name: (json.loads(low), json.loads(high)) for name, low, high in
              re.findall(r'^RENDER_BOUNDS (\S+) (\[[^\n]+?\]) (\[[^\n]+?\])$', output, re.M)}
    for name in nodes:
        if name not in orientations:
            continue
        axis, direction = orientations[name]
        if name not in bounds or any(point[axis]*direction <= 0 for point in bounds[name]):
            errors.append(f'Native orientation anchor points the wrong way: {name}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', required=True, type=Path)
    parser.add_argument('--package', type=Path, default=ROOT / MOD_ID)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'assets' / 'model-manifest.json')
    args = parser.parse_args()
    jar = args.game.resolve() / 'projectzomboid.jar'
    java = args.game.resolve() / 'jre64' / 'bin' / 'java.exe'
    javac = shutil.which('javac')
    if not jar.is_file() or not java.is_file() or not javac:
        parser.error('Requires installed game jar/runtime and javac supporting --release 25')
    manifest = json.loads(args.manifest.read_text(encoding='utf-8-sig'))
    groups = {}
    for part in manifest['parts']:
        mesh, node = part['mesh'].split('|', 1)
        groups.setdefault(mesh, []).append(node)
    clips = manifest['animations']
    errors = []
    with tempfile.TemporaryDirectory(prefix='j73-fbx-') as temporary:
        compilation = subprocess.run([javac, '--release', '25', '-classpath', str(jar), '-d', temporary, str(ROOT / 'tools' / 'InspectFbx.java')])
        if compilation.returncode:
            return compilation.returncode
        for mesh, nodes in groups.items():
            fbx = args.package / 'common' / 'media' / 'models_X' / (mesh + '.fbx')
            result = subprocess.run([str(java), '--enable-native-access=ALL-UNNAMED', '-cp', temporary + ';' + str(jar),
                                     'InspectFbx', str(args.game.resolve()), str(fbx.resolve()), *nodes], text=True, capture_output=True)
            print(result.stdout, end='')
            if result.returncode:
                errors.append(result.stderr.strip() or 'Native importer exited with an error')
            errors.extend(check_output(result.stdout, nodes, clips))
        animation = args.package / 'common' / 'media' / 'anims_X' / 'vehicles' / 'J73_Panels.fbx'
        result = subprocess.run([str(java), '--enable-native-access=ALL-UNNAMED', '-cp', temporary + ';' + str(jar),
                                 'InspectFbx', str(args.game.resolve()), str(animation.resolve())], text=True, capture_output=True)
        print(result.stdout, end='')
        if result.returncode:
            errors.append(result.stderr.strip() or 'Animation importer exited with an error')
        actual = set(re.findall(r'^ANIMATION .*? clip=(\S+)', result.stdout, re.M))
        imported = re.search(r'IMPORTED meshes=(\d+) animations=(\d+)', result.stdout)
        if actual != set(clips) or not imported or int(imported[2]) != len(clips):
            errors.append(f'Animation FBX does not export exactly {sorted(clips)}')
    for error in errors:
        print('ERROR: ' + error)
    print(f'{"FAIL" if errors else "PASS"}: native FBX mesh resolution and named clip checks')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
