"""Original vector trim for the supplied red 1973 Javelin AMX.

No fonts, image pixels or meshes are imported. Coordinates are authoring metres,
nose +Y. These functions append palette-aware faces to the generator's Part.
"""
import math


# Original stroke drawings, intentionally independent of a system font.
GLYPHS = {
    'A': (((0, 0), (.5, 1), (1, 0)), ((.22, .4), (.78, .4))),
    'B': (((0, 0), (0, 1), (.68, 1), (1, .83), (.9, .62), (.12, .51),
           (.75, .51), (1, .28), (.87, .08), (.65, 0), (0, 0)),),
    'C': (((1, .85), (.78, 1), (.25, 1), (0, .77), (0, .23), (.25, 0),
           (.78, 0), (1, .15)),),
    'D': (((0, 0), (0, 1), (.65, 1), (1, .75), (1, .25), (.65, 0), (0, 0)),),
    'F': (((0, 0), (0, 1), (1, 1)), ((0, .54), (.8, .54))),
    'G': (((1, .85), (.78, 1), (.25, 1), (0, .77), (0, .23), (.25, 0),
           (.85, 0), (1, .2), (1, .48), (.58, .48)),),
    'H': (((0, 0), (0, 1)), ((1, 0), (1, 1)), ((0, .5), (1, .5))),
    'I': (((.5, 0), (.5, 1)), ((.12, 1), (.88, 1)), ((.12, 0), (.88, 0))),
    'L': (((0, 1), (0, 0), (1, 0)),),
    'M': (((0, 0), (0, 1), (.5, .4), (1, 1), (1, 0)),),
    'O': (((.25, 0), (.75, 0), (1, .25), (1, .75), (.75, 1), (.25, 1),
           (0, .75), (0, .25), (.25, 0)),),
    'R': (((0, 0), (0, 1), (.7, 1), (1, .8), (.9, .6), (.65, .51),
           (0, .51)), ((.5, .51), (1, 0))),
    'T': (((0, 1), (1, 1)), ((.5, 1), (.5, 0))),
    'X': (((0, 0), (1, 1)), ((0, 1), (1, 0))),
    '/': (((0, 0), (1, 1)),),
    '3': (((0, .9), (.3, 1), (.8, 1), (1, .8), (.78, .53), (.36, .5),
           (.8, .48), (1, .2), (.8, 0), (.25, 0), (0, .12)),),
    '6': (((.92, .9), (.68, 1), (.25, .9), (0, .6), (0, .2), (.25, 0),
           (.78, 0), (1, .2), (1, .45), (.78, .61), (.25, .61), (0, .45)),),
    '0': (((.25, 0), (.75, 0), (1, .2), (1, .8), (.75, 1), (.25, 1),
           (0, .8), (0, .2), (.25, 0)),),
}


def stroke(part, path, width, point, colour, normal, round_joins=False):
    """Seat a flat vector ribbon on a supplied surface, with explicit facing."""
    for a, b in zip(path, path[1:]):
        du, dv = b[0] - a[0], b[1] - a[1]
        length = math.hypot(du, dv)
        if length < 1e-10:
            continue
        nu, nv = -dv / length * width / 2, du / length * width / 2
        part.face([point(a[0] + nu, a[1] + nv),
                   point(b[0] + nu, b[1] + nv),
                   point(b[0] - nu, b[1] - nv),
                   point(a[0] - nu, a[1] - nv)], colour, normal=normal)
    if round_joins:
        # A cast monogram has continuous metal at its bends. Independent stroke
        # rectangles otherwise leave tiny triangular red cracks at every joint.
        for u,v in path[1:-1]:
            part.face([point(u+width/2*math.cos(i*math.tau/8),
                             v+width/2*math.sin(i*math.tau/8))
                       for i in range(8)],colour,normal=normal)


