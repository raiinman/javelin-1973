"""Original Javelin geometry and palette. Run with Blender --background --python.

All coordinates and shapes are authored here from the reference video.
No mesh, UV layout, texture or rig is imported from another mod.
"""
import bpy
import json
import math
import sys
from pathlib import Path
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from surface_maps import build_atlases
from clean_fbx import clean_fbx
from javelin_front import build_front, build_valance, valance_point
from javelin_fender_artist import artist_point
from javelin_nose import terminal_wing_point, terminal_side_point, terminal_front_contract, terminal_cell_triangles
from javelin_decals import build_decals
from javelin_wheel import build_wheel
from javelin_rear import build_rear, build_rear_bumper, build_spoiler, build_trunk_lid, spoiler_rear_point
from javelin_plate import build_plate
from javelin_seats import build_seats
from javelin_cockpit import build_cockpit, build_steering, build_dashboard
from javelin_pedals import build_pedals
from javelin_roof_hardware import build_roof_hardware
from javelin_engine import build_engine
from javelin_sidepipes import build_sidepipe
from javelin_mirrors import build_mirror
from javelin_trim import build_handle, build_wipers
from javelin_doorcard import build_doorcard
MEDIA = ROOT / 'Javelin73PC/common/media'
ART = ROOT / 'assets'
for directory in ('models_X/vehicles', 'anims_X/vehicles', 'textures/Vehicles', 'scripts'):
    (MEDIA / directory).mkdir(parents=True, exist_ok=True)
ART.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 31

# A code-native swatch atlas provides exact, stable UVs and original colours.
PALETTE = {
    'red': '#ba2928', 'redLight': '#cf3430', 'redDark': '#8a201e',
    'black': '#141719', 'rubber': '#222426', 'chrome': '#b7bdc3',
    'chromeDark': '#687581', 'glass': '#34444a', 'headlamp': '#8b938b',
    'tail': '#a71b22', 'amber': '#e48c26', 'cream': '#d7c8a8',
    'pink': '#b94868', 'wine': '#773444', 'seat': '#343039',
    'white': '#e4e2d9', 'engine': '#435b66', 'grille': '#484e4f',
    'steel': '#73797d', 'shadow': '#0a0c0e', 'blue': '#315c9a',
    'plate': '#253b64', 'silverLight': '#e1e2df', 'wood': '#6e4832',
    'brakeRed': '#af1c24',
}
def rgba(hex_colour):
    def linear(v):
        v = v / 255
        return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4
    return tuple(linear(int(hex_colour[i:i+2], 16)) for i in (1, 3, 5)) + (1.0,)

names = list(PALETTE)
atlas = build_atlases(MEDIA,PALETTE)
(ART/'atlas-manifest.json').write_text(json.dumps(atlas.manifest,indent=2))
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">']
for i, name in enumerate(names):
    svg.append(f'<rect x="{(i % 8)*32}" y="{224-(i//8)*32}" width="32" height="32" fill="{PALETTE[name]}"/>')
svg.append('</svg>')
(ART / 'palette.svg').write_text('\n'.join(svg))
atlas_image = bpy.data.images.load(str(MEDIA/'textures/Vehicles/J73_Palette.png'))
atlas_image.pack()
atlas_image.filepath = '//../Javelin73PC/common/media/textures/Vehicles/J73_Palette.png'
atlas_material = bpy.data.materials.new('J73_PaletteAtlas')
atlas_material.use_nodes = True
atlas_bsdf = atlas_material.node_tree.nodes.get('Principled BSDF')
atlas_bsdf.inputs['Metallic'].default_value = .05
atlas_bsdf.inputs['Roughness'].default_value = .32
atlas_texture = atlas_material.node_tree.nodes.new('ShaderNodeTexImage')
atlas_texture.image = atlas_image
atlas_texture.interpolation = 'Closest'
atlas_material.node_tree.links.new(atlas_texture.outputs['Color'], atlas_bsdf.inputs['Base Color'])

