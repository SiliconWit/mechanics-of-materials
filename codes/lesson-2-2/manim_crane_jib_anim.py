#!/usr/bin/env python3
"""
Crane Jib Bending Analysis - Manim Animations
Based on crane_jib_analysis.py

Generates 4 scenes:
1. Real-world crane jib system
2. Loading diagram with exaggerated bending animation
3. Shear force diagram
4. Bending moment diagram
"""

from manim import *
import numpy as np

# Color scheme - bright and noticeable
COLORS = {
    'beam': '#405ab9',
    'load_arrow': '#ff8c36',
    'reaction': '#00d4ff',
    'shear_pos': '#00ff88',  # Bright green
    'shear_neg': '#ff3366',  # Bright red
    'moment_pos': '#ffdd00',  # Bright yellow
    'moment_neg': '#ff3366',  # Bright red
    'text': '#ffffff',  # White for better visibility
    'support': '#405ab9',
    'background': '#1a1a1a'
}

# Physical parameters from crane_jib_analysis.py
L_SPAN = 3.0  # meters
L_OVERHANG = 1.0  # meters
L_TOTAL = L_SPAN + L_OVERHANG  # 4.0 meters
P1 = 7000  # N (dynamic load at midspan)
P2 = 4200  # N (dynamic load at overhang end)
W = 800  # N/m (distributed load)
R_A = 3167  # N (reaction at A)
R_B = 11233  # N (reaction at B)


class Scene1_ImageCrane(Scene):
    """Scene 1: Display crane image from file"""

    def construct(self):
        self.camera.background_color = COLORS['background']

        # Title
        title = Text("Real Industrial System",
                    font_size=52, color=COLORS['text'], weight=BOLD)

        # Load and display image
        # Assuming image is in same directory or provide full path
        crane_image = ImageMobject("double-girder-gantry-crane.png")
        crane_image.scale_to_fit_width(9)  # Zoomed out to fit screen better
        crane_image.move_to(ORIGIN)

        # Fast animation - title fades in and out, then image appears
        self.play(FadeIn(title), run_time=0.4)
        self.wait(0.8)
        self.play(FadeOut(title), run_time=0.4)
        self.play(FadeIn(crane_image, scale=0.98), run_time=0.6)
        self.wait(1.5)


