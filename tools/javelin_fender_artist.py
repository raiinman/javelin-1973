"""Original broad convex front shoulder experiment, source metres."""

def artist_point(side,y,t,original,outer,side_z,side_slope,hood_z):
    if not .79<y<2.34:return original
    def smooth(a):
        a=max(0,min(1,a));return a*a*(3-2*a)
    blend=smooth((y-.79)/.23)*smooth((2.34-y)/.26)
    inner=.706;span=outer-inner;cut=.35;run=.62*span
    high=max(hood_z+.032,side_z+.012)
    outer_slope=-.08
    if t>=cut:
        u=(1-t)/(1-cut)
        rise=high-hood_z
        x=inner+run*u
        z=hood_z+(2*rise-outer_slope*run)*u+(-rise+outer_slope*run)*u*u
    else:
        dx=-run/(1-cut);dz=outer_slope*dx
        p3=(inner+run,high)
        p2=(p3[0]-dx*cut/3,p3[1]-dz*cut/3)
        lift=.75*(high-side_z)
        if side_slope<0:lift=min(lift,.92*(outer-p2[0])/-side_slope)
        p1=(outer+side_slope*lift,side_z+lift)
        p0=(outer,side_z);u=t/cut
        weights=((1-u)**3,3*(1-u)**2*u,3*(1-u)*u*u,u**3)
        x=sum(w*p[0] for w,p in zip(weights,(p0,p1,p2,p3)))
        z=sum(w*p[1] for w,p in zip(weights,(p0,p1,p2,p3)))
    return (original[0]*(1-blend)+side*x*blend,y,original[2]*(1-blend)+z*blend)
