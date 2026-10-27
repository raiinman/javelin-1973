"""Read-only saved Body surface ownership and rear join regression."""


def check_rear_haunch_joins(atlas):
    import bpy
    from collections import defaultdict
    from mathutils import Vector
    obj=bpy.data.objects['J73Mesh_Body'];mesh=obj.data
    def colour(index):
        face=mesh.polygons[index];uv=mesh.uv_layers.active.data[face.loop_start].uv
        slot=int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
        return atlas['colours'][slot%len(atlas['colours'])]
    failures=[];rays=0
    # Fixed probes from the diagnosed old overlap, independent of build helpers.
    for side in (-1,1):
        for y,low,inner in ((-1.73,.93243087,.96306667),(-1.75,.92909405,.9592),
                            (-1.80,.91860727,.94953333),(-1.85,.905027,.93986667)):
            for t in (.3,.5,.7):
                pos=Vector((side*1.1,y,low*(1-t)+inner*t-.65))
                direction=Vector((-side,0,0));hits=[]
                for i in range(8):
                    hit,point,normal,index=obj.ray_cast(pos,direction)
                    if not hit or point.x*side<.8:break
                    if colour(index)=='red' and normal.x*side>0:hits.append(index)
                    pos=point+direction*.000001
                if len(hits)!=1:failures.append(('outward red sheets',side,y,t,len(hits)))
                rays+=1
    adjacent=defaultdict(list)
    for face in mesh.polygons:
        for edge in face.edge_keys:adjacent[tuple(sorted(edge))].append(face.index)
    facing=mesh.attributes['J73SheetFacing']
    sharp=mesh.attributes.get('sharp_edge')
    indices={tuple(sorted(e.vertices)):e.index for e in mesh.edges}
    counts={side:{'outer':0,'apron':0,'front':0,'rear':0} for side in (-1,1)}
    for edge,faces in adjacent.items():
        points=[mesh.vertices[i].co for i in edge]
        red=[i for i in faces if colour(i)=='red']
        for side in (-1,1):
            if not all(q.x*side>.8 for q in points):continue
            tags=[facing.data[i].vector for i in red]
            side_faces=[i for i,v in zip(red,tags) if v.x*side>.9 and abs(v.z)<.1]
            upper_faces=[i for i,v in zip(red,tags) if v.x*side>.9 and v.z>.9]
            if all(-1.871<q.y<-1.719 and .24<q.z<.29 for q in points) and side_faces and upper_faces:
                counts[side]['outer']+=1
                if len(red)!=2 or (sharp and sharp.data[indices[edge]].value):
                    failures.append(('outer seam has extra paint/sharp split',side,edge,len(red)))
            apron_faces=[i for i,v in zip(red,tags) if abs(v.x)<.1 and v.z>.9]
            if all(-1.871<q.y<-1.719 and .837<q.x*side<.851 and .289<q.z<.316 for q in points):
                if upper_faces and apron_faces:
                    counts[side]['apron']+=1
                    if len(red)!=2:failures.append(('apron seam paint adjacency',side,edge,len(red)))
            for label,y in (('front',-1.87),('rear',-2.18092)):
                if all(abs(q.y-y)<.000002 and q.z>.13 for q in points):
                    forward=[i for i in red if mesh.polygons[i].center.y>y+.000001]
                    aft=[i for i in red if mesh.polygons[i].center.y<y-.000001]
                    if forward and aft:
                        counts[side][label]+=1
                        if len(red)!=2:failures.append((label+' seam paint adjacency',side,edge,len(red)))
    for side,data in counts.items():
        for name,minimum in (('outer',12),('apron',12),('front',27),('rear',25)):
            if data[name]<minimum:failures.append(('missing shared seam',side,name,data[name],minimum))
    assert not failures,f'Rear haunch joins: {len(failures)} failures, first {failures[:5]}; shared edges {counts}'
    print(f'PASS rear haunch joins: {rays} actual single-sheet rays, shared painted edges {counts}')
    return {'rays':rays,'shared_edges':counts}
