"""Consume original editable millimetre SVG and seat it on actual mesh triangles.

The drawing is independent of legacy hood/fender contour functions. SVG uses
M/L/C/Z only, absolute physical plan coordinates. Projection helpers are shared
technical infrastructure, not shared artwork.
"""
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from javelin_decals import _triangle_clip, _triangulate_outline, clean_decal_outline


def path_points(data):
    tokens=re.findall(r'[MLCZ]|[-+]?(?:\d*\.)?\d+(?:[eE][-+]?\d+)?',data)
    points=[];i=0;closed=False
    def pair():
        nonlocal i
        p=(float(tokens[i])/1000,float(tokens[i+1])/1000);i+=2
        return p
    while i<len(tokens):
        op=tokens[i];i+=1
        if op in ('M','L'):points.append(pair())
        elif op=='C':
            a=points[-1];b,c,d=pair(),pair(),pair()
            # Physical curve length controls sampling, independent of support.
            count=max(8,min(40,math.ceil(sum(math.dist(x,y) for x,y in ((a,b),(b,c),(c,d)))/.018)))
            for k in range(1,count+1):
                t=k/count;s=1-t
                points.append(tuple(s*s*s*a[j]+3*s*s*t*b[j]+3*s*t*t*c[j]+t*t*t*d[j] for j in (0,1)))
        elif op=='Z':closed=True
        else:raise ValueError('Unsupported SVG operation '+op)
    return points,closed


def artwork():
    root=ET.parse(Path(__file__).resolve().parents[1]/'assets/front-artwork.svg').getroot()
    triangles=[]
    for path in root.findall('{http://www.w3.org/2000/svg}path'):
        points,closed=path_points(path.attrib['d'])
        if path.get('fill')!='none':
            if not closed:raise ValueError('Filled artwork must be closed')
            triangles.extend(_triangulate_outline(points))
        else:
            # A single continuous narrow ribbon with shared miter joins avoids
            # overlapping segment quads and reflection seams.
            half=float(path.attrib['stroke-width'])/2000
            left=[];right=[]
            for k,p in enumerate(points):
                a=points[max(0,k-1)];b=points[min(len(points)-1,k+1)]
                dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
                nx,ny=-dy/length*half,dx/length*half
                left.append((p[0]+nx,p[1]+ny));right.append((p[0]-nx,p[1]-ny))
            for k in range(len(points)-1):
                triangles.extend(_triangulate_outline([left[k],left[k+1],right[k+1],right[k]]))
    return [(p,(min(x for x,y in p),max(x for x,y in p),min(y for x,y in p),max(y for x,y in p))) for p in triangles]


def project(part,support,art):
    count=0
    for triangle in support:
        a,b,c=triangle
        ab=tuple(b[i]-a[i] for i in range(3));ac=tuple(c[i]-a[i] for i in range(3))
        normal=(ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0])
        if abs(normal[2])<1e-12:continue
        direction=1 if normal[2]>0 else -1
        normal=tuple(v*direction/math.sqrt(sum(w*w for w in normal)) for v in normal)
        uv=[(p[0],p[1]) for p in triangle]
        bounds=(min(p[0] for p in uv),max(p[0] for p in uv),min(p[1] for p in uv),max(p[1] for p in uv))
        for polygon,box in art:
            if box[1]<bounds[0] or box[0]>bounds[1] or box[3]<bounds[2] or box[2]>bounds[3]:continue
            clipped=_triangle_clip(polygon,uv)
            if len(clipped)<3:continue
            area=abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(clipped,clipped[1:]+clipped[:1])))/2
            if area<1e-10:continue
            points=clean_decal_outline([(x,y,a[2]-(normal[0]*(x-a[0])+normal[1]*(y-a[1]))/normal[2]+.0008) for x,y in clipped])
            if points:part.face(points,'black',normal=normal);count+=1
    return count


