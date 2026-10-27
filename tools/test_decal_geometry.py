"""Regression for near-collinear fine-border ears observed in saved Blender."""
import unittest
from javelin_decals import clean_decal_outline, _triangulate_outline, _triangle_clip

class DecalContourTests(unittest.TestCase):
    def test_saved_sliver_is_rejected_before_tessellation(self):
        # Actual saved ear:65.18mm longest edge,43.95nm minimum altitude.
        points=[(.7906378507614136,2.044863700866699,.22122332453727722),
                (.7989526987075806,1.99167001247406,.23384778201580048),
                (.7891519665718079,2.0543692111968994,.21896737813949585)]
        self.assertEqual(clean_decal_outline(points),[])

    def test_straight_edge_knot_does_not_change_boundary(self):
        outline=[(0,0,0),(.05,.0000001,0),(.1,0,0),(.1,.005,0),(0,.005,0)]
        self.assertEqual(clean_decal_outline(outline),[(0,0,0),(.1,0,0),(.1,.005,0),(0,.005,0)])

    def test_real_five_millimetre_point_is_preserved(self):
        outline=[(0,0,0),(.03,-.005,0),(.1,0,0),(.1,.005,0),(0,.005,0)]
        self.assertEqual(clean_decal_outline(outline),outline)

class ArtworkTriangulationTests(unittest.TestCase):
    def test_concave_notch_remains_empty_after_clipping(self):
        outline=[(0,0),(3,0),(3,3),(2,3),(2,1),(1,1),(1,3),(0,3)]
        triangles=_triangulate_outline(outline)
        self.assertEqual(len(triangles),len(outline)-2)
        area=sum(abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(t,t[1:]+t[:1])))/2 for t in triangles)
        self.assertAlmostEqual(area,7)
        clip=[(0,2),(3,2),(1.5,4)]
        for triangle in triangles:
            polygon=_triangle_clip(triangle,clip)
            if len(polygon)<3:continue
            x=sum(v[0] for v in polygon)/len(polygon)
            y=sum(v[1] for v in polygon)/len(polygon)
            self.assertFalse(1<x<2 and y>1,'Clipping must not bridge the empty concave notch')

    def test_reversed_winding_has_same_coverage(self):
        outline=[(0,0),(2,0),(2,2),(1,1),(0,2)]
        for contour in (outline,list(reversed(outline))):
            triangles=_triangulate_outline(contour)
            area=sum(abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(t,t[1:]+t[:1])))/2 for t in triangles)
            self.assertAlmostEqual(area,3)
