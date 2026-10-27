"""Original localized fixed-wing/fascia terminal roll, source metres."""
from functools import lru_cache
from javelin_front import front_upper_point,front_columns

@lru_cache(maxsize=None)
def _end(x):return front_upper_point(x)

def terminal_wing_point(side,y,t,wing):
    start=wing(1,2.34,t)
    end=_end(start[0]);u=max(0,min(1,(y-2.34)/.05))
    run=end[1]-2.34
    # Quadratic depth turns vertically into the unchanged fascia upper edge.
    yy=2.34+run*(2*u-u*u)
    e=.00001;previous=wing(1,2.34-e,t)
    x_slope=(start[0]-previous[0])/e
    z_slope=(start[2]-previous[2])/e
    drop=start[2]-end[2]
    tangent=z_slope*2*run
    end_tangent=-min(.012,max(.003,drop))
    zz=((2*u**3-3*u*u+1)*start[2]+(u**3-2*u*u+u)*tangent
        +(-2*u**3+3*u*u)*end[2]+(u**3-u*u)*end_tangent)
    xx=start[0]+x_slope*2*run*u*(1-u)*(1-u)
    return side*xx,yy,zz

def terminal_side_point(side,y,z,base,wing,side_top,side_x):
    if y<=2.34 or z<=.70:return base
    top=side_top(y);weight=max(0,min(1,(z-.70)/(top-.70)))
    target=terminal_wing_point(side,y,0,wing)
    old_top=(side*side_x(y,top),y,top)
    return tuple(base[i]+weight*(target[i]-old_top[i]) for i in range(3))

def terminal_front_contract(wing,ts):
    xs=[abs(wing(1,2.34,t)[0]) for t in ts]
    return {'join_x':sorted(set(xs+[-x for x in xs])), 'outer_x':max(xs)}

@lru_cache(maxsize=None)
def terminal_end_splits(wing):
    outer=wing(1,2.34,0)[0];inner=wing(1,2.34,1)[0];result=[]
    for x in front_columns():
        if inner<x<outer:
            low,high=0.,1.
            for _ in range(45):
                mid=(low+high)/2
                if wing(1,2.34,mid)[0]>x:low=mid
                else:high=mid
            result.append((low+high)/2)
    return tuple(sorted(result))

def terminal_cell_triangles(ya,yb,ta,tb,wing):
    if yb>2.34+1e-9:
        extra=[t for t in terminal_end_splits(wing) if ta+1e-9<t<tb-1e-9]
        if ya<=2.34+1e-9:
            polygon=[(ta,ya),(ta,yb)]+[(t,yb) for t in extra]+[(tb,yb),(tb,ya)]
            return tuple((polygon[0],polygon[i],polygon[i+1]) for i in range(1,len(polygon)-1))
        ts=[ta]+extra+[tb];triangles=[]
        for a,b in zip(ts,ts[1:]):
            triangles.extend((((a,ya),(a,yb),(b,yb)),((a,ya),(b,yb),(b,ya))))
        return tuple(triangles)
    return (((ta,ya),(ta,yb),(tb,yb)),((ta,ya),(tb,yb),(tb,ya)))
