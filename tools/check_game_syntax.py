"""Compile packaged Lua and parse vehicle scripts with installed game classes."""
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from validate_mod import ROOT, MOD_ID


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', required=True, type=Path)
    parser.add_argument('--package', type=Path, default=ROOT / MOD_ID)
    args = parser.parse_args()
    jar = args.game / 'projectzomboid.jar'
    java = args.game / 'jre64' / 'bin' / 'java.exe'
    javac = shutil.which('javac')
    if not jar.is_file() or not java.is_file() or not javac:
        parser.error('Requires installed game jar/runtime and javac supporting --release 25')
    files = sorted(path.resolve() for path in args.package.rglob('*') if path.is_file() and (path.suffix == '.lua' or (path.suffix == '.txt' and 'scripts' in path.parts)))
    if not files:
        parser.error('Package contains no Lua or vehicle scripts')
    with tempfile.TemporaryDirectory(prefix='j73-syntax-') as temporary:
        compilation = subprocess.run([javac, '--release', '25', '-classpath', str(jar), '-d', temporary, str(ROOT / 'tools' / 'GameSyntaxCheck.java')])
        if compilation.returncode:
            return compilation.returncode
        return subprocess.run([str(java), '-Djava.awt.headless=true', '-cp', temporary + ';' + str(jar), 'GameSyntaxCheck', *map(str, files)]).returncode


if __name__ == '__main__':
    raise SystemExit(main())