class Part:
    def __init__(self, name):
        self.name, self.vertices, self.faces, self.colours = name, [], [], []
        self.sheet_normals=[]
        self.face_uvs=[]
    def face(self, points, colour, normal=None,uvs=None):
        start = len(self.vertices)
        self.vertices.extend(points)
        self.faces.append(tuple(range(start, start + len(points))))
        self.colours.append(colour)
        self.sheet_normals.append(normal)
        self.face_uvs.append(uvs)
    def sheet(self, points, colour, thickness=.012):
        """Closed sheet metal keeps fixed decks visible with native backface culling."""
        under=[(x,y,z-thickness) for x,y,z in points]
        self.face(points,colour)
        self.face(list(reversed(under)),colour)
        for index in range(len(points)):
            following=(index+1)%len(points)
            self.face([points[index],under[index],under[following],points[following]],colour)
    def box(self, center, size, colour):
        x,y,z = center
        a,b,c = (v/2 for v in size)
        p = [(x-a,y-b,z-c),(x+a,y-b,z-c),(x+a,y+b,z-c),(x-a,y+b,z-c),
             (x-a,y-b,z+c),(x+a,y-b,z+c),(x+a,y+b,z+c),(x-a,y+b,z+c)]
        for inds in ((0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)):
            self.face([p[i] for i in inds],colour)
    def cylinder(self, center, radius, length, colour, axis='X', segments=20, radius2=None):
        radius2 = radius if radius2 is None else radius2
        rings = []
        for sign, r in ((-1,radius),(1,radius2)):
            ring = []
            for i in range(segments):
                t = math.tau * i / segments
                v = [r*math.cos(t),r*math.sin(t),sign*length/2]
                if axis=='X': v=[v[2],v[0],v[1]]
                elif axis=='Y': v=[v[0],v[2],v[1]]
                ring.append(tuple(center[j]+v[j] for j in range(3)))
            rings.append(ring)
        self.face(list(reversed(rings[0])),colour)
        self.face(rings[1],colour)
        for i in range(segments):
            n=(i+1)%segments
            self.face([rings[0][i],rings[0][n],rings[1][n],rings[1][i]],colour)
    def beam(self, a, b, radius, colour, segments=8):
        va,vb=Vector(a),Vector(b)
        normal=(vb-va).normalized()
        u=normal.cross(Vector((0,0,1)))
        if u.length < .01: u=normal.cross(Vector((0,1,0)))
        u.normalize()
        v=normal.cross(u)
        rings=[[tuple(p+radius*(u*math.cos(i*math.tau/segments)+v*math.sin(i*math.tau/segments))) for i in range(segments)] for p in (va,vb)]
        for i in range(segments):
            n=(i+1)%segments
            self.face([rings[0][i],rings[0][n],rings[1][n],rings[1][i]],colour)
    def rounded_plate(self, center, size, radius, colour, segments=5):
        """A rounded rectangle prism facing front/rear along the Y axis."""
        x,y,z=center
        w,d,h=size
        r=min(radius,w/2,h/2)
        perimeter=[]
        for cx,cz,start in ((w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)):
            for step in range(segments+1):
                theta=math.radians(start+step*90/segments)
                perimeter.append((x+cx+r*math.cos(theta),z+cz+r*math.sin(theta)))
        rings=[[(xx,y+sign*d/2,zz) for xx,zz in perimeter] for sign in (-1,1)]
        self.face(list(reversed(rings[0])),colour)
        self.face(rings[1],colour)
        for i in range(len(perimeter)):
            j=(i+1)%len(perimeter)
            self.face([rings[0][i],rings[0][j],rings[1][j],rings[1][i]],colour)
    def ellipsoid(self, center, radii, colour, segments=16, rings=8):
        for j in range(rings):
            a,b=-math.pi/2+j*math.pi/rings,-math.pi/2+(j+1)*math.pi/rings
            for i in range(segments):
                c,d=i*math.tau/segments,(i+1)*math.tau/segments
                def p(t,u):
                    return (center[0]+radii[0]*math.cos(t)*math.cos(u),center[1]+radii[1]*math.cos(t)*math.sin(u),center[2]+radii[2]*math.sin(t))
                self.face([p(a,c),p(a,d),p(b,d),p(b,c)],colour)
    def object(self):
        mesh=bpy.data.meshes.new('J73Mesh_'+self.name)
        # Author around the chassis origin; native suspension settles world height.
        mesh.from_pydata([(x,y,z-.65) for x,y,z in self.vertices],[],self.faces)
        mesh.update()
        # Face-domain data survives welding and face reindexing. A positional
        # Python list does not, when fine grille/decal geometry collapses.
        facing=mesh.attributes.new('J73SheetFacing','FLOAT_VECTOR','FACE')
        for item,target in zip(facing.data,self.sheet_normals):
            item.vector=target or (0,0,0)
        obj=bpy.data.objects.new('J73Mesh_'+self.name,mesh)
        scene.collection.objects.link(obj)
        # Native Assimp splits material slots into meshes, preventing node lookup.
        mesh.materials.append(atlas_material)
        uv=mesh.uv_layers.new(name='Palette')
        for polygon, colour, face_uv in zip(mesh.polygons,self.colours,self.face_uvs):
            polygon.material_index=0
            center=polygon.center
            # from_pydata has not evaluated polygon centres yet in every Blender version.
            coords=[mesh.vertices[i].co for i in polygon.vertices]
            x,y,z=(sum(v[i] for v in coords)/len(coords) for i in range(3))
            zone={'Hood':'hood','Trunk':'trunk','DoorLeft':'doorleft','DoorRight':'doorright',
                  'WindowLeft':'windowleft','WindowRight':'windowright','Windshield':'windshield','RearGlass':'rearglass'}.get(self.name,'neutral')
            if self.name=='Body':
                side='left' if x<0 else 'right'
                if colour=='headlamp' and y>2.3: zone='head'+side
                elif colour=='brakeRed' and y<TAIL_FACE+.03: zone='brake'+side
                elif colour=='tail' and y<TAIL_FACE+.03: zone='tail'+side
                elif colour in ('red','redLight','redDark'):
                    zone=('guardf' if y>0 else 'guardr')+('l' if x<0 else 'r') if abs(x)>.55 else 'roof'
            for corner,loop in enumerate(polygon.loop_indices):
                point=mesh.vertices[mesh.loops[loop].vertex_index].co
                local_uv=((point.y*.73+point.x*.31)%1,(point.z*.83+point.x*.53)%1)
                if face_uv is not None:local_uv=face_uv[corner]
                uv.data[loop].uv=atlas.uv(zone,colour,local_uv)
        # Consistent outward normals, including mirrored quarter panels.
        bpy.context.view_layer.objects.active=obj
        obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=.00001)
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT')
        # Open upholstery sheets have an explicit visible side. Closed-component
        # normal recalculation cannot infer which side faces into the cabin.
        oriented=0
        targets=[item.vector.copy() for item in mesh.attributes['J73SheetFacing'].data]
        for polygon,target in zip(mesh.polygons,targets):
            if target.length_squared>0:
                if polygon.normal.dot(Vector(target))<0:
                    polygon.flip()
                oriented+=1
        if oriented:
            mesh.update()
            assert all(target.length_squared==0 or polygon.normal.dot(target)>0
                       for polygon,target in zip(mesh.polygons,targets))
            print('J73_ORIENTED_SHEETS',self.name,oriented)
        if self.name in ('WindowLeft','WindowRight'):
            exterior=-1 if self.name=='WindowLeft' else 1
            for polygon in mesh.polygons:
                if polygon.area>.05 and polygon.normal.x*exterior<-.5:
                    polygon.flip()
            mesh.update()
        for polygon in mesh.polygons:
            polygon.use_smooth=True
        mesh.set_sharp_from_angle(angle=math.radians(35))
        if self.name=='Body':
            # Reacquire UV RNA after edit-mode welding and mesh updates.
            mesh.update()
            uv=mesh.uv_layers.active
            # Glass and painted surround share positional vertices for a
            # closed aperture, but must retain separate reflection normals.
            glass_index=atlas.colours.index('glass')
            glass_faces=set()
            for polygon in mesh.polygons:
                uv_point=uv.data[polygon.loop_start].uv
                slot=int(uv_point.y*16)*32+int(uv_point.x*32)
                if slot%len(atlas.colours)==glass_index:
                    glass_faces.add(polygon.index)
            edge_faces={}
            for polygon in mesh.polygons:
                for loop_index in polygon.loop_indices:
                    edge_faces.setdefault(mesh.loops[loop_index].edge_index,[]).append(polygon.index)
            sharp=mesh.attributes.get('sharp_edge')
            if sharp:
                for edge_index,faces in edge_faces.items():
                    if any(i in glass_faces for i in faces) and any(i not in glass_faces for i in faces):
                        sharp.data[edge_index].value=True
        if self.name=='Body':
            from javelin_fender_normals import transfer_fender_graphic_normals
            transfer_fender_graphic_normals(mesh,atlas.colours,32,16)
        if self.name=='Hood':
            from javelin_fender_normals import transfer_hood_graphic_normals
            transfer_hood_graphic_normals(mesh,atlas.colours,32,16)
        obj.select_set(False)
        return obj

parts={name:Part(name) for name in ('Body','DoorLeft','DoorRight','Hood','Trunk','WindowLeft','WindowRight','Windshield','RearGlass','Interior','Wheel')}
body=parts['Body']

# Shared rear stations shorten only the overhang; cabin, axles and hinges stay fixed.
TAIL_SHORTEN=.11908
TRUNK_FRONT=-1.87
TRUNK_REAR=-2.30+TAIL_SHORTEN
TAIL_FACE=-2.414+TAIL_SHORTEN
TAIL_BUMPER=-2.43+TAIL_SHORTEN
TAIL_SKIN_END=-2.39+TAIL_SHORTEN
TRUNK_RUN=TRUNK_FRONT-TRUNK_REAR
CARGO_FRONT=-1.20
CARGO_REAR=-2.32+TAIL_SHORTEN
CARGO_MID=(CARGO_FRONT+CARGO_REAR)/2
CARGO_RUN=CARGO_FRONT-CARGO_REAR

def width(y):
    # Narrow waist and full wheel-arch shoulders, not a uniform slab side.
    return .8665 - .045 * max(0,(abs(y)-1.65)/.78) + .065*math.exp(-((y+1.36)/.55)**2) + .075*math.exp(-((y-1.43)/.52)**2)
def shoulder(y):
    # Wheelbase-normalized side-reference landmarks: full fender volumes and
    # a high waist, with the front and rear ends tapering below the crowns.
    return (.865 + .095*math.exp(-((y-1.43)/.65)**2)
            + .115*math.exp(-((y+1.36)/.67)**2)
            - .130*max(0,(abs(y)-1.70)/.72))

def side_top(y):
    # Give the rear haunch a broad vertical roll. Ending the upper patch at
    # its highest shoulder station compresses its curvature into a hard ridge.
    t=max(0,min(1,(-y-.85)/1.02))
    front_t=max(0,min(1,(y-.79)/1.60))
    front_drop=.135*math.exp(-((y-1.43)/.60)**2)*math.sin(math.pi*front_t)**2
    rear_t=max(0,min(1,(-y-.44)/1.43))
    rear_drop=.130*math.sin(math.pi*rear_t)**2
    return shoulder(y)-rear_drop-front_drop
def arch(y):
    for center in (1.43,-1.36):
        if abs(y-center)<.39:
            return .34 + math.sqrt(max(0,.39**2-(y-center)**2))
    front=max(0,min(1,(y-2.10)/.29))
    return .28+.035*front*front*(3-2*front)

# Profile samples resolve actual curved wheel openings rather than painted circles.
samples=sorted(set([TAIL_SKIN_END,TRUNK_REAR,-2.23+TAIL_SHORTEN,-1.95,TRUNK_FRONT,-1.72,-.44,.79,1.98,2.25,2.39]+[y for i in range(49) if (y:=round(-2.39+i*4.78/48,5))>TAIL_SKIN_END]+[c+.39*math.cos(i*math.pi/16) for c in (1.43,-1.36) for i in range(17)]))

def side_x(y,z):
    # A rolled lower sill, convex door skin, crisp beltline and rounded shoulders.
    w=width(y)
    rear_flare=.065*math.exp(-((y+1.36)/.55)**2)
    front_flare=.075*math.exp(-((y-1.43)/.52)**2)
    # Fullness is strongest around the wheel opening and rolls inward above
    # and below it. Applying the same width at every Z makes flat flared boxes.
    w-=rear_flare*(1-math.exp(-((z-.73)/.50)**2))
    w-=front_flare*(1-math.exp(-((z-.73)/.34)**2))
    waist=.012*math.exp(-((z-.62)/.24)**2)
    waist+=.0045*math.exp(-((z-.690)/.022)**2)
    sill=.075*max(0,(.37-z)/.16)
    return w+waist-sill

