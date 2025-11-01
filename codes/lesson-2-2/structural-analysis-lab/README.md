# Structural Analysis Laboratory - Example Solutions

This folder contains comprehensive example solutions for all three structural analysis laboratory experiments. These scripts demonstrate exactly what students are expected to produce for each lab.

## 📁 Folder Contents

### Lab 1: Robotic Arm Cantilever Analysis
- **`lab1_robotic_arm_analysis.py`** - Complete analytical solution with SFD/BMD
- **`lab1_freecad_model.py`** - FreeCAD 3D model generation script

**Problem**: Cantilever beam (L=500mm, 60×20mm rectangular, Al 6061-T6, P=500N)

**What it demonstrates**:
- Reaction force calculations
- Shear force and bending moment functions
- Maximum stress using flexure formula
- Safety factor analysis
- Professional SVG plot generation

**Outputs**:
- `lab1_loading_diagram.svg` - Beam with supports, loads, and reactions
- `lab1_sfd_bmd.svg` - Combined shear force and bending moment diagrams
- Console output with step-by-step calculations

---

### Lab 2: 3D Printer Gantry Rail Analysis
- **`lab2_gantry_rail_analysis.py`** - Parametric moving load analysis
- **`lab2_freecad_fem.py`** - Complete FEM setup with boundary conditions

**Problem**: Simply supported beam (L=800mm, hollow circular OD=30mm ID=24mm, Al 6061-T6, P=200N moving load)

**What it demonstrates**:
- Critical load position determination (midspan for simply supported)
- Parametric stress analysis vs load position
- Mesh convergence study template
- FEM validation against analytical solution
- Hollow circular section properties

**Outputs**:
- `lab2_stress_analysis.svg` - Moment and stress vs load position
- `lab2_convergence_template.svg` - Mesh convergence analysis
- FreeCAD document ready for FEM analysis

---

### Lab 3: Drone Arm Combined Loading
- **`lab3_drone_arm_analysis.py`** - Complete combined stress analysis
- **`lab3_freecad_combined_fem.py`** - FEM setup for combined loads

**Problem**: Cantilever (L=200mm, hollow circular OD=16mm ID=12mm, Carbon fiber, P=30N + F=5N + T=1.0N·m)

**What it demonstrates**:
- Stress superposition from multiple loading components
- Bending from two perpendicular planes
- Torsional shear stress
- Principal stress calculation
- Mohr's circle construction
- Von Mises, Tresca, and Maximum Stress criteria
- Design optimization for weight reduction

**Outputs**:
- `lab3_mohrs_circle.svg` - Complete Mohr's circle with annotations
- `lab3_optimization.svg` - Weight vs safety factor optimization
- Console output with complete stress analysis

---

## 🚀 How to Use These Examples

### For Students:

1. **Before writing your own code**: Read through the example to understand the structure
2. **While coding**: Use as reference for matplotlib styling, calculation methods, output formatting
3. **After coding**: Compare your results with the example values to validate
4. **For reports**: Use the console output format as a guide for presenting calculations

### 🐍 Standalone Python Scripts (Run Directly)

These scripts run with standard Python and generate analysis outputs:

```bash
# Lab 1 - Robotic Arm Analysis
python lab1_robotic_arm_analysis.py
# Outputs: lab1_loading_diagram.svg, lab1_sfd_bmd.svg

# Lab 2 - Gantry Rail Analysis
python lab2_gantry_rail_analysis.py
# Outputs: lab2_stress_analysis.svg, lab2_convergence_template.svg

# Lab 3 - Drone Arm Analysis
python lab3_drone_arm_analysis.py
# Outputs: lab3_mohrs_circle.svg, lab3_optimization.svg
```

**Requirements**:
```bash
pip install numpy matplotlib scipy pandas
```

**What these do**:
- Complete analytical calculations
- Generate professional SVG plots
- Print step-by-step results to console
- Validate against hand calculations

---

