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

        incident_ray_partial = Arrow(
            start=[-3, 0, 0],
            end=[0, 0, 0],
            buff=0,
            color=BLUE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.0,
        )
        incident_ray_continuation = Arrow(
            start=[0, 0, 0],
            end=[3, 0, 0],
            buff=0,
            color=BLUE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.025,
        )
        scattered_ray_top = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],  # Top edge of aperture entrance
            buff=0,
            color=RED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.025,
        )
        scattered_ray_bottom = Arrow(
            start=[0, 0, 0],
            end=[3, -1, 0],  # Bottom edge of aperture entrance
            buff=0,
            color=RED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.025,
        )

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

        # Timing setup
        total_animation_time = 2.0
        time_to_specimen = total_animation_time / 2
        time_to_aperture = total_animation_time / 2

        # Animate incident ray up to specimen plane
        self.play(
            Create(incident_ray_partial),
            run_time=time_to_specimen,
            rate_func=linear
        )

        # Animate all three rays simultaneously to the aperture
        self.play(
            Create(incident_ray_continuation),
            Create(scattered_ray_top),
            Create(scattered_ray_bottom),
            run_time=time_to_aperture,
            rate_func=linear
        )

        self.wait(10)
