from manim import *

class GeneratedScene(Scene):
    def construct(self):
        line = Line(start=LEFT, end=RIGHT)
        self.play(Create(line))
        self.wait(1)

        self.play(Rotate(line, angle=PI, about_point=ORIGIN, run_time=3))
        self.wait(1)

        self.play(Rotate(line, angle=PI, about_point=ORIGIN, run_time=3))
        self.wait(1)