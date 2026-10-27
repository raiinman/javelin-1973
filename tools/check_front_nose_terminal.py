"""Saved-mesh terminal-wing shape, visible support and shared-row diagnostic.

Bounds are trial acceptance criteria inferred from photos, not factory dimensions.
No file is opened or written by the callable.
"""
def check_front_nose_terminal(atlas, *, raise_on_error=True):
 import bpy, math
 from mathutils import Vector
 from collections import defaultdict
 obj=bpy.data.objects['J73Mesh_Body'];mesh=obj.data
 def semantic(index):
  face=mesh.polygons[index];uv=mesh.uv_layers.active.data[face.loop_start].uv
  slot=int(uv.x*atlas['columns'])+int(uv.y*atlas['rows'])*atlas['columns']
  return atlas['colours'][slot%len(atlas['colours'])]
 failures=[];probes=[]
 # These rays test the outermost actual saved surface, including fascia caps.
 for side in (-1,1):
  for y in (2.24,2.29,2.34,2.365,2.385,2.388):
   for x in (.74,.76,.78,.80,.82):
    # The known bowed front perimeter ends beforeY2.388 nearX.82.
    if y>=2.447-.046*(x/.84)**2-.016-.00005:continue
    origin=Vector((side*x,y,.60));hits=[]
    for _ in range(20):
     hit,point,normal,index=obj.ray_cast(origin,Vector((0,0,-1)))
     if not hit or point.z<.09:break
     hits.append((point.z,semantic(index),normal.z,index))
     origin=point-Vector((0,0,.000001))
    red=next((h for h in hits if h[1]=='red' and h[2]>.05),None)
    if red is None:
     failures.append(('missing outward red support',side,x,y));continue
    top=hits[0];gap=top[0]-red[0]
    probes.append({'side':side,'x':x,'y':y,'support_z':red[0]+.65,
                   'top_semantic':top[1],'top_gap_mm':gap*1000,'normal_z':red[2]})
    if top[1] not in ('red','black','cream') or gap>.00085:
     failures.append(('support occluded above decal allowance',side,x,y,gap*1000))
    if x==.8:
     band={2.24:(.813,.825),2.29:(.798,.810),2.34:(.784,.796),
           2.365:(.7755,.787),2.385:(.7681,.780),2.388:(.766,.779)}[y]
     if not band[0]<red[0]+.65<band[1]:failures.append(('terminal descent outside inferred band',side,y,red[0]+.65,band))
 mirrored={(p['x'],p['y']):p for p in probes if p['side']==-1}
 for p in probes:
  if p['side']!=1:continue
  other=mirrored.get((p['x'],p['y']))
  if other is None or abs(other['support_z']-p['support_z'])>.000002:
   failures.append(('asymmetric saved terminal support',p['x'],p['y']))
 adjacency=defaultdict(list)
 for face in mesh.polygons:
  if semantic(face.index)=='red' and face.normal.z>.5:
   for edge in face.edge_keys:adjacency[tuple(sorted(edge))].append(face.index)
 shared={side:0 for side in (-1,1)};max_turn=0
 for edge,faces in adjacency.items():
  points=[mesh.vertices[i].co for i in edge]
  for side in (-1,1):
   if all(.72<q.x*side<.83 and abs(q.y-2.34)<.000001 for q in points):
    if len(faces)!=2:failures.append(('hood-end shared row not two-sided',side,edge,len(faces)))
    else:
     shared[side]+=1;a,b=(mesh.polygons[i].normal for i in faces)
     angle=math.degrees(a.angle(b));max_turn=max(max_turn,angle)
     if angle>35:failures.append(('local support fold',side,angle))
 for side,count in shared.items():
  if count<10:failures.append(('missing shared hood-end row',side,count))
 front_shared={side:0 for side in (-1,1)};front_turn=0
 all_adj=defaultdict(list)
 for face in mesh.polygons:
  for edge in face.edge_keys:all_adj[tuple(sorted(edge))].append(face.index)
 for edge,faces in all_adj.items():
  points=[mesh.vertices[i].co for i in edge]
  for side in (-1,1):
   if not all(.72<q.x*side<.83 and 2.38<q.y<2.40 and .70<q.z+.65<.80 for q in points):continue
   red=[i for i in faces if semantic(i)=='red' and mesh.polygons[i].normal.y>.4]
   field=[i for i in faces if semantic(i)=='shadow' and mesh.polygons[i].normal.y>.8]
   if red and field:
    front_shared[side]+=1
    if len(faces)!=2:failures.append(('front perimeter excess face ownership',side,len(faces)))
    angle=math.degrees(mesh.polygons[red[0]].normal.angle(mesh.polygons[field[0]].normal));front_turn=max(front_turn,angle)
    if angle>25:failures.append(('front roll terminal tangent fold',side,angle))
 for side,count in front_shared.items():
  if count<20:failures.append(('missing welded red/fascia perimeter',side,count))
 decal_samples=0;decal_gaps=[]
 tags=mesh.attributes['J73SheetFacing']
 for face in mesh.polygons:
  if (semantic(face.index)!='black' or tags.data[face.index].vector.z<=.1
      or abs(face.center.x)<=.70 or face.center.y<=.79 or face.center.z+.65<=.72):continue
  points=[face.center.copy()]+[mesh.vertices[v].co*.98+face.center*.02 for v in face.vertices]
  for point in points:
   origin=Vector((point.x,point.y,.60));red=None;first=None
   for _ in range(12):
    hit,q,n,index=obj.ray_cast(origin,Vector((0,0,-1)))
    if not hit or q.z<point.z-.005:break
    if first is None:first=q.z
    if semantic(index)=='red' and n.z>.01:
     red=q.z;break
    origin=q-Vector((0,0,.000001))
   decal_samples+=1
   if red is None:
    failures.append(('decal has no actual red support',face.index));continue
   gap=point.z-red;decal_gaps.append(gap)
   if not .00075<gap<.00085:failures.append(('decal actual support clearance',face.index,gap*1000))
   if first>point.z+.00005:failures.append(('decal occluded by another Body surface',face.index,(first-point.z)*1000))
 result={'rays':len(probes),'decal_samples':decal_samples,'decal_gap_mm':(min(decal_gaps)*1000,max(decal_gaps)*1000),'front_shared_edges':front_shared,'front_maximum_face_turn_degrees':front_turn,'probes':probes,'shared_hood_end_edges':shared,'maximum_row_face_turn_degrees':max_turn,'failures':failures}
 if raise_on_error:
  assert not failures,failures
  print('PASS terminal wing actual first-hit visibility',len(probes),'rays; welded front edges',front_shared,'maximum face turn',round(front_turn,3))
 return result
