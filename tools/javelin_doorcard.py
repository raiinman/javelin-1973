"""Original padded interior door cards, pleated pulls and manual cranks."""
import math


def build_doorcard(door,side):
    def plaque(y,z,width,height,radius,x,depth,colour):
        perimeter=[]
        for cy,cz,start in ((width/2-radius,height/2-radius,0),
                            (-width/2+radius,height/2-radius,90),
                            (-width/2+radius,-height/2+radius,180),
                            (width/2-radius,-height/2+radius,270)):
            for i in range(7):
                a=math.radians(start+i*15)
                perimeter.append((y+cy+radius*math.cos(a),z+cz+radius*math.sin(a)))
        rings=[[(side*(x+d),yy,zz) for yy,zz in perimeter] for d in (-depth/2,depth/2)]
        door.face(rings[0],colour,normal=(-side,0,0))
        door.face(rings[1],colour,normal=(side,0,0))
        for i in range(len(perimeter)):
            j=(i+1)%len(perimeter)
            door.face([rings[0][i],rings[0][j],rings[1][j],rings[1][i]],colour)
    plaque(.14,.58,1.13,.46,.045,.815,.025,'black')
    plaque(.10,.735,.96,.105,.014,.796,.012,'chrome')
    plaque(.10,.735,.948,.093,.010,.788,.008,'seat')
    y=.20
    for colour,width in (('wine',.014),('pink',.021),('cream',.042),
                        ('black',.005),('cream',.042),('pink',.021),('wine',.014)):
        door.box((side*.782,y+width/2,.735),(.004,width,.087),colour)
        y+=width
    # Nine padded divisions on one broad pull, with an undercut lower return.
    profile=((.794,.655),(.776,.652),(.753,.610),(.750,.585),
             (.760,.567),(.789,.557),(.802,.566),(.802,.645))
    rows=sorted(set([-.35,.34]+[-.35+i*.69/9+d for i in range(1,9) for d in (-.002,0,.002)]))
    rings=[]
    for y in rows:
        nearest=min(abs(y-(-.35+i*.69/9)) for i in range(1,9))
        seam=.0025*max(0,1-nearest/.002)
        end=max(0,1-min(y+.35,.34-y)/.035)
        rings.append([(side*(x+seam+.010*end),y,z) for x,z in profile])
    for a,b in zip(rings,rings[1:]):
        for i in range(len(profile)):
            j=(i+1)%len(profile)
            door.face([a[i],b[i],b[j],a[j]],'black')
    door.face(list(reversed(rings[0])),'black')
    door.face(rings[-1],'black')
    # Release and separate manual window crank, not a substitute single lever.
    plaque(.43,.645,.070,.075,.008,.778,.008,'chrome')
    plaque(.43,.645,.055,.060,.005,.771,.004,'black')
    door.beam((side*.765,.445,.662),(side*.754,.415,.628),.006,'chrome',10)
    door.cylinder((side*.772,.55,.54),.021,.008,'chrome',axis='X',segments=32)
    door.cylinder((side*.765,.55,.54),.014,.006,'chromeDark',axis='X',segments=24)
    door.beam((side*.762,.55,.54),(side*.748,.525,.471),.006,'chrome',10)
    door.ellipsoid((side*.742,.525,.467),(.014,.014,.014),'black',20,12)
    for y in (-.35,.0,.34,.65):
        door.cylinder((side*.799,y,.375),.003,.003,'chromeDark',axis='X',segments=12)

    from javelin_doorcrest import build_cardin_door_crest
    build_cardin_door_crest(door,side)