def roof_point(x,y):
    # A compound crown keeps the roof from reading as a flat trapezoid.
    return (x,y,1.32-.070*(abs(x)/.70)**2-.030*((y+.27)/.63)**2)

# Shared closed-aperture anchors keep door skins, glass and fixed quarter trim
# on one continuous beltline instead of separately guessed rectangles.
DOOR_REAR,DOOR_FRONT,DOOR_BOTTOM=-.434,.784,.286
GLASS_BELT=.900
ROOF_REAR=-.80
QUARTER_TIP=-.95
def door_skin_top(y):
    t=(y+.44)/1.23
    return shoulder(-.44)*(1-t)+shoulder(.79)*t-.004
def glass_corner(side,rear,top):
    y=(-.46 if rear else .30) if top else (DOOR_REAR if rear else .79)
    return roof_point(side*.70,y) if top else (side*.82,y,GLASS_BELT)

def window_corner(side,rear,top):
    x,y,z=glass_corner(side,rear,top)
    return (x,y if rear else y-(.035 if top else .055),z)

def door_belt_y(y):
    # The front flange is relieved around the fixed A-pillar foot.
    return y-.038*min(1,max(0,(y-.70)/(DOOR_FRONT-.70)))

def door_edge_y(z,front):
    t=max(0,min(1,(z-DOOR_BOTTOM)/(.860-DOOR_BOTTOM)))
    t=t*t*(3-2*t)
    return DOOR_FRONT-.070*(1-t) if front else DOOR_REAR-.025*(1-t)

def body_side_point(side,y,z):
    if abs(y-.79)<1e-8:y=door_edge_y(z,True)+.006
    elif -.50<y<=-.44+1e-8:
        fade=max(0,min(1,(y+.50)/.06))
        fade=fade*fade*(3-2*fade)
        y+=(door_edge_y(z,False)-.006+.44)*fade
    x=side*side_x(y,z)
    # The front lower corner rolls back instead of ending in a vertical slab.
    front=max(0,min(1,(y-1.98)/.41))
    lower=max(0,min(1,(.50-z)/.22))
    point=(x,y-.150*front*front*lower*lower,z)
    if y>2.34 and z>.70:
        return terminal_side_point(side,y,z,point,front_fender_point,side_top,side_x)
    return point

def rear_quarter_surface(side,y,z):
    # One broad roof-to-flank volume. There is no quarter-tip residual patch.
    upper_z=roof_point(.70,y)[2] if y>=ROOF_REAR else rear_roof_edge(y)
    lower_z=side_top(y)
    upper_x=upper_sail_x(y)
    lower_x=side_x(y,lower_z)
    t=(upper_z-z)/(upper_z-lower_z)
    delta=lower_x-upper_x
    e=1e-5
    side_slope=(side_x(y,lower_z+e)-side_x(y,lower_z-e))/(2*e)
    start=1.15*delta
    end=side_slope*(lower_z-upper_z)
    x=((2*t**3-3*t*t+1)*upper_x+(t**3-2*t*t+t)*start
       +(-2*t**3+3*t*t)*lower_x+(t**3-t*t)*end)
    return (side*x,y,z)

def quarter_glass_point(side,y,z):
    ratio=(z-GLASS_BELT)/(roof_point(.70,-.46)[2]-GLASS_BELT)
    aft=max(0,min(1,(-y-.474)/(QUARTER_TIP* -1-.474)))
    aft=aft*aft*(3-2*aft)
    original=side*(.82-.12*ratio+.045*aft)
    blend=max(0,min(1,(-y-.474)/.226));blend=blend*blend*(3-2*blend)
    shared=rear_quarter_surface(side,y,z)
    return (original*(1-blend)+shared[0]*blend,y,z)

def monotone_profile(x,knots,start_slope,end_slope):
    """C1 cubic station interpolation, bounded without flattening every knot."""
    if x<=knots[0][0]: return knots[0][1]
    if x>=knots[-1][0]: return knots[-1][1]
    h=[b[0]-a[0] for a,b in zip(knots,knots[1:])]
    slopes=[(b[1]-a[1])/step for a,b,step in zip(knots,knots[1:],h)]
    tangents=[start_slope]
    for i in range(1,len(knots)-1):
        left,right=slopes[i-1],slopes[i]
        if left*right<=0: tangents.append(0)
        else:
            w1,w2=2*h[i]+h[i-1],h[i]+2*h[i-1]
            tangents.append((w1+w2)/(w1/left+w2/right))
    tangents.append(end_slope)
    for i,((xa,za),(xb,zb)) in enumerate(zip(knots,knots[1:])):
        if x<=xb:
            t=(x-xa)/(xb-xa)
            return ((2*t**3-3*t*t+1)*za+(t**3-2*t*t+t)*h[i]*tangents[i]
                    +(-2*t**3+3*t*t)*zb+(t**3-t*t)*h[i]*tangents[i+1])

def rear_roof_edge(y):
    knots=((-ROOF_REAR,roof_point(.70,ROOF_REAR)[2]),(.95,1.222),
           (1.13,1.170),(1.35,1.095),(1.52,1.030),(1.72,.965),(1.87,.940))
    roof_slope=.060*(ROOF_REAR+.27)/(.63**2)
    return monotone_profile(-y,knots,roof_slope,-.050/TRUNK_RUN)

def upper_sail_x(y):
    return monotone_profile(-y,((.80,.70),(1.72,.838),(1.87,.85)),0,.080)


def rear_wing_point(side,y,t):
    """One fixed wing profile, matching the sail forward and tail crown aft."""
    low=side_top(y)
    outer=side_x(y,low)
    run=max(0,min(1,(TRUNK_FRONT-y)/TRUNK_RUN))
    fade=max(0,min(1,(TRUNK_FRONT-y)/.05))
    fade=1-fade*fade*(3-2*fade)
    inner_x=.85-.024*run
    inner_z=.936-.050*run+.004*fade
    z=low*(1-t)+inner_z*t
    delta=outer-inner_x
    e=1e-5
    slope=(side_x(y,low+e)-side_x(y,low-e))/(2*e)
    outward=slope*(inner_z-low)
    inward=-1.15*delta
    curved=((2*t**3-3*t*t+1)*outer+(t**3-2*t*t+t)*outward
            +(-2*t**3+3*t*t)*inner_x+(t**3-t*t)*inward)
    blend=run*run*(3-2*run)
    x=curved*(1-blend)+(outer*(1-t)+inner_x*t)*blend
    return (side*x,y,z+.010*math.sin(math.pi*t)*blend)

# Match both adjoining transverse meshes, including the quarter-tip row.
rear_tip_t=(rear_roof_edge(QUARTER_TIP)-1.025)/(rear_roof_edge(QUARTER_TIP)-side_top(QUARTER_TIP))
REAR_WING_T=tuple(sorted(set([i/24 for i in range(25)]+[1-rear_tip_t])))

def hood_base(y):
    # The hood rises with the broad front-wheel fender volume, then falls to
    # the grille. A single sloping plane makes the adjacent crown a thin fin.
    t=max(0,min(1,(y-.81)/1.53))
    return (.875-(y-.81)*.061+.062*math.exp(-((y-1.43)/.55)**2)
            +1.10*t**3*(1-t)**2)

def front_fender_point(side,y,t):
    if y>2.34:return terminal_wing_point(side,y,t,front_fender_point)
    z=side_top(y)
    outer=side_x(y,z)
    slope=(side_x(y,z+.0001)-side_x(y,z-.0001))/.0002
    # A continuous rolled crown leaves the side tangentially, then flattens
    # into the hood edge. A linear ramp with a sine hump leaves a knife ridge.
    run=max(0,min(1,(y-.79)/1.60))
    # Sustain the shoulder into the forward run while retaining both end joins.
    fullness=math.exp(-((y-1.55)/.75)**4)*math.sin(math.pi*run)
    # Local terminal roll. Preserve the aft value/tangent and final edge position.
    # The radius distribution is inferred from the full-frame photographs.
    if 2.10<y<2.39:
        terminal=(y-2.10)/.29
        fullness+=.10*6.75*terminal*terminal*(1-terminal)
    rise=.008+.185*fullness
    controls=((outer,z),(outer+slope*rise,z+rise),(.755,hood_base(y)+.050*fullness),
              (.706,hood_base(y)))
    weights=((1-t)**3,3*(1-t)**2*t,3*(1-t)*t*t,t**3)
    x=sum(weight*point[0] for weight,point in zip(weights,controls))
    zz=sum(weight*point[1] for weight,point in zip(weights,controls))
    # Broaden the existing crest without raising its section maximum or ends.
    z0,z1,z2,z3=(point[1] for point in controls)
    a=-z0+3*z1-3*z2+z3
    b=2*(z0-2*z1+z2)
    c=z1-z0
    extrema=[0.,1.]
    if abs(a)<1e-12:
        if abs(b)>1e-12:extrema.append(-c/b)
    elif b*b-4*a*c>=0:
        root=math.sqrt(b*b-4*a*c)
        extrema.extend(((-b-root)/(2*a),(-b+root)/(2*a)))
    peak=max((1-u)**3*z0+3*(1-u)**2*u*z1+3*(1-u)*u*u*z2+u**3*z3
             for u in extrema if 0<=u<=1)
    breadth=.80*fullness*16*t*t*(1-t)*(1-t)
    zz+=(peak-zz)*breadth
    return artist_point(side,y,t,(side*x,y,zz),outer,z,slope,hood_base(y))