def lettering(part, text, width, height, point, colour, normal,
              stroke_ratio=.075, serifs=False):
    """Centred hand-authored lettering on an arbitrary 2D surface mapping."""
    count = len(text)
    advance = width / max(1, count)
    glyph_width = advance * .77
    for index, char in enumerate(text):
        if char == ' ':
            continue
        origin = (index - (count - 1) / 2) * advance - glyph_width / 2
        for path in GLYPHS[char]:
            stroke(part, [(origin + u * glyph_width, (v - .5) * height)
                          for u, v in path], height * stroke_ratio,
                   point, colour, normal)
        if serifs and char in 'AMX':
            # The rear AMX has short slab terminals, unlike a plain sans-serif X.
            terminals = {'A': ((0, 0), (1, 0)),
                         'M': ((0, 0), (1, 0), (0, 1), (1, 1)),
                         'X': ((0, 0), (1, 0), (0, 1), (1, 1))}[char]
            for u, v in terminals:
                stroke(part, [(origin + (u - .12) * glyph_width, (v - .5) * height),
                              (origin + (u + .12) * glyph_width, (v - .5) * height)],
                       height * stroke_ratio, point, colour, normal)


def _triangle_clip(poly, triangle):
    """Clip a 2D polygon into a triangle with either winding."""
    a,b,c=triangle
    winding=1 if ((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))>0 else -1
    for a, b in zip(triangle, triangle[1:] + triangle[:1]):
        out = []
        if not poly:
            return out
        def distance(p):
            return winding*((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]))
        previous = poly[-1]
        pd = distance(previous)
        for current in poly:
            cd = distance(current)
            if (cd >= -1e-10) != (pd >= -1e-10):
                t = pd / (pd - cd)
                out.append(tuple(previous[j] + (current[j] - previous[j]) * t
                                 for j in (0, 1)))
            if cd >= -1e-10:
                out.append(current)
            previous, pd = current, cd
        poly = out
    return poly






