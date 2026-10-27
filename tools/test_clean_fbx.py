import struct
import tempfile
import unittest
from pathlib import Path

from clean_fbx import clean_fbx


class CleanFbxTests(unittest.TestCase):
    def test_offsets_paths_arrays_and_idempotence(self):
        for wide, version in ((False, 7400), (True, 7500)):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                header = struct.Struct('<QQQB' if wide else '<IIIB')
                null = bytes(header.size)

                def string(value):
                    return b'S'+struct.pack('<I', len(value))+value

                def node(name, props, count, offset):
                    return header.pack(offset+header.size+len(name)+len(props), count,
                                       len(props), len(name))+name+props

                prefix = b'Kaydara FBX Binary  \x00\x1a\x00'+struct.pack('<I', version)
                creator = node(b'Creator', string(b'private exporter'), 1, 27)
                child_start = 27+len(creator)+header.size+len(b'Objects')
                texture = node(b'P', string(b'C:\\Users\\private\\atlas.png'), 1, child_start)
                array = b'f'+struct.pack('<III', 2, 0, 8)+struct.pack('<ff', 1.25, -2.5)
                vertices = node(b'Vertices', array, 1, child_start+len(texture))
                children = texture+vertices+null
                parent_end = child_start+len(children)
                parent = header.pack(parent_end, 0, 0, 7)+b'Objects'+children
                path = Path(directory)/'sample.fbx'
                path.write_bytes(prefix+creator+parent+null+b'footer')
                clean_fbx(path)
                result = path.read_bytes()
                self.assertNotIn(b'private', result)
                self.assertNotIn(b'Creator', result)
                self.assertIn(string(b'atlas.png'), result)
                self.assertIn(array, result)
                end = header.unpack_from(result, 27)[0]
                self.assertEqual(result[end:end+header.size], null)
                clean_fbx(path)
                self.assertEqual(path.read_bytes(), result)
