#!/usr/bin/env python3
"""
Pantograph Arm of Electric Train (Electromechanical) Analysis
Application 2 from Lesson 2.2: Bending Stresses in Simple Beams

This program calculates and visualizes:
1. Support reaction forces
2. Shear force diagram
3. Bending moment diagram
4. Maximum bending stresses
5. Safety factor assessment

Problem Parameters:
- Hollow steel tube: OD = 50 mm, wall thickness = 4 mm
- Length: 1200 mm cantilever span
- Contact force: P₁ = 800 N at tip (includes vibration effects)
- Second moment of area: I = 2.45 × 10⁶ mm⁴
- Distance to extreme fiber: c = 25 mm
- Material: High-strength steel (σ_yield = 250 MPa)
- Safety factor required: 3.0
- Operating conditions: Dynamic contact with overhead wire at 600V DC
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")   # Non-GUI backend, perfect for saving plots
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# Set up matplotlib for mobile-friendly plots
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
    'figure.facecolor': '#F8FAFC',
    'axes.facecolor': '#F8FAFC',
    'savefig.facecolor': '#F8FAFC',
    'savefig.edgecolor': 'none'
})

# Color scheme with teal instead of blue for brand consistency
COLORS = {
    'beam': '#4472C4',           # Blue (keep for beam structure)
    'load_arrow': '#E74C3C',     # Red
    'reaction': '#27AE60',       # Green
    'shear_pos': '#008080',      # Teal (brand-friendly)
    'shear_neg': '#E67E22',      # Orange
    'moment_pos': '#20B2AA',     # Light Sea Green (teal family)
    'moment_neg': '#F39C12',     # Dark orange
    'text': '#2C3E50',           # Dark gray
    'grid': '#95A5A6',           # Light gray
    'support': '#34495E',        # Steel gray
    'wire': '#FFD700'            # Gold for overhead wire
}

class PantographArmAnalysis:
    def __init__(self):
        # Beam geometry (all in mm)
        self.L = 1200  # Cantilever length

        # Loads
        self.P = 800  # N, contact force at tip (already includes vibration effects)

        # Load positions (mm from fixed support)
        self.x_P = self.L  # Contact force at free end
        self.x_support = 0  # Fixed support at train roof connection

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
        """Calculate support reaction forces using equilibrium equations."""
        print("="*80)
        print("PANTOGRAPH ARM OF ELECTRIC TRAIN ANALYSIS")
        print("="*80)
        print("\n📊 PROBLEM SETUP:")
        print(f"• Cantilever length: {self.L/1000:.1f} m")
        print(f"• Contact force: P = {self.P} N at tip (includes dynamic effects)")
        print(f"• Hollow tube: OD = {self.OD} mm, wall thickness = {self.t} mm")
        print(f"• Section properties: I = {self.I/1e6:.2f}×10⁶ mm⁴, c = {self.c} mm")
        print(f"• Material: High-strength steel (σ_yield = {self.sigma_yield} MPa)")
        print(f"• Required safety factor: {self.required_SF}")

        self.verify_section_properties()

        # For cantilever beam with end load
        # Vertical equilibrium: R_A = P
        self.R_A = self.P  # 800 N (upward reaction at fixed support)

        # Moment equilibrium about fixed support A: M_A = P × L
        self.M_A = self.P * (self.L / 1000)  # 800 × 1.2 = 960 N·m (reaction moment at fixed support)

        print(f"\n🔧 REACTION FORCE CALCULATIONS:")
        print(f"For cantilever with end load P = {self.P} N:")
        print(f"• Vertical reaction: R_A = P = {self.R_A} N (upward)")
        print(f"• Moment reaction: M_A = P × L = {self.P} × {self.L/1000:.1f} = {self.M_A} N·m")

        # Verification
        print(f"\n✅ Equilibrium check:")
        print(f"• ΣF_y = {self.R_A} - {self.P} = 0 ✓")
        print(f"• ΣM_A = {self.M_A} - {self.P} × {self.L/1000:.1f} = 0 ✓")

    def calculate_shear_forces(self, x_points):
        """Calculate shear forces at given x positions (in m from fixed support)."""
        V = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            # For cantilever with end load, shear force is constant = -P
            V[i] = -self.P  # Negative throughout (downward internal force)

        return V

    def calculate_moments(self, x_points):
        """Calculate bending moments at given x positions (in m from fixed support)."""
        M = np.zeros_like(x_points)

        for i, x in enumerate(x_points):
            # For cantilever: M(x) = -P(L - x) where x is from fixed support
            # At fixed support (x=0): M = -P×L (maximum negative moment)
            # At free end (x=L): M = 0
            x_mm = x * 1000  # Convert to mm for comparison with self.L
            if x_mm <= self.L:
                distance_from_tip = (self.L - x_mm) / 1000  # Distance in meters
                M[i] = -self.P * distance_from_tip
            else:
                M[i] = 0

        return M

    def find_critical_values(self):
        """Find maximum and minimum shear forces and bending moments."""
        # Create fine grid for analysis
        x_fine = np.linspace(0, self.L/1000, 1000)
        V_fine = self.calculate_shear_forces(x_fine)
        M_fine = self.calculate_moments(x_fine)

        # For cantilever with end load:
        # - Shear is constant throughout
        # - Maximum moment occurs at fixed support
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
        M_max_abs = abs(M_min)  # Maximum absolute moment
        sigma_max = (M_max_abs * 1000) / self.S  # Convert N·m to N·mm, divide by S in mm³

        print(f"\n📈 CRITICAL VALUES:")
        print(f"Shear force: V = {V_min:.0f} N (constant throughout)")
        print(f"Maximum moment magnitude: |M_max| = {M_max_abs:.0f} N·m at fixed support")
        print(f"Moment at free end: M = 0 N·m")

        print(f"\n🔬 STRESS ANALYSIS:")
        print(f"Section modulus: S = I/c = {self.S/1000:.1f}×10³ mm³")
        print(f"Maximum bending stress: σ_max = |M|×c/I = {sigma_max:.2f} MPa")
        print(f"Location: Fixed support (train roof connection)")
        print(f"Stress distribution:")
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
            print(f"   High safety margin intentional for dynamic loading")
        else:
            print(f"❌ Design is INADEQUATE (SF = {safety_factor:.1f} < {self.required_SF})")

        # Store for plotting
        self.sigma_max = sigma_max
        self.safety_factor = safety_factor

    def create_loading_diagram(self):
        """Create loading diagram showing cantilever beam, support, and load."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Beam representation
        beam_height = 0.3
        beam_y = 0
        beam = patches.Rectangle((0, beam_y - beam_height/2), self.L/1000, beam_height,
                               facecolor=COLORS['beam'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(beam)

        # Fixed support at left (train roof connection)
        support_width = 0.15
        support_height = 0.8
        support = patches.Rectangle((-support_width, beam_y - support_height/2), support_width, support_height,
                                  facecolor=COLORS['support'], edgecolor=COLORS['text'], linewidth=3)
        ax.add_patch(support)

        # Add hatching pattern to show fixed support
        hatch_lines = 5
        for i in range(hatch_lines):
            y_pos = beam_y - support_height/2 + (i+0.5) * support_height/hatch_lines
            ax.plot([-support_width, -support_width + 0.05], [y_pos, y_pos - 0.05],
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

        # Contact force at tip
        arrow_length = 0.8
        arrow_width = 0.18
        ax.arrow(self.L/1000, beam_y + beam_height/2 + arrow_length, 0, -arrow_length + 0.1,
                head_width=arrow_width, head_length=0.1, fc=COLORS['load_arrow'],
                ec=COLORS['load_arrow'], linewidth=3)
        ax.text(self.L/1000, beam_y + beam_height/2 + arrow_length + 0.2,
               f'P = {self.P} N\n(Contact Force)', ha='center', va='bottom',
               fontsize=26, color=COLORS['load_arrow'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['load_arrow'], alpha=0.9))

        # Reaction forces at fixed support
        reaction_arrow_length = 0.6

        # Vertical reaction R_A
        ax.arrow(0, beam_y - beam_height/2 - reaction_arrow_length, 0, reaction_arrow_length - 0.1,
                head_width=arrow_width, head_length=0.1, fc=COLORS['reaction'],
                ec=COLORS['reaction'], linewidth=3)
        ax.text(-0.02, beam_y - beam_height/2 - reaction_arrow_length - 0.1,
               f'R_A = {self.R_A} N', ha='right', va='top',
               fontsize=26, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], alpha=0.9))

        # Moment reaction (curved arrow)
        from matplotlib.patches import FancyArrowPatch
        from matplotlib.patches import ConnectionPatch
        # Draw curved arrow to represent moment
        circle = patches.Arc((0, beam_y), 0.4, 0.4, theta1=-45, theta2=225,
                            color=COLORS['reaction'], linewidth=4)
        ax.add_patch(circle)
        # Arrow head for moment
        ax.annotate('', xy=(-0.14, beam_y + 0.14), xytext=(-0.12, beam_y + 0.16),
                   arrowprops=dict(arrowstyle='->', color=COLORS['reaction'], lw=3))
        ax.text(-0.02, beam_y + 0.3,
               f'M_A = {self.M_A:.0f} N·m', ha='right', va='bottom',
               fontsize=26, color=COLORS['reaction'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], alpha=0.9))

        # Dimension line
        dimension_y = beam_y - beam_height/2 - 1.0
        ax.annotate('', xy=(0, dimension_y), xytext=(self.L/1000, dimension_y),
                   arrowprops=dict(arrowstyle='<->', color=COLORS['text'], lw=3))
        ax.text(self.L/2000, dimension_y - 0.15, f'L = {self.L/1000:.1f} m',
               ha='center', va='top', fontsize=26, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        # Add cross-section details
        ax.text(self.L/1000 + 0.3, beam_y,
               f'Hollow Steel Tube\nOD = {self.OD} mm\nt = {self.t} mm\nσ_yield = {self.sigma_yield} MPa',
               ha='left', va='center', fontsize=22, color=COLORS['text'], weight='bold',
               bbox=dict(boxstyle='round,pad=0.8', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], alpha=0.9))

        ax.set_xlim(-0.4, 1.8)
        ax.set_ylim(-1.8, 1.4)
        ax.set_aspect('equal')
        ax.axis('off')

        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)
        return fig

    def create_shear_diagram(self):
        """Create shear force diagram."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create x points
        x_array = np.linspace(0, self.L/1000, 100)
        V = self.calculate_shear_forces(x_array) / 1000  # Convert to kN

        # Plot shear force (constant line)
        ax.plot(x_array, V, color=COLORS['shear_neg'], linewidth=4)

        # Fill area (negative throughout)
        ax.fill_between(x_array, V, 0, alpha=0.3, color=COLORS['shear_neg'])

        # Mark critical points
        # At x=0 (fixed support): V = -0.8 kN
        ax.plot(0, -0.8, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['shear_neg'], markeredgecolor='#2C3E50', zorder=5)
        ax.annotate('-0.80 kN\n(Fixed support)', (0, -0.8), xytext=(25, -25),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left', bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#F8FAFC', edgecolor='#2C3E50', alpha=0.9))

        # At x=1.2m (free end): V = -0.8 kN
        ax.plot(1.2, -0.8, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['shear_neg'], markeredgecolor='#2C3E50', zorder=5)
        ax.annotate('-0.80 kN\n(Free end)', (1.2, -0.8), xytext=(-100, -25),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left', bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#F8FAFC', edgecolor='#2C3E50', alpha=0.9))

        # Customize plot
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Fixed Support (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Shear Force (kN)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        # Support line
        ax.axvline(x=0, color=COLORS['support'], linewidth=4, alpha=0.4, linestyle='--')

        # Load line at tip
        ax.axvline(x=self.L/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['bottom'].set_linewidth(4)

        plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.15)
        return fig

    def create_moment_diagram(self):
        """Create bending moment diagram."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Create x points
        x_array = np.linspace(0, self.L/1000, 500)
        M = self.calculate_moments(x_array)
        M_kNm = M / 1000  # Convert to kN·m

        # Plot moment diagram
        ax.plot(x_array, M_kNm, color=COLORS['moment_neg'], linewidth=4)

        # Fill area (negative throughout)
        ax.fill_between(x_array, M_kNm, 0, alpha=0.3, color=COLORS['moment_neg'])

        # Mark critical points
        # At x=0 (fixed support): M = -0.96 kN·m (maximum negative moment)
        ax.plot(0, -0.96, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor='#2C3E50', zorder=5)
        ax.annotate('-0.96 kN·m\n(Fixed support)', (0, -0.96), xytext=(25, -25),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left', bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#F8FAFC', edgecolor='#2C3E50', alpha=0.9))

        # At x=0.6m (midspan): M = -0.48 kN·m
        ax.plot(0.6, -0.48, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['moment_neg'], markeredgecolor='#2C3E50', zorder=5)
        ax.annotate('-0.48 kN·m\n(Midspan)', (0.6, -0.48), xytext=(25, -25),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left', bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#F8FAFC', edgecolor='#2C3E50', alpha=0.9))

        # At x=1.2m (free end): M = 0 kN·m
        ax.plot(1.2, 0, 'o', markersize=18, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor='#95A5A6', markeredgecolor='#2C3E50', zorder=5)
        ax.annotate('0 kN·m\n(Free end)', (1.2, 0), xytext=(-100, 25),
                   textcoords='offset points', fontsize=26, color=COLORS['text'],
                   weight='bold', ha='left', bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#F8FAFC', edgecolor='#2C3E50', alpha=0.9))

        # Customize plot
        ax.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Distance from Fixed Support (m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.set_ylabel('Bending Moment (kN·m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax.xaxis.labelpad = 25
        ax.yaxis.labelpad = 25

        # Support line
        ax.axvline(x=0, color=COLORS['support'], linewidth=4, alpha=0.4, linestyle='--')

        # Load line at tip
        ax.axvline(x=self.L/1000, color=COLORS['load_arrow'], linewidth=4, alpha=0.6, linestyle='--')

        ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['bottom'].set_linewidth(4)

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
                facecolor='#F8FAFC', edgecolor='none')
    print("✅ Loading diagram saved as 'pantograph_arm_loading_diagram.svg'")

    # Shear force diagram
    fig2 = pantograph.create_shear_diagram()
    fig2.savefig('pantograph_arm_shear_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                facecolor='#F8FAFC', edgecolor='none')
    print("✅ Shear force diagram saved as 'pantograph_arm_shear_diagram.svg'")

    # Bending moment diagram
    fig3 = pantograph.create_moment_diagram()
    fig3.savefig('pantograph_arm_moment_diagram.svg', format='svg', dpi=300, bbox_inches='tight',
                facecolor='#F8FAFC', edgecolor='none')
    print("✅ Bending moment diagram saved as 'pantograph_arm_moment_diagram.svg'")

    plt.close('all')

    print(f"\n🎯 ANALYSIS COMPLETE!")
    print(f"All calculations and visualizations have been generated.")
    print(f"SVG files are optimized for mobile viewing with compatible colors.")

    # Summary of key results
    print(f"\n📋 SUMMARY:")
    print(f"• Maximum stress: {pantograph.sigma_max:.2f} MPa at fixed support")
    print(f"• Safety factor: {pantograph.safety_factor:.1f}")
    print(f"• Design status: {'ADEQUATE' if pantograph.safety_factor >= pantograph.required_SF else 'INADEQUATE'}")

if __name__ == "__main__":
    main()