class Scene1_RealCrane(Scene):
    """Scene 1: Realistic crane jib in industrial setting (animated)"""

    def construct(self):
        self.camera.background_color = COLORS['background']

        # Title
        title = Text("Crane Jib System",
                    font_size=44, color=COLORS['text'], weight=BOLD).to_edge(UP)

        # Ground and foundation
        ground = Line(LEFT*7, RIGHT*7, color="#555555", stroke_width=6).shift(DOWN*2.8)

        # Concrete foundations
        foundation_A = Rectangle(height=0.4, width=1.2, color="#666666",
                                fill_opacity=1, stroke_color="#444444").next_to(ground, UP, buff=0).shift(LEFT*3)
        foundation_B = Rectangle(height=0.4, width=1.2, color="#666666",
                                fill_opacity=1, stroke_color="#444444").next_to(ground, UP, buff=0).shift(RIGHT*1.5)

        # Steel support columns (more realistic proportions)
        column_A = Rectangle(height=2.5, width=0.25, color=COLORS['support'],
                            fill_opacity=1, stroke_width=3).next_to(foundation_A, UP, buff=0)
        column_B = Rectangle(height=2.0, width=0.25, color=COLORS['support'],
                            fill_opacity=1, stroke_width=3).next_to(foundation_B, UP, buff=0)

        # I-beam - more realistic side view, positioned first
        beam_length = 7.5
        beam_center_y = column_A.get_top()[1] + 0.6
        beam_bottom_y = beam_center_y - 0.15

        # Flanges (top and bottom horizontal parts)
        top_flange = Rectangle(height=0.12, width=beam_length, color=COLORS['beam'],
                              fill_opacity=1, stroke_width=2).move_to([0, beam_center_y + 0.15, 0])
        web = Rectangle(height=0.3, width=beam_length*0.98, color=COLORS['beam'],
                       fill_opacity=0.7, stroke_width=2).move_to([0, beam_center_y, 0])
        bottom_flange = Rectangle(height=0.12, width=beam_length, color=COLORS['beam'],
                                 fill_opacity=1, stroke_width=2).move_to([0, beam_bottom_y, 0])
        i_beam = VGroup(top_flange, web, bottom_flange)

        # Support connection details - positioned after beam
        # Pinned joint at A - triangle with sharp point UP, base matching column width
        column_width = 0.25
        beam_bottom = beam_bottom_y - 0.06  # Bottom of beam flange

        # Calculate triangle height to span from column top to beam bottom
        gap_to_beam_A = beam_bottom - column_A.get_top()[1]
        triangle_height = gap_to_beam_A

        pinned_joint = Triangle(color=COLORS['support'], fill_opacity=1)
        pinned_joint.set_width(column_width)  # Match column width
        pinned_joint.set_height(triangle_height)
        # Position so apex touches beam bottom, base sits on column top
        pinned_joint.move_to([column_A.get_center()[0], column_A.get_top()[1] + triangle_height/2, 0])

        # Roller joint at B - circle touching beam bottom AND sitting on column
        roller_radius = 0.12
        roller_joint = Circle(radius=roller_radius, color=COLORS['support'], fill_opacity=1)
        # Calculate height needed: from column top to beam bottom
        gap_height = beam_bottom - column_B.get_top()[1]
        # Position circle so bottom sits on column top and top touches beam
        roller_joint.move_to([column_B.get_center()[0], column_B.get_top()[1] + gap_height - roller_radius, 0])

        # Loads - more realistic
        # P1 at midspan - container load
        P1_x = -1.5
        cable_1 = Line([P1_x, beam_center_y - 0.15, 0],
                      [P1_x, beam_center_y - 1.3, 0],
                      color="#333333", stroke_width=4)
        container = Rectangle(height=0.6, width=0.8, color="#FF6B35",
                            fill_opacity=0.9, stroke_color="#CC4420", stroke_width=3)
        container.next_to(cable_1, DOWN, buff=0.05)

        # P2 at overhang - steel coil
        P2_x = 3.5
        cable_2 = Line([P2_x, beam_center_y - 0.15, 0],
                      [P2_x, beam_center_y - 1.8, 0],
                      color="#333333", stroke_width=4)
        coil = Circle(radius=0.4, color="#B33030", fill_opacity=0.9,
                     stroke_color="#8B0000", stroke_width=3)
        coil.next_to(cable_2, DOWN, buff=0.05)

        # Labels - minimal
        label_P1 = MathTex("P_1", color=COLORS['load_arrow'], font_size=32).next_to(container, LEFT, buff=0.2)
        label_P2 = MathTex("P_2", color=RED, font_size=32).next_to(coil, RIGHT, buff=0.2)

        # Animation
        self.play(Write(title))
        self.wait(0.3)
        self.play(Create(ground), Create(foundation_A), Create(foundation_B))
        self.play(Create(column_A), Create(column_B), run_time=1)
        self.play(Create(pinned_joint), Create(roller_joint), run_time=0.8)
        self.play(Create(i_beam), run_time=1.5)
        self.wait(0.3)

        # Add loads
        self.play(Create(cable_1), FadeIn(container, scale=0.8), Write(label_P1))
        self.play(Create(cable_2), FadeIn(coil, scale=0.8), Write(label_P2))

        # Realistic loading motion
        self.play(
            container.animate.shift(DOWN*0.1),
            cable_1.animate.stretch(1.05, 1),
            rate_func=there_and_back,
            run_time=1.5
        )
        self.play(
            coil.animate.shift(DOWN*0.15),
            cable_2.animate.stretch(1.08, 1),
            rate_func=there_and_back,
            run_time=1.5
        )

        self.wait(1.5)


