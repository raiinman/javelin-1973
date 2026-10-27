"""Original stowed padded visors and simple upper-mounted interior mirror.

BaT048 supplies the small separate forms; positions, dimensions and hidden
support hardware are inferred. Preserve the existing Cardin ceiling and lamp.
"""
import math


def build_roof_hardware(inside, inner_roof, roof_x, roof_y):
    def roof_z(x,y):
        # Match the existing planar headliner cells, not its analytic crown.
        xa,xb=next((a,b) for a,b in zip(roof_x,roof_x[1:]) if a<=x<=b)
        ya,yb=next((a,b) for a,b in zip(roof_y,roof_y[1:]) if a<=y<=b)
        u,v=(x-xa)/(xb-xa),(y-ya)/(yb-ya)
        za=inner_roof(xa,ya)[2]*(1-u)+inner_roof(xb,ya)[2]*u
        zb=inner_roof(xa,yb)[2]*(1-u)+inner_roof(xb,yb)[2]*u
        return za*(1-v)+zb*v

    def closed_beam(a,b,radius,colour,segments):
        start=len(inside.vertices)
        inside.beam(a,b,radius,colour,segments)
        first=[inside.vertices[start+4*i] for i in range(segments)]
        last=[inside.vertices[start+4*i+3] for i in range(segments)]
        inside.face(list(reversed(first)),colour)
        inside.face(last,colour)

    def mount(x,y,w=.031,d=.023):
        points=[(x-w/2,y-d/2),(x+w/2,y-d/2),
                (x+w/2,y+d/2),(x-w/2,y+d/2)]
        upper=[(xx,yy,roof_z(xx,yy)-.0015) for xx,yy in points]
        lower=[(xx,yy,zz-.006) for xx,yy,zz in upper]
        inside.face(upper,'black');inside.face(list(reversed(lower)),'black')
        for i in range(4):
            j=(i+1)%4
            inside.face([upper[i],lower[i],lower[j],upper[j]],'black')

    def outline(cx,cy,w,d,r):
        points=[]
        for x,y,start in ((cx+w/2-r,cy+d/2-r,0),
                          (cx-w/2+r,cy+d/2-r,90),
                          (cx-w/2+r,cy-d/2+r,180),
                          (cx+w/2-r,cy-d/2+r,270)):
            for i in range(7):
                t=math.radians(start+i*90/6)
                points.append((x+r*math.cos(t),y+r*math.sin(t)))
        return points

    for side in (-1,1):
        cx,cy=side*.365,.145
        z=roof_z(cx,cy)
        # A shallow planar padded board, with rolled thickness at its outline.
        sx=(roof_z(cx+.001,cy)-roof_z(cx-.001,cy))/.002
        sy=(roof_z(cx,cy+.001)-roof_z(cx,cy-.001))/.002
        def plane(x,y):return z+sx*(x-cx)+sy*(y-cy)
        rings=[]
        for inset,drop in ((.006,.012),(0,.020),(.006,.028)):
            rings.append([(x,y,plane(x,y)-drop)
                          for x,y in outline(cx,cy,.330-2*inset,.150-2*inset,.018-inset)])
        inside.face(rings[0],'black')
        inside.face(list(reversed(rings[-1])),'black')
        for a,b in zip(rings,rings[1:]):
            for i in range(len(a)):
                j=(i+1)%len(a)
                inside.face([a[i],b[i],b[j],a[j]],'black')
        # Small outer pivot and inner retained rod, attached below the cloth.
        for x in (side*.560,side*.205):
            mount(x,.235,w=.026 if abs(x)<.3 else .031)
            top=(x,.235,roof_z(x,.235)-.0075)
            foot=(x,.210,plane(x,.210)-.020)
            closed_beam(top,foot,.0036,'chromeDark',10)
            inside.ellipsoid(foot,(.005,.005,.005),'black',segments=12,rings=6)
        hinge_z=plane(side*.500,.210)-.020
        inside.cylinder((side*.515,.210,hinge_z),.0035,.090,
                        'chromeDark',axis='X',segments=12)

    # Roof/header base and short stalk. No modern overhead console or screen.
    mount(0,.235,w=.032,d=.025)
    closed_beam((0,.235,roof_z(0,.235)-.0075),(0,.218,1.207),
                .0045,'chromeDark',12)
    inside.ellipsoid((0,.218,1.207),(.007,.007,.007),'black',segments=16,rings=8)
    start=len(inside.vertices)
    inside.rounded_plate((0,0,0),(.230,.018,.065),.009,'black',segments=8)
    inside.rounded_plate((0,-.010,.000),(.215,.002,.051),.006,'chromeDark',segments=8)
    # Cabin-facing rectangular surface has a small toe toward the driver.
    c,s=math.cos(-.10),math.sin(-.10)
    for i in range(start,len(inside.vertices)):
        x,y,z=inside.vertices[i]
        inside.vertices[i]=(c*x-s*y,s*x+c*y+.208,z+1.174)
