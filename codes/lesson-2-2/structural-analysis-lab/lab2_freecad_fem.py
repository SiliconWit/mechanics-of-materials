#!/usr/bin/env python3
"""
Lab 2: 3D Printer Gantry Rail - FreeCAD FEM Analysis
Structural Analysis Laboratory

This script creates a complete FEM analysis setup in FreeCAD for the gantry rail:
1. Hollow circular tube geometry (OD 30mm, ID 24mm, L = 800mm)
2. Material properties (Aluminum 6061-T6)
3. Boundary conditions (pinned and roller supports)
4. Load application at midspan (critical position)
5. Mesh generation instructions
6. Solver setup

Usage:
  - Run inside FreeCAD: exec(open('lab2_freecad_fem.py').read())
  - Or from command line: freecad lab2_freecad_fem.py

Note: This script sets up the analysis. Students should:
1. Run solver and view results
2. Perform mesh convergence study
3. Compare with analytical solution

Author: SiliconWit Mechanics of Materials Laboratory
"""

import FreeCAD as App
import Part
import ObjectsFem
import FemGui
import Fem
import math
import os

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Problem parameters
L = 800.0   # mm, beam length
OD = 30.0   # mm, outer diameter
t = 3.0     # mm, wall thickness
ID = OD - 2*t  # mm, inner diameter
P = 200.0   # N, print head weight
a_critical = L / 2  # mm, critical load position (midspan)


def create_hollow_tube():
    """Create hollow circular tube geometry."""
    print("Creating hollow circular tube geometry...")

    # Outer cylinder
    outer_cyl = Part.makeCylinder(OD/2, L)

    # Inner cylinder (hollow)
    inner_cyl = Part.makeCylinder(ID/2, L)

    # Subtract to create hollow tube
    tube = outer_cyl.cut(inner_cyl)

    # Rotate to align with X-axis (standard beam orientation)
    tube.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)

    return tube


def create_fem_analysis(doc):
    """Create FEM analysis container and setup."""
    print("\nSetting up FEM analysis...")

    # Create analysis container
    analysis = ObjectsFem.makeAnalysis(doc, "FEM_Analysis")
    print("✓ Analysis container created")

    return analysis


def add_material(doc, analysis):
    """Add Aluminum 6061-T6 material properties."""
    print("\nAdding material properties...")

    # Create material object
    material = ObjectsFem.makeMaterialSolid(doc, "Aluminum_6061_T6")

    # Set material properties
    mat_dict = {
        'Name': 'Aluminum-6061-T6',
        'YoungsModulus': '70000 MPa',  # 70 GPa
        'PoissonRatio': '0.33',
        'Density': '2700 kg/m^3',
        'YieldStrength': '275 MPa',
        'UltimateTensileStrength': '310 MPa'
    }

    material.Material = mat_dict
    analysis.addObject(material)

    print("✓ Material: Aluminum 6061-T6")
    print("  - Young's Modulus: 70 GPa")
    print("  - Poisson's Ratio: 0.33")
    print("  - Yield Strength: 275 MPa")
    print("  - Density: 2.70 g/cm³")

    return material


def add_fixed_constraint_pinned(doc, analysis, tube_obj):
    """Add pinned support constraint at left end (x=0)."""
    print("\nAdding boundary condition: Pinned support (left end)...")

    # Create fixed constraint (approximates pinned for 3D FEM)
    constraint = ObjectsFem.makeConstraintFixed(doc, "PinnedSupport_Left")

    # Get the left end face
    # For cylinder along X-axis, left face is at x=0
    # We need to select this face programmatically

    # Note: In practice, this requires GUI selection
    # Here we provide instructions
    print("  ⚠️  Manual step required:")
    print("     1. Select the circular face at x = 0 (left end)")
    print("     2. Assign to PinnedSupport_Left constraint")
    print("     3. Fix all DOF (X, Y, Z displacements)")

    analysis.addObject(constraint)

    return constraint


def add_displacement_constraint_roller(doc, analysis, tube_obj):
    """Add roller support constraint at right end (x=L)."""
    print("\nAdding boundary condition: Roller support (right end)...")

    # Create displacement constraint
    constraint = ObjectsFem.makeConstraintDisplacement(doc, "RollerSupport_Right")

    print("  ⚠️  Manual step required:")
    print("     1. Select the circular face at x = 800 mm (right end)")
    print("     2. Assign to RollerSupport_Right constraint")
    print("     3. Set displacement:")
    print("        - Y displacement = 0 (vertical support)")
    print("        - Z displacement = 0 (lateral support)")
    print("        - X displacement = FREE (allows thermal expansion)")

    analysis.addObject(constraint)

    return constraint


def add_point_load(doc, analysis, tube_obj):
    """Add point load at midspan (critical position)."""
    print(f"\nAdding point load at critical position (x = {a_critical} mm)...")

    # Create force constraint
    force = ObjectsFem.makeConstraintForce(doc, "PrintHeadLoad")

    # Set force magnitude
    force.Force = P  # N
    force.Reversed = True  # Makes force point downward

    print(f"  • Load magnitude: P = {P} N")
    print(f"  • Direction: Downward (−Z)")
    print(f"  • Position: x = {a_critical} mm (midspan)")

    print("  ⚠️  Manual step required:")
    print("     1. Select a small face/vertex at top of tube at x = 400 mm")
    print("     2. Assign to PrintHeadLoad constraint")
    print("     3. Select an edge parallel to Z-axis for direction reference")

    analysis.addObject(force)

    return force


