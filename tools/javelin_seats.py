"""Original rounded, reclined Cardin seat padding and surface-following ribbons."""
import math
from javelin_decals import _triangle_clip


def back_scale(z):
    t=max(0,min(1,(z-.425)/.510))
    return .88+.12*math.sin(math.pi*t)-.12*t**5


def build_seats(inside):
    def padded_box(centre,size,radius,recline=False,is_bench=False):
        halves=[value/2 for value in size]
        grids=[sorted(set((-h,-h+radius*.2,-h+radius*.6,-h+radius,0,
                           -h*.65,-h*.35,h*.35,h*.65,
                           h-radius,h-radius*.6,h-radius*.2,h))) for h in halves]
        if not recline:
            grids[1]=sorted(set(grids[1]+[.09,.115,.13,.145,.16,.19,.215,.235]))
        if recline:
            grids[0]=sorted(set(grids[0]+[-halves[0]+i*size[0]/20 for i in range(21)]))
            grids[2]=sorted(set(grids[2]+[.54-centre[2],.60-centre[2],.75-centre[2],.84-centre[2]]))
            # Sample both raised cream channels rather than losing their
            # volume between the coarse perimeter stations.
            grids[0]=sorted(set(grids[0]+[sign*(halves[0]-.025-inset)
                for sign in (-1,1) for inset in (.024,.0355,.047,.050,.0615,.073)]))
        elif not is_bench:
            grids[0]=sorted(set(grids[0]+[-.05,-.024,0,.024,.05]))
        def shape(out):
            dx=out[0]-centre[0]
            if recline:
                # Broad upholstered shoulders turn into a rounded high-back
                # crown. The displacement acts on the volume, not its seams.
                t=max(0,min(1,(out[2]-.425)/.510))
                if not is_bench:
                    out[2]-=.065*(abs(dx)/(size[0]/2))**2*t**4
                    # Softer pinched hip, full shoulder, and a domed face.
                    # This changes shell cross-sections, not only edge bevels.
                    waist=.045*math.exp(-((out[2]-.57)/.075)**2)
                    out[0]=centre[0]+dx*(1-waist)
                ribbon_z=1.45-out[2] if is_bench else out[2]
                edge=min(size[0]/2-.025-abs(dx),ribbon_z-.54)
                corner_x=size[0]/2-.100
                if abs(dx)>corner_x and ribbon_z<.615:
                    edge=.075-math.hypot(abs(dx)-corner_x,ribbon_z-.615)
                cloth_relief=.0035*sum(math.exp(-((edge-inset)/.012)**2)
                                       for inset in (.0355,.0615))
                out[0]=centre[0]+(out[0]-centre[0])*back_scale(out[2])
                out[1]-=.08*(out[2]-.425)
                forward=max(0,min(1,(out[1]-centre[1]+.0575)/.115))
                across=math.exp(-(dx/(size[0]*.56))**4)
                lumbar=.038*math.exp(-((out[2]-.56)/.110)**2)
                shoulder=.022*math.exp(-((out[2]-.77)/.14)**2)
                if is_bench:
                    across=sum(math.exp(-((dx-x)/.24)**4) for x in (-.37,.37))
                # Compressed border stitch channels run beside the raised cloth.
                seam=-.001*sum(math.exp(-((edge-inset)/.006)**2)
                              for inset in (.023,.073))
                out[1]+=forward*(across*(lumbar+shoulder)+cloth_relief+seam)
            else:
                weight=max(0,min(1,(out[2]-.44)/.08))
                dy=out[1]-centre[1]
                out[0]=centre[0]+dx*(1-.07*((dy-.04)/.285)**2)
                # Occupant bowls, raised side pads and a rounded thigh roll.
                centres=(-.37,.37) if is_bench else (0,)
                depression=sum(math.exp(-((dx-x)/(.21 if is_bench else .155))**4)
                               for x in centres)
                bowl=-.019*depression*math.exp(-((dy+.055)/.155)**4)
                thigh=.014*math.exp(-((dy-.14)/.075)**2)
                cloth_relief=0 if is_bench else .003*sum(
                    math.exp(-((dx-x)/.018)**2) for x in (-.024,.024))
                # Lift the underside without moving the native occupant surface.
                # A thin upholstered pan replaces the former 160mm slab.
                underside=.058*(1-weight)
                front_fall=-.030*math.exp(-((dy-.224)/.065)**2)
                compressed=-.0045*math.exp(-((dy-.13)/.012)**2)
                if not is_bench:
                    compressed-=.003*sum(math.exp(-((dx-x)/.011)**2)
                                        for x in (-.155,.155))
                out[2]+=underside+weight*(bowl+thigh+cloth_relief+front_fall+compressed)
            return tuple(out)
        def point(axis,sign,u,v,others):
            p=[0,0,0]
            p[axis]=sign*halves[axis]
            p[others[0]],p[others[1]]=u,v
            core=[max(-h+radius,min(h-radius,value)) for value,h in zip(p,halves)]
            delta=[a-b for a,b in zip(p,core)]
            length=math.sqrt(sum(value*value for value in delta))
            out=[c+base+radius*d/length for c,base,d in zip(centre,core,delta)]
            return shape(out)
        tops=[];fronts=[]
        for axis in range(3):
            others=[i for i in range(3) if i!=axis]
            for sign in (-1,1):
                for a,b in zip(grids[others[0]],grids[others[0]][1:]):
                    for c,d in zip(grids[others[1]],grids[others[1]][1:]):
                        points=[point(axis,sign,u,v,others) for u,v in ((a,c),(b,c),(b,d),(a,d))]
                        for indices in ((0,1,2),(0,2,3)):
                            triangle=[points[i] for i in indices]
                            inside.face(triangle,'seat')
                            if axis==2 and sign==1:tops.append(triangle)
                            if axis==1 and sign==1:fronts.append(triangle)
        return tops,fronts,shape

    # Two front buckets and one continuous rear bench. The two native rear
    # passenger locations remain supported at X +/-0.37, Y -0.80.
    for seat_x,y,seat_width,is_bench in ((-.37,-.08,.50,False),
                                       (.37,-.08,.50,False),(0,-.80,1.24,True)):
        tops,_,_=padded_box((seat_x,y,.44),(seat_width,.49,.16),.035,is_bench=is_bench)
        _,fronts,back_shape=padded_box((seat_x,y-.23,.68),(seat_width,.115,.51),.025,True,is_bench)
        def back_patch(polygon,colour):
            # Clip in source X/Z, then interpolate the real padded triangles.
            # This preserves support after shoulders and lumbar form change.
            for triangle in fronts:
                projected=[(p[0],p[2],p[1]) for p in triangle]
                clipped=_triangle_clip(polygon,projected)
                if len(clipped)<3:continue
                a,b,c=projected
                determinant=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
                if abs(determinant)<1e-12:continue
                points=[]
                for x,z in clipped:
                    u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(z-c[1]))/determinant
                    v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(z-c[1]))/determinant
                    points.append((x,a[2]*u+b[2]*v+c[2]*(1-u-v)+.0015,z))
                inside.face(points,colour,normal=(0,1,0))
        def seat_u(inset):
            half=seat_width/2-.025-inset;bottom=.54+inset;r=max(.012,.075-inset)
            path=[(-half,.910),(-half,bottom+r)]
            path += [(-half+r+r*math.cos(math.pi+i*math.pi/12),
                      bottom+r+r*math.sin(math.pi+i*math.pi/12)) for i in range(1,7)]
            path += [(half-r,bottom)]
            path += [(half-r+r*math.cos(math.pi*1.5+i*math.pi/12),
                      bottom+r+r*math.sin(math.pi*1.5+i*math.pi/12)) for i in range(1,7)]
            path += [(half,.910)]
            # Rear backrest's continuous border crosses the upper edge
            # and drops down its sides; front buckets turn at the base.
            return [(x,1.45-z) for x,z in path] if is_bench else path
        inset=0
        for colour,width in (('wine',.010),('pink',.014),('cream',.023),
                              ('black',.003),('cream',.023),('pink',.014),('wine',.010)):
            outer,inner=seat_u(inset),seat_u(inset+width)
            for i in range(len(outer)-1):
                polygon=[]
                for xx,z in (outer[i],outer[i+1],inner[i+1],inner[i]):
                    p=back_shape([seat_x+xx,y-.1725,z])
                    polygon.append((p[0],p[2]))
                back_patch(polygon,colour)
            inset+=width
        def cushion_point(xx,yy,lift=.0015):
            x=seat_x+xx
            for triangle in tops:
                a,b,c=triangle
                determinant=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
                if abs(determinant)<1e-12:continue
                u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(yy-c[1]))/determinant
                v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(yy-c[1]))/determinant
                if min(u,v,1-u-v)>=-1e-8:
                    return (x,yy,a[2]*u+b[2]*v+c[2]*(1-u-v)+lift)
            raise ValueError('Seat detail leaves its padded support')
        def cushion_patch(polygon,colour):
            # The lumbar pad overlaps the rear of the cushion. End the
            # exposed cloth pattern ahead of that solid, rather than drawing
            # a supported but buried ribbon through the hip junction.
            exposed=[]
            boundary=y-.145
            for a,b in zip(polygon,polygon[1:]+polygon[:1]):
                a_in,b_in=a[1]>=boundary,b[1]>=boundary
                if a_in:exposed.append(a)
                if a_in!=b_in:
                    t=(boundary-a[1])/(b[1]-a[1])
                    exposed.append((a[0]+t*(b[0]-a[0]),boundary))
            if len(exposed)<3:return
            for triangle in tops:
                clipped=_triangle_clip(exposed,triangle)
                if len(clipped)>=3:
                    inside.face([cushion_point(x-seat_x,cy) for x,cy in clipped],
                                colour,normal=(0,0,1))
        colours=(('wine',.014),('pink',.020),('cream',.045),
                 ('black',.003),('cream',.045),('pink',.020),('wine',.014))
        if not is_bench:
            # Front cushion bands run fore/aft, as the gallery close-up
            # shows, rather than sideways across both thighs.
            xx=-sum(width for _,width in colours)/2
            for colour,width in colours:
                cushion_patch([(seat_x+xx,y-.225),(seat_x+xx+width,y-.225),
                               (seat_x+xx+width,y+.225),(seat_x+xx,y+.225)],colour)
                xx+=width
        else:
            # The rear cushion carries one continuous rounded Cardin loop.
            # Its centre stays dark, with no invented central bucket gap.
            def cushion_loop(inset):
                half=seat_width/2-.035-inset
                run=.215-inset
                radius=max(.014,.095-inset*.65)
                radius=min(radius,run-.003)
                path=[]
                for cx,cy,start in ((half-radius,run-radius,0),
                                    (-half+radius,run-radius,math.pi/2),
                                    (-half+radius,-run+radius,math.pi),
                                    (half-radius,-run+radius,math.pi*1.5)):
                    for i in range(9):
                        angle=start+i*math.pi/16
                        path.append((seat_x+cx+radius*math.cos(angle),
                                     y+cy+radius*math.sin(angle)))
                return path
            inset=0
            for colour,width in (('wine',.010),('pink',.014),('cream',.023),
                                 ('black',.003),('cream',.023),('pink',.014),('wine',.010)):
                outer,inner=cushion_loop(inset),cushion_loop(inset+width)
                for i in range(len(outer)):
                    j=(i+1)%len(outer)
                    cushion_patch([outer[i],outer[j],inner[j],inner[i]],colour)
                inset+=width
        # Thin dark welt on the rounded cushion edge, visible in Druk141.
        # It is seated on the same padded triangles, never a floating outline.
        half=seat_width/2-.035;run=.205;radius=.045
        welt=[]
        for cx,cy,start in ((half-radius,run-radius,0),
                            (-half+radius,run-radius,math.pi/2),
                            (-half+radius,-run+radius,math.pi),
                            (half-radius,-run+radius,math.pi*1.5)):
            for i in range(9):
                angle=start+i*math.pi/16
                welt.append((cx+radius*math.cos(angle),y+cy+radius*math.sin(angle)))
        # Omit the hidden rear segment at the lumbar overlap.
        for a,b in zip(welt,welt[1:]+welt[:1]):
            if min(a[1],b[1])<y-.145:continue
            inside.beam(cushion_point(*a,.001),cushion_point(*b,.001),.0012,'black',6)
        # Broad cloth panel divisions, not a regular five-line grid.
        divisions=(-.155,.155) if not is_bench else (-.37,0,.37)
        for xx in divisions:
            for i in range(12):
                inside.beam(cushion_point(xx,y-.22+i*.44/12,.002),
                            cushion_point(xx,y-.22+(i+1)*.44/12,.002),.00065,'black',4)
