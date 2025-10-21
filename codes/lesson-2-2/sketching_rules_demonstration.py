#!/usr/bin/env python3
"""
Shear Force and Bending Moment Diagram Sketching Rules Demonstration
Visual guide for quick freehand sketching techniques
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Color scheme matching pantograph analysis style
COLORS = {
    'beam': '#405ab9',
    'load_arrow': '#ff8c36',
    'reaction': '#00a0d0',
    'moment_pos': '#405ab9',
    'moment_neg': '#ff8c36',
    'text': '#405ab9',
    'grid': '#9ea388',
    'background': 'none',
    'support': '#405ab9'
}

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_plot_style():
    """Configure matplotlib for consistent styling - matching pantograph style."""
    plt.rcParams.update({
        'font.size': 36,
        'axes.titlesize': 42,
        'axes.labelsize': 38,
        'xtick.labelsize': 34,
        'ytick.labelsize': 34,
        'legend.fontsize': 34,
        'figure.titlesize': 44,
        'lines.linewidth': 5,
        'axes.linewidth': 4,
        'xtick.major.width': 4,
        'ytick.major.width': 4,
        'xtick.major.size': 10,
        'ytick.major.size': 10,
        'figure.facecolor': 'none',
        'axes.facecolor': 'none',
        'savefig.facecolor': 'none',
        'savefig.edgecolor': 'none',
        'axes.edgecolor': COLORS['text'],
        'axes.labelcolor': COLORS['text'],
        'xtick.color': COLORS['text'],
        'ytick.color': COLORS['text'],
        'text.color': COLORS['text']
    })

class SketchingRulesDemonstration:
    """Demonstrates pattern progression from loading to shear to moment diagrams."""

    def __init__(self):
        setup_plot_style()

    def create_integration_pattern_diagram(self):
        """
        Shows the integration-like pattern in 3 columns:
        Column 1: Point load → Horizontal line → Slope
        Column 2: UDL → Slope → Parabola
        Column 3: Triangular load → Parabola → Cubic
        """
        fig, axes = plt.subplots(3, 3, figsize=(14, 11))
        fig.patch.set_facecolor(COLORS['background'])

        column_titles = [
            'Point Load',
            'Uniformly Distributed Load',
            'Triangular Load'
        ]

        diagram_types = ['Loading Diagram', 'Shear Force (V)', 'Bending Moment (M)']

        for col in range(3):
            for row in range(3):
                ax = axes[row, col]
                ax.set_xlim(0, 10)
                ax.set_ylim(-2.5, 2.5)
                ax.axhline(0, color=COLORS['text'], linewidth=1.5, linestyle='-', alpha=0.3)

                x = np.linspace(2, 8, 200)

                # Column 0: Point load → Horizontal → Slope
                if col == 0:
                    if row == 0:  # Point load
                        ax.arrow(5, 0, 0, -1.8, head_width=0.4, head_length=0.3,
                               fc=COLORS['load_arrow'], ec=COLORS['text'], linewidth=2.5)
                        ax.text(5, 0.3, 'Point Load', ha='center', fontsize=20,
                               fontweight='bold', color=COLORS['load_arrow'])
                    elif row == 1:  # Horizontal line (constant shear)
                        ax.plot([2, 8], [-1.2, -1.2], color=COLORS['moment_pos'], linewidth=4)
                        ax.plot(2, -1.2, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)
                        ax.plot(8, -1.2, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)
                    elif row == 2:  # Slope (linear moment)
                        ax.plot([2, 8], [0, -2], color=COLORS['moment_pos'], linewidth=4)
                        ax.plot(2, 0, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)
                        ax.plot(8, -2, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)

                # Column 1: UDL → Slope → Parabola
                elif col == 1:
                    if row == 0:  # Uniformly distributed load
                        # Draw multiple downward arrows
                        for pos in np.linspace(2.2, 7.8, 8):
                            ax.arrow(pos, 0, 0, -1.2, head_width=0.25, head_length=0.2,
                                   fc=COLORS['load_arrow'], ec=COLORS['text'], linewidth=2)
                        ax.text(5, 0.3, 'Uniformly Distributed Load', ha='center', fontsize=20,
                               fontweight='bold', color=COLORS['load_arrow'])
                    elif row == 1:  # Slope (linear shear from UDL)
                        ax.plot([2, 8], [1.5, -1.5], color=COLORS['moment_pos'], linewidth=4)
                        ax.plot(2, 1.5, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)
                        ax.plot(8, -1.5, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)
                    elif row == 2:  # Parabolic curve (quadratic moment) - match col 3 row 2 shape
                        # Make it exactly like column 3 row 2: horizontally wide, starting high, ending low
                        y_para = -0.05 * (x - 2)**2 + 1.5
                        ax.plot(x, y_para, color=COLORS['moment_pos'], linewidth=4)
                        ax.plot(2, 1.5, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)
                        ax.plot(8, -0.3, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)

                # Column 2: Triangular load → Parabola → Cubic
                elif col == 2:
                    if row == 0:  # Triangular distributed load
                        x_tri = np.linspace(2, 8, 100)
                        y_tri = -1.5 * (x_tri - 2) / 6
                        ax.fill_between(x_tri, y_tri, 0, color=COLORS['load_arrow'], alpha=0.3)
                        ax.plot(x_tri, y_tri, color=COLORS['load_arrow'], linewidth=3.5)
                        # Add some arrows to show varying load
                        for i, pos in enumerate(np.linspace(2.5, 7.5, 5)):
                            arrow_len = -0.3 * (i + 1)
                            ax.arrow(pos, 0, 0, arrow_len, head_width=0.2, head_length=0.15,
                                   fc=COLORS['load_arrow'], ec=COLORS['text'], linewidth=1.5, alpha=0.7)
                        ax.text(5, 0.3, 'Triangular Distributed Load', ha='center', fontsize=20,
                               fontweight='bold', color=COLORS['load_arrow'])
                    elif row == 1:  # Parabolic curve (shear from triangular load) - moved up to be visible
                        y_para = -0.05 * (x - 2)**2 + 1.5
                        ax.plot(x, y_para, color=COLORS['moment_pos'], linewidth=4)
                        ax.plot(2, 1.5, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)
                        ax.plot(8, -0.3, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)
                    elif row == 2:  # Cubic curve (moment from triangular load) - moved up to be visible
                        y_cubic = -0.0012 * (x - 2)**3 + 1.5
                        ax.plot(x, y_cubic, color=COLORS['moment_pos'], linewidth=4)
                        ax.plot(2, 1.5, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)
                        ax.plot(8, 0.94, 'o', markersize=16, color='#FFFFFF',
                               markeredgewidth=4, markerfacecolor=COLORS['moment_neg'],
                               markeredgecolor=COLORS['text'], zorder=5)

                # Styling
                ax.set_xticks([])
                ax.set_yticks([])
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.axhline(0, color=COLORS['text'], linewidth=1.5, alpha=0.3)

                # Y-axis labels for diagram types
                if col == 0:
                    ax.text(-1.5, 0, diagram_types[row], fontsize=18, fontweight='bold',
                           color=COLORS['text'], rotation=90, va='center', ha='center')

        plt.tight_layout()

        output_path = os.path.join(SCRIPT_DIR, 'sketching_integration_pattern.svg')
        plt.savefig(output_path, format='svg', dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'], edgecolor='none')
        print(f"✓ Created: {output_path}")
        plt.close()

    def create_slope_direction_guide(self):
        """
        Shows how to determine slope direction in shear diagrams
        and resulting curve shape in moment diagrams with wider curves
        and inverted car visualization.
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.patch.set_facecolor(COLORS['background'])

        cases = [
            {'name': 'Right Slope "/" (Positive)', 'direction': 'right'},
            {'name': 'Left Slope "\\\\" (Negative)', 'direction': 'left'}
        ]

        for col, case in enumerate(cases):
            # Shear Force Diagram (top row)
            ax_shear = axes[0, col]
            ax_shear.set_xlim(0, 12)
            ax_shear.set_ylim(-2, 2.5)
            ax_shear.axhline(2.22, color=COLORS['text'], linewidth=3, linestyle='-', alpha=0.4)
            ax_shear.grid(True, alpha=0.2, color=COLORS['grid'])

            if case['direction'] == 'right':
                # Positive slope (going up to the right)
                ax_shear.plot([2, 10], [-1, 1.5], color=COLORS['moment_pos'], linewidth=5)
                ax_shear.plot(2, -1, 'o', markersize=18, color='#FFFFFF',
                            markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                            markeredgecolor=COLORS['text'], zorder=5)
                ax_shear.plot(10, 1.5, 'o', markersize=18, color='#FFFFFF',
                            markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                            markeredgecolor=COLORS['text'], zorder=5)

                # Annotations
                ax_shear.annotate('Fast', xy=(2, -1), xytext=(2.5, 1.95),
                               fontsize=12, ha='right', color=COLORS['text'], fontweight='bold',
                               arrowprops=dict(arrowstyle='->', lw=2.5, color=COLORS['reaction']))
                ax_shear.annotate('Slow', xy=(10, 1.5), xytext=(9.6, 2),
                               fontsize=12, ha='left', color=COLORS['text'], fontweight='bold',
                               arrowprops=dict(arrowstyle='->', lw=2.5, color=COLORS['reaction']))
            else:
                # Negative slope (going down to the right)
                ax_shear.plot([2, 10], [1.5, -1], color=COLORS['moment_pos'], linewidth=5)
                ax_shear.plot(2, 1.5, 'o', markersize=18, color='#FFFFFF',
                            markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                            markeredgecolor=COLORS['text'], zorder=5)
                ax_shear.plot(10, -1, 'o', markersize=18, color='#FFFFFF',
                            markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                            markeredgecolor=COLORS['text'], zorder=5)

                # Annotations
                ax_shear.annotate('Slow', xy=(2, 1.5), xytext=(2.4, 2),
                               fontsize=12, ha='right', color=COLORS['text'], fontweight='bold',
                               arrowprops=dict(arrowstyle='->', lw=2.5, color=COLORS['reaction']))
                ax_shear.annotate('Fast', xy=(10, -1), xytext=(9.6, 1.95),
                               fontsize=12, ha='left', color=COLORS['text'], fontweight='bold',
                               arrowprops=dict(arrowstyle='->', lw=2.5, color=COLORS['reaction']))

            ax_shear.set_ylabel('Shear Force', fontsize=20, fontweight='bold', color=COLORS['text'])
            ax_shear.set_xticks([])
            ax_shear.set_yticks([])

            # Bending Moment Diagram (bottom row) - MUCH WIDER curves (horizontally wide, vertically narrow)
            ax_moment = axes[1, col]
            ax_moment.set_xlim(0, 12)
            ax_moment.set_ylim(-0.5, 2.5)
            ax_moment.axhline(2.22, color=COLORS['text'], linewidth=1.5, linestyle='-', alpha=0.4)
            ax_moment.grid(True, alpha=0.2, color=COLORS['grid'])

            x = np.linspace(2, 10, 300)

            if case['direction'] == 'right':
                # For positive slope: starts flat (slow), ends steep (fast)
                # Concave up parabola - VERY WIDE horizontally, narrow vertically (like Rule 1 col 3 row 2)
                y = -0.03 * (x - 10)**2 +2
                ax_moment.plot(x, y, color=COLORS['moment_pos'], linewidth=5)
                ax_moment.plot(1.9, 0, 'o', markersize=18, color='#FFFFFF',
                             markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                             markeredgecolor=COLORS['text'], zorder=5)
                ax_moment.plot(10, 2, 'o', markersize=18, color='#FFFFFF',
                             markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                             markeredgecolor=COLORS['text'], zorder=5)

                # Show tangent lines to illustrate flat vs steep regions