def add_mesh(doc, analysis, tube_obj):
    """Add mesh object with recommended settings."""
    print("\nAdding mesh settings...")

    # Create mesh using Gmsh
    mesh = ObjectsFem.makeMeshGmsh(doc, "FEM_Mesh")

    # Link mesh to geometry
    mesh.Part = tube_obj

    # Initial mesh settings (coarse)
    mesh.CharacteristicLengthMax = "20.0 mm"
    mesh.CharacteristicLengthMin = "5.0 mm"
    mesh.ElementOrder = "2nd"  # Use quadratic elements for better accuracy

    print("✓ Mesh settings (initial - coarse):")
    print(f"  • Max element size: 20 mm")
    print(f"  • Min element size: 5 mm")
    print(f"  • Element order: 2nd (quadratic)")

    print("\n📊 MESH CONVERGENCE STUDY:")
    print("   Run analysis multiple times with different mesh sizes:")
    print("   1. Coarse:  Max element = 20 mm")
    print("   2. Medium:  Max element = 10 mm")
    print("   3. Fine:    Max element = 5 mm")
    print("   4. V. Fine: Max element = 2.5 mm")
    print("   Compare max stress results to analytical solution")

    analysis.addObject(mesh)

    return mesh


def add_solver(doc, analysis):
    """Add CalculiX solver."""
    print("\nAdding CalculiX solver...")

    # Create solver
    solver = ObjectsFem.makeSolverCalculixCcxTools(doc, "CalculiX_Solver")
    solver.AnalysisType = "static"
    solver.GeometricalNonlinearity = "linear"
    solver.ThermoMechSteadyState = False
    solver.MatrixSolverType = "default"
    solver.IterationsControlParameterTimeUse = False

    analysis.addObject(solver)

    print("✓ Solver: CalculiX (static linear analysis)")
    print("\nTo run analysis:")
    print("  1. Double-click mesh to generate")
    print("  2. Right-click solver → 'Write .inp file'")
    print("  3. Right-click solver → 'Run CalculiX'")
    print("  4. Wait for completion")
    print("  5. Double-click Results to view")

    return solver


def fit_view_to_model():
    """Fit the 3D view to show all objects."""
    try:
        import FreeCADGui as Gui

        # Get active view
        view = Gui.ActiveDocument.ActiveView

        # Fit all objects in view
        view.fitAll()

        # Set to isometric view
        view.viewIsometric()

        print("\n✓ View fitted and set to isometric")
        return True
    except Exception as e:
        print(f"\n⚠️  Could not auto-fit view: {e}")
        print("   (Manual view adjustment may be needed)")
        return False


def create_document():
    """Create complete FreeCAD FEM document."""
    print("="*70)
    print("LAB 2: GANTRY RAIL - FREECAD FEM ANALYSIS SETUP")
    print("="*70)

    # Create new document
    doc_name = "Lab2_GantryRail_FEM"
    if App.ActiveDocument:
        if App.ActiveDocument.Name == doc_name:
            App.closeDocument(doc_name)

    doc = App.newDocument(doc_name)
    print(f"\nCreated document: {doc_name}")

    # Create geometry
    tube = create_hollow_tube()
    tube_obj = doc.addObject("Part::Feature", "GantryTube")
    tube_obj.Shape = tube
    tube_obj.ViewObject.ShapeColor = (0.18, 0.48, 0.56)  # Teal
    print("✓ Hollow tube geometry created")

    # Create FEM analysis
    analysis = create_fem_analysis(doc)

    # Add material
    material = add_material(doc, analysis)

    # Add boundary conditions
    pinned = add_fixed_constraint_pinned(doc, analysis, tube_obj)
    roller = add_displacement_constraint_roller(doc, analysis, tube_obj)

    # Add load
    load = add_point_load(doc, analysis, tube_obj)

    # Add mesh (pass tube_obj to link geometry)
    mesh = add_mesh(doc, analysis, tube_obj)

    # Add solver
    solver = add_solver(doc, analysis)

    # Recompute
    doc.recompute()

    # Fit view to model
    fit_view_to_model()

    print("\n" + "="*70)
    print("✅ FEM ANALYSIS SETUP COMPLETE!")
    print("="*70)

    print("\n📋 NEXT STEPS:")
    print("1. Complete manual face selections for constraints and load")
    print("2. Generate mesh (double-click FEM_Mesh)")
    print("3. Run solver (right-click CalculiX_Solver)")
    print("4. View results (double-click Results)")
    print("5. Record maximum von Mises stress value")
    print("6. Compare with analytical: σ_analytical ≈ 10.0 MPa")
    print("7. Repeat with finer meshes for convergence study")

    print("\n💡 EXPECTED RESULTS:")
    print("   • Maximum stress location: Midspan (x = 400 mm)")
    print("   • Position in cross-section: Top/bottom outer fibers")
    print("   • FEM should match analytical within 5% (fine mesh)")

    print("\n" + "="*70)

    return doc


def main():
    """Main execution function."""
    doc = create_document()

    print("\nDocument ready for FEM analysis!")
    print("Save document before running solver.")


if __name__ == "__main__" or __name__ == "__console__":
    main()