### 🔧 FreeCAD Scripts (Run Inside FreeCAD)

These scripts **MUST** run inside FreeCAD (not standalone Python):

**Files**:
- `lab1_freecad_model.py` - Creates 3D beam model for Lab 1
- `lab2_freecad_fem.py` - Sets up FEM analysis for Lab 2
- `lab3_freecad_combined_fem.py` - Sets up combined loading FEM for Lab 3

**How to run**:

**Option 1: FreeCAD GUI (Recommended)**
1. Open FreeCAD application
2. View → Panels → Python console
3. In console, type:
   ```python
   exec(open('/full/path/to/lab1_freecad_model.py').read())
   ```
   Replace `/full/path/to/` with actual path to this folder

**Option 2: FreeCAD Command Line**
```bash
freecad lab1_freecad_model.py
freecad lab2_freecad_fem.py
freecad lab3_freecad_combined_fem.py
```

**What these do**:
- Create 3D geometry in FreeCAD
- Set up FEM analysis containers
- Add material properties and boundary conditions
- Export models to STEP/STL formats
- Prepare for GLB export (manual step in GUI)

---

## ✅ Testing Status

All standalone Python scripts have been tested and run successfully:

| Script | Status | Output Files | File Size |
|--------|--------|--------------|-----------|
| `lab1_robotic_arm_analysis.py` | ✅ Working | `lab1_loading_diagram.svg` (24 KB)<br>`lab1_sfd_bmd.svg` (71 KB) | Console: 2.5 KB |
| `lab2_gantry_rail_analysis.py` | ✅ Working | `lab2_stress_analysis.svg` (86 KB)<br>`lab2_convergence_template.svg` (28 KB) | Console: 3.2 KB |
| `lab3_drone_arm_analysis.py` | ✅ Working | `lab3_mohrs_circle.svg` (56 KB)<br>`lab3_optimization.svg` (51 KB) | Console: 4.8 KB |

**FreeCAD Scripts** (require FreeCAD to run):
- `lab1_freecad_model.py` - Creates 3D beam with labels, auto-fits view, exports STEP/STL
- `lab2_freecad_fem.py` - FEM setup with materials and BC
- `lab3_freecad_combined_fem.py` - Combined loading FEM setup

**Lab 1 FreeCAD Script Features**:
- ✅ Arrow properly fused and pointing downward
- ✅ Automatic text labels (P=500N, L=500mm, Fixed)
- ✅ Object labels in tree view for easy identification
- ✅ Auto-fit isometric view
- ✅ GLB export with verification link to https://siliconwit.com/product-development/3d-model-viewer/

---

## 📊 Expected Results Summary

### Lab 1 Results:
- Maximum shear: |V_max| = 500 N (constant)
- Maximum moment: M_max = 250 N·m at fixed end
- Maximum stress: σ_max = 62.5 MPa
- Safety factor: SF = 4.4 (excellent for robotics)

### Lab 2 Results:
- Critical position: a = 400 mm (midspan)
- Maximum moment: M_max = 40 N·m
- Maximum stress: σ_max ≈ 10.0 MPa
- Safety factor: SF = 27.5 (high, but accounts for dynamics)

### Lab 3 Results:
- Combined bending: σ_x ≈ 25 MPa
- Torsional shear: τ_xy ≈ 3.5 MPa
- Maximum principal: σ₁ ≈ 26 MPa
- Von Mises stress: σ_VM ≈ 25 MPa
- Safety factor: SF ≈ 13 (governs: max tensile stress)

---

## 🎨 Styling and Formatting

All scripts use **consistent styling** matching the reference files:

### Color Scheme:
- Beam: `#2d7a8f` (dark teal)
- Supports: `#6B7280` (gray)
- Forces: `#ff8c36` (orange)
- Reactions: `#00a0d0` (light blue)
- Text/axes: `#405ab9` (blue)
- Grid: `#9ea388` (gray-green)

