"""Original visible engine-bay forms observed in the restored-car video."""
import math


def build_engine(body):
    # Closed curved inner housings bridge the flat liner to the outer arch.
    for side in (-1,1):
        rings=[]
        for x,radius in ((side*.53,.425),(side*.89,.425),
                         (side*.89,.435),(side*.53,.435)):
            rings.append([(x,1.43+radius*math.cos(i*math.pi/32),
                           .34+radius*math.sin(i*math.pi/32)) for i in range(33)])
        for k in range(4):
            a,b=rings[k],rings[(k+1)%4]
            for i in range(32):
                body.face([a[i],a[i+1],b[i+1],b[i]],'black')
        for i in (0,32):
            body.face([ring[i] for ring in rings],'black')
    body.box((0,1.57,.44),(1.08,1.15,.11),'shadow')
    body.box((0,1.46,.58),(.48,.67,.29),'engine')
    # Rounded pressed covers, with tapered longitudinal ends.
    for side in (-1,1):
        rings=[]
        for y,scale in ((-.33,.02),(-.315,.65),(-.29,1),(.29,1),(.315,.65),(.33,.02)):
            ring=[]
            for i in range(24):
                angle=2*math.pi*i/24
                c,s=math.cos(angle),math.sin(angle)
                ring.append((side*.26+.065*scale*math.copysign(abs(c)**.45,c),
                             1.45+y,.69+.065*scale*math.copysign(abs(s)**.45,s)))
            rings.append(ring)
        for a,b in zip(rings,rings[1:]):
            for i in range(24):
                j=(i+1)%24
                body.face([a[i],a[j],b[j],b[i]],'chromeDark')
        body.face(list(reversed(rings[0])),'chromeDark')
        body.face(rings[-1],'chromeDark')
    # Rolled can and domed lid. The label retains its radius .276m support.
    profile=((.245,.753),(.255,.762),(.275,.772),(.275,.820),
             (.266,.832),(.220,.844),(.100,.848),(.012,.850))
    rings=[[(r*math.cos(i*math.tau/64),1.47+r*math.sin(i*math.tau/64),z)
            for i in range(64)] for r,z in profile]
    for a,b in zip(rings,rings[1:]):
        for i in range(64):
            j=(i+1)%64
            body.face([a[i],a[j],b[j],b[i]],'black')
    body.face(list(reversed(rings[0])),'black')
    body.face(rings[-1],'black')
    body.cylinder((0,1.47,.854),.011,.008,'chromeDark',axis='Z',segments=24)
    body.box((0,2.04,.60),(1.22,.08,.28),'grille')
    for i in range(-8,9):
        body.box((i*.07,2.088,.60),(.008,.012,.24),'black')
    body.box((.43,1.76,.63),(.22,.28,.20),'black')
    for x in (.38,.49):
        body.cylinder((x,1.76,.738),.016,.015,'steel',axis='Z',segments=8)
    hose=((- .24,1.68,.73),(-.32,1.77,.75),(-.40,1.86,.72),(-.40,1.98,.68))
    for a,b in zip(hose,hose[1:]):
        body.beam(a,b,.019,'rubber',16)
    for point in hose[1:-1]:
        body.ellipsoid(point,(.019,.019,.019),'rubber',segments=16,rings=8)
    body.ellipsoid((-.41,.92,.68),(.11,.055,.11),'chromeDark',segments=32,rings=16)
    body.rounded_plate((-.41,1.04,.70),(.07,.16,.06),.012,'steel')
