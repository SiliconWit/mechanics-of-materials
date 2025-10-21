#!/usr/bin/env python3
"""
Generate animated GIFs showing different types of beam supports and their behavior.
Each animation demonstrates the constraints and degrees of freedom for each support type.

Author: SiliconWit Mechanics of Materials
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrow, Wedge, Rectangle
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib import font_manager
import os

# Find IBM Plex Sans font
def find_ibm_plex_font():
    """Locate IBM Plex Sans font in the project."""
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to project root (go up several directories)
    project_root = os.path.abspath(os.path.join(script_dir, '../../../../../..'))

    font_paths = [
        # IBM Plex Sans fonts (SemiBold for headings as per typography.css)
        os.path.join(project_root, 'public/fonts/IBM_Plex_Sans/static/IBMPlexSans-SemiBold.ttf'),
        os.path.join(project_root, 'public/fonts/IBM_Plex_Sans/static/IBMPlexSans-Bold.ttf'),
        os.path.join(project_root, 'public/fonts/IBM_Plex_Sans/static/IBMPlexSans-Medium.ttf'),
        # Fallback to system fonts if IBM Plex is not found
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            print(f"Found font: {font_path}")
            font_manager.fontManager.addfont(font_path)
            prop = font_manager.FontProperties(fname=font_path)
            return prop.get_name()

    print("No custom font found, using default")
    return 'sans-serif'

# Load IBM Plex Sans font
ibm_font = find_ibm_plex_font()

# Set style for professional technical diagrams (mobile-friendly)
plt.rcParams.update({
    'font.family': ibm_font,
    'font.size': 28,
    'font.weight': 'bold',
    'axes.linewidth': 4,
    'lines.linewidth': 5,
    'figure.facecolor': '#F8FAFC',  # Light gray background
    'axes.facecolor': '#F8FAFC',
    'savefig.facecolor': '#F8FAFC',
    'savefig.edgecolor': '#5ab9a0'  # Light teal border for saved figure (matching beam_type_diagrams.py)
})

class BeamSupportAnimator:
    """Create animations showing beam support behavior under loading."""

    def __init__(self, output_dir='support_animations'):
        """Initialize the animator with output directory."""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Animation parameters (optimized for smaller file size)
        self.fps = 20  # Reduced from 30 for smaller file size
        self.duration = 2.5  # seconds (reduced from 3.0)
        self.frames = int(self.fps * self.duration)

        # Beam parameters
        self.beam_length = 8.0
        self.beam_height = 0.4

        # Color scheme (matching beam_type_diagrams.py)
        self.beam_color = '#2d7a8f'      # Darker teal with blue undertone
        self.support_color = '#6B7280'   # Gray for triangles/supports
        self.ground_color = '#5ab9a0'    # Light teal for ground/fixed/outlines
        self.force_color = '#ff8c36'     # Orange for applied forces
        self.reaction_color = '#00a0d0'  # Light blue for reactions
        self.text_color = '#1F2937'      # Dark gray for text
        self.border_color = '#5ab9a0'    # Light teal for border (matching ground)
        self.checkmark_color = '#10B981' # Green for ✓
        self.cross_color = '#EF4444'     # Red for ✗
        self.bg_color = '#F8FAFC'        # Light gray background

    def _draw_ground(self, ax, x_center, y_level, width=2.0):
        """Draw ground hatching pattern centered at x_center."""
        x_start = x_center - width/2
        x_end = x_center + width/2

        # Ground line (black)
        ax.plot([x_start, x_end], [y_level, y_level],
                color=self.ground_color, linewidth=3)

        # Hatching (black)
        hatch_spacing = 0.3
        hatch_angle = 45
        hatch_length = 0.4
        num_hatches = int(width / hatch_spacing) + 1

        for i in range(num_hatches):
            x = x_start + i * hatch_spacing
            dx = hatch_length * np.cos(np.radians(hatch_angle))
            dy = -hatch_length * np.sin(np.radians(hatch_angle))
            ax.plot([x, x + dx], [y_level, y_level + dy],
                   color=self.ground_color, linewidth=2)

    def _draw_force_arrow(self, ax, x, y, direction='down', label='F', color=None):
        """Draw a force arrow with label."""
        if color is None:
            color = self.force_color

        arrow_length = 1.0
        arrow_width = 0.15

        if direction == 'down':
            dy = -arrow_length
            dx = 0
        elif direction == 'up':
            dy = arrow_length
            dx = 0
        elif direction == 'right':
            dx = arrow_length
            dy = 0
        elif direction == 'left':
            dx = -arrow_length
            dy = 0

        arrow = FancyArrow(x, y, dx, dy,
                          width=arrow_width,
                          head_width=arrow_width*2,
                          head_length=arrow_length*0.2,
                          fc=color, ec=color, linewidth=2)
        ax.add_patch(arrow)

        # Add label (larger for mobile, positioned close to arrow)
        label_offset = 0.15
        if direction == 'down':
            ax.text(x + label_offset, y - arrow_length/2, label,
                   fontsize=30, fontweight='bold', color=color)
        elif direction == 'up':
            ax.text(x + label_offset, y + arrow_length/2, label,
                   fontsize=30, fontweight='bold', color=color)

    def _draw_pinned_support(self, ax, x, y, scale=1.0):
        """Draw a pinned support symbol."""
        # Triangle (larger)
        triangle_height = 1.0 * scale
        triangle_width = 1.0 * scale

        triangle = Polygon([
            [x, y],
            [x - triangle_width/2, y - triangle_height],
            [x + triangle_width/2, y - triangle_height]
        ], closed=True, fc=self.support_color, ec=self.ground_color, linewidth=5, alpha=0.8)
        ax.add_patch(triangle)

        # Pin circle (black fill with teal edge, larger)
        pin = Circle((x, y), 0.2 * scale, fc='black', ec=self.ground_color, linewidth=5, zorder=10)
        ax.add_patch(pin)

        # Ground (centered at x)
        self._draw_ground(ax, x, y - triangle_height, width=2.5)

    def _draw_roller_support(self, ax, x, y, scale=1.0, ground_x=None):
        """Draw a roller support symbol.

        Args:
            x: X position of the roller support (this moves)
            y: Y position at beam connection
            scale: Scale factor
            ground_x: Fixed X position for ground (if None, uses x)
        """
        if ground_x is None:
            ground_x = x

        # Triangle (moves with x, larger)
        triangle_height = 1.0 * scale
        triangle_width = 1.0 * scale

        triangle = Polygon([
            [x, y],
            [x - triangle_width/2, y - triangle_height],
            [x + triangle_width/2, y - triangle_height]
        ], closed=True, fc=self.support_color, ec=self.ground_color, linewidth=5, alpha=0.8)
        ax.add_patch(triangle)

        # Pin circle at apex (black fill with teal edge, larger) - same as pinned support
        pin = Circle((x, y), 0.2 * scale, fc='black', ec=self.ground_color, linewidth=5, zorder=10)
        ax.add_patch(pin)

        # Rollers (circles) - these move with x (black fill with teal edge, larger)
        roller_y = y - triangle_height - 0.2
        roller1 = Circle((x - 0.3, roller_y), 0.2 * scale,
                        fc='black', ec=self.ground_color, linewidth=5, zorder=10)
        roller2 = Circle((x + 0.3, roller_y), 0.2 * scale,
                        fc='black', ec=self.ground_color, linewidth=5, zorder=10)
        ax.add_patch(roller1)
        ax.add_patch(roller2)

        # Ground - FIXED at ground_x (does not move)
        self._draw_ground(ax, ground_x, roller_y - 0.2, width=2.5)

    def _draw_fixed_support(self, ax, x, y, scale=1.0):
        """Draw a fixed support symbol."""
        wall_width = 0.6 * scale
        wall_height = 1.5 * scale

        # Wall rectangle (gray with black edge, larger)
        wall = FancyBboxPatch(
            (x - wall_width, y - wall_height/2),
            wall_width, wall_height,
            boxstyle="round,pad=0.05",
            fc=self.support_color, ec=self.ground_color, linewidth=5, alpha=0.8
        )
        ax.add_patch(wall)

        # Hatching on the left side of the wall (black, thicker)
        hatch_x = x - wall_width
        hatch_spacing = 0.25
        hatch_angle = 45
        hatch_length = 0.35
        num_hatches = int(wall_height / hatch_spacing) + 1

        for i in range(num_hatches):
            y_pos = (y - wall_height/2) + i * hatch_spacing
            dx = -hatch_length * np.cos(np.radians(hatch_angle))
            dy = -hatch_length * np.sin(np.radians(hatch_angle))
            ax.plot([hatch_x, hatch_x + dx], [y_pos, y_pos + dy],
                   color=self.ground_color, linewidth=4)

    def animate_pinned_support(self):
        """
        Animate a pinned support showing:
        - Beam can rotate at support
        - No vertical or horizontal movement at pin
        - Vertical and horizontal reaction forces
        """
        print("Creating pinned support animation...")

        fig, ax = plt.subplots(figsize=(12, 8))

        # Support location
        support_x = 2.0
        support_y = 0.0

        # Load application point
        load_x = 6.0

        def init():
            ax.clear()
            ax.set_xlim(-1, 10)
            ax.set_ylim(-3, 4)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title('Pinned Support Behavior\n(Allows Rotation, Prevents Translation)',
                        fontsize=18, fontweight='bold', pad=20)
            return []

        def animate(frame):
            ax.clear()
            ax.set_xlim(-1, 10)
            ax.set_ylim(-3, 4)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title('Pinned Support Behavior\n(Allows Rotation, Prevents Translation)',
                        fontsize=18, fontweight='bold', pad=20)

            # Animation phase
            t = frame / self.frames

            # Apply load with sinusoidal variation
            load_magnitude = np.sin(t * 2 * np.pi) * 0.5

            # Beam rotation angle (exaggerated)
            rotation_angle = load_magnitude * 15  # degrees

            # Calculate beam position with rotation about pin
            beam_left = support_x
            beam_right = support_x + self.beam_length

            # Rotate beam about support point
            cos_angle = np.cos(np.radians(rotation_angle))
            sin_angle = np.sin(np.radians(rotation_angle))

            # Beam endpoints
            x1, y1 = support_x, support_y
            x2 = support_x + self.beam_length * cos_angle
            y2 = support_y + self.beam_length * sin_angle

            # Draw beam as rotated rectangle
            beam_corners = np.array([
                [0, -self.beam_height/2],
                [self.beam_length, -self.beam_height/2],
                [self.beam_length, self.beam_height/2],
                [0, self.beam_height/2]
            ])

            # Rotation matrix
            R = np.array([[cos_angle, -sin_angle],
                         [sin_angle, cos_angle]])
            rotated_corners = beam_corners @ R.T
            rotated_corners[:, 0] += support_x
            rotated_corners[:, 1] += support_y

            beam = Polygon(rotated_corners, fc=self.beam_color, ec=self.ground_color,
                          linewidth=2, alpha=0.7)
            ax.add_patch(beam)

            # Draw pinned support
            self._draw_pinned_support(ax, support_x, support_y)

            # Applied load at free end
            load_x_pos = x2
            load_y_pos = y2 + self.beam_height/2
            if abs(load_magnitude) > 0.01:
                self._draw_force_arrow(ax, load_x_pos, load_y_pos, 'down', 'P')

            # Reaction forces at pin (vertical and horizontal)
            if abs(load_magnitude) > 0.01:
                # Vertical reaction
                self._draw_force_arrow(ax, support_x, support_y - 0.3, 'up',
                                     'Ry', self.reaction_color)
                # Horizontal reaction
                self._draw_force_arrow(ax, support_x - 0.3, support_y, 'left',
                                     'Rx', self.reaction_color)

            # Add annotations
            annotation_y = -2.5
            ax.text(5, annotation_y,
                   '✓ Rotation allowed\n✗ Vertical movement prevented\n✗ Horizontal movement prevented',
                   fontsize=14, ha='center',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

            return []

        anim = FuncAnimation(fig, animate, init_func=init,
                           frames=self.frames, interval=1000/self.fps, blit=True)

        output_path = os.path.join(self.output_dir, 'pinned_support.gif')
        writer = PillowWriter(fps=self.fps)
        anim.save(output_path, writer=writer)
        plt.close()

        print(f"✓ Pinned support animation saved to {output_path}")

    def animate_roller_support(self):
        """
        Animate a roller support showing:
        - Beam can rotate at support
        - Horizontal movement allowed (rollers move)
        - No vertical movement
        - Only vertical reaction force
        """
        print("Creating roller support animation...")

        fig, ax = plt.subplots(figsize=(12, 8))

        # Support location
        support_x_initial = 2.0
        support_y = 0.0

        # Load application point
        load_x = 6.0

        def init():
            ax.clear()
            ax.set_xlim(-1, 10)
            ax.set_ylim(-3, 4)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title('Roller Support Behavior\n(Allows Rotation and Horizontal Movement)',
                        fontsize=18, fontweight='bold', pad=20)
            return []

        def animate(frame):
            ax.clear()
            ax.set_xlim(-1, 10)
            ax.set_ylim(-3, 4)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title('Roller Support Behavior\n(Allows Rotation and Horizontal Movement)',
                        fontsize=18, fontweight='bold', pad=20)

            # Animation phase
            t = frame / self.frames

            # Apply load with sinusoidal variation
            load_magnitude = np.sin(t * 2 * np.pi) * 0.5

            # Horizontal movement of support (rollers sliding)
            horizontal_displacement = np.sin(t * 2 * np.pi) * 0.5
            support_x = support_x_initial + horizontal_displacement

            # Beam rotation angle (exaggerated)
            rotation_angle = load_magnitude * 15  # degrees

            # Calculate beam position with rotation about support
            cos_angle = np.cos(np.radians(rotation_angle))
            sin_angle = np.sin(np.radians(rotation_angle))

            # Beam endpoints
            x2 = support_x + self.beam_length * cos_angle
            y2 = support_y + self.beam_length * sin_angle

            # Draw beam as rotated rectangle
            beam_corners = np.array([
                [0, -self.beam_height/2],
                [self.beam_length, -self.beam_height/2],
                [self.beam_length, self.beam_height/2],
                [0, self.beam_height/2]
            ])

            # Rotation matrix
            R = np.array([[cos_angle, -sin_angle],
                         [sin_angle, cos_angle]])
            rotated_corners = beam_corners @ R.T
            rotated_corners[:, 0] += support_x
            rotated_corners[:, 1] += support_y

            beam = Polygon(rotated_corners, fc=self.beam_color, ec=self.ground_color,
                          linewidth=2, alpha=0.7)
            ax.add_patch(beam)

            # Draw roller support (moves horizontally)
            self._draw_roller_support(ax, support_x, support_y)

            # Applied load at free end
            load_x_pos = x2
            load_y_pos = y2 + self.beam_height/2
            if abs(load_magnitude) > 0.01:
                self._draw_force_arrow(ax, load_x_pos, load_y_pos, 'down', 'P')

            # Vertical reaction only (no horizontal reaction)
            if abs(load_magnitude) > 0.01:
                self._draw_force_arrow(ax, support_x, support_y - 1.2, 'up',
                                     'Ry', self.reaction_color)

            # Show horizontal movement with arrow
            if abs(horizontal_displacement) > 0.05:
                direction = 'right' if horizontal_displacement > 0 else 'left'
                ax.annotate('', xy=(support_x, -2.0),
                           xytext=(support_x_initial, -2.0),
                           arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
                ax.text(support_x_initial + horizontal_displacement/2, -2.3,
                       'Horizontal\nmovement', ha='center', fontsize=12, color='purple')

            # Add annotations
            annotation_y = -2.5
            ax.text(5, annotation_y - 0.5,
                   '✓ Rotation allowed\n✓ Horizontal movement allowed\n✗ Vertical movement prevented',
                   fontsize=14, ha='center',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

            return []

        anim = FuncAnimation(fig, animate, init_func=init,
                           frames=self.frames, interval=1000/self.fps, blit=True)

        output_path = os.path.join(self.output_dir, 'roller_support.gif')
        writer = PillowWriter(fps=self.fps)
        anim.save(output_path, writer=writer)
        plt.close()

        print(f"✓ Roller support animation saved to {output_path}")

    def animate_fixed_support(self):
        """
        Animate a fixed support showing:
        - No rotation allowed
        - No vertical movement
        - No horizontal movement
        - Moment reaction, vertical and horizontal reactions
        """
        print("Creating fixed support animation...")

        fig, ax = plt.subplots(figsize=(12, 8))

        # Support location
        support_x = 2.0
        support_y = 0.0

        def init():
            ax.clear()
            ax.set_xlim(-1, 10)
            ax.set_ylim(-3, 4)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title('Fixed Support Behavior\n(Prevents All Movement and Rotation)',
                        fontsize=18, fontweight='bold', pad=20)
            return []

        def animate(frame):
            ax.clear()
            ax.set_xlim(-1, 10)
            ax.set_ylim(-3, 4)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title('Fixed Support Behavior\n(Prevents All Movement and Rotation)',
                        fontsize=18, fontweight='bold', pad=20)

            # Animation phase
            t = frame / self.frames

            # Apply load with sinusoidal variation
            load_magnitude = np.sin(t * 2 * np.pi) * 0.5

            # Beam deflection (only elastic deformation, no rotation at support)
            # Cantilever beam deflection curve
            x_beam = np.linspace(0, self.beam_length, 50)

            # Deflection shape for cantilever with end load (exaggerated)
            deflection_scale = load_magnitude * 1.5
            y_deflection = deflection_scale * (x_beam / self.beam_length) ** 2

            # Draw deflected beam
            x_points = support_x + x_beam
            y_top = support_y + y_deflection + self.beam_height/2
            y_bottom = support_y + y_deflection - self.beam_height/2

            # Create beam polygon
            beam_x = np.concatenate([x_points, x_points[::-1]])
            beam_y = np.concatenate([y_top, y_bottom[::-1]])

            beam = Polygon(np.column_stack([beam_x, beam_y]),
                          fc=self.beam_color, ec=self.ground_color, linewidth=2, alpha=0.7)
            ax.add_patch(beam)

            # Draw fixed support
            self._draw_fixed_support(ax, support_x, support_y)

            # Applied load at free end
            load_x_pos = x_points[-1]
            load_y_pos = y_top[-1]
            if abs(load_magnitude) > 0.01:
                self._draw_force_arrow(ax, load_x_pos, load_y_pos, 'down', 'P')

            # Reaction forces and moment at fixed support
            if abs(load_magnitude) > 0.01:
                # Vertical reaction
                self._draw_force_arrow(ax, support_x + 0.3, support_y - 0.3, 'up',
                                     'Ry', self.reaction_color)
                # Horizontal reaction (minimal in this case, but shown for completeness)
                # self._draw_force_arrow(ax, support_x + 0.5, support_y, 'left',
                #                      'Rx', self.reaction_color)

                # Moment reaction (curved arrow)
                moment_arc = Wedge((support_x + 0.5, support_y), 0.6, -30, 210,
                                  width=0.15, fc='none', ec=self.reaction_color,
                                  linewidth=3)
                ax.add_patch(moment_arc)
                ax.text(support_x + 0.5, support_y + 1.0, 'M',
                       fontsize=16, fontweight='bold', color=self.reaction_color)

                # Add small arrowhead to moment arc
                arrow_angle = np.radians(210)
                arrow_r = 0.6
                arrow_x = support_x + 0.5 + arrow_r * np.cos(arrow_angle)
                arrow_y = support_y + arrow_r * np.sin(arrow_angle)
                ax.plot(arrow_x, arrow_y, marker='>', markersize=12,
                       color=self.reaction_color)

            # Show that beam slope at support = 0 (no rotation)
            if abs(load_magnitude) < 0.05:
                # Draw horizontal reference line at support
                ax.plot([support_x, support_x + 1.5], [support_y, support_y],
                       'r--', linewidth=2, label='No rotation')
                ax.text(support_x + 1.5, support_y + 0.2, 'θ = 0°',
                       fontsize=12, color='red', fontweight='bold')

            # Add annotations
            annotation_y = -2.5
            ax.text(5, annotation_y,
                   '✗ Rotation prevented\n✗ Vertical movement prevented\n✗ Horizontal movement prevented',
                   fontsize=14, ha='center',
                   bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

            return []

        anim = FuncAnimation(fig, animate, init_func=init,
                           frames=self.frames, interval=1000/self.fps, blit=True)

        output_path = os.path.join(self.output_dir, 'fixed_support.gif')
        writer = PillowWriter(fps=self.fps)
        anim.save(output_path, writer=writer)
        plt.close()

        print(f"✓ Fixed support animation saved to {output_path}")

    def animate_comparison(self):
        """
        Create a side-by-side comparison of all three support types under same loading.
        """
        print("Creating support comparison animation...")

        # Large figure size for mobile viewing
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 8))
        fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.08, wspace=0.02)

        # Add teal border around entire figure
        fig.patch.set_edgecolor(self.border_color)
        fig.patch.set_linewidth(8)

        support_y = 0.0
        beam_length = 5.0
        beam_height = 0.5  # Larger beam for visibility

        # Fixed position for roller ground (shifted left)
        roller_ground_x = 0.7

        def init():
            for ax in [ax1, ax2, ax3]:
                ax.clear()
                ax.set_xlim(-0.3, 6.3)
                ax.set_ylim(-2.5, 2.5)
                ax.set_aspect('equal')
                ax.axis('off')
            return []

        def animate(frame):
            for ax in [ax1, ax2, ax3]:
                ax.clear()
                ax.set_xlim(-0.3, 6.3)
                ax.set_ylim(-2.5, 2.5)
                ax.set_aspect('equal')
                ax.axis('off')

            t = frame / self.frames
            load_magnitude = np.sin(t * 2 * np.pi) * 0.5

            # PINNED SUPPORT (ax1)
            support_x = 1.0
            rotation_angle = load_magnitude * 15

            cos_angle = np.cos(np.radians(rotation_angle))
            sin_angle = np.sin(np.radians(rotation_angle))

            beam_corners = np.array([
                [0, -beam_height/2],
                [beam_length, -beam_height/2],
                [beam_length, beam_height/2],
                [0, beam_height/2]
            ])

            R = np.array([[cos_angle, -sin_angle], [sin_angle, cos_angle]])
            rotated_corners = beam_corners @ R.T
            rotated_corners[:, 0] += support_x
            rotated_corners[:, 1] += support_y

            beam = Polygon(rotated_corners, fc=self.beam_color, ec=self.ground_color,
                          linewidth=3, alpha=0.7)
            ax1.add_patch(beam)
            self._draw_pinned_support(ax1, support_x, support_y, scale=0.8)

            x2 = support_x + beam_length * cos_angle
            y2 = support_y + beam_length * sin_angle

            # Force follows beam direction (opposite of load_magnitude)
            if abs(load_magnitude) > 0.01:
                force_dir = 'up' if load_magnitude > 0 else 'down'
                force_offset = -beam_height/2 if load_magnitude > 0 else beam_height/2
                self._draw_force_arrow(ax1, x2, y2 + force_offset, force_dir, 'P')

            # Title
            ax1.text(3.0, 2.3, 'Pinned', ha='center', fontsize=34,
                    color=self.text_color, fontweight='bold')

            # Labels with colored checkmarks/crosses
            ax1.text(2.5, -2.0, '✓', ha='center', fontsize=32,
                    color=self.checkmark_color, fontweight='bold')
            ax1.text(2.85, -2.0, 'Rotation', ha='left', fontsize=28,
                    color=self.checkmark_color, fontweight='bold')
            ax1.text(2.5, -2.45, '✗', ha='center', fontsize=32,
                    color=self.cross_color, fontweight='bold')
            ax1.text(2.85, -2.45, 'Translation', ha='left', fontsize=28,
                    color=self.cross_color, fontweight='bold')

            # ROLLER SUPPORT (ax2)
            horizontal_displacement = np.sin(t * 2 * np.pi) * 0.3
            support_x_roller = roller_ground_x + horizontal_displacement

            rotated_corners = beam_corners @ R.T
            rotated_corners[:, 0] += support_x_roller
            rotated_corners[:, 1] += support_y

            beam = Polygon(rotated_corners, fc=self.beam_color, ec=self.ground_color,
                          linewidth=3, alpha=0.7)
            ax2.add_patch(beam)
            # Ground stays fixed at roller_ground_x, but support moves to support_x_roller
            self._draw_roller_support(ax2, support_x_roller, support_y, scale=0.8, ground_x=roller_ground_x)

            x2 = support_x_roller + beam_length * cos_angle
            y2 = support_y + beam_length * sin_angle

            # Force follows beam direction (opposite of load_magnitude)
            if abs(load_magnitude) > 0.01:
                force_dir = 'up' if load_magnitude > 0 else 'down'
                force_offset = -beam_height/2 if load_magnitude > 0 else beam_height/2
                self._draw_force_arrow(ax2, x2, y2 + force_offset, force_dir, 'P')

            # Title
            ax2.text(3.0, 2.3, 'Roller', ha='center', fontsize=34,
                    color=self.text_color, fontweight='bold')

            # Labels with colored checkmarks/crosses
            ax2.text(2.5, -2.0, '✓', ha='center', fontsize=32,
                    color=self.checkmark_color, fontweight='bold')
            ax2.text(2.85, -2.0, 'Rotation', ha='left', fontsize=28,
                    color=self.checkmark_color, fontweight='bold')
            ax2.text(2.5, -2.45, '✓', ha='center', fontsize=32,
                    color=self.checkmark_color, fontweight='bold')
            ax2.text(2.85, -2.45, 'Translation', ha='left', fontsize=28,
                    color=self.checkmark_color, fontweight='bold')

            # FIXED SUPPORT (ax3)
            support_x = 1.0

            x_beam = np.linspace(0, beam_length, 50)
            deflection_scale = load_magnitude * 1.0
            y_deflection = deflection_scale * (x_beam / beam_length) ** 2

            x_points = support_x + x_beam
            y_top = support_y + y_deflection + beam_height/2
            y_bottom = support_y + y_deflection - beam_height/2

            beam_x = np.concatenate([x_points, x_points[::-1]])
            beam_y = np.concatenate([y_top, y_bottom[::-1]])

            beam = Polygon(np.column_stack([beam_x, beam_y]),
                          fc=self.beam_color, ec=self.ground_color, linewidth=3, alpha=0.7)
            ax3.add_patch(beam)
            self._draw_fixed_support(ax3, support_x, support_y, scale=0.8)

            # Force follows beam direction (deflection) - opposite of load_magnitude
            if abs(load_magnitude) > 0.01:
                force_dir = 'up' if load_magnitude > 0 else 'down'
                force_y = y_bottom[-1] if load_magnitude > 0 else y_top[-1]
                self._draw_force_arrow(ax3, x_points[-1], force_y, force_dir, 'P')

            # Title
            ax3.text(3.0, 2.3, 'Fixed', ha='center', fontsize=34,
                    color=self.text_color, fontweight='bold')

            # Labels with colored checkmarks/crosses
            ax3.text(2.5, -2.0, '✗', ha='center', fontsize=32,
                    color=self.cross_color, fontweight='bold')
            ax3.text(2.85, -2.0, 'Rotation', ha='left', fontsize=28,
                    color=self.cross_color, fontweight='bold')
            ax3.text(2.5, -2.45, '✗', ha='center', fontsize=32,
                    color=self.cross_color, fontweight='bold')
            ax3.text(2.85, -2.45, 'Translation', ha='left', fontsize=28,
                    color=self.cross_color, fontweight='bold')

            # Add subtle watermark at bottom right
            fig.text(0.98, 0.05, 'SiliconWit.COM', ha='right', va='bottom',
                    fontsize=18, color='#CBD5E1', alpha=0.4, weight='normal')

            return []

        anim = FuncAnimation(fig, animate, init_func=init,
                           frames=self.frames, interval=1000/self.fps, blit=True)

        output_path = os.path.join(self.output_dir, 'support_comparison.gif')
        writer = PillowWriter(fps=self.fps)
        # Save with reduced DPI for smaller file size (default is 100)
        anim.save(output_path, writer=writer, dpi=80)
        plt.close()

        print(f"✓ Support comparison animation saved to {output_path}")

    def create_all_animations(self):
        """Generate all support type animations."""
        print("\n" + "="*60)
        print("BEAM SUPPORT ANIMATIONS GENERATOR")
        print("="*60 + "\n")

        # Only generate the comparison animation
        self.animate_comparison()

        print("\n" + "="*60)
        print("✓ Animation completed successfully!")
        print(f"Output directory: {os.path.abspath(self.output_dir)}")
        print("="*60 + "\n")


if __name__ == "__main__":
    # Create animator instance
    animator = BeamSupportAnimator()

    # Generate all animations
    animator.create_all_animations()
