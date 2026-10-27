"""Check authored surface joins without building or importing Blender."""
import ast
import math
from pathlib import Path
import unittest


def load_profiles():
    tree=ast.parse(Path(__file__).with_name('build_mod.py').read_text(encoding='utf-8'))
    wanted={'width','shoulder','side_top','side_x','hood_base','front_fender_point',
            'monotone_profile','roof_point','rear_roof_edge','upper_sail_x',
            'door_edge_y','body_side_point','rear_quarter_surface','quarter_glass_point'}
    from javelin_nose import terminal_wing_point,terminal_side_point
    from javelin_fender_artist import artist_point
    scope={'artist_point':artist_point,'terminal_wing_point':terminal_wing_point,'terminal_side_point':terminal_side_point,'math':math,'ROOF_REAR':-.80,'TRUNK_RUN':.31092,
           'DOOR_REAR':-.434,'DOOR_FRONT':.784,'DOOR_BOTTOM':.286,
           'GLASS_BELT':.900,'QUARTER_TIP':-.95}
    functions=[node for node in tree.body
               if isinstance(node,ast.FunctionDef) and node.name in wanted]
    exec(compile(ast.fix_missing_locations(ast.Module(body=functions,type_ignores=[])),
                 'body_profiles','exec'),scope)
    return scope


class FrontSectionTests(unittest.TestCase):
    def test_join_positions_and_side_tangent(self):
        p=load_profiles()
        for y in (.79,.94,1.23,1.43,1.78,2.10,2.34):
            z=p['side_top'](y)
            outer=p['front_fender_point'](1,y,0)
            inner=p['front_fender_point'](1,y,1)
            self.assertAlmostEqual(outer[0],p['side_x'](y,z))
            self.assertAlmostEqual(outer[2],z)
            self.assertAlmostEqual(inner[0],.706)
            self.assertAlmostEqual(inner[2],p['hood_base'](y))
            near=p['front_fender_point'](1,y,.00001)
            tangent=(near[0]-outer[0])/(near[2]-outer[2])
            wall=(p['side_x'](y,z+.0001)-p['side_x'](y,z-.0001))/.0002
            self.assertAlmostEqual(tangent,wall,places=3)

        from javelin_front import front_upper_point
        for side in (-1,1):
            for y in (2.35,2.37,2.39):
                outer=p['front_fender_point'](side,y,0)
                wall=p['body_side_point'](side,y,p['side_top'](y))
                for a,b in zip(outer,wall):self.assertAlmostEqual(a,b)
            for t in (0,.25,.5,.75,1):
                tip=p['front_fender_point'](side,2.39,t)
                expected=front_upper_point(abs(tip[0]))
                self.assertAlmostEqual(tip[1],expected[1])
                self.assertAlmostEqual(tip[2],expected[2])
                before=p['front_fender_point'](side,2.39-.000001,t)
                self.assertLess(abs(tip[1]-before[1]),abs(tip[2]-before[2])*.01)
                join=p['front_fender_point'](side,2.34,t)
                left=p['front_fender_point'](side,2.34-.000001,t)
                right=p['front_fender_point'](side,2.34+.000001,t)
                self.assertAlmostEqual((join[2]-left[2])/(join[1]-left[1]),
                                       (right[2]-join[2])/(right[1]-join[1]),places=3)

    def test_crown_is_mirrored_and_has_a_rounded_peak(self):
        p=load_profiles()
        for y in (.94,1.43,1.78,2.10):
            points=[p['front_fender_point'](1,y,i/100) for i in range(101)]
            self.assertTrue(all(a[0]>b[0] for a,b in zip(points,points[1:])))
            self.assertGreater(max(v[2] for v in points),points[0][2]+.001)
            for i,point in enumerate(points):
                opposite=p['front_fender_point'](-1,y,i/100)
                self.assertAlmostEqual(point[0],-opposite[0])
                self.assertEqual(point[1:],opposite[1:])

    def test_outer_roll_does_not_dip_before_rising_to_crown(self):
        # A visually rejected two-arc trial folded down immediately above the
        # side join at Y1.0..1.14 and2.1 despite passing endpoint/tangent tests.
        p=load_profiles()
        for side in (-1,1):
            for step in range(151):
                y=.80+step*.01
                points=[p['front_fender_point'](side,y,i/1000) for i in range(81)]
                self.assertTrue(all(b[2]>=a[2]-1e-9 for a,b in zip(points,points[1:])),
                                f'Outer roll folds down before the crown at side{side} Y{y:.2f}')

    def test_crown_roll_is_shallow_and_endpoints_meet_side_skin(self):
        p=load_profiles()
        for y in (1.10,1.23,1.43,1.60,1.78):
            points=[p['front_fender_point'](1,y,i/100) for i in range(101)]
            self.assertLess(max(v[2] for v in points)-points[-1][2],.060,
                            'Front wing must not become a tall rail above its hood edge')
        for y in (.79,2.39):
            self.assertAlmostEqual(p['side_top'](y),p['shoulder'](y))


class RearSectionTests(unittest.TestCase):
    def test_roof_profile_keeps_stations_and_monotonicity(self):
        p=load_profiles()
        # Revised roof/sail landmarks retain the roof lip and deck joins,
        # with a fuller upper transition from the supplemental profile views.
        for y,z in ((-.95,1.222),(-1.13,1.170),(-1.35,1.095),
                    (-1.52,1.030),(-1.72,.965),(-1.87,.940)):
            self.assertAlmostEqual(p['rear_roof_edge'](y),z)
        values=[p['rear_roof_edge'](-.8-i*1.07/1000) for i in range(1001)]
        self.assertTrue(all(a>=b for a,b in zip(values,values[1:])))

    def test_fastback_tangents_are_continuous(self):
        p=load_profiles()
        f=p['rear_roof_edge']
        e=.000001
        roof_tangent=(p['roof_point'](.70,-.8+e)[2]-p['roof_point'](.70,-.8)[2])/e
        self.assertAlmostEqual((f(-.8)-f(-.8-e))/e,roof_tangent,places=4)
        for y in (-.95,-1.13,-1.35,-1.52,-1.72):
            self.assertAlmostEqual((f(y+e)-f(y))/e,(f(y)-f(y-e))/e,places=4)
        self.assertAlmostEqual(p['upper_sail_x'](-1.72),.838)
        self.assertAlmostEqual(p['upper_sail_x'](-1.87),.850)
        self.assertAlmostEqual((p['upper_sail_x'](-.8-e)-.7)/e,0,places=4)


class SideSectionTests(unittest.TestCase):
    def test_curved_door_keeps_six_mm_body_seams(self):
        p=load_profiles()
        for side in (-1,1):
            for z in (.286,.37,.50,.69,.81,.86,.90):
                self.assertAlmostEqual(p['body_side_point'](side,.79,z)[1]-p['door_edge_y'](z,True),.006)
                self.assertAlmostEqual(p['door_edge_y'](z,False)-p['body_side_point'](side,-.44,z)[1],.006)
        self.assertLess(p['door_edge_y'](.286,True),p['door_edge_y'](.90,True)-.05)

    def test_pressed_character_line_has_local_volume(self):
        p=load_profiles()
        center=p['side_x'](0,.690)
        chord=(p['side_x'](0,.655)+p['side_x'](0,.725))/2
        self.assertGreater(center-chord,.0035)


if __name__=='__main__':
    unittest.main()
