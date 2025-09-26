#!/usr/bin/env python3
"""
Crane Jib with Overhang Loading Analysis
Application 3 from Lesson 2.2: Bending Stresses in Simple Beams

This program calculates and visualizes:
1. Support reaction forces
2. Shear force diagram
3. Bending moment diagram
4. Maximum bending stresses

Problem Parameters:
- Steel I-beam: 150 mm × 100 mm × 8 mm (I = 8.2 × 10⁶ mm⁴, c = 75 mm)
- Span: 3000 mm between supports A and B
- Overhang: 1000 mm beyond support B
- Load 1: P₁ = 5000 N at 1500 mm from A (midspan)
- Load 2: P₂ = 3000 N at end of overhang
- Load 3: Distributed load W = 800 N/m over entire length
- Dynamic amplification factor: 1.4
- Material: Structural steel (σ_yield = 250 MPa)
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")   # Non-GUI backend, perfect for saving plots
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# Set up matplotlib for mobile-friendly plots with transparent background
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

# Color scheme matching SVG colors
COLORS = {
    'beam': '#405ab9',           # Blue from SVG axes
    'load_arrow': '#ff8c36',     # Orange from SVG
    'reaction': '#00a0d0',       # Light blue from SVG
    'shear_pos': '#405ab9',      # Blue for positive shear
    'shear_neg': '#ff8c36',      # Orange for negative shear
    'moment_pos': '#405ab9',     # Blue for positive moment
    'moment_neg': '#ff8c36',     # Orange for negative moment
    'text': '#405ab9',           # Blue for all text/axes/labels
    'grid': '#9ea388',           # Gray-green from SVG
    'support': '#405ab9'         # Blue for supports
}

class CraneJibAnalysis:
    def __init__(self):
        # Beam geometry (all in mm)
        self.L_span = 3000  # Span between supports
        self.L_overhang = 1000  # Overhang length
        self.L_total = self.L_span + self.L_overhang  # Total beam length

        # Loads
        self.P1_original = 5000  # N, at midspan
        self.P2_original = 3000  # N, at end of overhang
        self.w = 800  # N/m, distributed load
        self.dynamic_factor = 1.4

        # Apply dynamic amplification to point loads only
        self.P1 = self.P1_original * self.dynamic_factor  # 7000 N
        self.P2 = self.P2_original * self.dynamic_factor  # 4200 N
        self.W_total = self.w * (self.L_total / 1000)  # 3200 N (distributed load in N)

        # Load positions (mm from left support A)
        self.x_P1 = 1500  # Midspan
        self.x_P2 = 4000  # End of overhang
        self.x_support_A = 0
        self.x_support_B = 3000

        # Beam properties
        self.I = 8.2e6  # mm⁴
        self.c = 75  # mm
        self.sigma_yield = 250  # MPa
        self.S = self.I / self.c  # Section modulus

        # Calculate reactions
        self.calculate_reactions()

    def calculate_reactions(self):
        """Calculate support reaction forces using equilibrium equations."""
        print("="*80)
        print("CRANE JIB WITH OVERHANG LOADING ANALYSIS")
        print("="*80)
        print("\n📊 PROBLEM SETUP:")
        print(f"• Beam length: {self.L_total/1000:.1f} m ({self.L_span/1000:.1f} m span + {self.L_overhang/1000:.1f} m overhang)")
        print(f"• Point load P₁: {self.P1_original} N × {self.dynamic_factor} = {self.P1} N at x = {self.x_P1/1000:.1f} m")
        print(f"• Point load P₂: {self.P2_original} N × {self.dynamic_factor} = {self.P2} N at x = {self.x_P2/1000:.1f} m")
        print(f"• Distributed load: {self.w} N/m over entire length = {self.W_total} N total")
        print(f"• Beam properties: I = {self.I/1e6:.1f}×10⁶ mm⁴, c = {self.c} mm")

        # Calculate reaction at B using moment equilibrium about A
        # ΣM_A = 0: R_B(3.0) - P1(1.5) - W_total(2.0) - P2(4.0) = 0
        moment_P1 = self.P1 * (self.x_P1 / 1000)  # 7000 × 1.5 = 10500 N·m
        moment_W = self.W_total * (self.L_total / 2000)  # 3200 × 2.0 = 6400 N·m
        moment_P2 = self.P2 * (self.x_P2 / 1000)  # 4200 × 4.0 = 16800 N·m

        self.R_B = (moment_P1 + moment_W + moment_P2) / (self.x_support_B / 1000)

        # Calculate reaction at A using force equilibrium
        # ΣF_y = 0: R_A + R_B - P1 - W_total - P2 = 0
        total_downward = self.P1 + self.W_total + self.P2
        self.R_A = total_downward - self.R_B

        print(f"\n🔧 REACTION FORCE CALCULATIONS:")
        print(f"Sum of moments about A:")
        print(f"  R_B × 3.0 = {self.P1} × 1.5 + {self.W_total} × 2.0 + {self.P2} × 4.0")
        print(f"  R_B × 3.0 = {moment_P1} + {moment_W} + {moment_P2} = {moment_P1 + moment_W + moment_P2} N·m")
        print(f"  R_B = {self.R_B:.0f} N")
        print(f"\nSum of vertical forces:")
        print(f"  R_A = {total_downward} - {self.R_B:.0f} = {self.R_A:.0f} N")

        # Verification
        force_sum = self.R_A + self.R_B - total_downward
        print(f"\n✅ Equilibrium check: ΣF_y = {force_sum:.1f} N (should be ≈ 0)")



    def calculate_shear_forces(self, x_points):
        """Calculate shear forces at given x positions (in m)."""
        V = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            V_current = self.R_A

            # Distributed load from 0 to x
            V_current -= self.w * x

            # Subtract P1 if passed
            if x*1000 >= self.x_P1:
                V_current -= self.P1

            # Add reaction at B if passed
            if x*1000 >= self.x_support_B:
                V_current += self.R_B

            # Subtract P2 if passed
            if x*1000 >= self.x_P2:
                V_current -= self.P2

            V[i] = V_current

        return V



    def calculate_moments(self, x_points):
        """Calculate bending moments at given x positions using area under shear diagram."""
        M = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            if x == 0:
                M[i] = 0
                continue

            x_mm = x * 1000

            # Method: Sum moments of all forces to the LEFT of the cut
            moment = 0

            # Moment from reaction R_A
            moment += self.R_A * x

            # Moment from distributed load (up to current position)
            dist_force = self.w * x  # Force from distributed load up to x
            dist_centroid = x / 2    # Centroid distance from current position
            moment -= dist_force * dist_centroid

            # Moment from P1 (if passed)
            if x_mm > self.x_P1:
                distance_from_cut = x - (self.x_P1 / 1000)
                moment -= self.P1 * distance_from_cut

            # Moment from reaction R_B (if passed)
            if x_mm > self.x_support_B:
                distance_from_cut = x - (self.x_support_B / 1000)
                moment += self.R_B * distance_from_cut

            # Moment from P2 (if passed)
            if x_mm > self.x_P2:
                distance_from_cut = x - (self.x_P2 / 1000)
                moment -= self.P2 * distance_from_cut

            M[i] = moment

        return M

    def find_critical_values(self):
        """Find maximum and minimum shear forces and bending moments."""
        # Create fine grid for analysis
        x_fine = np.linspace(0, self.L_total/1000, 1000)
        V_fine = self.calculate_shear_forces(x_fine)
        M_fine = self.calculate_moments(x_fine)

        # Find critical values
        V_max = np.max(V_fine)
        V_min = np.min(V_fine)
        M_max = np.max(M_fine)
        M_min = np.min(M_fine)

        # Find locations
        V_max_idx = np.argmax(V_fine)
        V_min_idx = np.argmin(V_fine)
        M_max_idx = np.argmax(M_fine)
        M_min_idx = np.argmin(M_fine)

        self.critical_results = {
            'V_max': V_max, 'V_max_x': x_fine[V_max_idx],
            'V_min': V_min, 'V_min_x': x_fine[V_min_idx],
            'M_max': M_max, 'M_max_x': x_fine[M_max_idx],
            'M_min': M_min, 'M_min_x': x_fine[M_min_idx]
        }

        # Calculate stresses (M in N·m, S in mm³, result in MPa)
        sigma_max_pos = (M_max * 1000) / self.S  # M*1000 converts N·m to N·mm, S is in mm³, result in MPa
        sigma_max_neg = abs(M_min * 1000) / self.S  # M*1000 converts N·m to N·mm, S is in mm³, result in MPa

        print(f"\n📈 CRITICAL VALUES:")
        print(f"Maximum positive shear: {V_max:.0f} N at x = {x_fine[V_max_idx]:.2f} m")
        print(f"Maximum negative shear: {V_min:.0f} N at x = {x_fine[V_min_idx]:.2f} m")
        print(f"Maximum positive moment: {M_max:.0f} N·m at x = {x_fine[M_max_idx]:.2f} m")
        print(f"Maximum negative moment: {M_min:.0f} N·m at x = {x_fine[M_min_idx]:.2f} m")

        print(f"\n🔬 STRESS ANALYSIS:")
        print(f"Section modulus S = I/c = {self.S/1000:.1f}×10³ mm³")
        print(f"Maximum stress (positive moment): σ = {sigma_max_pos:.1f} MPa")
        print(f"Maximum stress (negative moment): σ = {sigma_max_neg:.1f} MPa")
        print(f"Controlling stress: {max(sigma_max_pos, sigma_max_neg):.1f} MPa")
        print(f"Yield strength: {self.sigma_yield} MPa")

        max_stress = max(sigma_max_pos, sigma_max_neg)
        if max_stress > 0:
            safety_factor = self.sigma_yield / max_stress
            print(f"Safety factor: {safety_factor:.1f}")
        else:
            print(f"Safety factor: N/A (zero stress)")

    def create_loading_diagram(self):
        """Create loading diagram showing beam, supports, and loads."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Beam representation
        beam_height = 0.3
        beam_y = 0
        beam = patches.Rectangle((0, beam_y - beam_height/2), self.L_total/1000, beam_height,
                               facecolor=COLORS['beam'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(beam)

        # Supports
        support_size = 0.25

        # Support A (pinned)
        triangle_A = patches.RegularPolygon((self.x_support_A/1000, beam_y - beam_height/2 - support_size/2),
                                          3, support_size, orientation=0,
                                          facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(triangle_A)

        # Support B (roller)
        circle_B = patches.Circle((self.x_support_B/1000, beam_y - beam_height/2 - support_size/2),
                                support_size/2, facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(circle_B)

        # Point loads
        arrow_length = 0.8
        arrow_width = 0.18

        # P1 at midspan
        ax.arrow(self.x_P1/1000, beam_y + beam_height/2 + arrow_length, 0, -arrow_length + 0.1,
                head_width=arrow_width, head_length=0.1, fc=COLORS['load_arrow'], ec=COLORS['load_arrow'], linewidth=3)
        ax.text(self.x_P1/1000, beam_y + beam_height/2 + arrow_length + 0.2,
               f'P₁ = {self.P1:.0f} N\n(Dynamic)', ha='center', va='bottom',
               fontsize=26, color=COLORS['load_arrow'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor=COLORS['load_arrow'], alpha=0.9))

        # P2 at overhang end
        ax.arrow(self.x_P2/1000, beam_y + beam_height/2 + arrow_length, 0, -arrow_length + 0.1,
                head_width=arrow_width, head_length=0.1, fc=COLORS['load_arrow'], ec=COLORS['load_arrow'], linewidth=3)
        ax.text(self.x_P2/1000, beam_y + beam_height/2 + arrow_length + 0.2,
               f'P₂ = {self.P2:.0f} N\n(Dynamic)', ha='center', va='bottom',
               fontsize=26, color=COLORS['load_arrow'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor=COLORS['load_arrow'], alpha=0.9))

        # Distributed load (represented by arrows along the beam)
        n_arrows = 8
        for i in range(n_arrows):
            x_arrow = (i + 0.5) * (self.L_total/1000) / n_arrows
            arrow_len = 0.4
            ax.arrow(x_arrow, beam_y + beam_height/2 + arrow_len, 0, -arrow_len + 0.05,
                    head_width=0.1, head_length=0.06, fc=COLORS['load_arrow'], ec=COLORS['load_arrow'],
                    alpha=0.8, linewidth=2)

        ax.text(self.L_total/2000, beam_y + beam_height/2 + 0.6,
               f'w = {self.w} N/m\n(Self-weight + attachments)', ha='center', va='bottom',
               fontsize=26, color=COLORS['load_arrow'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor=COLORS['load_arrow'], alpha=0.9))

        # Reaction forces
        reaction_arrow_length = 0.6

        # R_A
        ax.arrow(self.x_support_A/1000, beam_y - beam_height/2 - reaction_arrow_length, 0, reaction_arrow_length - 0.1,
                head_width=arrow_width, head_length=0.1, fc=COLORS['reaction'], ec=COLORS['reaction'], linewidth=3)
        ax.text(self.x_support_A/1000, beam_y - beam_height/2 - reaction_arrow_length - 0.1,
               f'R_A = {self.R_A:.0f} N', ha='center', va='top',
               fontsize=26, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor=COLORS['reaction'], alpha=0.9))

        # R_B
        ax.arrow(self.x_support_B/1000, beam_y - beam_height/2 - reaction_arrow_length, 0, reaction_arrow_length - 0.1,
                head_width=arrow_width, head_length=0.1, fc=COLORS['reaction'], ec=COLORS['reaction'], linewidth=3)
        ax.text(self.x_support_B/1000, beam_y - beam_height/2 - reaction_arrow_length - 0.1,
               f'R_B = {self.R_B:.0f} N', ha='center', va='top',
               fontsize=26, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor=COLORS['reaction'], alpha=0.9))

        # Dimensions
        dimension_y = beam_y - beam_height/2 - 1.2

        # Span dimension
        ax.annotate('', xy=(0, dimension_y), xytext=(self.x_support_B/1000, dimension_y),
                   arrowprops=dict(arrowstyle='<->', color=COLORS['text'], lw=3))
        ax.text(self.x_support_B/2000, dimension_y - 0.15, f'{self.L_span/1000:.1f} m span',
               ha='center', va='top', fontsize=26, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor=COLORS['text'], alpha=0.9))

        # Overhang dimension
        ax.annotate('', xy=(self.x_support_B/1000, dimension_y - 0.4), xytext=(self.x_P2/1000, dimension_y - 0.4),
                   arrowprops=dict(arrowstyle='<->', color=COLORS['text'], lw=3))
        ax.text((self.x_support_B + self.x_P2)/(2*1000), dimension_y - 0.55, f'{self.L_overhang/1000:.1f} m overhang',
               ha='center', va='top', fontsize=26, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor=COLORS['text'], alpha=0.9))

        ax.set_xlim(-0.6, 4.9)
        ax.set_ylim(-2.4, 2.0)
        ax.set_aspect('equal')
        ax.axis('off')

        # Extend figure margins
        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)
        return fig

    def create_shear_diagram(self):
        """Create shear force diagram."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create x points for each region separately to ensure correct plotting
        # Region 1: 0 to P1 (1.5m)
        x1 = np.linspace(0, self.x_P1/1000, 50)
        V1 = self.calculate_shear_forces(x1) / 1000

        # Region 2: P1 to support B (1.5m to 3m)
        x2 = np.linspace(self.x_P1/1000 + 0.001, self.x_support_B/1000, 50)
        V2 = self.calculate_shear_forces(x2) / 1000

        # Region 3: Support B to P2 (3m to 4m) - this should be the diagonal line
        x3 = np.linspace(self.x_support_B/1000 + 0.001, self.x_P2/1000, 50)
        V3 = self.calculate_shear_forces(x3) / 1000

        # Plot each region with consistent color (blue for all lines)
        for i in range(len(x1)-1):
            ax.plot([x1[i], x1[i+1]], [V1[i], V1[i+1]], color=COLORS['shear_pos'], linewidth=4)

        for i in range(len(x2)-1):
            ax.plot([x2[i], x2[i+1]], [V2[i], V2[i+1]], color=COLORS['shear_pos'], linewidth=4)

        for i in range(len(x3)-1):
            ax.plot([x3[i], x3[i+1]], [V3[i], V3[i+1]], color=COLORS['shear_pos'], linewidth=4)

        # Fill areas for each region separately to ensure proper diagonal shading
        ax.fill_between(x1, V1, 0, where=(V1 >= 0), alpha=0.3, color=COLORS['shear_pos'])
        ax.fill_between(x1, V1, 0, where=(V1 < 0), alpha=0.3, color=COLORS['shear_neg'])

        ax.fill_between(x2, V2, 0, where=(V2 >= 0), alpha=0.3, color=COLORS['shear_pos'])
        ax.fill_between(x2, V2, 0, where=(V2 < 0), alpha=0.3, color=COLORS['shear_neg'])

        # Special handling for diagonal region (x3) to ensure proper shading
        ax.fill_between(x3, V3, 0, where=(V3 >= 0), alpha=0.3, color=COLORS['shear_pos'])
        ax.fill_between(x3, V3, 0, where=(V3 < 0), alpha=0.3, color=COLORS['shear_neg'])

        # Add ONLY vertical dashed lines at discontinuities
        discontinuity_points = [self.x_P1/1000, self.x_support_B/1000]
        for x_disc in discontinuity_points:
            ax.axvline(x=x_disc, color=COLORS['load_arrow'], linewidth=3, alpha=0.7, linestyle='--')

        # Mark critical points with correct annotations - using larger, uniform font sizes
        # At x=0: V = +3.167 kN
        ax.plot(0, 3.167, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('3.17 kN', (0, 3.167), xytext=(40, 40),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=1.5m (before P1): V = +1.967 kN (missing annotation you mentioned)
        ax.plot(1.5, 1.967, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('1.97 kN', (1.5, 1.967), xytext=(40, 40),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=1.5m (after P1): V = -5.033 kN (on negative side)
        ax.plot(1.5, -5.033, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('-5.03 kN', (1.5, -5.033), xytext=(-140, 30),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=3m (before support B): V = -6.233 kN (on negative side, no overlap)
        ax.plot(3.0, -6.233, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('-6.23 kN', (3.0, -6.233), xytext=(140, 30),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=3m (after support B): V = +5.00 kN (on positive side, no overlap)
        ax.plot(3.0, 5.0, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('5.00 kN', (3.0, 5.0), xytext=(40, 20),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=4m: V = 0 kN
        ax.plot(4.0, 0, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('0 kN', (4.0, 0), xytext=(20, 40),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Customize plot with larger font sizes
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Support A (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Shear Force (kN)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        # Add subtle support lines without labels
        for x_sup in [0, self.x_support_B/1000]:
            ax.axvline(x=x_sup, color=COLORS['load_arrow'], linewidth=4, alpha=0.4, linestyle='--')

        # Add load lines (vertical dashed lines only)
        ax.axvline(x=self.x_P2/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['left'].set_color(COLORS['text'])
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['bottom'].set_color(COLORS['text'])

        # Extend figure margins
        plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.15)
        return fig

    def create_moment_diagram(self):
        """Create bending moment diagram."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create smooth x array
        x_array = np.linspace(0, self.L_total/1000, 500)

        # Calculate moments
        M = self.calculate_moments(x_array)

        # Convert to kNm for display
        M_kNm = M / 1000

        # Plot moment diagram
        ax.plot(x_array, M_kNm, color=COLORS['moment_pos'], linewidth=4)

        # Fill areas
        ax.fill_between(x_array, M_kNm, 0, where=(M >= 0), alpha=0.3, color=COLORS['moment_pos'])
        ax.fill_between(x_array, M_kNm, 0, where=(M < 0), alpha=0.3, color=COLORS['moment_neg'])

        # Add ONLY vertical dashed lines at critical load positions
        critical_load_positions = [self.x_P1/1000, self.x_P2/1000]
        for x_pos in critical_load_positions:
            ax.axvline(x=x_pos, color=COLORS['load_arrow'], linewidth=3, alpha=0.7, linestyle='--')

        # Mark critical points with larger markers and text - uniform with shear diagram
        critical_x = [0, 1.5, 3.0, 4.0]  # Key locations
        critical_labels = ['0 kNm', '3.85 kNm', '-4.60 kNm', '0 kNm']

        for i, x_crit in enumerate(critical_x):
            if 0 <= x_crit <= self.L_total/1000:
                M_crit = self.calculate_moments(np.array([x_crit]))[0] / 1000
                # Use orange for all dots (same as negative moment color)
                ax.plot(x_crit, M_crit, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
                       markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)

                # Position arrows based on sign of moment to avoid overlap
                if M_crit >= 0:
                    xytext_offset = (-10, 40)
                    ha_align = 'left'
                else:
                    xytext_offset = (40, 40)
                    ha_align = 'left'

                ax.annotate(critical_labels[i], (x_crit, M_crit), xytext=xytext_offset,
                           textcoords='offset points', fontsize=26, color=COLORS['text'],
                           weight='bold', ha=ha_align,
                           arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Customize plot with uniform larger font sizes
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Support A (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Bending Moment (kNm)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        # Add subtle support lines without labels
        for x_sup in [0, self.x_support_B/1000]:
            ax.axvline(x=x_sup, color=COLORS['load_arrow'], linewidth=4, alpha=0.4, linestyle='--')

        ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['left'].set_color(COLORS['text'])
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['bottom'].set_color(COLORS['text'])

        # Extend figure margins
        plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.15)
        return fig

def main():
    """Main analysis function."""
    # Create analysis object
    crane = CraneJibAnalysis()

    # Find critical values
    crane.find_critical_values()

    # Create and save plots
    print(f"\n📊 GENERATING PLOTS...")

    # Loading diagram
    fig1 = crane.create_loading_diagram()
    fig1.savefig('crane_jib_loading_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                facecolor='none', edgecolor='none', transparent=True)
    print("✅ Loading diagram saved as 'crane_jib_loading_diagram.svg'")

    # Shear force diagram
    fig2 = crane.create_shear_diagram()
    fig2.savefig('crane_jib_shear_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                facecolor='none', edgecolor='none', transparent=True)
    print("✅ Shear force diagram saved as 'crane_jib_shear_diagram.svg'")

    # Bending moment diagram
    fig3 = crane.create_moment_diagram()
    fig3.savefig('crane_jib_moment_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                facecolor='none', edgecolor='none', transparent=True)
    print("✅ Bending moment diagram saved as 'crane_jib_moment_diagram.svg'")

    plt.close('all')

    print(f"\n🎯 ANALYSIS COMPLETE!")
    print(f"All calculations and visualizations have been generated.")
    print(f"SVG files are optimized for mobile viewing with compatible colors.")

if __name__ == "__main__":
    main()
