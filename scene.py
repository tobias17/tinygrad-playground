from manim import Scene, Square, VGroup, ManimColor # type: ignore
import functools, operator
from typing import List, Tuple, Iterable, Union, TypeVar

DEFAULT_VIEW_HEIGHT = 3.0
DEFAULT_VIEW_WIDTH  = 6.0

BLUE = (31,119,180)

T = TypeVar("T")
def prod(x:Iterable[T]) -> Union[T,int]: return functools.reduce(operator.mul, x, 1)

class TensorView:
    def __init__(self, *shape, color:Tuple[int,int,int]=BLUE, min_c:float=0.3, max_c:float=0.7):
        self.shape = shape
        def lerp_color(n, N) -> ManimColor:
            def l(v): return int(v * (min_c + (n/N * (max_c - min_c))))
            return ManimColor(f"#{l(color[0]):02X}{l(color[1]):02X}{l(color[2]):02X}")
        assert len(shape) > 0 and len(shape) < 3, f"Can only view 1D and 2D shapes, found {len(shape)}D shape"
        sz = prod(shape)
        if len(shape) == 1: shape = (shape[0],1)
        self.grid = VGroup(*[Square(fill_color=lerp_color(i, sz), fill_opacity=1).move_to([(i % shape[1])*2 - shape[1] + 1, ((i // shape[1])*2 - shape[0] + 1) * -1, 0]) for i in range(sz)])

class CreateGrid(Scene):
    def construct(self):
        w, h = 10, 5

        # r, g, b = 31, 119, 180
        # min_p, max_p = 0.3, 0.7
        # def lerp_color(n, N) -> ManimColor:
        #     def l(v): return int(v * (min_p + (n/N * (max_p - min_p))))
        #     return ManimColor(f"#{l(r):02X}{l(g):02X}{l(b):02X}")

        # squares = VGroup(*[Square(fill_color=lerp_color(i, w*h), fill_opacity=1) for i in range(w * h)])
        # grid = VGroup(*[squares[i].move_to([(i % w)*2 - w + 1, ((i // w)*2 - h + 1) * -1, 0]) for i in range(w * h)])
        # self.add(grid)
        # self.camera.frame_width *= 1
        # self.camera.frame_height *= 1
        # self.camera.background_color = ManimColor("#FFFFFF")

        tv = TensorView(5, 10)
        self.add(tv.grid)
        self.camera.frame_width *= 2
        self.camera.frame_height *= 2

        self.wait()
