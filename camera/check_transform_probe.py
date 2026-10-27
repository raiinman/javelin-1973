"""Compile the experimental image-transform mod and test its visual transport."""
import argparse
from pathlib import Path
import shutil
import subprocess
import zipfile

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    package=root/'DeadSignalCameraTransformProbe'
    output=root.parent/'build/camera-transform-probe'
    checks=output/'checks'
    checks.mkdir(parents=True,exist_ok=True)
    jar=(args.game/'projectzomboid.jar').resolve()
    java=(args.game/'jre64/bin/java.exe').resolve()
    javac=shutil.which('javac')
    if not javac or not jar.is_file() or not java.is_file(): parser.error('Installed game and JDK required')
    subprocess.run([javac,'--release','25','-cp',str(jar),'-d',str(checks),str(root/'tests/ProbeCheck.java')],check=True)
    subprocess.run([str(java),'-Djava.awt.headless=true','-cp',str(checks)+';'+str(jar),'ProbeCheck',
        str(package/'42/media/lua/shared/DeadSignalCameraTransform/Transport.lua'),str(root/'tests/transform_transport_test.lua'),
        str(package/'42/media/lua/client/DeadSignalCameraTransformProbe.lua')],cwd=args.game.resolve(),check=True)
    files=sorted(path for path in package.rglob('*') if path.is_file())
    assert len(files)==5
    for path in files:
        assert path.suffix in {'.lua','.vert','.info','.txt'}
        content=path.read_text(encoding='utf-8').lower()
        assert not any(token in content for token in ['http://','https://','c:/','c:\\','require='])
    shader=(package/'42/media/shaders/screen.vert').read_text()
    assert '#version 330' in shader and 'SearchMode.x > 31.5' in shader and 'VarInfo.x == 0.0' in shader
    archive=output/'DeadSignalCameraTransformProbe.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as zipped:
        for path in files: zipped.write(path,path.relative_to(package.parent).as_posix())
    with zipfile.ZipFile(archive) as zipped: assert zipped.testzip() is None
    print('PASS: five-file standalone transform probe; shader driver compilation and gameplay remain native gates')

if __name__=='__main__': main()