#                ax_moment.plot([2, 4.5], [0, 0.08], '--', color=COLORS['reaction'],
#                             linewidth=3, alpha=0.7, label='Flat (slow)')
#                ax_moment.plot([7.5, 10], [1.51, 3.5], '--', color=COLORS['load_arrow'],
#                             linewidth=3, alpha=0.7, label='Steep (fast)')

                # Draw car BELOW the curve at start (slow region) with wheels touching from below
                car_x = 3.5
                curve_y = 0.05 * (car_x - 2)**2  +0.75 # Get y value on curve
                car_y = curve_y - 0.45  # Position car body below curve

                car_body = patches.FancyBboxPatch((car_x - 0.3, car_y), 0.6, 0.1,
                                                 boxstyle="round,pad=0.05",
                                                 facecolor='#404040', edgecolor=COLORS['text'],
                                                 linewidth=2, transform=ax_moment.transData, zorder=10)
                ax_moment.add_patch(car_body)
                # Wheels touching curve from BELOW
                ax_moment.plot([car_x - 0.15, car_x + 0.15], [car_y + 0.17, car_y + 0.17], 'o',
                             markersize=10, color='#202020', markeredgecolor=COLORS['text'],
                             markeredgewidth=2, zorder=11)

#                ax_moment.text(6, 1.5, 'Flat → Steep\n(Concave Up)', ha='center',
#                             fontsize=12, color=COLORS['text'], fontweight='bold',
#                             bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
#                                      edgecolor=COLORS['text'], alpha=0.9))
            else:
                # For negative slope: starts steep (fast), ends flat (slow)
                # Concave down parabola - VERY WIDE horizontally, narrow vertically
                y = -0.025 + 0.03 * (x - 2)**2
                ax_moment.plot(x, y, color=COLORS['moment_pos'], linewidth=5)
                ax_moment.plot(1.9, 0, 'o', markersize=18, color='#FFFFFF',
                             markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                             markeredgecolor=COLORS['text'], zorder=5)
                ax_moment.plot(10, 1.9, 'o', markersize=18, color='#FFFFFF',
                             markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                             markeredgecolor=COLORS['text'], zorder=5)

                # Show tangent lines
