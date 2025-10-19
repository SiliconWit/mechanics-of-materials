#!/usr/bin/env python3
"""
Solar Tracker Arm Analysis (Electronics/Mechatronics)
Application 3 from Lesson 2.1: Shear Force and Bending Moment in Beams

This program calculates and visualizes:
1. Support reaction forces for overhanging beam configuration
2. Shear force diagram (with discontinuity at intermediate support)
3. Bending moment diagram (positive and negative regions)
4. Critical section identification

Problem Parameters:
- Overhanging simply supported beam: L_total = 3.0 m (2.5 m span + 0.5 m overhang)
- Support A (pinned) at x = 0
- Support B (roller) at x = 2.5 m
- Uniformly distributed load: w = 300 N/m across entire length
- Point load at tip: P = 600 N at x = 3.0 m (clamp mechanism)
- Cross-section: Structural steel I-beam (I = 6.8×10⁶ mm⁴, c = 40 mm)
- Material: Structural steel (σ_yield = 250 MPa)
- Application: Solar panel tracking system

Key Insight:
Overhanging beams experience both positive and negative bending moments.
The maximum negative moment at the intermediate support is typically larger
than the maximum positive moment in the span.
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
    'spring': '#00d000',         # Green for spring
    'shear_pos': '#405ab9',      # Blue for positive shear
    'shear_neg': '#ff8c36',      # Orange for negative shear
    'moment_pos': '#405ab9',     # Blue for positive moment
    'moment_neg': '#ff8c36',     # Orange for negative moment
    'text': '#405ab9',           # Blue for all text/axes/labels
    'grid': '#9ea388',           # Gray-green from SVG
    'support': '#405ab9',        # Blue for supports
    'wire': '#FFD700'            # Gold for overhead wire
}

class SolarTrackerArmAnalysis:
    def __init__(self):
        # Beam geometry (all in mm)
        self.L_span = 2500  # Span between supports
        self.L_overhang = 500  # Overhang length
        self.L_total = 3000  # Total beam length

        # Supports
        self.x_A = 0  # Pinned support location
        self.x_B = 2500  # Roller support location

        # Loads
        self.w = 300  # N/m, uniformly distributed load (panel weight + wind)
        self.P = 600  # N, point load at tip (clamp mechanism)

        # Beam properties
        self.I = 6.8e6  # mm⁴, I-beam section
        self.c = 40  # mm, distance to extreme fiber
        self.sigma_yield = 250  # MPa
        self.S = self.I / self.c  # Section modulus

        # Calculate reactions
        self.calculate_reactions()

    def verify_section_properties(self):
        """Display section properties information."""
        print(f"\n🔍 SECTION PROPERTY INFORMATION:")
        print(f"Given I = {self.I/1e6:.2f}×10⁶ mm⁴ (structural steel I-beam)")
        print(f"Section modulus S = I/c = {self.S/1000:.2f}×10³ mm³")
        print(f"Distance to extreme fiber c = {self.c} mm")

    def calculate_reactions(self):
        """Calculate support reactions using equilibrium equations."""
        print("="*80)
        print("SOLAR TRACKER ARM ANALYSIS")
        print("OVERHANGING SIMPLY SUPPORTED BEAM")
        print("="*80)
        print("\n📊 PROBLEM SETUP:")
        print(f"• Total beam length: {self.L_total/1000:.1f} m ({self.L_span/1000:.1f} m span + {self.L_overhang/1000:.1f} m overhang)")
        print(f"• Support A (pinned): x = {self.x_A/1000:.1f} m")
        print(f"• Support B (roller): x = {self.x_B/1000:.1f} m")
        print(f"• Uniformly distributed load: w = {self.w} N/m across entire length")
        print(f"• Point load at tip: P = {self.P} N at x = {self.L_total/1000:.1f} m")
        print(f"• Cross-section: Structural steel I-beam")
        print(f"• Section properties: I = {self.I/1e6:.2f}×10⁶ mm⁴, c = {self.c} mm")
        print(f"• Material: Steel (σ_yield = {self.sigma_yield} MPa)")

        self.verify_section_properties()

        # Total distributed load
        self.W_total = self.w * (self.L_total / 1000)  # Convert to meters for calculation

        # Calculate reaction at B using moment equilibrium about A
        # ΣM_A = 0: R_B × 2.5 - w × 3.0 × 1.5 - P × 3.0 = 0
        moment_from_w = self.w * (self.L_total / 1000) * (self.L_total / 1000 / 2)
        moment_from_P = self.P * (self.L_total / 1000)
        self.R_B = (moment_from_w + moment_from_P) / (self.L_span / 1000)

        # Calculate reaction at A using vertical force equilibrium
        # ΣF_y = 0: R_A + R_B - W_total - P = 0
        self.R_A = self.W_total + self.P - self.R_B

        print(f"\n🔧 REACTION FORCE CALCULATIONS:")
        print(f"\n1. Total distributed load:")
        print(f"   W_total = w × L_total = {self.w} × {self.L_total/1000:.1f} = {self.W_total:.1f} N")

        print(f"\n2. Sum of moments about A (counterclockwise positive):")
        print(f"   From UDL: w × L_total × (L_total/2) = {self.w} × {self.L_total/1000:.1f} × {self.L_total/2000:.2f} = {moment_from_w:.1f} N·m")
        print(f"   From P: P × L_total = {self.P} × {self.L_total/1000:.1f} = {moment_from_P:.1f} N·m")
        print(f"   Total moment = {moment_from_w:.1f} + {moment_from_P:.1f} = {moment_from_w + moment_from_P:.1f} N·m")

        print(f"\n3. Reaction at B (from moment equilibrium about A):")
        print(f"   ΣM_A = 0: R_B({self.L_span/1000:.1f}) - {moment_from_w + moment_from_P:.1f} = 0")
        print(f"   R_B = {moment_from_w + moment_from_P:.1f} / {self.L_span/1000:.1f} = {self.R_B:.0f} N (upward)")

        print(f"\n4. Reaction at A (from vertical force equilibrium):")
        print(f"   ΣF_y = 0: R_A + {self.R_B:.0f} - {self.W_total:.1f} - {self.P} = 0")
        print(f"   R_A = {self.W_total:.1f} + {self.P} - {self.R_B:.0f} = {self.R_A:.0f} N (upward)")

        # Verification by moments about B
        print(f"\n5. Verification by moments about B:")
        moment_R_A = self.R_A * (self.L_span / 1000)
        moment_w_span = self.w * (self.L_span / 1000) * (self.L_span / 1000 / 2)
        moment_w_overhang = self.w * (self.L_overhang / 1000) * (self.L_overhang / 1000 / 2)
        moment_P = self.P * (self.L_overhang / 1000)

        print(f"   Moment from R_A: +{self.R_A:.0f}({self.L_span/1000:.1f}) = +{moment_R_A:.1f} N·m")
        print(f"   Moment from UDL on span: -{self.w}({self.L_span/1000:.1f})({self.L_span/2000:.2f}) = -{moment_w_span:.1f} N·m")
        print(f"   Moment from UDL on overhang: +{self.w}({self.L_overhang/1000:.1f})({self.L_overhang/2000:.2f}) = +{moment_w_overhang:.1f} N·m")
        print(f"   Moment from P: +{self.P}({self.L_overhang/1000:.1f}) = +{moment_P:.1f} N·m")

        sum_MB = moment_R_A - moment_w_span + moment_w_overhang + moment_P
        print(f"   ΣM_B = {moment_R_A:.1f} - {moment_w_span:.1f} + {moment_w_overhang:.1f} + {moment_P:.1f} = {sum_MB:.1f} ≈ 0 ✓")

        # Equilibrium verification
        print(f"\n✅ Equilibrium verification:")
        sum_Fy = self.R_A + self.R_B - self.W_total - self.P
        print(f"• ΣF_y = {self.R_A:.0f} + {self.R_B:.0f} - {self.W_total:.1f} - {self.P} = {sum_Fy:.1f} ≈ 0 ✓")

    def calculate_shear_forces(self, x_points):
        """Calculate shear forces at given x positions (in mm from left support)."""
        V = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            if x <= self.x_B:
                # Region 1: Between supports (0 ≤ x ≤ 2500 mm)
                # V(x) = R_A - w×x
                V[i] = self.R_A - self.w * (x / 1000)
            else:
                # Region 2: Overhang (2500 < x ≤ 3000 mm)
                # V(x) = R_A - w×x + R_B
                V[i] = self.R_A - self.w * (x / 1000) + self.R_B

        return V

    def calculate_moments(self, x_points):
        """Calculate bending moments at given x positions (in mm from left support)."""
        M = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            x_m = x / 1000  # Convert to meters

            if x <= self.x_B:
                # Region 1: Between supports (0 ≤ x ≤ 2500 mm)
                # M(x) = R_A × x - w × x × (x/2) = 240x - 150x²
                M[i] = self.R_A * x_m - self.w * x_m * x_m / 2
            else:
                # Region 2: Overhang (2500 < x ≤ 3000 mm)
                # M(x) = R_A × x - w × x × (x/2) + R_B × (x - 2.5)
                # M(x) = 1500x - 150x² - 3150
                M[i] = self.R_A * x_m - self.w * x_m * x_m / 2 + self.R_B * (x_m - self.L_span / 1000)

        return M

    def find_critical_values(self):
        """Find maximum and minimum shear forces and bending moments."""
        # Create fine grid for analysis
        x_fine = np.linspace(0, self.L_total, 10000)
        V_fine = self.calculate_shear_forces(x_fine)
        M_fine = self.calculate_moments(x_fine)

        # Find maximum absolute values
        V_max = np.max(V_fine)
        V_min = np.min(V_fine)
        M_max = np.max(M_fine)
        M_min = np.min(M_fine)

        # Find locations
        V_max_idx = np.argmax(V_fine)
        V_min_idx = np.argmin(V_fine)
        M_max_idx = np.argmax(M_fine)
        M_min_idx = np.argmin(M_fine)

        # Find zero shear location (max positive moment)
        zero_shear_idx = np.argmin(np.abs(V_fine[0:np.where(x_fine <= self.x_B)[0][-1]]))
        x_zero_shear = x_fine[zero_shear_idx]
        M_at_zero_shear = M_fine[zero_shear_idx]

        self.critical_results = {
            'V_max': V_max, 'V_max_x': x_fine[V_max_idx],
            'V_min': V_min, 'V_min_x': x_fine[V_min_idx],
            'M_max': M_max, 'M_max_x': x_fine[M_max_idx],
            'M_min': M_min, 'M_min_x': x_fine[M_min_idx],
            'x_zero_shear': x_zero_shear,
            'M_at_zero_shear': M_at_zero_shear
        }

        print(f"\n📈 CRITICAL VALUES:")
        print(f"\nShear force distribution:")
        print(f"• At x = 0 (support A): V(0) = {self.calculate_shear_forces(np.array([0]))[0]:.0f} N")
        print(f"• At x = 0.8 m (zero shear): V = 0 N (indicates max positive moment)")
        print(f"• Just before support B (x = 2.5⁻ m): V = {self.calculate_shear_forces(np.array([2499]))[0]:.0f} N")
        print(f"• Just after support B (x = 2.5⁺ m): V = {self.calculate_shear_forces(np.array([2501]))[0]:.0f} N (jump of {self.R_B:.0f} N)")
        print(f"• Just before tip (x = 3.0⁻ m): V = {self.calculate_shear_forces(np.array([2999]))[0]:.0f} N")
        print(f"• Maximum positive shear: V_max = {V_max:.0f} N at x = {x_fine[V_max_idx]/1000:.2f} m")
        print(f"• Maximum negative shear: V_min = {V_min:.0f} N at x = {x_fine[V_min_idx]/1000:.2f} m")

        print(f"\nBending moment distribution:")
        print(f"• At x = 0 (support A): M = 0 N·m")
        print(f"• At x = 0.8 m (zero shear): M = {M_at_zero_shear:.1f} N·m (MAX POSITIVE) ✅")
        print(f"• At x = 2.5 m (support B): M = {self.calculate_moments(np.array([2500]))[0]:.1f} N·m (MAX NEGATIVE) ✅")
        print(f"• At x = 3.0 m (tip): M = {self.calculate_moments(np.array([3000]))[0]:.1f} N·m")

        print(f"\n💡 KEY ENGINEERING INSIGHT:")
        print(f"• Maximum positive moment: +{M_max:.1f} N·m at x = {x_zero_shear/1000:.2f} m")
        print(f"• Maximum negative moment: {M_min:.1f} N·m at support B (x = 2.5 m)")
        print(f"• Critical location: Support B due to larger moment magnitude ({abs(M_min):.1f} > {M_max:.1f})")
        print(f"• Overhanging beams experience both positive and negative bending")

        # Store for plotting
        self.M_max = M_max
        self.M_min = M_min
        self.V_max = V_max
        self.x_zero_shear = x_zero_shear
        self.M_at_zero_shear = M_at_zero_shear

    def create_loading_diagram(self):
        """Create loading diagram showing supports, beam, distributed load, and point load."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Beam representation
        beam_height = 0.15
        beam_y = 0
        beam = patches.Rectangle((0, beam_y - beam_height/2), self.L_total/1000, beam_height,
                               facecolor=COLORS['beam'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(beam)

        # Pinned support at left (A)
        pin_size = 0.08
        triangle_A = patches.Polygon([
            (0, beam_y - beam_height/2),
            (-pin_size, beam_y - beam_height/2 - 0.15),
            (pin_size, beam_y - beam_height/2 - 0.15)
        ], facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(triangle_A)

        pin_A = patches.Circle((0, beam_y - beam_height/2), pin_size * 0.4,
                             facecolor='#FFFFFF', edgecolor=COLORS['support'], linewidth=3)
        ax.add_patch(pin_A)

        # Ground hatching for support A
        for i in range(7):
            x_offset = -0.15 + i * 0.05
            ax.plot([x_offset, x_offset + 0.03],
                   [beam_y - beam_height/2 - 0.15, beam_y - beam_height/2 - 0.18],
                   color=COLORS['text'], linewidth=2)

        # Roller support at B
        roller_x = self.x_B / 1000
        triangle_B = patches.Polygon([
            (roller_x, beam_y - beam_height/2),
            (roller_x - pin_size, beam_y - beam_height/2 - 0.15),
            (roller_x + pin_size, beam_y - beam_height/2 - 0.15)
        ], facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(triangle_B)

        roller_1 = patches.Circle((roller_x - pin_size/2, beam_y - beam_height/2 - 0.15), pin_size * 0.3,
                                 facecolor='#FFFFFF', edgecolor=COLORS['support'], linewidth=3)
        roller_2 = patches.Circle((roller_x + pin_size/2, beam_y - beam_height/2 - 0.15), pin_size * 0.3,
                                 facecolor='#FFFFFF', edgecolor=COLORS['support'], linewidth=3)
        ax.add_patch(roller_1)
        ax.add_patch(roller_2)

        # Ground hatching for support B
        for i in range(7):
            x_offset = roller_x - 0.15 + i * 0.05
            ax.plot([x_offset, x_offset + 0.03],
                   [beam_y - beam_height/2 - 0.21, beam_y - beam_height/2 - 0.24],
                   color=COLORS['text'], linewidth=2)

        # Distributed load (downward arrows along entire beam)
        n_arrows = 12
        arrow_spacing = (self.L_total/1000) / n_arrows
        arrow_length = 0.5
        arrow_width = 0.10

        for i in range(n_arrows + 1):
            x_arrow = i * arrow_spacing
            ax.arrow(x_arrow, beam_y + beam_height/2 + arrow_length, 0, -arrow_length + 0.08,
                    head_width=arrow_width, head_length=0.08, fc=COLORS['load_arrow'],
                    ec=COLORS['load_arrow'], linewidth=2, alpha=0.8)

        # Distributed load label
        ax.text(self.L_total/2000, beam_y + beam_height/2 + arrow_length + 0.25,
               f'w = {self.w} N/m\n(Panel + Wind)', ha='center', va='bottom',
               fontsize=22, color=COLORS['load_arrow'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['load_arrow'], alpha=0.9))

        # Point load at tip (downward)
        tip_x = self.L_total / 1000
        conc_arrow_length = 0.7
        conc_arrow_width = 0.15
        ax.arrow(tip_x, beam_y + beam_height/2 + conc_arrow_length, 0, -conc_arrow_length + 0.08,
                head_width=conc_arrow_width, head_length=0.08, fc=COLORS['load_arrow'],
                ec=COLORS['load_arrow'], linewidth=3)
        ax.text(tip_x + 0.25, beam_y + beam_height/2 + conc_arrow_length/2,
               f'P = {self.P} N\n(Clamp)', ha='left', va='center',
               fontsize=22, color=COLORS['load_arrow'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['load_arrow'], alpha=0.9))

        # Reaction forces
        # Reaction at A (upward)
        ax.arrow(0, beam_y - beam_height/2 - 0.35, 0, 0.15,
                head_width=conc_arrow_width, head_length=0.08, fc=COLORS['reaction'],
                ec=COLORS['reaction'], linewidth=3)
        ax.text(-0.2, beam_y - beam_height/2 - 0.3,
               f'R_A = {self.R_A:.0f} N', ha='right', va='center',
               fontsize=22, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], alpha=0.9))

        # Reaction at B (upward)
        ax.arrow(roller_x, beam_y - beam_height/2 - 0.41, 0, 0.15,
                head_width=conc_arrow_width, head_length=0.08, fc=COLORS['reaction'],
                ec=COLORS['reaction'], linewidth=3)
        ax.text(roller_x, beam_y - beam_height/2 - 0.65,
               f'R_B = {self.R_B:.0f} N', ha='center', va='top',
               fontsize=22, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], alpha=0.9))

        # Dimension lines
        dimension_y = beam_y - beam_height/2 - 0.95
        # Span dimension
        ax.annotate('', xy=(0, dimension_y), xytext=(roller_x, dimension_y),
                   arrowprops=dict(arrowstyle='<->', color=COLORS['text'], lw=3))
        ax.text(roller_x/2, dimension_y - 0.12, f'Span = {self.L_span/1000:.1f} m',
               ha='center', va='top', fontsize=22, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        # Overhang dimension
        dimension_y2 = beam_y + beam_height/2 + 1.05
        ax.annotate('', xy=(roller_x, dimension_y2), xytext=(tip_x, dimension_y2),
                   arrowprops=dict(arrowstyle='<->', color=COLORS['text'], lw=3))
        ax.text((roller_x + tip_x)/2, dimension_y2 + 0.12, f'Overhang = {self.L_overhang/1000:.1f} m',
               ha='center', va='bottom', fontsize=22, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        # Add cross-section details
        ax.text(tip_x + 0.3, beam_y - 0.2,
               f'Structural Steel I-Beam\nI = {self.I/1e6:.1f}×10⁶ mm⁴\nσ_yield = {self.sigma_yield} MPa',
               ha='left', va='top', fontsize=18, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.7', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        ax.set_xlim(-0.5, 3.8)
        ax.set_ylim(-1.3, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')

        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)
        return fig

    def create_shear_diagram(self):
        """Create shear force diagram showing linear variation with jump at support B."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create separate arrays for each region
        # Region 1: 0 to 2.5 m (before support B)
        x_region1 = np.linspace(0, self.x_B - 1, 500)
        V_region1 = self.calculate_shear_forces(x_region1) / 1000  # Convert to kN

        # Region 2: 2.5 to 3.0 m (after support B)
        x_region2 = np.linspace(self.x_B + 1, self.L_total, 500)
        V_region2 = self.calculate_shear_forces(x_region2) / 1000

        # Plot regions
        ax.plot(x_region1/1000, V_region1, color=COLORS['shear_pos'], linewidth=4)
        ax.plot(x_region2/1000, V_region2, color=COLORS['shear_pos'], linewidth=4)

        # Fill areas
        # Region 1 - mixed positive and negative
        mask_pos_1 = V_region1 > 0
        mask_neg_1 = V_region1 < 0
        ax.fill_between(x_region1[mask_pos_1]/1000, V_region1[mask_pos_1], 0,
                       alpha=0.3, color=COLORS['moment_pos'])
        ax.fill_between(x_region1[mask_neg_1]/1000, V_region1[mask_neg_1], 0,
                       alpha=0.3, color=COLORS['shear_neg'])

        # Region 2 - all positive
        ax.fill_between(x_region2/1000, V_region2, 0, alpha=0.3, color=COLORS['moment_pos'])

        # Vertical jump at support B
        V_before_B = self.calculate_shear_forces(np.array([self.x_B - 1]))[0] / 1000
        V_after_B = self.calculate_shear_forces(np.array([self.x_B + 1]))[0] / 1000
        ax.plot([self.x_B/1000, self.x_B/1000], [V_before_B, V_after_B],
               color=COLORS['shear_pos'], linewidth=4, linestyle='-')

        # Mark critical points with scatter dots
        # At x=0 (support A)
        V_0 = self.calculate_shear_forces(np.array([0]))[0] / 1000
        ax.plot(0, V_0, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'+{V_0:.2f} kN', (0, V_0), xytext=(40, 40),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At zero shear location (x ≈ 0.8 m)
        V_zero = 0
        ax.plot(self.x_zero_shear/1000, V_zero, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'0 kN\n(x={self.x_zero_shear/1000:.1f}m)', (self.x_zero_shear/1000, V_zero), xytext=(30, -80),
                   textcoords='offset points', fontsize=22, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Just before support B
        ax.plot(self.x_B/1000, V_before_B, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'{V_before_B:.2f} kN', (self.x_B/1000, V_before_B), xytext=(-60, 10),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Just after support B
        ax.plot(self.x_B/1000, V_after_B, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'+{V_after_B:.2f} kN', (self.x_B/1000, V_after_B), xytext=(-160, -30),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At tip (before point load)
        V_tip = self.calculate_shear_forces(np.array([self.L_total - 1]))[0] / 1000
        ax.plot(self.L_total/1000, V_tip, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'+{V_tip:.2f} kN', (self.L_total/1000, V_tip), xytext=(-40, -30),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Customize plot
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Left Support (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Shear Force (kN)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        # Vertical dashed lines at supports
        ax.axvline(x=0, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')
        ax.axvline(x=self.x_B/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')
        ax.axvline(x=self.L_total/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        # Vertical dashed line at zero shear
        ax.axvline(x=self.x_zero_shear/1000, color=COLORS['load_arrow'], linewidth=3, alpha=0.4, linestyle='--')

        ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['left'].set_color(COLORS['text'])
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['bottom'].set_color(COLORS['text'])

        plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.15)
        return fig

    def create_moment_diagram(self):
        """Create bending moment diagram showing positive and negative regions."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create x points for entire beam
        x_array = np.linspace(0, self.L_total, 1000)
        M = self.calculate_moments(x_array)
        M_kNm = M / 1000  # Convert to kN·m

        # Plot moment diagram
        ax.plot(x_array/1000, M_kNm, color=COLORS['moment_pos'], linewidth=4)

        # Fill areas - positive and negative regions
        mask_pos = M_kNm > 0
        mask_neg = M_kNm < 0
        ax.fill_between(x_array[mask_pos]/1000, M_kNm[mask_pos], 0,
                       alpha=0.3, color=COLORS['moment_pos'])
        ax.fill_between(x_array[mask_neg]/1000, M_kNm[mask_neg], 0,
                       alpha=0.3, color=COLORS['moment_neg'])

        # Mark critical points with scatter dots
        # At x=0 (support A): M = 0
        ax.plot(0, 0, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('0 kN·m', (0, 0), xytext=(40, 10),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At zero shear location (max positive moment)
        ax.plot(self.x_zero_shear/1000, self.M_at_zero_shear/1000, 'o', markersize=18,
               color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'+{self.M_at_zero_shear/1000:.1f} kN·m\n(MAX POS)',
                   (self.x_zero_shear/1000, self.M_at_zero_shear/1000), xytext=(30, 10),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At support B (max negative moment)
        M_B = self.calculate_moments(np.array([self.x_B]))[0] / 1000
        ax.plot(self.x_B/1000, M_B, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'{M_B:.1f} kN·m\n(MAX NEG)', (self.x_B/1000, M_B), xytext=(30, 10),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At tip: M = 0
        M_tip = self.calculate_moments(np.array([self.L_total]))[0] / 1000
        ax.plot(self.L_total/1000, M_tip, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'{M_tip:.1f} kN·m', (self.L_total/1000, M_tip), xytext=(-60, 60),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Customize plot
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Left Support (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Bending Moment (kN·m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        # Vertical dashed lines at critical locations
        ax.axvline(x=0, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')
        ax.axvline(x=self.x_zero_shear/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')
        ax.axvline(x=self.x_B/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')
        ax.axvline(x=self.L_total/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['left'].set_color(COLORS['text'])
        ax.spines['bottom'].set_color(COLORS['text'])

        plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.15)
        return fig

def main():
    """Main analysis function."""
    # Create analysis object
    solar_tracker = SolarTrackerArmAnalysis()

    # Find critical values
    solar_tracker.find_critical_values()

    # Create and save plots
    print(f"\n📊 GENERATING PLOTS...")

    # Loading diagram
    fig1 = solar_tracker.create_loading_diagram()
    fig1.savefig('solar_tracker_arm_loading_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Loading diagram saved as 'solar_tracker_arm_loading_diagram.svg'")

    # Shear force diagram
    fig2 = solar_tracker.create_shear_diagram()
    fig2.savefig('solar_tracker_arm_shear_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Shear force diagram saved as 'solar_tracker_arm_shear_diagram.svg'")

    # Bending moment diagram
    fig3 = solar_tracker.create_moment_diagram()
    fig3.savefig('solar_tracker_arm_moment_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Bending moment diagram saved as 'solar_tracker_arm_moment_diagram.svg'")

    plt.close('all')

    print(f"\n🎯 ANALYSIS COMPLETE!")
    print(f"All calculations and visualizations have been generated.")
    print(f"SVG files are optimized for mobile viewing with compatible colors.")

    # Summary of key results
    print(f"\n📋 SUMMARY:")
    print(f"• Left reaction (A): {solar_tracker.R_A:.0f} N (upward)")
    print(f"• Right reaction (B): {solar_tracker.R_B:.0f} N (upward)")
    print(f"• Maximum positive shear: {solar_tracker.V_max:.0f} N just after support B")
    print(f"• Maximum negative shear: {abs(solar_tracker.critical_results['V_min']):.0f} N just before support B")
    print(f"• Maximum positive moment: {solar_tracker.M_max:.1f} N·m at x={solar_tracker.x_zero_shear/1000:.2f} m")
    print(f"• Maximum negative moment: {abs(solar_tracker.M_min):.1f} N·m at support B (x=2.5 m)")
    print(f"• Critical location: Support B (larger moment magnitude)")
    print(f"\n💡 Overhanging beams have both positive and negative bending moments!")

if __name__ == "__main__":
    main()
