"""Original AMX dial markings and rounded white-ball manual shifter."""
import math
from javelin_decals import stroke


def build_steering(inside):
    """Original slotted metal three-spoke wheel, padded boss and round rim."""
    cx,cy,cz=-.38,.23,.87
    inside.beam((cx,.48,.74),(cx,.25,cz),.022,'black')
    def rim(a,b):
        return (cx+(.16+.012*math.cos(b))*math.cos(a),
                cy+.012*math.sin(b),cz+(.16+.012*math.cos(b))*math.sin(a))
    for i in range(64):
        for j in range(12):
            a,b=i*math.tau/64,(i+1)*math.tau/64
            u,v=j*math.tau/12,(j+1)*math.tau/12
            inside.face([rim(a,u),rim(b,u),rim(b,v),rim(a,v)],'black')
    centres=(.062,.095,.128)
    radius=.0045
    half_run=.008
    columns=sorted(set([.035,.151]+[c+sign*half_run+radius*math.cos(i*math.pi/12)
                       for c in centres for sign in (-1,1) for i in range(13)]))
    def aperture(u,c):
        du=max(0,abs(u-c)-half_run)
        return math.sqrt(max(0,radius*radius-du*du))
    for angle in (0,math.pi,-math.pi/2):
        def point(u,v,layer):
            return (cx+u*math.cos(angle)-v*math.sin(angle),
                    cy-.012*(1-u/.151)+layer*.0015,
                    cz+u*math.sin(angle)+v*math.cos(angle))
        def skin(a,b,va,vb,wa,wb):
            for layer in (-1,1):
                inside.face([point(a,va,layer),point(b,vb,layer),
                             point(b,wb,layer),point(a,wa,layer)],'chrome')
        for a,b in zip(columns,columns[1:]):
            centre=next((c for c in centres if abs((a+b)/2-c)<half_run+radius),None)
            if centre is None:skin(a,b,-.017,-.017,.017,.017)
            else:
                ha,hb=aperture(a,centre),aperture(b,centre)
                skin(a,b,-.017,-.017,-ha,-hb)
                skin(a,b,ha,hb,.017,.017)
                for sign in (-1,1):
                    inside.face([point(a,sign*ha,-1),point(a,sign*ha,1),
                                 point(b,sign*hb,1),point(b,sign*hb,-1)],'chromeDark')
            for sign in (-1,1):
                inside.face([point(a,sign*.017,-1),point(b,sign*.017,-1),
                             point(b,sign*.017,1),point(a,sign*.017,1)],'chrome')
        for u in (columns[0],columns[-1]):
            inside.face([point(u,-.017,-1),point(u,.017,-1),
                         point(u,.017,1),point(u,-.017,1)],'chrome')
    inside.ellipsoid((cx,.215,cz),(.051,.024,.051),'black',segments=48,rings=20)
    inside.cylinder((cx,.190,cz),.025,.002,'chrome',axis='Y',segments=48)
    inside.cylinder((cx,.1885,cz),.022,.001,'blue',axis='Y',segments=48)
    inside.cylinder((cx,.1875,cz),.019,.001,'cream',axis='Y',segments=48)


def dashboard_face_y(x):
    """A slight transverse bow brings the driver cluster toward the cabin."""
    return .438+.047*((x+.30)/.48)**2


def _rounded_outline(cx,cz,width,height,radius,steps=8):
    path=[]
    for x,z,start in ((cx+width/2-radius,cz+height/2-radius,0),
                      (cx-width/2+radius,cz+height/2-radius,math.pi/2),
                      (cx-width/2+radius,cz-height/2+radius,math.pi),
                      (cx+width/2-radius,cz-height/2+radius,math.pi*1.5)):
        for i in range(steps+1):
            angle=start+i*math.pi/(2*steps)
            path.append((x+radius*math.cos(angle),z+radius*math.sin(angle)))
    return path


def _pad_loft(inside, stations, profile, colour='black'):
    """Closed padded sweep, longitudinal stations (x, frontY, heightZ, scale)."""
    # Periodic cubic B-spline rounds the authored cross-section without bevel boxes.
    ring=[]
    for i in range(len(profile)):
        a,b,c,d=[profile[(i+j)%len(profile)] for j in (-1,0,1,2)]
        for step in range(4):
            t=step/4
            weights=((1-t)**3/6,(3*t**3-6*t*t+4)/6,(-3*t**3+3*t*t+3*t+1)/6,t**3/6)
            ring.append(tuple(sum(w*p[k] for w,p in zip(weights,(a,b,c,d))) for k in range(2)))
    loops=[[(x,y+dy*scale,z+dz*scale) for dy,dz in ring] for x,y,z,scale in stations]
    inside.face(list(reversed(loops[0])),colour);inside.face(loops[-1],colour)
    for a,b in zip(loops,loops[1:]):
        for i in range(len(ring)):
            j=(i+1)%len(ring)
            inside.face([a[i],a[j],b[j],b[i]],colour)