FENDER_T=tuple(i/20 for i in range(21))
SIDE_Z=(.28,.32,.37,.43,.50,.56,.62,.655,.675,.690,.705,.725,.76,.81,.86,.90,.94,.98,1.02)

quarter_controls=((-.474,-.448,roof_point(.70,-.46)[2],GLASS_BELT),
                  (-.59,-.59,1.232,.901),(-.73,-.73,1.207,.907),
                  (-.85,-.85,1.113,.930),(-.93,-.93,1.046,.987),
                  (QUARTER_TIP,QUARTER_TIP,1.025,1.025))
quarter_y=sorted(set([row[0] for row in quarter_controls]
                    +[-.474+i*(QUARTER_TIP+.474)/40 for i in range(41)]),reverse=True)
def quarter_value(y,index):
    knots=tuple((-row[0],row[index]) for row in quarter_controls)
    start=(knots[1][1]-knots[0][1])/(knots[1][0]-knots[0][0])
    end=(knots[-1][1]-knots[-2][1])/(knots[-1][0]-knots[-2][0])
    return monotone_profile(-y,knots,start,end)
quarter_rows=tuple((y,quarter_value(y,1),quarter_value(y,2),quarter_value(y,3)) for y in quarter_y)
def rear_screen(x,t):
    # Local rounded aperture, preserving the existing roof/sail envelope.
    # Photo-derived dimensions are inferred, not a recovered factory radius.
    import math
    u=abs(x)/.66
    blend=t*t*(3-2*t)
    half_width=.66*(1-blend)+.58*blend+.018*math.sin(math.pi*t)**2
    corner=max(0,min(1,(u-.82)/.18))
    radius_fraction=(.050/.66)*(1-blend)+(.060/.58)*blend
    if u<=.82:
        mapped=u/.82*(1-radius_fraction)
    else:
        mapped=1-radius_fraction+radius_fraction*math.sin(corner*math.pi/2)
    xx=math.copysign(half_width*mapped,x) if x else 0
    turn=1-math.cos(corner*math.pi/2)
    yy=-1.64*(1-t)+ROOF_REAR*t+turn*(.045*(1-t)**8-.055*t**8)
    crown=.070*t+.025*(1-t)
    return (xx,yy,rear_roof_edge(yy)+crown*(1-(xx/.70)**2))

def backlight_top_support(x):
    p=rear_screen(x,1)
    corner=max(0,min(1,(abs(x)/.66-.82)/.18))
    if not corner:return p
    # Fixed roof boundary stays at Y=-.80; corner filler closes the local cut.
    xx=p[0]+math.copysign(.12*(1-math.cos(corner*math.pi/2)),x)
    return roof_point(xx,ROOF_REAR)

rear_x=tuple(sorted(set([.66*i/24 for i in range(-24,25)]+[-.50,-.28,.28,.50,-.66*.82,.66*.82])))

backlight_t=tuple(i/20 for i in range(21))
# Shared longitudinal stations prevent T junctions along the sculpted shoulder.
# Independently subdividing the sail leaves alternating shading wedges at its
# join to the coarser side skin, even if both evaluate the same analytic curve.
samples=sorted(set(samples+[2.10,2.24]+[round(2.34+i*.05/12,10) for i in range(13)]+[2.38875,2.3895]+[row[1] for row in quarter_rows]
                   +[QUARTER_TIP-i*(1.87+QUARTER_TIP)/48 for i in range(49)]
                   +[-1.72*(1-t)+ROOF_REAR*t for t in backlight_t]))