#                ax_moment.plot([2, 4.5], [3.2, 3.12], '--', color=COLORS['load_arrow'],
#                             linewidth=3, alpha=0.7, label='Steep (fast)')
#                ax_moment.legend('Steep (fast)')
#                ax_moment.plot([7.5, 10], [1.69, -0.3], '--', color=COLORS['reaction'],
#                             linewidth=3, alpha=0.7, label='Flat (slow)')

                # Draw car BELOW the curve at end (slow region) with wheels touching from below
                car_x = 8.5
                curve_y = 3.3 - 0.05 * (car_x - 2)**2 +0.2 # Get y value on curve
                car_y = curve_y - 0.45  # Position car body below curve

                car_body = patches.FancyBboxPatch((car_x - 0.3, car_y), 0.6, 0.1,
                                                 boxstyle="round,pad=0.05",
                                                 facecolor='#404040', edgecolor=COLORS['text'],
                                                 linewidth=2, transform=ax_moment.transData, zorder=10)
                ax_moment.add_patch(car_body)
                # Wheels touching curve from BELOW
                ax_moment.plot([car_x - 0.15, car_x + 0.15], [car_y + 0.17, car_y + 0.17], 'o',
                             markersize=10, color='#202020', markeredgecolor=COLORS['text'],
                             markeredgewidth=2, zorder=11)

