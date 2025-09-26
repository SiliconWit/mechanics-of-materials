#!/usr/bin/env python3
"""
Pantograph Arm Structural Analysis
=====================================

This script calculates the structural response of a cantilever pantograph arm
for electric train/bus applications and generates JSON data for visualizations.

Application: Pantograph Arm of Electric Bus (Electromechanical)
System: Cantilever beam with concentrated end load
"""

import json
import numpy as np
import math
from pathlib import Path

class PantographAnalysis:
    """Cantilever beam analysis for pantograph arm"""

    def __init__(self):
        # Material and geometric properties
        self.L = 1200  # Length in mm
        self.P = 800   # Applied load in N (contact force)
        self.OD = 50   # Outer diameter in mm
        self.t = 4     # Wall thickness in mm
        self.I = 2.45e6  # Second moment of area in mm⁴
        self.c = 25    # Distance to extreme fiber in mm
        self.sigma_yield = 250  # Yield strength in MPa
        self.SF_required = 3.0  # Required safety factor

        # Calculated properties
        self.S = self.I / self.c  # Section modulus

    def calculate_reactions(self):
        """Calculate support reaction forces and moments"""
        # For cantilever with end load
        R_A = self.P  # Vertical reaction at fixed support
        M_A = self.P * self.L  # Reaction moment at fixed support

        return {
            'vertical_reaction': R_A,  # N
            'moment_reaction': M_A     # N⋅mm
        }

    def calculate_shear_force(self, x_values):
        """Calculate shear force at given positions along beam"""
        # For cantilever with end load, shear is constant
        shear_values = [-self.P] * len(x_values)  # Negative indicates downward internal force

        return {
            'positions': x_values.tolist(),
            'shear_forces': shear_values,
            'max_shear': abs(self.P),
            'location_max': 'Throughout beam length'
        }

    def calculate_bending_moment(self, x_values):
        """Calculate bending moment at given positions along beam"""
        # For cantilever: M(x) = -P * x (from free end)
        moment_values = [-self.P * x for x in x_values]

        return {
            'positions': x_values.tolist(),
            'moments': moment_values,
            'max_moment': abs(self.P * self.L),  # Maximum at fixed support
            'location_max': f'Fixed support (x = {self.L} mm)'
        }

    def calculate_bending_stress(self):
        """Calculate maximum bending stress"""
        M_max = self.P * self.L  # Maximum moment magnitude

        # Using flexural formula
        sigma_max = (M_max * self.c) / self.I

        # Alternative using section modulus
        sigma_max_alt = M_max / self.S

        return {
            'max_moment': M_max,           # N⋅mm
            'max_stress': sigma_max,       # MPa
            'max_stress_alt': sigma_max_alt,  # MPa (verification)
            'location': 'Fixed support, extreme fibers',
            'tensile_stress': sigma_max,   # Bottom fiber
            'compressive_stress': -sigma_max  # Top fiber
        }

    def calculate_safety_factor(self):
        """Calculate safety factor assessment"""
        stress_result = self.calculate_bending_stress()
        sigma_max = stress_result['max_stress']

        SF_actual = self.sigma_yield / sigma_max

        return {
            'actual_safety_factor': SF_actual,
            'required_safety_factor': self.SF_required,
            'design_adequate': SF_actual >= self.SF_required,
            'over_design_factor': SF_actual / self.SF_required,
            'yield_strength': self.sigma_yield,
            'working_stress': sigma_max
        }

    def generate_chart_data(self, num_points=50):
        """Generate data for shear and moment diagrams"""
        x_values = np.linspace(0, self.L, num_points)

        # Shear force data
        shear_data = self.calculate_shear_force(x_values)

        # Bending moment data
        moment_data = self.calculate_bending_moment(x_values)

        return {
            'shear': shear_data,
            'moment': moment_data,
            'beam_length': self.L,
            'applied_load': self.P
        }

    def comprehensive_analysis(self):
        """Perform complete structural analysis"""
        # Step 1: Support reactions
        reactions = self.calculate_reactions()

        # Step 2: Shear and moment analysis
        x_analysis = np.linspace(0, self.L, 50)
        shear_analysis = self.calculate_shear_force(x_analysis)
        moment_analysis = self.calculate_bending_moment(x_analysis)

        # Step 3: Maximum bending stress
        stress_analysis = self.calculate_bending_stress()

        # Step 4: Safety factor assessment
        safety_analysis = self.calculate_safety_factor()

        # Chart data generation
        chart_data = self.generate_chart_data()

        return {
            'system_parameters': {
                'length': self.L,
                'applied_load': self.P,
                'outer_diameter': self.OD,
                'wall_thickness': self.t,
                'moment_of_inertia': self.I,
                'section_modulus': self.S,
                'yield_strength': self.sigma_yield
            },
            'support_reactions': reactions,
            'shear_analysis': shear_analysis,
            'moment_analysis': moment_analysis,
            'stress_analysis': stress_analysis,
            'safety_analysis': safety_analysis,
            'chart_data': chart_data
        }

    def verify_calculations(self):
        """Verify key calculations match MDX content"""
        results = self.comprehensive_analysis()

        # Verification against expected values from MDX
        expected_max_moment = 960000  # N⋅mm
        expected_max_stress = 9.80    # MPa
        expected_safety_factor = 25.5

        calculated_moment = results['moment_analysis']['max_moment']
        calculated_stress = results['stress_analysis']['max_stress']
        calculated_sf = results['safety_analysis']['actual_safety_factor']

        verification = {
            'moment_check': {
                'expected': expected_max_moment,
                'calculated': calculated_moment,
                'match': abs(calculated_moment - expected_max_moment) < 1e-6
            },
            'stress_check': {
                'expected': expected_max_stress,
                'calculated': calculated_stress,
                'match': abs(calculated_stress - expected_max_stress) < 0.01
            },
            'safety_factor_check': {
                'expected': expected_safety_factor,
                'calculated': calculated_sf,
                'match': abs(calculated_sf - expected_safety_factor) < 0.1
            }
        }

        return verification

