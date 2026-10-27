"""Original upper rear-wheelhouse/cargo returns. Hidden dimensions are inferred."""
import math

def build_cargo_returns(part, rear, front, side_x):
    # Closed 8mm shells bridge the former unlined tire-shoulder sightline.
    # Existing cargo sidewalls remain their inboard support.
    stations=[rear+(front-rear)*i/24 for i in range(25)]
    for side in (-1,1):
        grid=[]
        for y in stations:
            crown=.720+.035*math.exp(-((y+1.36)/.34)**2)
            outer=side_x(y,crown)-.004
            grid.append([(side*(.590+(outer-.590)*t),y,.707+(crown-.707)*math.sin(t*math.pi/2)) for t in (0,.25,.5,.75,1)])
        lower=lambda p:(p[0],p[1],p[2]-.008)
        for a,b in zip(grid,grid[1:]):
            for i in range(4):
                points=[a[i],a[i+1],b[i+1],b[i]]
                if side<0:points.reverse()
                part.face(points,'black')
                part.face([lower(p) for p in reversed(points)],'black')
        perimeter=grid[0][:]+[row[-1] for row in grid[1:]]+list(reversed(grid[-1][:-1]))+[row[0] for row in reversed(grid[1:-1])]
        if side<0:perimeter.reverse()
        for a,b in zip(perimeter,perimeter[1:]+perimeter[:1]):
            part.face([a,lower(a),lower(b),b],'black')
