"""Original rear Michigan plate artwork from the supplied restored car.

All glyph paths are authored vectors, without imported fonts or image pixels.
The reference's bottom web address is deliberately absent from game geometry.
"""
import math
from javelin_decals import GLYPHS, stroke


_GLYPHS = dict(GLYPHS, **{
    'N': (((0, 0), (0, 1), (1, 0), (1, 1)),),
    'S': (((1, .88), (.78, 1), (.22, 1), (0, .82), (0, .64),
           (.20, .53), (.78, .47), (1, .34), (1, .16), (.78, 0),
           (.22, 0), (0, .13)),),
    'U': (((0, 1), (0, .20), (.22, 0), (.78, 0), (1, .20), (1, 1)),),
})


def _text(part, text, width, height, centre_x, centre_z, y, colour,
          stroke_ratio=.075):
    advance = width / len(text)
    glyph_width = advance * .71
    point = lambda u, v: (centre_x + u, y, centre_z + v)
    for index, char in enumerate(text):
        origin = (index - (len(text) - 1) / 2) * advance - glyph_width / 2
        for path in _GLYPHS[char]:
            stroke(part, [(origin + u * glyph_width, (v - .5) * height)
                          for u, v in path], height * stroke_ratio,
                   point, colour, (0, -1, 0), round_joins=True)


def build_plate(body, tail_face):
    """Append the rear plate within the existing .29 x .14 metre envelope.

    Readable registration is BOBSAMX. O/0 and S/5 remain photographically
    ambiguous; the visible rounded letterforms are drawn directly here.
    """
    centre_z = .325
    centre_y = tail_face - .082
    face_y = centre_y - .0093
    body.rounded_plate((0, centre_y, centre_z), (.29, .017, .14),
                       .009, 'cream', segments=6)
    # Fine navy perimeter follows the softly rounded stamped plate edge.
    perimeter = []
    for cx, cz, start in ((.133, .058, 0), (-.133, .058, 90),
                          (-.133, -.058, 180), (.133, -.058, 270)):
        for index in range(9):
            angle = math.radians(start + index * 90 / 8)
            perimeter.append((cx + .006 * math.cos(angle),
                              cz + .006 * math.sin(angle)))
    perimeter.append(perimeter[0])
    point = lambda u, v: (u, face_y, centre_z + v)
    stroke(body, perimeter, .0011, point, 'plate', (0, -1, 0),
           round_joins=True)
    # Cream field and dark Michigan header, plus the small renewal tab.
    body.face([(-.135, face_y, .364), (.135, face_y, .364),
               (.135, face_y, .385), (-.135, face_y, .385)],
              'plate', normal=(0, -1, 0))
    _text(body, 'MICHIGAN', .166, .0125, -.009, .3745,
          face_y - .0007, 'cream', .085)
    # Existing engine swatch is the closest available muted blue-green. Keep
    # the shared native palette stable instead of adding another material.
    body.face([(.103, face_y-.0005, .365), (.131, face_y-.0005, .365),
               (.131, face_y-.0005, .383), (.103, face_y-.0005, .383)],
              'engine', normal=(0, -1, 0))
    _text(body, 'AUG', .022, .008, .117, .374,
          face_y - .0012, 'plate', .08)
    _text(body, 'BOBSAMX', .249, .069, 0, .321,
          face_y - .0011, 'plate', .062)
    # Small dark mounting holes are flat, outward-facing disks, avoiding
    # projecting fasteners beyond the prior plate's depth envelope.
    for x in (-.106, .106):
        for z in (.270, .376):
            if x > 0 and z > .3:
                continue  # The renewal tab covers this corner in the image.
            body.face([(x+.0018*math.cos(i*math.tau/12), face_y-.0015,
                        z+.0018*math.sin(i*math.tau/12))
                       for i in range(12)], 'black', normal=(0, -1, 0))
