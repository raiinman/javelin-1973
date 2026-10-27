"""Exercise the generator's sail function without importing Blender or building assets."""
import ast
import math
from pathlib import Path
import unittest


def load_sail(side):
    from test_body_sections import load_profiles
    source = Path(__file__).with_name('build_mod.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    function = next(node for node in ast.walk(tree)
                    if isinstance(node, ast.FunctionDef) and node.name == 'sail')
    scope=load_profiles()
    scope['side']=side
    edge_function=next(node for node in ast.walk(tree)
                       if isinstance(node,ast.FunctionDef) and node.name=='sail_edge')
    module=ast.fix_missing_locations(ast.Module(body=[edge_function,function],type_ignores=[]))
    exec(compile(module,'actual_sail_surfaces','exec'),scope)
    edge=scope['sail_edge']
    tip_y=scope['QUARTER_TIP']
    upper,lower=edge(tip_y,True),edge(tip_y,False)
    tip=scope['quarter_glass_point'](side,tip_y,1.025)
    tip_t = (upper[2]-tip[2])/(upper[2]-lower[2])
    return scope['sail'], edge, upper, lower, tip, tip_t


class SailSurfaceTests(unittest.TestCase):
    def assert_point(self, actual, expected):
        for actual_coordinate, expected_coordinate in zip(actual, expected):
            self.assertAlmostEqual(actual_coordinate, expected_coordinate, places=10)

    def test_top_and_bottom_follow_local_edges_through_blend(self):
        for side in (-1, 1):
            sail, edge, *_ = load_sail(side)
            for y in (-.85, -.95, -1.08, -1.13, -1.22, -1.35, -1.52, -1.87):
                for t, top in ((0, True), (1, False)):
                    with self.subTest(side=side, y=y, t=t):
                        self.assert_point(sail(y, t), edge(y, top))

    def test_quarter_window_tip_anchors_and_smooth_boundary(self):
        for side in (-1, 1):
            sail, _, upper, lower, tip, tip_t = load_sail(side)
            for t,expected in ((0,upper),(tip_t,tip),(1,lower)):
                with self.subTest(side=side, t=t):
                    self.assert_point(sail(tip[1], t), expected)
            e=.000001
            left=(sail(tip[1],tip_t)[0]-sail(tip[1],tip_t-e)[0])/e
            right=(sail(tip[1],tip_t+e)[0]-sail(tip[1],tip_t)[0])/e
            self.assertAlmostEqual(left,right,places=4)

    def test_lower_surface_is_tangent_to_side_skin(self):
        from test_body_sections import load_profiles
        profile=load_profiles()
        for side in (-1, 1):
            sail, edge, *_ = load_sail(side)
            for y in (-.95,-1.13,-1.35,-1.52,-1.72,-1.87):
                upper, lower = edge(y, True), edge(y, False)
                e=.000001
                point=sail(y,1-e)
                actual=(point[0]-lower[0])/(point[2]-lower[2])
                expected=side*(profile['side_x'](y,lower[2]+e)-profile['side_x'](y,lower[2]-e))/(2*e)
                with self.subTest(side=side,y=y):
                    self.assertAlmostEqual(actual,expected,places=4)


class BacklightApronTests(unittest.TestCase):
    def test_apron_follows_every_curved_lower_glass_column(self):
        source = Path(__file__).with_name('build_mod.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        screen = next(node for node in ast.walk(tree)
                      if isinstance(node, ast.FunctionDef) and node.name == 'rear_screen')
        start=next(i for i,node in enumerate(tree.body) if isinstance(node,ast.Assign)
                   and any(isinstance(t,ast.Name) and t.id=='apron_x' for t in node.targets))
        end=next(i for i,node in enumerate(tree.body) if isinstance(node,ast.For)
                 and 'apron_edge' in ast.unparse(node.iter))
        faces = []

        class Capture:
            def face(self, vertices, colour, **kwargs):
                if colour=='red':faces.append(vertices)

        columns = (-.66, -.50, -.28, 0, .28, .50, .66)
        from test_body_sections import load_profiles
        scope = load_profiles()
        scope.update(body=Capture(), rear_x=columns, samples=(-1.87,-1.80,-1.72))
        module = ast.fix_missing_locations(ast.Module(body=[screen]+tree.body[start:end+1], type_ignores=[]))
        exec(compile(module, 'backlight_apron_from_generator', 'exec'), scope)
        points = [point for face in faces for point in face]
        for x in columns:
            expected = scope['rear_screen'](x, 0)
            distance = min(math.dist(expected, point) for point in points)
            with self.subTest(column=x):
                self.assertLess(distance, 1e-10)
        for x in (-.838, .838):
            self.assertLess(min(math.dist((x,-1.72,.965),p) for p in points),1e-10)
        for x in (-.85,.85):
            self.assertLess(min(math.dist((x,-1.87,.940),p) for p in points),1e-10)


if __name__ == '__main__':
    unittest.main()
