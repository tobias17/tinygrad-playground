from manim import Scene, Square, VGroup, ManimColor # type: ignore
from typing import List, Tuple

class CreateGrid(Scene):
    def construct(self):
        w, h = 10, 5

        r, g, b = 31, 119, 180
        min_p, max_p = 0.3, 0.7
        def lerp_color(n, N) -> ManimColor:
            def l(v): return int(v * (min_p + (n/N * (max_p - min_p))))
            return ManimColor(f"#{l(r):02X}{l(g):02X}{l(b):02X}")

        squares = VGroup(*[Square(fill_color=lerp_color(i, w*h), fill_opacity=1) for i in range(w * h)])
        grid = VGroup(*[squares[i].move_to([(i % w)*2 - w + 1, ((i // w)*2 - h + 1) * -1, 0]) for i in range(w * h)])
        self.add(grid)
        self.camera.frame_width *= 2.0
        self.camera.frame_height *= 2.0

        self.wait()
