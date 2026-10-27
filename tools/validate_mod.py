"""Dependency-free package checks. These do not replace a game driving test."""
import argparse
import json
import math
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD_ID = 'Javelin73PC'


def clean(text):
    return re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S)


def balanced(text):
    text = re.sub(r'"(?:\\.|[^"\\])*"', '""', clean(text))
    depth = 0
    for char in text:
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
        if depth < 0:
            return False
    return depth == 0


def media_path(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Asset reference escapes media: {value}')
    return path


def interaction_clearance_errors(text):
    """Mirror native area target placement against its 0.15m padded nav polygon."""
    extents = re.search(r'\bextents\s*=\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', text)
    if not extents:
        return []
    width, _, length = map(float, extents.groups())
    errors = []
    for name, values in re.findall(r'\barea\s+(\w+)\s*\{\s*xywh\s*=\s*([^,}]+)', text):
        x, y, area_width, area_height = map(float, values.split())
        side = abs(x)>width/2
        target = abs(x)-area_width*.3 if side else abs(y)-area_height*.3
        obstacle = (width if side else length)/2+.15
        if target-obstacle<.025:
            errors.append(f'Interaction area {name} target overlaps native navigation padding '
                          f'or lacks clearance: {target-obstacle:.3f}m')
    return errors


def physics_origin_errors(text):
    """Keep the native rigid-body origin above ground after suspension travel."""
    model = re.search(r'\bmodel\s*\{[^}]*\boffset\s*=\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', text)
    rest = re.search(r'\bsuspensionRestLength\s*=\s*([-\d.]+)', text)
    if not model or not rest:
        return []
    model_y = float(model[2])
    errors = []
    for name, wheel in re.findall(r'\bwheel\s+(\w+)\s*\{([^}]+)', text):
        offset = re.search(r'\boffset\s*=\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', wheel)
        radius = re.search(r'\bradius\s*=\s*([-\d.]+)', wheel)
        if offset and radius:
            margin = float(radius[1])-float(offset[2])-model_y-float(rest[1])
            if margin<.05:
                errors.append(f'Wheel {name} may settle the native physics origin below ground: '
                              f'suspension clearance {margin:.3f}m')
    return errors


def validate(package, game=None, manifest=None):
    package = Path(package).resolve()
    game = Path(game).resolve() if game else None
    errors, notes = [], []
    info = package / '42' / 'mod.info'
    if not info.is_file():
        errors.append('Missing 42/mod.info')
    elif not re.search(r'^id\s*=\s*Javelin73PC\s*$', info.read_text(encoding='utf-8-sig'), re.M):
        errors.append('42/mod.info must declare id=Javelin73PC')
    for relative in ['42/media/scripts', 'common/media/models_X', 'common/media/textures']:
        if not (package / relative).is_dir():
            errors.append(f'Missing {relative}')
    files = [path for path in package.rglob('*') if path.is_file() and path.name != 'AGENTS.md']
    scripts = {path: clean(path.read_text(encoding='utf-8-sig')) for path in files if path.suffix == '.txt' and 'scripts' in path.parts}
    lua = {path: path.read_text(encoding='utf-8-sig') for path in files if path.suffix == '.lua'}
    for path in files:
        if re.search(r'en72_Javelin|DSI_', path.relative_to(package).as_posix(), re.I):
            errors.append(f'Forbidden donor filename: {path.relative_to(package)}')
        if path.is_symlink():
            errors.append(f'Symlink not allowed in package: {path.relative_to(package)}')
        if path.suffix.lower() in ('.lua', '.txt', '.info', '.xml'):
            text = path.read_text(encoding='utf-8-sig')
            if re.search(r'en72_Javelin|DSI_', text, re.I):
                errors.append(f'Forbidden donor reference: {path.relative_to(package)}')
    for path, text in scripts.items():
        if not balanced(text):
            errors.append(f'Unbalanced script braces: {path.relative_to(package)}')
        if re.search(r'\bvehicle\s+Javelin73PC\s*\{', text):
            errors.extend(interaction_clearance_errors(text))
            errors.extend(physics_origin_errors(text))
    combined = '\n'.join(scripts.values())
    if not re.search(r'\bvehicle\s+Javelin73PC\s*\{', combined):
        errors.append('Missing vehicle Javelin73PC definition')
    models = set(re.findall(r'\bmodel\s+(\w+)\s*\{', combined))
    for name in re.findall(r'\bfile\s*=\s*(J73_\w+)\s*,', combined):
        if name not in models:
            errors.append(f'Missing model definition: {name}')
    media = package / 'common' / 'media'
    mesh_refs = re.findall(r'\bmesh\s*=\s*([^,\n]+)', combined)
    for ref in mesh_refs:
        mesh = ref.strip().split('|')[0]
        try:
            path = media_path(media / 'models_X', mesh + '.fbx')
            if not path.is_file():
                errors.append(f'Missing model asset: {mesh}.fbx')
            elif not path.read_bytes().startswith(b'Kaydara FBX Binary  \x00\x1a\x00'):
                errors.append(f'Invalid binary FBX header: {mesh}.fbx')
        except ValueError as error:
            errors.append(str(error))
    for ref in re.findall(r'\b(?:texture|textureMask|textureLights|textureDamage1Overlay|textureDamage1Shell|textureDamage2Overlay|textureDamage2Shell|textureRust|textureShadow)\s*=\s*([^,\n]+)', combined):
        ref = ref.strip()
        if ref.lower() in ('null', ''):
            continue
        try:
            choices = [media_path(base / 'textures', ref + '.png') for base in (media, package / '42' / 'media')]
            if game:
                choices.append(media_path(game / 'media' / 'textures', ref + '.png'))
            if not any(path.is_file() for path in choices):
                # Vanilla packed textures are checked against game script usage below.
                if not game:
                    errors.append(f'Missing texture asset: {ref}.png')
                elif ref.startswith(('Vehicles/J73_', 'J73_')):
                    errors.append(f'Missing texture asset: {ref}.png')
        except ValueError as error:
            errors.append(str(error))
    for path in files:
        if path.suffix.lower() == '.png':
            data = path.read_bytes()
            if len(data) < 33 or data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR':
                errors.append(f'Invalid PNG header: {path.relative_to(package)}')
            else:
                width, height = struct.unpack('>II', data[16:24])
                if not (0 < width <= 8192 and 0 < height <= 8192):
                    errors.append(f'Invalid PNG dimensions: {path.relative_to(package)} {width}x{height}')
                notes.append(f'PNG {path.relative_to(package)}: {width}x{height}')
    if manifest is None:
        manifest = package.parent / 'assets' / 'model-manifest.json'
    if Path(manifest).is_file():
        try:
            data = json.loads(Path(manifest).read_text(encoding='utf-8-sig'))
            if data.get('vehicle') != 'Base.Javelin73PC' or data.get('units') != 'metres':
                errors.append('Manifest must declare Base.Javelin73PC in metres')
            if not data.get('parts'):
                errors.append('Manifest contains no model parts')
            for part in data.get('parts', []):
                if part['model'] not in models:
                    errors.append(f'Manifest model absent from definitions: {part["model"]}')
                if part['mesh'] not in [ref.strip() for ref in mesh_refs]:
                    errors.append(f'Manifest mesh absent from definitions: {part["mesh"]}')
                if part.get('vertices', 0) <= 0 or part.get('triangles', 0) <= 0:
                    errors.append(f'Empty manifest geometry: {part["name"]}')
                bounds = part['bounds']
                if len(bounds) != 2 or any(len(point) != 3 for point in bounds) or not all(math.isfinite(value) for point in bounds for value in point):
                    errors.append(f'Invalid bounds: {part["name"]}')
                elif any(a > b for a, b in zip(*bounds)):
                    errors.append(f'Inverted bounds: {part["name"]}')
                mesh, _, obj = part['mesh'].partition('|')
                fbx = media_path(media / 'models_X', mesh + '.fbx')
                if fbx.is_file() and obj and obj.encode() not in fbx.read_bytes():
                    errors.append(f'FBX object missing: {part["mesh"]}')
            notes.append(f'Manifest: {len(data.get("parts", []))} original model parts')
        except (ValueError, KeyError, TypeError) as error:
            errors.append(f'Invalid manifest: {error}')
    else:
        errors.append('Missing assets/model-manifest.json (use --manifest for installed packages)')
    if game:
        if not (game / 'media' / 'scripts').is_dir():
            errors.append(f'Game scripts directory missing: {game}')
        else:
            native_scripts = '\n'.join(path.read_text(encoding='utf-8-sig', errors='replace') for path in (game / 'media' / 'scripts').rglob('*.txt'))
            templates = set(re.findall(r'\btemplate\s+vehicle\s+(\w+)', native_scripts + '\n' + combined))
            for name in re.findall(r'\btemplate!?\s*=\s*([^,\n]+)', combined):
                base = name.strip().split('/')[0].removeprefix('Base.')
                if base not in templates:
                    errors.append(f'Unknown native vehicle template: {name.strip()}')
            native_lua = '\n'.join(path.read_text(encoding='utf-8-sig', errors='replace') for path in (game / 'media' / 'lua').rglob('*.lua'))
            for callback in set(re.findall(r'=\s*(Vehicles\.\w+\.\w+)\s*,', combined)):
                if not re.search(r'(?:function\s+' + re.escape(callback) + r'\s*\(|' + re.escape(callback) + r'\s*=)', native_lua + '\n' + '\n'.join(lua.values())):
                    errors.append(f'Undefined vehicle callback: {callback}')
            notes.append(f'Native template and callback references checked against {game.name}')
    else:
        notes.append('Native template/callback checks skipped, pass --game to enable')
    notes.append('Static checks only; Lua syntax, animation playback and driving need runtime checks')
    return errors, notes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=ROOT / MOD_ID)
    parser.add_argument('--game', type=Path)
    parser.add_argument('--manifest', type=Path)
    args = parser.parse_args()
    errors, notes = validate(args.package, args.game, args.manifest)
    for note in notes:
        print(note)
    for error in errors:
        print('ERROR: ' + error)
    print(f'{"PASS" if not errors else "FAIL"}: {len(errors)} error(s)')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
