"""Read-only saved-mesh checks for the original Cardin door appliques."""


def check_door_crests(atlas):
    import bpy
    from collections import Counter
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    from mathutils.kdtree import KDTree

    signatures=[]
    for side,suffix in ((-1,'Left'),(1,'Right')):
        mesh=bpy.data.objects['J73Mesh_Door'+suffix].data
        mesh.calc_loop_triangles()
        def colour(face):
            uv=mesh.uv_layers.active.data[face.loop_start].uv
            slot=int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
            return atlas['colours'][slot%len(atlas['colours'])]
        # Broad depth selection includes buried/raised artwork so support rays,
        # rather than the expected applique plane alone, decide physical seating.
        artwork={face.index for face in mesh.polygons
                 if colour(face) in {'chrome','silverLight','black'}
                 and all(.775<abs(mesh.vertices[i].co.x)<.7901
                         and .087<mesh.vertices[i].co.y<.123
                         and .059<mesh.vertices[i].co.z<.109 for i in face.vertices)}
        triangles=[t for t in mesh.loop_triangles if t.polygon_index in artwork]
        assert len(artwork)==376 and len(triangles)==1516, \
            f'{suffix} crest incomplete: {len(artwork)} faces, {len(triangles)} triangles'
        normal=Vector((-side,0,0))
        assert all(mesh.polygons[i].normal.dot(normal)>.999 for i in artwork), \
            f'{suffix} crest faces away from cabin'
        support=[tuple(t.vertices) for t in mesh.loop_triangles
                 if colour(mesh.polygons[t.polygon_index])=='seat']
        assert support, f'{suffix} crest inlay support missing'
        tree=BVHTree.FromPolygons([v.co for v in mesh.vertices],support,all_triangles=True)
        gaps=[]
        for triangle in triangles:
            points=[mesh.vertices[i].co for i in triangle.vertices]
            centre=sum(points,Vector())/3
            for sample in [centre]+[p*.8+centre*.2 for p in points]:
                hit,facing,index,gap=tree.ray_cast(sample,-normal,.02)
                assert hit is not None and facing.dot(normal)>.999, \
                    f'{suffix} crest lacks cabin-facing upholstered support'
                assert .00025<gap<.0025, f'{suffix} crest buried or floating: {gap:.7f}m'
                gaps.append(gap)
        signatures.append((Counter((colour(mesh.polygons[i]),len(mesh.polygons[i].vertices))
                                   for i in artwork),
            {name:[(abs(mesh.vertices[j].co.x),side*(.105-mesh.vertices[j].co.y),mesh.vertices[j].co.z)
                   for i in artwork if colour(mesh.polygons[i])==name
                   for j in mesh.polygons[i].vertices] for name in ('chrome','silverLight','black')}))
        print(f'PASS {suffix} Cardin crest: {len(artwork)} faces, {len(gaps)} support rays, '
              f'{min(gaps)*1000:.3f}..{max(gaps)*1000:.3f}mm')
    assert signatures[0][0]==signatures[1][0], 'Door crest semantic/topology counts differ'
    for name in ('chrome','silverLight','black'):
        for source,target in ((0,1),(1,0)):
            points=signatures[target][1][name]
            assert points, f'Door crest {name} artwork missing'
            tree=KDTree(len(points))
            for i,point in enumerate(points):tree.insert(point,i)
            tree.balance()
            assert all(tree.find(point)[2]<.000002 for point in signatures[source][1][name]), \
                f'Door crest {name} artwork differs between cabin-readable sides'
