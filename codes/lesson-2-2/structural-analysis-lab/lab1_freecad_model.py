#!/usr/bin/env python3
"""
Lab 1: Robotic Arm - FreeCAD 3D Model Generation
Structural Analysis Laboratory

This script creates a complete 3D model of the robotic arm cantilever beam
using FreeCAD Python API. It generates:
1. Beam geometry (60mm × 20mm × 500mm rectangular cross-section)
2. Fixed support visualization
3. Load arrows and annotations
4. Material properties (Aluminum 6061-T6)
5. Export to GLB format for web visualization

Usage:
  - Run inside FreeCAD: exec(open('lab1_freecad_model.py').read())
  - Or from command line: freecad lab1_freecad_model.py

Author: SiliconWit Mechanics of Materials Laboratory
"""

import FreeCAD as App
import Part
import Mesh
import math
import os

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Problem parameters
L = 500.0  # mm, beam length
b = 60.0   # mm, width
h = 20.0   # mm, height
P = 500.0  # N, point load


def create_beam():
    """Create rectangular beam geometry."""
    print("Creating beam geometry...")

    # Create rectangular cross-section centered on origin
    beam_box = Part.makeBox(L, b, h)

    # Move so fixed end is at origin and beam extends in +X direction
    # Center the beam vertically and horizontally
    beam_box.translate(App.Vector(0, -b/2, -h/2))

    return beam_box


def create_fixed_support_visual():
    """Create visual representation of fixed support (wall)."""
    print("Creating fixed support visualization...")

    # Wall dimensions
    wall_thickness = 30.0  # mm
    wall_width = b + 40.0   # mm (wider than beam)
    wall_height = h + 40.0  # mm (taller than beam)

    # Create wall box
    wall = Part.makeBox(wall_thickness, wall_width, wall_height)

    # Position wall at left end of beam
    wall.translate(App.Vector(-wall_thickness, -wall_width/2, -wall_height/2))

    return wall


def create_load_arrow(position, magnitude, direction='down'):
    """Create arrow representing applied load."""
    print(f"Creating load arrow at x = {position} mm...")

    arrow_length = 80.0  # mm
    arrow_radius = 8.0   # mm
    head_radius = 15.0   # mm
    head_length = 25.0   # mm

    # Arrow shaft (cylinder)
    shaft = Part.makeCylinder(arrow_radius, arrow_length)

    # Arrow head (cone)
    head = Part.makeCone(head_radius, 0, head_length)

    if direction == 'down':
        # Position above beam, pointing down
        y_pos = 0
        z_pos = h/2  # Top of beam

        # Rotate shaft to point downward (180 degrees around Y axis)
        shaft.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 180)

        # Rotate head to point downward (180 degrees around Y axis)
        head.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 180)

        # Position shaft above beam
        shaft.translate(App.Vector(position, y_pos, z_pos + arrow_length))

        # Position head at bottom of shaft (pointing down at beam)
        head.translate(App.Vector(position, y_pos, z_pos))

    # Fuse shaft and head into single solid
    arrow = shaft.fuse(head)

    return arrow


def add_text_labels(doc):
    """Add text labels for loads and dimensions."""
    try:
        import Draft

        # Define colors matching respective components
        bright_teal = (0.3, 1.0, 1.0)  # Brighter teal for beam edge and text
        brighter_orange = (1.0, 0.85, 0.65)  # Brighter orange for load arrow edge and text
        orangeish_green = (0.9, 1.0, 0.4)  # Orangeish green for fixed support edge and text

        # Label for load - larger and more visible (using brighter arrow edge color)
        load_label_pos = App.Vector(L, -30, h/2 + 120)
        load_text = Draft.make_text([f"P = {P} N"], load_label_pos)
        load_text.Label = "Label_Load_P500N"  # Descriptive name in tree
        load_text.ViewObject.FontSize = 28.0  # Larger font
        load_text.ViewObject.TextColor = brighter_orange

        # Try to add outline for better visibility on dark backgrounds
        try:
            load_text.ViewObject.LineColor = brighter_orange
            load_text.ViewObject.LineWidth = 2.0
        except:
            pass

        # Label for beam length - larger and more visible (using brighter beam edge color)
        length_label_pos = App.Vector(L/3, -45, -h/2 - 10)
        length_text = Draft.make_text([f"L = {L} mm"], length_label_pos)
        length_text.Label = "Label_Length_500mm"  # Descriptive name in tree
        length_text.ViewObject.FontSize = 24.0  # Larger font
        length_text.ViewObject.TextColor = orangeish_green

        try:
            length_text.ViewObject.LineColor = orangeish_green
            length_text.ViewObject.LineWidth = 2.0
        except:
            pass

        # Label for fixed support - rotated 90 degrees CCW about Z axis (using fixed support edge color)
        support_label_pos = App.Vector(-70, 0, 0)  # Lowered to beam center height
        support_text = Draft.make_text(["Fixed"], support_label_pos)
        support_text.Label = "Label_FixedSupport"  # Descriptive name in tree
        support_text.ViewObject.FontSize = 22.0  # Larger font
        support_text.ViewObject.TextColor = bright_teal

        # Rotate text 90 degrees counter-clockwise about Z axis
        support_text.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), 90)

        try:
            support_text.ViewObject.LineColor = bright_teal
            support_text.ViewObject.LineWidth = 2.0
        except:
            pass

        print("✓ Labels added (color-coded to match components, 'Fixed' rotated 90° CCW)")
        return True
    except Exception as e:
        print(f"⚠️  Could not add labels (Draft workbench): {e}")
        print("   (Labels are optional - model is still complete)")
        return False


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

        print("✓ View fitted and set to isometric")
        return True
    except Exception as e:
        print(f"⚠️  Could not auto-fit view: {e}")
        print("   (Manual view adjustment may be needed)")
        return False