def main():
    """Main execution function"""
    # Initialize analysis
    pantograph = PantographAnalysis()

    # Perform comprehensive analysis
    results = pantograph.comprehensive_analysis()

    # Verify calculations
    verification = pantograph.verify_calculations()

    # Create output directory
    output_dir = Path(__file__).parent.parent.parent.parent.parent.parent / 'public' / 'education' / 'mechanics-of-materials' / 'components' / 'lesson-2-2'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save comprehensive results
    results_file = output_dir / 'pantograph_analysis_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Save chart-specific data
    shear_data_file = output_dir / 'pantograph_shear_data.json'
    with open(shear_data_file, 'w') as f:
        json.dump(results['chart_data']['shear'], f, indent=2)

    moment_data_file = output_dir / 'pantograph_moment_data.json'
    with open(moment_data_file, 'w') as f:
        json.dump(results['chart_data']['moment'], f, indent=2)

    # Save verification results
    verification_file = output_dir / 'calculation_verification.json'
    with open(verification_file, 'w') as f:
        json.dump(verification, f, indent=2)

    # Print summary
    print("Pantograph Arm Structural Analysis")
    print("=" * 40)
    print(f"Maximum Moment: {results['moment_analysis']['max_moment']:.0f} N⋅mm")
    print(f"Maximum Stress: {results['stress_analysis']['max_stress']:.2f} MPa")
    print(f"Safety Factor: {results['safety_analysis']['actual_safety_factor']:.1f}")
    print(f"Design Adequate: {results['safety_analysis']['design_adequate']}")
    print("\nVerification Results:")
    for check, data in verification.items():
        print(f"{check}: {'✓' if data['match'] else '✗'} (Expected: {data['expected']}, Got: {data['calculated']:.3f})")

    print(f"\nJSON files generated in: {output_dir}")

if __name__ == "__main__":
    main()