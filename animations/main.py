from manim import *


class MicroscopeObjective(Scene):
    def construct(self):
        title = Text("Ewald Sphere", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        objective_housing = Polygram(
            [[10, 3, 0], [5, 3, 0], [3, 1, 0], [3, -1, 0], [5, -3, 0], [10, -3, 0]],
            fill_color=DARK_GRAY,
            fill_opacity=0.8,
            stroke_color=GRAY,
            stroke_width=2
        )

        specimen_line = DashedLine(
            start=[0, -3, 0],
            end=[0, 3, 0],
            color=YELLOW,
            stroke_width=2
        )
        specimen_label = Text("Specimen", font_size=20, color=YELLOW)
        specimen_label.next_to(specimen_line, DOWN)

        self.play(
            Create(objective_housing),
            run_time=0.5,
        )
        self.wait()

        self.play(
            Create(specimen_line),
            Write(specimen_label),
            run_time=0.5
        )

        self.wait(10)