class Scene2_LoadingDiagram(Scene):
    """Scene 2: Loading diagram with exaggerated bending animation"""

    def construct(self):
        self.camera.background_color = COLORS['background']

        # Title - will fade in and out before diagram
        title = Text("Loading Diagram",
                    font_size=52, color=COLORS['text'], weight=BOLD)

        # Create beam - EVEN BIGGER and more visible
        beam_length = 11  # Even longer
        beam_height = 0.15
        beam = Line(LEFT*beam_length/2, RIGHT*beam_length/2,
                   color='#00d4ff', stroke_width=16).move_to(ORIGIN + UP*0.3)  # Even thicker, positioned higher

        # Supports - BIGGER and more visible
        # Support A (pinned) - triangle pointing up with apex just touching beam
        support_A_pos = beam.get_left()
        triangle_height = 0.6  # Bigger (was 0.4)
        triangle_A = Triangle(color='#00d4ff', fill_opacity=1, stroke_width=3).scale(0.4)  # Bigger, bright cyan
        # Position triangle so top vertex just touches beam bottom
        triangle_A.move_to(support_A_pos + DOWN*triangle_height/2)
        ground_line_A = Line(triangle_A.get_bottom() + LEFT*0.6,
                            triangle_A.get_bottom() + RIGHT*0.6,
                            color=WHITE, stroke_width=5)  # Thicker, white

        # Support B (roller) - circle just touching beam from below
        support_B_x = beam.get_left()[0] + beam_length * (L_SPAN / L_TOTAL)
        roller_radius = 0.2  # Bigger (was 0.12)
        support_B_pos = np.array([support_B_x, beam.get_center()[1], 0])
        circle_B = Circle(radius=roller_radius, color='#00d4ff', fill_opacity=1, stroke_width=3)  # Bright cyan
        # Position circle so top edge just touches beam
        circle_B.move_to([support_B_x, support_B_pos[1] - roller_radius, 0])
        ground_line_B = Line(circle_B.get_bottom() + LEFT*0.6,
                            circle_B.get_bottom() + RIGHT*0.6,
                            color=WHITE, stroke_width=5)  # Thicker, white

        # Load arrows - EVEN BIGGER and VERY NOTICEABLE
        # P1 at midspan
        P1_x = beam.get_left()[0] + beam_length * 0.375  # 1.5m / 4m = 0.375
        P1_arrow = Arrow(start=UP*2.0, end=UP*0.05, color='#ffaa00',
                        stroke_width=14, max_tip_length_to_length_ratio=0.2)  # Very thick, bright yellow-orange
        P1_arrow.move_to(np.array([P1_x, beam.get_center()[1] + 1.1, 0]))
        P1_label = MathTex(r"P_1", color='#ffaa00',
                          font_size=60, stroke_width=2).next_to(P1_arrow, UP, buff=0.15)  # Much bigger!

        # P2 at overhang end
        P2_x = beam.get_right()[0]
        P2_arrow = Arrow(start=UP*2.0, end=UP*0.05, color='#ff0066',
                        stroke_width=14, max_tip_length_to_length_ratio=0.2)  # Very thick, hot pink
        P2_arrow.move_to(np.array([P2_x, beam.get_center()[1] + 1.1, 0]))
        P2_label = MathTex(r"P_2", color='#ff0066',
                          font_size=60, stroke_width=2).next_to(P2_arrow, UP, buff=0.15)  # Much bigger!

        # Distributed load (multiple arrows) - BIGGER and more visible
        dist_load_arrows = VGroup()
        n_arrows = 18  # Even more arrows
        for i in range(n_arrows):
            x_pos = beam.get_left()[0] + (i + 0.5) * beam_length / n_arrows
            arrow = Arrow(start=UP*0.8, end=UP*0.05, color='#ffaa00',
                         stroke_width=8, max_tip_length_to_length_ratio=0.3)  # Thicker
            arrow.move_to(np.array([x_pos, beam.get_center()[1] + 0.45, 0]))
            dist_load_arrows.add(arrow)

        dist_label = MathTex(r"w", color='#ffaa00',
                            font_size=56, stroke_width=2).move_to(beam.get_center() + UP*1.6 + LEFT*4.5)  # Much bigger!

        # Reaction forces - BIGGER and bright cyan
        R_A_arrow = Arrow(start=DOWN*1.4, end=DOWN*0.05, color='#00ffff',
                         stroke_width=14, max_tip_length_to_length_ratio=0.2)  # Very thick, bright cyan
        R_A_arrow.move_to(support_A_pos + DOWN*1.0).flip(UP)
        R_A_label = MathTex(r"R_A", color='#00ffff',
                           font_size=56, stroke_width=2).next_to(R_A_arrow, DOWN, buff=0.2)  # Bigger

        R_B_arrow = Arrow(start=DOWN*1.4, end=DOWN*0.05, color='#00ffff',
                         stroke_width=14, max_tip_length_to_length_ratio=0.2)  # Very thick
        R_B_arrow.move_to(support_B_pos + DOWN*1.0).flip(UP)
        R_B_label = MathTex(r"R_B", color='#00ffff',
                           font_size=56, stroke_width=2).next_to(R_B_arrow, DOWN, buff=0.2)  # Bigger

        # Fast animation sequence - title fades in and out first
        self.play(FadeIn(title), run_time=0.4)
        self.wait(0.6)
        self.play(FadeOut(title), run_time=0.4)

        # Show diagram quickly
        self.play(Create(beam), run_time=0.5)
        self.play(
            Create(triangle_A), Create(ground_line_A),
            Create(circle_B), Create(ground_line_B),
            run_time=0.5
        )

        # Add loads quickly
        self.play(
            GrowArrow(P1_arrow), Write(P1_label),
            GrowArrow(P2_arrow), Write(P2_label),
            run_time=0.6
        )
        self.play(
            *[GrowArrow(arrow) for arrow in dist_load_arrows],
            Write(dist_label),
            run_time=0.8
        )

        # Add reactions quickly
        self.play(
            GrowArrow(R_A_arrow), Write(R_A_label),
            GrowArrow(R_B_arrow), Write(R_B_label),
            run_time=0.6
        )

        self.wait(0.3)

        # EXAGGERATED BENDING ANIMATION - oscillating 3 times
        # Beam stays at supports, only bends between them

        # Store original beam center for reference
        beam_y_center = beam.get_center()[1]
        beam_x_left = beam.get_left()[0]

        def get_deflected_curve(alpha):
            """Beam deflection - stays at support points, sags between"""
            points = []
            n_points = 100

            # Support positions along beam
            support_A_t = 0  # Left end (x = 0)
            support_B_t = L_SPAN / L_TOTAL  # 3.0/4.0 = 0.75

            for i in range(n_points):
                t = i / (n_points - 1)
                x = beam_x_left + t * beam_length

                # Calculate deflection, but ensure beam passes through supports
                if t <= support_B_t:  # Between A and B - sagging downward
                    # Parabolic sag with zero deflection at supports
                    # Maximum sag at midpoint
                    relative_t = t / support_B_t
                    sag_factor = relative_t * (1 - relative_t)
                    deflection = -0.8 * alpha * sag_factor * 4  # Exaggerated sag
                else:  # Overhang beyond B - drooping down
                    # Zero deflection at B, increasing deflection toward P2
                    overhang_t = (t - support_B_t) / (1 - support_B_t)
                    deflection = -0.6 * alpha * (overhang_t ** 2) * 2  # Exaggerated droop

                # Beam stays at same vertical position at supports
                y = beam_y_center + deflection
                points.append([x, y, 0])

            return points

        # Animate bending oscillation - swings back and forth 3 times
        # Beam returns to straight each time
        def beam_updater(mob, alpha):
            curve_points = get_deflected_curve(alpha)
            new_curve = VMobject(color='#00d4ff', stroke_width=16)
            new_curve.set_points_as_corners(curve_points)
            mob.become(new_curve)

        # Swing back and forth 3 times - beam stays in position
        # Using there_and_back makes it go: straight → bent → straight
        self.play(
            UpdateFromAlphaFunc(beam, beam_updater),
            run_time=0.7,
            rate_func=there_and_back
        )
        self.play(
            UpdateFromAlphaFunc(beam, beam_updater),
            run_time=0.7,
            rate_func=there_and_back
        )
        self.play(
            UpdateFromAlphaFunc(beam, beam_updater),
            run_time=0.7,
            rate_func=there_and_back
        )

        self.wait(0.8)


