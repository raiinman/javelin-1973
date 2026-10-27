"""Check native-camera Lua with the installed Kahlua runtime and package it."""
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
    package = root / 'DeadSignalCamera'
    output = root.parent / 'build/camera'
    checks = output / 'checks'
    checks.mkdir(parents=True, exist_ok=True)
    jar = (args.game / 'projectzomboid.jar').resolve()
    java = (args.game / 'jre64/bin/java.exe').resolve()
    javac = shutil.which('javac')
    if not javac or not jar.is_file() or not java.is_file():
        parser.error('Installed game and JDK 25 required for development checks')
    subprocess.run([javac, '--release', '25', '-cp', str(jar), '-d', str(checks), str(root/'tests/ProbeCheck.java'),
                    str(root/'tests/CameraRuntimeCheck.java')], check=True)
    client = package / '42/media/lua/client/DeadSignalCamera.lua'
    subprocess.run([str(java), '-Djava.awt.headless=true', '-cp', str(checks)+';'+str(jar), 'ProbeCheck',
                    str(root/'tests/experimental_state.lua'), str(root/'tests/camera_state_test.lua'),
                    str(client), str(package/'42/media/lua/client/DeadSignalCamera/Controls.lua')], cwd=args.game.resolve(), check=True)
    subprocess.run([str(java), '-Djava.awt.headless=true', '-cp', str(checks)+';'+str(jar), 'ProbeCheck',
                    str(root/'tests/experimental_bridge.lua'), str(root/'tests/camera_bridge_test.lua'),
                    str(client)], cwd=args.game.resolve(), check=True)
    subprocess.run([str(java), '-Djava.awt.headless=true', '-cp', str(checks)+';'+str(jar), 'CameraRuntimeCheck',
                    str(root/'tests/experimental_state.lua'),
                    str(root/'tests/experimental_bridge.lua'), str(root/'tests/camera_runtime_test.lua'),
                    str(client)], cwd=args.game.resolve(), check=True)
    files = sorted(p for p in package.rglob('*') if p.is_file())
    for path in files:
        assert path.suffix in {'.lua', '.info', '.txt'}
        content = path.read_text(encoding='utf-8').lower()
        assert not any(token in content for token in ['require=', 'http://', 'https://', 'c:/', 'c:\\'])
    workshop = output / 'Workshop/DeadSignalCamera'
    target = workshop / 'Contents/mods/DeadSignalCamera'
    target.mkdir(parents=True, exist_ok=True)
    for stale in target.rglob('*'):
        if stale.is_file() and not (package/stale.relative_to(target)).is_file():
            stale.unlink()
    for path in files:
        dest = target/path.relative_to(package)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path,dest)
    (workshop/'workshop.txt').write_text('version=1\ntitle=Dead Signal Camera\ndescription=Native zoom presets and camera-pan binding guidance. Fixed isometric orientation.\ntags=Interface;Build 42\nvisibility=private\n',encoding='utf-8')
    archive = output/'DeadSignalCamera.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as zipped:
        for path in files:
            zipped.write(path,path.relative_to(package.parent).as_posix())
    with zipfile.ZipFile(archive) as zipped:
        assert zipped.testzip() is None
    print(f'PASS: standalone package ({len(files)} files): {archive}')
    print('Native gameplay verification is separate. Nothing was installed or published.')


if __name__ == '__main__':
    main()
