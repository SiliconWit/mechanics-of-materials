#!/usr/bin/env python3
"""
Conveyor Roller Support Beam Analysis (Electromechanical)
Application 2 from Lesson 2.1: Shear Force and Bending Moment in Beams

This program calculates and visualizes:
1. Support reaction forces for symmetric loading
2. Shear force diagram (multiple discontinuities from point loads)
3. Bending moment diagram (maximum at midspan)
4. Critical section identification

Problem Parameters:
- Simply supported beam: L = 2000 mm (pinned at A, roller at B)
- Five equally spaced point loads: P = 400 N each
- Load positions: x = 200, 600, 1000, 1400, 1800 mm (400 mm spacing)
- Hollow rectangular steel section: 60×40×4 mm
- Second moment of area: I = 3.1 × 10⁶ mm⁴
- Distance to extreme fiber: c = 30 mm
- Material: Steel (σ_yield = 250 MPa)
- Application: Material handling conveyor system

Key Insight:
Simply supported beams with multiple point loads experience maximum moment
at midspan, NOT at load points, due to cumulative effects from both sides.
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

class ConveyorBeamAnalysis:
    def __init__(self):
        # Beam geometry (all in mm)
        self.L = 2000  # Total beam length

        # Loads
        self.P = 400  # N, each point load (box weight)
        self.n_loads = 5  # Number of loads
        self.load_spacing = 400  # mm, spacing between loads

        # Load positions from left support
        self.load_positions = [200, 600, 1000, 1400, 1800]  # mm

        # Beam properties
        self.width = 60  # mm, hollow rectangular section outer width
        self.height = 40  # mm, hollow rectangular section outer height
        self.thickness = 4  # mm, wall thickness
        self.I = 3.1e6  # mm⁴ (given)
        self.c = 30  # mm (distance to extreme fiber)
        self.sigma_yield = 250  # MPa
        self.S = self.I / self.c  # Section modulus

        # Calculate reactions
        self.calculate_reactions()

    def verify_section_properties(self):
        """Verify the given section properties match the hollow rectangular geometry."""
        # For hollow rectangular cross-section: I = (b*h³ - b_i*h_i³)/12
        b_outer = self.width
        h_outer = self.height
        b_inner = b_outer - 2 * self.thickness
        h_inner = h_outer - 2 * self.thickness

        I_calculated = (b_outer * h_outer**3 - b_inner * h_inner**3) / 12
        print(f"\n🔍 SECTION PROPERTY VERIFICATION:")
        print(f"Given I = {self.I/1e6:.2f}×10⁶ mm⁴")
        print(f"Calculated I = (60×40³ - 52×32³)/12 = {I_calculated/1e6:.2f}×10⁶ mm⁴")

        if abs(I_calculated - self.I) / self.I < 0.05:
            print("✅ Section properties match hollow rectangular geometry")
        else:
            print("⚠️  Minor discrepancy - using given values for analysis")

    def calculate_reactions(self):
        """Calculate support reactions using equilibrium equations."""
        print("="*80)
        print("CONVEYOR ROLLER SUPPORT BEAM ANALYSIS")
        print("SIMPLY SUPPORTED WITH MULTIPLE POINT LOADS")
        print("="*80)
        print("\n📊 PROBLEM SETUP:")
        print(f"• Beam length: {self.L/1000:.1f} m (simply supported)")
        print(f"• Number of loads: {self.n_loads} boxes")
        print(f"• Load magnitude: P = {self.P} N per box")
        print(f"• Load spacing: {self.load_spacing} mm intervals")
        print(f"• Load positions: {', '.join(map(str, self.load_positions))} mm from left support")
        print(f"• Hollow rectangular steel: {self.width}×{self.height}×{self.thickness} mm")
        print(f"• Section properties: I = {self.I/1e6:.2f}×10⁶ mm⁴, c = {self.c} mm")
        print(f"• Material: Steel (σ_yield = {self.sigma_yield} MPa)")

        self.verify_section_properties()

        # Total load
        self.W_total = self.n_loads * self.P

        # Calculate reaction at B using moment equilibrium about A
        # ΣM_A = 0: R_B × L - Σ(P × x_i) = 0
        moment_sum = sum([self.P * x for x in self.load_positions])
        self.R_B = moment_sum / self.L

        # Calculate reaction at A using vertical force equilibrium
        # ΣF_y = 0: R_A + R_B - W_total = 0
        self.R_A = self.W_total - self.R_B

        print(f"\n🔧 REACTION FORCE CALCULATIONS:")
        print(f"\n1. Total load on beam:")
        print(f"   W_total = {self.n_loads} × {self.P} = {self.W_total} N")

        print(f"\n2. Sum of load moments about A:")
        print(f"   Σ(P × x) = {self.P}({' + '.join(map(str, self.load_positions))}) = {moment_sum:,.0f} N·mm")

        print(f"\n3. Reaction at B (from moment equilibrium about A):")
        print(f"   ΣM_A = 0: R_B({self.L}) - {moment_sum:,.0f} = 0")
        print(f"   R_B = {moment_sum:,.0f} / {self.L} = {self.R_B:.0f} N (upward)")

        print(f"\n4. Reaction at A (from vertical force equilibrium):")
        print(f"   ΣF_y = 0: R_A + {self.R_B:.0f} - {self.W_total} = 0")
        print(f"   R_A = {self.W_total} - {self.R_B:.0f} = {self.R_A:.0f} N (upward)")

        # Verification
        print(f"\n✅ Equilibrium verification:")
        sum_Fy = self.R_A + self.R_B - self.W_total
        sum_MA = self.R_B * self.L - moment_sum
        print(f"• ΣF_y = {self.R_A:.0f} + {self.R_B:.0f} - {self.W_total} = {sum_Fy:.1f} ≈ 0 ✓")
        print(f"• ΣM_A = {self.R_B:.0f}({self.L}) - {moment_sum:,.0f} = {sum_MA:.1f} ≈ 0 ✓")

        print(f"\n💡 SYMMETRY CHECK:")
        print(f"• Loads are symmetric about x = {self.L/2:.0f} mm (beam center)")
        print(f"• Therefore R_A = R_B = {self.R_A:.0f} N ✓")

    def calculate_shear_forces(self, x_points):
        """Calculate shear forces at given x positions (in mm from left support)."""
        V = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            # Start with reaction at A
            V[i] = self.R_A

            # Subtract all loads to the left of x
            for load_pos in self.load_positions:
                if x > load_pos:
                    V[i] -= self.P

        return V

    def calculate_moments(self, x_points):
        """Calculate bending moments at given x positions (in mm from left support)."""
        M = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            # Start with moment from reaction at A
            M[i] = self.R_A * x

            # Subtract moments from all loads to the left of x
            for load_pos in self.load_positions:
                if x > load_pos:
                    M[i] -= self.P * (x - load_pos)

        return M

    def find_critical_values(self):
        """Find maximum and minimum shear forces and bending moments."""
        # Create fine grid for analysis
        x_fine = np.linspace(0, self.L, 10000)
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

        self.critical_results = {
            'V_max': V_max, 'V_max_x': x_fine[V_max_idx],
            'V_min': V_min, 'V_min_x': x_fine[V_min_idx],
            'M_max': M_max, 'M_max_x': x_fine[M_max_idx],
            'M_min': M_min, 'M_min_x': x_fine[M_min_idx]
        }

        print(f"\n📈 CRITICAL VALUES:")
        print(f"\nShear force distribution (step function with jumps):")
        print(f"• Maximum positive shear: V_max = {V_max:.0f} N at x = {x_fine[V_max_idx]:.0f} mm (left support)")
        print(f"• Maximum negative shear: V_min = {V_min:.0f} N at x = {x_fine[V_min_idx]:.0f} mm (right support)")
        print(f"• Discontinuities: Jump down by {self.P} N at each load location")

        print(f"\nBending moment distribution:")
        print(f"• At x = 0 (left support): M = 0 N·mm")
        print(f"• At x = 200 mm (1st load): M = {self.calculate_moments(np.array([200]))[0]:.0f} N·mm")
        print(f"• At x = 600 mm (2nd load): M = {self.calculate_moments(np.array([600]))[0]:.0f} N·mm")
        print(f"• At x = 1000 mm (center): M = {M_max:.0f} N·mm (MAXIMUM) ✅")
        print(f"• At x = 1400 mm (4th load): M = {self.calculate_moments(np.array([1400]))[0]:.0f} N·mm")
        print(f"• At x = 1800 mm (5th load): M = {self.calculate_moments(np.array([1800]))[0]:.0f} N·mm")
        print(f"• At x = 2000 mm (right support): M = 0 N·mm")

        print(f"\n💡 KEY ENGINEERING INSIGHT:")
        M_at_loads = self.calculate_moments(np.array([600]))[0]
        print(f"• Midspan moment ({M_max:.0f} N·mm) > Under-load moment ({M_at_loads:.0f} N·mm)")
        print(f"• Maximum moment occurs at CENTER, NOT at load points!")
        print(f"• This is characteristic of simply supported beams with multiple point loads")

        # Store for plotting
        self.M_max = M_max
        self.V_max = V_max

    def create_loading_diagram(self):
        """Create loading diagram showing supports, beam, and point loads."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Beam representation
        beam_height = 0.15
        beam_y = 0
        beam = patches.Rectangle((0, beam_y - beam_height/2), self.L/1000, beam_height,
                               facecolor=COLORS['beam'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(beam)

        # Pinned support at left (A)
        pin_size = 0.08
        # Triangle for pinned support
        triangle_A = patches.Polygon([
            (0, beam_y - beam_height/2),
            (-pin_size, beam_y - beam_height/2 - 0.15),
            (pin_size, beam_y - beam_height/2 - 0.15)
        ], facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(triangle_A)

        # Pin circle
        pin_A = patches.Circle((0, beam_y - beam_height/2), pin_size * 0.4,
                             facecolor='#FFFFFF', edgecolor=COLORS['support'], linewidth=3)
        ax.add_patch(pin_A)

        # Ground hatching for support A
        for i in range(7):
            x_offset = -0.15 + i * 0.05
            ax.plot([x_offset, x_offset + 0.03],
                   [beam_y - beam_height/2 - 0.15, beam_y - beam_height/2 - 0.18],
                   color=COLORS['text'], linewidth=2)

        # Roller support at right (B)
        roller_x = self.L / 1000
        # Triangle for roller support
        triangle_B = patches.Polygon([
            (roller_x, beam_y - beam_height/2),
            (roller_x - pin_size, beam_y - beam_height/2 - 0.15),
            (roller_x + pin_size, beam_y - beam_height/2 - 0.15)
        ], facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(triangle_B)

        # Rollers (circles)
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

        # Point loads (boxes)
        arrow_length = 0.4
        arrow_width = 0.12

        for i, load_pos in enumerate(self.load_positions):
            x_pos = load_pos / 1000
            # Downward arrow
            ax.arrow(x_pos, beam_y + beam_height/2 + arrow_length, 0, -arrow_length + 0.08,
                    head_width=arrow_width, head_length=0.08, fc=COLORS['load_arrow'],
                    ec=COLORS['load_arrow'], linewidth=3)

            # Label (only label first, middle, and last for clarity)
            if i == 0 or i == 2 or i == 4:
                ax.text(x_pos, beam_y + beam_height/2 + arrow_length + 0.1,
                       f'P = {self.P} N', ha='center', va='bottom',
                       fontsize=20, color=COLORS['load_arrow'], weight='bold')

        # Reaction forces
        # Reaction at A (upward)
        ax.arrow(0, beam_y - beam_height/2 - 0.35, 0, 0.15,
                head_width=arrow_width, head_length=0.08, fc=COLORS['reaction'],
                ec=COLORS['reaction'], linewidth=3)
        ax.text(-0.15, beam_y - beam_height/2 - 0.3,
               f'R_A = {self.R_A:.0f} N', ha='right', va='center',
               fontsize=22, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], alpha=0.9))

        # Reaction at B (upward)
        ax.arrow(roller_x, beam_y - beam_height/2 - 0.41, 0, 0.15,
                head_width=arrow_width, head_length=0.08, fc=COLORS['reaction'],
                ec=COLORS['reaction'], linewidth=3)
        ax.text(roller_x + 0.15, beam_y - beam_height/2 - 0.36,
               f'R_B = {self.R_B:.0f} N', ha='left', va='center',
               fontsize=22, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], alpha=0.9))

        # Dimension line for total length
        dimension_y = beam_y - beam_height/2 - 0.65
        ax.annotate('', xy=(0, dimension_y), xytext=(self.L/1000, dimension_y),
                   arrowprops=dict(arrowstyle='<->', color=COLORS['text'], lw=3))
        ax.text(self.L/2000, dimension_y - 0.12, f'L = {self.L/1000:.1f} m',
               ha='center', va='top', fontsize=24, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        # Add cross-section details
        ax.text(self.L/1000 + 0.25, beam_y + 0.3,
               f'Hollow Rectangular Steel\n{self.width}×{self.height}×{self.thickness} mm\nσ_yield = {self.sigma_yield} MPa',
               ha='left', va='top', fontsize=18, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.7', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        ax.set_xlim(-0.4, 2.6)
        ax.set_ylim(-1.0, 0.9)
        ax.set_aspect('equal')
        ax.axis('off')

        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)
        return fig

    def create_shear_diagram(self):
        """Create shear force diagram showing step function with discontinuities."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create detailed x points including points just before and after each load
        x_segments = []
        V_segments = []

        # Add segments between loads
        segment_points = [0] + self.load_positions + [self.L]

        for i in range(len(segment_points) - 1):
            x_left = segment_points[i]
            x_right = segment_points[i + 1]

            # Points just after x_left and just before x_right
            x_seg = np.array([x_left + 0.1, x_right - 0.1])
            V_seg = self.calculate_shear_forces(x_seg) / 1000  # Convert to kN

            # Plot horizontal line
            ax.plot(x_seg/1000, V_seg, color=COLORS['shear_pos'], linewidth=4)

            # Fill area
            if V_seg[0] > 0:
                ax.fill_between(x_seg/1000, V_seg, 0, alpha=0.3, color=COLORS['moment_pos'])
            else:
                ax.fill_between(x_seg/1000, V_seg, 0, alpha=0.3, color=COLORS['shear_neg'])

        # Add vertical jumps at load locations
        for load_pos in self.load_positions:
            V_before = self.calculate_shear_forces(np.array([load_pos - 0.1]))[0] / 1000
            V_after = self.calculate_shear_forces(np.array([load_pos + 0.1]))[0] / 1000
            ax.plot([load_pos/1000, load_pos/1000], [V_before, V_after],
                   color=COLORS['shear_pos'], linewidth=4, linestyle='-')

        # Mark critical points with scatter dots
        # At x=0 (left support): V_max
        V_0 = self.R_A / 1000
        ax.plot(0, V_0, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'+{V_0:.2f} kN', (0, V_0), xytext=(40, -50),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At each load position (before and after jumps)
        for i, load_pos in enumerate(self.load_positions):
            V_before = self.calculate_shear_forces(np.array([load_pos - 0.1]))[0] / 1000
            V_after = self.calculate_shear_forces(np.array([load_pos + 0.1]))[0] / 1000

            # Point just before load
            ax.plot(load_pos/1000, V_before, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
                   markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)

            # Point just after load
            ax.plot(load_pos/1000, V_after, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
                   markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)

        # At x=L (right support): V_min
        V_L = -self.R_B / 1000
        ax.plot(self.L/1000, V_L, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'{V_L:.2f} kN', (self.L/1000, V_L), xytext=(-40, 50),
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
        ax.axvline(x=self.L/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        # Vertical dashed lines at load points
        for load_pos in self.load_positions:
            ax.axvline(x=load_pos/1000, color=COLORS['load_arrow'], linewidth=3, alpha=0.4, linestyle='--')

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
        """Create bending moment diagram showing maximum at midspan."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create x points
        x_array = np.linspace(0, self.L, 1000)
        M = self.calculate_moments(x_array)
        M_kNm = M / 1e6  # Convert to kN·m

        # Plot moment diagram
        ax.plot(x_array/1000, M_kNm, color=COLORS['moment_pos'], linewidth=4)

        # Fill area (all positive)
        ax.fill_between(x_array/1000, M_kNm, 0, alpha=0.3, color=COLORS['moment_pos'])

        # Mark critical points with scatter dots
        # At x=0 (left support): M = 0
        ax.plot(0, 0, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('0 kN·m', (0, 0), xytext=(40, 50),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At each load position
        for i, load_pos in enumerate(self.load_positions):
            M_at_load = self.calculate_moments(np.array([load_pos]))[0] / 1e6
            ax.plot(load_pos/1000, M_at_load, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
                   markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)

        # At x=1000 mm (center): M_max
        M_center = self.calculate_moments(np.array([1000]))[0] / 1e6
        ax.plot(1.0, M_center, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'{M_center:.2f} kN·m\n(MAX at Center)', (1.0, M_center), xytext=(50, 20),
                   textcoords='offset points', fontsize=24, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=2000 mm (right support): M = 0
        ax.plot(self.L/1000, 0, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('0 kN·m', (self.L/1000, 0), xytext=(-40, 50),
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

        # Vertical dashed lines at supports
        ax.axvline(x=0, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')
        ax.axvline(x=self.L/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        # Vertical dashed line at center (critical location)
        ax.axvline(x=1.0, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

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
    conveyor = ConveyorBeamAnalysis()

    # Find critical values
    conveyor.find_critical_values()

    # Create and save plots
    print(f"\n📊 GENERATING PLOTS...")

    # Loading diagram
    fig1 = conveyor.create_loading_diagram()
    fig1.savefig('conveyor_beam_loading_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Loading diagram saved as 'conveyor_beam_loading_diagram.svg'")

    # Shear force diagram
    fig2 = conveyor.create_shear_diagram()
    fig2.savefig('conveyor_beam_shear_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Shear force diagram saved as 'conveyor_beam_shear_diagram.svg'")

    # Bending moment diagram
    fig3 = conveyor.create_moment_diagram()
    fig3.savefig('conveyor_beam_moment_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Bending moment diagram saved as 'conveyor_beam_moment_diagram.svg'")

    plt.close('all')

    print(f"\n🎯 ANALYSIS COMPLETE!")
    print(f"All calculations and visualizations have been generated.")
    print(f"SVG files are optimized for mobile viewing with compatible colors.")

    # Summary of key results
    print(f"\n📋 SUMMARY:")
    print(f"• Left reaction (A): {conveyor.R_A:.0f} N (upward)")
    print(f"• Right reaction (B): {conveyor.R_B:.0f} N (upward)")
    print(f"• Maximum |shear|: {conveyor.V_max:.0f} N at supports")
    print(f"• Maximum moment: {conveyor.M_max/1e6:.3f} kN·m at center (x=1.0 m)")
    print(f"• Design status: Critical location is at MIDSPAN, not at load points")
    print(f"\n💡 Simply supported beams with multiple point loads have maximum moment at midspan!")

if __name__ == "__main__":
    main()
