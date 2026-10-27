"""Original rounded tire and dished five-spoke wheel for the supplied video car.

Metres, X axle, centre Z=.65 before the generator's chassis offset. No wheel
manufacturer or tire size is inferred from the small reference frames.
"""
import math


def build_wheel(wheel):
    """Append closed, palette-aware geometry to the original Wheel Part."""
    def point(x, radius, angle):
        return (x, radius * math.cos(angle), .65 + radius * math.sin(angle))

    def lathe(profile, colours, segments=64, tread=False):
        rings = []
        for x, radius in profile:
            ring = []
            for i in range(segments):
                angle = i * math.tau / segments
                if tread and radius >= .315:
                    # Narrow channels cut into the tread, never above its radius.
                    phase = (i + (1 if x > .015 else -1 if x < -.015 else 0)) % 4
                    groove = .0025 if phase == 0 else 0
                    radius_here = radius - groove
                else:
                    radius_here = radius
                ring.append(point(x, radius_here, angle))
            rings.append(ring)
        for j, (a, b) in enumerate(zip(rings, rings[1:] + rings[:1])):
            colour = colours[j % len(colours)]
            for i in range(segments):
                following = (i + 1) % segments
                wheel.face([a[i], a[following], b[following], b[i]], colour)

    # The lettering strip stays at X=.103 over R=.266..290, leaving 1.2mm
    # clearance below the separate raised lettering module at X=.1042.
    tire = [(-.080, .215), (-.092, .226), (-.099, .245), (-.103, .266),
            (-.103, .290), (-.097, .305), (-.087, .317), (-.065, .325),
            (-.030, .327), (0, .327), (.030, .327), (.065, .325),
            (.087, .317), (.097, .305), (.103, .290), (.103, .266),
            (.099, .245), (.092, .226), (.080, .215)]
    lathe(tire, ['rubber'], 128, tread=True)
    # Thin sidewall bead/rub strips, kept inside the white-lettering band.
    for side in (-1, 1):
        lathe([(side*.0965, .244), (side*.100, .245),
               (side*.1005, .247), (side*.098, .248)], ['black'], 64)
        lathe([(side*.096, .303), (side*.098, .304),
               (side*.097, .306), (side*.095, .305)], ['black'], 64)

    # A true barrel and rolled rim edge leave visible depth behind the spokes.
    lathe([(-.088, .216), (.088, .216), (.094, .209), (.081, .195),
           (-.081, .195), (-.094, .209)], ['chromeDark'], 64)
    for side in (-1, 1):
        lathe([(side*.080, .213), (side*.094, .217), (side*.104, .214),
               (side*.108, .208), (side*.105, .202), (side*.097, .200),
               (side*.078, .194), (side*.067, .184), (side*.060, .183),
               (side*.065, .200)],
              ['chrome', 'silverLight', 'chrome', 'chrome', 'silverLight',
               'chromeDark', 'chromeDark', 'black', 'chromeDark', 'chrome'], 64)
        # Shadowed brake backing is inset 50mm behind the rim lip. It does not
        # substitute a flat grey disc for the holes between the five spokes.
        wheel.cylinder((side*.046, 0, .65), .169, .012, 'shadow', segments=48)
        wheel.cylinder((side*.096, 0, .65), .060, .027, 'chromeDark', segments=32)
        for spoke in range(5):
            angle = math.pi/2 + spoke * math.tau / 5
            # Radius, tangential half-width, outward X, subtle tangential sweep.
            stations = [(.048, .022, .111, -.004), (.073, .028, .111, -.003),
                        (.108, .031, .105, 0), (.147, .030, .092, .003),
                        (.181, .024, .079, .004), (.201, .018, .077, .002)]
            rings = []
            for radius, width, axial, sweep in stations:
                # Eight-point bevelled section gives each spoke a curved crown.
                section = [(-width*.78, -.010), (-width, -.004),
                           (-width*.78, .003), (-width*.30, .007),
                           (width*.30, .007), (width*.78, .003),
                           (width, -.004), (width*.78, -.010)]
                ring = []
                for tangent, outward in section:
                    tangent += sweep
                    ring.append((side * (axial + outward),
                                 radius*math.cos(angle)-tangent*math.sin(angle),
                                 .65+radius*math.sin(angle)+tangent*math.cos(angle)))
                rings.append(ring)
            wheel.face(list(reversed(rings[0])), 'chromeDark')
            for a, b in zip(rings, rings[1:]):
                for i in range(8):
                    following = (i + 1) % 8
                    colour = 'chromeDark' if i in (0, 6, 7) else 'chrome'
                    if i == 3:
                        colour = 'silverLight'
                    wheel.face([a[i], a[following], b[following], b[i]], colour)
            wheel.face(rings[-1], 'chrome')
            lug_angle = angle + math.pi/5
            wheel.cylinder((side*.113, .043*math.cos(lug_angle),
                            .65+.043*math.sin(lug_angle)), .0075, .014,
                           'chrome', segments=6)
        # Raised centre cap with a shallow rolled edge and dark insert.
        lathe([(side*.107, .031), (side*.115, .034), (side*.121, .030),
               (side*.1215, .024), (side*.118, .023), (side*.111, .025)],
              ['chrome', 'chrome', 'silverLight', 'chromeDark', 'chrome', 'chrome'], 32)
        wheel.cylinder((side*.1195, 0, .65), .023, .004, 'chrome', segments=32)
        wheel.cylinder((side*.122, 0, .65), .011, .001, 'black', segments=24)
        # Valve near the lip, shortened so its total axial envelope stays .245m.
        wheel.cylinder((side*.101, .178, .65-.061), .004, .010,
                       'rubber', segments=8)
