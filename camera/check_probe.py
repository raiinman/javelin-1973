"""Check and package the development probe without installing or launching it."""
import argparse
from pathlib import Path
import shutil
import subprocess
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    package = root / 'DeadSignalCameraProbe'
    output = root.parent / 'build' / 'camera-probe'
    checks = output / 'checks'
    checks.mkdir(parents=True, exist_ok=True)
    jar = (args.game / 'projectzomboid.jar').resolve()
    java = (args.game / 'jre64' / 'bin' / 'java.exe').resolve()
    javac = shutil.which('javac')
    if not jar.is_file() or not java.is_file() or not javac:
        parser.error('Requires installed game and JDK 25 javac')
    subprocess.run([javac, '--release', '25', '-cp', str(jar), '-d', str(checks), str(root / 'tests' / 'ProbeCheck.java')], check=True)
    subprocess.run([str(java), '-Djava.awt.headless=true', '-cp', str(checks) + ';' + str(jar), 'ProbeCheck',
                    str(package / '42/media/lua/shared/DeadSignalCamera/Sample.lua'), str(root / 'tests/sample_test.lua'),
                    str(package / '42/media/lua/client/DeadSignalCameraProbe.lua'),
                    str(package / '42/media/lua/client/DeadSignalTexturedWorldProbe.lua')], cwd=args.game.resolve(), check=True)
    subprocess.run([str(java), '-Djava.awt.headless=true', '-cp', str(checks) + ';' + str(jar), 'ProbeCheck',
                    str(package / '42/media/lua/shared/DeadSignalCamera/Orbit.lua'), str(root / 'tests/orbit_test.lua')],
                    cwd=args.game.resolve(), check=True)
    files = sorted(path for path in package.rglob('*') if path.is_file())
    assert len(files) == 6, 'Unexpected runtime files'
    for path in files:
        assert path.suffix in {'.lua', '.info', '.txt'}
        text = path.read_text(encoding='utf-8').lower()
        assert 'require=' not in text, 'Probe must not depend on another mod'
        assert 'http://' not in text and 'https://' not in text and 'c:/' not in text and 'c:\\' not in text
    archive = output / 'DeadSignalCameraProbe.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zipped:
        for path in files:
            zipped.write(path, path.relative_to(package.parent).as_posix())
    with zipfile.ZipFile(archive) as zipped:
        assert zipped.testzip() is None
        assert len(zipped.namelist()) == 6
    print(f'PASS: six-file Lua-only package: {archive}')
    print('This command checks source behavior, syntax and packaging only. See camera/research.md for separate native results.')


if __name__ == '__main__':
    main()
