#!/usr/bin/env python3
"""
Lab 3: Drone Arm - FreeCAD FEM with Combined Loading
Structural Analysis Laboratory

This script creates a complete FEM analysis setup for drone arm with:
1. Hollow circular tube geometry (OD 16mm, ID 12mm, L = 200mm)
2. Material properties (Carbon Fiber Composite)
3. Fixed support at left end
4. Combined loading: vertical thrust + horizontal drag + torsion
5. Solver setup for combined stress analysis

Usage:
  - Run inside FreeCAD: exec(open('lab3_freecad_combined_fem.py').read())

Author: SiliconWit Mechanics of Materials Laboratory
"""

import FreeCAD as App
import Part
import ObjectsFem
import math
import os

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Problem parameters
L = 200.0           # mm, arm length
OD = 16.0           # mm, outer diameter
ID = 12.0           # mm, inner diameter
P_vertical = 30.0   # N, vertical thrust
F_horizontal = 5.0  # N, horizontal drag
T_torque = 1000.0   # N·mm, gyroscopic torque


def create_hollow_tube():
    """Create hollow circular tube (drone arm)."""
    print("Creating drone arm geometry...")

    # Outer cylinder
    outer_cyl = Part.makeCylinder(OD/2, L)

    # Inner cylinder
    inner_cyl = Part.makeCylinder(ID/2, L)

    # Hollow tube
    tube = outer_cyl.cut(inner_cyl)

    # Rotate to align with X-axis
    tube.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)

    return tube


def create_fem_analysis(doc):
    """Create FEM analysis container."""
    print("\nSetting up FEM analysis...")
    analysis = ObjectsFem.makeAnalysis(doc, "DroneArm_CombinedLoading")
    return analysis


def add_carbon_fiber_material(doc, analysis):
    """Add carbon fiber composite material."""
    print("\nAdding carbon fiber composite material...")

    material = ObjectsFem.makeMaterialSolid(doc, "CarbonFiber")

    # Equivalent isotropic properties for initial analysis
    mat_dict = {
        'Name': 'Carbon-Fiber-Composite',
        'YoungsModulus': '70000 MPa',  # Longitudinal direction
        'PoissonRatio': '0.10',        # Orthotropic, using equivalent
        'Density': '1600 kg/m^3',      # 1.6 g/cm³
        'YieldStrength': '500 MPa',    # Compressive (conservative)
        'UltimateTensileStrength': '600 MPa'
    }

    material.Material = mat_dict
    analysis.addObject(material)

    print("✓ Material: Carbon Fiber Composite")
    print("  - E_longitudinal: 70 GPa (equivalent isotropic)")
    print("  - ν: 0.10")
    print("  - Tensile strength: 600 MPa")
    print("  - Compressive strength: 500 MPa")

    return material


def add_fixed_support(doc, analysis):
    """Add fixed support at left end (drone body connection)."""
    print("\nAdding fixed support (left end - drone body)...")

    constraint = ObjectsFem.makeConstraintFixed(doc, "FixedSupport_DroneBody")

    print("  ⚠️  Manual step:")
    print("     1. Select circular face at x = 0 (left end)")
    print("     2. Assign to FixedSupport_DroneBody")
    print("     3. Fix all DOF (cantilever)")

    analysis.addObject(constraint)
    return constraint


def add_vertical_thrust(doc, analysis):
    """Add vertical thrust force from motor."""
    print(f"\nAdding vertical thrust load (motor)...")

    force = ObjectsFem.makeConstraintForce(doc, "VerticalThrust")
    force.Force = P_vertical
    force.Direction = (App.Vector(0, 0, -1))  # Downward

    print(f"  • Magnitude: {P_vertical} N")
    print(f"  • Direction: −Z (downward)")
    print(f"  • Location: Right end face center (x = {L} mm)")

    print("  ⚠️  Manual step:")
    print("     1. Select small face/vertex at top of tube at x = 200 mm")
    print("     2. Assign to VerticalThrust constraint")

    analysis.addObject(force)
    return force


def add_horizontal_drag(doc, analysis):
    """Add horizontal drag force."""
    print(f"\nAdding horizontal drag load (aerodynamic)...")

    force = ObjectsFem.makeConstraintForce(doc, "HorizontalDrag")
    force.Force = F_horizontal
    force.Direction = (App.Vector(0, 1, 0))  # Horizontal (Y direction)

    print(f"  • Magnitude: {F_horizontal} N")
    print(f"  • Direction: +Y (horizontal)")
    print(f"  • Location: Right end face (x = {L} mm)")

    print("  ⚠️  Manual step:")
    print("     1. Select small face at side of tube at x = 200 mm")
    print("     2. Assign to HorizontalDrag constraint")

    analysis.addObject(force)
    return force


