"""Original 1973 AMX front insert, authored from the supplied restored car.

Coordinates are metres, nose +Y. Call with the generator's palette-aware Part.
The small AMO club badges are separate from the red rally-lamp lenses.
"""
import math
from javelin_decals import _triangle_clip


def valance_point(u,t,back=False):
    """Shared lower nose edge for its front skin and corner returns."""
    return (u*(.800+.035*t),
            2.405-.140*(1-t)**2-.025*u**4-(.008 if back else 0),
            .280+.240*t+.035*u**4*(1-t))


def build_valance(body):
    """Closed curved lower nose, rolling rearward below the bumper."""
    point=valance_point
    columns=tuple(-1+i/12 for i in range(25))
    levels=tuple(i/12 for i in range(13))
    for a,b in zip(columns,columns[1:]):
        for lo,hi in zip(levels,levels[1:]):
            body.face([point(a,lo),point(b,lo),point(b,hi),point(a,hi)],'red')
            body.face([point(a,hi,True),point(b,hi,True),
                       point(b,lo,True),point(a,lo,True)],'redDark')
        for t in (0,1):
            body.face([point(a,t),point(a,t,True),point(b,t,True),point(b,t)],'red')
    for u in (-1,1):
        for lo,hi in zip(levels,levels[1:]):
            body.face([point(u,lo),point(u,hi),point(u,hi,True),point(u,lo,True)],'red')


def front_depth(x):
    return 2.447-.046*(abs(x)/.84)**2


def front_outline():
    outline = [(-.84, .550), (-.836, .716), (-.812, .763), (-.770, .782),
               (-.59, .785), (0, .790), (.59, .785), (.770, .782),
               (.812, .763), (.836, .716), (.84, .550), (.814, .507),
               (.76, .493), (.59, .497), (0, .505), (-.59, .497),
               (-.76, .493), (-.814, .507)]
    # Round the existing stamped corners without altering lamp/hood anchors.
    rounded=[]
    for index,point in enumerate(outline):
        before_point=outline[index-1]
        after_point=outline[(index+1)%len(outline)]
        def approach(other):
            length=math.dist(point,other)
            t=min(.018/length,.30)
            return tuple(point[k]+t*(other[k]-point[k]) for k in (0,1))
        a,b=approach(before_point),approach(after_point)
        for step in range(7):
            t=step/6
            rounded.append(tuple((1-t)**2*a[k]+2*t*(1-t)*point[k]+t*t*b[k]
                                 for k in (0,1)))
    outline=rounded
    return outline


def front_columns(outline=None):
    outline=front_outline() if outline is None else outline
    lamp_centres=(-.708,.708)
    aperture=.122
    columns=sorted(set(round(x,10) for x in (
        [x for x,z in outline]+[-.84+i*1.68/120 for i in range(121)]+
        [centre+aperture*math.cos(i*math.tau/40)
         for centre in lamp_centres for i in range(40)])))

    columns=[x for x in columns if min(p[0] for p in outline)-1e-9<=x<=max(p[0] for p in outline)+1e-9]

    return columns


def front_bounds(x,outline=None):
    outline=front_outline() if outline is None else outline
    crossings=[]
    for a,b in zip(outline,outline[1:]+outline[:1]):
        if a[0]!=b[0] and min(a[0],b[0])-1e-9<=x<=max(a[0],b[0])+1e-9:
            t=(x-a[0])/(b[0]-a[0]);crossings.append(a[1]+t*(b[1]-a[1]))
    return min(crossings),max(crossings)


def front_upper_point(x):
    # Interpolate the exact original saved fascia upper-edge segments.
    columns=front_columns()
    for a,b in zip(columns,columns[1:]):
        if a-1e-9<=x<=b+1e-9:
            t=(x-a)/(b-a)
            return (x,(front_depth(a)*(1-t)+front_depth(b)*t)-.016,
                    front_bounds(a)[1]*(1-t)+front_bounds(b)[1]*t)
    raise ValueError(x)


