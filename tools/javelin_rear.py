"""Original curved rear fascia with real lamp apertures and thin rolled bezels."""
import math


def build_rear_bumper(body,centre_y):
    """Swept chrome section with rolled edges and a lower plate notch."""
    columns=sorted(set([i*.89/24 for i in range(-24,25)]+
                       [-.19,-.18,-.17,-.16,.16,.17,.18,.19]))
    rings=[]
    for x in columns:
        fraction=abs(x)/.89
        y=centre_y+.10*fraction**5
        top=.490-.020*fraction**4
        notch=max(0,min(1,(.19-abs(x))/.03))
        notch=notch*notch*(3-2*notch)
        low=.345+.008*fraction**2+.060*notch
        rings.append([(x,y+dy,z) for dy,z in
                      ((.045,top-.012),(-.015,top),(-.055,top-.018),
                       (-.060,low+.025),(-.045,low+.006),(.045,low))])
    for a,b in zip(rings,rings[1:]):
        for i in range(6):
            j=(i+1)%6
            body.face([a[i],a[j],b[j],b[i]],'chrome')
    body.face(list(reversed(rings[0])),'chrome')
    body.face(rings[-1],'chrome')
    for x in (-.57,.57):
        body.rounded_plate((x,centre_y-.012,.425),(.078,.145,.190),.012,'rubber')


def build_trunk_lid(trunk,front,rear):
    """Shallow crowned closed lid, retaining its four body seam anchors."""
    def top(u,t):
        half=.84-.02*t
        return (u*half,(front-.006)*(1-t)+rear*t,
                .940-.050*t+.012*(1-u*u)*math.sin(math.pi*t))
    rows=[i/16 for i in range(17)]
    columns=[i/16 for i in range(-16,17)]
    for a,b in zip(rows,rows[1:]):
        for u,v in zip(columns,columns[1:]):
            points=[top(u,a),top(u,b),top(v,b),top(v,a)]
            trunk.face(points,'red',normal=(0,0,1))
            trunk.face([(x,y,z-.012) for x,y,z in reversed(points)],'redDark')
    perimeter=([top(-1,t) for t in rows]+[top(u,1) for u in columns[1:]]+
               [top(1,t) for t in reversed(rows[:-1])]+
               [top(u,0) for u in reversed(columns[1:-1])])
    for a,b in zip(perimeter,perimeter[1:]+perimeter[:1]):
        trunk.face([a,(a[0],a[1],a[2]-.012),(b[0],b[1],b[2]-.012),b],'redDark')


def spoiler_height(x):
    t=max(0,min(1,(abs(x)-.775)/.075))
    return 1.020-.010*(x/.850)**2-.060*(1-math.sqrt(max(0,1-t*t)))


def spoiler_rear_point(x,z,tail_face):
    t=max(0,min(1,(z-.840)/(spoiler_height(x)-.840)))
    bow=.030*(abs(x)/.850)**4
    radius=math.sqrt((x/.0544375)**2+((z-.935)/.065)**2)
    # A pressed oval cup with a tangent outer blend, not a cylindrical bore.
    well=.048*max(0,1-radius*radius)**1.25
    return (x,tail_face-.032+bow-.010*t*t+.008*math.sin(math.pi*t)+well,z)


def build_spoiler(trunk,deck_rear,tail_face):
    """Raised moving deck spoiler, with rounded ends and a latch depression."""
    columns=sorted(set(round(x,9) for x in ([i*.850/24 for i in range(-24,25)]+
                       [i*.0045 for i in range(-20,21)]+
                       [side*(.74+i*.005) for side in (-1,1) for i in range(23)]+
                       [side*x for side in (-1,1) for x in (.848,.849,.8498)])))
    levels=[i/60 for i in range(61)]
    def rear(x,t):
        return spoiler_rear_point(x,.840+(spoiler_height(x)-.840)*t,tail_face)
    rings=[]
    for x in columns:
        front=(x*.821/.850,deck_rear+.015,.895)
        crest=spoiler_height(x)
        lip_t=1-.010/(crest-.840)
        below=rear(x,lip_t)
        top=(below[0],below[1]+.010,crest)
        ramp=[]
        for index in range(13):
            t=index/12
            ramp.append((front[0]*(1-t)+top[0]*t,front[1]*(1-t)+top[1]*t,
                         front[2]+(top[2]-front[2])*t*t*(3-2*t)))
        lip=[]
        for index in range(1,7):
            angle=index*math.pi/12
            lip.append((x,below[1]+.010-.010*math.sin(angle),
                        crest-.010+.010*math.cos(angle)))
        # Full end cheeks join the curved ramp to the lower lid return.
        # A folded thin U here leaves an exposed triangular hole at both ends.
        ring=ramp+lip+[rear(x,t*lip_t) for t in reversed(levels[:-1])]
        bottom=rear(x,0)
        # Thin pressed backing follows the actual lower cup instead of
        # crossing the depressed outer wall with a flat vertical return.
        backing_top=.887+.026*(abs(x)/.850)**8
        for step in range(17):
            backing_z=.840+(backing_top-.840)*step/16
            backing=spoiler_rear_point(x,backing_z,tail_face)
            ring.append((x,backing[1]+.005,backing_z))
        ring.append((front[0],front[1],front[2]-.008))
        rings.append(ring)
    for a,b in zip(rings,rings[1:]):
        for i in range(len(a)):
            j=(i+1)%len(a)
            trunk.face([a[i],a[j],b[j],b[i]],'red')
    trunk.face(list(reversed(rings[0])),'red')
    trunk.face(rings[-1],'red')
    latch_y=spoiler_rear_point(0,.906,tail_face)[1]-.002
    trunk.cylinder((0,latch_y,.906),.012,.005,'chrome',axis='Y',segments=24)


