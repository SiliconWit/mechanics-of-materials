#!/usr/bin/env python3
"""
Lab 1: Robotic Arm Cantilever Beam Analysis
Structural Analysis Laboratory - Shear Force and Bending Moment

This script provides a complete example solution for Lab 1, demonstrating:
1. Analytical calculations for cantilever beam
2. Shear force and bending moment diagrams
3. Maximum stress calculations
4. Safety factor analysis
5. Professional visualization

Problem: 6-DOF industrial robot forearm segment
- Cantilever beam: L = 500 mm
- Cross-section: Rectangular 60 mm × 20 mm
- Material: Aluminum alloy 6061-T6
- Load: P = 500 N at free end (gripper + payload)
- Fixed support at x = 0 (elbow joint)

Author: SiliconWit Mechanics of Materials Laboratory
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrow, Circle, Polygon, FancyBboxPatch
import os

# Get script directory for output
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Color scheme matching reference files
COLORS = {
    'beam': '#2d7a8f',           # Darker teal
    'support': '#6B7280',        # Gray for supports
    'ground': '#5ab9a0',         # Light teal for ground
    'force': '#ff8c36',          # Orange for applied forces
    'load_arrow': '#ff8c36',     # Orange for load arrows (same as force)
    'reaction': '#00a0d0',       # Light blue for reactions
    'text': '#405ab9',           # Blue for text
    'shear_pos': '#405ab9',      # Blue for positive shear
    'shear_neg': '#ff8c36',      # Orange for negative shear
    'moment_pos': '#405ab9',     # Blue for positive moment
    'moment_neg': '#ff8c36',     # Orange for negative moment
    'grid': '#9ea388',           # Gray-green for grid
    'bg': '#F8FAFC'              # Light gray background
}

# Matplotlib settings for professional plots
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 28,
    'font.weight': 'bold',
    'axes.titlesize': 32,
    'axes.labelsize': 30,
    'xtick.labelsize': 26,
    'ytick.labelsize': 26,
    'legend.fontsize': 26,
    'lines.linewidth': 5,
    'axes.linewidth': 4,
    'figure.facecolor': 'none',
    'axes.facecolor': 'none',
    'savefig.facecolor': 'none',
    'savefig.edgecolor': 'none'
})


class RoboticArmAnalysis:
    """Complete analysis for robotic arm cantilever beam."""

    def __init__(self):
        """Initialize problem parameters."""
        # Geometry (all in mm)
        self.L = 500.0              # Beam length
        self.b = 60.0               # Width
        self.h = 20.0               # Height

        # Loading (in N)
        self.P = 500.0              # Point load at free end

        # Material properties
        self.sigma_yield = 275.0    # MPa (Aluminum 6061-T6)
        self.E = 69000.0            # MPa (Young's modulus)

        # Section properties
        self.I = (self.b * self.h**3) / 12  # Moment of inertia (mm⁴)
        self.c = self.h / 2                  # Distance to outer fiber (mm)
        self.S = self.I / self.c             # Section modulus (mm³)

        print("="*80)
        print("LAB 1: ROBOTIC ARM CANTILEVER BEAM ANALYSIS")
        print("="*80)
        print("\n📋 PROBLEM PARAMETERS:")
        print(f"• Beam length: L = {self.L} mm")
        print(f"• Cross-section: {self.b} mm × {self.h} mm (rectangular)")
        print(f"• Point load: P = {self.P} N at free end")
        print(f"• Material: Aluminum 6061-T6")
        print(f"• Yield strength: σ_yield = {self.sigma_yield} MPa")
        print(f"• Young's modulus: E = {self.E} MPa")

        print(f"\n📐 SECTION PROPERTIES:")
        print(f"• Moment of inertia: I = bh³/12 = {self.b}×{self.h}³/12 = {self.I:.2e} mm⁴")
        print(f"• Distance to outer fiber: c = h/2 = {self.c} mm")
        print(f"• Section modulus: S = I/c = {self.S:.2e} mm³")

    def calculate_reactions(self):
        """Calculate reaction forces and moments at fixed support."""
        print("\n🔧 REACTION FORCE CALCULATIONS:")

        # Vertical force equilibrium
        self.R_y = self.P
        print(f"\n1. Vertical force equilibrium (↑ positive):")
        print(f"   ΣF_y = 0: R_y - P = 0")
        print(f"   R_y = {self.P} N (upward)")

        # Moment equilibrium about fixed support
        self.M_A = self.P * self.L
        print(f"\n2. Moment equilibrium about A (⟲ positive):")
        print(f"   ΣM_A = 0: M_A - P × L = 0")
        print(f"   M_A = {self.P} × {self.L} = {self.M_A:.0f} N·mm = {self.M_A/1000:.2f} N·m")
        print(f"   Direction: Counterclockwise (resists clockwise moment from load)")

        # Verification
        print(f"\n✅ Equilibrium verification:")
        print(f"• ΣF_y = {self.R_y} - {self.P} = 0 ✓")
        print(f"• ΣM_A = {self.M_A:.0f} - {self.P}×{self.L} = 0 ✓")

    def shear_force_function(self, x):
        """
        Calculate shear force at position x (mm from fixed end).

        For cantilever with end load:
        V(x) = -P for 0 ≤ x < L
        V(x) = 0 at x = L (after load)
        """
        V = np.where(x < self.L, -self.P, 0)
        return V

    def bending_moment_function(self, x):
        """
        Calculate bending moment at position x (mm from fixed end).

        For cantilever with end load:
        M(x) = -P × (L - x)

        Note: Negative sign indicates tension on top fiber
        """
        M = -self.P * (self.L - x)
        return M

    def calculate_critical_values(self):
        """Find maximum shear force and bending moment."""
        print("\n📈 CRITICAL VALUES:")

        # Shear force analysis
        print("\n1. Shear Force Distribution:")
        print(f"   V(x) = -P = -{self.P} N for 0 ≤ x < {self.L} mm")
        print(f"   V(x) = 0 N at x = {self.L} mm (free end, after load)")
        print(f"   |V_max| = {abs(-self.P)} N (constant throughout beam)")

        # Bending moment analysis
        print("\n2. Bending Moment Distribution:")
        print(f"   M(x) = -P(L - x) = -{self.P}({self.L} - x) N·mm")
        print(f"\n   At key points:")

        M_0 = self.bending_moment_function(0)
        M_250 = self.bending_moment_function(250)
        M_500 = self.bending_moment_function(500)

        print(f"   • x = 0 mm (fixed end): M = {M_0:.0f} N·mm = {M_0/1000:.2f} N·m ← MAXIMUM")
        print(f"   • x = 250 mm (midpoint): M = {M_250:.0f} N·mm = {M_250/1000:.2f} N·m")
        print(f"   • x = 500 mm (free end): M = {M_500:.0f} N·mm")

        self.V_max = abs(-self.P)
        self.M_max = abs(M_0)
        self.M_max_location = 0

        print(f"\n   |M_max| = {self.M_max:.0f} N·mm at x = {self.M_max_location} mm (fixed support)")

    def calculate_stresses(self):
        """Calculate maximum bending stress and safety factor."""
        print("\n🔬 STRESS ANALYSIS:")

        # Maximum bending stress using flexure formula
        self.sigma_max = (self.M_max * self.c) / self.I

        print(f"\n1. Maximum Bending Stress (Flexure Formula):")
        print(f"   σ_max = (M_max × c) / I")
        print(f"   σ_max = ({self.M_max:.0f} N·mm × {self.c} mm) / {self.I:.2e} mm⁴")
        print(f"   σ_max = {self.sigma_max:.2f} MPa")
        print(f"\n   Location: x = 0 mm (fixed support)")
        print(f"   Position in cross-section: Top and bottom fibers (±{self.c} mm from neutral axis)")
        print(f"   Top fiber: TENSION (+{self.sigma_max:.2f} MPa)")
        print(f"   Bottom fiber: COMPRESSION (-{self.sigma_max:.2f} MPa)")

        # Safety factor
        self.SF = self.sigma_yield / self.sigma_max

        print(f"\n2. Safety Factor:")
        print(f"   SF = σ_yield / σ_max")
        print(f"   SF = {self.sigma_yield} MPa / {self.sigma_max:.2f} MPa")
        print(f"   SF = {self.SF:.2f}")

        # Engineering assessment
        print(f"\n💡 ENGINEERING ASSESSMENT:")
        if self.SF >= 3.0 and self.SF <= 5.0:
            print(f"   ✅ Safety factor ({self.SF:.2f}) is EXCELLENT for robotic applications")
            print(f"   • Typical target for robotics: SF = 3-5")
            print(f"   • Accounts for: dynamic loads, impact, fatigue, reliability")
        elif self.SF > 5.0:
            print(f"   ⚠️  Safety factor ({self.SF:.2f}) is HIGH - consider weight reduction")
            print(f"   • Over-designed for static loading")
            print(f"   • Could reduce cross-section for mass savings")
        else:
            print(f"   ❌ Safety factor ({self.SF:.2f}) is TOO LOW for robotic applications")
            print(f"   • Increase cross-section or use stronger material")

    def create_loading_diagram(self):
        """Create loading diagram with supports, beam, and forces."""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Beam dimensions for visualization
        beam_start = 0.0
        beam_end = self.L / 100  # Scale to cm for better visualization
        beam_y = 0.0
        beam_height = 0.4

        # Draw beam
        beam = patches.Rectangle((beam_start, beam_y - beam_height/2),
                                beam_end - beam_start, beam_height,
                                fc=COLORS['beam'], ec=COLORS['ground'],
                                linewidth=4, alpha=0.8)
        ax.add_patch(beam)

        # Fixed support at left end
        wall_width = 0.6
        wall_height = 1.5
        wall = FancyBboxPatch(
            (beam_start - wall_width, beam_y - wall_height/2),
            wall_width, wall_height,
            boxstyle="round,pad=0.05",
            fc=COLORS['support'], ec=COLORS['ground'],
            linewidth=4, alpha=0.8
        )
        ax.add_patch(wall)

        # Hatching on wall
        for i in range(8):
            y_pos = (beam_y - wall_height/2) + i * 0.25
            ax.plot([beam_start - wall_width, beam_start - wall_width - 0.4],
                   [y_pos, y_pos - 0.2],
                   color=COLORS['ground'], linewidth=3)

        # Point load at free end
        arrow_length = 1.2
        arrow = FancyArrow(beam_end, beam_y + beam_height/2 + arrow_length,
                          0, -arrow_length + 0.15,
                          width=0.2, head_width=0.4, head_length=0.25,
                          fc=COLORS['force'], ec=COLORS['force'], linewidth=3)
        ax.add_patch(arrow)

        # Load label
        ax.text(beam_end + 0.8, beam_y + beam_height/2 + arrow_length/2,
               f'P = {self.P:.0f} N',
               fontsize=26, fontweight='bold', color=COLORS['force'],
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC',
                        edgecolor=COLORS['force'], linewidth=3, alpha=0.95))

        # Reaction force (upward)
        r_arrow = FancyArrow(beam_start, beam_y - beam_height/2 - 1.5,
                            0, 0.8,
                            width=0.2, head_width=0.4, head_length=0.25,
                            fc=COLORS['reaction'], ec=COLORS['reaction'], linewidth=3)
        ax.add_patch(r_arrow)

        ax.text(beam_start - 1.2, beam_y - beam_height/2 - 1.1,
               f'R_y = {self.R_y:.0f} N',
               fontsize=24, fontweight='bold', color=COLORS['reaction'],
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], linewidth=3, alpha=0.95))

        # Reaction moment (curved arrow representation)
        ax.text(beam_start - 1.2, beam_y + 0.8,
               f'M_A = {self.M_A/1000:.0f} N·m',
               fontsize=24, fontweight='bold', color=COLORS['reaction'],
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['reaction'], linewidth=3, alpha=0.95))

        # Length dimension
        dim_y = beam_y - beam_height/2 - 2.2
        ax.annotate('', xy=(beam_start, dim_y), xytext=(beam_end, dim_y),
                   arrowprops=dict(arrowstyle='<->', color=COLORS['text'], lw=4))
        ax.text((beam_start + beam_end)/2, dim_y - 0.4,
               f'L = {self.L:.0f} mm',
               ha='center', fontsize=26, fontweight='bold', color=COLORS['text'],
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], linewidth=3, alpha=0.95))

        # Cross-section info
        ax.text(beam_end + 1.5, beam_y - 1.0,
               f'Rectangular Section\n{self.b:.0f} mm × {self.h:.0f} mm\nAl 6061-T6',
               fontsize=20, fontweight='bold', color=COLORS['text'],
               bbox=dict(boxstyle='round,pad=0.7', facecolor='#F8FAFC',
                        edgecolor=COLORS['text'], linewidth=3, alpha=0.95))

        ax.set_xlim(-2.5, beam_end + 3.5)
        ax.set_ylim(-3.0, 2.5)
        ax.set_aspect('equal')
        ax.axis('off')

        plt.tight_layout()
        return fig

    def create_sfd_bmd_diagrams(self):
        """Create combined shear force and bending moment diagrams."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))

        # Create x array
        x_array = np.linspace(0, self.L, 200)

        # Calculate shear and moment
        V = self.shear_force_function(x_array)
        M = self.bending_moment_function(x_array)

        # --- Shear Force Diagram ---
        ax1.plot(x_array, V, color=COLORS['shear_neg'], linewidth=5)
        ax1.fill_between(x_array, 0, V, alpha=0.3, color=COLORS['shear_neg'])

        # Zero line
        ax1.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)

        # Mark critical points
        ax1.plot([0, self.L-1], [V[0], V[-2]], 'o', markersize=16,
                color='#FFFFFF', markeredgewidth=5,
                markerfacecolor=COLORS['moment_neg'],
                markeredgecolor=COLORS['text'], zorder=5)

        # Annotations
        ax1.annotate(f'V = {V[0]:.0f} N', (self.L/4, V[0]),
                    xytext=(0, -60), textcoords='offset points',
                    fontsize=24, color=COLORS['text'], weight='bold',
                    arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=3))

        ax1.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax1.set_xlabel('Position x (mm)', fontsize=30, color=COLORS['text'], weight='bold')
        ax1.set_ylabel('Shear Force V (N)', fontsize=30, color=COLORS['text'], weight='bold')
        ax1.set_title('Shear Force Diagram - Robotic Arm Cantilever',
                     fontsize=32, color=COLORS['text'], weight='bold', pad=20)

        # Vertical line at fixed support
        ax1.axvline(x=0, color=COLORS['load_arrow'], linewidth=4, alpha=0.5, linestyle='--')

        ax1.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_linewidth(4)
        ax1.spines['bottom'].set_linewidth(4)
        ax1.spines['left'].set_color(COLORS['text'])
        ax1.spines['bottom'].set_color(COLORS['text'])

        # --- Bending Moment Diagram ---
        ax2.plot(x_array, M/1000, color=COLORS['moment_neg'], linewidth=5)
        ax2.fill_between(x_array, 0, M/1000, alpha=0.3, color=COLORS['moment_neg'])

        # Zero line
        ax2.axhline(y=0, color=COLORS['text'], linewidth=4, alpha=0.8)

        # Mark critical points
        ax2.plot([0, self.L/2, self.L],
                [M[0]/1000, M[100]/1000, M[-1]/1000],
                'o', markersize=16, color='#FFFFFF', markeredgewidth=5,
                markerfacecolor=COLORS['moment_neg'],
                markeredgecolor=COLORS['text'], zorder=5)

        # Annotations
        ax2.annotate(f'M_max = {M[0]/1000:.2f} N·m\n(at fixed support)',
                    (0, M[0]/1000), xytext=(60, 20),
                    textcoords='offset points', fontsize=24,
                    color=COLORS['text'], weight='bold',
                    arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=3))

        ax2.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax2.set_xlabel('Position x (mm)', fontsize=30, color=COLORS['text'], weight='bold')
        ax2.set_ylabel('Bending Moment M (N·m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax2.set_title('Bending Moment Diagram - Robotic Arm Cantilever',
                     fontsize=32, color=COLORS['text'], weight='bold', pad=20)

        # Vertical line at fixed support
        ax2.axvline(x=0, color=COLORS['load_arrow'], linewidth=4, alpha=0.5, linestyle='--')

        ax2.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_linewidth(4)
        ax2.spines['bottom'].set_linewidth(4)
        ax2.spines['left'].set_color(COLORS['text'])
        ax2.spines['bottom'].set_color(COLORS['text'])

        plt.tight_layout()
        return fig

    def generate_summary_report(self):
        """Print comprehensive summary of analysis."""
        print("\n" + "="*80)
        print("📊 ANALYSIS SUMMARY REPORT")
        print("="*80)

        print(f"\n1. GEOMETRY:")
        print(f"   • Beam type: Cantilever (fixed-free)")
        print(f"   • Length: {self.L} mm")
        print(f"   • Cross-section: {self.b} mm × {self.h} mm rectangular")

        print(f"\n2. LOADING:")
        print(f"   • Point load: P = {self.P} N at free end")

        print(f"\n3. REACTIONS:")
        print(f"   • Vertical reaction: R_y = {self.R_y} N (upward)")
        print(f"   • Reaction moment: M_A = {self.M_A/1000:.2f} N·m (counterclockwise)")

        print(f"\n4. INTERNAL FORCES:")
        print(f"   • Maximum shear: |V_max| = {self.V_max} N (constant)")
        print(f"   • Maximum moment: |M_max| = {self.M_max/1000:.2f} N·m at x = 0 mm")

        print(f"\n5. STRESSES:")
        print(f"   • Maximum bending stress: σ_max = {self.sigma_max:.2f} MPa")
        print(f"   • Location: Fixed support, top/bottom fibers")
        print(f"   • Yield strength: σ_yield = {self.sigma_yield} MPa")

        print(f"\n6. SAFETY FACTOR:")
        print(f"   • SF = {self.SF:.2f}")

        if self.SF >= 3.0 and self.SF <= 5.0:
            status = "✅ ACCEPTABLE"
        elif self.SF > 5.0:
            status = "⚠️  OVER-DESIGNED"
        else:
            status = "❌ INSUFFICIENT"

        print(f"   • Status: {status}")

        print(f"\n7. DESIGN RECOMMENDATIONS:")
        if self.SF >= 3.0 and self.SF <= 5.0:
            print(f"   • Current design is well-balanced for robotic applications")
            print(f"   • Adequate margin for dynamic loads and fatigue")
            print(f"   • No changes required")
        elif self.SF > 5.0:
            print(f"   • Consider reducing cross-section to save weight")
            print(f"   • Target SF = 3-4 for robotics")
            print(f"   • Could reduce h to ~{self.h * np.sqrt(self.sigma_yield/(4*self.sigma_max)):.1f} mm")
        else:
            print(f"   • Increase cross-section or use stronger material")
            print(f"   • Target SF ≥ 3.0 for robotic applications")

        print("\n" + "="*80)