#                ax_moment.text(6, 1.6, 'Steep → Flat\n(Concave Down)', ha='center',
#                             fontsize=12, color=COLORS['text'], fontweight='bold',
#                             bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
#                                      edgecolor=COLORS['text'], alpha=0.9))

            ax_moment.set_ylabel('Bending Moment', fontsize=20, fontweight='bold', color=COLORS['text'])
            ax_moment.set_xlabel('Distance along beam', fontsize=18, color=COLORS['text'])
            ax_moment.set_xticks([])
            ax_moment.set_yticks([])
            ax_moment.legend(loc='upper left', fontsize=16, framealpha=0.9)

        plt.tight_layout()

        output_path = os.path.join(SCRIPT_DIR, 'sketching_slope_direction_guide.svg')
        plt.savefig(output_path, format='svg', dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'], edgecolor='none')
        print(f"✓ Created: {output_path}")
        plt.close()

    def create_boundary_conditions_cheatsheet(self):
        """
        This function is no longer needed - boundary conditions will be
        presented as text in the lesson content.
        """
        # This diagram is no longer created as per user request
        pass

def main():
    """Generate all sketching rule demonstration diagrams."""
    print("\n" + "="*60)
    print("Generating Shear & Moment Sketching Rules Diagrams")
    print("="*60 + "\n")

    demo = SketchingRulesDemonstration()

    print("Creating demonstration diagrams...")
    demo.create_integration_pattern_diagram()
    demo.create_slope_direction_guide()
    demo.create_boundary_conditions_cheatsheet()

    print("\n" + "="*60)
    print("✓ All sketching rules diagrams generated successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
