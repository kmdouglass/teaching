from manim import *
import numpy as np
import numpy.typing as npt


OBJ_BARREL_HEIGHT = 1.0  # Height of the objective barrel
OBJ_FOCAL_LENGTH = 4.0  # Focal length of the objective lens
OBJ_WORKING_DISTANCE = 3.0  # Working distance of the objective lens
OBJ_COLLECTION_ANGLE = 2 * np.atan2(OBJ_BARREL_HEIGHT, OBJ_WORKING_DISTANCE)


def vector_length_and_dir_to_coords(
    vec: npt.NDArray[np.float64],
    origin: npt.NDArray[np.float64],
    length: float
    ) -> npt.NDArray[np.float64]:
    direction = vec / np.linalg.norm(vec)
    return origin + direction * length


def reciprocal_lattice_vector(
    k_inc: npt.NDArray[np.float64],
    k_scat: npt.NDArray[np.float64]
) -> npt.NDArray[np.float64]:
    origin = k_inc
    return k_scat - k_inc + origin


def ewald_circle_group() -> VGroup:
    circ = Circle(radius=OBJ_FOCAL_LENGTH, color=GREEN, stroke_width=3)
    k_inc = Arrow(
        start=[0, 0, 0],
        end=[OBJ_FOCAL_LENGTH, 0, 0],
        buff=0,
        color=GREEN,
        stroke_width=2,
        max_tip_length_to_length_ratio=0.025,
    )

    scattered_wave_vector = vector_length_and_dir_to_coords(
        np.array([3, 1, 0]),
        np.array([0, 0, 0]),
        OBJ_FOCAL_LENGTH
    )
    k_scat = Arrow(
        start=[0, 0, 0],
        end=scattered_wave_vector,
        buff=0,
        color=GREEN,
        stroke_width=2,
        max_tip_length_to_length_ratio=0.025,
    )

    na_limits = Arc(
        radius=OBJ_FOCAL_LENGTH,
        start_angle=-OBJ_COLLECTION_ANGLE / 2,
        angle=OBJ_COLLECTION_ANGLE,
        color=YELLOW,
        stroke_width=5,
    )

    vg_ewald_circle = VGroup(circ, k_inc, k_scat, na_limits)
    return vg_ewald_circle


