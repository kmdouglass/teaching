from manim import *

from common_anims import by, explain
from settings import *


def create_3d_crystal_lattice(
    num_points_per_axis: int = 3,
    point_radius: float = 0.1,
    dx: float = 1.0,
    dy: float = 1.0,
    dz: float = 1.0,
    scale: float = 3.0,
) -> tuple[VGroup, list[float]]:
    lattice = VGroup()

    # Axes
    # The axes are centered at zero and at most two units longer than the extent of the atoms
    axis_range = (
        (-((num_points_per_axis + 1) // 2) * dx, ((num_points_per_axis + 1) // 2) * dx, 1),
        (-((num_points_per_axis + 1) // 2) * dy, ((num_points_per_axis + 1) // 2) * dy, 1),
        (-((num_points_per_axis + 1) // 2) * dz, ((num_points_per_axis + 1) // 2) * dz, 1),
    )

    axes = ThreeDAxes(
        x_range=axis_range[0],
        y_range=axis_range[1],
        z_range=axis_range[2],
        x_length=scale * ((num_points_per_axis + 1) // 2 * dx),
        y_length=scale * ((num_points_per_axis + 1) // 2 * dy),
        z_length=scale * ((num_points_per_axis + 1) // 2 * dz),
    )
    lattice.add(axes)

    # Track the y-positions of the atoms projected onto the origin in the world coordinate system
    y_projected = []

    # Atoms
    for i in range(num_points_per_axis):
        x_pos = i * dx - (num_points_per_axis / 2 - 0.5)

        for j in range(num_points_per_axis):
            y_pos = j * dy - (num_points_per_axis / 2 - 0.5)

            for k in range(num_points_per_axis):
                z_pos = k * dz - (num_points_per_axis / 2 - 0.5)

                atom = Sphere(radius=point_radius)
                atom.set_color(YELLOW)
                atom.move_to(axes.coords_to_point(x_pos, y_pos, z_pos))
                lattice.add(atom)

                # Save the y-positions of the atoms projected onto the origin for a later scene
                if i == 0 and k == 0:
                    y_projected.append(axes.coords_to_point(0, y_pos, 0)[1])
    
    return lattice, y_projected


class BraggCondition3D(ThreeDScene):
    def construct(self) -> None:

        #------------------------------------------------------------------------------------------
        # Title
        title = Title("The Bragg Condition", font_size=TITLE_FONT_SIZE)
        self.play(Write(title))
        self.wait(TITLE_WAIT_TIME_S)
        self.play(FadeOut(title))

        #------------------------------------------------------------------------------------------
        # Crystal Lattice
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, focal_distance=100)

        lattice, _ = create_3d_crystal_lattice()
        lattice.move_to(ORIGIN)
        self.play(Create(lattice))
        self.wait(1)

        explain("An orthorhombic crystal lattice...", self)

        self.move_camera(phi=75 * DEGREES, theta=-30 * DEGREES)
        self.wait(2)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.wait(2)

        self.play(FadeOut(lattice), run_time=0.5)


def create_lattice_planes(
    num_planes = 3,
    separation_distance = 1.0,
) -> VGroup:
    planes = VGroup()

    starting_y = (-(num_planes / 2.0) + 0.5) * separation_distance
    x_range = (-5.0, 5.0) 
    for i in range(num_planes):
        current_y = starting_y + i * separation_distance

        plane = Line(
            start=(x_range[0], current_y, 0.0),
            end=(x_range[1], current_y, 0.0),
            stroke_width=5,
            color=YELLOW,
        )
        planes.add(plane)

    return planes


class BraggCondition2D(Scene):
    def construct(self) -> None:
        #------------------------------------------------------------------------------------------
        # 2D Lattice Planes
        _, y_projected = create_3d_crystal_lattice(num_points_per_axis=3)
        num_planes = len(y_projected)
        separation_distance = y_projected[1] - y_projected[0]

        lattice_planes = create_lattice_planes(
            num_planes=num_planes,
            separation_distance=separation_distance
        )
        self.play(FadeIn(lattice_planes), run_time=0.5)

        explain("...is represented as a set of lattice planes.", self)

        #------------------------------------------------------------------------------------------
        # Incident and Reflected Rays
        incident_angle = 45 * DEGREES
        incident_length = 6.0

        # The incident ray intersects the origin (0, 0)
        assert num_planes % 2 == 1, "Number of planes must be odd to center at origin."
        y_min = min(y_projected)

        lattice_plane_intersection_points = []
        for i in range(num_planes):
            current_y = y_min + i * separation_distance
            lattice_plane_intersection_points.append((0.0, current_y, 0.0))

        # Reverse the list to go from top to bottom
        lattice_plane_intersection_points = lattice_plane_intersection_points[::-1]

        explain("Incident light reflects off of each lattice plane.", self, DOWN)

        ray_pairs = []
        for end in lattice_plane_intersection_points:
            start = (
                end[0] - incident_length * np.cos(incident_angle),
                end[1] + incident_length * np.sin(incident_angle),
                0.0,
            )

            incident = Line(
                start=start,
                end=end,
                stroke_width=5,
                color=WHITE,
            )
            reflected = Line(
                start=end,
                end=(
                    -start[0],
                    start[1],
                    0.0,
                ),
                stroke_width=5,
                color=WHITE,
            )

            ray_pairs.append((incident, reflected))

        for i in range(len(ray_pairs) + 1):
            if i == 0:
                # First, just draw the incident ray to the top plane
                self.play(Create(ray_pairs[0][0]), rate_func=linear, run_time=0.75)
            elif i < len(ray_pairs):
                # Then, for each subsequent plane, draw the reflected ray from the previous plane
                # and the incident ray to the current plane
                self.play(
                    Create(ray_pairs[i - 1][1]),
                    Create(ray_pairs[i][0]),
                    rate_func=linear,
                    run_time=0.75,
                )
            else:
                # Finally, draw the reflected ray from the last plane
                self.play(Create(ray_pairs[i - 1][1]), rate_func=linear, run_time=0.75)
        #------------------------------------------------------------------------------------------
        # Rotate the angle of incidence
        explain("As the angle of incidence changes...", self, DOWN)

        def rotate_incidence_angle(rotation_angle: float, wait_time: float = 0.5) -> None:
            animations = []
            for i in range(len(ray_pairs)):
                incident, reflected = ray_pairs[i]

                animations.append(
                    incident.animate.rotate(-rotation_angle, about_point=incident.get_end())
                )
                animations.append(
                    reflected.animate.rotate(rotation_angle, about_point=reflected.get_start())
                )

            self.play(*animations)
            self.wait(wait_time)

        rotate_incidence_angle(15 * DEGREES)
        rotate_incidence_angle(-30 * DEGREES)
        rotate_incidence_angle(15 * DEGREES)

        #------------------------------------------------------------------------------------------
        # Optical Path Difference
        explain("...the optical path difference (OPD) between successive rays...", self, DOWN)

        construction_lines = VGroup()
        vertical_construction = DashedLine(
            start=(0.0, 2.0, 0.0),
            end=(0.0, -2.0, 0.0),
            stroke_width=5,
            color=BLUE,
        )

        middle_incident = ray_pairs[len(ray_pairs) // 2][0]
        middle_reflected = ray_pairs[len(ray_pairs) // 2][1]

        def perpendicular_foot(point, line_start, line_end):
            """
            Find the foot of the perpendicular from a point to a line.
            
            Parameters
            ----------
            point
                The point from which to drop the perpendicular
            line_start: Start point of the line
                Start point of the line
            line_end
                End point of the line
            
            Returns
            -------
            The point on the line closest to the input point.
    
            """
            point = np.array(point)
            line_start = np.array(line_start)
            line_end = np.array(line_end)
            
            # Direction vector of the line
            line_vec = line_end - line_start
            
            # Vector from line start to the point
            point_vec = point - line_start
            
            # Project point_vec onto line_vec
            line_length_sq = np.dot(line_vec, line_vec)
            if line_length_sq == 0:
                return line_start  # Line has zero length
            
            t = np.dot(point_vec, line_vec) / line_length_sq
            
            # The foot of the perpendicular
            foot = line_start + t * line_vec
            
            return foot

        dropped_perpendicular_start = lattice_plane_intersection_points[len(ray_pairs) // 2 - 1]
        left_dropped_perpendicular = DashedLine(
            start=dropped_perpendicular_start,
            end=perpendicular_foot(
                dropped_perpendicular_start,
                middle_incident.get_start(),
                middle_incident.get_end()
            ),
            stroke_width=5,
            color=BLUE,
        )
        right_dropped_perpendicular = DashedLine(
            start=dropped_perpendicular_start,
            end=perpendicular_foot(
                dropped_perpendicular_start,
                middle_reflected.get_start(),
                middle_reflected.get_end()
            ),
            stroke_width=5,
            color=BLUE,
        )
        construction_lines.add(
            vertical_construction,
            left_dropped_perpendicular,
            right_dropped_perpendicular
        )
        self.play(
            Create(construction_lines),
            *[ray.animate.set_opacity(0.5) for pair in ray_pairs for ray in pair],
        )

        opd_path = VGroup()
        opd_path.add(
            Line(
                start=left_dropped_perpendicular.get_end(),
                end=(0.0, 0.0, 0.0),
                stroke_width=8,
                color=PURE_GREEN,
            ),
            Line(
                start=(0.0, 0.0, 0.0),
                end=right_dropped_perpendicular.get_end(),
                stroke_width=8,
                color=PURE_GREEN,
            ),
        )
        self.play(Create(opd_path),)

        explain("...changes as well.", self, DOWN)

        opd_value = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=False,
            font_size=36,
        )
        opd_value.add_updater(
            lambda v: v.set_value(
                opd_path[0].get_length() + opd_path[1].get_length()
            )
        )

        opd_indicator = VGroup(
            Text("OPD = ", font_size=24),
            opd_value,
            MathTex("\\lambda", font_size=36),
        ).arrange(RIGHT, buff=0.08).to_corner(UP + LEFT)
        self.play(Write(opd_indicator))

        def rotate_incidence_angle_opd(
            rotation_angle: float,
            dropped_perpendicular_start=dropped_perpendicular_start,
            opd_bend_location=(0.0, 0.0, 0.0),
            run_time_s: float = 1.0,
            rate_func = smooth,
            wait_time_s: float = 0.5
        ) -> None:
            # Add updaters to the construction lines
            left_dropped_perpendicular.add_updater(
                lambda line: line.put_start_and_end_on(
                    dropped_perpendicular_start,
                    perpendicular_foot(
                        dropped_perpendicular_start,
                        middle_incident.get_start(),
                        middle_incident.get_end()
                    )
                )
            )
            
            right_dropped_perpendicular.add_updater(
                lambda line: line.put_start_and_end_on(
                    dropped_perpendicular_start,
                    perpendicular_foot(
                        dropped_perpendicular_start,
                        middle_reflected.get_start(),
                        middle_reflected.get_end()
                    )
                )
            )
            
            # Add updaters to the OPD path lines
            opd_path[0].add_updater(
                lambda line: line.put_start_and_end_on(
                    left_dropped_perpendicular.get_end(),
                    opd_bend_location,
                )
            )
            
            opd_path[1].add_updater(
                lambda line: line.put_start_and_end_on(
                    opd_bend_location,
                    right_dropped_perpendicular.get_end()
                )
            )
            
            # Now animate the rotations
            animations = []
            for i in range(len(ray_pairs)):
                incident, reflected = ray_pairs[i]
                animations.append(
                    incident.animate.rotate(-rotation_angle, about_point=incident.get_end())
                )
                animations.append(
                    reflected.animate.rotate(rotation_angle, about_point=reflected.get_start())
                )
            
            self.play(*animations, run_time=run_time_s, rate_func=rate_func)
            self.wait(wait_time_s)
            
            # Remove updaters after animation (optional, but good practice)
            left_dropped_perpendicular.clear_updaters()
            right_dropped_perpendicular.clear_updaters()
            opd_path[0].clear_updaters()
            opd_path[1].clear_updaters()

        rotate_incidence_angle_opd(15 * DEGREES)
        rotate_incidence_angle_opd(-30 * DEGREES)
        rotate_incidence_angle_opd(15 * DEGREES)

        #------------------------------------------------------------------------------------------
        # Bragg Condition
        explain("When the OPD is an integer multiple of wavelengths...", self, DOWN)

        # Bragg condition at 42.1 incidence angle w.r.t. the lattice planes
        rotate_incidence_angle_opd(-3.19 * DEGREES, wait_time_s=2.0)

        explain("...constructive interference occurs...", self, DOWN)

        reflected_rays = [pair[1] for pair in ray_pairs]
        self.play(
            *[ray.animate.set_opacity(1.0) for ray in reflected_rays],
            run_time=0.5
        )
        self.play(
            *[ray.animate.set_opacity(0.5) for ray in reflected_rays],
            run_time=0.5
        )
        self.play(
            *[ray.animate.set_opacity(1.0) for ray in reflected_rays],
            run_time=0.5
        )
        self.play(
            *[ray.animate.set_opacity(0.5) for ray in reflected_rays],
            run_time=0.5
        )

        explain("...and a diffraction peak is observed.", self, DOWN)

        illustrations = VGroup(
            lattice_planes,
            *ray_pairs,
            construction_lines,
            opd_path,
        )
        scale_factor = 0.65
        opd_value.clear_updaters()
        self.play(
            illustrations.animate.scale(scale_factor).to_edge(DOWN),
            run_time=SCALING_RUN_TIME_S,
        )
        opd_value.add_updater(
            lambda v: v.set_value(
                (opd_path[0].get_length() + opd_path[1].get_length()) / scale_factor
            )
        )

        # Create a horizontal axis
        axis = NumberLine(
            x_range=(0, 90, 10),
            length=8.0,
            color=WHITE,
            include_ticks=True,
            label_direction=DOWN,
        ).to_edge(UP)
        axis.add_labels({
            0: MathTex("0^\\circ", font_size=24),
            30: MathTex("30^\\circ", font_size=24),
            60: MathTex("60^\\circ", font_size=24),
            90: MathTex("90^\\circ", font_size=24),
        })
        self.play(Create(axis))
        self.wait(2)

        # Find the centers of the lattice plane after scaling and moving down
        first_plane_center = lattice_planes[-1].get_center()
        middle_plane_center = lattice_planes[len(lattice_planes) // 2].get_center()
        rotate_incidence_angle_opd(
            -41.81 * DEGREES,
            dropped_perpendicular_start=first_plane_center,
            opd_bend_location=middle_plane_center,
            wait_time_s=2.0
        )

        bragg_peaks = VGroup()

        added_dots = {}
        peak_values = [0, 19.47, 41.81, 90.0] # Precomputed peak angles for n=0,1,2,3
        def update_bragg_peaks(mob):
            current_opd = opd_value.get_value()
            
            # Check if OPD is close to an integer (within tolerance)
            tolerance = 0.001  # Adjust this value as needed
            closest_integer = round(current_opd)
            
            if current_opd > closest_integer - tolerance:
                if added_dots.get(closest_integer, None) is None:
                    dot_position = axis.number_to_point(peak_values[closest_integer])
                    dot = Dot(point=dot_position, color=YELLOW, radius=0.15)
                    mob.add(dot)
                    added_dots[closest_integer] = True
                    
                else:
                    # Bragg peak already drawn for this integer
                    return

        bragg_peaks.add_updater(update_bragg_peaks)
        self.add(bragg_peaks)

        rotate_incidence_angle_opd(
            90 * DEGREES,
            dropped_perpendicular_start=first_plane_center,
            opd_bend_location=middle_plane_center,
            run_time_s=7.5,
            rate_func=linear,
            wait_time_s=2.00,
        )
        bragg_peaks.clear_updaters()

        self.play(
            FadeOut(illustrations),
            FadeOut(opd_indicator),
            FadeOut(axis),
            FadeOut(bragg_peaks),
        )

        by(self)


if __name__ == "__main__":
    create_3d_crystal_lattice()
