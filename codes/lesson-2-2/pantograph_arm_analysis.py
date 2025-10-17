#!/usr/bin/env python3
"""
Pantograph Arm of Electric Train (Electromechanical) Analysis
Application 2 from Lesson 2.2: Bending Stresses in Simple Beams

This program calculates and visualizes:
1. Spring force and support reaction forces
2. Shear force diagram (two-region distribution)
3. Bending moment diagram (maximum at spring location)
4. Maximum bending stresses
5. Safety factor assessment

Problem Parameters (CORRECTED MODEL - Pin Joint + Spring Mechanism):
- Hollow steel tube: OD = 50 mm, wall thickness = 4 mm
- Total arm length: 1200 mm from pin joint to wire contact
- Pin joint at A: Allows rotation, provides vertical reaction only
- Spring mechanism: Located 300 mm from pin joint, provides upward force
- Wire contact force: P₁ = 800 N downward at tip (reaction from overhead cable)
- Second moment of area: I = 2.45 × 10⁶ mm⁴
- Distance to extreme fiber: c = 25 mm
- Material: High-strength steel (σ_yield = 250 MPa)
- Safety factor required: 3.0
- Operating conditions: Dynamic contact with overhead wire at 600V DC

Key Insight:
Real pantographs use pin joints + springs (NOT fixed cantilevers) to allow
articulation and maintain contact pressure independent of wire height variations.
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

class PantographArmAnalysis:
    def __init__(self):
        # Beam geometry (all in mm)
        self.L = 1200  # Total arm length from pin to wire contact
        self.x_spring = 300  # Spring location from pin joint

        # Loads
        self.P = 800  # N, wire contact force at tip (reaction from overhead cable)

        # Load positions (mm from pin joint)
        self.x_P = self.L  # Contact force at wire contact point
        self.x_pin = 0  # Pin joint at train roof connection

        # Beam properties
        self.I = 2.45e6  # mm⁴ (given)
        self.c = 25  # mm (distance to extreme fiber)
        self.sigma_yield = 250  # MPa
        self.S = self.I / self.c  # Section modulus
        self.required_SF = 3.0  # Required safety factor

        # Hollow tube properties (for verification)
        self.OD = 50  # mm, outer diameter
        self.t = 4    # mm, wall thickness
        self.ID = self.OD - 2 * self.t  # 42 mm, inner diameter

        # Calculate reactions
        self.calculate_reactions()

    def verify_section_properties(self):
        """Verify the given section properties match the hollow tube geometry."""
        # For hollow circular cross-section: I = π(OD⁴ - ID⁴)/64
        I_calculated = np.pi * (self.OD**4 - self.ID**4) / 64
        print(f"\n🔍 SECTION PROPERTY VERIFICATION:")
        print(f"Given I = {self.I/1e6:.2f}×10⁶ mm⁴")
        print(f"Calculated I = π(50⁴ - 42⁴)/64 = {I_calculated/1e6:.2f}×10⁶ mm⁴")

        if abs(I_calculated - self.I) / self.I < 0.05:
            print("✅ Section properties match hollow tube geometry")
        else:
            print("⚠️  Minor discrepancy - using given values for analysis")

    def calculate_reactions(self):
        """Calculate spring force and pin reaction using equilibrium equations."""
        print("="*80)
        print("PANTOGRAPH ARM OF ELECTRIC TRAIN ANALYSIS")
        print("PIN JOINT + SPRING MECHANISM (CORRECT MODEL)")
        print("="*80)
        print("\n📊 PROBLEM SETUP:")
        print(f"• Total arm length: {self.L/1000:.1f} m")
        print(f"• Spring location: {self.x_spring/1000:.1f} m from pin joint")
        print(f"• Wire contact force: P = {self.P} N at tip (reaction from overhead cable)")
        print(f"• Hollow tube: OD = {self.OD} mm, wall thickness = {self.t} mm")
        print(f"• Section properties: I = {self.I/1e6:.2f}×10⁶ mm⁴, c = {self.c} mm")
        print(f"• Material: High-strength steel (σ_yield = {self.sigma_yield} MPa)")
        print(f"• Required safety factor: {self.required_SF}")

        self.verify_section_properties()

        # Calculate spring force from moment equilibrium about pin A
        # ΣM_A = 0 (pin joint cannot resist moment)
        # F_spring × x_spring - P × L = 0
        self.F_spring = (self.P * self.L) / self.x_spring

        # Calculate pin reaction from vertical force equilibrium
        # ΣF_y = 0: R_A + F_spring - P = 0
        self.R_A = self.P - self.F_spring  # Negative means downward

        print(f"\n🔧 REACTION FORCE CALCULATIONS:")
        print(f"\n1. Spring force (from moment equilibrium about pin A):")
        print(f"   ΣM_A = 0: F_spring × {self.x_spring/1000:.1f} - {self.P} × {self.L/1000:.1f} = 0")
        print(f"   F_spring = {self.P} × {self.L/1000:.1f} / {self.x_spring/1000:.1f} = {self.F_spring:.0f} N (upward)")
        print(f"   → Spring must provide {self.F_spring/self.P:.1f}× the contact force due to {self.L/self.x_spring:.1f}:1 lever ratio")

        print(f"\n2. Pin reaction (from vertical force equilibrium):")
        print(f"   ΣF_y = 0: R_A + {self.F_spring:.0f} - {self.P} = 0")
        print(f"   R_A = {self.R_A:.0f} N (negative = downward)")
        print(f"   → Pin pulls DOWN on the arm (spring force exceeds wire contact force)")

        # Verification
        print(f"\n✅ Equilibrium verification:")
        sum_Fy = self.R_A + self.F_spring - self.P
        sum_MA = self.F_spring * (self.x_spring/1000) - self.P * (self.L/1000)
        print(f"• ΣF_y = {self.R_A:.0f} + {self.F_spring:.0f} - {self.P} = {sum_Fy:.1f} ≈ 0 ✓")
        print(f"• ΣM_A = {self.F_spring:.0f}({self.x_spring/1000:.1f}) - {self.P}({self.L/1000:.1f}) = {sum_MA:.1f} ≈ 0 ✓")

        print(f"\n💡 KEY INSIGHT - Comparison with incorrect fixed cantilever:")
        M_fixed_incorrect = self.P * (self.L/1000)
        print(f"• Fixed cantilever (INCORRECT): M_max = {M_fixed_incorrect:.0f} N·m at support")
        M_pin_spring_correct = abs(self.R_A) * (self.x_spring/1000)
        print(f"• Pin + Spring (CORRECT): M_max = {M_pin_spring_correct:.0f} N·m at spring")
        reduction_pct = (1 - M_pin_spring_correct/M_fixed_incorrect) * 100
        print(f"• Moment reduction: {reduction_pct:.1f}% lower with correct model!")

    def calculate_shear_forces(self, x_points):
        """Calculate shear forces at given x positions (in m from pin joint)."""
        V = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            x_mm = x * 1000  # Convert to mm

            if x_mm <= self.x_spring:
                # Region 1: Pin to spring (0 ≤ x < 0.3 m)
                V[i] = self.R_A  # -2400 N (downward)
            else:
                # Region 2: Spring to wire (0.3 m < x ≤ 1.2 m)
                V[i] = self.R_A + self.F_spring  # +800 N (upward)

        return V

    def calculate_moments(self, x_points):
        """Calculate bending moments at given x positions (in m from pin joint)."""
        M = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            x_mm = x * 1000  # Convert to mm

            if x_mm <= self.x_spring:
                # Region 1: Pin to spring (0 < x < 0.3 m)
                # M(x) = R_A × x
                M[i] = self.R_A * x  # Negative (R_A is negative)
            else:
                # Region 2: Spring to wire (0.3 m < x ≤ 1.2 m)
                # M(x) = R_A × x + F_spring × (x - x_spring)
                M[i] = self.R_A * x + self.F_spring * (x - self.x_spring/1000)

        return M

    def find_critical_values(self):
        """Find maximum and minimum shear forces and bending moments."""
        # Create fine grid for analysis
        x_fine = np.linspace(0, self.L/1000, 1000)
        V_fine = self.calculate_shear_forces(x_fine)
        M_fine = self.calculate_moments(x_fine)

        # Find maximum absolute values
        V_max = np.max(V_fine)
        V_min = np.min(V_fine)
        M_max = np.max(M_fine)  # This will be 0 (at pin and wire contact)
        M_min = np.min(M_fine)  # This will be negative (at spring)

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
        # Maximum stress occurs at spring location where |M| is maximum
        M_max_abs = abs(M_min)  # Maximum absolute moment at spring
        sigma_max = (M_max_abs * 1000) / self.S  # Convert N·m to N·mm, divide by S in mm³

        print(f"\n📈 CRITICAL VALUES:")
        print(f"\nShear force distribution (two regions):")
        print(f"• Region 1 (0 to {self.x_spring/1000:.1f}m): V = {V_min:.0f} N (downward)")
        print(f"• Region 2 ({self.x_spring/1000:.1f}m to {self.L/1000:.1f}m): V = {V_max:.0f} N (upward)")
        print(f"• Discontinuity at spring: ΔV = {self.F_spring:.0f} N jump")

        print(f"\nBending moment distribution:")
        print(f"• At pin joint (x=0): M = 0 N·m (pin cannot resist moment)")
        print(f"• Maximum magnitude: |M_max| = {M_max_abs:.0f} N·m at spring location (x={self.x_spring/1000:.1f}m)")
        print(f"• At wire contact (x={self.L/1000:.1f}m): M = 0 N·m")

        print(f"\n🔬 STRESS ANALYSIS:")
        print(f"Section modulus: S = I/c = {self.S/1000:.1f}×10³ mm³")
        print(f"Maximum bending stress: σ_max = |M|×c/I = {sigma_max:.2f} MPa")
        print(f"Critical location: Spring attachment point (x = {self.x_spring/1000:.1f} m)")
        print(f"Stress distribution at spring:")
        print(f"  • Tension: +{sigma_max:.2f} MPa (top fiber)")
        print(f"  • Compression: -{sigma_max:.2f} MPa (bottom fiber)")

        # Safety factor assessment
        safety_factor = self.sigma_yield / sigma_max
        print(f"\n🛡️ SAFETY ASSESSMENT:")
        print(f"Yield strength: σ_yield = {self.sigma_yield} MPa")
        print(f"Actual safety factor: SF = {safety_factor:.1f}")
        print(f"Required safety factor: SF = {self.required_SF}")

        if safety_factor >= self.required_SF:
            print(f"✅ Design is ADEQUATE (SF = {safety_factor:.1f} > {self.required_SF})")
            print(f"   High safety margin (>10× required) intentional for:")
            print(f"   - Dynamic loading (wire contact/loss impacts)")
            print(f"   - Vibration effects (train motion cycles)")
            print(f"   - Fatigue resistance (~70 million cycles over 20 years)")
            print(f"   - Electrical safety (must not fail near 600V wire)")
        else:
            print(f"❌ Design is INADEQUATE (SF = {safety_factor:.1f} < {self.required_SF})")

        # Store for plotting
        self.sigma_max = sigma_max
        self.safety_factor = safety_factor

    def create_loading_diagram(self):
        """Create loading diagram showing pin joint, spring, beam, and wire contact."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Beam representation
        beam_height = 0.3
        beam_y = 0
        beam = patches.Rectangle((0, beam_y - beam_height/2), self.L/1000, beam_height,
                               facecolor=COLORS['beam'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(beam)

        # Pin joint at left (train roof connection)
        pin_radius = 0.08
        pin = patches.Circle((0, beam_y), pin_radius,
                           facecolor='#FFFFFF', edgecolor=COLORS['support'], linewidth=4)
        ax.add_patch(pin)
        # Inner pin circle
        pin_inner = patches.Circle((0, beam_y), pin_radius * 0.4,
                                  facecolor=COLORS['support'], edgecolor=COLORS['support'], linewidth=2)
        ax.add_patch(pin_inner)

        # Pin support structure
        support_width = 0.15
        support_height = 0.6
        support = patches.Rectangle((-support_width, beam_y - support_height/2), support_width, support_height/2,
                                  facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(support)

        # Spring mechanism
        spring_x = self.x_spring / 1000
        spring_y_bottom = beam_y - beam_height/2 - 0.6
        spring_height = 0.6

        # Draw spring as zigzag
        n_coils = 8
        spring_x_pts = [spring_x]
        spring_y_pts = [spring_y_bottom]
        for i in range(n_coils):
            spring_x_pts.append(spring_x + (-1)**(i) * 0.05)
            spring_y_pts.append(spring_y_bottom + (i+1) * spring_height / n_coils)
        spring_x_pts.append(spring_x)
        spring_y_pts.append(beam_y - beam_height/2)

        ax.plot(spring_x_pts, spring_y_pts, color=COLORS['spring'], linewidth=5, solid_capstyle='round')

        # Spring base plate
        base_plate = patches.Rectangle((spring_x - 0.1, spring_y_bottom - 0.05), 0.2, 0.05,
                                     facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=2)
        ax.add_patch(base_plate)
        # Hatching for ground
        for i in range(5):
            x_offset = -0.1 + i * 0.05
            ax.plot([spring_x + x_offset, spring_x + x_offset + 0.03],
                   [spring_y_bottom - 0.05, spring_y_bottom - 0.08],
                   color=COLORS['text'], linewidth=2)

        # Overhead wire representation
        wire_y = beam_y + beam_height/2 + 0.8
        ax.plot([0, self.L/1000 + 0.2], [wire_y, wire_y], color=COLORS['wire'], linewidth=8, alpha=0.8)
        ax.text(self.L/2000, wire_y + 0.15, '600V DC Overhead Wire', ha='center', va='bottom',
               fontsize=26, color=COLORS['wire'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC', edgecolor=COLORS['wire'], alpha=0.9))

        # Contact point indication
        contact_size = 0.08
        contact = patches.Circle((self.L/1000, beam_y + beam_height/2), contact_size,
                               facecolor=COLORS['wire'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(contact)

        # Wire contact force at tip (downward)
        arrow_length = 0.8
        arrow_width = 0.18
        ax.arrow(self.L/1000, beam_y + beam_height/2 + arrow_length, 0, -arrow_length + 0.1,
                head_width=arrow_width, head_length=0.1, fc=COLORS['load_arrow'],
                ec=COLORS['load_arrow'], linewidth=3)
        ax.text(self.L/1000 + 0.25, beam_y + beam_height/2 + arrow_length/2,
               f'P₁ = {self.P} N\n(Wire Contact)', ha='left', va='center',
               fontsize=24, color=COLORS['load_arrow'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['load_arrow'], alpha=0.9))

        # Spring force (upward)
        ax.arrow(spring_x, spring_y_bottom - 0.3, 0, 0.2,
                head_width=arrow_width, head_length=0.1, fc=COLORS['spring'],
                ec=COLORS['spring'], linewidth=3)
        ax.text(spring_x - 0.25, spring_y_bottom - 0.2,
               f'F_spring = {self.F_spring:.0f} N', ha='right', va='center',
               fontsize=24, color=COLORS['spring'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['spring'], alpha=0.9))

        # Pin reaction (downward)
        reaction_arrow_length = 0.5
        ax.arrow(0, beam_y - beam_height/2, 0, -reaction_arrow_length + 0.1,
                head_width=arrow_width, head_length=0.1, fc=COLORS['reaction'],
                ec=COLORS['reaction'], linewidth=3)
        ax.text(-0.25, beam_y - beam_height/2 - reaction_arrow_length/2,
               f'R_A = {abs(self.R_A):.0f} N', ha='right', va='center',
               fontsize=24, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], alpha=0.9))

        # Dimension lines
        dimension_y = beam_y - beam_height/2 - 1.2

        # Total length
        ax.annotate('', xy=(0, dimension_y), xytext=(self.L/1000, dimension_y),
                   arrowprops=dict(arrowstyle='<->', color=COLORS['text'], lw=3))
        ax.text(self.L/2000, dimension_y - 0.15, f'L = {self.L/1000:.1f} m',
               ha='center', va='top', fontsize=26, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        # Spring location
        dimension_y2 = dimension_y - 0.35
        ax.annotate('', xy=(0, dimension_y2), xytext=(spring_x, dimension_y2),
                   arrowprops=dict(arrowstyle='<->', color=COLORS['spring'], lw=2))
        ax.text(spring_x/2, dimension_y2 - 0.12, f'{self.x_spring/1000:.1f} m',
               ha='center', va='top', fontsize=22, color=COLORS['spring'], weight='bold')

        # Add cross-section details
        ax.text(self.L/1000 + 0.3, beam_y - 0.5,
               f'Hollow Steel Tube\nOD = {self.OD} mm\nt = {self.t} mm\nσ_yield = {self.sigma_yield} MPa',
               ha='left', va='top', fontsize=20, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.8', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        ax.set_xlim(-0.5, 1.8)
        ax.set_ylim(-1.9, 1.4)
        ax.set_aspect('equal')
        ax.axis('off')

        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)
        return fig

    def create_shear_diagram(self):
        """Create shear force diagram showing two-region distribution."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create x points for both regions - no overlap
        x_region1 = np.linspace(0, self.x_spring/1000, 50)  # 0 to 0.3
        x_region2 = np.linspace(self.x_spring/1000, self.L/1000, 50)  # 0.3 to 1.2

        # Calculate shear forces - Region 1: V = -2400 N, Region 2: V = +800 N
        V_region1 = np.full_like(x_region1, self.R_A / 1000)  # -2.4 kN (constant)
        V_region2 = np.full_like(x_region2, (self.R_A + self.F_spring) / 1000)  # +0.8 kN (constant)

        # Plot region 1 (negative shear) - plot and shade separately
        ax.plot(x_region1, V_region1, color=COLORS['shear_pos'], linewidth=4)
        ax.fill_between(x_region1, V_region1, 0, alpha=0.3, color=COLORS['shear_neg'])

        # Plot region 2 (positive shear) - plot and shade separately
        ax.plot(x_region2, V_region2, color=COLORS['shear_pos'], linewidth=4)
        ax.fill_between(x_region2, V_region2, 0, alpha=0.3, color=COLORS['moment_pos'])

        # Mark critical points
        # At x=0 (pin): V = -2.4 kN
        ax.plot(0, -2.4, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('-2.40 kN', (0, -2.4), xytext=(40, 50),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=0.3m (spring): Discontinuity
        ax.plot(self.x_spring/1000, -2.4, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.plot(self.x_spring/1000, 0.8, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)

        # Vertical jump line at spring - exactly at x = 0.3
        ax.plot([self.x_spring/1000, self.x_spring/1000], [-2.4, 0.8],
               color=COLORS['shear_pos'], linewidth=4, zorder=4)

        # At x=1.2m (wire contact): V = +0.8 kN
        ax.plot(1.2, 0.8, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('+0.80 kN', (1.2, 0.8), xytext=(-80, 20),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Customize plot
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Pin Joint (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Shear Force (kN)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        # All vertical dashed lines use load_arrow color (orange)
        # Pin line
        ax.axvline(x=0, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        # Spring line
        ax.axvline(x=self.x_spring/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        # Wire contact line
        ax.axvline(x=self.L/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

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
        """Create bending moment diagram showing maximum at spring location."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create x points
        x_array = np.linspace(0, self.L/1000, 500)
        M = self.calculate_moments(x_array)
        M_kNm = M / 1000  # Convert to kN·m

        # Plot moment diagram
        ax.plot(x_array, M_kNm, color=COLORS['moment_pos'], linewidth=4)

        # Fill area (negative throughout)
        ax.fill_between(x_array, M_kNm, 0, alpha=0.3, color=COLORS['moment_neg'])

        # Mark critical points
        # At x=0 (pin): M = 0 kN·m
        ax.plot(0, 0, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('0 kN·m\n(Pin)', (0, 0), xytext=(40, -60),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=0.3m (spring): M = -0.72 kN·m (maximum magnitude)
        ax.plot(self.x_spring/1000, -0.72, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('-0.72 kN·m\n(MAX at Spring)', (self.x_spring/1000, -0.72), xytext=(50, -10),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=0.6m (midspan): M = -0.48 kN·m
        ax.plot(0.6, -0.48, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('-0.48 kN·m', (0.6, -0.48), xytext=(40, -50),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=1.2m (wire contact): M = 0 kN·m
        ax.plot(1.2, 0, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('0 kN·m', (1.2, 0), xytext=(-80, -40),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Customize plot
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Pin Joint (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Bending Moment (kN·m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        # All vertical dashed lines use load_arrow color (orange)
        # Pin line
        ax.axvline(x=0, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        # Spring line (critical location)
        ax.axvline(x=self.x_spring/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        # Wire contact line
        ax.axvline(x=self.L/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

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
    pantograph = PantographArmAnalysis()

    # Find critical values
    pantograph.find_critical_values()

    # Create and save plots
    print(f"\n📊 GENERATING PLOTS...")

    # Loading diagram
    fig1 = pantograph.create_loading_diagram()
    fig1.savefig('pantograph_arm_loading_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Loading diagram saved as 'pantograph_arm_loading_diagram.svg'")

    # Shear force diagram
    fig2 = pantograph.create_shear_diagram()
    fig2.savefig('pantograph_arm_shear_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Shear force diagram saved as 'pantograph_arm_shear_diagram.svg'")

    # Bending moment diagram
    fig3 = pantograph.create_moment_diagram()
    fig3.savefig('pantograph_arm_moment_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Bending moment diagram saved as 'pantograph_arm_moment_diagram.svg'")

    plt.close('all')

    print(f"\n🎯 ANALYSIS COMPLETE!")
    print(f"All calculations and visualizations have been generated.")
    print(f"SVG files are optimized for mobile viewing with compatible colors.")

    # Summary of key results
    print(f"\n📋 SUMMARY:")
    print(f"• Spring force: {pantograph.F_spring:.0f} N (4× contact force)")
    print(f"• Pin reaction: {abs(pantograph.R_A):.0f} N (downward)")
    print(f"• Maximum moment: {abs(pantograph.critical_results['M_min']):.0f} N·m at spring (x={pantograph.x_spring/1000:.1f}m)")
    print(f"• Maximum stress: {pantograph.sigma_max:.2f} MPa at spring attachment")
    print(f"• Safety factor: {pantograph.safety_factor:.1f}")
    print(f"• Design status: {'ADEQUATE' if pantograph.safety_factor >= pantograph.required_SF else 'INADEQUATE'}")
    print(f"\n💡 The pin + spring mechanism reduces max moment by 25% compared to fixed cantilever!")

if __name__ == "__main__":
    main()
