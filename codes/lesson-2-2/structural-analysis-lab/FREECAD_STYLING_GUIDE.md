# FreeCAD Model Styling Guide - Lab 1

**Date**: 2025-11-01
**Purpose**: Professional 3D model appearance with visibility on dark backgrounds

---

## 🎨 Color Scheme

### Model Edge Colors (All Objects)
- **Color**: Bright Teal/Cyan
- **RGB**: `(0.0, 0.9, 0.9)`
- **Hex**: `#00E6E6`
- **Line Width**: 3.0 pt
- **Purpose**: High visibility on both light and dark backgrounds, matches beam theme

### Object Face Colors

| Object | Face Color (RGB) | Description |
|--------|-----------------|-------------|
| Beam | `(0.18, 0.48, 0.56)` | Teal - represents aluminum |
| Fixed Support | `(0.42, 0.45, 0.50)` | Gray - structural support |
| Load Arrow | `(1.0, 0.55, 0.21)` | Orange - represents applied force |

### Text Labels
- **Color**: Bright Teal/Cyan `(0.0, 0.9, 0.9)`
- **Font Sizes**:
  - Load label (P = 500 N): 28 pt
  - Length label (L = 500 mm): 24 pt
  - Support label (Fixed): 22 pt
- **Outline**: Bright Teal, 2.0 pt width
- **Position**: "Fixed" label moved away from model to avoid overlap (x = -80 mm)
- **Purpose**: Maximum visibility on dark FreeCAD backgrounds

---

## 📝 Tree View Naming Convention

Clear, descriptive names instead of generic "Part", "Text", "Text001":

| Object Type | Tree View Name | Description |
|-------------|---------------|-------------|
| Beam | `Beam_500x60x20mm` | Includes dimensions for clarity |
| Fixed Support | `Support_Fixed_LeftEnd` | Support type and location |
| Load Arrow | `Arrow_Load_P500N_Downward` | Load magnitude and direction |
| Load Text | `Label_Load_P500N` | What the label describes |
| Length Text | `Label_Length_500mm` | What the label describes |
| Support Text | `Label_FixedSupport` | What the label describes |

**Benefits**:
- ✅ Easy to identify objects in complex models
- ✅ No confusion between multiple text labels
- ✅ Clear indication of what each component represents
- ✅ Professional organization

---

## 🖼️ Visual Appearance

### On Light Backgrounds
- Gold edges provide clear definition without being overwhelming
- Face colors remain vivid and distinguishable
- Text labels stand out clearly

### On Dark Backgrounds (FreeCAD Default)
- **Gold edges shine brilliantly** - highly visible
- **Gold text labels** are easy to read
- Face colors provide good contrast
- Professional engineering appearance

---

## 💻 Implementation in Python

### Setting Edge Colors and Width
```python
obj.ViewObject.LineColor = (1.0, 0.84, 0.0)  # Gold
obj.ViewObject.LineWidth = 3.0  # Visible but not overwhelming
```

### Setting Descriptive Tree Names
```python
obj.Label = "Beam_500x60x20mm"  # Instead of default "Part"
```

### Setting Text Label Properties
```python
text_obj.Label = "Label_Load_P500N"  # Tree view name
text_obj.ViewObject.FontSize = 28.0  # Larger for visibility
text_obj.ViewObject.TextColor = (1.0, 0.84, 0.0)  # Gold
text_obj.ViewObject.LineColor = (1.0, 0.84, 0.0)  # Gold outline
text_obj.ViewObject.LineWidth = 2.0
```

---

## 📊 Before vs After Comparison

### Before (Default FreeCAD)
```
Tree View:
├── Part
├── Part001
├── Part002
├── Text
├── Text001
└── Text002

Edges: Black (invisible on dark backgrounds)
Text: Small, hard to read
Labels: Generic "Part", "Text"
```

### After (Improved)
```
Tree View:
├── Beam_500x60x20mm
├── Support_Fixed_LeftEnd
├── Arrow_Load_P500N_Downward
├── Label_Load_P500N
├── Label_Length_500mm
└── Label_FixedSupport

Edges: Gold (highly visible on dark backgrounds)
Text: Larger (22-28 pt), gold color
Labels: Descriptive, professional
```

---

## 🎯 Design Rationale

### Why Bright Teal/Cyan Edges?
1. **Universal Visibility**: Works on both light and dark backgrounds
2. **Theme Consistency**: Matches the teal beam color scheme
3. **Non-Intrusive**: Bright enough to see, not overwhelming
4. **Professional**: Clean, modern appearance for technical models
5. **Contrast**: Stands out against orange load arrows and gray supports

### Why Larger Text?
1. **Screenshot Quality**: Labels remain readable in exported images
2. **Presentation Ready**: Suitable for reports and presentations
3. **Accessibility**: Easier to read for all users
4. **Web Viewing**: GLB files viewed in browsers need larger text

### Why Descriptive Tree Names?
1. **Student Learning**: Clear what each object represents
2. **Organization**: Easy to select specific objects
3. **Professional Practice**: Industry standard for CAD models
4. **Collaboration**: Others can understand the model structure

---

## 🔧 Student Benefits

When students use this model:

1. ✅ **Easy Navigation**: Find objects quickly in tree view
2. ✅ **Clear Visualization**: Gold edges visible on any background
3. ✅ **Professional Output**: Screenshots look polished
4. ✅ **Learning Aid**: Names reinforce what each component is
5. ✅ **Web Ready**: GLB exports look great in 3D viewers
6. ✅ **Dark Mode Friendly**: Perfect for FreeCAD's default dark theme

---

## 📐 Technical Specifications

### Edge Rendering
- **Type**: Solid lines
- **Color**: RGB (1.0, 0.84, 0.0) = Hex #FFD700
- **Width**: 3.0 points
- **Applied to**: All Part::Feature objects (beam, support, arrow)

### Text Rendering
- **Font**: FreeCAD default (system sans-serif)
- **Sizes**: 22-28 pt (varies by label importance)
- **Color**: RGB (1.0, 0.84, 0.0) = Hex #FFD700
- **Outline**: 2.0 pt gold (when supported)
- **Position**: Offset from geometry for clarity

### Naming Convention
- **Format**: `ObjectType_Descriptors_Details`
- **Examples**:
  - `Beam_500x60x20mm` (type_dimensions)
  - `Support_Fixed_LeftEnd` (type_characteristic_location)
  - `Arrow_Load_P500N_Downward` (type_function_magnitude_direction)
  - `Label_Load_P500N` (type_purpose_value)

---

## ✅ Quality Checklist

When reviewing the FreeCAD model, verify:

- [ ] All edges are gold/yellow (RGB: 1.0, 0.84, 0.0)
- [ ] Edge width is 3.0 pt (visible but not thick)
- [ ] All tree view names are descriptive (no "Part", "Text")
- [ ] Text labels are 22-28 pt size
- [ ] Text labels are gold/yellow color
- [ ] Text is readable on dark background
- [ ] Object names include key dimensions/characteristics
- [ ] Model exports cleanly to GLB format

---

## 🌐 Web Viewer Compatibility

When viewed at https://siliconwit.com/product-development/3d-model-viewer/:

✅ **Gold edges** render correctly in WebGL
✅ **Text labels** remain visible and readable
✅ **Object names** are preserved in GLB metadata
✅ **Colors** match FreeCAD appearance
✅ **Dark background** shows gold elements clearly

---

**This styling creates professional, accessible 3D models suitable for education, presentations, and web viewing!** 🎉
