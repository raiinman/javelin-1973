"""Check original Fast Load runtime against the installed game's Kahlua, then ZIP it."""
import argparse
from pathlib import Path
import shutil
import subprocess
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--game', required=True, type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parent
package = root / 'DeadSignalFastLoad'
output = root.parent / 'build/fast-load'
classes = output / 'checks'
classes.mkdir(parents=True, exist_ok=True)
jar = (args.game / 'projectzomboid.jar').resolve()
javac = shutil.which('javac') or 'C:/Program Files/Eclipse Adoptium/jdk-25.0.3.9-hotspot/bin/javac.exe'
subprocess.run([javac, '--release', '25', '-cp', str(jar), '-d', str(classes), str(root / 'tests/FastLoadCheck.java')], check=True)
source = package / '42/media/lua/client/DeadSignalFastLoad.lua'
subprocess.run([str((args.game / 'jre64/bin/java.exe').resolve()), '-Djava.awt.headless=true', '-cp', str(classes) + ';' + str(jar),
                'FastLoadCheck', str(root / 'tests/fixture.lua'),
                'compile-only:' + str(package / '42/media/lua/client/DeadSignalFastLoad/StartupOrder.lua'),
                'compile-only:' + str(package / '42/media/lua/client/DeadSignalFastLoad/StartupScene.lua'),
                'compile-only:' + str(package / '42/media/lua/client/DeadSignalFastLoad/SurvivalTips.lua'),
                'compile-only:' + str(package / '42/media/lua/client/DeadSignalFastLoad/TipIndex.lua'),
                str(source), str(root / 'tests/lifecycle.lua')],
               cwd=args.game.resolve(), check=True)
files = sorted(path for path in package.rglob('*') if path.is_file())
assert len(files) >= 4
for path in files:
    assert path.suffix in {'.lua', '.info', '.txt', '.json', '.png'}
    if path.suffix == '.png':
        continue
    text = path.read_text(encoding='utf-8').lower()
    assert not any(value in text for value in ('http://', 'https://', 'c:/', 'c:\\', 'require=', 'pztoolkitbridge', 'getclassfield', 'ingamestate.new'))
archive = output / 'DeadSignalFastLoad.zip'
workshop = output / 'Workshop/DeadSignalFastLoad'
target = workshop / 'Contents/mods/DeadSignalFastLoad'
target.mkdir(parents=True, exist_ok=True)
# Remove old mod-owned translation files before copying the current tip catalog.
for obsolete in (target / '42/media/lua/shared/Translate').glob('*/UI.json'):
    obsolete.unlink()
for path in files:
    destination = target / path.relative_to(package)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)
(workshop / 'workshop.txt').write_text(
    'version=1\ntitle=Dead Signal Fast Load\n'
    'description=120 survival tips in native save loading and a shuffled menu carousel, rain artwork, selected-save mod matching, backup and Undo. Never auto-loads saves. Required loading remains.\n'
    'tags=Interface;Build 42\nvisibility=private\n', encoding='utf-8')
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zipped:
    for path in files:
        zipped.write(path, path.relative_to(root).as_posix())
with zipfile.ZipFile(archive) as zipped:
    assert zipped.testzip() is None and len(zipped.namelist()) == len(files)
print('PASS: independent Workshop-format package:', archive)
print('Native logo, startup timings and gameplay remain separate verification gates.')
