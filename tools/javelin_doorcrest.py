"""Original procedural door-insert Cardin spiral and caption, no imported art."""
from javelin_decals import stroke

# Hand-authored open spiral silhouette, distinct from the exterior PC strokes.
OUTLINE=((- .50,-.50),(-.50,.50),(.05,.50),(.28,.47),(.44,.34),(.49,.16),
         (.46,.00),(.37,-.12),(.24,-.17),(.08,-.13),(-.015,-.035),(-.005,.085),
         (.065,.165),(.16,.18),(.235,.135),(.255,.065),(.22,.015),(.16,.005),
         (.125,.04),(.135,.08),(.175,.085),(.18,.115),(.125,.135),(.075,.10),
         (.05,.035),(.075,-.025),(.135,-.065),(.235,-.075),(.325,-.025),
         (.35,.065),(.30,.16),(.20,.22),(.075,.235),(-.065,.20),(-.17,.10),
         (-.22,-.055),(-.17,-.235),(-.05,-.375),(.14,-.455),(.48,-.49),(.48,-.53))
def rounded_outline(points):
    # Retain the straight cast upright/base, round only the authored curl turns.
    result=[]
    for i,p in enumerate(points):
        if i in (0,1,39,40):
            result.append(p)
            continue
        previous,following=points[i-1],points[(i+1)%len(points)]
        a=tuple(p[j]+(previous[j]-p[j])*.22 for j in (0,1))
        b=tuple(p[j]+(following[j]-p[j])*.22 for j in (0,1))
        for t in (0,.333333,.666667,1):
            result.append(tuple((1-t)**2*a[j]+2*(1-t)*t*p[j]+t*t*b[j] for j in (0,1)))
    return tuple(result)

OUTLINE=rounded_outline(OUTLINE)

# Original compact lowercase stroke alphabet for the tiny cast caption.
GLYPHS={
 'p':(((0,-.25),(0,1),(.60,1),(.88,.82),(.88,.56),(.60,.40),(0,.40)),),
 'i':(((.35,0),(.35,.70)),((.35,.92),(.35,1))),
 'e':(((.85,.20),(.65,.02),(.20,.02),(0,.25),(0,.58),(.20,.80),(.65,.80),(.85,.60),(.85,.40),(0,.40)),),
 'r':(((0,0),(0,.80)),((0,.55),(.25,.80),(.65,.80),(.85,.60))),
 'c':(((.85,.65),(.65,.80),(.20,.80),(0,.60),(0,.20),(.20,0),(.65,0),(.85,.15)),),
 'a':(((.80,0),(.80,.80),(.25,.80),(0,.60),(0,.20),(.25,0),(.80,0)),),
 'd':(((.80,0),(.80,1)),((.80,.70),(.25,.80),(0,.60),(0,.20),(.25,0),(.80,0))),
 'n':(((0,0),(0,.80)),((0,.55),(.25,.80),(.60,.80),(.80,.60),(.80,0))),
}

def build_cardin_door_crest(door,side,y=.105,z=.739):
    normal=(-side,0,0)
    def point(u,v,x=.7824):
        # Camera-right from the cabin is source -side*Y, so neither wordmark mirrors.
        return (side*x,y-side*u,z+v)
    polygon=[point(u*.031,v*.038) for u,v in OUTLINE]
    door.face(polygon,'chrome',normal=normal)
    edge=[(u*.031,v*.038) for u,v in OUTLINE]+[(OUTLINE[0][0]*.031,OUTLINE[0][1]*.038)]
    stroke(door,edge,.0007,lambda u,v:point(u,v,.7819),'silverLight',normal,round_joins=True)
    # Cast caption foot, with no inferred enamel pigment or copied font.
    foot=[(-.016,-.029),(.016,-.029),(.016,-.020),(-.016,-.020)]
    door.face([point(u,v) for u,v in foot],'chrome',normal=normal)
    stroke(door,foot+[foot[0]],.00065,lambda u,v:point(u,v,.7819),'silverLight',normal,round_joins=True)
    text='pierre cardin';advance=.029/len(text);height=.0048
    for i,char in enumerate(text):
        if char==' ':continue
        origin=-len(text)*advance/2+i*advance
        for path in GLYPHS[char]:
            curve=[(origin+u*advance*.78,-.0275+v*height) for u,v in path]
            stroke(door,curve,.00016,lambda u,v:point(u,v,.7818),'black',normal)
