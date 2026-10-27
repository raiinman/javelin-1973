"""Exercise the headliner geometry ray gate in a disposable Blender scene."""
from pathlib import Path
import subprocess
import unittest


BLENDER = Path('C:/Program Files/Blender Foundation/Blender 5.2/blender.exe')


@unittest.skipUnless(BLENDER.is_file(), 'Requires installed Blender')
class CabinSheetChecks(unittest.TestCase):
    def test_supported_occluded_and_detached_ribbons(self):
        source = r'''
import bpy
import sys
sys.path.insert(0, sys.argv[sys.argv.index('--')+1])
from check_vehicle_placement import check_headliner_clearance
mesh = bpy.data.meshes.new('test_headliner')
mesh.from_pydata([(-1,-1,.6),(1,-1,.6),(1,1,.6),(-1,1,.6),
                  (-.5,-.5,.599),(.5,-.5,.599),(.5,.5,.599),(-.5,.5,.599)],
                 [], [(0,3,2,1),(4,7,6,5)])
mesh.update()
def check():
    check_headliner_clearance(mesh, list(mesh.polygons),
                             lambda face: 'seat' if face.index == 0 else 'cream')
check()
for z, x_shift, reason in ((.601,0,'occluded'),(.590,0,'detached'),(.599,3,'unsupported')):
    for vertex in mesh.vertices[4:]:
        vertex.co.z = z
        vertex.co.x += x_shift
    mesh.update()
    try:
        check()
    except AssertionError:
        print('EXPECTED_REJECTION', reason)
    else:
        raise AssertionError('Accepted '+reason+' ribbon')
print('CABIN_RAY_NEGATIVE_CHECKS_PASS')
'''
        result = subprocess.run(
            [str(BLENDER), '--background', '--factory-startup', '--python-exit-code', '1',
             '--python-expr', source, '--', str(Path(__file__).resolve().parent)],
            capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('CABIN_RAY_NEGATIVE_CHECKS_PASS', result.stdout)


if __name__ == '__main__':
    unittest.main()