class Scene3_ShearDiagram(Scene):
    """Scene 3: Animated shear force diagram"""

    def construct(self):
        self.camera.background_color = COLORS['background']

        # Title - will fade in and out
        title = Text("Shear Force Diagram", font_size=52,
                    color=COLORS['text'], weight=BOLD)

        # Create axes - BIGGER and more visible
        axes = Axes(
            x_range=[0, 4.2, 0.5],
            y_range=[-7, 6, 2],
            x_length=11,  # Wider
            y_length=6.5,  # Taller
            axis_config={"color": WHITE, "stroke_width": 5},  # Thicker, white axes
            tips=False
        ).shift(DOWN*0.3)

        # Labels
        x_label = Text("Distance from A (m)", font_size=28, color=WHITE).next_to(
            axes.x_axis, DOWN, buff=0.3
        )
        y_label = Text("Shear Force (kN)", font_size=28, color=WHITE).rotate(PI/2).next_to(
            axes.y_axis, LEFT, buff=0.4
        )

        # Shear force values (from analysis)
        # Region 1: 0 to 1.5m (before P1)
        V_0 = 3.167  # kN
        V_before_P1 = 1.967  # kN

        # Region 2: 1.5m to 3.0m (after P1, before B)
        V_after_P1 = -5.033  # kN
        V_before_B = -6.233  # kN

        # Region 3: 3.0m to 4.0m (after B, overhang)
        V_after_B = 5.0  # kN
        V_end = 0.0  # kN

        # Create shear diagram segments - THICKER and more visible
        # Segment 1: 0 to 1.5m
        seg1_start = axes.c2p(0, V_0)
        seg1_end = axes.c2p(1.5, V_before_P1)
        seg1 = Line(seg1_start, seg1_end, color=COLORS['shear_pos'], stroke_width=10)

        # Jump at P1
        jump1_start = axes.c2p(1.5, V_before_P1)
        jump1_end = axes.c2p(1.5, V_after_P1)
        jump1 = DashedLine(jump1_start, jump1_end, color=COLORS['load_arrow'],
                          stroke_width=6, dash_length=0.1)

        # Segment 2: 1.5m to 3.0m
        seg2_start = axes.c2p(1.5, V_after_P1)
        seg2_end = axes.c2p(3.0, V_before_B)
        seg2 = Line(seg2_start, seg2_end, color=COLORS['shear_neg'], stroke_width=10)

        # Jump at B
        jump2_start = axes.c2p(3.0, V_before_B)
        jump2_end = axes.c2p(3.0, V_after_B)
        jump2 = DashedLine(jump2_start, jump2_end, color=COLORS['reaction'],
                          stroke_width=6, dash_length=0.1)

        # Segment 3: 3.0m to 4.0m (overhang)
        seg3_start = axes.c2p(3.0, V_after_B)
        seg3_end = axes.c2p(4.0, V_end)
        seg3 = Line(seg3_start, seg3_end, color=COLORS['shear_pos'], stroke_width=10)

        # Create filled polygons for shear areas
        # Region 1 fill
        fill1_points = [seg1_start]
        for i in range(len([seg1_start, seg1_end])):
            if i == 0:
                fill1_points.append(seg1_start)
            else:
                fill1_points.append(seg1_end)
        fill1_points.append(axes.c2p(1.5, 0))
        fill1_points.append(axes.c2p(0, 0))
        fill1 = Polygon(*fill1_points, color=COLORS['shear_pos'],
                       fill_opacity=0.3, stroke_width=0)

        # Region 2 fill
        fill2_points = [seg2_start, seg2_end,
                       axes.c2p(3.0, 0), axes.c2p(1.5, 0)]
        fill2 = Polygon(*fill2_points, color=COLORS['shear_neg'],
                       fill_opacity=0.3, stroke_width=0)

        # Region 3 fill
        fill3_points = [seg3_start, seg3_end,
                       axes.c2p(4.0, 0), axes.c2p(3.0, 0)]
        fill3 = Polygon(*fill3_points, color=COLORS['shear_pos'],
                       fill_opacity=0.3, stroke_width=0)

        # Critical value labels - BIGGER and more visible
        dot_V0 = Dot(seg1_start, color=YELLOW, radius=0.12)
        label_V0 = MathTex(r"V_0", font_size=38,
                          color=YELLOW).next_to(dot_V0, UP+RIGHT, buff=0.15)

        dot_Vmin = Dot(seg2_end, color="#ff3366", radius=0.12)
        label_Vmin = MathTex(r"V_{\text{min}}", font_size=38,
                            color="#ff3366").next_to(dot_Vmin, DOWN+LEFT, buff=0.15)

        dot_Vmax = Dot(seg3_start, color="#00ff88", radius=0.12)
        label_Vmax = MathTex(r"V_{\text{max}}", font_size=38,
                            color="#00ff88").next_to(dot_Vmax, UP+RIGHT, buff=0.15)

        # Reference lines at key locations
        line_P1 = DashedLine(axes.c2p(1.5, -7), axes.c2p(1.5, 6),
                            color=COLORS['load_arrow'], stroke_width=2,
                            dash_length=0.15, stroke_opacity=0.5)
        label_line_P1 = Text("P₁", font_size=24, color=COLORS['load_arrow']).next_to(
            axes.c2p(1.5, 6), UP, buff=0.1
        )

        line_B = DashedLine(axes.c2p(3.0, -7), axes.c2p(3.0, 6),
                           color=COLORS['reaction'], stroke_width=2,
                           dash_length=0.15, stroke_opacity=0.5)
        label_line_B = Text("B", font_size=24, color=COLORS['reaction']).next_to(
            axes.c2p(3.0, 6), UP, buff=0.1
        )

        # Fast animation - title fades in and out first
        self.play(FadeIn(title), run_time=0.4)
        self.wait(0.6)
        self.play(FadeOut(title), run_time=0.4)

        # Show axes and labels quickly
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.6)

        # Show reference lines quickly
        self.play(
            Create(line_P1), Write(label_line_P1),
            Create(line_B), Write(label_line_B),
            run_time=0.5
        )

        # Animate shear diagram faster
        self.play(Create(seg1), FadeIn(fill1), run_time=0.8)
        self.play(FadeIn(dot_V0), Write(label_V0), run_time=0.4)

        self.play(Create(jump1), run_time=0.3)
        self.play(Create(seg2), FadeIn(fill2), run_time=0.8)
        self.play(FadeIn(dot_Vmin), Write(label_Vmin), run_time=0.4)

        self.play(Create(jump2), run_time=0.3)
        self.play(Create(seg3), FadeIn(fill3), run_time=0.8)
        self.play(FadeIn(dot_Vmax), Write(label_Vmax), run_time=0.4)

        # Highlight zero crossing
        zero_line = axes.get_horizontal_line(axes.c2p(4, 0),
                                            color=WHITE, stroke_width=4)
        self.play(Create(zero_line), run_time=0.4)

        self.wait(1.0)


