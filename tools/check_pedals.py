"""Saved-mesh guard proposal, call from the source pose/placement gate."""
import bpy,math
from mathutils import Vector
# Independent expected locations: do not import the builder into a regression.
PEDALS=(('parking',-.665,.645,.440,.049,.054,16),
        ('clutch',-.490,.610,.438,.078,.064,18),
        ('brake',-.355,.620,.438,.082,.063,18),
        ('accelerator',-.230,.650,.414,.043,.139,12))


def check_saved_pedals():
    """Promotion guard: front-facing physical pads, distinct locations and arms."""
    obj=bpy.data.objects['J73Mesh_Interior']
    results=[]
    for name,x,y,z,w,h,angle in PEDALS:
        t=math.radians(angle);c,s=math.cos(t),math.sin(t)
        target=Vector((0,-c,s));hits=[]
        for u,v in ((0,0),(-w*.25,h*.23),(w*.25,-h*.23)):
            zz=z+c*v-.65
            ok,p,n,index=obj.ray_cast((x+u,y-.12+s*v,zz),(0,1,0),distance=.15)
            assert ok and y-.032<p.y<y-.003, f'{name}: no recessed pad at expected location'
            assert n.dot(target)>.985, f'{name}: foot face points away from driver'
            # Closed rubber tread/face has actual positive thickness behind it.
            cursor=p.copy();backing=None
            for _ in range(8):
                ok2,p2,n2,_=obj.ray_cast(cursor+Vector((0,.00005,0)),(0,1,0),distance=.025)
                if not ok2:break
                if n2.y>.90 and .001<p2.y-p.y<.020:
                    backing=p2.y-p.y;break
                cursor=p2
            assert backing is not None, f'{name}: pad lacks physical backing'
            hits.append(dict(point=list(p),normal=list(n),thickness_y=backing))
        # Probe two arm spans below the old dash. These rays miss the frozen
        # cabin entirely, so existing ledge vertices cannot satisfy support.
        pivot_x=x+(.025 if name=='clutch' else 0)
        end_z=z-s*.011
        spans=[(pivot_x,(.510+y+.015)/2,(.608+.572)/2),
               (x,(y+.045+y+c*.011)/2,
                ((.486 if name=='accelerator' else .505)+end_z)/2)]
        arm_hits=[]
        for xx,yy,zz in spans:
            hit,q,n,index=obj.ray_cast((xx-.055,yy,zz-.65),(1,0,0),distance=.11)
            assert hit and abs(q.x-xx)<.009 and n.x<-.95, f'{name}: suspended arm span missing'
            arm_hits.append(dict(point=list(q),normal=list(n)))
        hit,mount,n,_=obj.ray_cast((pivot_x+.015,.495,.590-.65),(0,0,1),distance=.03)
        assert hit and abs(mount.z+.65-.611)<.001 and n.z<-.99, f'{name}: upper mounting plate missing'
        results.append(dict(name=name,pad_hits=hits,arm_hits=arm_hits,mount=list(mount)))
    return results