class MicroscopeObjective(Scene):
    def construct(self):
        title = Text("The 3D Aperture", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))
        
        objective_housing = Polygram(
            [[10, 3, 0], [5, 3, 0], [3, 1, 0], [3, -1, 0], [5, -3, 0], [10, -3, 0]],
            fill_color=DARK_GRAY,
            fill_opacity=0.8,
            stroke_color=GRAY,
            stroke_width=2
        )
        
        # Principal surface - arc centered at origin
        principal_surface = Arc(
            radius=OBJ_FOCAL_LENGTH,
            start_angle=-OBJ_COLLECTION_ANGLE / 2,
            angle=OBJ_COLLECTION_ANGLE,
            color=BLUE,
            stroke_width=3
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
            end=[OBJ_FOCAL_LENGTH, 0, 0],
            buff=0,
            color=BLUE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.025,
        )

        scattered_wave_vector_top = vector_length_and_dir_to_coords(
            np.array([3, 1, 0]),
            np.array([0, 0, 0]),
            OBJ_FOCAL_LENGTH
        )
        scattered_wave_vector_bottom = vector_length_and_dir_to_coords(
            np.array([3, -1, 0]),
            np.array([0, 0, 0]),
            OBJ_FOCAL_LENGTH
        )
        scattered_ray_top = Arrow(
            start=[0, 0, 0],
            end=scattered_wave_vector_top,  # Top edge of aperture entrance
            buff=0,
            color=RED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.025,
        )
        scattered_ray_bottom = Arrow(
            start=[0, 0, 0],
            end=scattered_wave_vector_bottom,  # Bottom edge of aperture entrance
            buff=0,
            color=RED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.025,
        )

        vg_microscope = VGroup(
            objective_housing,
            principal_surface,
            specimen_line,
            specimen_label,
            incident_ray_partial,
            incident_ray_continuation,
            scattered_ray_top,
            scattered_ray_bottom
        )

        self.play(
            Create(objective_housing),
            Create(principal_surface),
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

        vg_ewald = ewald_circle_group()
        ewald_circle, k_inc, k_scat, na_limits = vg_ewald
        self.play(
            FadeOut(vg_microscope),
            FadeIn(vg_ewald),
            run_time=2.0,
        )

        k_inc_label = MathTex(r"\vec{k}_{inc}", font_size=36, color=GREEN)
        k_inc_label.next_to(k_inc.get_end(), DOWN - RIGHT * 1.0)

        k_scat_label = MathTex(r"\vec{k}_{sca}", font_size=36, color=GREEN)
        k_scat_label.next_to(k_scat.get_end(), UP - RIGHT * 1.0)

        self.play(
            Write(k_inc_label),
            Write(k_scat_label),
        )
        self.wait(1)
        self.play(
            FadeOut(k_inc_label),
            FadeOut(k_scat_label),
        )

        self.play(
            Rotate(k_scat, angle=-OBJ_COLLECTION_ANGLE, about_point=[0, 0, 0]),
        )
        self.wait(1)
        self.play(
            Rotate(k_scat, angle=OBJ_COLLECTION_ANGLE, about_point=[0, 0, 0]),
        )
        self.wait(1)

        # Try to pass the NA limits but fail
        bump = 1 * DEGREES
        self.play(
            Rotate(k_scat, angle=-bump, about_point=[0, 0, 0]),
            run_time=0.3,
        )
        self.play(
            Rotate(k_scat, angle=bump, about_point=[0, 0, 0]),
            run_time=0.3,
        )
        self.play(
            Rotate(k_scat, angle=-bump, about_point=[0, 0, 0]),
            run_time=0.2,
        )
        self.play(
            Rotate(k_scat, angle=bump, about_point=[0, 0, 0]),
            run_time=0.2,
        )

        G = Arrow(
            start=k_inc.get_end(),
            end = reciprocal_lattice_vector(k_inc.get_end(), k_scat.get_end()),
            buff=0,
            color=PURPLE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.1,
        )
        G_label = MathTex(r"\vec{G}", font_size=36, color=PURPLE)
        G_label.next_to(G.get_center(), UP + RIGHT * 1.0)

        # Pin G to the end of k_scat
        def update_G(m):
            new_G = Arrow(
                start=k_inc.get_end(),
                end=k_scat.get_end(),
                buff=0,
                color=PURPLE,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.1,
            )
            m.become(new_G)
        G.add_updater(update_G)

        self.play(
            Create(G),
            Write(G_label),
            run_time=2.0
        )
        self.wait(1)
        self.play(
            FadeOut(G_label),
        )

        # Rotate k_scat and show how G changes
        self.play(
            Rotate(k_scat, angle=-OBJ_COLLECTION_ANGLE, about_point=[0, 0, 0]),
            rate_func=linear,
        )
        self.wait(1)
        self.play(
            Rotate(k_scat, angle=OBJ_COLLECTION_ANGLE, about_point=[0, 0, 0]),
            rate_func=linear,
        )


        #--------------------------------
        # Scale the scene to make room for the plot
        self.play(
            vg_ewald.animate.scale(0.5).shift(LEFT * 3.5),
            G.animate.scale(0.5).shift(LEFT * 3.5),
            run_time=1.5
        )

        # Create axes for the G vector plot on the right side
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=4,
            axis_config={"color": WHITE, "include_tip": False},
            tips=False,
        )
        axes.shift(RIGHT * 3.5)

        # Create grid
        grid = NumberPlane(
            x_range=[-1, 4, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=4,
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            }
        )
        grid.shift(RIGHT * 3.5)

        # Add axes labels
        x_label = MathTex("G_z", font_size=28).next_to(axes.x_axis, RIGHT)
        y_label = MathTex("G_x", font_size=28).next_to(axes.y_axis, UP)

        self.play(
            Create(grid),
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=1
        )

        # Create a dot that tracks the G vector endpoint
        def get_G_vector():
            return k_scat.get_end() - k_inc.get_end()

        G_dot = Dot(color=PURPLE, radius=0.04)
        G_dot.move_to(axes.coords_to_point(get_G_vector()[0] * 0.5, get_G_vector()[1] * 0.5))

        # Add updater to track G vector
        G_dot.add_updater(
            lambda m: m.move_to(axes.coords_to_point(get_G_vector()[0] * 0.5, get_G_vector()[1] * 0.5))
        )

        self.play(Create(G_dot))
        self.wait(1)

        # Now animate k_scat and watch G_dot move on the plot
        self.play(
            Rotate(k_scat, angle=-OBJ_COLLECTION_ANGLE, about_point=[0, 0, 0]),
            rate_func=linear,
            run_time=2
        )
        self.wait(1)
        self.play(
            Rotate(k_scat, angle=OBJ_COLLECTION_ANGLE, about_point=[0, 0, 0]),
            rate_func=linear,
            run_time=2
        )

        self.wait(10)


if __name__ == "__main__":
    print("Objective collection angle, degrees:", OBJ_COLLECTION_ANGLE * DEGREES)
