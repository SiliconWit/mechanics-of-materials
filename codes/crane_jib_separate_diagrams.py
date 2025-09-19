#!/usr/bin/env python3
"""
Crane Jib Beam Analysis - Separate Diagrams Generator
Application 3: Industrial Crane Jib with Overhang Loading

This script generates 3 separate PNG diagrams with transparent backgrounds:
1. Beam loading diagram
2. Shear force diagram
3. Bending moment diagram

Colors are chosen to be visible on both light and dark backgrounds.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def setup_plot_style():
    """Configure matplotlib for transparent backgrounds and appropriate colors"""
    plt.style.use('default')
    plt.rcParams.update({
        'figure.facecolor': 'none',  # Transparent figure background
        'axes.facecolor': 'none',    # Transparent axes background
        'savefig.facecolor': 'none', # Transparent saved figure background
        'text.color': '#333333',     # Dark gray text (visible on light/dark)
        'axes.labelcolor': '#333333',
        'xtick.color': '#333333',
        'ytick.color': '#333333',
        'axes.edgecolor': '#666666', # Medium gray for axes edges
        'grid.color': '#888888',     # Light gray for grid
        'grid.alpha': 0.5,
        'font.size': 12,
        'axes.linewidth': 1.5
    })

def create_beam_diagram():
    """Create the beam loading diagram"""
    setup_plot_style()

    fig, ax = plt.subplots(figsize=(14, 8))

    # Beam geometry
    beam_height = 0.3
    beam_y = 0

    # Draw main beam
    beam = patches.Rectangle((0, beam_y - beam_height/2), 4.0, beam_height,
                            linewidth=2, edgecolor='#333333', facecolor='#CCCCCC', alpha=0.7)
    ax.add_patch(beam)

    # Support A (pinned) at x = 0
    support_size = 0.2
    triangle_a = patches.Polygon([(0, beam_y - beam_height/2),
                                 (-support_size, beam_y - beam_height/2 - support_size),
                                 (support_size, beam_y - beam_height/2 - support_size)],
                                closed=True, facecolor='#666666', edgecolor='#333333', linewidth=2)
    ax.add_patch(triangle_a)

    # Support B (roller) at x = 3.0
    circle_b = patches.Circle((3.0, beam_y - beam_height/2 - support_size/2), support_size/2,
                             facecolor='#666666', edgecolor='#333333', linewidth=2)
    ax.add_patch(circle_b)

    # Draw reaction forces
    arrow_props = dict(arrowstyle='->', connectionstyle='arc3', lw=3, color='#0066CC')

    # R_A = 3167 N (upward)
    ax.annotate('', xy=(0, beam_y - beam_height/2), xytext=(0, beam_y - beam_height/2 - 1.0),
                arrowprops=arrow_props)
    ax.text(0, beam_y - beam_height/2 - 1.3, 'R_A = 3167 N', ha='center', va='top',
            fontweight='bold', color='#0066CC', fontsize=11)

    # R_B = 11233 N (upward)
    ax.annotate('', xy=(3.0, beam_y - beam_height/2), xytext=(3.0, beam_y - beam_height/2 - 1.0),
                arrowprops=arrow_props)
    ax.text(3.0, beam_y - beam_height/2 - 1.3, 'R_B = 11233 N', ha='center', va='top',
            fontweight='bold', color='#0066CC', fontsize=11)

    # Draw applied loads
    load_arrow_props = dict(arrowstyle='->', connectionstyle='arc3', lw=3, color='#CC0000')

    # P₁ = 7000 N at x = 1.5 m (downward)
    ax.annotate('', xy=(1.5, beam_y + beam_height/2), xytext=(1.5, beam_y + beam_height/2 + 1.0),
                arrowprops=load_arrow_props)
    ax.text(1.5, beam_y + beam_height/2 + 1.3, 'P₁ = 7000 N\n(includes dynamic factor)',
            ha='center', va='bottom', fontweight='bold', color='#CC0000', fontsize=11)

    # P₂ = 4200 N at x = 4.0 m (downward)
    ax.annotate('', xy=(4.0, beam_y + beam_height/2), xytext=(4.0, beam_y + beam_height/2 + 1.0),
                arrowprops=load_arrow_props)
    ax.text(4.0, beam_y + beam_height/2 + 1.3, 'P₂ = 4200 N\n(includes dynamic factor)',
            ha='center', va='bottom', fontweight='bold', color='#CC0000', fontsize=11)

    # Distributed load w = 800 N/m
    x_dist = np.linspace(0, 4.0, 21)
    for xi in x_dist:
        ax.annotate('', xy=(xi, beam_y + beam_height/2), xytext=(xi, beam_y + beam_height/2 + 0.4),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='#FF6600'))

    ax.text(2.0, beam_y + beam_height/2 + 0.7, 'w = 800 N/m (distributed load)',
            ha='center', va='bottom', fontweight='bold', color='#FF6600', fontsize=11)

    # Dimensions
    ax.annotate('', xy=(0, -2.0), xytext=(3.0, -2.0),
                arrowprops=dict(arrowstyle='<->', lw=2, color='#333333'))
    ax.text(1.5, -2.3, '3000 mm span', ha='center', va='top', fontweight='bold', color='#333333')

    ax.annotate('', xy=(3.0, -2.5), xytext=(4.0, -2.5),
                arrowprops=dict(arrowstyle='<->', lw=2, color='#333333'))
    ax.text(3.5, -2.8, '1000 mm\noverhang', ha='center', va='top', fontweight='bold', color='#333333')

    # Labels
    ax.text(0, beam_y - beam_height/2 - 0.6, 'A\n(Pinned)', ha='center', va='top',
            fontweight='bold', color='#333333')
    ax.text(3.0, beam_y - beam_height/2 - 0.6, 'B\n(Roller)', ha='center', va='top',
            fontweight='bold', color='#333333')
    ax.text(4.0, beam_y - beam_height/2 - 0.4, 'Free End', ha='center', va='top',
            fontweight='bold', color='#333333')

    # Position labels
    for x_pos, label in [(0, '0'), (1.5, '1.5'), (3.0, '3.0'), (4.0, '4.0')]:
        ax.axvline(x=x_pos, color='#888888', linestyle=':', alpha=0.7)
        ax.text(x_pos, -3.5, f'{label} m', ha='center', va='top', color='#333333')

    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-4, 3)
    ax.set_xlabel('Distance from Support A (m)', fontweight='bold', color='#333333')
    ax.set_title('Crane Jib Beam - Loading Diagram', fontweight='bold', fontsize=14, color='#333333')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

    # Remove y-axis for beam diagram
    ax.set_yticks([])

    plt.tight_layout()
    plt.savefig('/home/sam/Documents/starlight/siliconwit-com-astro/siliconwit-com/src/content/docs/education/mechanics-of-materials/crane_jib_beam_diagram.png',
                dpi=300, bbox_inches='tight', facecolor='none', edgecolor='none')
    plt.close()

def create_shear_diagram():
    """Create the shear force diagram"""
    setup_plot_style()

    fig, ax = plt.subplots(figsize=(12, 8))

    # Critical points and values
    x_points = np.array([0, 1.5, 1.5, 3.0, 3.0, 4.0])
    V_points = np.array([3167, 1967, -5033, -6233, 5000, 0])

    # Create detailed x array for smooth curves
    x1 = np.linspace(0, 1.5, 100)
    V1 = 3167 - 800 * x1  # Linear decrease due to distributed load

    x2 = np.linspace(1.5, 3.0, 100)
    V2 = -5033 - 800 * (x2 - 1.5)  # Continue linear decrease

    # Overhang section: from x = 3.0 to just before x = 4.0
    x3a = np.linspace(3.0, 3.99, 50)  # Just before P₂
    V3a = 5000 - 800 * (x3a - 3.0)   # Linear decrease in overhang

    # At x = 4.0, show the discontinuity due to P₂
    # Before P₂: V = 5000 - 800(1.0) = 4200
    # After P₂: V = 4200 - 4200 = 0

    # Plot shear force diagram
    ax.plot(x1, V1, 'b-', linewidth=3, label='Shear Force')
    ax.plot(x2, V2, 'b-', linewidth=3)
    ax.plot(x3a, V3a, 'b-', linewidth=3)

    # Show the final drop to zero at P₂
    ax.plot([4.0, 4.0], [4200, 0], 'b-', linewidth=3)  # Vertical line showing drop
    ax.plot([4.0], [0], 'bo', markersize=6, markerfacecolor='blue', markeredgecolor='white')

    # Mark critical points
    critical_x = [0, 1.5, 1.5, 3.0, 3.0, 4.0]
    critical_V = [3167, 1967, -5033, -6233, 5000, 0]
    ax.plot(critical_x, critical_V, 'ro', markersize=8, markerfacecolor='#CC0000',
            markeredgecolor='#333333', markeredgewidth=2, label='Critical Points')

    # Add value annotations
    annotations = [
        (0, 3167, '+3167'),
        (1.4, 1967, '+1967'),
        (1.6, -5033, '-5033'),
        (2.9, -6233, '-6233'),
        (3.1, 5000, '+5000'),
        (4.0, 0, '0')
    ]

    for x, y, text in annotations:
        ax.annotate(f'{text} N', xy=(x, y), xytext=(x, y + 1000 if y >= 0 else y - 1000),
                   ha='center', va='bottom' if y >= 0 else 'top',
                   fontweight='bold', color='#333333', fontsize=10,
                   arrowprops=dict(arrowstyle='->', color='#666666', lw=1))

    # Zero line
    ax.axhline(y=0, color='#333333', linestyle='-', linewidth=1.5, alpha=0.8)

    # Support and load locations
    for x_pos, label, color in [(0, 'A', '#0066CC'), (1.5, 'P₁', '#CC0000'),
                                (3.0, 'B', '#0066CC'), (4.0, 'P₂', '#CC0000')]:
        ax.axvline(x=x_pos, color=color, linestyle='--', alpha=0.7, linewidth=2)
        ax.text(x_pos, ax.get_ylim()[1]*0.9, label, ha='center', va='center',
               fontweight='bold', color=color, fontsize=12,
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.8))

    ax.set_xlabel('Distance from A (m)', fontweight='bold', color='#333333')
    ax.set_ylabel('Shear Force (N)', fontweight='bold', color='#333333')
    ax.set_title('Shear Force Diagram', fontweight='bold', fontsize=14, color='#333333')
    ax.grid(True, alpha=0.4)
    ax.legend(loc='upper right', fancybox=True, shadow=True)

    ax.set_xlim(-0.2, 4.2)
    ax.set_ylim(-8000, 6000)

    plt.tight_layout()
    plt.savefig('/home/sam/Documents/starlight/siliconwit-com-astro/siliconwit-com/src/content/docs/education/mechanics-of-materials/crane_jib_shear_diagram.png',
                dpi=300, bbox_inches='tight', facecolor='none', edgecolor='none')
    plt.close()

def create_moment_diagram():
    """Create the bending moment diagram"""
    setup_plot_style()

    fig, ax = plt.subplots(figsize=(12, 8))

    # Create detailed x array for smooth moment curve
    x = np.linspace(0, 4.0, 1000)
    M = np.zeros_like(x)

    # Calculate moment at each point using cut method
    for i, xi in enumerate(x):
        M_calc = 3167 * xi - 800 * xi * (xi / 2)  # R_A and distributed load

        if xi >= 1.5:  # Past P1
            M_calc -= 7000 * (xi - 1.5)
        if xi >= 3.0:  # Past support B
            M_calc += 11233 * (xi - 3.0)
        if xi >= 4.0:  # Past P2 (should be minimal effect)
            M_calc -= 4200 * (xi - 4.0)

        M[i] = M_calc

    # Plot moment diagram
    ax.plot(x, M, 'r-', linewidth=3, label='Bending Moment')

    # Fill positive and negative regions
    ax.fill_between(x, M, 0, where=(M >= 0), alpha=0.3, color='#00AA00',
                   label='Positive Moment\n(Tension bottom)')
    ax.fill_between(x, M, 0, where=(M < 0), alpha=0.3, color='#FF6600',
                   label='Negative Moment\n(Tension top)')

    # Mark critical points
    critical_x = [0, 1.5, 3.0, 4.0]
    critical_M = [0, 3850.5, -4599, 1]  # From lesson calculations
    ax.plot(critical_x, critical_M, 'ko', markersize=8, markerfacecolor='#333333',
            markeredgecolor='white', markeredgewidth=2, label='Critical Points')

    # Annotate maximum moments
    ax.annotate(f'M_max = +3851 N·m', xy=(1.5, 3850.5),
                xytext=(2.2, 4500), ha='center', va='bottom',
                fontweight='bold', color='#00AA00', fontsize=11,
                arrowprops=dict(arrowstyle='->', color='#00AA00', lw=2),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#00AA00', alpha=0.9))

    ax.annotate(f'M_min = -4599 N·m', xy=(3.0, -4599),
                xytext=(2.2, -5500), ha='center', va='top',
                fontweight='bold', color='#FF6600', fontsize=11,
                arrowprops=dict(arrowstyle='->', color='#FF6600', lw=2),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#FF6600', alpha=0.9))

    # Zero line
    ax.axhline(y=0, color='#333333', linestyle='-', linewidth=1.5, alpha=0.8)

    # Support and load locations
    for x_pos, label, color in [(0, 'A', '#0066CC'), (1.5, 'P₁', '#CC0000'),
                                (3.0, 'B', '#0066CC'), (4.0, 'P₂', '#CC0000')]:
        ax.axvline(x=x_pos, color=color, linestyle='--', alpha=0.7, linewidth=2)
        ax.text(x_pos, ax.get_ylim()[1]*0.85, label, ha='center', va='center',
               fontweight='bold', color=color, fontsize=12,
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.8))

    ax.set_xlabel('Distance from A (m)', fontweight='bold', color='#333333')
    ax.set_ylabel('Bending Moment (N·m)', fontweight='bold', color='#333333')
    ax.set_title('Bending Moment Diagram', fontweight='bold', fontsize=14, color='#333333')
    ax.grid(True, alpha=0.4)
    ax.legend(loc='upper left', fancybox=True, shadow=True)

    ax.set_xlim(-0.2, 4.2)
    ax.set_ylim(-6000, 5000)

    plt.tight_layout()
    plt.savefig('/home/sam/Documents/starlight/siliconwit-com-astro/siliconwit-com/src/content/docs/education/mechanics-of-materials/crane_jib_moment_diagram.png',
                dpi=300, bbox_inches='tight', facecolor='none', edgecolor='none')
    plt.close()

def main():
    """Generate all three diagrams"""
    print("Generating crane jib beam diagrams...")

    print("1. Creating beam loading diagram...")
    create_beam_diagram()
    print("   ✓ Saved: crane_jib_beam_diagram.png")

    print("2. Creating shear force diagram...")
    create_shear_diagram()
    print("   ✓ Saved: crane_jib_shear_diagram.png")

    print("3. Creating bending moment diagram...")
    create_moment_diagram()
    print("   ✓ Saved: crane_jib_moment_diagram.png")

    print("\nAll diagrams generated successfully!")
    print("Files are saved with transparent backgrounds and colors visible on both light/dark themes.")

if __name__ == "__main__":
    main()