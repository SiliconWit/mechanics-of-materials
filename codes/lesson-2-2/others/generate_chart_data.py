#!/usr/bin/env python3
"""
Generate JSON data for Chart.js implementations
Creates the data files that can be used by Chart.js for dynamic loading
"""

import json
import numpy as np

def generate_shear_data():
    """Generate corrected shear force data"""
    return {
        "title": "Shear Force Diagram",
        "xLabel": "Distance from A (m)",
        "yLabel": "Shear Force (N)",
        "xMin": -0.2,
        "xMax": 4.2,
        "yMin": -7500,
        "yMax": 5500,
        "segments": [
            {
                "name": "segment1",
                "x": [0, 1.5],
                "y": [3167, 1967],
                "description": "Linear decrease due to distributed load"
            },
            {
                "name": "segment2",
                "x": [1.5, 3.0],
                "y": [-5033, -6233],
                "description": "After P1, continued decrease"
            },
            {
                "name": "segment3",
                "x": [3.0, 4.0],
                "y": [5000, 0],
                "description": "CORRECTED: Direct line from +5000 to 0"
            }
        ],
        "criticalPoints": [
            {"x": 0, "y": 3167, "label": "+3167 N", "description": "At support A"},
            {"x": 1.5, "y": 1967, "label": "+1967 N", "description": "Just before P1"},
            {"x": 1.5, "y": -5033, "label": "-5033 N", "description": "Just after P1"},
            {"x": 3.0, "y": -6233, "label": "-6233 N", "description": "Just before B"},
            {"x": 3.0, "y": 5000, "label": "+5000 N", "description": "Just after B"},
            {"x": 4.0, "y": 0, "label": "0 N", "description": "At free end"}
        ],
        "indicators": [
            {"x": 0, "label": "A", "type": "support", "color": "#2A9D8F"},
            {"x": 1.5, "label": "P₁", "type": "load", "color": "#F4D03F"},
            {"x": 3.0, "label": "B", "type": "support", "color": "#2A9D8F"},
            {"x": 4.0, "label": "P₂", "type": "load", "color": "#F4D03F"}
        ]
    }

def generate_moment_data():
    """Generate bending moment data using exact equations"""
    # Generate high-resolution curve
    x_points = np.linspace(0, 4.0, 200)
    moment_points = []

    for x in x_points:
        # Calculate moment using exact equations from lesson
        M = 3167 * x - 800 * x * (x / 2)  # R_A and distributed load

        if x >= 1.5:  # Past P1
            M -= 7000 * (x - 1.5)
        if x >= 3.0:  # Past support B
            M += 11233 * (x - 3.0)
        if x >= 4.0:  # At P2
            M -= 4200 * (x - 4.0)

        moment_points.append({"x": float(x), "y": float(M)})

    return {
        "title": "Bending Moment Diagram",
        "xLabel": "Distance from A (m)",
        "yLabel": "Bending Moment (N·m)",
        "xMin": -0.2,
        "xMax": 4.2,
        "yMin": -5200,
        "yMax": 4200,
        "curveData": moment_points,
        "criticalPoints": [
            {"x": 0, "y": 0, "label": "0 N·m", "description": "At support A"},
            {"x": 1.5, "y": 3850.5, "label": "+3851 N·m", "description": "Maximum positive moment"},
            {"x": 3.0, "y": -4599, "label": "-4599 N·m", "description": "Maximum negative moment"},
            {"x": 4.0, "y": 1, "label": "≈0 N·m", "description": "At free end"}
        ],
        "indicators": [
            {"x": 0, "label": "A", "type": "support", "color": "#2A9D8F"},
            {"x": 1.5, "label": "P₁", "type": "load", "color": "#F4D03F"},
            {"x": 3.0, "label": "B", "type": "support", "color": "#2A9D8F"},
            {"x": 4.0, "label": "P₂", "type": "load", "color": "#F4D03F"}
        ],
        "annotations": [
            {
                "x": 1.5,
                "y": 3850.5,
                "text": "M_max = +3851 N·m",
                "color": "#2A9D8F",
                "position": "top"
            },
            {
                "x": 3.0,
                "y": -4599,
                "text": "M_min = -4599 N·m",
                "color": "#F4D03F",
                "position": "bottom"
            }
        ]
    }

def main():
    """Generate and save JSON data files"""

    print("📊 Generating Chart.js JSON data files...")

    # Generate shear force data
    shear_data = generate_shear_data()
    shear_path = '/home/sam/Documents/starlight/siliconwit-com-astro/siliconwit-com/src/content/docs/education/mechanics-of-materials/codes/lesson-2-2/shear_force_data.json'

    with open(shear_path, 'w') as f:
        json.dump(shear_data, f, indent=2)

    print(f"✓ Saved: shear_force_data.json")

    # Generate moment data
    moment_data = generate_moment_data()
    moment_path = '/home/sam/Documents/starlight/siliconwit-com-astro/siliconwit-com/src/content/docs/education/mechanics-of-materials/codes/lesson-2-2/bending_moment_data.json'

    with open(moment_path, 'w') as f:
        json.dump(moment_data, f, indent=2)

    print(f"✓ Saved: bending_moment_data.json")

    print("\n🎉 JSON data files generated successfully!")
    print("📁 These can be used for:")
    print("   • Dynamic Chart.js loading")
    print("   • Interactive web applications")
    print("   • Data analysis and verification")
    print("   • Future interactivity features")

if __name__ == "__main__":
    main()