def create_document():
    """Create complete FreeCAD document with all components."""
    print("="*70)
    print("LAB 1: ROBOTIC ARM - FREECAD 3D MODEL GENERATION")
    print("="*70)

    # Create new document (close existing one if it exists)
    doc_name = "Lab1_RoboticArm"

    # Close the document if it already exists (regardless of whether it's active)
    if doc_name in [doc.Name for doc in App.listDocuments().values()]:
        App.closeDocument(doc_name)
        print(f"Closed existing document: {doc_name}")

    doc = App.newDocument(doc_name)
    print(f"\nCreated fresh document: {doc_name}")

    # Define edge colors for all objects
    bright_teal = (0.3, 1.0, 1.0)  # Brighter teal for beam
    brighter_orange = (1.0, 0.85, 0.65)  # Brighter orange for load arrow
    orangeish_green = (0.9, 1.0, 0.4)  # Orangeish green for fixed support

    # Create beam with brighter teal edges
    beam = create_beam()
    beam_obj = doc.addObject("Part::Feature", "Beam")
    beam_obj.Shape = beam
    beam_obj.ViewObject.ShapeColor = (0.18, 0.48, 0.56)  # Teal color
    beam_obj.ViewObject.LineColor = orangeish_green  # Brighter teal edges
    beam_obj.ViewObject.LineWidth = 3.0  # Thicker edges for visibility
    beam_obj.Label = "Beam_500x60x20mm"  # Descriptive name in tree
    print("✓ Beam created (with brighter teal edges)")

    # Create fixed support with orangeish green edges
    wall = create_fixed_support_visual()
    wall_obj = doc.addObject("Part::Feature", "FixedSupport")
    wall_obj.Shape = wall
    wall_obj.ViewObject.ShapeColor = (0.25, 0.27, 0.30)  # Darker gray color for better contrast
    wall_obj.ViewObject.LineColor = bright_teal  # Orangeish green edges (matches "Fixed" text)
    wall_obj.ViewObject.LineWidth = 3.0  # Thicker edges
    wall_obj.ViewObject.Transparency = 30
    wall_obj.Label = "Support_Fixed_LeftEnd"  # Descriptive name in tree
    print(f"✓ Fixed support created (darker gray faces with orangeish green edges: {orangeish_green})")

    # Create load arrow at free end with same orange as faces for edges
    load_arrow = create_load_arrow(L, P, 'down')
    load_obj = doc.addObject("Part::Feature", "LoadArrow")
    load_obj.Shape = load_arrow
    arrow_orange = (1.0, 0.55, 0.21)  # Orange color for both faces and edges
    load_obj.ViewObject.ShapeColor = arrow_orange
    load_obj.ViewObject.LineColor = arrow_orange  # Same orange as faces
    load_obj.ViewObject.LineWidth = 3.0  # Thicker edges
    load_obj.Label = f"Arrow_Load_P{int(P)}N_Downward"  # Descriptive name in tree
    print("✓ Load arrow created (with orange edges matching faces)")

    # Recompute document
    doc.recompute()

    print("\n✓ Model creation complete!")
    print(f"\nModel components:")
    print(f"  • Beam: {L} mm × {b} mm × {h} mm (teal with orangeish green edges)")
    print(f"  • Fixed support at x = 0 (darker gray with bright teal edges)")
    print(f"  • Point load P = {P} N at x = {L} mm (orange faces and edges)")

    print(f"\nTree view labels:")
    print(f"  • Beam_500x60x20mm")
    print(f"  • Support_Fixed_LeftEnd")
    print(f"  • Arrow_Load_P{int(P)}N_Downward")

    # Add text labels (optional, may fail if Draft not available)
    add_text_labels(doc)

    # Fit view to model (if GUI is available)
    fit_view_to_model()

    print(f"\n💡 Styling notes:")
    print(f"  • Beam: Teal faces (0.18, 0.48, 0.56) + Orangeish green edges (0.9, 1.0, 0.4)")
    print(f"  • Fixed support: Darker gray faces (0.25, 0.27, 0.30) + Bright teal edges (0.3, 1.0, 1.0)")
    print(f"  • Load arrow: Orange faces and edges (1.0, 0.55, 0.21)")
    print(f"  • Text labels:")
    print(f"    - 'P = 500 N': Brighter orange (1.0, 0.85, 0.65)")
    print(f"    - 'L = 500 mm': Orangeish green (0.9, 1.0, 0.4)")
    print(f"    - 'Fixed': Bright teal (0.3, 1.0, 1.0), rotated 90° CCW")
    print(f"  • All components have distinct colors for clear visual differentiation")
    print(f"  • Descriptive tree names for easy identification")

    return doc