def main():
    """Main analysis function."""
    # Create analysis object
    robot_arm = RoboticArmAnalysis()

    # Perform calculations
    robot_arm.calculate_reactions()
    robot_arm.calculate_critical_values()
    robot_arm.calculate_stresses()

    # Generate plots
    print("\n📊 GENERATING VISUALIZATIONS...")

    # Loading diagram
    fig1 = robot_arm.create_loading_diagram()
    output_path1 = os.path.join(SCRIPT_DIR, 'lab1_loading_diagram.svg')
    fig1.savefig(output_path1, format='svg', dpi=300,
                bbox_inches='tight', transparent=True)
    print(f"✅ Loading diagram saved: {output_path1}")

    # SFD and BMD
    fig2 = robot_arm.create_sfd_bmd_diagrams()
    output_path2 = os.path.join(SCRIPT_DIR, 'lab1_sfd_bmd.svg')
    fig2.savefig(output_path2, format='svg', dpi=300,
                bbox_inches='tight', transparent=True)
    print(f"✅ SFD/BMD diagrams saved: {output_path2}")

    plt.close('all')

    # Generate summary
    robot_arm.generate_summary_report()

    print(f"\n🎯 LAB 1 ANALYSIS COMPLETE!")
    print(f"\nOutput files:")
    print(f"  1. {output_path1}")
    print(f"  2. {output_path2}")


if __name__ == "__main__":
    main()
