"""Independent saved-source visor/mirror guard, no generator import."""
import bpy,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def check_saved_roof_hardware(atlas):
    obj=bpy.data.objects['J73Mesh_Interior'];mesh=obj.data
    uv=mesh.uv_layers.active.data
    def colour(p):
        q=uv[p.loop_start].uv
        slot=int(q.x*atlas['columns'])+int(q.y*atlas['rows'])*atlas['columns']
        return atlas['colours'][slot%len(atlas['colours'])]
    roof_ids=[p for p in mesh.polygons if colour(p)=='seat' and p.normal.z<-.8
              and all(mesh.vertices[i].co.z>.45 for i in p.vertices)]
    assert roof_ids,'Actual Cardin roof base missing'
    roof=BVHTree.FromPolygons([v.co for v in mesh.vertices],[tuple(p.vertices) for p in roof_ids])
    records=[]
    for side in (-1,1):
        thickness=[]
        for dx,dy in ((0,0),(-.10,0),(.10,0),(0,-.04),(0,.04)):
            x,y=side*.365+dx,.145+dy
            ok,p,n,index=obj.ray_cast((x,y,.45),(0,0,1),distance=.22)
            assert ok and .55<p.z<.65 and n.z<-.94, 'Stowed padded visor missing or reversed'
            assert colour(mesh.polygons[index])=='black','Visor should use neutral dark padding'
            ok2,p2,n2,_=obj.ray_cast(p+Vector((0,0,.00005)),(0,0,1),distance=.025)
            assert ok2 and n2.z>.94 and .012<p2.z-p.z<.021,'Visor lacks positive padded thickness'
            q,_,_,gap=roof.ray_cast(p2+Vector((0,0,.00005)),Vector((0,0,1)),.04)
            assert q is not None and .006<gap<.023,'Stowed visor intersects or floats far from ceiling'
            thickness.append(dict(point=list(p),normal=list(n),thickness=p2.z-p.z,roof_gap=gap))
        # Small mounting plates at both ends must seat near actual roof fabric.
        mounts=[];pivots=[]
        slope_x=(thickness[2]['point'][2]-thickness[1]['point'][2])/.20
        slope_y=(thickness[4]['point'][2]-thickness[3]['point'][2])/.08
        for xx in (side*.560,side*.205):
            x,y=xx+side*.010,.241
            q,_,_,_=roof.ray_cast(Vector((x,y,.50)),Vector((0,0,1)),.20)
            assert q is not None
            ok,p,n,_=obj.ray_cast((x,y,q.z-.030),(0,0,1),distance=.035)
            assert ok and n.z<-.94 and .006<q.z-p.z<.009,'Visor upper support plate missing'
            mounts.append(list(p))
            foot_z=thickness[0]['point'][2]+.008+slope_x*(xx-side*.365)+slope_y*(.210-.145)
            mid_z=(q.z-.0075+foot_z)/2
            ok,pivot,n,_=obj.ray_cast((xx-.04,.2225,mid_z),(1,0,0),distance=.08)
            assert ok and abs(pivot.x-xx)<.005 and n.x<-.9,'Physical visor pivot/support span missing'
            pivots.append(list(pivot))
        records.append(dict(side=side,visor_samples=thickness,mounts=mounts,pivots=pivots))
    ok,p,n,index=obj.ray_cast((0,.05,1.174-.65),(0,1,0),distance=.20)
    target=Vector((-math.sin(.10),-math.cos(.10),0))
    assert ok and .190<p.y<.205 and n.dot(target)>.995,'Interior mirror reflective face missing or reversed'
    assert colour(mesh.polygons[index])=='chromeDark','Mirror face semantic colour missing'
    mirror_hit=dict(point=list(p),normal=list(n))
    q,_,_,_=roof.ray_cast(Vector((0,.235,.50)),Vector((0,0,1)),.20)
    assert q is not None
    stem_y=(.235+.218)/2;stem_z=(q.z-.0075+1.207-.65)/2
    ok,p,n,_=obj.ray_cast((-.05,stem_y,stem_z),(1,0,0),distance=.10)
    assert ok and abs(p.x)<.006 and n.x<-.90,'Short physical mirror stalk missing'
    return dict(visors=records,mirror=mirror_hit,stalk=list(p))