class Scene4_MomentDiagram(Scene):
    """Scene 4: Animated bending moment diagram"""

    def construct(self):
        self.camera.background_color = COLORS['background']

        # Title - will fade in and out
        title = Text("Bending Moment Diagram", font_size=52,
                    color=COLORS['text'], weight=BOLD)

        # Create axes - BIGGER and more visible
        axes = Axes(
            x_range=[0, 4.2, 0.5],
            y_range=[-6, 5, 2],
            x_length=11,  # Wider
            y_length=6.5,  # Taller
            axis_config={"color": WHITE, "stroke_width": 5},  # Thicker, white axes
            tips=False
        ).shift(DOWN*0.3)

        # Labels
        x_label = Text("Distance from A (m)", font_size=28, color=WHITE).next_to(
            axes.x_axis, DOWN, buff=0.3
        )
        y_label = Text("Bending Moment (kNm)", font_size=28, color=WHITE).rotate(PI/2).next_to(
            axes.y_axis, LEFT, buff=0.4
        )

        # Moment function (simplified from analysis)
        def moment_func(x):
            """Calculate bending moment at position x (in meters)"""
            R_A = 3.167  # kN
            w = 0.8  # kN/m

            M = R_A * x - 0.5 * w * x**2

            if x >= 1.5:
                M -= 7.0 * (x - 1.5)

            if x >= 3.0:
                M += 11.233 * (x - 3.0)

            if x >= 4.0:
                M -= 4.2 * (x - 4.0)

            return M

        # Create moment curve - THICKER and bright yellow
        moment_curve = axes.plot(
            moment_func,
            x_range=[0, 4.0],
            color=COLORS['moment_pos'],
            stroke_width=10  # Thicker line
        )

        # Fill areas (positive and negative) using get_riemann_rectangles approach
        # Positive region
        x_vals_pos = np.linspace(0, 3.5, 100)
        fill_pos_points = [axes.c2p(0, 0)]
        for x in x_vals_pos:
            fill_pos_points.append(axes.c2p(x, moment_func(x)))
        fill_pos_points.append(axes.c2p(3.5, 0))
        fill_pos = Polygon(*fill_pos_points, color=COLORS['moment_pos'],
                          fill_opacity=0.3, stroke_width=0)

        # Negative region
        x_vals_neg = np.linspace(3.5, 4.0, 50)
        fill_neg_points = [axes.c2p(3.5, 0)]
        for x in x_vals_neg:
            fill_neg_points.append(axes.c2p(x, moment_func(x)))
        fill_neg_points.append(axes.c2p(4.0, 0))
        fill_neg = Polygon(*fill_neg_points, color=COLORS['moment_neg'],
                          fill_opacity=0.3, stroke_width=0)

        # Critical points - BIGGER and more visible
        # Maximum positive moment at ~1.5m
        M_max = moment_func(1.5)
        dot_Mmax = Dot(axes.c2p(1.5, M_max), color="#00ff88", radius=0.14)
        label_Mmax = MathTex(r"M_{\text{max}}", font_size=40,
                            color="#00ff88").next_to(dot_Mmax, UP+LEFT, buff=0.2)

        # Maximum negative moment at x=3.0m (support B)
        M_min_x = 3.0
        M_min = moment_func(M_min_x)
        dot_Mmin = Dot(axes.c2p(M_min_x, M_min), color="#ff3366", radius=0.14)
        label_Mmin = MathTex(r"M_{\text{min}}", font_size=40,
                            color="#ff3366").next_to(dot_Mmin, DOWN+RIGHT, buff=0.2)

        # Reference lines
        line_P1 = DashedLine(axes.c2p(1.5, -6), axes.c2p(1.5, 5),
                            color=COLORS['load_arrow'], stroke_width=2,
                            dash_length=0.15, stroke_opacity=0.5)
        label_line_P1 = Text("P₁", font_size=24, color=COLORS['load_arrow']).next_to(
            axes.c2p(1.5, 5), UP, buff=0.1
        )

        line_B = DashedLine(axes.c2p(3.0, -6), axes.c2p(3.0, 5),
                           color=COLORS['reaction'], stroke_width=2,
                           dash_length=0.15, stroke_opacity=0.5)
        label_line_B = Text("B", font_size=24, color=COLORS['reaction']).next_to(
            axes.c2p(3.0, 5), UP, buff=0.1
        )

        line_P2 = DashedLine(axes.c2p(4.0, -6), axes.c2p(4.0, 5),
                            color=RED, stroke_width=2,
                            dash_length=0.15, stroke_opacity=0.5)
        label_line_P2 = Text("P₂", font_size=24, color=RED).next_to(
            axes.c2p(4.0, 5), UP, buff=0.1
        )

        # Fast animation - title fades in and out first
        self.play(FadeIn(title), run_time=0.4)
        self.wait(0.6)
        self.play(FadeOut(title), run_time=0.4)

        # Show axes and labels quickly
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.6)

        # Show reference lines quickly
        self.play(
            Create(line_P1), Write(label_line_P1),
            Create(line_B), Write(label_line_B),
            Create(line_P2), Write(label_line_P2),
            run_time=0.5
        )

        # Animate moment curve drawing faster
        self.play(Create(moment_curve), run_time=1.5, rate_func=smooth)

        # Add fills quickly
        self.play(FadeIn(fill_pos), FadeIn(fill_neg), run_time=0.6)

        # Highlight critical points faster
        self.play(
            FadeIn(dot_Mmax, scale=1.3), Write(label_Mmax),
            Flash(dot_Mmax, color="#00ff88", flash_radius=0.3),
            run_time=0.5
        )

        self.play(
            FadeIn(dot_Mmin, scale=1.3), Write(label_Mmin),
            Flash(dot_Mmin, color="#ff3366", flash_radius=0.3),
            run_time=0.5
        )

        # Highlight zero crossing
        zero_line = axes.get_horizontal_line(axes.c2p(4, 0),
                                            color=WHITE, stroke_width=4)
        self.play(Create(zero_line), run_time=0.4)

        self.wait(1.0)


# To render individual scenes:
# manim -pql manim_crane_jib_anim.py Scene1_ImageCrane       # Image version
# manim -pql manim_crane_jib_anim.py Scene1_RealCrane        # Animated version
# manim -pql manim_crane_jib_anim.py Scene2_LoadingDiagram
# manim -pql manim_crane_jib_anim.py Scene3_ShearDiagram
# manim -pql manim_crane_jib_anim.py Scene4_MomentDiagram
#
# High quality (1080p60):
# manim -pqh manim_crane_jib_anim.py Scene1_ImageCrane Scene2_LoadingDiagram Scene3_ShearDiagram Scene4_MomentDiagram
#
# To combine all MP4s into one:
# cd media/videos/manim_crane_jib_anim/1080p60
# ffmpeg -i Scene1_ImageCrane.mp4 -i Scene2_LoadingDiagram.mp4 -i Scene3_ShearDiagram.mp4 -i Scene4_MomentDiagram.mp4 \
#   -filter_complex "[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[outv]" -map "[outv]" crane_jib_complete.mp4
#
# To create a lightweight GIF from combined video:
# ffmpeg -i crane_jib_complete.mp4 -vf "fps=10,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
#   -loop 0 crane_jib_complete.gif
