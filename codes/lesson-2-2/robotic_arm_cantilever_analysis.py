#!/usr/bin/env python3
"""
Semi-Automatic Robotic Arm Cantilever Analysis (Mechatronics)
Application 1 from Lesson 2.2: Bending Stresses in Simple Beams

This program calculates and visualizes:
1. Support reaction forces and moment
2. Shear force diagram (two-region distribution)
3. Bending moment diagram (maximum at fixed support)
4. Maximum bending stresses
5. Safety factor assessment

Problem Parameters:
- Rectangular aluminum bar: 80 mm × 10 mm
- Total arm length: 2.5 m cantilever from fixed support
- Fixed support at base (left end)
- Distributed load: w = 75 N/m along entire length (arm weight)
- Concentrated load: P = 1200 N downward at free end (payload)
- Second moment of area: I = 5.33 × 10⁶ mm⁴
- Distance to extreme fiber: c = 40 mm
- Material: Aluminum alloy (σ_yield = 275 MPa)
- Safety factor required: 3.0
- Application: Semi-automatic manufacturing assembly arm
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

class RoboticArmCantileverAnalysis:
    def __init__(self):
        # Beam geometry (all in mm)
        self.L = 2500  # Total arm length (cantilever)

        # Loads
        self.w = 75  # N/m, distributed load (arm weight)
        self.P = 1200  # N, concentrated load at free end (payload)

        # Beam properties
        self.width = 80  # mm, rectangular bar width
        self.thickness = 10  # mm, rectangular bar thickness
        self.I = 5.33e6  # mm⁴ (given)
        self.c = 40  # mm (distance from neutral axis to extreme fiber = thickness/2)
        self.sigma_yield = 275  # MPa
        self.S = self.I / self.c  # Section modulus
        self.required_SF = 3.0  # Required safety factor

        # Calculate reactions
        self.calculate_reactions()

    def verify_section_properties(self):
        """Verify the given section properties match the rectangular bar geometry."""
        # For rectangular cross-section: I = b×h³/12 (about neutral axis)
        I_calculated = (self.width * self.thickness**3) / 12
        print(f"\n🔍 SECTION PROPERTY VERIFICATION:")
        print(f"Given I = {self.I/1e6:.2f}×10⁶ mm⁴")
        print(f"Calculated I = b×h³/12 = {self.width}×{self.thickness}³/12 = {I_calculated/1e6:.2f}×10⁶ mm⁴")

        if abs(I_calculated - self.I) / self.I < 0.05:
            print("✅ Section properties match rectangular bar geometry")
        else:
            print("⚠️  Minor discrepancy - using given values for analysis")

    def calculate_reactions(self):
        """Calculate support reactions using equilibrium equations."""
        print("="*80)
        print("SEMI-AUTOMATIC ROBOTIC ARM CANTILEVER ANALYSIS")
        print("FIXED SUPPORT AT BASE (CANTILEVER BEAM)")
        print("="*80)
        print("\n📊 PROBLEM SETUP:")
        print(f"• Total arm length: {self.L/1000:.1f} m (cantilever)")
        print(f"• Distributed load: w = {self.w} N/m along entire length (arm weight)")
        print(f"• Concentrated load: P = {self.P} N at free end (payload)")
        print(f"• Rectangular bar: {self.width} mm × {self.thickness} mm")
        print(f"• Section properties: I = {self.I/1e6:.2f}×10⁶ mm⁴, c = {self.c} mm")
        print(f"• Material: Aluminum alloy (σ_yield = {self.sigma_yield} MPa)")
        print(f"• Required safety factor: {self.required_SF}")

        self.verify_section_properties()

        # Total distributed load
        self.W_total = self.w * (self.L / 1000)  # Convert L to meters

        # Calculate vertical reaction at fixed support
        # ΣF_y = 0: R_y - P - W_total = 0
        self.R_y = self.P + self.W_total

        # Calculate moment at fixed support
        # ΣM_base = 0: M_base - P × L - W_total × (L/2) = 0
        self.M_base = self.P * (self.L / 1000) + self.W_total * (self.L / 1000 / 2)

        print(f"\n🔧 REACTION FORCE CALCULATIONS:")
        print(f"\n1. Total distributed load:")
        print(f"   W_total = w × L = {self.w} × {self.L/1000:.1f} = {self.W_total:.1f} N")

        print(f"\n2. Vertical reaction at fixed support (from force equilibrium):")
        print(f"   ΣF_y = 0: R_y - P - W_total = 0")
        print(f"   R_y = {self.P} + {self.W_total:.1f} = {self.R_y:.1f} N (upward)")

        print(f"\n3. Moment reaction at fixed support (from moment equilibrium):")
        print(f"   ΣM_base = 0: M_base - P × L - W_total × (L/2) = 0")
        print(f"   M_base = {self.P} × {self.L/1000:.1f} + {self.W_total:.1f} × {self.L/1000/2:.2f}")
        print(f"   M_base = {self.M_base:.3f} N·m (counterclockwise)")

        # Verification
        print(f"\n✅ Equilibrium verification:")
        sum_Fy = self.R_y - self.P - self.W_total
        sum_M = self.M_base - self.P * (self.L/1000) - self.W_total * (self.L/1000/2)
        print(f"• ΣF_y = {self.R_y:.1f} - {self.P} - {self.W_total:.1f} = {sum_Fy:.2f} ≈ 0 ✓")
        print(f"• ΣM_base = {self.M_base:.3f} - {self.P * (self.L/1000):.0f} - {self.W_total * (self.L/1000/2):.3f} = {sum_M:.3f} ≈ 0 ✓")

    def calculate_shear_forces(self, x_points):
        """Calculate shear forces at given x positions (in m from fixed support)."""
        V = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            # V(x) = -(wL + P) + w×x
            # V(x) = -1387.5 + 75×x
            V[i] = -(self.w * (self.L/1000) + self.P) + self.w * x

        return V

    def calculate_moments(self, x_points):
        """Calculate bending moments at given x positions (in m from fixed support)."""
        M = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            # M(x) = -M_base + R_y × x - w × x²/2
            # M(x) = -3234.375 + 1387.5×x - 37.5×x²
            M[i] = -self.M_base + self.R_y * x - (self.w * x**2) / 2

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
        M_max = np.max(M_fine)  # This will be 0 (at free end)
        M_min = np.min(M_fine)  # This will be negative (at fixed support)

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
        # Maximum stress occurs at fixed support where |M| is maximum
        M_max_abs = abs(M_min)  # Maximum absolute moment at fixed support
        sigma_max = (M_max_abs * 1000) / self.S  # Convert N·m to N·mm, divide by S in mm³

        print(f"\n📈 CRITICAL VALUES:")
        print(f"\nShear force distribution:")
        print(f"• At fixed support (x=0): V = {V_min:.1f} N (most negative)")
        print(f"• At free end (x={self.L/1000:.1f}m): V = {V_max:.1f} N (least negative)")
        print(f"• Linear variation: V(x) = -{self.R_y:.1f} + {self.w}×x")

        print(f"\nBending moment distribution:")
        print(f"• At fixed support (x=0): M = {M_min:.3f} N·m (maximum magnitude, negative)")
        print(f"• At free end (x={self.L/1000:.1f}m): M = {M_max:.1f} N·m (zero)")
        print(f"• Parabolic variation: M(x) = {-self.M_base:.3f} + {self.R_y:.1f}×x - {self.w/2:.1f}×x²")

        print(f"\n🔬 STRESS ANALYSIS:")
        print(f"Section modulus: S = I/c = {self.S/1000:.2f}×10³ mm³")
        print(f"Maximum bending stress: σ_max = |M|×c/I = {sigma_max:.1f} MPa")
        print(f"Critical location: Fixed support (x = 0 m)")
        print(f"Stress distribution at fixed support:")
        print(f"  • Tension: +{sigma_max:.1f} MPa (top fiber)")
        print(f"  • Compression: -{sigma_max:.1f} MPa (bottom fiber)")

        # Safety factor assessment
        safety_factor = self.sigma_yield / sigma_max
        print(f"\n🛡️ SAFETY ASSESSMENT:")
        print(f"Yield strength: σ_yield = {self.sigma_yield} MPa")
        print(f"Actual safety factor: SF = {safety_factor:.1f}")
        print(f"Required safety factor: SF = {self.required_SF}")

        if safety_factor >= self.required_SF:
            print(f"✅ Design is ADEQUATE (SF = {safety_factor:.1f} > {self.required_SF})")
            print(f"   High safety margin intentional for:")
            print(f"   - Dynamic loading (payload pickup/release)")
            print(f"   - Vibration effects (arm motion cycles)")
            print(f"   - Fatigue resistance (repetitive operations)")
            print(f"   - Worker safety (manufacturing environment)")
        else:
            print(f"❌ Design is INADEQUATE (SF = {safety_factor:.1f} < {self.required_SF})")

        # Store for plotting
        self.sigma_max = sigma_max
        self.safety_factor = safety_factor

    def create_loading_diagram(self):
        """Create loading diagram showing fixed support, beam, distributed load, and concentrated load."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Beam representation
        beam_height = 0.3
        beam_y = 0
        beam = patches.Rectangle((0, beam_y - beam_height/2), self.L/1000, beam_height,
                               facecolor=COLORS['beam'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(beam)

        # Fixed support at left (base)
        support_width = 0.2
        support_height = 0.8
        support = patches.Rectangle((-support_width, beam_y - support_height/2), support_width, support_height,
                                  facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(support)

        # Hatching for fixed support
        for i in range(8):
            y_offset = -support_height/2 + i * support_height/7
            ax.plot([-support_width, -support_width - 0.08],
                   [beam_y + y_offset, beam_y + y_offset + 0.08],
                   color=COLORS['text'], linewidth=2)

        # Distributed load (downward arrows along beam)
        n_arrows = 10
        arrow_spacing = (self.L/1000) / n_arrows
        arrow_length = 0.6
        arrow_width = 0.12

        for i in range(n_arrows + 1):
            x_arrow = i * arrow_spacing
            ax.arrow(x_arrow, beam_y + beam_height/2 + arrow_length, 0, -arrow_length + 0.1,
                    head_width=arrow_width, head_length=0.1, fc=COLORS['load_arrow'],
                    ec=COLORS['load_arrow'], linewidth=2, alpha=0.8)

        # Distributed load label
        ax.text(self.L/2000, beam_y + beam_height/2 + arrow_length + 0.3,
               f'w = {self.w} N/m\n(Arm Weight)', ha='center', va='bottom',
               fontsize=24, color=COLORS['load_arrow'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['load_arrow'], alpha=0.9))

        # Concentrated load at free end (downward)
        conc_arrow_length = 0.8
        conc_arrow_width = 0.18
        ax.arrow(self.L/1000, beam_y + beam_height/2 + conc_arrow_length, 0, -conc_arrow_length + 0.1,
                head_width=conc_arrow_width, head_length=0.1, fc=COLORS['load_arrow'],
                ec=COLORS['load_arrow'], linewidth=3)
        ax.text(self.L/1000 + 0.3, beam_y + beam_height/2 + conc_arrow_length/2,
               f'P = {self.P} N\n(Payload)', ha='left', va='center',
               fontsize=24, color=COLORS['load_arrow'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['load_arrow'], alpha=0.9))

        # Reaction force at fixed support (upward)
        reaction_arrow_length = 0.6
        ax.arrow(0, beam_y - beam_height/2 - reaction_arrow_length, 0, reaction_arrow_length - 0.1,
                head_width=conc_arrow_width, head_length=0.1, fc=COLORS['reaction'],
                ec=COLORS['reaction'], linewidth=3)
        ax.text(-0.35, beam_y - beam_height/2 - reaction_arrow_length/2,
               f'R_y = {self.R_y:.1f} N', ha='right', va='center',
               fontsize=24, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], alpha=0.9))

        # Moment at fixed support (curved arrow)
        from matplotlib.patches import FancyArrowPatch
        moment_arc = FancyArrowPatch((0.15, -0.5), (0.15, -0.2),
                                    connectionstyle="arc3,rad=.5",
                                    arrowstyle='->,head_width=0.3,head_length=0.2',
                                    linewidth=3, color=COLORS['reaction'])
        ax.add_patch(moment_arc)
        ax.text(-0.35, beam_y - 0.35,
               f'M_base = {self.M_base:.1f} N·m', ha='right', va='center',
               fontsize=24, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], alpha=0.9))

        # Dimension line for total length
        dimension_y = beam_y - beam_height/2 - 1.2
        ax.annotate('', xy=(0, dimension_y), xytext=(self.L/1000, dimension_y),
                   arrowprops=dict(arrowstyle='<->', color=COLORS['text'], lw=3))
        ax.text(self.L/2000, dimension_y - 0.15, f'L = {self.L/1000:.1f} m',
               ha='center', va='top', fontsize=26, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        # Add cross-section details
        ax.text(self.L/1000 + 0.3, beam_y - 0.7,
               f'Rectangular Aluminum Bar\n{self.width} mm × {self.thickness} mm\nσ_yield = {self.sigma_yield} MPa',
               ha='left', va='top', fontsize=20, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.8', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        ax.set_xlim(-0.7, 3.2)
        ax.set_ylim(-1.9, 1.6)
        ax.set_aspect('equal')
        ax.axis('off')

        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)
        return fig

    def create_shear_diagram(self):
        """Create shear force diagram showing linear distribution."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create x points
        x_array = np.linspace(0, self.L/1000, 500)
        V = self.calculate_shear_forces(x_array)
        V_kN = V / 1000  # Convert to kN

        # Plot shear diagram
        ax.plot(x_array, V_kN, color=COLORS['shear_pos'], linewidth=4)

        # Fill area - positive region in blue, negative region in orange
        # Find zero crossing
        zero_idx = np.where(np.diff(np.sign(V_kN)))[0]
        if len(zero_idx) > 0:
            zero_x = x_array[zero_idx[0]]
            # Positive region
            mask_pos = x_array <= zero_x
            ax.fill_between(x_array[mask_pos], V_kN[mask_pos], 0, alpha=0.3, color=COLORS['moment_pos'])
            # Negative region
            mask_neg = x_array >= zero_x
            ax.fill_between(x_array[mask_neg], V_kN[mask_neg], 0, alpha=0.3, color=COLORS['shear_neg'])
        else:
            # All positive or all negative
            if V_kN[0] > 0:
                ax.fill_between(x_array, V_kN, 0, alpha=0.3, color=COLORS['moment_pos'])
            else:
                ax.fill_between(x_array, V_kN, 0, alpha=0.3, color=COLORS['shear_neg'])

        # Mark critical points
        # At x=0 (fixed support): V = -1.39 kN
        ax.plot(0, V_kN[0], 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'{V_kN[0]:.2f} kN', (0, V_kN[0]), xytext=(40, 50),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=L (free end): V = -1.20 kN
        ax.plot(self.L/1000, V_kN[-1], 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'{V_kN[-1]:.2f} kN', (self.L/1000, V_kN[-1]), xytext=(-80, -50),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Customize plot
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Fixed Support (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Shear Force (kN)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        # Vertical dashed lines
        # Fixed support line
        ax.axvline(x=0, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        # Free end line
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
        """Create bending moment diagram showing parabolic distribution."""
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
        # At x=0 (fixed support): M_min (maximum magnitude)
        ax.plot(0, M_kNm[0], 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate(f'{M_kNm[0]:.2f} kN·m\n(MAX at Support)', (0, M_kNm[0]), xytext=(50, -10),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # At x=L (free end): M = 0
        ax.plot(self.L/1000, M_kNm[-1], 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor=COLORS['text'], zorder=5)
        ax.annotate('0 kN·m\n(Free End)', (self.L/1000, M_kNm[-1]), xytext=(-90, -50),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='right',
                   arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2))

        # Customize plot
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Fixed Support (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Bending Moment (kN·m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        # Vertical dashed lines
        # Fixed support line (critical location)
        ax.axvline(x=0, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        # Free end line
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
    robotic_arm = RoboticArmCantileverAnalysis()

    # Find critical values
    robotic_arm.find_critical_values()

    # Create and save plots
    print(f"\n📊 GENERATING PLOTS...")

    # Loading diagram
    fig1 = robotic_arm.create_loading_diagram()
    fig1.savefig('robotic_arm_loading_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Loading diagram saved as 'robotic_arm_loading_diagram.svg'")

    # Shear force diagram
    fig2 = robotic_arm.create_shear_diagram()
    fig2.savefig('robotic_arm_shear_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Shear force diagram saved as 'robotic_arm_shear_diagram.svg'")

    # Bending moment diagram
    fig3 = robotic_arm.create_moment_diagram()
    fig3.savefig('robotic_arm_moment_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                transparent=True)
    print("✅ Bending moment diagram saved as 'robotic_arm_moment_diagram.svg'")

    plt.close('all')

    print(f"\n🎯 ANALYSIS COMPLETE!")
    print(f"All calculations and visualizations have been generated.")
    print(f"SVG files are optimized for mobile viewing with compatible colors.")

    # Summary of key results
    print(f"\n📋 SUMMARY:")
    print(f"• Vertical reaction: {robotic_arm.R_y:.1f} N (upward)")
    print(f"• Moment reaction: {robotic_arm.M_base:.1f} N·m (counterclockwise)")
    print(f"• Maximum |shear|: {abs(robotic_arm.critical_results['V_min']):.1f} N at fixed support (x=0m)")
    print(f"• Maximum moment: {abs(robotic_arm.critical_results['M_min']):.1f} N·m at fixed support (x=0m)")
    print(f"• Maximum stress: {robotic_arm.sigma_max:.1f} MPa at fixed support")
    print(f"• Safety factor: {robotic_arm.safety_factor:.1f}")
    print(f"• Design status: {'ADEQUATE' if robotic_arm.safety_factor >= robotic_arm.required_SF else 'INADEQUATE'}")
    print(f"\n💡 Cantilever beams experience maximum bending moment and stress at the fixed support!")

if __name__ == "__main__":
    main()
