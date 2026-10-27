"""Validate and copy only this project's Build 42 package, preserving owned backups."""
import argparse
import hashlib
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from validate_mod import MOD_ID, ROOT, validate

MARKER = '.j73-install.json'


def install(source, destination, update=False):
    source, destination = Path(source).resolve(), Path(destination).absolute()
    if destination.name != MOD_ID or destination.is_symlink():
        raise ValueError('Destination must be a separate directory named Javelin73PC')
    resolved = destination.resolve()
    if source == resolved or source.is_relative_to(resolved) or resolved.is_relative_to(source):
        raise ValueError('Source and destination must be separate trees')
    if destination.exists():
        marker = destination / MARKER
        try:
            owned = json.loads(marker.read_text(encoding='utf-8')).get('mod_id') == MOD_ID
        except (OSError, ValueError):
            owned = False
        if not owned:
            raise ValueError('Existing destination is not owned by this installer; nothing changed')
        if not update:
            raise ValueError('Already installed; pass --update to preserve a backup and replace it')
    payload = []
    for directory in ('42', 'common'):
        for path in (source / directory).rglob('*'):
            if path.is_symlink():
                raise ValueError(f'Symlinks cannot be installed: {path}')
            if path.is_file() and path.name != 'AGENTS.md' and '__pycache__' not in path.parts:
                payload.append(path)
    if not payload:
        raise ValueError('No package payload found')
    destination.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    with tempfile.TemporaryDirectory(prefix='j73-stage-', dir=destination.parent) as temporary:
        stage = Path(temporary) / MOD_ID
        stage.mkdir()
        hashes = {}
        for path in payload:
            relative = path.relative_to(source)
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            expected = hashlib.sha256(path.read_bytes()).hexdigest()
            if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                raise OSError(f'Copied file differs: {relative}')
            hashes[relative.as_posix()] = expected
        (stage / MARKER).write_text(json.dumps({'mod_id': MOD_ID, 'files': hashes}, indent=2) + '\n', encoding='utf-8')
        if destination.exists():
            backups = destination.parent.parent / 'Javelin73PC-backups'
            backups.mkdir(exist_ok=True)
            backup = backups / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            destination.rename(backup)
        try:
            stage.rename(destination)
        except OSError:
            if backup:
                backup.rename(destination)
            raise
    return backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / MOD_ID)
    parser.add_argument('--destination', type=Path, default=Path.home() / 'Zomboid' / 'mods' / MOD_ID)
    parser.add_argument('--game', type=Path)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--validate', action='store_true', help='Validate only; leave destination untouched')
    args = parser.parse_args()
    errors, notes = validate(args.source, args.game, args.manifest)
    if errors:
        for error in errors:
            print('ERROR: ' + error)
        return 1
    if args.validate:
        print('PASS: source package validated; no files installed')
        return 0
    try:
        backup = install(args.source, args.destination, args.update)
    except (OSError, ValueError) as error:
        print('ERROR: ' + str(error))
        return 1
    print(f'Installed {MOD_ID}: {args.destination}')
    if backup:
        print(f'Previous version preserved: {backup}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
