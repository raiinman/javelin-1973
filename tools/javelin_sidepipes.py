"""Original paired side pipes, close-set rocker fit and perforated chrome guards."""
import math

PIPE_X=.835
PIPE_Z=.217
GUARD_RADIUS=.055


def _bezier(a,b,c,steps=12):
    return [tuple((1-t)**2*a[k]+2*t*(1-t)*b[k]+t*t*c[k] for k in range(3))
            for t in (i/steps for i in range(steps+1))]


def _tube(part,path,side):
    rings=[]
    for index,p in enumerate(path):
        a,b=path[max(0,index-1)],path[min(len(path)-1,index+1)]
        tangent=[b[k]-a[k] for k in range(3)]
        length=math.sqrt(sum(v*v for v in tangent))
        tx,ty,tz=(v/length for v in tangent)
        xy=math.hypot(tx,ty)
        ux,uy=ty/xy,-tx/xy
        v=(-uy*tz,ux*tz,uy*tx-ux*ty)
        # Keep the local circular section independent of left/right reflection.
        sections=[]
        for radius in (.040,.034):
            sections.append([(side*(p[0]+radius*(ux*math.cos(t)+v[0]*math.sin(t))),
                              p[1]+radius*(uy*math.cos(t)+v[1]*math.sin(t)),
                              p[2]+radius*v[2]*math.sin(t))
                             for t in (i*math.tau/40 for i in range(40))])
        rings.append(sections)
    for a,b in zip(rings,rings[1:]):
        for shell,colour in ((0,'chrome'),(1,'shadow')):
            for i in range(40):
                j=(i+1)%40
                finish='chromeDark' if shell==0 and -.8<(a[0][i][1]+b[0][i][1])/2<.78 else colour
                part.face([a[shell][i],a[shell][j],b[shell][j],b[shell][i]],finish)
    for ring in (rings[0],rings[-1]):
        for i in range(40):
            j=(i+1)%40
            part.face([ring[0][i],ring[0][j],ring[1][j],ring[1][i]],'chrome')


def _guard(part,side):
    # True openings in a curved thin shell, rather than black bars on a pipe.
    slots=[-.710+i*.048 for i in range(29)]
    ys=sorted(set([-.770,.700]+[v+d for v in slots for d in (-.007,.007)]))
    angles=tuple(math.radians(a) for a in (-70,-50,-25,-10,5,20,35,50,55,70,90,110))
    cells=[]
    def point(y,angle,radius):
        return (side*(PIPE_X+radius*math.cos(angle)),y,PIPE_Z+radius*math.sin(angle))
    edge_counts={}
    for j,(a,b) in enumerate(zip(ys,ys[1:])):
        slot=any(abs((a+b)/2-centre)<.0071 for centre in slots)
        for i,(lo,hi) in enumerate(zip(angles,angles[1:])):
            if slot and math.radians(-25)<=(lo+hi)/2<=math.radians(55):continue
            ids=((j,i),(j+1,i),(j+1,i+1),(j,i+1))
            cells.append(ids)
            for aa,bb in zip(ids,ids[1:]+ids[:1]):
                key=tuple(sorted((aa,bb)))
                edge_counts[key]=edge_counts.get(key,0)+1
    def p(vertex,inner=False):
        j,i=vertex
        return point(ys[j],angles[i],GUARD_RADIUS-(.0015 if inner else 0))
    for ids in cells:
        part.face([p(v) for v in ids],'chrome')
        part.face([p(v,True) for v in reversed(ids)],'chromeDark')
    for (a,b),count in edge_counts.items():
        if count==1:part.face([p(a),p(b),p(b,True),p(a,True)],'chrome')
    # Closed rolled end bands, without a painted runner.
    for y in (-.770,.700):
        rings=[[point(y+dy,a,r) for a in angles]
               for dy,r in ((-.006,.055),(-.003,.057),(.003,.057),
                            (.006,.055),(.006,.0535),(-.006,.0535))]
        for aa,bb in zip(rings,rings[1:]+rings[:1]):
            for i in range(len(angles)-1):
                part.face([aa[i],aa[i+1],bb[i+1],bb[i]],'chrome')
        for index in (0,len(angles)-1):
            part.face([ring[index] for ring in rings],'chrome')


def build_sidepipe(part,side):
    inlet=_bezier((.620,.990,.247),(PIPE_X,1.000,PIPE_Z),
                  (PIPE_X,.780,PIPE_Z),16)
    outlet=_bezier((PIPE_X,-.800,PIPE_Z),(PIPE_X,-.940,PIPE_Z),
                   (.890,-.980,.237),12)
    _tube(part,inlet+[(PIPE_X,-.800,PIPE_Z)]+outlet[1:],side)
    _guard(part,side)
