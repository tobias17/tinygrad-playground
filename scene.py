from manim import * # type: ignored

class CreateGrid(Scene):
    def construct(self):
        w, h = 10, 5

        squares = VGroup(*[Square() for _ in range(w * h)])
        grid = VGroup(*[squares[i].move_to([(i % w) - (w / 2.0) + 0.5, (i // w) - (h / 2.0) + 0.5, 0]) for i in range(w * h)])
        self.add(grid)
        self.wait()