def build_dashboard(inside):
    """Original sculpted driver hood, perforated fascia and passenger dash."""
    def crown(x,z):
        upper=max(0,min(1,(z-.78)/.08))
        return z+.014*upper*max(0,1-((x+.30)/.49)**2)
    # The broad upper pad remains behind and below the windshield foot.
    # Driver brow: round cabin-facing bead opens into a deep sloped windshield pad.
    brow_profile=[(-.012,-.009),(-.022,.008),(-.010,.034),(.030,.043),
                  (.110,.040),(.210,.018),(.280,-.010),(.265,-.026),(.070,-.025),(.004,-.018)]
    brow_stations=[]
    for i in range(49):
        x=-.770+.974*i/48
        taper=.65+.35*min(1,(x+.770)/.035,(.204-x)/.035)
        brow_stations.append((x,dashboard_face_y(x)-.006,.874,taper))
    _pad_loft(inside,brow_stations,brow_profile)
    outline=_rounded_outline(-.2925,.770,.965,.224,.044,12)
    rings=[[(x,dashboard_face_y(x)+depth,crown(x,z)) for x,z in outline]
           for depth in (.013,.150)]
    inside.face(list(reversed(rings[0])),'black')
    inside.face(rings[1],'black')
    for i in range(len(outline)):
        j=(i+1)%len(outline)
        inside.face([rings[0][i],rings[0][j],rings[1][j],rings[1][i]],'black')

    # Holes are actual openings in the original metal face, with dark tunnels.
    apertures=[(-.56,.771,.145,.151,.025),(-.365,.771,.145,.151,.025),
               (-.17,.771,.145,.151,.025),(-.704,.765,.055,.142,.005),
               (.043,.814,.172,.055,.006),(.043,.725,.172,.067,.005)]
    bounds=(-.755,.173,.673,.865,.018)
    def interval(hole,z):
        cx,cz,w,h,r=hole
        t=max(0,min(r,abs(z-cz)-(h/2-r)))
        run=w/2-r+math.sqrt(max(0,r*r-t*t))
        return cx-run,cx+run
    def outer(z):
        lo,hi,bot,top,r=bounds
        d=max(0,min(r,max(bot+r-z,z-(top-r))))
        inset=r-math.sqrt(max(0,r*r-d*d))
        return lo+inset,hi-inset
    rows=sorted(set([bounds[2],bounds[3]]+
                    [bounds[2]+i*(bounds[3]-bounds[2])/40 for i in range(41)]+
                    [cz+sign*(h/2-r+r*math.sin(i*math.pi/16))
                     for cx,cz,w,h,r in apertures for sign in (-1,1) for i in range(9)]))
    def point(x,z,depth=0):return (x,dashboard_face_y(x)+depth,crown(x,z))
    for za,zb in zip(rows,rows[1:]):
        holes=sorted([h for h in apertures if abs((za+zb)/2-h[1])<h[3]/2],key=lambda h:h[0])
        la,ra=outer(za);lb,rb=outer(zb)
        for hole in holes:
            ha,hb=interval(hole,za),interval(hole,zb)
            if min(ha[0]-la,hb[0]-lb)>1e-9:
                inside.face([point(la,za),point(ha[0],za),point(hb[0],zb),point(lb,zb)],'silverLight',normal=(0,-1,0))
            la,lb=ha[1],hb[1]
        if min(ra-la,rb-lb)>1e-9:
            inside.face([point(la,za),point(ra,za),point(rb,zb),point(lb,zb)],'silverLight',normal=(0,-1,0))
    for cx,cz,w,h,r in apertures:
        outer_path=_rounded_outline(cx,cz,w+.004,h+.004,r+.002)
        inner_path=_rounded_outline(cx,cz,w,h,r)
        for i in range(len(outer_path)):
            j=(i+1)%len(outer_path)
            inside.face([point(*outer_path[i],-.0008),point(*outer_path[j],-.0008),
                         point(*inner_path[j],.002),point(*inner_path[i],.002)],'chrome',normal=(0,-1,0))
            inside.face([point(*inner_path[i],.002),point(*inner_path[j],.002),
                         point(*inner_path[j],.016),point(*inner_path[i],.016)],'black')
    # Restrained original scallops suggest engine-turned metal without a
    # borrowed image or new texture/material. Skip each aperture and its rim.
    for row in range(7):
        z=.687+row*.025
        for column in range(29):
            x=-.741+column*.031+(row%2)*.0155
            if not bounds[0]+.008<x<bounds[1]-.008:continue
            if any(abs(x-cx)<w/2+.009 and abs(z-cz)<h/2+.009
                   for cx,cz,w,h,r in apertures):continue
            arc=[(x+.0045*math.cos(t),z+.0045*math.sin(t))
                 for t in (0,math.pi/3,math.pi*2/3,math.pi)]
            for a,b in zip(arc,arc[1:]):
                inside.beam(point(*a,-.0008),point(*b,-.0008),.00035,'chromeDark',4)
    # Fine dark/red border follows the same bow; it is original trim artwork.
    for colour,w,h,r,depth in (('redLight',.932,.196,.020,-.0006),
                               ('chromeDark',.940,.204,.024,.001)):
        path=_rounded_outline(-.291,.769,w,h,r,12)
        for a,b in zip(path,path[1:]+path[:1]):
            inside.beam(point(*a,depth),point(*b,depth),.0013,colour,6)
    # Left ventilation grille and radio/vent retain the supplemental layout.
    for i in range(7):
        z=.709+i*.018
        inside.beam(point(-.724,z,.008),point(-.684,z,.008),.0024,'chromeDark',6)
    inside.rounded_plate((.043,dashboard_face_y(.043)+.014,.814),(.162,.010,.045),.005,'black')
    inside.rounded_plate((.043,dashboard_face_y(.043)+.006,.818),(.110,.002,.024),.003,'chromeDark')
    for x in (-.022,.108):
        inside.cylinder((x,dashboard_face_y(x)+.001,.817),.010,.012,'chrome',axis='Y',segments=24)
    for x in (-.007,.018,.043,.068,.093):
        inside.box((x,dashboard_face_y(x)-.001,.799),(.018,.008,.006),'chrome')
    for x in (-.024,.003,.030,.057,.084,.111):
        inside.beam(point(x,.700,.009),point(x,.750,.009),.0018,'chromeDark',4)
    # The lower control ledge is a separate deep padded form below the dials.
    inside.rounded_plate((-.276,.479,.651),(.920,.120,.060),.019,'black')
    for x in (-.64,-.49,-.065,.077):
        y=dashboard_face_y(x)-.016
        inside.beam((x,y+.022,.668),(x,y,.680),.003,'chrome',6)
        inside.box((x,y-.004,.684),(.016,.009,.021),'black')
    # Continuous central cheek steps the passenger face back toward the glass.
    # The tall cheek is part of the same closed sweep, not an added upright nub.
    def passenger_front(x):
        t=max(0,min(1,(x-.178)/.200))
        return .495+.112*(t*t*(3-2*t))+.015*max(0,(x-.378)/.370)
    passenger_profile=[(0,.006),(0,.025),(0,.065),(0,.115),(0,.151),
                       (.003,.166),(.010,.177),(.035,.186),(.075,.198),
                       (.125,.208),(.182,.213),(.203,.207),(.211,.192),
                       (.211,.145),(.211,.070),(.211,.020),(.200,.005),(.120,0),(.035,0)]
    passenger_stations=[]
    for i in range(49):
        x=.178+.570*i/48
        t=max(0,min(1,(x-.178)/.22)); fall=t*t*(3-2*t)
        passenger_stations.append((x,passenger_front(x),.672,1.055-.185*fall-.025*max(0,(x-.398)/.35)))
    _pad_loft(inside,passenger_stations,passenger_profile)
    # Surface-following original horizontal centre vent, seated on tall cheek.
    # Its black field is in front of the pad and behind a shallow moulded bezel.
    def cheek_point(x,z,depth):return (x,passenger_front(x)+depth,z)
    for outer,inner,depth,colour in (((.140,.096,.010),(.126,.082,.008),-.003,'chromeDark'),
                                     ((.126,.082,.008),(.113,.068,.006),-.006,'chrome')):
        op=_rounded_outline(.282,.762,*outer,8)
        ip=_rounded_outline(.282,.762,*inner,8)
        for i in range(len(op)):
            j=(i+1)%len(op)
            inside.face([cheek_point(*op[i],depth),cheek_point(*op[j],depth),
                         cheek_point(*ip[j],depth),cheek_point(*ip[i],depth)],colour,normal=(0,-1,0))
    # Small strips follow the curved cheek instead of a nonplanar spanning ngon.
    def vent_z(x):
        dx=max(0,abs(x-.282)-(.113/2-.006))
        dz=.068/2-.006+math.sqrt(max(0,.006**2-dx**2))
        return .762-dz,.762+dz
    for i in range(32):
        xa=.282-.113/2+.113*i/32;xb=.282-.113/2+.113*(i+1)/32
        za,zb=vent_z(xa),vent_z(xb)
        inside.face([cheek_point(xa,za[0],-.004),cheek_point(xb,zb[0],-.004),
                     cheek_point(xb,zb[1],-.004),cheek_point(xa,za[1],-.004)],'black',normal=(0,-1,0))
    for x in (.241,.257,.273,.289,.305,.321):
        inside.beam(cheek_point(x,.736,-.007),cheek_point(x,.788,-.007),.0020,'chromeDark',6)
    # Shallow lower glovebox follows the recessed passenger face.
    inside.rounded_plate((.511,.628,.619),(.435,.055,.106),.012,'black')
    trim=[(.182,passenger_front(.182)-.010,.677),(.225,passenger_front(.225)-.010,.675),
          (.282,passenger_front(.282)-.010,.672),(.360,passenger_front(.360)-.010,.669),
          (.440,passenger_front(.440)-.010,.667),(.570,passenger_front(.570)-.010,.665),
          (.733,passenger_front(.733)-.010,.663)]
    for a,b in zip(trim,trim[1:]):inside.beam(a,b,.0026,'chrome',8)
    # Bowed passenger handle and short return supports below the bright boundary.
    handle=[]
    for i in range(25):
        t=i/24;x=.397+.265*t
        handle.append((x,passenger_front(x)-.013-.035*math.sin(math.pi*t),.658-.008*math.sin(math.pi*t)))
    for a,b in zip(handle,handle[1:]):inside.beam(a,b,.0075,'black',10)
    for a,b in zip(handle,handle[1:]):
        inside.beam((a[0],a[1]-.005,a[2]+.003),(b[0],b[1]-.005,b[2]+.003),.0017,'chromeDark',6)
    for x,y,z in (handle[0],handle[-1]):inside.beam((x,passenger_front(x)+.009,z+.005),(x,y,z),.006,'black',10)
    inside.cylinder((.514,.596,.627),.005,.005,'chrome',axis='Y',segments=16)
    # Outer vertical vent follows the same broad front plane, not the end cap.
    vy=passenger_front(.695)
    inside.rounded_plate((.695,vy-.009,.750),(.056,.013,.117),.005,'chrome')
    inside.rounded_plate((.695,vy-.018,.750),(.045,.008,.105),.003,'black')
    for i in range(6):
        z=.708+i*.016
        inside.beam((.676,vy-.024,z),(.714,vy-.024,z),.0015,'chromeDark',4)
    # Centre lower heater control stack; the manual console/shifter is separate.
    inside.rounded_plate((.055,.487,.587),(.233,.100,.133),.014,'black')
    inside.rounded_plate((.055,.432,.605),(.203,.006,.069),.005,'chromeDark')
    for z,x in ((.622,.012),(.601,.078),(.581,.035)):
        inside.beam((-.031,.426,z),(.141,.426,z),.0012,'chrome',4)
        inside.box((x,.421,z),(.012,.013,.011),'chrome')


