"""Original round chrome rear-view mirrors, attached to their moving doors."""
import math


def mirror_frame(side):
    """Source +Y is the nose; reflective normals face aft and slightly inward."""
    normal=(-side*.18,-math.sqrt(1-.18**2),0)
    horizontal=(math.sqrt(1-.18**2),-side*.18,0)
    return normal,horizontal


def build_mirror(door,side,side_x):
    normal,horizontal=mirror_frame(side)
    center=(side*.965,.615,.986)

    def point(depth,radius,angle):
        return (center[0]+normal[0]*depth+horizontal[0]*radius*math.cos(angle),
                center[1]+normal[1]*depth+horizontal[1]*radius*math.cos(angle),
                center[2]+radius*math.sin(angle))

    # Short swept pedestal, seated on the actual door skin, supports a round
    # domed pod. The former side-facing elongated ellipsoid is removed.
    foot=(side*(side_x(.59,.88)+.002),.59,.88)
    door.ellipsoid(foot,(.010,.038,.011),'chrome',segments=24,rings=8)
    door.beam(foot,(side*.947,.618,.947),.009,'chrome',12)
    door.beam((side*.947,.618,.947),(side*.965,.620,.961),.011,'chrome',12)
    segments=48
    sections=((-0.044,.012),(-.035,.033),(-.018,.048),(.007,.055),(.020,.055))
    rings=[[point(depth,radius,i*math.tau/segments) for i in range(segments)]
           for depth,radius in sections]
    tip=point(-.047,0,0)
    for i in range(segments):
        j=(i+1)%segments
        door.face([tip,rings[0][j],rings[0][i]],'chrome')
    for a,b in zip(rings,rings[1:]):
        for i in range(segments):
            j=(i+1)%segments
            door.face([a[i],a[j],b[j],b[i]],'chrome')
    # Rolled bright lip, narrow dark seal and recessed reflective disk.
    seal=[point(.020,.050,i*math.tau/segments) for i in range(segments)]
    glass=[point(.0185,.0485,i*math.tau/segments) for i in range(segments)]
    for i in range(segments):
        j=(i+1)%segments
        door.face([rings[-1][i],rings[-1][j],seal[j],seal[i]],'chrome')
        door.face([seal[i],seal[j],glass[j],glass[i]],'black')
        door.face([point(.0185,0,0),glass[i],glass[j]],'silverLight')