### Plot Settings:
- Font size: 28-32pt (mobile-friendly)
- Line width: 5pt
- Axes width: 4pt
- Format: SVG (transparent background)
- DPI: 300 (publication quality)

### Output Format:
- Step-by-step calculations with equations
- Professional formatting with Unicode symbols
- Clear section headers with emojis
- Engineering assessment and recommendations

---

## 📝 File Naming Convention

Students should name their files according to lab manual specifications:

```
E022-01-XXXX-YYYY-Lab1-Analysis.py
E022-01-XXXX-YYYY-Lab1-Model.glb
E022-01-XXXX-YYYY-Lab1-SFD-BMD.svg
...
```

Where:
- `XXXX` = Your 4-digit registration number
- `YYYY` = Registration year

---

## 🔧 Customization for Group Parameters

Each lab has group-specific parameters. To adapt these examples:

1. Find the parameter table in the lab manual
2. Locate your group number
3. Replace the values in the `__init__` method:

```python
# Example: Lab 1, Group 5
self.L = 524.0   # Your group's beam length
self.P = 524.0   # Your group's load
```

All calculations will automatically update!

---

## 🐛 Troubleshooting

### Python script errors:
- **Import error**: Install missing packages with `pip install`
- **No output plots**: Check that script completed without errors
- **Different results**: Verify you're using your group's parameters

### FreeCAD script errors:
- **Module not found**: Ensure running inside FreeCAD (not standalone Python)
- **Document exists**: Script auto-closes if document already open
- **Geometry issues**: Clear undo history and try again

### Results don't match analytical:
- **FEM stress differs**: Check mesh quality and refinement
- **Wrong critical location**: Verify load positions and support types
- **Safety factor too high/low**: Confirm material properties

---

## 📚 Learning Objectives

By studying and adapting these examples, you will learn:

1. **Programming skills**:
   - Structured code organization (classes, methods)
   - Professional documentation and comments
   - Data visualization with matplotlib
   - File I/O and path handling

2. **Engineering analysis**:
   - Equilibrium equations and reactions
   - Internal force distributions
   - Stress calculations and failure criteria
   - FEM validation and convergence

3. **Technical communication**:
   - Clear presentation of calculations
   - Professional plot formatting
   - Engineering assessment and recommendations
   - Documentation standards

---

## 💡 Tips for Success

1. **Understand before copying**: Read through the code to understand each section
2. **Validate your work**: Compare intermediate results with example outputs
3. **Customize thoughtfully**: Change parameters but maintain calculation logic
4. **Test incrementally**: Run code after each section to catch errors early
5. **Document thoroughly**: Add comments explaining your group's specific setup
6. **Ask questions**: If results differ significantly, consult with instructor

---

## 📖 References

- Lab manual: `structural-analysis-laboratory-manual.mdx`
- Beam diagrams reference: `beam_type_diagrams.py`
- Multi-load analysis reference: `conveyor_beam_analysis.py`
- FreeCAD documentation: https://wiki.freecad.org/
- Matplotlib gallery: https://matplotlib.org/stable/gallery/

---

## ⚠️ Important Notes

1. **Academic integrity**: These are **examples** for learning. Your submission must:
   - Use your group's assigned parameters
   - Include your own analysis and interpretations
   - Show understanding through comments and documentation

2. **File submissions**: Follow naming conventions exactly to avoid penalties

3. **FEM analysis**: Manual face selection required in FreeCAD - scripts provide setup only

4. **Units**: All scripts use consistent units (mm, N, MPa) - verify in your calculations

---

## 🎯 Success Criteria

Your submission should match or exceed these examples in:
- ✅ Code organization and documentation
- ✅ Calculation accuracy and validation
- ✅ Plot quality and professional formatting
- ✅ Engineering assessment depth
- ✅ File naming and submission standards

Good luck with your laboratory work! 🚀

---

**Author**: SiliconWit Mechanics of Materials Laboratory Team
**Course**: E022-01 Modeling and Simulation
**Last Updated**: 2025-11-01
