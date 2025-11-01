#!/usr/bin/env python3
"""
Lab 2: 3D Printer Gantry Rail - FreeCAD 3D Model Generation
Structural Analysis Laboratory

This script creates a complete 3D model of the gantry rail beam
using FreeCAD Python API. It generates:
1. Hollow circular tube geometry (OD=30mm, ID=24mm, L=800mm)
2. Pinned and roller support visualizations
3. Load arrow at midspan
4. Text labels and annotations
5. Export to GLB format for web visualization

Usage:
  - Run inside FreeCAD: exec(open('lab2_freecad_model.py').read())
  - Or from command line: freecad lab2_freecad_model.py

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
L = 800.0   # mm, beam length
OD = 30.0   # mm, outer diameter
ID = 24.0   # mm, inner diameter (OD - 2×3mm wall)
t = 3.0     # mm, wall thickness
P = 200.0   # N, print head weight


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
    # Cylinder is created along Z-axis, rotate 90° around Y to align with X
    tube.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)

    return tube


def create_pinned_support_visual():
    """Create visual representation of pinned support (triangle)."""
    print("Creating pinned support visualization (left end)...")

    # Triangle support dimensions
    base_width = 60.0   # mm
    height = 50.0       # mm
    thickness = 40.0    # mm (depth in Y direction)

    # Create triangular prism using vertices
    # Triangle in XZ plane, extruded in Y direction
    v1 = App.Vector(0, -thickness/2, -OD/2 - height)        # Bottom left
    v2 = App.Vector(0, -thickness/2, -OD/2)                 # Top left (at beam)
    v3 = App.Vector(-base_width/2, -thickness/2, -OD/2 - height)  # Bottom right

    # Create front face (triangle)
    line1 = Part.LineSegment(v1, v2)
    line2 = Part.LineSegment(v2, v3)
    line3 = Part.LineSegment(v3, v1)

    # Create wire from edges
    wire = Part.Wire([line1.toShape(), line2.toShape(), line3.toShape()])

    # Create face from wire
    face = Part.Face(wire)

    # Extrude in Y direction to create solid
    triangle = face.extrude(App.Vector(0, thickness, 0))

    return triangle


def create_roller_support_visual():
    """Create visual representation of roller support (triangle + cylinders)."""
    print("Creating roller support visualization (right end)...")

    # Triangle support (same as pinned)
    base_width = 60.0   # mm
    height = 50.0       # mm
    thickness = 40.0    # mm

    # Create triangular prism at right end
    v1 = App.Vector(L, -thickness/2, -OD/2 - height)
    v2 = App.Vector(L, -thickness/2, -OD/2)
    v3 = App.Vector(L + base_width/2, -thickness/2, -OD/2 - height)

    line1 = Part.LineSegment(v1, v2)
    line2 = Part.LineSegment(v2, v3)
    line3 = Part.LineSegment(v3, v1)

    wire = Part.Wire([line1.toShape(), line2.toShape(), line3.toShape()])
    face = Part.Face(wire)
    triangle = face.extrude(App.Vector(0, thickness, 0))

    # Add small rollers (cylinders) underneath to indicate roller support
    roller_radius = 8.0  # mm
    roller_length = 50.0  # mm

    # Two rollers side by side
    roller1 = Part.makeCylinder(roller_radius, roller_length)
    roller1.rotate(App.Vector(0, 25, 25), App.Vector(1, 0, 0), 90)  # Align with Y-axis
    roller1.translate(App.Vector(L - 0, -roller_length/2, -OD/2 - height - roller_radius))

    roller2 = Part.makeCylinder(roller_radius, roller_length)
    roller2.rotate(App.Vector(0, 25, 25), App.Vector(1, 0, 0), 90)
    roller2.translate(App.Vector(L + 30, -roller_length/2, -OD/2 - height - roller_radius))

    # Fuse triangle and rollers
    support = triangle.fuse([roller1, roller2])

    return support


def create_load_arrow(position, magnitude, direction='down'):
    """Create arrow representing applied load."""
    print(f"Creating load arrow at x = {position} mm...")

    arrow_length = 60.0  # mm
    arrow_radius = 6.0   # mm
    head_radius = 12.0   # mm
    head_length = 20.0   # mm

    # Arrow shaft (cylinder)
    shaft = Part.makeCylinder(arrow_radius, arrow_length)

    # Arrow head (cone)
    head = Part.makeCone(head_radius, 0, head_length)

    if direction == 'down':
        # Position above beam, pointing down
        y_pos = 0
        z_pos = OD/2  # Top of tube

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
    """Add text labels for loads, dimensions, and supports."""
    try:
        import Draft

        # Define colors matching respective components
        bright_teal = (0.3, 1.0, 1.0)  # Brighter teal for beam edge and text
        brighter_orange = (1.0, 0.85, 0.65)  # Brighter orange for load arrow edge and text
        orangeish_green = (0.9, 1.0, 0.4)  # Orangeish green for support edges and text

        # Label for load at midspan
        load_label_pos = App.Vector(L/2, -30, OD/2 + 90)
        load_text = Draft.make_text([f"P = {P} N"], load_label_pos)
        load_text.Label = "Label_Load_P200N"
        load_text.ViewObject.FontSize = 28.0
        load_text.ViewObject.TextColor = brighter_orange

        try:
            load_text.ViewObject.LineColor = brighter_orange
            load_text.ViewObject.LineWidth = 2.0
        except:
            pass

        # Label for beam length
        length_label_pos = App.Vector(L/2 - 80, -45, -OD/2 - 10)
        length_text = Draft.make_text([f"L = {L} mm"], length_label_pos)
        length_text.Label = "Label_Length_800mm"
        length_text.ViewObject.FontSize = 24.0
        length_text.ViewObject.TextColor = orangeish_green

        try:
            length_text.ViewObject.LineColor = orangeish_green
            length_text.ViewObject.LineWidth = 2.0
        except:
            pass

        # Label for pinned support - rotated 90 degrees CCW about Z axis
        pinned_label_pos = App.Vector(-30, 0, 0)
        pinned_text = Draft.make_text(["Pinned"], pinned_label_pos)
        pinned_text.Label = "Label_PinnedSupport"
        pinned_text.ViewObject.FontSize = 22.0
        pinned_text.ViewObject.TextColor = bright_teal

        # Rotate text 90 degrees counter-clockwise about Z axis
        pinned_text.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), 90)

        try:
            pinned_text.ViewObject.LineColor = bright_teal
            pinned_text.ViewObject.LineWidth = 2.0
        except:
            pass

        # Label for roller support - rotated 90 degrees CCW about Z axis
        roller_label_pos = App.Vector(L + 70, 0, 0)
        roller_text = Draft.make_text(["Roller"], roller_label_pos)
        roller_text.Label = "Label_RollerSupport"
        roller_text.ViewObject.FontSize = 22.0
        roller_text.ViewObject.TextColor = bright_teal

        # Rotate text 90 degrees counter-clockwise about Z axis
        roller_text.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), 90)

        try:
            roller_text.ViewObject.LineColor = bright_teal
            roller_text.ViewObject.LineWidth = 2.0
        except:
            pass

        print("✓ Labels added (color-coded to match components)")
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
    print("LAB 2: GANTRY RAIL - FREECAD 3D MODEL GENERATION")
    print("="*70)

    # Create new document (close existing one if it exists)
    doc_name = "Lab2_GantryRail"

    # Close the document if it already exists
    if doc_name in [doc.Name for doc in App.listDocuments().values()]:
        App.closeDocument(doc_name)
        print(f"Closed existing document: {doc_name}")

    doc = App.newDocument(doc_name)
    print(f"\nCreated fresh document: {doc_name}")

    # Define edge colors for all objects
    bright_teal = (0.3, 1.0, 1.0)  # Brighter teal for supports
    brighter_orange = (1.0, 0.85, 0.65)  # Brighter orange for load arrow
    orangeish_green = (0.9, 1.0, 0.4)  # Orangeish green for beam

    # Create hollow tube with orangeish green edges
    tube = create_hollow_tube()
    tube_obj = doc.addObject("Part::Feature", "Tube")
    tube_obj.Shape = tube
    tube_obj.ViewObject.ShapeColor = (0.18, 0.48, 0.56)  # Teal color
    tube_obj.ViewObject.LineColor = orangeish_green  # Orangeish green edges
    tube_obj.ViewObject.LineWidth = 3.0
    tube_obj.Label = f"Tube_Hollow_OD{int(OD)}mm_ID{int(ID)}mm_L{int(L)}mm"
    print("✓ Hollow tube created (with orangeish green edges)")

    # Create pinned support with bright teal edges
    pinned_support = create_pinned_support_visual()
    pinned_obj = doc.addObject("Part::Feature", "PinnedSupport")
    pinned_obj.Shape = pinned_support
    pinned_obj.ViewObject.ShapeColor = (0.25, 0.27, 0.30)  # Darker gray
    pinned_obj.ViewObject.LineColor = bright_teal  # Bright teal edges
    pinned_obj.ViewObject.LineWidth = 3.0
    pinned_obj.ViewObject.Transparency = 30
    pinned_obj.Label = "Support_Pinned_LeftEnd"
    print("✓ Pinned support created (darker gray faces with bright teal edges)")

    # Create roller support with bright teal edges
    roller_support = create_roller_support_visual()
    roller_obj = doc.addObject("Part::Feature", "RollerSupport")
    roller_obj.Shape = roller_support
    roller_obj.ViewObject.ShapeColor = (0.25, 0.27, 0.30)  # Darker gray
    roller_obj.ViewObject.LineColor = bright_teal  # Bright teal edges
    roller_obj.ViewObject.LineWidth = 3.0
    roller_obj.ViewObject.Transparency = 30
    roller_obj.Label = "Support_Roller_RightEnd"
    print("✓ Roller support created (darker gray faces with bright teal edges)")

    # Create load arrow at midspan with orange edges
    load_arrow = create_load_arrow(L/2, P, 'down')
    load_obj = doc.addObject("Part::Feature", "LoadArrow")
    load_obj.Shape = load_arrow
    arrow_orange = (1.0, 0.55, 0.21)  # Orange color
    load_obj.ViewObject.ShapeColor = arrow_orange
    load_obj.ViewObject.LineColor = arrow_orange  # Same orange as faces
    load_obj.ViewObject.LineWidth = 3.0
    load_obj.Label = f"Arrow_Load_P{int(P)}N_Midspan"
    print("✓ Load arrow created at midspan (with orange edges matching faces)")

    # Recompute document
    doc.recompute()

    print("\n✓ Model creation complete!")
    print(f"\nModel components:")
    print(f"  • Hollow tube: OD={OD} mm, ID={ID} mm, L={L} mm (teal with orangeish green edges)")
    print(f"  • Pinned support at x = 0 (darker gray with bright teal edges)")
    print(f"  • Roller support at x = {L} mm (darker gray with bright teal edges)")
    print(f"  • Point load P = {P} N at x = {L/2} mm (orange faces and edges)")

    print(f"\nTree view labels:")
    print(f"  • Tube_Hollow_OD{int(OD)}mm_ID{int(ID)}mm_L{int(L)}mm")
    print(f"  • Support_Pinned_LeftEnd")
    print(f"  • Support_Roller_RightEnd")
    print(f"  • Arrow_Load_P{int(P)}N_Midspan")

    # Add text labels (optional, may fail if Draft not available)
    add_text_labels(doc)

    # Fit view to model (if GUI is available)
    fit_view_to_model()

    print(f"\n💡 Styling notes:")
    print(f"  • Beam: Teal faces (0.18, 0.48, 0.56) + Orangeish green edges (0.9, 1.0, 0.4)")
    print(f"  • Supports: Darker gray faces (0.25, 0.27, 0.30) + Bright teal edges (0.3, 1.0, 1.0)")
    print(f"  • Load arrow: Orange faces and edges (1.0, 0.55, 0.21)")
    print(f"  • Text labels:")
    print(f"    - 'P = 200 N': Brighter orange (1.0, 0.85, 0.65)")
    print(f"    - 'L = 800 mm': Orangeish green (0.9, 1.0, 0.4)")
    print(f"    - 'Pinned'/'Roller': Bright teal (0.3, 1.0, 1.0), rotated 90° CCW")
    print(f"  • All components have distinct colors for clear visual differentiation")
    print(f"  • Descriptive tree names for easy identification")

    return doc


def export_model(doc, filename="lab2_gantry_rail_model"):
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
    """Add material property annotations."""
    print("\n🔧 MATERIAL PROPERTIES:")
    print("  • Material: Aluminum Alloy 6061-T6")
    print("  • Yield Strength: 275 MPa")
    print("  • Young's Modulus: 70 GPa")
    print("  • Poisson's Ratio: 0.33")
    print("  • Density: 2.70 g/cm³")


def main():
    """Main execution function."""
    # Create model
    doc = create_document()

    # Add material info
    add_material_properties(doc)

    # Export files
    export_model(doc, "lab2_gantry_rail_model")

    print("\n" + "="*70)
    print("🎯 LAB 2 FREECAD MODEL GENERATION COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Open the document in FreeCAD GUI to view the 3D model")
    print("2. Rotate to isometric view and take screenshots")
    print("3. Export to GLB format for web visualization")
    print("4. For FEM analysis, use the FEM workbench manually")
    print("\n" + "="*70)


if __name__ == "__main__" or __name__ == "__console__":
    main()