def build_cockpit(inside):
    for dial,x in enumerate((-.56,-.365,-.17)):
        y=dashboard_face_y(x)+.014
        inside.cylinder((x,y,.771),.063,.004,'black',axis='Y',segments=64)
        inside.cylinder((x,y-.0025,.771),.034,.001,'silverLight',axis='Y',segments=48)
        for index in range(25):
            angle=math.radians(-135+index*11.25)
            inner=.050 if index%2==0 else .054
            inside.beam((x+inner*math.sin(angle),y-.004,.771+inner*math.cos(angle)),
                        (x+.058*math.sin(angle),y-.004,.771+.058*math.cos(angle)),
                        .00065,'white',4)
        # Static authored dial artwork, not a gameplay instrument simulation.
        angle=math.radians(-112 if dial<2 else 24)
        inside.beam((x,y-.005,.771),
                    (x+.045*math.sin(angle),y-.005,.771+.045*math.cos(angle)),
                    .0008,'redLight',4)
        inside.cylinder((x,y-.006,.771),.004,.002,'black',axis='Y',segments=16)
        if dial==0:
            inside.beam((x,y-.005,.771),(x+.041,y-.005,.745),.0008,'redLight',4)
        if dial==1:
            inside.box((x,y-.005,.742),(.047,.001,.012),'black')
            for k in range(5):inside.box((x-.018+k*.009,y-.006,.742),(.004,.001,.006),'cream')
    inside.ellipsoid((-.035,.12,.558),(.045,.062,.020),'black',segments=24,rings=10)
    inside.beam((-.035,.12,.56),(-.035,.09,.70),.0065,'chrome')
    inside.ellipsoid((-.035,.09,.72),(.026,.026,.026),'white',segments=40,rings=24)
    def ball_point(u,v):
        return (-.035+u,.09+v,.72+math.sqrt(max(0,.026**2-u*u-v*v))+.0005)
    for path in (((-.007,-.009),(-.007,.009)),((.007,-.009),(.007,.009)),
                 ((-.007,0),(.007,0))):
        a,b=path
        samples=[(a[0]+(b[0]-a[0])*i/8,a[1]+(b[1]-a[1])*i/8) for i in range(9)]
        stroke(inside,samples,.00065,ball_point,'black',(0,0,1))