for side in (-1,1):
    for a,b in zip(samples,samples[1:]):
        if -.44 <= (a+b)/2 <= .79: continue
        z1,z2=side_top(a),side_top(b)
        for low,high in zip(SIDE_Z,SIDE_Z[1:]):
            za1,za2=(max(arch(a),min(z1,z)) for z in (low,high))
            zb1,zb2=(max(arch(b),min(z2,z)) for z in (low,high))
            points=[body_side_point(side,a,za1),body_side_point(side,b,zb1),
                    body_side_point(side,b,zb2),body_side_point(side,a,za2)]
            if len(set(points))>=3:body.face(points,'red',normal=(side,0,0))
        # The upper fender crown is a curved section, not a separate raised rail.
        crown_t=FENDER_T if (a+b)/2>=.79 else REAR_WING_T if (a+b)/2<=TRUNK_REAR else (0,.25,.55,.8,1)
        for t1,t2 in zip(crown_t,crown_t[1:]):
            def crown(y,z,t):
                if y>=.79:
                    # One continuous wing surface avoids a folded lip where
                    # the narrow nose tapers inside the long hood edge.
                    return front_fender_point(side,y,t)
                if y<=-1.87:
                    lid_t=min(1,max(0,(TRUNK_FRONT-y)/TRUNK_RUN))
                    inner_x=.84-.02*lid_t+.006
                    inner_z=.940-.050*lid_t-.004
                    if y<TRUNK_REAR:
                        aft=max(0,min(1,(TRUNK_REAR-y)/(TRUNK_REAR-TAIL_FACE)))
                        inner_x=.826+.030*aft
                        inner_z=.886+.020*aft
                    return (side*(side_x(y,z)*(1-t)+inner_x*t),y,
                            z*(1-t)+inner_z*t+.010*math.sin(math.pi*t))
                return (side*(width(y)*(1-.13*t)),y,z+.022*math.sin(t*math.pi)-.018*t)
            # The sail/quarter-light surface owns the rear upper quarter.
            # A second inward crown here creates intersecting painted folds.
            if not TRUNK_REAR<(a+b)/2<-.44:
                points=[crown(a,z1,t1),crown(b,z2,t1),crown(b,z2,t2),crown(a,z1,t2)]
                if (a+b)/2>=.79:
                    for triangle in terminal_cell_triangles(a,b,t1,t2,front_fender_point):
                        body.face([front_fender_point(side,y,t) for t,y in triangle],'red')
                else:
                    body.face(points,'red')
        if arch(a)>.25 or arch(b)>.25:
            pa,pb=body_side_point(side,a,arch(a)),body_side_point(side,b,arch(b))
            body.beam((pa[0]*1.002,pa[1],pa[2]),(pb[0]*1.002,pb[1],pb[2]),.006,'chrome',4)
    # Recessed fixed jambs back the narrow panel clearance. The closed door
    # retains a visible seam without a daylight opening into the cabin.
    for y in (-.44,.79):
        levels=sorted(set(max(.28,min(shoulder(y),z)) for z in SIDE_Z))
        for za,zb in zip(levels,levels[1:]):
            outer=[]
            for z,offset in ((za,-.018 if y<0 else 0),(za,0 if y<0 else .018),
                             (zb,0 if y<0 else .018),(zb,-.018 if y<0 else 0)):
                x,yy,_=body_side_point(side,y,z)
                outer.append((x-side*.006,yy+offset,z))
            inner=[(x-side*.015,yy,z) for x,yy,z in outer]
            body.face(outer,'redDark')
            body.face(list(reversed(inner)),'redDark')
            for index in range(4):
                following=(index+1)%4
                body.face([outer[index],inner[index],inner[following],outer[following]],'redDark')
    # Close the wing tops between hood/deck and the muscular outer fender line.
    for a,b in zip(samples,samples[1:]):
        if TRUNK_REAR < (a+b)/2 < TRUNK_FRONT:
            for ta,tb in zip(REAR_WING_T,REAR_WING_T[1:]):
                body.face([rear_wing_point(side,a,ta),rear_wing_point(side,b,ta),
                           rear_wing_point(side,b,tb),rear_wing_point(side,a,tb)],'red',normal=(side,0,1))
    # C pillar, sail panel and bright side-window surround.
    # Broad, tapering sail panels flow into the rear haunches.
    def sail_edge(y,top):
        if top:
            z=roof_point(.70,y)[2] if y>=ROOF_REAR else rear_roof_edge(y)
            x=upper_sail_x(y)
            return (side*x,y,z)
        return (side*side_x(y,side_top(y)),y,side_top(y))
    # The forward quarter-glass edge parallels the main glass divider. Its
    # Small rounded hardtop quarter light, enclosed by a broad painted sail.
    # Shared rounded perimeter, also sampled by the side skin below it.
    for a,b in zip(quarter_rows,quarter_rows[1:]):
        at,ab=quarter_glass_point(side,a[0],a[2]),quarter_glass_point(side,a[1],a[3])
        bt,bb=quarter_glass_point(side,b[0],b[2]),quarter_glass_point(side,b[1],b[3])
        body.face([at,bt,bb,ab],'glass',normal=(side,0,0))
        # The surround is curved sheet metal, not one large flat triangular
        # patch between the glass and roof/shoulder boundary.
        def surround(edge,glass,t):
            y=edge[1]*(1-t)+glass[1]*t
            z=edge[2]*(1-t)+glass[2]*t
            shared=rear_quarter_surface(side,y,z)
            correction=glass[0]-rear_quarter_surface(side,glass[1],glass[2])[0]
            return (shared[0]+correction*t*t*(3-2*t),y,z)
        for i in range(6):
            u,v=i/6,(i+1)/6
            body.face([surround(sail_edge(a[0],True),at,u),surround(sail_edge(b[0],True),bt,u),
                       surround(sail_edge(b[0],True),bt,v),surround(sail_edge(a[0],True),at,v)],'red',normal=(side,0,1))
            body.face([surround(sail_edge(a[1],False),ab,v),surround(sail_edge(b[1],False),bb,v),
                       surround(sail_edge(b[1],False),bb,u),surround(sail_edge(a[1],False),ab,u)],'red',normal=(side,0,1))
        body.beam(at,bt,.007,'chrome')
        body.beam(ab,bb,.007,'chrome')
    quarter_top=quarter_glass_point(side,-.474,roof_point(.70,-.46)[2])
    quarter_bottom=quarter_glass_point(side,-.448,GLASS_BELT)
    body.face([glass_corner(side,True,True),quarter_top,quarter_bottom,glass_corner(side,True,False)],'red')
    body.beam(quarter_bottom,quarter_top,.006,'chrome')
    sail_y=tuple(sorted(set([QUARTER_TIP,-1.52,-1.72,-1.87]
                           +[y for y in samples if -1.87<=y<=QUARTER_TIP]
                           +[QUARTER_TIP-i*(1.87+QUARTER_TIP)/48 for i in range(49)]),reverse=True))
    tip=quarter_glass_point(side,QUARTER_TIP,1.025)
    upper_tip,lower_tip=sail_edge(QUARTER_TIP,True),sail_edge(QUARTER_TIP,False)
    tip_t=(upper_tip[2]-tip[2])/(upper_tip[2]-lower_tip[2])
    transverse=sorted(set([i/24 for i in range(25)]+[tip_t]))
    for a,b in zip(sail_y,sail_y[1:]):
        def sail(y,t):
            upper,lower=sail_edge(y,True),sail_edge(y,False)
            return rear_quarter_surface(side,y,upper[2]*(1-t)+lower[2]*t)
        for t1,t2 in zip(transverse,transverse[1:]):
            body.face([sail(a,t1),sail(b,t1),sail(b,t2),sail(a,t2)],'red',normal=(side,0,1))
    body.beam(glass_corner(side,True,False),glass_corner(side,True,True),.006,'chrome')
    roof_border=tuple(-.46+i*.76/32 for i in range(33))
    for a,b in zip(roof_border,roof_border[1:]):
        body.beam(roof_point(side*.70,a),roof_point(side*.70,b),.009,'chrome')
    body.beam(glass_corner(side,False,True),glass_corner(side,False,False),.025,'red')
    body.beam(glass_corner(side,False,True),glass_corner(side,False,False),.008,'chrome')
    # Side marker lamps.
    body.box((side*(width(1.95)+.006),1.95,.57),(.015,.14,.045),'chromeDark')
    body.box((side*(width(1.95)+.015),1.95,.57),(.012,.105,.024),'amber')
    body.box((side*(width(-2.06)+.009),-2.06,.56),(.02,.11,.035),'tail')
    # The video car has exposed chrome side exhausts with slotted heat shields.
    build_sidepipe(body,side)

# Roof, rear deck and low nose, all independent of opening panels.
roof_y=tuple(sorted(set([ROOF_REAR,-.70,-.57,-.46,-.27,-.15,.0,.12,.30]
                       +[ROOF_REAR+i*(.30-ROOF_REAR)/36 for i in range(37)])))
roof_x=tuple(sorted(set([-.70+i*1.40/40 for i in range(41)]+[backlight_top_support(x)[0] for x in rear_x])))
for ya,yb in zip(roof_y,roof_y[1:]):
    for xa,xb in zip(roof_x,roof_x[1:]):
        body.face([roof_point(xa,ya),roof_point(xb,ya),roof_point(xb,yb),roof_point(xa,yb)],'red')
# The apron is generated below with the backlight columns so both boundaries
# share one crowned surface, without an underlying overlapping planar chord.
body.sheet([(-.82,.79,.895),(.82,.79,.895),(.81,.805,.875),(-.81,.805,.875)],'redDark',.008)
build_valance(body)
# The lower nose and side share a real corner return instead of an open step.
for side in (-1,1):
    for index in range(12):
        a,b=index/12,(index+1)/12
        pa,pb=valance_point(side,a),valance_point(side,b)
        sa,sb=body_side_point(side,2.39,pa[2]),body_side_point(side,2.39,pb[2])
        body.face([sa,sb,pb,pa],'red',normal=(side,0,0))
# Lower rear sheet is built from the shared curved fascia boundary.
# The rear module cuts real apertures into the fascia before seating lenses.
# Narrow axle-zone floor rails leave the tires' steering sweep unobstructed.
body.box((0,0,.26),(1.08,4.2,.065),'shadow')
body.box((0,0,.26),(1.50,2.0,.065),'shadow')
# Chromed bumpers with rubber overriders.
build_rear_bumper(body,TAIL_BUMPER)

# The front bumper wraps back around the headlamp pods. Its upper and lower
# chamfers follow the same shallow bow instead of reading as a straight rail.
bumper_x=tuple(-.89+i*1.78/64 for i in range(65))
def bumper_section(x):
    y=2.426-.135*(abs(x)/.89)**3
    z=.452-.015*(abs(x)/.89)**2
    def roll(value):
        return math.copysign(math.sqrt(abs(value)),value)
    return [(x,y+.052*.70*roll(math.cos(i*math.tau/24)),
             z+(.002+.045*roll(math.sin(i*math.tau/24)))*.58) for i in range(24)]
for a,b in zip(bumper_x,bumper_x[1:]):
    aa,bb=bumper_section(a),bumper_section(b)
    for i in range(len(aa)):
        j=(i+1)%len(aa)
        body.face([aa[i],bb[i],bb[j],aa[j]],'chrome')
body.face(bumper_section(bumper_x[0]),'chrome')
body.face(list(reversed(bumper_section(bumper_x[-1]))),'chrome')
for x in (-.57,.57):
    body.rounded_plate((x,2.432,.450),(.078,.112,.170),.012,'rubber')

# Shaped recessed 1973 front fascia, authored from the supplied car.
build_front(body,terminal_front_contract(front_fender_point,FENDER_T))
# Recessed reference tail lamps with thin chrome lips and curved sheet metal.
build_rear(body,TAIL_FACE)
build_plate(body,TAIL_FACE)
# Close the fixed tail behind the opening trunk and seat the factory lip on
# that deck, instead of leaving an open slot underneath a separate raised bar.

