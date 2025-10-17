#!/usr/bin/env python3
"""
3D Printer Gantry Rail Bending Analysis
Application 1: Simply supported beam with moving concentrated load

This script generates:
1. Loading diagram showing moving print head
2. Shear force diagram for critical load position (midspan)
3. Bending moment diagram for critical load position (midspan)

Author: SiliconWit Engineering Team
Date: 2025-10-17
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrow, Circle, Rectangle
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# Set up matplotlib for mobile-friendly plots with transparent background (matching pantograph style)
plt.rcParams.update({
    'font.size': 28,
    'axes.titlesize': 32,
    'axes.labelsize': 30,
    'xtick.labelsize': 26,
    'ytick.labelsize': 26,
    'legend.fontsize': 26,
    'figure.titlesize': 34,
    'lines.linewidth': 5,
    'axes.linewidth': 4,
    'xtick.major.width': 4,
    'ytick.major.width': 4,
    'xtick.major.size': 10,
    'ytick.major.size': 10,
    'figure.facecolor': 'none',
    'axes.facecolor': 'none',
    'savefig.facecolor': 'none',
    'savefig.edgecolor': 'none'
})

# Color scheme (matching pantograph analysis - NO BLACK!)
COLORS = {
    'beam': '#405ab9',           # Blue for beam
    'support': '#405ab9',         # Blue for supports
    'load_arrow': '#ff8c36',     # Orange for loads
    'shear_pos': '#405ab9',      # Blue for positive shear
    'shear_neg': '#ff8c36',      # Orange for negative shear
    'moment_pos': '#405ab9',     # Blue for positive moment
    'moment_neg': '#ff8c36',     # Orange for negative moment
    'text': '#405ab9',           # Blue for all text/axes/labels (NO BLACK!)
    'grid': '#9ea388',           # Gray-green for grid
    'dimension': '#7f8c8d'       # Medium gray for dimensions
}

class GantryRailAnalysis:
    """Analyzes bending in a 3D printer gantry rail with moving load"""

    def __init__(self):
        # Geometric properties (all in mm)
        self.L = 1200  # Beam span

        # Loading conditions
        self.P = 250  # Print head load (N)

        # Critical position for diagrams (midspan - worst case)
        self.a = 600  # Load position (mm) - at midspan for maximum moment

        # Calculate support reactions at critical position
        self.R_A = self.P * (self.L - self.a) / self.L  # Reaction at A
        self.R_B = self.P * self.a / self.L              # Reaction at B

        # Cross-section properties
        self.I = 2.2e6  # mm^4
        self.c = 25     # mm
        self.S = self.I / self.c  # Section modulus

        # Material properties
        self.sigma_yield = 275  # MPa
        self.E = 69000  # MPa (Aluminum 6061-T6)

    def plot_loading_diagram(self):
        """Generate loading diagram showing simply supported beam with moving load"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))

        # Draw beam
        beam_y = 0
        beam_height = 0.03
        beam = Rectangle((0, beam_y - beam_height/2), self.L/1000, beam_height,
                         facecolor=COLORS['beam'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(beam)

        # Draw support A (pin support - triangle)
        support_A_x = 0
        support_A_y = beam_y - beam_height/2
        triangle_A = np.array([[support_A_x - 0.04, support_A_y - 0.08],
                               [support_A_x + 0.04, support_A_y - 0.08],
                               [support_A_x, support_A_y]])
        ax.add_patch(mpatches.Polygon(triangle_A, closed=True,
                                     facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3))

        # Draw support B (roller support - triangle on circle)
        support_B_x = self.L/1000
        support_B_y = beam_y - beam_height/2
        triangle_B = np.array([[support_B_x - 0.04, support_B_y - 0.08],
                               [support_B_x + 0.04, support_B_y - 0.08],
                               [support_B_x, support_B_y]])
        ax.add_patch(mpatches.Polygon(triangle_B, closed=True,
                                     facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3))

        # Add circles under roller support
        circle_B = Circle((support_B_x, support_B_y - 0.1), 0.02,
                         facecolor='white', edgecolor=COLORS['text'], linewidth=2)
        ax.add_patch(circle_B)

        # Draw ground lines
        ax.plot([-0.08, 0.08], [-0.16, -0.16], color=COLORS['support'], linewidth=3)
        ax.plot([support_B_x - 0.08, support_B_x + 0.08], [-0.12, -0.12],
               color=COLORS['support'], linewidth=3)

        # Add hatching for ground
        for i in range(-4, 5):
            ax.plot([i*0.02, i*0.02 - 0.02], [-0.16, -0.18],
                   color=COLORS['support'], linewidth=2)
        for i in range(-4, 5):
            ax.plot([support_B_x + i*0.02, support_B_x + i*0.02 - 0.02],
                   [-0.12, -0.14], color=COLORS['support'], linewidth=2)

        # Draw print head load at critical position (midspan)
        load_x = self.a / 1000
        load_y = beam_y + beam_height/2
        arrow_length = 0.15
        arrow_width = 0.18

        # Load arrow
        ax.arrow(load_x, load_y + arrow_length, 0, -arrow_length + 0.01,
                head_width=arrow_width*0.22, head_length=0.03, fc=COLORS['load_arrow'],
                ec=COLORS['load_arrow'], linewidth=3, zorder=5)

        # Load label
        ax.text(load_x, load_y + arrow_length + 0.05, f'P = {self.P} N\n(Print Head)',
               ha='center', va='bottom', fontsize=24, fontweight='bold',
               color=COLORS['load_arrow'],
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['load_arrow'], alpha=0.9))

        # Draw reaction forces
        # Reaction at A
        ax.arrow(0, support_A_y - 0.25, 0, 0.13,
                head_width=arrow_width*0.22, head_length=0.03, fc=COLORS['moment_pos'],
                ec=COLORS['moment_pos'], linewidth=3, zorder=5)
        ax.text(0, support_A_y - 0.28, f'R_A = {self.R_A:.0f} N',
               ha='center', va='top', fontsize=22, fontweight='bold',
               color=COLORS['text'],
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        # Reaction at B
        ax.arrow(support_B_x, support_B_y - 0.25, 0, 0.13,
                head_width=arrow_width*0.22, head_length=0.03, fc=COLORS['moment_pos'],
                ec=COLORS['moment_pos'], linewidth=3, zorder=5)
        ax.text(support_B_x, support_B_y - 0.28, f'R_B = {self.R_B:.0f} N',
               ha='center', va='top', fontsize=22, fontweight='bold',
               color=COLORS['text'],
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        # Add support labels
        ax.text(0, support_A_y - 0.18, 'A (Pin)', ha='center', va='top',
               fontsize=20, color=COLORS['text'], weight='bold')
        ax.text(support_B_x, support_B_y - 0.14, 'B (Roller)', ha='center', va='top',
               fontsize=20, color=COLORS['text'], weight='bold')

        # Add dimension lines
        # Total length
        dim_y = -0.35
        ax.plot([0, self.L/1000], [dim_y, dim_y], color=COLORS['dimension'],
               linewidth=2, linestyle='-')
        ax.plot([0, 0], [dim_y - 0.02, dim_y + 0.02], color=COLORS['dimension'], linewidth=2)
        ax.plot([self.L/1000, self.L/1000], [dim_y - 0.02, dim_y + 0.02],
               color=COLORS['dimension'], linewidth=2)
        ax.text(self.L/2000, dim_y - 0.04, f'L = {self.L} mm', ha='center', va='top',
               fontsize=22, color=COLORS['dimension'], weight='bold')

        # Distance to load (a)
        dim_y2 = 0.28
        ax.plot([0, load_x], [dim_y2, dim_y2], color=COLORS['dimension'],
               linewidth=2, linestyle='--')
        ax.plot([0, 0], [dim_y2 - 0.02, dim_y2 + 0.02], color=COLORS['dimension'], linewidth=2)
        ax.plot([load_x, load_x], [dim_y2 - 0.02, dim_y2 + 0.02],
               color=COLORS['dimension'], linewidth=2)
        ax.text(load_x/2, dim_y2 + 0.03, f'a = {self.a} mm',
               ha='center', va='bottom', fontsize=20, color=COLORS['dimension'],
               style='italic', weight='bold')

        # Add cross-section details
        ax.text(self.L/1000 + 0.3, beam_y - 0.5,
               f'Aluminum 6061-T6\nI = {self.I/1e6:.1f}×10⁶ mm⁴\nσ_yield = {self.sigma_yield} MPa',
               ha='left', va='top', fontsize=20, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.8', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        # Set axis properties
        ax.set_xlim(-0.15, self.L/1000 + 0.15)
        ax.set_ylim(-0.45, 0.45)
        ax.set_aspect('equal')
        ax.axis('off')

        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)
        return fig

    def plot_shear_diagram(self):
        """Generate shear force diagram for critical load position (midspan)"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))

        # Create x points for regions
        x_region1 = np.linspace(0, self.a/1000, 50)  # 0 to a (load position)
        x_region2 = np.linspace(self.a/1000, self.L/1000, 50)  # a to L

        # Calculate shear forces
        # Region 1 (0 to a): V = +R_A (constant)
        V_region1 = np.full_like(x_region1, self.R_A / 1000)  # Convert to kN

        # Region 2 (a to L): V = R_A - P = -R_B (constant, negative)
        V_region2 = np.full_like(x_region2, -self.R_B / 1000)  # Convert to kN

        # Plot shear force regions
        ax.plot(x_region1, V_region1, color=COLORS['shear_pos'], linewidth=4, zorder=4)
        ax.fill_between(x_region1, V_region1, 0, alpha=0.3, color=COLORS['moment_pos'], zorder=1)

        ax.plot(x_region2, V_region2, color=COLORS['shear_pos'], linewidth=4, zorder=4)
        ax.fill_between(x_region2, V_region2, 0, alpha=0.3, color=COLORS['shear_neg'], zorder=1)

        # Vertical discontinuity line at load position
        ax.plot([self.a/1000, self.a/1000], [self.R_A/1000, -self.R_B/1000],
               color=COLORS['shear_pos'], linewidth=4, zorder=4)

        # Zero line
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)

        # Mark critical points with enhanced visibility (matching pantograph style)
        critical_points = [
            (0, self.R_A/1000),
            (self.a/1000, self.R_A/1000),
            (self.a/1000, -self.R_B/1000),
            (self.L/1000, -self.R_B/1000),
        ]

        for x, y in critical_points:
            # White background circle with orange center
            ax.plot(x, y, 'o', markersize=18, color='#FFFFFF',
                   markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                   markeredgecolor=COLORS['text'], zorder=5)

        # Add annotations
        ax.annotate(f'+{self.R_A/1000:.2f} kN', (0, self.R_A/1000), xytext=(40, 50),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        ax.annotate(f'{-self.R_B/1000:.2f} kN', (self.L/1000, -self.R_B/1000), xytext=(-80, 20),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Add vertical dashed lines at critical positions (orange color like pantograph)
        for x_pos in [0, self.a/1000, self.L/1000]:
            ax.axvline(x=x_pos, color=COLORS['load_arrow'], linewidth=4,
                      linestyle='--', alpha=0.6, zorder=2)

        # Customize plot (NO TITLE!)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Support A (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Shear Force (kN)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['left'].set_color(COLORS['text'])
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['bottom'].set_color(COLORS['text'])

        # Set axis limits
        ax.set_xlim(-0.05, self.L/1000 + 0.05)
        y_max = max(abs(self.R_A/1000), abs(self.R_B/1000)) * 1.3
        ax.set_ylim(-y_max, y_max)

        plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.15)
        return fig

    def plot_moment_diagram(self):
        """Generate bending moment diagram for critical load position (midspan)"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))

        # Create x points for regions
        x_region1 = np.linspace(0, self.a/1000, 100)  # 0 to a
        x_region2 = np.linspace(self.a/1000, self.L/1000, 100)  # a to L

        # Calculate moment values
        # Region 1 (0 to a): M(x) = R_A * x
        M_region1 = (self.R_A * x_region1 * 1000) / 1e6  # Convert to kN·m

        # Region 2 (a to L): M(x) = R_A * x - P * (x - a)
        M_region2 = (self.R_A * x_region2 * 1000 - self.P * (x_region2 * 1000 - self.a)) / 1e6

        # Plot moment curves
        ax.plot(x_region1, M_region1, color=COLORS['moment_pos'], linewidth=4, zorder=4)
        ax.fill_between(x_region1, M_region1, 0, alpha=0.3, color=COLORS['moment_pos'], zorder=1)

        ax.plot(x_region2, M_region2, color=COLORS['moment_pos'], linewidth=4, zorder=4)
        ax.fill_between(x_region2, M_region2, 0, alpha=0.3, color=COLORS['moment_pos'], zorder=1)

        # Zero line
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)

        # Calculate maximum moment (at load position, x = a)
        M_max = (self.R_A * self.a) / 1e6  # kN·m

        # Mark critical points (matching pantograph style)
        critical_points = [
            (0, 0, '0 kN·m\n(Support A)'),
            (self.a/1000, M_max, f'{M_max:.3f} kN·m\n(MAX)'),
            (self.L/1000, 0, '0 kN·m\n(Support B)'),
        ]

        for x, y, label in critical_points:
            # White background circle with orange center
            ax.plot(x, y, 'o', markersize=18, color='#FFFFFF',
                   markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                   markeredgecolor=COLORS['text'], zorder=5)

        # Add annotations
        ax.annotate(critical_points[0][2], (0, 0), xytext=(40, -60),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        ax.annotate(critical_points[1][2], (self.a/1000, M_max), xytext=(50, -10),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        ax.annotate(critical_points[2][2], (self.L/1000, 0), xytext=(-80, -60),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Add vertical dashed lines at critical positions (orange color like pantograph)
        for x_pos in [0, self.a/1000, self.L/1000]:
            ax.axvline(x=x_pos, color=COLORS['load_arrow'], linewidth=4,
                      linestyle='--', alpha=0.6, zorder=2)

        # Customize plot (NO TITLE!)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Support A (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Bending Moment (kN·m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['left'].set_color(COLORS['text'])
        ax.spines['bottom'].set_color(COLORS['text'])

        # Set axis limits
        ax.set_xlim(-0.05, self.L/1000 + 0.05)
        ax.set_ylim(-0.015, M_max * 1.4)

        plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.15)
        return fig

    def generate_all_diagrams(self):
        """Generate all three diagrams"""
        print("\n" + "="*60)
        print("3D PRINTER GANTRY RAIL ANALYSIS")
        print("="*60)
        print(f"\nSystem Parameters:")
        print(f"  Beam span: L = {self.L} mm")
        print(f"  Print head load: P = {self.P} N")
        print(f"  Critical load position: a = {self.a} mm (midspan)")
        print(f"\nSupport Reactions (at a = {self.a} mm):")
        print(f"  R_A = {self.R_A:.1f} N")
        print(f"  R_B = {self.R_B:.1f} N")
        print(f"\nMaximum Moment:")
        M_max = (self.R_A * self.a) / 1e6  # kN·m
        print(f"  M_max = {M_max:.3f} kN·m = {M_max*1e6:.0f} N·mm")
        print(f"  Location: x = {self.a} mm (at load position)")
        print(f"\nMaximum Stress:")
        sigma_max = (M_max * 1e6) / self.S  # MPa
        print(f"  σ_max = {sigma_max:.3f} MPa")
        print(f"\nSafety Factor:")
        SF = self.sigma_yield / sigma_max
        print(f"  SF = {SF:.1f}")
        print(f"\nGenerating diagrams...")

        # Generate loading diagram
        fig1 = self.plot_loading_diagram()
        fig1.savefig('gantry_rail_loading_diagram.svg', format='svg', dpi=300,
                    bbox_inches='tight', transparent=True)
        print("✓ Loading diagram saved: gantry_rail_loading_diagram.svg")
        plt.close(fig1)

        # Generate shear diagram
        fig2 = self.plot_shear_diagram()
        fig2.savefig('gantry_rail_shear_diagram.svg', format='svg', dpi=300,
                    bbox_inches='tight', transparent=True)
        print("✓ Shear diagram saved: gantry_rail_shear_diagram.svg")
        plt.close(fig2)

        # Generate moment diagram
        fig3 = self.plot_moment_diagram()
        fig3.savefig('gantry_rail_moment_diagram.svg', format='svg', dpi=300,
                    bbox_inches='tight', transparent=True)
        print("✓ Moment diagram saved: gantry_rail_moment_diagram.svg")
        plt.close(fig3)

        print(f"\n✓ All diagrams generated successfully!")
        print("="*60 + "\n")

if __name__ == "__main__":
    # Create analysis instance and generate diagrams
    analysis = GantryRailAnalysis()
    analysis.generate_all_diagrams()
