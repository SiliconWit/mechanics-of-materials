#!/usr/bin/env python3
"""
Generate static SVG diagrams for common beam types.
These diagrams will be embedded in the lesson content cards.

Author: SiliconWit Mechanics of Materials
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrow, Wedge
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Color scheme matching support_animations.py
COLORS = {
    'beam': '#2d7a8f',           # Darker teal with blue undertone
    'support': '#6B7280',        # Gray for triangles/supports
    'ground': '#5ab9a0',         # Light teal for ground/fixed/outlines
    'force': '#ff8c36',          # Orange for applied forces
    'reaction': '#00a0d0',       # Light blue for reactions
    'text': '#405ab9',           # Blue for text
    'bg': '#F8FAFC'              # Light gray background
}

# Set style for professional technical diagrams (mobile-friendly)
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 32,
    'font.weight': 'bold',
    'axes.linewidth': 4,
    'lines.linewidth': 5,
    'figure.facecolor': 'none',  # Transparent background for SVG
    'axes.facecolor': 'none',
    'savefig.facecolor': 'none',
    'savefig.edgecolor': 'none'
})

def draw_ground(ax, x_center, y_level, width=2.0):
    """Draw ground hatching pattern centered at x_center."""
    x_start = x_center - width/2
    x_end = x_center + width/2

    # Ground line
    ax.plot([x_start, x_end], [y_level, y_level],
            color=COLORS['ground'], linewidth=4)

    # Hatching
    hatch_spacing = 0.25
    hatch_angle = 45
    hatch_length = 0.35
    num_hatches = int(width / hatch_spacing) + 1

    for i in range(num_hatches):
        x = x_start + i * hatch_spacing
        dx = hatch_length * np.cos(np.radians(hatch_angle))
        dy = -hatch_length * np.sin(np.radians(hatch_angle))
        ax.plot([x, x + dx], [y_level, y_level + dy],
               color=COLORS['ground'], linewidth=3)

def draw_pinned_support(ax, x, y, scale=1.0):
    """Draw a pinned support symbol."""
    triangle_height = 0.8 * scale
    triangle_width = 0.8 * scale

    triangle = Polygon([
        [x, y],
        [x - triangle_width/2, y - triangle_height],
        [x + triangle_width/2, y - triangle_height]
    ], closed=True, fc=COLORS['support'], ec=COLORS['ground'], linewidth=4, alpha=0.8)
    ax.add_patch(triangle)

    # Pin circle
    pin = Circle((x, y), 0.18 * scale, fc='black', ec=COLORS['ground'], linewidth=4, zorder=10)
    ax.add_patch(pin)

    # Ground
    draw_ground(ax, x, y - triangle_height, width=2.0)

def draw_roller_support(ax, x, y, scale=1.0):
    """Draw a roller support symbol."""
    triangle_height = 0.8 * scale
    triangle_width = 0.8 * scale

    triangle = Polygon([
        [x, y],
        [x - triangle_width/2, y - triangle_height],
        [x + triangle_width/2, y - triangle_height]
    ], closed=True, fc=COLORS['support'], ec=COLORS['ground'], linewidth=4, alpha=0.8)
    ax.add_patch(triangle)

    # Pin circle at apex
    pin = Circle((x, y), 0.18 * scale, fc='black', ec=COLORS['ground'], linewidth=4, zorder=10)
    ax.add_patch(pin)

    # Rollers (circles)
    roller_y = y - triangle_height - 0.18
    roller1 = Circle((x - 0.25, roller_y), 0.18 * scale,
                    fc='black', ec=COLORS['ground'], linewidth=4, zorder=10)
    roller2 = Circle((x + 0.25, roller_y), 0.18 * scale,
                    fc='black', ec=COLORS['ground'], linewidth=4, zorder=10)
    ax.add_patch(roller1)
    ax.add_patch(roller2)

    # Ground
    draw_ground(ax, x, roller_y - 0.18, width=2.0)

def draw_fixed_support(ax, x, y, scale=1.0):
    """Draw a fixed support symbol."""
    wall_width = 0.5 * scale
    wall_height = 1.2 * scale

    # Wall rectangle
    wall = FancyBboxPatch(
        (x - wall_width, y - wall_height/2),
        wall_width, wall_height,
        boxstyle="round,pad=0.05",
        fc=COLORS['support'], ec=COLORS['ground'], linewidth=4, alpha=0.8
    )
    ax.add_patch(wall)

    # Hatching on the left side of the wall
    hatch_x = x - wall_width
    hatch_spacing = 0.22
    hatch_angle = 45
    hatch_length = 0.3
    num_hatches = int(wall_height / hatch_spacing) + 1

    for i in range(num_hatches):
        y_pos = (y - wall_height/2) + i * hatch_spacing
        dx = -hatch_length * np.cos(np.radians(hatch_angle))
        dy = -hatch_length * np.sin(np.radians(hatch_angle))
        ax.plot([hatch_x, hatch_x + dx], [y_pos, y_pos + dy],
               color=COLORS['ground'], linewidth=3)

def draw_force_arrow(ax, x, y, direction='down', label='', color=None, label_offset=0.3, arrow_length=0.9):
    """Draw a force arrow with label."""
    if color is None:
        color = COLORS['force']

    arrow_width = 0.12

    if direction == 'down':
        dy = -arrow_length
        dx = 0
    elif direction == 'up':
        dy = arrow_length
        dx = 0

    arrow = FancyArrow(x, y, dx, dy,
                      width=arrow_width,
                      head_width=arrow_width*2.2,
                      head_length=arrow_length*0.22,
                      fc=color, ec=color, linewidth=2)
    ax.add_patch(arrow)

    # Add label
    if label:
        if direction == 'down':
            ax.text(x + label_offset, y - arrow_length/2, label,
                   fontsize=28, fontweight='bold', color=color)
        elif direction == 'up':
            ax.text(x + label_offset, y + arrow_length/2, label,
                   fontsize=28, fontweight='bold', color=color)

def draw_udl(ax, x_start, x_end, y, num_arrows=6, label='w', arrow_length=0.7):
    """Draw uniformly distributed load."""
    x_positions = np.linspace(x_start, x_end, num_arrows)
    arrow_width = 0.1

    for x_pos in x_positions:
        arrow = FancyArrow(x_pos, y, 0, -arrow_length,
                          width=arrow_width,
                          head_width=arrow_width*2,
                          head_length=arrow_length*0.2,
                          fc=COLORS['force'], ec=COLORS['force'], linewidth=1.5)
        ax.add_patch(arrow)

    # Label in the middle, closer to arrows
    mid_x = (x_start + x_end) / 2
    ax.text(mid_x, y + 0.15, label, fontsize=26, fontweight='bold',
           color=COLORS['force'], ha='center')

def create_cantilever_beam():
    """Create diagram for cantilever beam (fixed-free)."""
    print("Creating cantilever beam diagram...")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Beam dimensions
    beam_start = 0.0
    beam_end = 6.0
    beam_y = 0.0
    beam_height = 0.35

    # Fixed support dimensions: wall_width=0.5, wall_height=1.2
    # Hatching extends 0.3 to the left
    # Tight bounds: left edge of hatching to right end of beam
    ax.set_xlim(-0.9, 6.2)
    ax.set_ylim(-0.8, 0.8)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw beam
    beam = patches.Rectangle((beam_start, beam_y - beam_height/2), beam_end - beam_start, beam_height,
                             fc=COLORS['beam'], ec=COLORS['ground'], linewidth=3, alpha=0.8)
    ax.add_patch(beam)

    # Fixed support at left end
    draw_fixed_support(ax, beam_start, beam_y, scale=1.0)

    # Add length label L with dimension line at BOTTOM
    dim_y = beam_y - beam_height/2 - 0.5
    ax.plot([beam_start, beam_end], [dim_y, dim_y], color=COLORS['text'], linewidth=2)
    ax.plot([beam_start, beam_start], [dim_y - 0.1, dim_y + 0.1], color=COLORS['text'], linewidth=2)
    ax.plot([beam_end, beam_end], [dim_y - 0.1, dim_y + 0.1], color=COLORS['text'], linewidth=2)
    ax.text((beam_start + beam_end)/2, dim_y - 0.25, 'L', fontsize=28, fontweight='bold',
           color=COLORS['text'], ha='center')

    # Add x label (distance from fixed end) - moved up
    x_pos = beam_end * 0.6
    ax.text(x_pos, beam_y - beam_height/2 - 0.2, 'x', fontsize=26, fontweight='bold',
           color=COLORS['text'], ha='center', style='italic')

    # Add uniformly distributed load w along the beam (shorter arrows, adjusted positioning)
    udl_y = beam_y + beam_height/2 + 0.26
    draw_udl(ax, beam_start + 0.5, beam_end - 0.5, udl_y, num_arrows=8, label='w', arrow_length=0.2)

    # Add point load P at free end (shorter arrow)
    draw_force_arrow(ax, beam_end, beam_y + beam_height/2, 'down', 'P', arrow_length=0.6)

    # Add reaction Ry as upward arrow below fixed support
    draw_force_arrow(ax, beam_start, beam_y - beam_height/2 - 0.8, 'up', 'Ry', color=COLORS['reaction'])

    plt.tight_layout()
    output_path = os.path.join(SCRIPT_DIR, 'cantilever_beam.svg')
    plt.savefig(output_path, format='svg', bbox_inches='tight', transparent=True)
    plt.close()
    print(f"✓ Created: {output_path}")

def create_simply_supported_beam():
    """Create diagram for simply supported beam (pin-roller)."""
    print("Creating simply supported beam diagram...")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Beam dimensions
    beam_start = 0.5
    beam_end = 7.0
    beam_y = 0.0
    beam_height = 0.35

    # Pinned support: triangle_height=0.8, ground extends 1.0 on each side
    # Roller support: triangle_height=0.8, rollers=0.18, ground extends 1.0 on each side
    # Total height needed: beam center to ground hatching bottom
    # Ground is at y - 0.8 - 0.35 (for rollers) ≈ -1.16 with hatching
    # Tight bounds: minimal padding around supports
    ax.set_xlim(-0.6, 8.1)
    ax.set_ylim(-1.5, 0.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw beam
    beam = patches.Rectangle((beam_start, beam_y - beam_height/2), beam_end - beam_start, beam_height,
                             fc=COLORS['beam'], ec=COLORS['ground'], linewidth=3, alpha=0.8)
    ax.add_patch(beam)

    # Pinned support at left
    draw_pinned_support(ax, beam_start, beam_y, scale=1.0)

    # Roller support at right
    draw_roller_support(ax, beam_end, beam_y, scale=1.0)

    # Add length label L with dimension line at BOTTOM
    dim_y = beam_y - 1.3
    ax.plot([beam_start, beam_end], [dim_y, dim_y], color=COLORS['text'], linewidth=2)
    ax.plot([beam_start, beam_start], [dim_y - 0.1, dim_y + 0.1], color=COLORS['text'], linewidth=2)
    ax.plot([beam_end, beam_end], [dim_y - 0.1, dim_y + 0.1], color=COLORS['text'], linewidth=2)
    ax.text((beam_start + beam_end)/2, dim_y - 0.25, 'L', fontsize=28, fontweight='bold',
           color=COLORS['text'], ha='center')

    # Add x label (distance from left support) - moved up
    x_pos = beam_start + (beam_end - beam_start) * 0.6
    ax.text(x_pos, beam_y - beam_height/2 - 0.25, 'x', fontsize=26, fontweight='bold',
           color=COLORS['text'], ha='center', style='italic')

    # Add central point load P (arrow tip just touches beam upper surface)
    center_x = (beam_start + beam_end) / 2
    draw_force_arrow(ax, center_x, beam_y + beam_height/1 + 0.6, 'down', 'P', arrow_length=0.6)

    # Add reaction labels RA and RB (moved down further to avoid overlap)
    ax.text(beam_start, beam_y - 1.7, 'RA', fontsize=24, fontweight='bold',
           color=COLORS['reaction'], ha='center')
    ax.text(beam_end, beam_y - 1.7, 'RB', fontsize=24, fontweight='bold',
           color=COLORS['reaction'], ha='center')

    plt.tight_layout()
    output_path = os.path.join(SCRIPT_DIR, 'simply_supported_beam.svg')
    plt.savefig(output_path, format='svg', bbox_inches='tight', transparent=True)
    plt.close()
    print(f"✓ Created: {output_path}")

def create_overhanging_beam():
    """Create diagram for overhanging beam."""
    print("Creating overhanging beam diagram...")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Beam dimensions
    beam_start = 0.5
    beam_end = 8.0
    support1_x = 1.5
    support2_x = 6.0
    beam_y = 0.0
    beam_height = 0.35

    # Overhanging beam with pinned and roller supports
    # Tight bounds: beam start to beam end horizontally, supports vertically
    ax.set_xlim(0.0, 8.5)
    ax.set_ylim(-1.6, 0.6)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw beam (extends beyond supports)
    beam = patches.Rectangle((beam_start, beam_y - beam_height/2), beam_end - beam_start, beam_height,
                             fc=COLORS['beam'], ec=COLORS['ground'], linewidth=3, alpha=0.8)
    ax.add_patch(beam)

    # Pinned support
    draw_pinned_support(ax, support1_x, beam_y, scale=1.0)

    # Roller support
    draw_roller_support(ax, support2_x, beam_y, scale=1.0)

    # Add length label L with dimension line at BOTTOM (total beam length)
    dim_y = beam_y - 1.3
    ax.plot([beam_start, beam_end], [dim_y, dim_y], color=COLORS['text'], linewidth=2)
    ax.plot([beam_start, beam_start], [dim_y - 0.1, dim_y + 0.1], color=COLORS['text'], linewidth=2)
    ax.plot([beam_end, beam_end], [dim_y - 0.1, dim_y + 0.1], color=COLORS['text'], linewidth=2)
    ax.text((beam_start + beam_end)/2, dim_y - 0.25, 'L', fontsize=28, fontweight='bold',
           color=COLORS['text'], ha='center')

    # Add x label (distance from left end)
    x_pos = beam_start + (beam_end - beam_start) * 0.6
    ax.text(x_pos, dim_y + 0.85, 'x', fontsize=26, fontweight='bold',
           color=COLORS['text'], ha='center', style='italic')

    # Add uniformly distributed load w across entire beam length (same as cantilever)
    udl_y = beam_y + beam_height/2 + 0.26
    draw_udl(ax, beam_start + 0.5, beam_end - 0.5, udl_y, num_arrows=8, label='w', arrow_length=0.2)

    # Add reaction labels RA and RB (moved down further to avoid overlap)
    ax.text(support1_x, beam_y - 1.7, 'RA', fontsize=24, fontweight='bold',
           color=COLORS['reaction'], ha='center')
    ax.text(support2_x, beam_y - 1.7, 'RB', fontsize=24, fontweight='bold',
           color=COLORS['reaction'], ha='center')

    plt.tight_layout()
    output_path = os.path.join(SCRIPT_DIR, 'overhanging_beam.svg')
    plt.savefig(output_path, format='svg', bbox_inches='tight', transparent=True)
    plt.close()
    print(f"✓ Created: {output_path}")

def main():
    """Generate all beam type diagrams."""
    print("\n" + "="*60)
    print("Generating Common Beam Type Diagrams")
    print("="*60 + "\n")

    create_cantilever_beam()
    create_simply_supported_beam()
    create_overhanging_beam()

    print("\n" + "="*60)
    print("✓ All beam diagrams generated successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
