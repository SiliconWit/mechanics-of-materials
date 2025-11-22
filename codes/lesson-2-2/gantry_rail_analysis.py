#!/usr/bin/env python3
"""
3D Printer Gantry Rail Bending Analysis
Application 3: Simply supported beam with point load at different positions

This script generates diagrams showing ALL THREE load positions analyzed in the lesson:
1. Loading diagram showing print head at positions a = 300, 600, 900 mm
2. Shear force diagram for all three positions
3. Bending moment diagram for all three positions

Students compare the three positions to discover that midspan (a=600mm)
gives maximum bending moment and stress.

Expected Results:
- Position 1 (a=300mm): M_max = 56.25 N·m, σ = 0.639 MPa
- Position 2 (a=600mm): M_max = 75.0 N·m,  σ = 0.852 MPa ⭐ CRITICAL
- Position 3 (a=900mm): M_max = 56.25 N·m, σ = 0.639 MPa

Author: SiliconWit Engineering Team
Date: 2025-10-17
Updated: 2025-11-23 (Updated to show all three positions)
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

        # Three load positions analyzed in the lesson
        self.positions = [
            {'a': 300, 'name': 'Position 1 (a=300 mm)'},
            {'a': 600, 'name': 'Position 2 (a=600 mm)'},
            {'a': 900, 'name': 'Position 3 (a=900 mm)'}
        ]

        # Calculate reactions and moments for all three positions
        for pos in self.positions:
            a = pos['a']
            pos['R_A'] = self.P * (self.L - a) / self.L
            pos['R_B'] = self.P * a / self.L
            pos['M_max'] = pos['R_A'] * a  # N·mm

        # Cross-section properties
        self.I = 2.2e6  # mm^4
        self.c = 25     # mm
        self.S = self.I / self.c  # Section modulus

        # Material properties
        self.sigma_yield = 275  # MPa
        self.E = 69000  # MPa (Aluminum 6061-T6)

    def plot_loading_diagram(self):
        """Generate loading diagram showing simply supported beam with three load positions"""
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

        # Draw print head loads at all three positions
        load_y = beam_y + beam_height/2
        arrow_length = 0.15
        arrow_width = 0.18

        for i, pos in enumerate(self.positions):
            load_x = pos['a'] / 1000
            # Load arrow
            ax.arrow(load_x, load_y + arrow_length, 0, -arrow_length + 0.01,
                    head_width=arrow_width*0.22, head_length=0.03, fc=COLORS['load_arrow'],
                    ec=COLORS['load_arrow'], linewidth=3, zorder=5, alpha=0.7)

            # Load position label
            ax.text(load_x, load_y + arrow_length + 0.05, f'a={pos["a"]} mm',
                   ha='center', va='bottom', fontsize=20, fontweight='bold',
                   color=COLORS['load_arrow'],
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8FAFC',
                            edgecolor=COLORS['load_arrow'], alpha=0.8))

        # Add general load label above
        ax.text(self.L/2000, load_y + arrow_length + 0.18, f'P = {self.P} N (Print Head)',
               ha='center', va='bottom', fontsize=24, fontweight='bold',
               color=COLORS['load_arrow'],
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['load_arrow'], alpha=0.9))

        # Note: Reactions vary by position, shown in shear diagram

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
        """Generate shear force diagram for center position only"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))

        # Use only the center position (a=600mm)
        pos = self.positions[1]  # Position 2: midspan
        a = pos['a'] / 1000  # meters
        R_A = pos['R_A'] / 1000  # kN
        R_B = pos['R_B'] / 1000  # kN

        # Create x points for regions
        x_region1 = np.linspace(0, a, 50)
        x_region2 = np.linspace(a, self.L/1000, 50)

        # Calculate shear forces
        V_region1 = np.full_like(x_region1, R_A)
        V_region2 = np.full_like(x_region2, -R_B)

        # Plot shear force regions
        ax.plot(x_region1, V_region1, color=COLORS['shear_pos'], linewidth=4, zorder=4)
        ax.fill_between(x_region1, V_region1, 0, alpha=0.3, color=COLORS['moment_pos'], zorder=1)

        ax.plot(x_region2, V_region2, color=COLORS['shear_pos'], linewidth=4, zorder=4)
        ax.fill_between(x_region2, V_region2, 0, alpha=0.3, color=COLORS['shear_neg'], zorder=1)

        # Vertical discontinuity line at load position
        ax.plot([a, a], [R_A, -R_B], color=COLORS['shear_pos'], linewidth=4, zorder=4)

        # Zero line
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)

        # Mark critical points
        critical_points = [
            (0, R_A),
            (a, R_A),
            (a, -R_B),
            (self.L/1000, -R_B),
        ]

        for x, y in critical_points:
            ax.plot(x, y, 'o', markersize=18, color='#FFFFFF',
                   markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                   markeredgecolor=COLORS['text'], zorder=5)

        # Add annotations
        ax.annotate(f'+{R_A:.3f} kN', (0, R_A), xytext=(40, 50),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        ax.annotate(f'{-R_B:.3f} kN', (self.L/1000, -R_B), xytext=(-40, -50),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Add vertical dashed lines at critical positions
        for x_pos in [0, a, self.L/1000]:
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
        # Find maximum shear force from all positions
        max_R = max(max(pos['R_A'], pos['R_B']) for pos in self.positions)
        y_max = (max_R / 1000) * 1.3
        ax.set_ylim(-y_max, y_max)

        plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.15)
        return fig

    def plot_moment_diagram(self):
        """Generate bending moment diagram connecting moments at three load positions"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))

        # Zero line
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)

        # Create points: (0,0) -> (0.3, M1) -> (0.6, M2) -> (0.9, M3) -> (1.2, 0)
        x_points = [0]
        y_points = [0]

        for pos in self.positions:
            x_points.append(pos['a'] / 1000)  # meters
            y_points.append(pos['M_max'] / 1e6)  # kN·m

        x_points.append(self.L / 1000)
        y_points.append(0)

        # Plot single line connecting all points
        ax.plot(x_points, y_points, color=COLORS['moment_pos'], linewidth=4, zorder=4)
        ax.fill_between(x_points, y_points, 0, alpha=0.3, color=COLORS['moment_pos'], zorder=1)

        # Mark all critical points
        for i, (x, y) in enumerate(zip(x_points, y_points)):
            ax.plot(x, y, 'o', markersize=18, color='#FFFFFF',
                   markeredgewidth=5, markerfacecolor=COLORS['moment_neg'],
                   markeredgecolor=COLORS['text'], zorder=5)

            # Add annotations only for non-zero moments
            if y > 0.001:
                # Offset positioning for readability
                if i == 1:  # First moment point
                    offset = (-40, 50)
                    ha = 'right'
                elif i == 2:  # Middle moment point (max)
                    offset = (50, -10)
                    ha = 'left'
                else:  # Third moment point
                    offset = (40, 50)
                    ha = 'left'

                ax.annotate(f'{y:.3f} kN·m',
                           (x, y), xytext=offset,
                           textcoords='offset points', fontsize=26, color=COLORS['text'],
                           weight='bold', ha=ha,
                           arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Add vertical dashed lines at load positions only (not at supports)
        for pos in self.positions:
            ax.axvline(x=pos['a']/1000, color=COLORS['load_arrow'], linewidth=3,
                      linestyle='--', alpha=0.5, zorder=2)

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
        # Find maximum moment from all positions
        max_M = max(pos['M_max'] for pos in self.positions) / 1e6  # Convert to kN·m
        ax.set_ylim(-0.015, max_M * 1.4)

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

        print(f"\nAnalyzing THREE load positions:")
        for i, pos in enumerate(self.positions, 1):
            print(f"\n  Position {i}: a = {pos['a']} mm")
            print(f"    R_A = {pos['R_A']:.1f} N")
            print(f"    R_B = {pos['R_B']:.1f} N")
            print(f"    M_max = {pos['M_max']/1e6:.5f} kN·m = {pos['M_max']:.1f} N·mm")
            sigma = pos['M_max'] / self.S
            print(f"    σ_max = {sigma:.3f} MPa")

        # Find overall maximum
        max_pos = max(self.positions, key=lambda p: p['M_max'])
        print(f"\n  CRITICAL POSITION: a = {max_pos['a']} mm")
        print(f"  Maximum stress: σ = {max_pos['M_max']/self.S:.3f} MPa")
        SF = self.sigma_yield / (max_pos['M_max'] / self.S)
        print(f"  Safety Factor: SF = {SF:.1f}")

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
