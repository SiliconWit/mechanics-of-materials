#!/usr/bin/env python3
"""
Lab 2: 3D Printer Gantry Rail Analysis
Structural Analysis Laboratory - Bending Stresses and FEM

This script provides a complete example solution for Lab 2, demonstrating:
1. Parametric analysis of moving load on simply supported beam
2. Critical load position determination
3. Maximum bending stress calculation
4. Stress vs load position visualization
5. Mesh convergence study analysis

Problem: Desktop 3D printer gantry rail
- Simply supported beam: L = 800 mm (pinned at A, roller at B)
- Cross-section: Hollow circular tube OD 30mm, ID 24mm (wall = 3mm)
- Material: Aluminum alloy 6061-T6
- Load: P = 200 N (print head weight)
- Moving load position: variable (0 ≤ x ≤ L)

Author: SiliconWit Mechanics of Materials Laboratory
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrow, Circle, Polygon
import os

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Color scheme
COLORS = {
    'beam': '#2d7a8f',
    'support': '#6B7280',
    'ground': '#5ab9a0',
    'force': '#ff8c36',
    'reaction': '#00a0d0',
    'text': '#405ab9',
    'shear_pos': '#405ab9',
    'shear_neg': '#ff8c36',
    'moment_pos': '#405ab9',
    'grid': '#9ea388'
}

# Matplotlib settings
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
    'savefig.facecolor': 'none'
})


class GantryRailAnalysis:
    """Complete analysis for 3D printer gantry rail."""

    def __init__(self):
        """Initialize problem parameters."""
        # Geometry (all in mm)
        self.L = 800.0              # Beam length
        self.OD = 30.0              # Outer diameter
        self.t = 3.0                # Wall thickness
        self.ID = self.OD - 2*self.t  # Inner diameter

        # Loading (in N)
        self.P = 200.0              # Print head weight

        # Material properties
        self.sigma_yield = 275.0    # MPa (Aluminum 6061-T6)
        self.E = 70000.0            # MPa (Young's modulus)
        self.nu = 0.33              # Poisson's ratio

        # Section properties (hollow circular)
        self.I = (np.pi / 64) * (self.OD**4 - self.ID**4)  # Moment of inertia
        self.c = self.OD / 2                                # Distance to outer fiber
        self.S = self.I / self.c                            # Section modulus
        self.J = 2 * self.I                                 # Polar moment (circular)

        print("="*80)
        print("LAB 2: 3D PRINTER GANTRY RAIL ANALYSIS")
        print("="*80)
        print("\n📋 PROBLEM PARAMETERS:")
        print(f"• Beam length: L = {self.L} mm")
        print(f"• Support type: Simply supported (pin-roller)")
        print(f"• Cross-section: Hollow circular tube")
        print(f"  - Outer diameter: OD = {self.OD} mm")
        print(f"  - Inner diameter: ID = {self.ID} mm")
        print(f"  - Wall thickness: t = {self.t} mm")
        print(f"• Point load: P = {self.P} N (print head)")
        print(f"• Load position: VARIABLE (moving)")
        print(f"• Material: Aluminum 6061-T6")
        print(f"• Yield strength: σ_yield = {self.sigma_yield} MPa")
        print(f"• Young's modulus: E = {self.E} MPa")

        print(f"\n📐 SECTION PROPERTIES:")
        print(f"• Moment of inertia: I = π(OD⁴-ID⁴)/64 = {self.I:.2e} mm⁴")
        print(f"• Distance to outer fiber: c = OD/2 = {self.c} mm")
        print(f"• Section modulus: S = I/c = {self.S:.2e} mm³")

    def calculate_reactions(self, a):
        """
        Calculate support reactions for load at position 'a' from left support.

        Parameters:
        a : float or array, load position from left support (mm)

        Returns:
        R_A, R_B : reactions at left and right supports (N)
        """
        R_B = (self.P * a) / self.L
        R_A = self.P - R_B
        return R_A, R_B

    def calculate_moment_under_load(self, a):
        """
        Calculate bending moment directly under the load at position 'a'.

        For simply supported beam with point load at 'a':
        M(a) = (P × a × (L - a)) / L

        Parameters:
        a : float or array, load position from left support (mm)

        Returns:
        M : bending moment (N·mm)
        """
        M = (self.P * a * (self.L - a)) / self.L
        return M

    def find_critical_position(self):
        """
        Find load position that produces maximum bending moment.

        For simply supported beam with point load:
        dM/da = 0 when a = L/2 (midspan)
        """
        print("\n🔍 CRITICAL LOAD POSITION ANALYSIS:")
        print("\nFor simply supported beam with point load at position 'a':")
        print(f"M(a) = P·a·(L-a)/L = {self.P}·a·({self.L}-a)/{self.L}")

        print(f"\nTo find maximum, take derivative and set to zero:")
        print(f"dM/da = P(L - 2a)/L = 0")
        print(f"L - 2a = 0")
        print(f"a = L/2 = {self.L}/2 = {self.L/2} mm")

        self.a_critical = self.L / 2

        print(f"\n✓ Critical position: a = {self.a_critical} mm (MIDSPAN)")

        # Calculate moment at critical position
        self.M_max = self.calculate_moment_under_load(self.a_critical)
        print(f"✓ Maximum moment: M_max = {self.M_max:.0f} N·mm = {self.M_max/1000:.2f} N·m")

        return self.a_critical, self.M_max

    def calculate_stress(self, M):
        """
        Calculate maximum bending stress using flexure formula.

        σ_max = M·c / I

        Parameters:
        M : bending moment (N·mm)

        Returns:
        σ : maximum bending stress (MPa)
        """
        sigma = (M * self.c) / self.I
        return sigma

    def parametric_stress_analysis(self):
        """Analyze stress for all possible load positions."""
        print("\n📊 PARAMETRIC STRESS ANALYSIS:")

        # Create array of load positions
        a_positions = np.linspace(0.1, self.L-0.1, 200)  # Avoid exactly 0 and L

        # Calculate moments and stresses
        M_values = self.calculate_moment_under_load(a_positions)
        sigma_values = self.calculate_stress(M_values)

        # Find maximum
        max_idx = np.argmax(sigma_values)
        self.sigma_max = sigma_values[max_idx]
        a_at_max = a_positions[max_idx]

        print(f"\nStress at various load positions:")
        positions_to_check = [100, 200, 400, 600, 700]
        for pos in positions_to_check:
            M = self.calculate_moment_under_load(pos)
            sigma = self.calculate_stress(M)
            print(f"  • a = {pos:3.0f} mm: σ = {sigma:.3f} MPa")

        print(f"\n✓ Maximum stress: σ_max = {self.sigma_max:.3f} MPa")
        print(f"✓ Occurs at: a = {a_at_max:.1f} mm ≈ {self.a_critical:.0f} mm (midspan)")

        # Safety factor
        self.SF = self.sigma_yield / self.sigma_max
        print(f"\n🔧 SAFETY FACTOR:")
        print(f"SF = σ_yield / σ_max = {self.sigma_yield} / {self.sigma_max:.3f} = {self.SF:.1f}")

        if self.SF > 10:
            print(f"\n💡 ASSESSMENT:")
            print(f"   • SF = {self.SF:.1f} is VERY HIGH for static loading")
            print(f"   • Design is over-conservative for static loads")
            print(f"   • However, 3D printers experience:")
            print(f"     - Dynamic loads (acceleration/deceleration)")
            print(f"     - Vibration during rapid movements")
            print(f"     - Millions of load cycles (fatigue)")
            print(f"   • High static SF provides margin for dynamic effects")
            print(f"   • Dynamic amplification: 2-5× static loads")
            print(f"   • Effective dynamic SF ≈ {self.SF/3:.1f} (reasonable)")

        return a_positions, M_values, sigma_values

    def create_stress_analysis_plots(self, a_positions, M_values, sigma_values):
        """Create plots showing stress vs load position."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))

        # Plot 1: Bending Moment vs Load Position
        ax1.plot(a_positions, M_values/1000, color=COLORS['moment_pos'], linewidth=5)
        ax1.fill_between(a_positions, 0, M_values/1000, alpha=0.3, color=COLORS['moment_pos'])

        # Mark critical position
        ax1.axvline(x=self.a_critical, color=COLORS['force'], linewidth=4,
                   linestyle='--', alpha=0.6, label=f'Critical: a = {self.a_critical:.0f} mm')
        ax1.plot(self.a_critical, self.M_max/1000, 'o', markersize=18,
                color='#FFFFFF', markeredgewidth=5,
                markerfacecolor=COLORS['force'], markeredgecolor=COLORS['text'], zorder=5)

        ax1.annotate(f'M_max = {self.M_max/1000:.2f} N·m', (self.a_critical, self.M_max/1000),
                    xytext=(50, 20), textcoords='offset points',
                    fontsize=24, color=COLORS['text'], weight='bold',
                    arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=3))

        ax1.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax1.set_xlabel('Load Position a (mm)', fontsize=30, color=COLORS['text'], weight='bold')
        ax1.set_ylabel('Bending Moment (N·m)', fontsize=30, color=COLORS['text'], weight='bold')
        ax1.set_title('Bending Moment vs Print Head Position',
                     fontsize=32, color=COLORS['text'], weight='bold', pad=20)
        ax1.legend(loc='upper right', fontsize=24)
        ax1.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_linewidth(4)
        ax1.spines['bottom'].set_linewidth(4)
        ax1.spines['left'].set_color(COLORS['text'])
        ax1.spines['bottom'].set_color(COLORS['text'])

        # Plot 2: Bending Stress vs Load Position
        ax2.plot(a_positions, sigma_values, color=COLORS['moment_pos'], linewidth=5,
                label='Max bending stress')
        ax2.fill_between(a_positions, 0, sigma_values, alpha=0.3, color=COLORS['moment_pos'])

        # Yield strength line
        ax2.axhline(y=self.sigma_yield, color=COLORS['force'], linewidth=4,
                   linestyle='--', alpha=0.7, label=f'Yield strength = {self.sigma_yield} MPa')

        # Mark critical position
        ax2.axvline(x=self.a_critical, color=COLORS['force'], linewidth=4,
                   linestyle='--', alpha=0.6)
        ax2.plot(self.a_critical, self.sigma_max, 'o', markersize=18,
                color='#FFFFFF', markeredgewidth=5,
                markerfacecolor=COLORS['force'], markeredgecolor=COLORS['text'], zorder=5)

        ax2.annotate(f'σ_max = {self.sigma_max:.3f} MPa\nSF = {self.SF:.1f}',
                    (self.a_critical, self.sigma_max),
                    xytext=(50, 50), textcoords='offset points',
                    fontsize=24, color=COLORS['text'], weight='bold',
                    arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=3))

        ax2.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax2.set_xlabel('Load Position a (mm)', fontsize=30, color=COLORS['text'], weight='bold')
        ax2.set_ylabel('Maximum Bending Stress (MPa)', fontsize=30, color=COLORS['text'], weight='bold')
        ax2.set_title('Bending Stress vs Print Head Position',
                     fontsize=32, color=COLORS['text'], weight='bold', pad=20)
        ax2.legend(loc='upper right', fontsize=24)
        ax2.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_linewidth(4)
        ax2.spines['bottom'].set_linewidth(4)
        ax2.spines['left'].set_color(COLORS['text'])
        ax2.spines['bottom'].set_color(COLORS['text'])

        plt.tight_layout()
        return fig

    def mesh_convergence_template(self):
        """Provide template for mesh convergence study."""
        print("\n" + "="*80)
        print("🔬 MESH CONVERGENCE STUDY TEMPLATE")
        print("="*80)

        print("\nThis template shows how to analyze FEM mesh convergence.")
        print("Fill in the actual FEM results from FreeCAD analysis.\n")

        # Example data (students fill in their actual values)
        element_sizes = np.array([20, 10, 5, 2.5])  # mm
        num_elements = np.array([150, 500, 2000, 8000])  # Example values
        max_stress_fem = np.array([0, 0, 0, 0])  # TO BE FILLED FROM FEM

        print("Element Size (mm) | Num Elements | Max Stress (MPa) | Error (%)")
        print("-" * 65)
        for i in range(len(element_sizes)):
            if max_stress_fem[i] > 0:
                error = abs(max_stress_fem[i] - self.sigma_max) / self.sigma_max * 100
                print(f"{element_sizes[i]:^17.1f} | {num_elements[i]:^12d} | "
                      f"{max_stress_fem[i]:^16.3f} | {error:^9.2f}")
            else:
                print(f"{element_sizes[i]:^17.1f} | {num_elements[i]:^12d} | "
                      f"{'TO BE FILLED':^16} | {'---':^9}")

        print(f"\nAnalytical solution: σ_max = {self.sigma_max:.3f} MPa (at midspan)")
        print("\n💡 Convergence criterion: Error < 5% indicates adequate mesh")

        return element_sizes, num_elements, max_stress_fem

    def create_convergence_plot_template(self, element_sizes, num_elements, max_stress_fem):
        """Create convergence plot template."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

        # Only plot if data is filled in
        if np.any(max_stress_fem > 0):
            # Stress vs Number of Elements
            ax1.plot(num_elements, max_stress_fem, 'bo-', linewidth=4, markersize=12,
                    label='FEM Results')
            ax1.axhline(y=self.sigma_max, color=COLORS['force'], linewidth=4,
                       linestyle='--', label=f'Analytical = {self.sigma_max:.3f} MPa')

            ax1.set_xlabel('Number of Elements', fontsize=30, color=COLORS['text'], weight='bold')
            ax1.set_ylabel('Maximum Stress (MPa)', fontsize=30, color=COLORS['text'], weight='bold')
            ax1.set_title('Mesh Convergence Study', fontsize=32, color=COLORS['text'],
                         weight='bold', pad=20)
            ax1.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
            ax1.legend(fontsize=24)

            # Percent Error vs Number of Elements
            percent_error = np.abs(max_stress_fem - self.sigma_max) / self.sigma_max * 100
            ax2.plot(num_elements, percent_error, 'ro-', linewidth=4, markersize=12)
            ax2.axhline(y=5, color=COLORS['grid'], linewidth=3, linestyle='--',
                       label='5% threshold')

            ax2.set_xlabel('Number of Elements', fontsize=30, color=COLORS['text'], weight='bold')
            ax2.set_ylabel('Percent Error (%)', fontsize=30, color=COLORS['text'], weight='bold')
            ax2.set_title('FEM Error vs Mesh Refinement', fontsize=32, color=COLORS['text'],
                         weight='bold', pad=20)
            ax2.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
            ax2.legend(fontsize=24)
        else:
            ax1.text(0.5, 0.5, 'Fill in FEM data\nto generate plot',
                    ha='center', va='center', fontsize=32, color=COLORS['text'],
                    transform=ax1.transAxes)
            ax2.text(0.5, 0.5, 'Fill in FEM data\nto generate plot',
                    ha='center', va='center', fontsize=32, color=COLORS['text'],
                    transform=ax2.transAxes)

        for ax in [ax1, ax2]:
            ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_linewidth(4)
            ax.spines['bottom'].set_linewidth(4)
            ax.spines['left'].set_color(COLORS['text'])
            ax.spines['bottom'].set_color(COLORS['text'])

        plt.tight_layout()
        return fig


def main():
    """Main analysis function."""
    # Create analysis object
    gantry = GantryRailAnalysis()

    # Find critical position
    gantry.find_critical_position()

    # Parametric analysis
    a_positions, M_values, sigma_values = gantry.parametric_stress_analysis()

    # Generate plots
    print("\n📊 GENERATING VISUALIZATIONS...")

    # Stress analysis plots
    fig1 = gantry.create_stress_analysis_plots(a_positions, M_values, sigma_values)
    output_path1 = os.path.join(SCRIPT_DIR, 'lab2_stress_analysis.svg')
    fig1.savefig(output_path1, format='svg', dpi=300,
                bbox_inches='tight', transparent=True)
    print(f"✅ Stress analysis plots saved: {output_path1}")

    # Mesh convergence template
    element_sizes, num_elements, max_stress_fem = gantry.mesh_convergence_template()

    fig2 = gantry.create_convergence_plot_template(element_sizes, num_elements, max_stress_fem)
    output_path2 = os.path.join(SCRIPT_DIR, 'lab2_convergence_template.svg')
    fig2.savefig(output_path2, format='svg', dpi=300,
                bbox_inches='tight', transparent=True)
    print(f"✅ Convergence template saved: {output_path2}")

    plt.close('all')

    print("\n" + "="*80)
    print("🎯 LAB 2 ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nKey Results:")
    print(f"  • Critical position: a = {gantry.a_critical} mm (midspan)")
    print(f"  • Maximum moment: M_max = {gantry.M_max/1000:.2f} N·m")
    print(f"  • Maximum stress: σ_max = {gantry.sigma_max:.3f} MPa")
    print(f"  • Safety factor: SF = {gantry.SF:.1f}")
    print(f"\nOutput files:")
    print(f"  1. {output_path1}")
    print(f"  2. {output_path2}")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