def _triangulate_outline(points):
    """Ear-clip a simple2D artwork outline before support-cell clipping.

    Clipping a concave outline can join disconnected pieces by backtracking
    edges. Convex source triangles avoid those weakly-simple contours.
    """
    points=list(points)
    area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(points,points[1:]+points[:1]))
    if abs(area)<1e-14:return []
    sign=1 if area>0 else -1
    def turn(a,b,c):
        return sign*((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
    indices=list(range(len(points)));result=[]
    while len(indices)>3:
        for k,b in enumerate(indices):
            a=indices[k-1];c=indices[(k+1)%len(indices)]
            if turn(points[a],points[b],points[c])<=1e-14:continue
            if any(min(turn(points[a],points[b],points[j]),
                       turn(points[b],points[c],points[j]),
                       turn(points[c],points[a],points[j]))>=-1e-14
                   for j in indices if j not in (a,b,c)):continue
            result.append([points[a],points[b],points[c]])
            indices.pop(k);break
        else:
            raise ValueError('Artwork outline is non-simple or degenerate')
    if len(indices)==3 and turn(*(points[i] for i in indices))>1e-14:
        result.append([points[i] for i in indices])
    return result


def clean_decal_outline(points, tolerance=.000002):
    """Remove sub-weld collinear contour knots before float32 tessellation.

    Only points between their neighbours can be removed. The2micrometre
    chord tolerance is below the existing10micrometre mesh weld and avoids
    long, nanometre-altitude ears in the clipped fine border.
    """
    result=list(points)
    while len(result)>=3:
        removed=False
        for i,point in enumerate(result):
            a=result[i-1];b=result[(i+1)%len(result)]
            chord=tuple(b[k]-a[k] for k in range(3))
            length2=sum(v*v for v in chord)
            if length2<1e-24:
                result.pop(i);removed=True;break
            u=sum((point[k]-a[k])*chord[k] for k in range(3))/length2
            if not 0<=u<=1:continue
            error2=sum((point[k]-a[k]-u*chord[k])**2 for k in range(3))
            if error2<=tolerance*tolerance:
                result.pop(i);removed=True;break
        if not removed:break
    return result if len(result)>=3 else []




def build_cardin_crests(body, side_x, y=.91, z=.63):
    """Open chrome stacked P/C monogram seen at 0:16, without a black plaque."""
    # One shared upright, upper P loop, lower C turn. These are original paths,
    # not extracted badge pixels. The red body remains visible through the loops.
    paths = [((-.022,-.035),(-.022,.035),(.001,.035),(.017,.030),
              (.024,.018),(.021,.007),(.010,.000),(-.021,.000)),
             ((.023,-.012),(.014,-.006),(-.001,-.006),(-.010,-.015),
              (-.010,-.025),(-.002,-.032),(.014,-.032),(.024,-.026)),
             ((-.022,-.035),(.024,-.035))]
    for side in (-1,1):
        def point(u,v):
            yy,zz = y+side*u,z+v
            return (side*(side_x(yy,zz)+.0025),yy,zz)
        for path in paths:
            stroke(body,path,.0044,point,'chromeDark',(side,0,0),round_joins=True)
        def highlight(u,v):
            p=point(u,v)
            return (p[0]+side*.0006,p[1],p[2])
        for path in paths:
            stroke(body,path,.0024,highlight,'silverLight',(side,0,0),round_joins=True)


def build_rear_badges(trunk, tail_face, badge_z=.843, badge_y=None):
    """Small AMC left and slab-serif AMX right, on the moving rear lid return.

    The caller owns seating these on its rear return. badge_y can override the
    surface position (constant or callable x,z) when rebuilt; letters face -Y.
    """
    rear_y=tail_face-.024 if badge_y is None else badge_y
    for text,center,width,height in (('AMC',-.685,.049,.016),
                                     ('AMX',.614,.224,.045)):
        def point(u,v):
            x,z=center+u,badge_z+v
            return (x,rear_y(x,z) if callable(rear_y) else rear_y,z)
        lettering(trunk,text,width,height,point,'chrome',(0,-1,0),
                  stroke_ratio=.10,serifs=text=='AMX')


def build_tire_lettering(wheel):
    """Raised white BFGoodrich and Radial T/A treatment seen at 0:16.

    Readable original uppercase stroke lettering substitutes for the tiny
    proprietary mixed-case shapes. It does not assert tire size or provenance.
    """
    radius=.278
    for side in (-1,1):
        for text,angle,width in (('BFGOODRICH',math.pi/2,.39),
                                 ('RADIAL T/A',-math.pi/2,.36)):
            def point(u,v):
                # Looking directly at either outside face, text remains readable.
                theta=angle-side*u/radius
                if angle<0:
                    theta=angle+side*u/radius
                r=radius+v if angle>0 else radius-v
                return (side*.1042,r*math.cos(theta),.65+r*math.sin(theta))
            lettering(wheel,text,width,.022,point,'white',(side,0,0),.075)


def build_aircleaner_label(body):
    """Original 360 / red-white-blue air-cleaner label, visible at 1:07."""
    radius=.276
    def point(u,v,offset=0):
        theta=-u/radius
        return ((radius+offset)*math.sin(theta),
                1.47+(radius+offset)*math.cos(theta),.798+v)
    for left,right,col in ((-.115,.114,'steel'),):
        for i in range(12):
            a=left+(right-left)*i/12
            b=left+(right-left)*(i+1)/12
            body.face([point(a,-.018),point(b,-.018),point(b,.018),point(a,.018)],
                      col,normal=(0,1,0))
    for lo,hi,col in ((.010,.016,'red'),(-.016,-.010,'blue')):
        for i in range(8):
            a=-.110+i*.014
            b=a+.014
            body.face([point(a,lo,.0004),point(b,lo,.0004),
                       point(b,hi,.0004),point(a,hi,.0004)],col,normal=(0,1,0))
    lettering(body,'360',.086,.027,
              lambda u,v:point(u+.062,v,.0008),'black',(0,1,0),.09)


def build_decals(body, hood, trunk, wheel, *, hood_point, hood_x, hood_y,
                 side_x, tail_face, badge_z=.843, badge_y=None,
                 fender_point=None, fender_y=None, fender_t=(0,.25,.55,.8,1),fender_front=2.385,fender_triangles=None):
    """Append reference-supported graphics after base geometry, before object()."""
    from javelin_front_artwork import build_front_artwork
    build_front_artwork(body,hood,hood_point,hood_x,hood_y,fender_point,fender_y,fender_t,fender_triangles)
    build_cardin_crests(body,side_x)
    build_rear_badges(trunk,tail_face,badge_z,badge_y)
    build_tire_lettering(wheel)
    build_aircleaner_label(body)
