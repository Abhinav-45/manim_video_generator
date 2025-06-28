from manim import *

class GeneratedScene(Scene):
    def construct(self):
        square = Square(side_length=2, color=BLUE)
        self.play(Create(square))

        side1_text = Tex("Side 1").next_to(square, DOWN)
        side2_text = Tex("Side 2").next_to(square, LEFT)
        side3_text = Tex("Side 3").next_to(square, UP)
        side4_text = Tex("Side 4").next_to(square, RIGHT)

        self.play(Write(side1_text), Write(side2_text), Write(side3_text), Write(side4_text))

        point = Dot(square.get_center(), color=RED)
        self.play(Create(point))

        self.wait(2)

        self.play(
            Transform(point, square),
            FadeOut(side1_text, side2_text, side3_text, side4_text)
        )

        self.wait(2)

        self.play(
            Transform(square, point),
            FadeOut(point)
        )
        self.wait(1)