# Long door skins, chrome handles, separate frameless side windows and mirrors.
for side,suffix in ((-1,'Left'),(1,'Right')):
    door=parts['Door'+suffix]
    door_y=tuple(DOOR_REAR+(DOOR_FRONT-DOOR_REAR)*i/24 for i in range(25))
    def skin_z(y,z):
        z=max(DOOR_BOTTOM,min(door_skin_top(y),z))
        u=(y-DOOR_REAR)/(DOOR_FRONT-DOOR_REAR)
        yy=door_edge_y(z,False)*(1-u)+door_edge_y(z,True)*u
        return (side*side_x(yy,z),yy,z)
    def skin(y,t):
        return skin_z(y,DOOR_BOTTOM+(door_skin_top(y)-DOOR_BOTTOM)*t)
    for a,b in zip(door_y,door_y[1:]):
        for za,zb in zip(SIDE_Z,SIDE_Z[1:]):
            points=[skin_z(a,za),skin_z(b,za),skin_z(b,zb),skin_z(a,zb)]
            if len(set(points))>=3:door.face(points,'red')
        door.face([skin(a,1),skin(b,1),(side*.82,door_belt_y(b),GLASS_BELT),(side*.82,door_belt_y(a),GLASS_BELT)],'red')
    for y in (DOOR_REAR,DOOR_FRONT):
        door_t=sorted(set(max(0,min(1,(z-DOOR_BOTTOM)/(door_skin_top(y)-DOOR_BOTTOM))) for z in SIDE_Z))
        def cap(t):
            outer=skin(y,t)
            inner=(side*.82,outer[1]-(.038*t**3 if y==DOOR_FRONT else 0),
                   outer[2]+(GLASS_BELT-door_skin_top(y))*t**3)
            return outer,inner
        for ta,tb in zip(door_t,door_t[1:]):
            oa,ia=cap(ta);ob,ib=cap(tb)
            door.face([oa,ia,ib,ob],'redDark')
    # Dark door card with the factory-style Cardin fabric inset.
    build_doorcard(door,side)
    build_handle(door,side,side_x)
    build_mirror(door,side,side_x)
    glass=parts['Window'+suffix]
    glass.face([window_corner(side,True,False),window_corner(side,False,False),
                window_corner(side,False,True),window_corner(side,True,True)],'glass')
    glass.beam(window_corner(side,True,False),window_corner(side,False,False),.007,'chrome')

def screen(x,t):
    top_x=x*(.70/.815)
    top_z=roof_point(top_x,.30)[2]
    return (x*(1-t)+top_x*t,.79*(1-t)+.30*t-.020*math.sin(math.pi*t)*(1-(x/.815)**2),GLASS_BELT*(1-t)+top_z*t)
for xa,xb in zip((-.815,-.61,-.32,0,.32,.61),(-.61,-.32,0,.32,.61,.815)):
    parts['Windshield'].face([screen(xa,0),screen(xb,0),screen(xb,1),screen(xa,1)],'glass')
for xa,xb in zip(rear_x,rear_x[1:]):
    if abs(xa)/.66>.82 or abs(xb)/.66>.82:
        body.face([rear_screen(xa,1),rear_screen(xb,1),backlight_top_support(xb),backlight_top_support(xa)],'red',normal=(0,0,1))
    for a,b in zip(backlight_t,backlight_t[1:]):
        parts['RearGlass'].face([rear_screen(xa,a),rear_screen(xb,a),rear_screen(xb,b),rear_screen(xa,b)],'glass',normal=(0,-.35,.94))
    body.beam(rear_screen(xa,0),rear_screen(xb,0),.009,'chrome')
    body.beam(rear_screen(xa,1),rear_screen(xb,1),.009,'chrome')
for side in (-1,1):
    for a,b in zip(backlight_t,backlight_t[1:]):
        def backlight_border(t,u):
            p=rear_screen(side*.66,t)
            outer_y=-1.72*(1-t)+ROOF_REAR*t
            outer_x=side*upper_sail_x(outer_y)
            outer_z=rear_roof_edge(outer_y)
            return (p[0]*(1-u)+outer_x*u,p[1]*(1-u)+outer_y*u,
                    p[2]*(1-u)+outer_z*u+.012*math.sin(math.pi*u)*math.sin(math.pi*t)+.006*math.sin(math.pi*u)*(1-t)**8)
        for u,v in zip((0,.33,.66),(.33,.66,1)):
            body.face([backlight_border(a,u),backlight_border(b,u),backlight_border(b,v),backlight_border(a,v)],'red')
        body.beam(rear_screen(side*.66,a),rear_screen(side*.66,b),.009,'chrome')
# Match every curved lower-glass column instead of spanning its corners with
# a straight chord, which leaves the crowned centre unsupported.
apron_x=tuple(sorted(set([i/24 for i in range(-24,25)]+[x/.66 for x in rear_x])))
apron_y=tuple(sorted(set([i/12 for i in range(13)]+[.08/.23]
                        +[(-y-1.64)/.23 for y in samples if -1.87<=y<=-1.72])))
def apron_point(u,t):
    glass=rear_screen(u*.66,0)
    corner=.08/.23
    if t<=corner:
        v=t/corner
        xx=glass[0]*(1-v)+u*.838*v
        yy=glass[1]*(1-v)-1.72*v
        z=glass[2]*(1-v)+.965*v+.006*math.sin(math.pi*v)
    else:
        v=(t-corner)/(1-corner)
        yy=-1.72*(1-v)-1.87*v
        xx=u*upper_sail_x(yy)
        z=rear_roof_edge(yy)
    return (xx,yy,z)
for ua,ub in zip(apron_x,apron_x[1:]):
    for a,b in zip(apron_y,apron_y[1:]):
        points=[apron_point(ua,a),apron_point(ua,b),apron_point(ub,b),apron_point(ub,a)]
        body.face(points,'red',normal=(0,0,1))
        body.face([(x,y,z-.012) for x,y,z in reversed(points)],'redDark')
apron_edge=([apron_point(-1,t) for t in apron_y]+
            [apron_point(u,1) for u in apron_x[1:]]+
            [apron_point(1,t) for t in reversed(apron_y[:-1])]+
            [apron_point(u,0) for u in reversed(apron_x[1:-1])])
for a,b in zip(apron_edge,apron_edge[1:]+apron_edge[:1]):
    body.face([a,(a[0],a[1],a[2]-.012),(b[0],b[1],b[2]-.012),b],'redDark')
for xa,xb in zip((-.815,-.61,-.32,0,.32,.61),(-.61,-.32,0,.32,.61,.815)):
    body.beam(screen(xa,0),screen(xb,0),.009,'chrome')
    body.beam(screen(xa,1),screen(xb,1),.009,'chrome')
build_wipers(body,screen)

# Continuous contoured hood skin; the AMX bulge is stamped into the panel.
hood=parts['Hood']
hood_x=(-.700,-.60,-.46,-.29,-.14,0,.14,.29,.46,.60,.700)
hood_y=(.81,.94,1.08,1.23,1.40,1.60,1.78,1.96,2.10,2.24,2.34)
def hood_point(x,y):
    bulge=.055*math.exp(-(x/.38)**4)*math.exp(-((y-1.55)/.54)**4)
    return (x,y,hood_base(y)+.014*(1-(x/.8)**2)+bulge)
for a,b in zip(hood_y,hood_y[1:]):
    for xa,xb in zip(hood_x,hood_x[1:]):
        colour='red'
        top=[hood_point(xa,a),hood_point(xb,a),hood_point(xb,b),hood_point(xa,b)]
        for indices in ((0,1,2),(0,2,3)):
            hood.face([top[i] for i in indices],colour)
        hood.face([(x,y,z-.012) for x,y,z in reversed(top)],'redDark')
for x in (hood_x[0],hood_x[-1]):
    for a,b in zip(hood_y,hood_y[1:]):
        pa,pb=hood_point(x,a),hood_point(x,b)
        hood.face([pa,(pa[0],pa[1],pa[2]-.012),(pb[0],pb[1],pb[2]-.012),pb],'redDark')
for y in (hood_y[0],hood_y[-1]):
    for a,b in zip(hood_x,hood_x[1:]):
        pa,pb=hood_point(a,y),hood_point(b,y)
        hood.face([pa,(pa[0],pa[1],pa[2]-.012),(pb[0],pb[1],pb[2]-.012),pb],'redDark')
