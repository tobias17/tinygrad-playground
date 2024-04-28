from manim import Scene, Square, VGroup, ManimColor, FadeIn # type: ignore
import functools, operator
from typing import List, Tuple, Iterable, Union, TypeVar

DEFAULT_VIEW_HEIGHT = 3.0
DEFAULT_VIEW_WIDTH  = 6.0

BLUE   = (0x1f, 0x77, 0xb4)
ORANGE = (0xff, 0x7f, 0x0e)
GREEN  = (0x2c, 0xa0, 0x2c)

T = TypeVar("T")
def prod(x:Iterable[T]) -> Union[T,int]: return functools.reduce(operator.mul, x, 1)

class TensorView:
    def __init__(self, *shape, color:Tuple[int,int,int]=BLUE, min_c:float=0.1, max_c:float=0.9, opacity:float=1.0):
        self.shape = shape
        def lerp_color(n, N) -> ManimColor:
            def l(v): return int(v * (min_c + (n/N * (max_c - min_c))))
            return ManimColor(f"#{l(color[0]):02X}{l(color[1]):02X}{l(color[2]):02X}")
        assert len(shape) > 0 and len(shape) < 3, f"Can only view 1D and 2D shapes, found {len(shape)}D shape"
        if len(shape) == 1: shape = (shape[0],1)
        w, h = self.shape[0], (self.shape[1] if len(self.shape) > 1 else 1)
        self.grid = VGroup(VGroup(*[Square(fill_color=lerp_color(i, prod(shape)), fill_opacity=opacity) for i in range(prod(shape))]))
        for x in range(w):
            for y in range(h):
                i = x + y * w
                self.grid[0][i].move_to([(-w/2.0) + x + 0.5, (h/2.0) - y - 0.5, 0]).scale(0.5)
        self.grid[0].scale(1 / max(w, h))

class CreateGrid(Scene):
    def construct(self):

        tv_1 = TensorView(10, 5)
        tv_1.grid.move_to([-3.5, 2.0, 0]).scale(5)
        self.add(tv_1.grid)

        tv_2 = TensorView(10, 5, color=ORANGE)
        tv_2.grid.move_to([ 3.5, 2.0, 0]).scale(5)
        self.add(tv_2.grid)

        tv_3 = TensorView(10, 5, color=GREEN, opacity=0.0)
        tv_3.grid.move_to([0, -2.0, 0]).scale(5)
        self.add(tv_3.grid)

        self.wait()
        for i in range(10*5):
            self.play(tv_3.grid[0][i].animate.set_fill(opacity=1.0), run_time=0.1)
        self.wait()
