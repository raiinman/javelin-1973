"""Original semantic swatch textures for the native Build 42 vehicle shader.

Mask RGB comes from shipped vehicle.frag and BaseVehicle.MASK constants.
All artwork is generated here with standard Python, without imported bitmaps.
"""
from pathlib import Path
import struct
import zlib

WIDTH, HEIGHT, CELL = 1024, 512, 32
ZONES = (
    'roof', 'hood', 'trunk', 'doorleft', 'doorright',
    'windowleft', 'windowright', 'windshield', 'rearglass',
    'headleft', 'headright', 'tailleft', 'tailright',
    'guardfl', 'guardfr', 'guardrl', 'guardrr', 'neutral',
    'brakeleft', 'brakeright',
)
MASK_RGB = {
    'roof': (0, 0, 0), 'hood': (255, 0, 127), 'trunk': (0, 255, 127),
    'doorleft': (255, 0, 255), 'doorright': (0, 255, 255),
    'windowleft': (127, 0, 127), 'windowright': (0, 127, 127),
    'windshield': (127, 0, 0), 'rearglass': (0, 127, 0),
    'headleft': (191, 0, 0), 'headright': (64, 0, 0),
    'tailleft': (0, 64, 0), 'tailright': (0, 191, 0),
    'guardfl': (0, 191, 191), 'guardfr': (191, 0, 191),
    'guardrl': (191, 191, 0), 'guardrr': (0, 0, 191),
    'neutral': (255, 255, 255),
    'brakeleft': (127, 191, 0), 'brakeright': (127, 64, 0),
}
GLASS = {'windowleft', 'windowright', 'windshield', 'rearglass'}
LIGHTS = {'headleft', 'headright', 'tailleft', 'tailright', 'brakeleft', 'brakeright'}


def _chunk(kind, data):
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)


def _png(path, pixels):
    stride = WIDTH * 4
    # Atlas coordinates start at bottom left, PNG scanlines start at top left.
    rows = b''.join(b'\0' + pixels[y * stride:(y + 1) * stride] for y in reversed(range(HEIGHT)))
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + _chunk(b'IHDR', struct.pack('>IIBBBBB', WIDTH, HEIGHT, 8, 6, 0, 0, 0))
                     + _chunk(b'IDAT', zlib.compress(rows, 9)) + _chunk(b'IEND', b''))


class SurfaceAtlas:
    """Stable slot mapping shared by generated PNGs and Blender face UVs."""
    def __init__(self, colours):
        self.colours = tuple(colours)
        if not self.colours or len(self.colours) * len(ZONES) > WIDTH * HEIGHT // CELL ** 2:
            raise ValueError('Semantic atlas requires 1 to 25 colours')
        self.manifest = {
            'width': WIDTH, 'height': HEIGHT, 'cellSize': CELL,
            'columns': WIDTH // CELL, 'rows': HEIGHT // CELL,
            'zones': list(ZONES), 'colours': list(self.colours),
            'slotCount': len(ZONES) * len(self.colours),
            'origin': 'bottom-left', 'paintAlpha': 255,
        }
        self.textures = {
            'texture': 'Vehicles/J73_Palette',
            'textureMask': 'Vehicles/J73_Mask',
            'textureLights': 'Vehicles/J73_Lights',
            'textureRust': 'Vehicles/J73_Rust',
            'textureDamage1Overlay': 'Vehicles/J73_Damage1',
            'textureDamage1Shell': 'Vehicles/J73_Blank',
            'textureDamage2Overlay': 'Vehicles/J73_Damage2',
            'textureDamage2Shell': 'Vehicles/J73_Blank',
        }

    def slot(self, zone, colour):
        return ZONES.index(zone) * len(self.colours) + self.colours.index(colour)

    def uv(self, zone, colour, local_uv=(.5, .5)):
        """Return a UV within a semantic cell, with a two-pixel filter margin."""
        if len(local_uv) != 2 or any(not 0 <= value <= 1 for value in local_uv):
            raise ValueError('local_uv must contain two values in [0,1]')
        slot = self.slot(zone, colour)
        x, y = slot % (WIDTH // CELL), slot // (WIDTH // CELL)
        return ((x * CELL + 2 + local_uv[0] * (CELL - 4)) / WIDTH,
                (y * CELL + 2 + local_uv[1] * (CELL - 4)) / HEIGHT)


def build_atlases(media, colours):
    """Write semantic PNGs beneath media/textures/Vehicles and return UV helpers.

    colours is an insertion-ordered mapping of swatch names to #RRGGBB strings.
    All generated models use shader=vehicle for the native imported UV layout.
    Palette alpha stays 255 so the shader preserves the authored red paint.
    """
    atlas = SurfaceAtlas(colours)
    output = Path(media) / 'textures' / 'Vehicles'
    output.mkdir(parents=True, exist_ok=True)
    images = {name: bytearray(WIDTH * HEIGHT * 4) for name in
              ('Palette', 'Mask', 'Lights', 'Rust', 'Damage1', 'Damage2', 'Blank', 'Blood')}
    images['Palette'][:] = bytes((20, 20, 20, 255)) * (WIDTH * HEIGHT)
    images['Mask'][:] = bytes((255, 255, 255, 255)) * (WIDTH * HEIGHT)
    for zone in ZONES:
        for colour, value in colours.items():
            if len(value) != 7 or not value.startswith('#'):
                raise ValueError(f'Expected #RRGGBB colour: {colour}')
            base = tuple(int(value[index:index + 2], 16) for index in (1, 3, 5))
            slot = atlas.slot(zone, colour)
            x0, y0 = (slot % 32) * CELL, (slot // 32) * CELL
            for dy in range(CELL):
                for dx in range(CELL):
                    offset = ((y0 + dy) * WIDTH + x0 + dx) * 4
                    pixels = {'Palette': (*base, 255), 'Mask': (*MASK_RGB[zone], 255)}
                    if colour=='grille':
                        # Original expanded-metal weave. The sampled28px tile
                        # repeats at its edges and remains opaque for vehicle paint.
                        wire=((dx-2+2*(dy-2))%14<3 or (dx-2-2*(dy-2))%14<3)
                        pixels['Palette']=(168,177,181,255) if wire else (17,21,24,255)
                    if zone in LIGHTS:
                        lamp = (255, 245, 212) if zone.startswith('head') else (255, 24, 12)
                        pixels['Lights'] = (*lamp, 255)
                    elif zone != 'neutral':
                        # Original repeatable small scratches, sampled only when worn.
                        scratch = ((dx + 2 * dy + slot) % 19 <= 1)
                        if zone in GLASS:
                            pixels['Damage1'] = (181, 190, 193, 95 if scratch else 12)
                            pixels['Damage2'] = (158, 170, 177, 190 if scratch else 65)
                        else:
                            grain = (dx * 17 + dy * 31 + slot * 7) % 97
                            pixels['Rust'] = (112 + grain // 5, 63 + grain // 8, 31, 75 if grain < 17 else 12)
                            pixels['Damage1'] = (105, 109, 112, 125 if scratch else 10)
                            pixels['Damage2'] = (76, 80, 83, 205 if scratch else 35)
                    for image, pixel in pixels.items():
                        images[image][offset:offset + 4] = bytes(pixel)
    for name, pixels in images.items():
        _png(output / f'J73_{name}.png', pixels)
    return atlas