# The short fixed nose return closes the gap between the opening hood edge
# and the top of the grille while continuing the reference's black T stripe.
for xa,xb in zip(hood_x,hood_x[1:]):
    rear_a,rear_b=hood_point(xa,hood_y[-1]),hood_point(xb,hood_y[-1])
    def nose_point(x,rear,y):
        t=(y-2.34)/(.059)
        return (x,y,rear[2]*(1-t)+.79*t)
    mid_a,mid_b=nose_point(xa,rear_a,2.385),nose_point(xb,rear_b,2.385)
    body.sheet([rear_a,rear_b,mid_b,mid_a],'black')
    body.sheet([mid_a,mid_b,(xb,2.399,.79),(xa,2.399,.79)],'red')
for x in (-.31,.31):
    for y in (.90,.935,.97): hood.box((x,y,hood_point(x,y)[2]+.003),(.25,.009,.008),'black')
trunk=parts['Trunk']
build_trunk_lid(trunk,TRUNK_FRONT,TRUNK_REAR)
# The rear return, its emblems and factory deck lip belong to the opening lid.
build_spoiler(trunk,TRUNK_REAR,TAIL_FACE)

build_engine(body)

# Original cabin: bucket seats, sculpted backrests and ribbon upholstery.
inside=parts['Interior']
inside.box((0,-.17,.30),(1.08,2.75,.04),'black')
inside.box((0,-.005,.30),(1.58,2.01,.04),'black')
# Dark compartment liners keep the visible engine and usable cargo cavity
# separate from the tires and road, including when either lid is open.
inside.box((0,CARGO_MID,.285),(1.20,CARGO_RUN,.035),'black')
inside.box((0,TRUNK_REAR-.005,.505),(1.20,.025,.44),'black')
inside.box((0,-1.20,.56),(1.20,.025,.55),'black')
for side in (-1,1):
    inside.box((side*.60,CARGO_MID,.50),(.026,CARGO_RUN,.43),'black')
    inside.box((side*.55,1.48,.515),(.026,1.27,.43),'black')
from javelin_cargo import build_cargo_returns
build_cargo_returns(inside, CARGO_REAR, CARGO_FRONT, side_x)
build_dashboard(inside)
inside.box((0,-.01,.43),(.20,1.13,.25),'black')
build_cockpit(inside)
build_pedals(inside)
build_seats(inside)

# Downward-facing original headliner follows the inside of the crowned roof.
HEADLINER_X=(-.66,-.44,-.22,0,.22,.44,.66)
HEADLINER_Y=(-.77,-.60,-.43,-.26,-.09,.09,.27)
def inner_roof(x,y,lower=0):
    p=roof_point(x,y)
    return (x,y,p[2]-.018-lower)
for xa,xb in zip(HEADLINER_X,HEADLINER_X[1:]):
    for ya,yb in zip(HEADLINER_Y,HEADLINER_Y[1:]):
        inside.face([inner_roof(xa,ya),inner_roof(xa,yb),inner_roof(xb,yb),inner_roof(xb,ya)],'seat',normal=(0,0,-1))

def clip_roof_cell(poly,xa,xb,ya,yb):
    """Clip a ribbon into one planar base cell before placing it 1mm below."""
    for axis,bound,sign in ((0,xa,1),(0,xb,-1),(1,ya,1),(1,yb,-1)):
        result=[]
        if not poly: break
        previous=poly[-1]
        previous_inside=sign*(previous[axis]-bound)>=-1e-10
        for point in poly:
            current_inside=sign*(point[axis]-bound)>=-1e-10
            if current_inside!=previous_inside:
                t=(bound-previous[axis])/(point[axis]-previous[axis])
                result.append(tuple(previous[j]+t*(point[j]-previous[j]) for j in (0,1)))
            if current_inside:result.append(point)
            previous,previous_inside=point,current_inside
        poly=result
    if len(poly)<3:return []
    area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2
    if area<1e-10:return []
    points=[]
    for x,y in poly:
        u,v=(x-xa)/(xb-xa),(y-ya)/(yb-ya)
        za=inner_roof(xa,ya)[2]*(1-u)+inner_roof(xb,ya)[2]*u
        zb=inner_roof(xa,yb)[2]*(1-u)+inner_roof(xb,yb)[2]*u
        points.append((x,y,za*(1-v)+zb*v-.001))
    return points
def roof_u(inset):
    half=.62-inset;back=-.73+inset;r=max(.03,.18-inset)
    path=[(-half,.24),(-half,back+r)]
    path += [(-half+r+r*math.cos(math.pi+i*math.pi/12),back+r+r*math.sin(math.pi+i*math.pi/12)) for i in range(1,7)]
    path += [(half-r,back)]
    path += [(half-r+r*math.cos(math.pi*1.5+i*math.pi/12),back+r+r*math.sin(math.pi*1.5+i*math.pi/12)) for i in range(1,7)]
    path += [(half,.24)]
    return path
inset=0
for col,w in (('wine',.010),('pink',.014),('cream',.023),('black',.003),('cream',.023),('pink',.014),('wine',.010)):
    outer,inner=roof_u(inset),roof_u(inset+w)
    for i in range(len(outer)-1):
        quad=[outer[i],outer[i+1],inner[i+1],inner[i]]
        for xa,xb in zip(HEADLINER_X,HEADLINER_X[1:]):
            for ya,yb in zip(HEADLINER_Y,HEADLINER_Y[1:]):
                pts=clip_roof_cell(quad,xa,xb,ya,yb)
                if pts:inside.face(list(reversed(pts)),col,normal=(0,0,-1))
    inset+=w
# Central roof lamp, seen between the Cardin ribbon runs in the cabin gallery.
dome_z=inner_roof(0,-.25)[2]-.010
inside.ellipsoid((0,-.25,dome_z),(.059,.051,.009),'chrome',segments=40,rings=16)
inside.ellipsoid((0,-.25,dome_z-.007),(.051,.043,.007),'cream',segments=40,rings=16)
build_steering(inside)
build_roof_hardware(inside,inner_roof,HEADLINER_X,HEADLINER_Y)

# Wheel at origin, tire around X axle. Four instances are placed by the game.
wheel=parts['Wheel']
build_wheel(wheel)

build_decals(body,hood,trunk,wheel,hood_point=hood_point,hood_x=hood_x,
             hood_y=hood_y,side_x=side_x,tail_face=TAIL_FACE,
             badge_z=.885,badge_y=lambda x,z:spoiler_rear_point(x,z,TAIL_FACE)[1]-.001,
             fender_point=front_fender_point,
             fender_y=[y for y in samples if y>=.79],fender_t=FENDER_T,fender_front=2.375,
             fender_triangles=lambda ya,yb,ta,tb:terminal_cell_triangles(ya,yb,ta,tb,front_fender_point))
objects={name:part.object() for name,part in parts.items()}

# One original armature, identity object transforms, explicit mechanical pivots.
rig_data=bpy.data.armatures.new('J73_Skeleton')
rig=bpy.data.objects.new('J73_Skeleton',rig_data)
scene.collection.objects.link(rig)
bpy.context.view_layer.objects.active=rig
rig.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
door_hinge_x=width(.79)+.022+.004
pivots={'Root':(0,0,.65),'DoorLeft':(-door_hinge_x,.79,.65),'DoorRight':(door_hinge_x,.79,.65),'Hood':(0,.81,hood_point(0,.81)[2]),'Trunk':(0,-1.87,.940),
        'WindowLeft':(-door_hinge_x,.79,.65),'WindowRight':(door_hinge_x,.79,.65)}
for name,pivot in pivots.items():
    bone=rig_data.edit_bones.new(name)
    bone.head=(pivot[0],pivot[1],pivot[2]-.65)
    # Vertical bones keep the local Y hinge axis vertical for door swings.
    bone.tail=(pivot[0],pivot[1],pivot[2]-.45)
    if name!='Root':
        parent='Door'+name.removeprefix('Window') if name.startswith('Window') else 'Root'
        bone.parent=rig_data.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
rig.select_set(False)
bone_for={'WindowLeft':'WindowLeft','WindowRight':'WindowRight'}
for name,obj in objects.items():
    if name=='Wheel': continue
    bone=bone_for.get(name,name if name in pivots else 'Root')
    group=obj.vertex_groups.new(name=bone)
    group.add(list(range(len(obj.data.vertices))),1.0,'REPLACE')
    modifier=obj.modifiers.new('J73_RigidPanels','ARMATURE')
    modifier.object=rig
    obj.parent=rig

