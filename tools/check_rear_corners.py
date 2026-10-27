def check_rear_corner_closure(atlas):
    """Reject sightlines through the fixed lamp-to-lower-panel corner wedges.

    Reads saved Body geometry and semantic UVs without changing the scene.
    """
    import bpy
    from mathutils import Vector
    obj=bpy.data.objects['J73Mesh_Body']
    samples=0
    failures=[]
    for side in (-1,1):
        for i in range(51):
            x=side*(.795+i*.001)
            for j in range(41):
                z=.545+j*.0025
                hit,point,normal,index=obj.ray_cast(Vector((x,-3,z-.65)),Vector((0,1,0)))
                valid=False
                colour=None
                if hit:
                    face=obj.data.polygons[index]
                    uv=obj.data.uv_layers.active.data[face.loop_start].uv
                    slot=int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
                    colour=atlas['colours'][slot%len(atlas['colours'])]
                    valid=point.y<-2.25 and normal.y<-.95 and colour=='red'
                if not valid:
                    failures.append((x,z,tuple(point) if hit else None,colour))
                samples+=1
    assert not failures, f'Rear corner closure: {len(failures)}/{samples} missing rear-facing red surfaces; first {failures[:3]}'
    print(f'PASS fixed rear corners: {samples} rays hit outward red rear sheet, no remote/internal surface leaks')