def build_front(body, terminal=None):
    """Build a bowed mesh insert, recessed lamps and reference-specific badges."""
    def lettering(text, x, y, z, height, colour):
        paths = {'A': (((0, 0), (.5, 1), (1, 0)), ((.23, .4), (.77, .4))),
                 'M': (((0, 0), (0, 1), (.5, .4), (1, 1), (1, 0)),),
                 'O': (((.2, 0), (.8, 0), (1, .2), (1, .8), (.8, 1),
                        (.2, 1), (0, .8), (0, .2), (.2, 0)),),
                 'X': (((0, 0), (1, 1)), ((0, 1), (1, 0)))}
        for i, char in enumerate(text):
            origin = x - (i - (len(text)-1)/2) * height * .9
            for path in paths[char]:
                for a, b in zip(path, path[1:]):
                    body.beam((origin-(a[0]-.5)*height*.65, y, z+(a[1]-.5)*height),
                              (origin-(b[0]-.5)*height*.65, y, z+(b[1]-.5)*height),
                              height*.045, colour, 4)

    depth=front_depth

    def rim(outline, width, colour, inset=0):
        # A closed ring with a shallow rear return, never a floating front line.
        outer = [(x, depth(x) + inset, z) for x, z in outline]
        inner = [(x * (1 - width / .84), depth(x) + inset,
                  .64 + (z - .64) * (1 - width / .15)) for x, z in outline]
        rings = [outer, inner,
                 [(x, y - .014, z) for x, y, z in inner],
                 [(x, y - .014, z) for x, y, z in outer]]
        for a, b in zip(rings, rings[1:] + rings[:1]):
            for i in range(len(a)):
                j = (i + 1) % len(a)
                body.face([a[i], a[j], b[j], b[i]], colour)

    def revolved(x, z, profile, colour, segments=32):
        # Closed axial profile. Radius/Y pairs form reflector bowls and rolled rims.
        rings = [[(x + r * math.cos(i * math.tau / segments), y,
                   z + r * math.sin(i * math.tau / segments))
                  for i in range(segments)] for r, y in profile]
        for a, b in zip(rings, rings[1:] + rings[:1]):
            for i in range(segments):
                j = (i + 1) % segments
                body.face([a[i], a[j], b[j], b[i]], colour)

    def lens(x, z, radius, back, crown, colour):
        rings = []
        for scale, y in ((1, back), (.83, crown - .004), (.42, crown)):
            rings.append([(x + radius * scale * math.cos(i * math.tau / 32), y,
                           z + radius * scale * math.sin(i * math.tau / 32))
                          for i in range(32)])
        body.face(list(reversed(rings[0])), colour)
        for a, b in zip(rings, rings[1:]):
            for i in range(32):
                j = (i + 1) % 32
                body.face([a[i], a[j], b[j], b[i]], colour)
        body.face(rings[-1], colour)

    outline=front_outline()
    # Shared stations leave actual lamp openings through both fascia skins.
    lamp_centres=(-.708,.708)
    aperture=.122
    columns=front_columns(outline)
    def bounds(x):return front_bounds(x,outline)

    def hole(x,centre):
        half=math.sqrt(max(0,aperture**2-(x-centre)**2))
        return .641-half,.641+half

    def skin(points):
        front=[(x,depth(x)-.016,z) for x,z in points]
        back=[(x,2.345,z) for x,z in points]
        if terminal:
            split=[]
            for pa,pb in zip(front,front[1:]+front[:1]):
                split.append(pa)
                if (abs(pa[2]-bounds(pa[0])[1])<1e-8
                        and abs(pb[2]-bounds(pb[0])[1])<1e-8):
                    xs=sorted((x for x in terminal['join_x'] if min(pa[0],pb[0])+1e-8<x<max(pa[0],pb[0])-1e-8),reverse=pa[0]>pb[0])
                    for x in xs:
                        t=(x-pa[0])/(pb[0]-pa[0]);split.append(tuple(pa[k]*(1-t)+pb[k]*t for k in range(3)))
            front=split
        body.face(front,'shadow',normal=(0,1,0))
        body.face(list(reversed(back)),'shadow',normal=(0,-1,0))

    for a,b in zip(columns,columns[1:]):
        low_a,high_a=bounds(a)
        low_b,high_b=bounds(b)
        centre=next((c for c in lamp_centres if abs((a+b)/2-c)<aperture),None)
        intervals=[(low_a,low_b,.641,.641),(.641,.641,high_a,high_b)]
        if centre is not None:
            hole_low_a,hole_high_a=hole(a,centre)
            hole_low_b,hole_high_b=hole(b,centre)
            intervals=[(low_a,low_b,hole_low_a,hole_low_b),
                       (hole_high_a,hole_high_b,high_a,high_b)]
            for za,zb,sign in ((hole_low_a,hole_low_b,1),
                               (hole_high_a,hole_high_b,-1)):
                points=[(a,depth(a)-.016,za),(b,depth(b)-.016,zb),
                        (b,2.345,zb),(a,2.345,za)]
                body.face(points if sign>0 else list(reversed(points)),'black')
        for lo_a,lo_b,hi_a,hi_b in intervals:
            skin([(a,lo_a),(a,hi_a),(b,hi_b),(b,lo_b)])
        for za,zb,sign in ((low_a,low_b,-1),(high_a,high_b,1)):
            points=[(a,depth(a)-.016,za),(b,depth(b)-.016,zb),
                    (b,2.345,zb),(a,2.345,za)]
            if terminal and sign>0:
                def clip_x(poly,limit,keep_greater):
                    result=[]
                    for pa,pb in zip(poly,poly[1:]+poly[:1]):
                        ina=pa[0]>=limit if keep_greater else pa[0]<=limit
                        inb=pb[0]>=limit if keep_greater else pb[0]<=limit
                        if ina:result.append(pa)
                        if ina!=inb:
                            t=(limit-pa[0])/(pb[0]-pa[0]);result.append(tuple(pa[k]*(1-t)+pb[k]*t for k in range(3)))
                    return result
                central=clip_x(clip_x(points,-.706,True),.706,False)
                if len(central)>=3:body.face(central,'black')
                for side in (-1,1):
                    corner=clip_x(points,side*terminal['outer_x'],side>0)
                    if len(corner)>=3:body.face(corner,'red')
            else:
                body.face(points if sign>0 else list(reversed(points)),'black')
    for x in (columns[0],columns[-1]):
        low,high=bounds(x)
        for a,b in ((low,.641),(.641,high)):
            points=[(x,depth(x)-.016,a),(x,depth(x)-.016,b),
                    (x,2.345,b),(x,2.345,a)]
            body.face(points if x<0 else list(reversed(points)),'black')
    rim(outline, .009, 'chrome')
    # Central insert has slanted ends and a deeper surround than the lamp pods.
    corners = [(-.594, .761), (.594, .761), (.542, .520),
               (0, .500), (-.542, .520)]
    insert=[]
    # Rounded stamped corners preserve a convex clipping domain and tapered ends.
    for index,point in enumerate(corners):
        before=corners[index-1]
        after=corners[(index+1)%len(corners)]
        def approach(other):
            distance=math.dist(point,other)
            blend=min(.040/distance,.22)
            return tuple(point[k]+(other[k]-point[k])*blend for k in (0,1))
        a,b=approach(before),approach(after)
        for step in range(7):
            t=step/6
            insert.append(tuple((1-t)**2*a[k]+2*t*(1-t)*point[k]+t*t*b[k]
                                for k in (0,1)))
    rim(insert, .008, 'chromeDark', -.004)
    rim(insert, .0035, 'silverLight', -.001)
    # Fine original weave occupies repeated atlas tiles on the bowed insert.
    # Its physical pitch is about12x6mm, rather than the old48mm lattice.
    pitch=.024
    domain=[(x,z) for x,z in insert]
    triangles=[[domain[0],domain[i],domain[i+1]] for i in range(1,len(domain)-1)]
    for column in range(50):
        xa=-.60+column*pitch
        for row in range(11):
            za=.50+row*pitch
            cell=[(xa,za),(xa+pitch,za),(xa+pitch,za+pitch),(xa,za+pitch)]
            for triangle in triangles:
                clipped=_triangle_clip(cell,triangle)
                if len(clipped)<3:continue
                area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(clipped,clipped[1:]+clipped[:1])))/2
                if area<1e-10:continue
                body.face([(x,depth(x)-.002,z) for x,z in clipped],'grille',normal=(0,1,0),
                          uvs=[(max(0,min(1,(x-xa)/pitch)),max(0,min(1,(z-za)/pitch))) for x,z in clipped])
    for x in lamp_centres:
        mouth=depth(x)-.016
        # Rolled bezel and reflector seat inside the open field, without a cap.
        revolved(x,.641,[(.120,mouth-.003),(.120,mouth+.002),
                         (.112,mouth+.004),(.109,mouth-.030)],'black',40)
        revolved(x,.641,[(.112,mouth-.028),(.112,mouth+.004),
                         (.101,mouth+.007),(.098,mouth-.014)],'chromeDark',40)
        revolved(x,.641,[(.098,mouth-.021),(.098,mouth-.002),
                         (.089,mouth-.003),(.071,mouth-.025)],'chrome',40)
        lens(x,.641,.089,mouth-.021,mouth-.012,'headlamp')
        # Raised reflector flutes follow the convex lens, avoiding opaque stripes.
        for offset in (-.052, -.026, 0, .026, .052):
            extent = math.sqrt(.078**2 - offset**2)
            chain = []
            for step in range(13):
                dz = -extent + step * 2 * extent / 12
                radius = math.hypot(offset, dz)
                y = mouth-.012 if radius < .089*.42 else mouth-.012 - .004*(radius/.089-.42)/.41
                if radius > .089*.83:
                    y = mouth-.016 - .005*(radius/.089-.83)/.17
                chain.append((x + offset, y + .0006, .641 + dz))
            for a, b in zip(chain, chain[1:]):
                body.beam(a, b, .0007, 'chromeDark', 4)
    for x in (-.455, .455):
        body.cylinder((x, 2.452, .638), .082, .022, 'shadow', axis='Y', segments=32)
        revolved(x, .638, [(.079, 2.449), (.079, 2.476),
                          (.070, 2.481), (.066, 2.453)], 'chrome', 32)
        lens(x, .638, .066, 2.463, 2.483, 'redDark')
        for angle in (math.pi/2,math.pi*7/6,math.pi*11/6):
            body.beam((x,2.485,.638),
                      (x+.054*math.cos(angle),2.485,.638+.054*math.sin(angle)),
                      .0014,'chrome',4)
    # Two observed American Motors Owners Association club medallions.
    for x, z, r in ((-.174, .633, .037), (-.278, .650, .034)):
        body.cylinder((x, 2.470, z), r+.004, .016, 'chrome', axis='Y', segments=24)
        body.cylinder((x, 2.480, z), r, .005, 'blue', axis='Y', segments=24)
        body.cylinder((x, 2.484, z), r-.005, .004, 'cream', axis='Y', segments=24)
        lettering('AMO', x, 2.487, z, .018, 'blue')
    body.rounded_plate((-.055, 2.466, .636), (.125, .012, .032), .004, 'chrome')
    body.box((-.055, 2.474, .636), (.111, .005, .022), 'black')
    lettering('AMX', -.055, 2.478, .636, .017, 'chrome')