rig.animation_data_create()
clips=('J73_Panels','J73_WindowLeft','J73_WindowRight')
for clip in clips:
    rig.animation_data.action=bpy.data.actions.new(clip)
    rig.animation_data.action.use_fake_user=True
    for bone in rig.pose.bones:
        bone.rotation_mode='XYZ'
        bone.rotation_euler=(0,0,0)
        bone.location=(0,0,0)
        bone.keyframe_insert(data_path='rotation_euler',frame=1)
        bone.keyframe_insert(data_path='location',frame=1)
        if clip=='J73_Panels':
            if bone.name=='DoorLeft': bone.rotation_euler[1]=math.radians(-66)
            elif bone.name=='DoorRight': bone.rotation_euler[1]=math.radians(66)
            elif bone.name=='Hood': bone.rotation_euler[0]=math.radians(57)
            elif bone.name=='Trunk': bone.rotation_euler[0]=math.radians(-47)
        elif bone.name==clip.removeprefix('J73_'):
            # Local Y follows the vertical bone, lowering glass into its door.
            bone.location[1]=-.45
        bone.keyframe_insert(data_path='rotation_euler',frame=31)
        bone.keyframe_insert(data_path='location',frame=31)
rig.animation_data.action=bpy.data.actions['J73_Panels']
scene.frame_set(1)

manifest={'vehicle':'Base.Javelin73PC','units':'metres','source':'Original procedural geometry authored in tools/build_mod.py',
          'animations':list(clips),'parts':[]}
for name,obj in objects.items():
    coords=[v.co for v in obj.data.vertices]
    bounds=[[round(f(v[i] for v in coords),5) for i in range(3)] for f in (min,max)]
    manifest['parts'].append({'name':name,'model':'J73_'+name,'mesh':'vehicles/J73_Car|J73Mesh_'+name,
        'vertices':len(coords),'triangles':sum(len(p.vertices)-2 for p in obj.data.polygons),'bounds':bounds})
manifest['bounds']=[[min(part['bounds'][0][axis] for part in manifest['parts']) for axis in range(3)],
                    [max(part['bounds'][1][axis] for part in manifest['parts']) for axis in range(3)]]
(ART / 'model-manifest.json').write_text(json.dumps(manifest,indent=2))

# Explicit per-part colours use the shared original atlas, with no random tint.
model_defs=['module Base','{']
for name in objects:
    animated=name in ('DoorLeft','DoorRight','Hood','Trunk','WindowLeft','WindowRight')
    model_defs.extend([f'    model J73_{name}','    {',f'        mesh = vehicles/J73_Car|J73Mesh_{name},',
        '        texture = Vehicles/J73_Palette,','        shader = vehicle,',
        '        scale = 0.01,',f'        static = {str(not animated).lower()},','        invertX = false,'])
    if name in ('WindowLeft','WindowRight'):
        model_defs.append(f'        boneWeight = {name} 1.0,')
    model_defs.append('    }')
model_defs.append('}')
(MEDIA / 'scripts/j73_models.txt').write_text('\n'.join(model_defs)+'\n')

# Bake only export copies into native centimetre coordinates. The renderer
# transposes imported node transforms, so bake the effective -90-degree X basis.
export_objects=list(objects.values())+[rig]
bpy.ops.object.select_all(action='DESELECT')
for obj in export_objects: obj.select_set(True)
bpy.context.view_layer.objects.active=rig
export_args=dict(use_selection=True,object_types={'ARMATURE','MESH'},axis_forward='Y',axis_up='Z',
    global_scale=1.0,apply_unit_scale=True,apply_scale_options='FBX_SCALE_NONE',
    add_leaf_bones=False,bake_anim=True,bake_anim_use_nla_strips=False,
    bake_anim_use_all_actions=True,bake_anim_simplify_factor=0,use_triangles=True,path_mode='STRIP')
source_data={obj:obj.data for obj in export_objects}
source_unit_scale=scene.unit_settings.scale_length
source_keys=[]
export_basis=Matrix.Scale(100,4) @ Matrix.Rotation(-math.pi/2,4,'X')
try:
    for obj in export_objects:
        obj.data=obj.data.copy()
        obj.data.transform(export_basis)
    for clip in clips:
        action=bpy.data.actions[clip]
        for slot in action.slots:
            for layer in action.layers:
                for strip in layer.strips:
                    bag=strip.channelbag(slot)
                    if not bag: continue
                    for curve in bag.fcurves:
                        if not curve.data_path.endswith('.location'): continue
                        for key in curve.keyframe_points:
                            source_keys.append((key,key.co.copy(),key.handle_left.copy(),key.handle_right.copy()))
                            key.co[1]*=100
                            key.handle_left[1]*=100
                            key.handle_right[1]*=100
    scene.unit_settings.scale_length=.01
    bpy.context.view_layer.update()
    bpy.ops.export_scene.fbx(filepath=str(MEDIA/'models_X/vehicles/J73_Car.fbx'),**export_args)
    bpy.ops.export_scene.fbx(filepath=str(MEDIA/'anims_X/vehicles/J73_Panels.fbx'),**export_args)
    for exported in (MEDIA/'models_X/vehicles/J73_Car.fbx', MEDIA/'anims_X/vehicles/J73_Panels.fbx'):
        clean_fbx(exported)
finally:
    for key,coordinate,left,right in source_keys:
        key.co=coordinate
        key.handle_left=left
        key.handle_right=right
    for obj,data in source_data.items():
        exported_data=obj.data
        obj.data=data
        if obj.type=='ARMATURE': bpy.data.armatures.remove(exported_data)
        else: bpy.data.meshes.remove(exported_data)
    scene.unit_settings.scale_length=source_unit_scale
    bpy.context.view_layer.update()

# Editable source and a transparent studio preview, independent of game testing.
from blender_studio_material import configure_studio
configure_studio(atlas_material,atlas_texture,atlas_bsdf,PALETTE,rgba)
for side in (-1,1):
    for y in (1.43,-1.36):
        copy=objects['Wheel'].copy()
        copy.data=objects['Wheel'].data
        copy.name=f'PreviewWheel_{side}_{y}'
        copy.location=(side*.77,y,.33-.65)
        scene.collection.objects.link(copy)
objects['Wheel'].hide_render=True
objects['Wheel'].hide_set(True)
scene.world=bpy.data.worlds.new('StudioWorld')
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.14,.18,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.4
for position,energy,size in (((-3,4,7),1100,5),((4,1,4),650,4),((0,-5,5),850,3)):
    light_data=bpy.data.lights.new('Softbox','AREA')
    light_data.energy=energy
    light_data.shape='DISK'
    light_data.size=size
    light=bpy.data.objects.new('Softbox',light_data)
    scene.collection.objects.link(light)
    light.location=position
    light.rotation_euler=(Vector((0,0,0))-light.location).to_track_quat('-Z','Y').to_euler()
camera_data=bpy.data.cameras.new('PreviewCamera')
camera=bpy.data.objects.new('PreviewCamera',camera_data)
scene.collection.objects.link(camera)
scene.camera=camera
camera.location=(-6,8,3.9)
camera.rotation_euler=(Vector((0,0,.1))-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type='ORTHO'
camera_data.ortho_scale=6.1
scene.render.engine='CYCLES'
scene.cycles.samples=32
scene.render.resolution_x=1400
scene.render.resolution_y=1000
scene.render.resolution_percentage=100
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(ART/'javelin-preview.png')
for screen_data in bpy.data.screens:
    for area in screen_data.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active
            space.shading.type='MATERIAL'
            space.overlay.show_overlays=False
            space.region_3d.view_perspective='CAMERA'
bpy.ops.wm.save_as_mainfile(filepath=str(ART/'Javelin73PC.blend'))
bpy.ops.render.render(write_still=True)
# Reproducible orthographic silhouette and rear-trim inspection views.
scene.render.resolution_y=800
for name,position,target in (
        ('side',(-8,0,.5),(0,0,0)),
        ('front',(0,8,.6),(0,0,.05)),
        ('rear',(-4,-7,3),(0,0,.1))):
    camera.location=position
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    camera_data.ortho_scale=5.8
    scene.render.filepath=str(ART/f'javelin-{name}.png')
    bpy.ops.render.render(write_still=True)
# Low perspective view for comparison with the supplied video's camera height.
# This is an estimated inspection camera, not an optical calibration.
camera_data.type='PERSP'
camera_data.lens=45
camera.location=(-1.0,6.0,.75)
camera.rotation_euler=(Vector((0,.6,.0))-camera.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_y=1000
scene.render.filepath=str(ART/'javelin-perspective.png')
bpy.ops.render.render(write_still=True)
print('J73_BUILD_COMPLETE',sum(p['triangles'] for p in manifest['parts']),'triangles')
