from manim import Scene, Square, VGroup, ManimColor, Animation, LEFT # type: ignore
import sys, os
from typing import List, Tuple, Iterable, Union, TypeVar, Callable

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tinygrad"))
from tinygrad import Tensor
from tinygrad.helpers import prod

ANIM_DELTA = 0.1

BLUE   = (0x1f, 0x77, 0xb4)
ORANGE = (0xff, 0x7f, 0x0e)
GREEN  = (0x2c, 0xa0, 0x2c)

T = TypeVar("T")

class TensorView:
    def __init__(self, *shape, color:Tuple[int,int,int]=BLUE, min_c:float=0.1, max_c:float=0.9, opacity:float=1.0):
        self.shape = shape
        def lerp_color(n, N) -> ManimColor:
            def l(v): return int(v * (0.2+0.8*n/N) + 127 * (0.8 - 0.8*n/N))
            return ManimColor(f"#{l(color[0]):02X}{l(color[1]):02X}{l(color[2]):02X}")
        assert len(shape) > 0 and len(shape) < 3, f"Can only view 1D and 2D shapes, found {len(shape)}D shape"
        if len(shape) == 1: shape = (shape[0],1)
        w, h = self.shape[0], (self.shape[1] if len(self.shape) > 1 else 1)
        self.grid = VGroup(VGroup(*[Square(fill_color=lerp_color(i, prod(shape)), fill_opacity=opacity) for i in range(prod(shape))], Square(stroke_opacity=0.0).scale(0.7)))
        for x in range(w):
            for y in range(h):
                self.grid[0][x+y*w].move_to([x, y, 0]).scale(0.5)
        self.grid[0].move_to([-w, -h, 0]).scale(1 / max(w, h)).flip(LEFT)
    
    def indicator_opacity_anim(self, opacity:float) -> Animation:
        return self.grid[0][-1].animate.set_stroke(opacity=opacity)

    def indicator_move_anim(self, x:int, y:int) -> Animation:
        index = (x if self.shape[0] > 1 else 0) + (y * self.shape[0] if len(self.shape) > 1 and self.shape[1] > 1 else 0)
        return self.grid[0][-1].animate.move_to(self.grid[0][index].get_center())

def elementwise(scene:Scene, a:TensorView, b:TensorView):
    assert len(a.shape) == len(b.shape) and len(a.shape) >= 1 and len(a.shape) <= 2
    assert all(sa==sb or sa==1 or sb==1 for sa, sb in zip(a.shape, b.shape))
    assert all(s > 0 for s in a.shape)

    c = TensorView(*[max(sa, sb) for sa, sb in zip(a.shape, b.shape)], color=GREEN, opacity=0.0)
    c.grid.move_to([0, -2.0, 0]).scale(5)
    scene.add(c.grid)

    w, h = c.shape[0], c.shape[1] if len(c.shape) > 1 else 1

    def apply_all(func:Callable[[TensorView],T]) -> List[T]:
        return [func(a), func(b), func(c)]

    scene.play(*apply_all(lambda tv: tv.indicator_opacity_anim(1.0)), run_time=0.5)
    for y in range(h):
        for x in range(w):
            c.grid[0][x+y*w].set_fill(opacity=-x)
        scene.play(*[c.grid[0][y*w+i].animate.set_fill(opacity=w-i) for i in range(w)], *apply_all(lambda tv: tv.indicator_move_anim(w-1, y)), run_time=ANIM_DELTA*w)
        if y+1 < h:
            scene.play(*apply_all(lambda tv: tv.indicator_move_anim(0, y+1)), run_time=ANIM_DELTA*2.0)
            scene.wait(ANIM_DELTA)
    scene.play(*apply_all(lambda tv: tv.indicator_opacity_anim(0.0)), run_time=0.5)
    scene.wait()

class CreateGrid(Scene):
    def construct(self):

        tv_1 = TensorView(10, 5)
        tv_1.grid.move_to([-3.5, 2.0, 0]).scale(5)
        self.add(tv_1.grid)

        tv_2 = TensorView(10, 1, color=ORANGE)
        tv_2.grid.move_to([ 3.5, 2.0, 0]).scale(5)
        self.add(tv_2.grid)

        elementwise(self, tv_1, tv_2)