def add_torsion_couple(doc, analysis):
    """Add torsion using force couple method."""
    print(f"\nAdding torsional load (gyroscopic effect)...")
    print(f"  Using force couple method (FreeCAD workaround):")

    # Torque T = F × d, choose convenient arm length
    moment_arm = 8.0  # mm (OD = 16mm, so diameter)
    F_couple = T_torque / moment_arm

    print(f"  • Torque: T = {T_torque} N·mm = {T_torque/1000:.1f} N·m")
    print(f"  • Moment arm: d = {moment_arm} mm")
    print(f"  • Couple force: F = T/d = {F_couple:.1f} N")

    # Positive force
    force1 = ObjectsFem.makeConstraintForce(doc, "TorsionCouple_Plus")
    force1.Force = F_couple
    force1.Direction = (App.Vector(0, 1, 0))  # +Y direction

    # Negative force
    force2 = ObjectsFem.makeConstraintForce(doc, "TorsionCouple_Minus")
    force2.Force = F_couple
    force2.Direction = (App.Vector(0, -1, 0))  # −Y direction

    print("  ⚠️  Manual steps:")
    print("     1. Select vertex at TOP of tube at x = 200 mm")
    print("        Assign to TorsionCouple_Plus (+Y, creates CCW torque)")
    print("     2. Select vertex at BOTTOM of tube at x = 200 mm")
    print("        Assign to TorsionCouple_Minus (−Y)")
    print("     3. These create a couple producing the required torque")

    analysis.addObject(force1)
    analysis.addObject(force2)

    return force1, force2


def add_mesh(doc, analysis):
    """Add mesh with appropriate settings for thin-walled tube."""
    print("\nAdding mesh settings...")

    mesh = ObjectsFem.makeMeshGmsh(doc, "FEM_Mesh")

    # Fine mesh for accurate stress capture
    mesh.CharacteristicLengthMax = "5.0 mm"
    mesh.CharacteristicLengthMin = "1.0 mm"
    mesh.ElementOrder = "2nd"  # Quadratic elements

    print("✓ Mesh settings:")
    print(f"  • Max element: 5 mm (fine mesh)")
    print(f"  • Min element: 1 mm")
    print(f"  • Element order: 2nd (quadratic)")
    print("\n  💡 For thin-walled tube, use fine mesh to capture:")
    print("     - Stress gradients through wall thickness")
    print("     - Combined stress effects")
    print("     - Torsional shear distribution")

    analysis.addObject(mesh)
    return mesh


def add_solver(doc, analysis):
    """Add CalculiX solver."""
    print("\nAdding CalculiX solver...")

    solver = ObjectsFem.makeSolverCalculixCcxTools(doc, "CalculiX_Solver")
    solver.AnalysisType = "static"
    solver.GeometricalNonlinearity = "linear"
    solver.ThermoMechSteadyState = False

    analysis.addObject(solver)

    print("✓ Solver: CalculiX (static linear)")
    print("\nTo run analysis:")
    print("  1. Generate mesh")
    print("  2. Assign all manual constraints")
    print("  3. Write .inp file")
    print("  4. Run CalculiX")
    print("  5. View results:")
    print("     - Von Mises stress")
    print("     - Principal stresses")
    print("     - Compare with analytical")

    return solver


def create_document():
    """Create complete FEM document."""
    print("="*70)
    print("LAB 3: DRONE ARM - COMBINED LOADING FEM SETUP")
    print("="*70)

    # Create document
    doc_name = "Lab3_DroneArm_CombinedFEM"
    if App.ActiveDocument:
        if App.ActiveDocument.Name == doc_name:
            App.closeDocument(doc_name)

    doc = App.newDocument(doc_name)
    print(f"\nCreated document: {doc_name}")

    # Create geometry
    tube = create_hollow_tube()
    tube_obj = doc.addObject("Part::Feature", "DroneArm")
    tube_obj.Shape = tube
    tube_obj.ViewObject.ShapeColor = (0.18, 0.48, 0.56)
    print("✓ Drone arm geometry created")

    # FEM analysis
    analysis = create_fem_analysis(doc)
    material = add_carbon_fiber_material(doc, analysis)
    fixed = add_fixed_support(doc, analysis)

    # All three loading components
    thrust = add_vertical_thrust(doc, analysis)
    drag = add_horizontal_drag(doc, analysis)
    torque_plus, torque_minus = add_torsion_couple(doc, analysis)

    # Mesh and solver
    mesh = add_mesh(doc, analysis)
    solver = add_solver(doc, analysis)

    # Recompute
    doc.recompute()

    print("\n" + "="*70)
    print("✅ COMBINED LOADING FEM SETUP COMPLETE!")
    print("="*70)

    print("\n📋 ANALYSIS SUMMARY:")
    print("  Loading components:")
    print(f"    1. Vertical thrust: {P_vertical} N (bending in XZ plane)")
    print(f"    2. Horizontal drag: {F_horizontal} N (bending in XY plane)")
    print(f"    3. Gyroscopic torque: {T_torque/1000:.1f} N·m (torsion about X)")

    print("\n  Expected stress state at fixed end:")
    print("    • Combined bending stress: ~25 MPa (normal)")
    print("    • Torsional shear stress: ~3.5 MPa")
    print("    • Maximum principal: ~26 MPa (analytical)")
    print("    • Von Mises stress: ~25 MPa (analytical)")

    print("\n  Critical location:")
    print("    • Fixed end (x = 0)")
    print("    • Outer surface at ~45° (both bendings contribute)")

    print("\n💡 COMPARISON CHECKLIST:")
    print("  □ Compare FEM von Mises stress with analytical")
    print("  □ Check principal stress directions")
    print("  □ Verify stress is maximum at fixed end")
    print("  □ Confirm outer surface has max stress")
    print("  □ Validate against hand calculations")

    print("\n" + "="*70)

    return doc


def main():
    """Main execution."""
    doc = create_document()
    print("\nDocument ready!")
    print("Complete manual constraint assignments, then run FEM.")


if __name__ == "__main__" or __name__ == "__console__":
    main()
