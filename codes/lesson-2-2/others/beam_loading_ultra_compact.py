#!/usr/bin/env python3
"""
Ultra-Compact Beam Loading Diagram - Maximum Mobile Optimization
ULTRA-COMPACT SPECIFICATIONS:
- Even larger text for mobile visibility
- Use same color as 'w' for all invisible text
- UDL arrows height reduced by half
- P1/P2 arrows reduced to 3/4 height
- Move P1/P2 and w labels down
- Move R_A, R_B labels up
- Reduce beam thickness to 3/4
- Minimize ALL unused vertical space
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as path_effects

def setup_style():
    """Configure matplotlib with ultra-compact mobile-optimized styling"""
    colors = {
        'teal': '#2A9D8F',
        'golden_yellow': '#F4D03F',
        'slate_blue': '#5DADE2',      # This is the 'w' color - use for all text
        'warm_gray': '#BDC3C7',
        'outline_color': '#F8F9FA',
    }

    plt.style.use('default')
    plt.rcParams.update({
        'figure.facecolor': 'none',
        'axes.facecolor': 'none',
        'savefig.facecolor': 'none',
        'savefig.edgecolor': 'none',
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'sans-serif'],
        'font.size': 28,  # Larger for mobile
        'font.weight': 'normal',
        'axes.linewidth': 3.0,
        'lines.linewidth': 5.0,
        'patch.linewidth': 3.0,
    })

    return colors

def add_visible_text(ax, x, y, text, color, fontsize=28, ha='center', va='center',
                    fontweight='normal', outline_width=0):
    """Add text without outline, larger size, non-bold"""
    text_obj = ax.text(x, y, text, ha=ha, va=va, fontsize=fontsize,
                      fontweight=fontweight, color=color, zorder=10)

    # No outline for text
    return text_obj

def create_ultra_compact_diagram():
    """Create ultra-compact beam loading diagram"""
    colors = setup_style()

    # LARGER for mobile visibility
    fig, ax = plt.subplots(figsize=(18, 10))  # Wider but shorter

    # REDUCED: Beam thickness to 3/4
    beam_height = 0.22  # Reduced from 0.3 to 0.22 (3/4)
    beam_y = 0

    # Enhanced beam with reduced thickness
    beam = FancyBboxPatch((0, beam_y - beam_height/2), 4.0, beam_height,
                         boxstyle="round,pad=0.01",
                         linewidth=3.0, edgecolor=colors['slate_blue'],
                         facecolor=colors['warm_gray'], alpha=0.8)
    ax.add_patch(beam)

    # Support A (pinned) - proportionally adjusted
    support_size = 0.14  # Slightly smaller
    triangle_a = patches.Polygon([(0, beam_y - beam_height/2),
                                 (-support_size, beam_y - beam_height/2 - support_size),
                                 (support_size, beam_y - beam_height/2 - support_size)],
                                closed=True, facecolor=colors['slate_blue'],
                                edgecolor=colors['slate_blue'], linewidth=2.5, alpha=0.9)
    ax.add_patch(triangle_a)

    # Support base
    ax.plot([-support_size*1.2, support_size*1.2],
           [beam_y - beam_height/2 - support_size, beam_y - beam_height/2 - support_size],
           color=colors['slate_blue'], linewidth=4, alpha=0.9, zorder=3)

    # Support B (roller)
    circle_b = patches.Circle((3.0, beam_y - beam_height/2 - support_size/2), support_size/2,
                             facecolor=colors['slate_blue'], edgecolor=colors['slate_blue'],
                             linewidth=2.5, alpha=0.9)
    ax.add_patch(circle_b)

    # Roller base
    ax.plot([3.0-support_size, 3.0+support_size],
           [beam_y - beam_height/2 - support_size, beam_y - beam_height/2 - support_size],
           color=colors['slate_blue'], linewidth=4, alpha=0.9, zorder=3)

    # MOVED UP: Reaction forces
    arrow_props = dict(arrowstyle='->', lw=6.0, color=colors['teal'])

    # R_A - moved up significantly
    ax.annotate('', xy=(0, beam_y - beam_height/2), xytext=(0, beam_y - beam_height/2 - 0.5),
                arrowprops=arrow_props, zorder=4)
    add_visible_text(ax, 0, beam_y - beam_height/2 - 0.7, 'R_A',
                    colors['slate_blue'], fontsize=30, va='top')  # Using slate_blue like 'w'

    # R_B - moved up significantly
    ax.annotate('', xy=(3.0, beam_y - beam_height/2), xytext=(3.0, beam_y - beam_height/2 - 0.5),
                arrowprops=arrow_props, zorder=4)
    add_visible_text(ax, 3.0, beam_y - beam_height/2 - 0.7, 'R_B',
                    colors['slate_blue'], fontsize=30, va='top')  # Using slate_blue like 'w'

    # REDUCED: Applied loads to 3/4 height and moved down
    load_arrow_props = dict(arrowstyle='->', lw=6.0, color=colors['golden_yellow'])

    # P₁ = 5000 N (3/4 height, moved down more)
    p1_height = 0.52  # 3/4 of original ~0.7
    ax.annotate('', xy=(1.5, beam_y + beam_height/2), xytext=(1.5, beam_y + beam_height/2 + p1_height),
                arrowprops=load_arrow_props, zorder=4)
    add_visible_text(ax, 1.5, beam_y + beam_height/2 + p1_height + 0.15, 'P₁ = 5000 N',
                    colors['golden_yellow'], fontsize=30, va='bottom')

    # P₂ = 3000 N (3/4 height, moved down more)
    ax.annotate('', xy=(4.0, beam_y + beam_height/2), xytext=(4.0, beam_y + beam_height/2 + p1_height),
                arrowprops=load_arrow_props, zorder=4)
    add_visible_text(ax, 4.0, beam_y + beam_height/2 + p1_height + 0.15, 'P₂ = 3000 N',
                    colors['golden_yellow'], fontsize=30, va='bottom')

    # REDUCED: Distributed load arrows to half height
    udl_height = 0.175  # Half of original ~0.35
    x_dist = np.linspace(0, 4.0, 25)
    for xi in x_dist:
        ax.annotate('', xy=(xi, beam_y + beam_height/2), xytext=(xi, beam_y + beam_height/2 + udl_height),
                    arrowprops=dict(arrowstyle='->', lw=2.5, color=colors['slate_blue']), zorder=3)

    # MOVED DOWN: Distributed load label
    add_visible_text(ax, 2.0, beam_y + beam_height/2 + udl_height + 0.1, 'w = 800 N/m',
                    colors['slate_blue'], fontsize=28, va='bottom')

    # ALL TEXT USING SLATE_BLUE COLOR (same as 'w')
    add_visible_text(ax, 0, beam_y - beam_height/2 - 0.25, 'A\n(Pinned)',
                    colors['slate_blue'], fontsize=24, va='top')
    add_visible_text(ax, 3.0, beam_y - beam_height/2 - 0.25, 'B\n(Roller)',
                    colors['slate_blue'], fontsize=24, va='top')
    add_visible_text(ax, 4.0, beam_y - beam_height/2 - 0.2, 'Free End',
                    colors['slate_blue'], fontsize=24, va='top')

    # Position markers using slate_blue
    for x_pos, label in [(0, '0'), (1.5, '1.5'), (3.0, '3.0'), (4.0, '4.0')]:
        ax.axvline(x=x_pos, color=colors['warm_gray'], linestyle=':', alpha=0.6, linewidth=2.0)
        add_visible_text(ax, x_pos, -1.0, f'{label} m', colors['slate_blue'],
                        fontsize=24, va='top')

    # ULTRA-COMPACT: Extremely tight bounds
    ax.set_xlim(-0.25, 4.25)
    ax.set_ylim(-1.2, 1.0)  # Much tighter - removed almost all unused space

    # Remove all axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    output_path = '/home/sam/Documents/starlight/siliconwit-com-astro/siliconwit-com/src/content/docs/education/mechanics-of-materials/codes/lesson-2-2/crane_jib_loading_diagram.svg'
    plt.savefig(output_path, format='svg', bbox_inches='tight', facecolor='none', edgecolor='none',
                transparent=True, pad_inches=0.01)  # Minimal padding
    plt.close()
    return output_path

def main():
    print("🔧 Creating ULTRA-COMPACT beam loading diagram...")
    print("✅ ULTRA-COMPACT SPECIFICATIONS:")
    print("   • Even larger text (24-26px) for mobile")
    print("   • All text using slate_blue color (same as 'w')")
    print("   • UDL arrows reduced to half height")
    print("   • P1/P2 arrows reduced to 3/4 height")
    print("   • Labels moved down (P1/P2/w) and up (R_A/R_B)")
    print("   • Beam thickness reduced to 3/4")
    print("   • Minimized ALL unused vertical space")

    try:
        beam_path = create_ultra_compact_diagram()
        print(f"   ✓ Saved: {beam_path.split('/')[-1]}")
        print("\\n🎉 Ultra-compact mobile-optimized diagram generated!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()