def export_model(doc, filename="lab1_robotic_arm_model"):
    """Export model to various formats."""
    print(f"\n📦 EXPORTING MODEL...")

    # Get all shapes
    shapes = []
    for obj in doc.Objects:
        if hasattr(obj, 'Shape'):
            shapes.append(obj.Shape)

    # Create compound of all shapes
    compound = Part.makeCompound(shapes)

    # Export to STEP (for CAD interoperability)
    step_path = os.path.join(SCRIPT_DIR, filename + ".step")
    compound.exportStep(step_path)
    print(f"✓ STEP file exported: {step_path}")

    # Export to STL (for 3D printing/meshing)
    stl_path = os.path.join(SCRIPT_DIR, filename + ".stl")
    Mesh.export([obj for obj in doc.Objects if hasattr(obj, 'Shape')], stl_path)
    print(f"✓ STL file exported: {stl_path}")

    # Export to GLB (for web visualization)
    try:
        import importWebGL
        glb_path = os.path.join(SCRIPT_DIR, filename + ".glb")

        # Get all visible objects
        objs = [obj for obj in doc.Objects if hasattr(obj, 'Shape') and obj.ViewObject.Visibility]

        # Export to GLB format
        importWebGL.export(objs, glb_path)
        print(f"✓ GLB file exported: {glb_path}")
        print(f"  → Verify at: https://siliconwit.com/product-development/3d-model-viewer/")
    except Exception as e:
        print(f"⚠️  GLB export failed: {e}")
        print(f"\n   Manual export steps:")
        print(f"   1. Select all objects (Ctrl+A)")
        print(f"   2. File → Export → Select 'glTF 2.0 (*.glb *.gltf)'")
        print(f"   3. Change extension from .gltf to .glb")
        print(f"   4. Save as: {filename}.glb")
        print(f"   5. Verify at: https://siliconwit.com/product-development/3d-model-viewer/")

    print(f"\n✅ Export complete!")


def add_material_properties(doc):
    """Add material property annotations (for FEM later)."""
    print("\n🔧 MATERIAL PROPERTIES:")
    print("  • Material: Aluminum Alloy 6061-T6")
    print("  • Yield Strength: 275 MPa")
    print("  • Young's Modulus: 69 GPa")
    print("  • Poisson's Ratio: 0.33")
    print("  • Density: 2.70 g/cm³")

    # Note: Material properties would be assigned in FEM workbench
    # This is informational for Lab 1


def main():
    """Main execution function."""
    # Create model
    doc = create_document()

    # Add material info
    add_material_properties(doc)

    # Export files
    export_model(doc, "lab1_robotic_arm_model")

    print("\n" + "="*70)
    print("🎯 LAB 1 FREECAD MODEL GENERATION COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Open the document in FreeCAD GUI to view the 3D model")
    print("2. Rotate to isometric view and take screenshots")
    print("3. Export to GLB format for web visualization")
    print("4. Create technical drawing using TechDraw workbench")
    print("\n" + "="*70)


if __name__ == "__main__" or __name__ == "__console__":
    main()
