"""Seat fixed-fender graphic shading on its actual painted support normals."""

def transfer_fender_graphic_normals(mesh, colours, columns, rows):
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    mesh.calc_loop_triangles()
    automatic=[n.vector.copy() for n in mesh.corner_normals]
    def colour(face):
        uv=mesh.uv_layers.active.data[face.loop_start].uv
        return colours[(int(uv.x*columns)+int(uv.y*rows)*columns)%len(colours)]
    support=[tri for tri in mesh.loop_triangles if colour(mesh.polygons[tri.polygon_index])=='red']
    tree=BVHTree.FromPolygons([v.co for v in mesh.vertices],[tri.vertices for tri in support],all_triangles=True)
    facing=mesh.attributes['J73SheetFacing']
    graphic=[face for face in mesh.polygons if colour(face)=='black' and
             facing.data[face.index].vector.z>.001 and
             all(.79<=mesh.vertices[i].co.y<=2.376 and abs(mesh.vertices[i].co.x)>=.7058 for i in face.vertices)]
    normals=[(0.,0.,0.)]*len(mesh.loops);cache={};samples=0;edge_fallbacks=0
    for face in graphic:
        for loop in face.loop_indices:
            vertex=mesh.loops[loop].vertex_index
            if vertex not in cache:
                point=mesh.vertices[vertex].co
                hit,normal,index,distance=tree.ray_cast(point+Vector((0,0,.003)),Vector((0,0,-1)),.01)
                if hit is None:
                    # Exact welded boundary vertices can lie one float32 ULP
                    # beyond a ray edge. Retain only an actual red support
                    # within the existing0.8mm vertical seating envelope.
                    hit,normal,index,distance=tree.find_nearest(point,.00081)
                    edge_fallbacks+=1
                if hit is None:raise ValueError('Fender graphic corner lacks nearby painted support')
                tri=support[index];a,b,c=[mesh.vertices[i].co for i in tri.vertices]
                # Double scalar arithmetic avoids extra float32 cancellation on steep sheets.
                ab=tuple(float(b[k])-a[k] for k in range(3));ac=tuple(float(c[k])-a[k] for k in range(3));ap=tuple(float(hit[k])-a[k] for k in range(3))
                dot=lambda u,v:sum(x*y for x,y in zip(u,v))
                aa,bb,cc,dd,ee=dot(ab,ab),dot(ab,ac),dot(ac,ac),dot(ap,ab),dot(ap,ac)
                determinant=aa*cc-bb*bb
                if determinant<=1e-20:raise ValueError('Degenerate fender normal support')
                u=(cc*dd-bb*ee)/determinant;v=(aa*ee-bb*dd)/determinant
                weights=(1-u-v,u,v)
                value=sum((automatic[i]*w for i,w in zip(tri.loops,weights)),Vector()).normalized()
                if value.dot(normal)<0:raise ValueError('Inward fender graphic shading normal')
                cache[vertex]=tuple(value);samples+=1
            normals[loop]=cache[vertex]
    # Installed Blender documents zero vectors as preserving automatic normals.
    mesh.normals_split_custom_set(normals)
    mesh.update()
    print('J73_FENDER_SUPPORT_NORMALS',len(graphic),'faces',samples,'vertices',edge_fallbacks,'bounded edge normal lookups')


def transfer_hood_graphic_normals(mesh, colours, columns, rows):
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    mesh.calc_loop_triangles()
    automatic=[n.vector.copy() for n in mesh.corner_normals]
    def colour(face):
        uv=mesh.uv_layers.active.data[face.loop_start].uv
        return colours[(int(uv.x*columns)+int(uv.y*rows)*columns)%len(colours)]
    support=[tri for tri in mesh.loop_triangles if colour(mesh.polygons[tri.polygon_index])=='red' and mesh.polygons[tri.polygon_index].normal.z>.05]
    tree=BVHTree.FromPolygons([v.co for v in mesh.vertices],[tri.vertices for tri in support],all_triangles=True)
    facing=mesh.attributes['J73SheetFacing']
    graphic=[face for face in mesh.polygons if colour(face)=='black' and
             facing.data[face.index].vector.z>.001 and
             all(.80<=mesh.vertices[i].co.y<=2.34001 for i in face.vertices)]
    normals=[tuple(n) for n in automatic];cache={};samples=0;edge_fallbacks=0
    for face in graphic:
        for loop in face.loop_indices:
            vertex=mesh.loops[loop].vertex_index
            if vertex not in cache:
                point=mesh.vertices[vertex].co
                hit,normal,index,distance=tree.ray_cast(point+Vector((0,0,.003)),Vector((0,0,-1)),.01)
                if hit is None:
                    # Exact welded boundary vertices can lie one float32 ULP
                    # beyond a ray edge. Retain only an actual red support
                    # within the existing0.8mm vertical seating envelope.
                    hit,normal,index,distance=tree.find_nearest(point,.00081)
                    edge_fallbacks+=1
                if hit is None:raise ValueError('Hood graphic corner lacks nearby painted support')
                tri=support[index];a,b,c=[mesh.vertices[i].co for i in tri.vertices]
                # Double scalar arithmetic avoids extra float32 cancellation on steep sheets.
                ab=tuple(float(b[k])-a[k] for k in range(3));ac=tuple(float(c[k])-a[k] for k in range(3));ap=tuple(float(hit[k])-a[k] for k in range(3))
                dot=lambda u,v:sum(x*y for x,y in zip(u,v))
                aa,bb,cc,dd,ee=dot(ab,ab),dot(ab,ac),dot(ac,ac),dot(ap,ab),dot(ap,ac)
                determinant=aa*cc-bb*bb
                if determinant<=1e-20:raise ValueError('Degenerate hood normal support')
                u=(cc*dd-bb*ee)/determinant;v=(aa*ee-bb*dd)/determinant
                weights=(1-u-v,u,v)
                value=sum((automatic[i]*w for i,w in zip(tri.loops,weights)),Vector()).normalized()
                if value.dot(normal)<0:raise ValueError('Inward fender graphic shading normal')
                cache[vertex]=tuple(value);samples+=1
            normals[loop]=cache[vertex]
    # Preserve explicit original normals on unselected paint, chrome and vents.
    mesh.normals_split_custom_set(normals)
    mesh.update()
    print('J73_HOOD_SUPPORT_NORMALS',len(graphic),'faces',samples,'vertices',edge_fallbacks,'bounded edge normal lookups')
