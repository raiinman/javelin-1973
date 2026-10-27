import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from surface_maps import build_atlases, MASK_RGB, SurfaceAtlas, WIDTH, HEIGHT


def rgba_at(path, uv):
    data = path.read_bytes()
    cursor, compressed = 8, bytearray()
    while cursor < len(data):
        length = struct.unpack('>I', data[cursor:cursor + 4])[0]
        if data[cursor + 4:cursor + 8] == b'IDAT':
            compressed.extend(data[cursor + 8:cursor + 8 + length])
        cursor += length + 12
    pixels = zlib.decompress(compressed)
    x, y = int(uv[0] * WIDTH), HEIGHT - 1 - int(uv[1] * HEIGHT)
    offset = y * (WIDTH * 4 + 1) + 1 + x * 4
    return tuple(pixels[offset:offset + 4])


class SurfaceMapTests(unittest.TestCase):
    def test_semantic_masks_and_lamp_alpha(self):
        with tempfile.TemporaryDirectory() as folder:
            atlas = build_atlases(folder, {'red': '#ba2928', 'chrome': '#b7bdc3'})
            output = Path(folder) / 'textures' / 'Vehicles'
            for zone, mask in MASK_RGB.items():
                uv = atlas.uv(zone, 'red')
                self.assertEqual(rgba_at(output / 'J73_Mask.png', uv), (*mask, 255))
                self.assertEqual(rgba_at(output / 'J73_Palette.png', uv), (186, 41, 40, 255))
            self.assertEqual(rgba_at(output / 'J73_Lights.png', atlas.uv('headleft', 'red'))[3], 255)
            self.assertEqual(rgba_at(output / 'J73_Lights.png', atlas.uv('brakeleft', 'red'))[3], 255)
            self.assertEqual(rgba_at(output / 'J73_Lights.png', atlas.uv('hood', 'red'))[3], 0)
            self.assertEqual(rgba_at(output / 'J73_Blank.png', atlas.uv('hood', 'red')), (0, 0, 0, 0))

    def test_capacity_and_bad_uv_rejected(self):
        with self.assertRaises(ValueError):
            SurfaceAtlas({str(i): '#000000' for i in range(26)})
        with self.assertRaises(ValueError):
            SurfaceAtlas({'red': '#ff0000'}).uv('hood', 'red', (2, 0))

    def test_original_grille_tile_repeats_and_preserves_native_mask(self):
        with tempfile.TemporaryDirectory() as folder:
            atlas=build_atlases(folder,{'grille':'#575b5f'})
            output=Path(folder)/'textures/Vehicles'
            samples=set()
            for i in range(29):
                t=i/28
                for a,b in (((0,t),(1,t)),((t,0),(t,1))):
                    first=rgba_at(output/'J73_Palette.png',atlas.uv('neutral','grille',a))
                    second=rgba_at(output/'J73_Palette.png',atlas.uv('neutral','grille',b))
                    self.assertEqual(first,second)
                    self.assertEqual(first[3],255)
                    samples.add(first[:3])
            self.assertGreater(len(samples),1)
            self.assertEqual(rgba_at(output/'J73_Mask.png',atlas.uv('neutral','grille')),
                             (*MASK_RGB['neutral'],255))


if __name__ == '__main__':
    unittest.main()