def build_front_artwork(body,hood,hood_point,hood_x,hood_y,fender_point,fender_y,fender_t,fender_triangles):
    art=artwork();hood_support=[];wing_support=[]
    for ya,yb in zip(hood_y,hood_y[1:]):
        for xa,xb in zip(hood_x,hood_x[1:]):
            quad=[hood_point(xa,ya),hood_point(xb,ya),hood_point(xb,yb),hood_point(xa,yb)]
            hood_support.extend([[quad[i] for i in ids] for ids in ((0,1,2),(0,2,3))])
    for side in (-1,1):
        for ya,yb in zip(fender_y,fender_y[1:]):
            for ta,tb in zip(fender_t,fender_t[1:]):
                domain=[(ta,ya),(ta,yb),(tb,yb),(tb,ya)]
                tris=fender_triangles(ya,yb,ta,tb) if fender_triangles else [[domain[i] for i in ids] for ids in ((0,1,2),(0,2,3))]
                wing_support.extend([[fender_point(side,y,t) for t,y in tri] for tri in tris])
    build_hood_script(hood,hood_point,hood_x,hood_y)
    print('J73_FRESH_SVG_ART',project(hood,hood_support,art),'hood faces',project(body,wing_support,art),'fixed wing faces')


def build_hood_script(hood, hood_point, hood_x, hood_y):
    """Original hand-drawn cursive cast badge from the target video0:05.

    No font, pixel trace or external geometry is imported. Position/size and
    hidden mounting are inferred. Driver side is source-X, on the moving hood.
    """
    paths=[[(.00,.92),(.08,.76),(.17,.78),(.29,1.12),(.27,1.20),
            (.21,.92),(.18,.37),(.12,.06),(.04,.08),(.01,.25),(.10,.12),(.23,.29)],
           [(.23,.25),(.30,.42),(.36,.37),(.32,.14),(.25,.12),(.24,.25),
            (.31,.42),(.37,.42),(.35,.17),(.39,.16)],
           [(.39,.16),(.42,.39),(.43,.12),(.48,.13),(.55,.43),(.53,.28),(.56,.23)],
           [(.56,.23),(.62,.27),(.65,.39),(.61,.43),(.56,.29),(.57,.14),(.63,.11),(.68,.18)],
           [(.68,.18),(.73,.60),(.79,1.06),(.76,1.10),(.72,.87),(.68,.40),(.69,.14),(.74,.11),(.78,.20)],
           [(.79,.37),(.77,.14),(.81,.12),(.85,.20)],
           [(.85,.20),(.86,.38),(.83,.14),(.88,.36),(.93,.37),(.90,.12),(.94,.12),(1.,.19)],
           [(.802,.54),(.812,.56)]]
    def support(x,y):
        ix=next(i for i in range(len(hood_x)-1) if hood_x[i]-1e-10<=x<=hood_x[i+1]+1e-10)
        iy=next(i for i in range(len(hood_y)-1) if hood_y[i]-1e-10<=y<=hood_y[i+1]+1e-10)
        xa,xb=hood_x[ix:ix+2];ya,yb=hood_y[iy:iy+2]
        u=(x-xa)/(xb-xa);v=(y-ya)/(yb-ya)
        z00=hood_point(xa,ya)[2];z10=hood_point(xb,ya)[2]
        z11=hood_point(xb,yb)[2];z01=hood_point(xa,yb)[2]
        return z00+u*(z10-z00)+v*(z11-z10) if v<=u else z00+u*(z11-z01)+v*(z01-z00)
    for path in paths:
        # Centripetal-looking restrained interpolation, original drawing knots
        # remain explicit and editable. Endpoints duplicated for stable caps.
        points=[]
        ext=[path[0]]+path+[path[-1]]
        for j in range(1,len(ext)-2):
            p0,p1,p2,p3=ext[j-1:j+3]
            for sample in range(6):
                t=sample/6
                points.append(tuple(.5*((2*p1[k])+(-p0[k]+p2[k])*t+
                    (2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+
                    (-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t) for k in (0,1)))
        points.append(path[-1]);rings=[]
        for i,(u,v) in enumerate(points):
            x=-.255-u*.240;y=2.285-v*.043
            a=points[max(0,i-1)];b=points[min(len(points)-1,i+1)]
            dx=-(b[0]-a[0])*.240;dy=-(b[1]-a[1])*.043
            length=math.hypot(dx,dy)
            if length<1e-10:continue
            nx,ny=-dy/length,dx/length
            ring=[]
            for k in range(8):
                theta=k*math.tau/8
                xx=x+nx*.00115*math.cos(theta);yy=y+ny*.00115*math.cos(theta)
                ring.append((xx,yy,support(xx,yy)+.00215+.00065*math.sin(theta)))
            rings.append(ring)
        if not rings:continue
        hood.face(list(reversed(rings[0])),'chrome')
        hood.face(rings[-1],'chrome')
        for a,b in zip(rings,rings[1:]):
            for k in range(8):hood.face([a[k],a[(k+1)%8],b[(k+1)%8],b[k]],'chrome')
