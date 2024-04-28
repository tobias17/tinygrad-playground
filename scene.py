from manim import Scene, Square, VGroup, ManimColor # type: ignore
import functools, operator
from typing import List, Tuple, Iterable, Union, TypeVar, Optional, Iterator

DEFAULT_VIEW_HEIGHT = 3.0
DEFAULT_VIEW_WIDTH  = 6.0

BLUE = (31,119,180)

T = TypeVar("T")
def prod(x:Iterable[T]) -> Union[T,int]: return functools.reduce(operator.mul, x, 1)

class TensorView:
    def __init__(self, *shape, color:Tuple[int,int,int]=BLUE, min_c:float=0.1, max_c:float=0.9):
        self.shape = shape
        def lerp_color(n, N) -> ManimColor:
            def l(v): return int(v * (min_c + (n/N * (max_c - min_c))))
            return ManimColor(f"#{l(color[0]):02X}{l(color[1]):02X}{l(color[2]):02X}")
        assert len(shape) > 0 and len(shape) < 3, f"Can only view 1D and 2D shapes, found {len(shape)}D shape"
        if len(shape) == 1: shape = (shape[0],1)
        self.grid = VGroup(*[Square(fill_color=lerp_color(i, prod(shape)), fill_opacity=1) for i in range(prod(shape))])

    def box(self, box_x:float, box_y:float, box_w:float, box_h:float) -> 'TensorView':
        grid_w, grid_h = self.shape[0], (self.shape[1] if len(self.shape) > 1 else 1)
        side = min(box_w / grid_w, box_h / grid_h)
        print(box_w / grid_w, box_h / grid_h)
        center_x, center_y = box_x + (box_w/2.0), box_y + (box_h/2.0)
        print(center_x, center_y)
        origin_x, origin_y = center_x - (grid_w / 2.0 * side), center_y - (grid_h / 2.0 * side)
        print(origin_x, origin_y)
        for grid_x in range(grid_w):
            for grid_y in range(grid_h):
                i = grid_x + grid_y * grid_w
                self.grid[i].move_to([origin_x + (grid_x * side) + side/2.0, origin_y + ((grid_h - grid_y) * side) - side/2.0, 0]).scale(side / 2.0)
        return self

class CreateGrid(Scene):
    def construct(self):

        tv = TensorView(10, 5).box(-6, -3, 12, 6)
        self.add(tv.grid)

        self.wait()
