import unittest
from check_fbx_import import check_output


class FbxOutputTests(unittest.TestCase):
    def test_asymmetric_nose_anchor_rejects_raw_right_handed_import(self):
        output = 'IMPORTED meshes=1 animations=0\nRESOLVED J73Mesh_Hood mesh=x\n'
        correct = output+'RENDER_BOUNDS J73Mesh_Hood [-80, 8, 81] [80, 18, 234]\n'
        reversed_axis = output+'RENDER_BOUNDS J73Mesh_Hood [-80, 8, -234] [80, 18, -81]\n'
        self.assertEqual(check_output(correct, ['J73Mesh_Hood'], []), [])
        self.assertTrue(any('orientation' in error for error in check_output(reversed_axis, ['J73Mesh_Hood'], [])))

    def test_exact_mesh_and_clip_pass(self):
        output = 'IMPORTED meshes=1 animations=1\nRESOLVED Body mesh=Body\nANIMATION name=x|Panels clip=Panels duration=30\n'
        self.assertEqual(check_output(output, ['Body'], ['Panels']), [])

    def test_split_mesh_and_missing_clip_fail(self):
        output = 'IMPORTED meshes=19 animations=1\nRESOLVED Body mesh=Body\nANIMATION name=Scene clip=Scene duration=30\n'
        errors = check_output(output, ['Body'], ['Panels'])
        self.assertTrue(any('material split' in error for error in errors))
        self.assertTrue(any('Expected clips' in error for error in errors))

    def test_unresolved_node_fails(self):
        self.assertTrue(check_output('IMPORTED meshes=1 animations=0\nUNRESOLVED Body\n', ['Body'], []))


if __name__ == '__main__':
    unittest.main()
