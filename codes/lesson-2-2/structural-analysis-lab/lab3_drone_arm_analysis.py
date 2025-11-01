#!/usr/bin/env python3
"""
Lab 3: Drone Arm Combined Loading Analysis
Structural Analysis Laboratory - Combined Bending and Torsion

This script provides a complete example solution for Lab 3, demonstrating:
1. Combined loading analysis (bending + torsion)
2. Principal stress calculations
3. Mohr's circle construction and visualization
4. Von Mises and maximum stress failure criteria
5. Design optimization for weight reduction

Problem: Quadcopter drone motor arm
- Cantilever: L = 200 mm (fixed to drone body)
- Cross-section: Circular tube OD 16mm, ID 12mm
- Material: Carbon fiber composite
- Loads:
  * Vertical thrust: P = 30 N (motor thrust)
  * Horizontal drag: F_drag = 5 N
  * Gyroscopic torque: T = 1.0 N·m (propeller effect)

Author: SiliconWit Mechanics of Materials Laboratory
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Wedge, FancyArrowPatch
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
    'mohr_circle': '#405ab9',
    'principal': '#ff8c36',
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


class DroneArmAnalysis:
    """Complete analysis for drone arm with combined loading."""

    def __init__(self):
        """Initialize problem parameters."""
        # Geometry (all in mm)
        self.L = 200.0              # Arm length
        self.OD = 16.0              # Outer diameter
        self.ID = 12.0              # Inner diameter
        self.r_outer = self.OD / 2  # Outer radius
        self.r_inner = self.ID / 2  # Inner radius

        # Loading
        self.P_vertical = 30.0      # N, vertical thrust
        self.F_horizontal = 5.0     # N, horizontal drag
        self.T_torque = 1000.0      # N·mm, gyroscopic torque (1.0 N·m)

        # Material properties (Carbon fiber composite)
        self.sigma_tensile = 600.0    # MPa, tensile strength
        self.sigma_compressive = 500.0  # MPa, compressive strength
        self.tau_ultimate = 70.0      # MPa, shear strength
        self.E = 70000.0              # MPa, Young's modulus (longitudinal)
        self.nu = 0.10                # Poisson's ratio (orthotropic, use equiv.)

        # Section properties (hollow circular)
        self.I = (np.pi / 64) * (self.OD**4 - self.ID**4)  # Bending inertia
        self.J = (np.pi / 32) * (self.OD**4 - self.ID**4)  # Polar inertia (torsion)

        print("="*80)
        print("LAB 3: DRONE ARM COMBINED LOADING ANALYSIS")
        print("="*80)
        print("\n📋 PROBLEM PARAMETERS:")
        print(f"• Arm length: L = {self.L} mm")
        print(f"• Support type: Cantilever (fixed to drone body)")
        print(f"• Cross-section: Hollow circular tube")
        print(f"  - Outer diameter: OD = {self.OD} mm")
        print(f"  - Inner diameter: ID = {self.ID} mm")
        print(f"  - Wall thickness: t = {(self.OD-self.ID)/2} mm")

        print(f"\n⚡ LOADING (Combined):")
        print(f"• Vertical thrust: P = {self.P_vertical} N (motor)")
        print(f"• Horizontal drag: F = {self.F_horizontal} N (aerodynamic)")
        print(f"• Gyroscopic torque: T = {self.T_torque/1000:.1f} N·m (propeller)")

        print(f"\n🧪 MATERIAL (Carbon Fiber Composite):")
        print(f"• Tensile strength: {self.sigma_tensile} MPa")
        print(f"• Compressive strength: {self.sigma_compressive} MPa")
        print(f"• Shear strength: {self.tau_ultimate} MPa")
        print(f"• Young's modulus: {self.E} MPa")

        print(f"\n📐 SECTION PROPERTIES:")
        print(f"• Bending moment of inertia: I = {self.I:.1f} mm⁴")
        print(f"• Polar moment of inertia: J = {self.J:.1f} mm⁴")

    def analyze_bending_from_vertical_load(self):
        """Analyze bending stress from vertical thrust."""
        print("\n" + "="*80)
        print("1️⃣  BENDING FROM VERTICAL THRUST")
        print("="*80)

        # Bending moment at fixed end
        self.M_vertical = self.P_vertical * self.L

        # Bending stress at outer fiber
        self.sigma_vertical = (self.M_vertical * self.r_outer) / self.I

        print(f"\nBending moment at fixed end:")
        print(f"  M_y = P × L = {self.P_vertical} × {self.L} = {self.M_vertical:.0f} N·mm")

        print(f"\nMaximum bending stress (flexure formula):")
        print(f"  σ_bending_vertical = (M_y × c) / I")
        print(f"  σ_bending_vertical = ({self.M_vertical:.0f} × {self.r_outer}) / {self.I:.1f}")
        print(f"  σ_bending_vertical = {self.sigma_vertical:.2f} MPa")

        print(f"\nStress distribution:")
        print(f"  • Top fiber: COMPRESSION (−{self.sigma_vertical:.2f} MPa)")
        print(f"  • Bottom fiber: TENSION (+{self.sigma_vertical:.2f} MPa)")

        return self.M_vertical, self.sigma_vertical

    def analyze_bending_from_horizontal_load(self):
        """Analyze bending stress from horizontal drag."""
        print("\n" + "="*80)
        print("2️⃣  BENDING FROM HORIZONTAL DRAG")
        print("="*80)

        # Bending moment at fixed end
        self.M_horizontal = self.F_horizontal * self.L

        # Bending stress at outer fiber
        self.sigma_horizontal = (self.M_horizontal * self.r_outer) / self.I

        print(f"\nBending moment at fixed end:")
        print(f"  M_z = F_drag × L = {self.F_horizontal} × {self.L} = {self.M_horizontal:.0f} N·mm")

        print(f"\nMaximum bending stress (flexure formula):")
        print(f"  σ_bending_horizontal = (M_z × c) / I")
        print(f"  σ_bending_horizontal = ({self.M_horizontal:.0f} × {self.r_outer}) / {self.I:.1f}")
        print(f"  σ_bending_horizontal = {self.sigma_horizontal:.2f} MPa")

        print(f"\nStress distribution:")
        print(f"  • Side fibers: Max stress ±{self.sigma_horizontal:.2f} MPa")

        return self.M_horizontal, self.sigma_horizontal

    def analyze_torsion(self):
        """Analyze torsional shear stress."""
        print("\n" + "="*80)
        print("3️⃣  TORSION FROM GYROSCOPIC MOMENT")
        print("="*80)

        # Torsional shear stress
        self.tau_torsion = (self.T_torque * self.r_outer) / self.J

        print(f"\nApplied torque:")
        print(f"  T = {self.T_torque:.0f} N·mm = {self.T_torque/1000:.2f} N·m")

        print(f"\nMaximum torsional shear stress:")
        print(f"  τ_xy = (T × r) / J")
        print(f"  τ_xy = ({self.T_torque:.0f} × {self.r_outer}) / {self.J:.1f}")
        print(f"  τ_xy = {self.tau_torsion:.2f} MPa")

        print(f"\nShear stress distribution:")
        print(f"  • Maximum at outer surface: {self.tau_torsion:.2f} MPa")
        print(f"  • Zero at centerline (neutral axis)")

        return self.tau_torsion

    def combine_stresses(self):
        """Combine all stress components at critical point."""
        print("\n" + "="*80)
        print("4️⃣  STRESS SUPERPOSITION AT CRITICAL POINT")
        print("="*80)

        print("\nCritical location: Fixed end, outer fiber at 45°")
        print("(where both bending components contribute)")

        # Combined bending stress (vector sum for worst case)
        self.sigma_x = np.sqrt(self.sigma_vertical**2 + self.sigma_horizontal**2)

        # Shear stress from torsion
        self.tau_xy = self.tau_torsion

        # Other normal stresses (plane stress assumption)
        self.sigma_y = 0.0
        self.sigma_z = 0.0

        print(f"\nStress state at critical point:")
        print(f"  • Normal stress (axial): σ_x = {self.sigma_x:.2f} MPa (tension)")
        print(f"  • Shear stress: τ_xy = {self.tau_xy:.2f} MPa (torsion)")
        print(f"  • σ_y = σ_z = 0 (plane stress assumption)")

        print(f"\n💡 Note: Combined bending from both planes:")
        print(f"  σ_x = √(σ_vertical² + σ_horizontal²)")
        print(f"  σ_x = √({self.sigma_vertical:.2f}² + {self.sigma_horizontal:.2f}²)")
        print(f"  σ_x = {self.sigma_x:.2f} MPa")

        return self.sigma_x, self.tau_xy

    def calculate_principal_stresses(self):
        """Calculate principal stresses from combined state."""
        print("\n" + "="*80)
        print("5️⃣  PRINCIPAL STRESS CALCULATION")
        print("="*80)

        # Average normal stress
        sigma_avg = (self.sigma_x + self.sigma_y) / 2

        # Radius of Mohr's circle
        R = np.sqrt(((self.sigma_x - self.sigma_y)/2)**2 + self.tau_xy**2)

        # Principal stresses
        self.sigma_1 = sigma_avg + R  # Maximum principal
        self.sigma_2 = sigma_avg - R  # Minimum principal
        self.sigma_3 = 0.0            # Out-of-plane (plane stress)

        # Maximum shear stress
        self.tau_max = (self.sigma_1 - self.sigma_2) / 2

        # Principal angle
        if abs(self.sigma_x - self.sigma_y) > 1e-6:
            self.theta_p = 0.5 * np.arctan2(2*self.tau_xy, self.sigma_x - self.sigma_y)
            theta_p_deg = np.degrees(self.theta_p)
        else:
            theta_p_deg = 45.0

        print(f"\nPrincipal stress formulas:")
        print(f"  σ_avg = (σ_x + σ_y) / 2 = {sigma_avg:.2f} MPa")
        print(f"  R = √[(σ_x - σ_y)/2)² + τ_xy²]")
        print(f"  R = √[({self.sigma_x:.2f}/2)² + {self.tau_xy:.2f}²] = {R:.2f} MPa")

        print(f"\n📊 PRINCIPAL STRESSES:")
        print(f"  • σ₁ (maximum): {self.sigma_1:.2f} MPa (TENSILE)")
        print(f"  • σ₂ (minimum): {self.sigma_2:.2f} MPa")
        print(f"  • σ₃ (out-of-plane): {self.sigma_3:.2f} MPa")
        print(f"  • τ_max (Tresca): {self.tau_max:.2f} MPa")
        print(f"  • θ_p (principal angle): {theta_p_deg:.1f}°")

        return self.sigma_1, self.sigma_2, self.sigma_3, self.tau_max

    def apply_failure_criteria(self):
        """Apply various failure criteria."""
        print("\n" + "="*80)
        print("6️⃣  FAILURE CRITERIA ANALYSIS")
        print("="*80)

        # Von Mises stress (for ductile materials)
        self.sigma_vm = np.sqrt(((self.sigma_1 - self.sigma_2)**2 +
                                 (self.sigma_2 - self.sigma_3)**2 +
                                 (self.sigma_3 - self.sigma_1)**2) / 2)

        print(f"\n1. Von Mises Criterion (ductile materials):")
        print(f"   σ_VM = √[((σ₁-σ₂)² + (σ₂-σ₃)² + (σ₃-σ₁)²) / 2]")
        print(f"   σ_VM = {self.sigma_vm:.2f} MPa")

        SF_vm = self.sigma_compressive / self.sigma_vm
        print(f"   SF (Von Mises) = {self.sigma_compressive} / {self.sigma_vm:.2f} = {SF_vm:.2f}")

        # Maximum stress criterion (for brittle materials like composites)
        print(f"\n2. Maximum Stress Criterion (brittle/composite):")
        print(f"   Compare max principal stress to strengths:")

        SF_tension = self.sigma_tensile / self.sigma_1
        SF_compression = self.sigma_compressive / abs(self.sigma_2) if abs(self.sigma_2) > 0.1 else 1000
        SF_shear = self.tau_ultimate / self.tau_max

        print(f"   • Tension check: SF = {self.sigma_tensile} / {self.sigma_1:.2f} = {SF_tension:.2f}")
        print(f"   • Compression check: SF = {self.sigma_compressive} / {abs(self.sigma_2):.2f} = {SF_compression:.1f}")
        print(f"   • Shear check: SF = {self.tau_ultimate} / {self.tau_max:.2f} = {SF_shear:.2f}")

        # Governing safety factor
        self.SF_governing = min(SF_tension, SF_compression, SF_shear)

        print(f"\n3. Tresca Criterion (Maximum Shear Stress):")
        print(f"   τ_max = (σ₁ - σ₃) / 2 = {self.tau_max:.2f} MPa")
        SF_tresca = self.tau_ultimate / self.tau_max
        print(f"   SF (Tresca) = {self.tau_ultimate} / {self.tau_max:.2f} = {SF_tresca:.2f}")

        print(f"\n" + "="*80)
        print(f"📈 SAFETY FACTOR SUMMARY:")
        print(f"="*80)
        print(f"  • Von Mises: SF = {SF_vm:.2f}")
        print(f"  • Max Stress (tension): SF = {SF_tension:.2f} ← GOVERNS (composite)")
        print(f"  • Max Stress (compression): SF = {SF_compression:.1f}")
        print(f"  • Max Stress (shear): SF = {SF_shear:.2f}")
        print(f"  • Tresca: SF = {SF_tresca:.2f}")
        print(f"\n  ✅ GOVERNING SAFETY FACTOR: {self.SF_governing:.2f}")

        if self.SF_governing >= 3.0 and self.SF_governing <= 5.0:
            print(f"\n  ✅ Excellent for drone applications (target: 3-5)")
        elif self.SF_governing > 5.0:
            print(f"\n  ⚠️  Over-designed - consider weight reduction")
        else:
            print(f"\n  ❌ Insufficient - increase strength or reduce load")

        return self.sigma_vm, self.SF_governing

    def create_mohrs_circle(self):
        """Create Mohr's circle visualization."""
        fig, ax = plt.subplots(figsize=(14, 14))

        # Circle parameters
        sigma_avg = (self.sigma_x + self.sigma_y) / 2
        R = np.sqrt(((self.sigma_x - self.sigma_y)/2)**2 + self.tau_xy**2)

        # Draw Mohr's circle
        theta = np.linspace(0, 2*np.pi, 200)
        circle_x = sigma_avg + R * np.cos(theta)
        circle_y = R * np.sin(theta)

        ax.plot(circle_x, circle_y, color=COLORS['mohr_circle'],
               linewidth=5, label="Mohr's Circle")
        ax.fill(circle_x, circle_y, alpha=0.1, color=COLORS['mohr_circle'])

        # Axes
        ax.axhline(y=0, color=COLORS['text'], linewidth=3, alpha=0.7)
        ax.axvline(x=0, color=COLORS['text'], linewidth=3, alpha=0.7)

        # Principal stresses on σ-axis
        ax.plot([self.sigma_1, self.sigma_2], [0, 0], 'o',
               markersize=20, color='#FFFFFF', markeredgewidth=5,
               markerfacecolor=COLORS['principal'],
               markeredgecolor=COLORS['text'], zorder=10,
               label='Principal Stresses')

        # Labels for principal stresses
        ax.text(self.sigma_1, -3, f'σ₁ = {self.sigma_1:.1f} MPa',
               fontsize=24, ha='center', va='top', weight='bold',
               color=COLORS['text'],
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['principal'], linewidth=3))

        ax.text(self.sigma_2, 3, f'σ₂ = {self.sigma_2:.1f} MPa',
               fontsize=24, ha='center', va='bottom', weight='bold',
               color=COLORS['text'],
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC',
                        edgecolor=COLORS['principal'], linewidth=3))

        # Original stress state points
        ax.plot([self.sigma_x, self.sigma_y], [self.tau_xy, -self.tau_xy], 's',
               markersize=16, color='#FFFFFF', markeredgewidth=4,
               markerfacecolor=COLORS['force'], markeredgecolor=COLORS['text'],
               zorder=10, label='Original State')

        # Line connecting original state points
        ax.plot([self.sigma_x, self.sigma_y], [self.tau_xy, -self.tau_xy],
               color=COLORS['force'], linewidth=3, linestyle='--')

        # Label original state
        if self.tau_xy > 0:
            ax.text(self.sigma_x + 3, self.tau_xy + 0.5,
                   f'(σ_x, τ_xy)\n({self.sigma_x:.1f}, {self.tau_xy:.1f})',
                   fontsize=20, ha='left', weight='bold', color=COLORS['text'])

        # Center point
        ax.plot(sigma_avg, 0, 'x', markersize=15, markeredgewidth=4,
               color=COLORS['text'], zorder=10)
        ax.text(sigma_avg, -1, f'σ_avg = {sigma_avg:.1f}',
               fontsize=20, ha='center', va='top', weight='bold',
               color=COLORS['text'])

        # Maximum shear stress
        ax.plot([sigma_avg, sigma_avg], [R, -R], 'o',
               markersize=14, color='#FFFFFF', markeredgewidth=4,
               markerfacecolor=COLORS['force'], markeredgecolor=COLORS['text'],
               zorder=10)
        ax.text(sigma_avg - 5, R, f'τ_max = {R:.1f} MPa',
               fontsize=20, ha='right', va='center', weight='bold',
               color=COLORS['text'])

        # Grid and formatting
        ax.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax.set_xlabel('Normal Stress σ (MPa)', fontsize=32,
                     color=COLORS['text'], weight='bold')
        ax.set_ylabel('Shear Stress τ (MPa)', fontsize=32,
                     color=COLORS['text'], weight='bold')
        ax.set_title("Mohr's Circle - Drone Arm Combined Loading",
                    fontsize=36, color=COLORS['text'], weight='bold', pad=25)

        ax.legend(loc='upper right', fontsize=24, framealpha=0.95)
        ax.set_aspect('equal')
        ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)

        for spine in ax.spines.values():
            spine.set_linewidth(4)
            spine.set_color(COLORS['text'])

        plt.tight_layout()
        return fig

    def design_optimization(self):
        """Perform design optimization for weight reduction."""
        print("\n" + "="*80)
        print("7️⃣  DESIGN OPTIMIZATION FOR WEIGHT REDUCTION")
        print("="*80)

        # Target safety factor
        SF_target = 3.0

        # Vary outer diameter, keep wall thickness proportional
        OD_range = np.linspace(12, 20, 25)
        wall_fraction = 0.25  # Keep wall as 25% of OD

        masses = []
        safety_factors = []

        # Material density (carbon fiber)
        rho = 1.6e-6  # kg/mm³

        print(f"\nOptimization parameters:")
        print(f"  • Target safety factor: {SF_target}")
        print(f"  • Variable: Outer diameter (OD)")
        print(f"  • Constraint: Wall thickness = 25% of OD")
        print(f"  • Arm length: {self.L} mm (fixed)")
        print(f"  • Loading: Same as current analysis")

        for OD in OD_range:
            ID = OD * (1 - 2*wall_fraction)
            r_out = OD / 2
            r_in = ID / 2

            # Section properties
            I = (np.pi / 64) * (OD**4 - ID**4)
            J = (np.pi / 32) * (OD**4 - ID**4)

            # Stresses
            M_v = self.P_vertical * self.L
            M_h = self.F_horizontal * self.L
            sigma_v = (M_v * r_out) / I
            sigma_h = (M_h * r_out) / I
            sigma_x = np.sqrt(sigma_v**2 + sigma_h**2)
            tau_xy = (self.T_torque * r_out) / J

            # Principal stress
            R = np.sqrt((sigma_x/2)**2 + tau_xy**2)
            sigma_1 = sigma_x/2 + R

            # Safety factor (max stress criterion)
            SF = self.sigma_tensile / sigma_1
            safety_factors.append(SF)

            # Mass
            volume = np.pi * (r_out**2 - r_in**2) * self.L
            mass = volume * rho * 1000  # Convert to grams
            masses.append(mass)

        # Find optimal design
        safety_factors = np.array(safety_factors)
        masses = np.array(masses)

        optimal_idx = np.argmin(np.abs(safety_factors - SF_target))
        optimal_OD = OD_range[optimal_idx]
        optimal_mass = masses[optimal_idx]
        optimal_SF = safety_factors[optimal_idx]

        # Current design
        current_volume = np.pi * (self.r_outer**2 - self.r_inner**2) * self.L
        current_mass = current_volume * rho * 1000

        print(f"\n📊 OPTIMIZATION RESULTS:")
        print(f"  • Original design:")
        print(f"    - OD = {self.OD} mm, ID = {self.ID} mm")
        print(f"    - Mass = {current_mass:.2f} g")
        print(f"    - SF = {self.SF_governing:.2f}")

        print(f"\n  • Optimized design:")
        print(f"    - OD = {optimal_OD:.1f} mm, ID = {optimal_OD*(1-2*wall_fraction):.1f} mm")
        print(f"    - Mass = {optimal_mass:.2f} g")
        print(f"    - SF = {optimal_SF:.2f}")

        savings = current_mass - optimal_mass
        savings_pct = (savings / current_mass) * 100

        print(f"\n  • Weight savings:")
        print(f"    - Per arm: {savings:.2f} g ({savings_pct:.1f}%)")
        print(f"    - For 4 arms: {4*savings:.2f} g")

        if savings > 0:
            print(f"\n  ✅ Lighter design achieves target SF = {SF_target}")
        else:
            print(f"\n  ⚠️  Current design is already optimal or lighter than target")

        return OD_range, masses, safety_factors, optimal_OD, optimal_mass

    def create_optimization_plots(self, OD_range, masses, safety_factors,
                                 optimal_OD, optimal_mass):
        """Create design optimization visualization."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

        # Plot 1: Mass vs OD
        ax1.plot(OD_range, masses, color=COLORS['mohr_circle'], linewidth=5)
        ax1.fill_between(OD_range, 0, masses, alpha=0.2, color=COLORS['mohr_circle'])

        # Mark optimal
        optimal_idx = np.argmin(np.abs(OD_range - optimal_OD))
        ax1.plot(optimal_OD, optimal_mass, 'o', markersize=20,
                color='#FFFFFF', markeredgewidth=5,
                markerfacecolor=COLORS['principal'],
                markeredgecolor=COLORS['text'], zorder=10)

        ax1.annotate(f'Optimal:\nOD = {optimal_OD:.1f} mm\nm = {optimal_mass:.1f} g',
                    (optimal_OD, optimal_mass), xytext=(20, 30),
                    textcoords='offset points', fontsize=22,
                    color=COLORS['text'], weight='bold',
                    arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=3))

        ax1.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax1.set_xlabel('Outer Diameter (mm)', fontsize=30,
                      color=COLORS['text'], weight='bold')
        ax1.set_ylabel('Mass per Arm (grams)', fontsize=30,
                      color=COLORS['text'], weight='bold')
        ax1.set_title('Arm Mass vs Tube Diameter',
                     fontsize=32, color=COLORS['text'], weight='bold', pad=20)

        # Plot 2: Safety Factor vs OD
        ax2.plot(OD_range, safety_factors, color=COLORS['principal'], linewidth=5)
        ax2.fill_between(OD_range, 0, safety_factors, alpha=0.2, color=COLORS['principal'])

        # Target SF line
        ax2.axhline(y=3.0, color=COLORS['force'], linewidth=4,
                   linestyle='--', alpha=0.7, label='Target SF = 3.0')

        # Mark optimal
        ax2.plot(optimal_OD, safety_factors[optimal_idx], 'o', markersize=20,
                color='#FFFFFF', markeredgewidth=5,
                markerfacecolor=COLORS['principal'],
                markeredgecolor=COLORS['text'], zorder=10)

        ax2.annotate(f'SF = {safety_factors[optimal_idx]:.2f}',
                    (optimal_OD, safety_factors[optimal_idx]),
                    xytext=(20, -30), textcoords='offset points',
                    fontsize=22, color=COLORS['text'], weight='bold',
                    arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=3))

        ax2.grid(True, alpha=0.3, color=COLORS['grid'], linewidth=2)
        ax2.set_xlabel('Outer Diameter (mm)', fontsize=30,
                      color=COLORS['text'], weight='bold')
        ax2.set_ylabel('Safety Factor', fontsize=30,
                      color=COLORS['text'], weight='bold')
        ax2.set_title('Safety Factor vs Tube Diameter',
                     fontsize=32, color=COLORS['text'], weight='bold', pad=20)
        ax2.legend(fontsize=24)

        for ax in [ax1, ax2]:
            ax.tick_params(colors=COLORS['text'], labelsize=26, width=4, length=10)
            for spine in ax.spines.values():
                spine.set_linewidth(4)
                spine.set_color(COLORS['text'])

        plt.tight_layout()
        return fig


def main():
    """Main analysis function."""
    # Create analysis object
    drone = DroneArmAnalysis()

    # Perform step-by-step analysis
    drone.analyze_bending_from_vertical_load()
    drone.analyze_bending_from_horizontal_load()
    drone.analyze_torsion()
    drone.combine_stresses()
    drone.calculate_principal_stresses()
    drone.apply_failure_criteria()

    # Generate Mohr's circle
    print("\n📊 GENERATING VISUALIZATIONS...")

    fig1 = drone.create_mohrs_circle()
    output_path1 = os.path.join(SCRIPT_DIR, 'lab3_mohrs_circle.svg')
    fig1.savefig(output_path1, format='svg', dpi=300,
                bbox_inches='tight', transparent=True)
    print(f"✅ Mohr's circle saved: {output_path1}")

    # Design optimization
    OD_range, masses, safety_factors, optimal_OD, optimal_mass = drone.design_optimization()

    fig2 = drone.create_optimization_plots(OD_range, masses, safety_factors,
                                          optimal_OD, optimal_mass)
    output_path2 = os.path.join(SCRIPT_DIR, 'lab3_optimization.svg')
    fig2.savefig(output_path2, format='svg', dpi=300,
                bbox_inches='tight', transparent=True)
    print(f"✅ Optimization plots saved: {output_path2}")

    plt.close('all')

    print("\n" + "="*80)
    print("🎯 LAB 3 ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nOutput files:")
    print(f"  1. {output_path1}")
    print(f"  2. {output_path2}")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