def rear_fascia_depth(x,tail_face):
    return tail_face-.012+.022*(abs(x)/.85)**3

def rear_fascia_half_height(x):
    offset=max(0,abs(x)-(.85-.055))
    return .285/2-.055+math.sqrt(max(0,.055*.055-offset*offset))

def build_lower_rear(body,tail_face,columns):
    """Replace the old independent rounded block with a shared-edge lower panel."""
    def front(x,z):return (x,rear_fascia_depth(x,tail_face),z)
    def low(x):
        offset=max(0,min(.09,abs(x)-(.85-.09)))
        return .210+.09-math.sqrt(max(0,.09*.09-offset*offset))
    def top(x):return .730-rear_fascia_half_height(x)
    for a,b in zip(columns,columns[1:]):
        points=[front(a,low(a)),front(b,low(b)),front(b,top(b)),front(a,top(a))]
        back=[(x,y+.15,z) for x,y,z in points]
        body.face(points,'red')
        body.face(list(reversed(back)),'redDark')
        body.face([points[0],back[0],back[1],points[1]],'redDark')
        # Fascia's 18mm inner skin joins this return. There is no duplicate
        # cap between the fascia and the lower panel's continuous outer face.
        body.face([(points[3][0],points[3][1]+.018,points[3][2]),
                   (points[2][0],points[2][1]+.018,points[2][2]),back[2],back[3]],'redDark')
    for x,reverse in ((columns[0],False),(columns[-1],True)):
        p=front(x,low(x));q=front(x,top(x))
        face=[p,q,(q[0],q[1]+.15,q[2]),(p[0],p[1]+.15,p[2])]
        body.face(list(reversed(face)) if reverse else face,'redDark')

def build_rear(body,tail_face):
    centres=(-.67,-.43,.43,.67)
    def depth(x):
        return rear_fascia_depth(x,tail_face)
    def half_height(x,width,height,radius):
        offset=max(0,abs(x)-(width/2-radius))
        return height/2-radius+math.sqrt(max(0,radius*radius-offset*offset))
    def patch(points,lower_join=False):
        rear=[(x,y+.018,z) for x,y,z in points]
        body.face(points,'red')
        body.face(list(reversed(rear)),'redDark')
        for i in range(4):
            if i==0 and lower_join:continue
            j=(i+1)%4
            body.face([points[i],rear[i],rear[j],points[j]],'redDark')
    columns=set([-.85,.85]+[i*.017 for i in range(-50,51)])
    for centre in centres:
        columns.update(centre+dx for dx in (-.1025,-.070,-.035,0,.035,.070,.1025))
    columns=sorted(set(round(x,6) for x in columns if -.850001<=x<=.850001))
    build_lower_rear(body,tail_face,columns)
    for a,b in zip(columns,columns[1:]):
        centre=next((c for c in centres if abs((a+b)/2-c)<.1025),None)
        low_a,high_a=.730-rear_fascia_half_height(a),.730+rear_fascia_half_height(a)
        low_b,high_b=.730-rear_fascia_half_height(b),.730+rear_fascia_half_height(b)
        intervals=[(low_a,low_b,high_a,high_b)]
        if centre is not None:
            ha=half_height(a-centre,.205,.135,.035)
            hb=half_height(b-centre,.205,.135,.035)
            intervals=[(low_a,low_b,.720-ha,.720-hb),(.720+ha,.720+hb,high_a,high_b)]
        for za,zb,zc,zd in intervals:
            patch([(a,depth(a),za),(b,depth(b),zb),(b,depth(b),zd),(a,depth(a),zc)],
                  lower_join=abs(za-low_a)<1e-10 and abs(zb-low_b)<1e-10)
    for centre in centres:
        rings=[]
        # Thin bright outer lip, with the cavity extending into the fascia.
        for width,height,radius,offset in ((.225,.165,.045,.001),
                                          (.225,.165,.045,-.005),
                                          (.205,.135,.035,-.006),
                                          (.191,.121,.030,.024)):
            ring=[]
            for cx,cz,start in ((width/2-radius,height/2-radius,0),
                                (-width/2+radius,height/2-radius,90),
                                (-width/2+radius,-height/2+radius,180),
                                (width/2-radius,-height/2+radius,270)):
                for step in range(7):
                    theta=math.radians(start+step*90/6)
                    x=centre+cx+radius*math.cos(theta)
                    ring.append((x,depth(x)+offset,.720+cz+radius*math.sin(theta)))
            rings.append(ring)
        for index,(aa,bb) in enumerate(zip(rings,rings[1:]+rings[:1])):
            for i in range(len(aa)):
                j=(i+1)%len(aa)
                body.face([aa[i],aa[j],bb[j],bb[i]],'chromeDark' if index==2 else 'chrome')
        yy=depth(centre)+.026
        body.rounded_plate((centre,yy,.720),(.191,.006,.121),.030,'tail')
        body.rounded_plate((centre,yy-.004,.754),(.156,.003,.018),.007,'brakeRed')
        if abs(centre)<.5:
            body.rounded_plate((centre,yy-.004,.710),(.150,.003,.047),.016,'cream')
    yy=depth(0)
    for radius,offset,length,colour in ((.028,-.004,.012,'chrome'),(.020,-.011,.003,'blue'),
                                        (.014,-.014,.002,'white'),(.008,-.016,.001,'red')):
        body.cylinder((0,yy+offset,.725),radius,length,colour,axis='Y',segments=24)
