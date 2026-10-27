"""Original surface-seated exterior handles and parked windshield wipers.

Source metres, +Y forward and +Z up. Uses the existing Part and palette only.
"""
import math


def _rounded_outline(width, height, radius, segments=5):
    points=[]
    for cy,cz,start in ((width/2-radius,height/2-radius,0),
                        (-width/2+radius,height/2-radius,90),
                        (-width/2+radius,-height/2+radius,180),
                        (width/2-radius,-height/2+radius,270)):
        for step in range(segments+1):
            angle=math.radians(start+90*step/segments)
            points.append((cy+radius*math.cos(angle),cz+radius*math.sin(angle)))
    return points


def build_handle(door, side, side_x):
    """Shallow rectangular bright bezel, dark grip pocket and front button.

    The pocket is an original dark overlay over the uncut door skin. Its
    raised bezel and grip make a shallow apparent recess without cutting a
    second aperture into the mechanically checked moving panel.
    """
    center_y,center_z=-.21,.74
    def point(y,z,offset):
        yy,zz=center_y+y,center_z+z
        return (side*(side_x(yy,zz)+offset),yy,zz)
    outer=_rounded_outline(.146,.048,.007)
    inner=_rounded_outline(.133,.034,.004)
    back=[point(y,z,.0012) for y,z in outer]
    crest=[point(y,z,.0055) for y,z in outer]
    inset=[point(y,z,.0040) for y,z in inner]
    pocket=[point(y,z,.0015) for y,z in inner]
    for aa,bb,colour in ((back,crest,'chrome'),(crest,inset,'chrome'),
                          (inset,pocket,'chromeDark')):
        for i in range(len(aa)):
            j=(i+1)%len(aa)
            door.face([aa[i],aa[j],bb[j],bb[i]],colour)
    door.face(pocket,'shadow',normal=(side,0,0))
    # Horizontal grip floats only within the outlined pocket. End returns
    # attach it to the bezel, with black undercut visible below its edge.
    chain=[(-.054,.010,.005),(-.046,.010,.010),(.027,.010,.010),(.035,.010,.005)]
    for a,b in zip(chain,chain[1:]):
        door.beam(point(*a),point(*b),.0032,'chrome',8)
    # Front push button is inset into a separate dark rectangular surround.
    def plaque(y0,z0,width,height,offset,colour):
        outline=_rounded_outline(width,height,min(.002,width/4,height/4),3)
        door.face([point(y0+y,z0+z,offset) for y,z in outline],colour,
                  normal=(side,0,0))
    plaque(.052,0,.020,.026,.0058,'black')
    plaque(.052,.001,.014,.019,.0065,'chrome')


def build_wipers(body, screen):
    """Two articulated parked arms supported by the actual windshield mesh.

    screen(x,t) is the builder's baseline-x parameterization. The saved
    windshield uses six transverse strips with only bottom/top endpoints,
    so sampling its analytic sine bow would place trim below its triangles.
    Reconstruct those exact planar triangles and offset toward the exterior.
    All trim remains aft of source Y=.79, clear of the forward opening hood.
    """
    stations=(-.815,-.61,-.32,0,.32,.61,.815)
    def support(x,t,clearance=.004):
        xa,xb=next((a,b) for a,b in zip(stations,stations[1:]) if a-1e-9<=x<=b+1e-9)
        u=(x-xa)/(xb-xa)
        p0,p1,p2,p3=screen(xa,0),screen(xb,0),screen(xb,1),screen(xa,1)
        if u>=t:
            tri=(p0,p1,p2)
            weights=(1-u,u-t,t)
        else:
            tri=(p0,p2,p3)
            weights=(1-t,u,t-u)
        a,b,c=tri
        ab=[b[i]-a[i] for i in range(3)]
        ac=[c[i]-a[i] for i in range(3)]
        normal=(ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0])
        length=math.sqrt(sum(value*value for value in normal))
        if normal[1]<0:normal=tuple(-value for value in normal)
        return tuple(sum(weight*point[i] for weight,point in zip(weights,tri))
                     +clearance*normal[i]/length for i in range(3))
    for pivot,end in ((-.22,-.63),(.43,.01)):
        # Knuckle, slender articulated arm and black rubber blade. Parked
        # blade leans upward slightly, matching the observed lower-screen arc.
        body.ellipsoid(support(pivot,.026,.0085),(.009,.007,.005),'chromeDark',12,6)
        arm=[(pivot,.026), (pivot-.045,.060), (end+.13,.090)]
        for a,b in zip(arm,arm[1:]):
            body.beam(support(*a,.0065),support(*b,.0065),.0022,'chromeDark',6)
        body.ellipsoid(support(end+.13,.090,.0065),(.005,.004,.004),'black',8,4)
        blade_start,blade_end=end-.070,end+.265
        for index in range(12):
            a,b=index/12,(index+1)/12
            def blade(t,offset):
                return support(blade_start+(blade_end-blade_start)*t,.070+.040*t,offset)
            body.beam(blade(a,.0036),blade(b,.0036),.0015,'rubber',6)
            body.beam(blade(a,.0064),blade(b,.0064),.0013,'chromeDark',6)
