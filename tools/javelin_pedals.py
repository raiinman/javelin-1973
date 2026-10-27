"""Original static manual foot controls, from BaT048 and 1973 AMC linkage evidence.

Positions, pad dimensions and hidden pivots are reconstruction choices, not
factory measurements. Coordinates use the existing builder's authoring basis.
"""
import math


PEDALS = (
    ('parking', -.665, .645, .440, .049, .054, 16),
    ('clutch', -.490, .610, .438, .078, .064, 18),
    ('brake', -.355, .620, .438, .082, .063, 18),
    ('accelerator', -.230, .650, .414, .043, .139, 12),
)


def build_pedals(inside):
    """Four independent controls, with compact manual pads and suspended arms."""
    def plate(center, size, radius, colour, tilt):
        start = len(inside.vertices)
        inside.rounded_plate((0, 0, 0), size, radius, colour, segments=4)
        c, s = math.cos(tilt), math.sin(tilt)
        for i in range(start, len(inside.vertices)):
            x, y, z = inside.vertices[i]
            inside.vertices[i] = (center[0]+x, center[1]+c*y+s*z,
                                  center[2]-s*y+c*z)

    def arm(path, width=.012, depth=.010):
        # One closed bent rectangular metal strip, rather than floating pads
        # or several disconnected sticks. Smooth bends retain its full width.
        rings = []
        for i, p in enumerate(path):
            a, b = path[max(0, i-1)], path[min(len(path)-1, i+1)]
            dy, dz = b[1]-a[1], b[2]-a[2]
            length = math.hypot(dy, dz)
            ny, nz = -dz/length, dy/length
            rings.append([(p[0]+sx*width/2, p[1]+sn*ny*depth/2,
                           p[2]+sn*nz*depth/2)
                          for sx, sn in ((-1,-1),(1,-1),(1,1),(-1,1))])
        inside.face(list(reversed(rings[0])), 'chromeDark')
        inside.face(rings[-1], 'chromeDark')
        for a, b in zip(rings, rings[1:]):
            for i in range(4):
                j = (i+1)%4
                inside.face([a[i],a[j],b[j],b[i]], 'chromeDark')

    for name, x, y, z, w, h, angle in PEDALS:
        tilt = math.radians(angle)
        c, s = math.cos(tilt), math.sin(tilt)
        # Upper plate seats against the existing lower dash underside (z=.621).
        # All support hardware stays in the fixed Interior part.
        pivot_x = x + (.025 if name == 'clutch' else 0)
        inside.box((pivot_x,.505,.616),(.036,.042,.010),'black')
        inside.cylinder((pivot_x,.510,.606),.010,.026,'chromeDark',axis='X',segments=12)
        end = (x, y+c*.011, z-s*.011)
        arm([(pivot_x,.510,.608), (pivot_x,y+.015,.572),
             (x,y+.045,.505 if name != 'accelerator' else .486), end],
            width=.010 if name in ('parking','accelerator') else .014)
        # Thin metal backing, rubber face and raised perimeter are separate
        # original volumes. The face normal points aft and slightly upward.
        plate((x,y,z), (w,.014,h), .007, 'chromeDark', tilt)
        face = (x,y-c*.008,z+s*.008)
        plate(face, (w-.005,.006,h-.005), .006, 'rubber', tilt)
        # Parallel molded tread is geometry on the face, with positive support.
        if name == 'accelerator':
            for offset in (-.012,-.006,0,.006,.012):
                plate((x+offset,y-c*.012,z+s*.012),(.0025,.0035,h-.020),
                      .0012,'black',tilt)
        else:
            for k in range(5):
                v=(k-2)*(h-.018)/4
                plate((x,y-c*.012+s*v,z+s*.012+c*v),
                      (w-.018,.0035,.0025),.0012,'black',tilt)
