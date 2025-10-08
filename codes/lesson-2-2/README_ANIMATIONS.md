# Crane Jib Analysis - Manim Animations

## Overview
This directory contains Manim animations for crane jib bending analysis with 4 scenes:
1. **Scene 1**: Crane jib system (image or animated version)
2. **Scene 2**: Loading diagram with exaggerated bending
3. **Scene 3**: Shear force diagram
4. **Scene 4**: Bending moment diagram

---

## Files

- `manim_crane_jib_anim.py` - Main animation code
- `crane_jib_analysis.py` - Original analysis calculations
- `combine_and_convert.sh` - Helper script for combining videos and creating GIFs
- `double-girder-gantry-crane.png` - Crane image for Scene 1 (place in this directory)

---

## Quick Start

### Option 1: Automated (Recommended)

```bash
# Make sure image file is in this directory
# Run the complete automation script
./combine_and_convert.sh
```

This will:
1. Render all 4 scenes in high quality (1080p60)
2. Combine them into one MP4 file
3. Create lightweight GIF (600px width, 10fps)
4. Create ultra-light GIF (400px width, 8fps)

**Output files:**
```
media/videos/manim_crane_jib_anim/1080p60/
├── crane_jib_complete.mp4           # Combined MP4
├── crane_jib_complete_light.gif     # Lightweight GIF (~2-4 MB)
└── crane_jib_complete_ultralight.gif # Ultra-light GIF (~1-2 MB)
```

---

### Option 2: Manual Step-by-Step

#### Step 1: Place Image File
```bash
# Copy your crane image to this directory
cp /path/to/double-girder-gantry-crane.png .
```

#### Step 2: Render Individual Scenes

**Low quality (fast preview):**
```bash
manim -pql manim_crane_jib_anim.py Scene1_ImageCrane
manim -pql manim_crane_jib_anim.py Scene2_LoadingDiagram
manim -pql manim_crane_jib_anim.py Scene3_ShearDiagram
manim -pql manim_crane_jib_anim.py Scene4_MomentDiagram
```

**High quality (1080p60 - recommended for final output):**
```bash
manim -pqh manim_crane_jib_anim.py Scene1_ImageCrane Scene2_LoadingDiagram Scene3_ShearDiagram Scene4_MomentDiagram
```

**Alternative: Use animated crane instead of image:**
```bash
manim -pqh manim_crane_jib_anim.py Scene1_RealCrane Scene2_LoadingDiagram Scene3_ShearDiagram Scene4_MomentDiagram
```

#### Step 3: Combine Videos into One MP4

```bash
cd media/videos/manim_crane_jib_anim/1080p60

ffmpeg -y -i Scene1_ImageCrane.mp4 -i Scene2_LoadingDiagram.mp4 \
  -i Scene3_ShearDiagram.mp4 -i Scene4_MomentDiagram.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[outv]" \
  -map "[outv]" crane_jib_complete.mp4
```

#### Step 4: Create Lightweight GIF

**Method 1: Light GIF (600px, 10fps) - Recommended**
```bash
ffmpeg -y -i crane_jib_complete.mp4 \
  -vf "fps=10,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  -loop 0 crane_jib_complete_light.gif
```

**Method 2: Ultra-Light GIF (400px, 8fps, 128 colors)**
```bash
ffmpeg -y -i crane_jib_complete.mp4 \
  -vf "fps=8,scale=400:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" \
  -loop 0 crane_jib_complete_ultralight.gif
```

**Method 3: Custom GIF**
```bash
# Adjust parameters as needed:
# - fps: Frame rate (lower = smaller file)
# - scale: Width in pixels (lower = smaller file)
# - max_colors: Color palette size (lower = smaller file)

ffmpeg -y -i crane_jib_complete.mp4 \
  -vf "fps=12,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse" \
  -loop 0 crane_jib_complete_custom.gif
```

---

## Quality Settings

Manim render quality flags:
- `-pql` = 480p @ 15fps (low quality, fast preview)
- `-pqm` = 720p @ 30fps (medium quality)
- `-pqh` = 1080p @ 60fps (high quality, recommended)
- `-pqk` = 2160p @ 60fps (4K quality)

---

## Typical File Sizes

### MP4 (1080p60)
- Individual scene: ~1-3 MB each
- Combined (all 4 scenes): ~6-10 MB

### GIF
- Light (600px, 10fps): ~2-4 MB
- Ultra-light (400px, 8fps, 128 colors): ~1-2 MB
- Custom (800px, 12fps): ~4-6 MB

---

## Scene Descriptions

### Scene 1: Crane System (Image)
- Displays `double-girder-gantry-crane.png`
- Duration: ~3.5 seconds
- Shows realistic crane in industrial setting

**Alternative**: `Scene1_RealCrane` (animated version)
- Animated crane with support joints
- Pinned joint (triangle) and roller joint (circle)
- Loading animations

### Scene 2: Loading Diagram
- Beam with pinned and roller supports
- Point loads P₁ and P₂
- Distributed load w
- Reaction forces R_A and R_B
- Exaggerated bending animation
- Duration: ~10 seconds

### Scene 3: Shear Force Diagram
- Complete shear diagram with 3 regions
- Discontinuities at load points
- Critical values labeled
- Y-axis rotated vertically
- Duration: ~9 seconds

### Scene 4: Bending Moment Diagram
- Smooth moment curve
- Critical points (M_max at x=1.5m, M_min at x=3.0m)
- Color-coded positive/negative regions
- Y-axis rotated vertically
- Duration: ~8 seconds

---

## Troubleshooting

### "ImageMobject: file not found"
- Ensure `double-girder-gantry-crane.png` is in the same directory as the script
- Or provide full path in code: `ImageMobject("/full/path/to/image.png")`

### "ffmpeg: command not found"
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### GIF too large
- Reduce fps: `fps=8` or `fps=10`
- Reduce width: `scale=400:-1` or `scale=500:-1`
- Reduce colors: `max_colors=128` or `max_colors=64`
- Use dithering: `paletteuse=dither=bayer:bayer_scale=5`

### Videos out of sync when combining
- All scenes must have same framerate
- Re-render all with same quality flag (e.g., all `-pqh`)

---

## Tips for Best Results

1. **Use high quality for final output**: Always render with `-pqh` for production
2. **Test with low quality first**: Use `-pql` for quick previews
3. **Optimize GIF size**: Start with light settings, increase only if needed
4. **Keep image aspect ratio**: PNG images work best when aspect ratio matches video (16:9)
5. **Check file sizes**: Use `ls -lh` to monitor output file sizes

---

## Example Workflow

```bash
# 1. Prepare image
cp ~/Pictures/crane.png double-girder-gantry-crane.png

# 2. Quick preview (low quality)
manim -pql manim_crane_jib_anim.py Scene1_ImageCrane

# 3. Render all in high quality
manim -pqh manim_crane_jib_anim.py Scene1_ImageCrane Scene2_LoadingDiagram Scene3_ShearDiagram Scene4_MomentDiagram

# 4. Combine and create GIFs
./combine_and_convert.sh

# 5. Check results
ls -lh media/videos/manim_crane_jib_anim/1080p60/crane_jib_complete*
```

---

## Advanced: Custom Modifications

### Change scene durations
Edit `self.wait(X)` values in each scene's `construct()` method

### Change colors
Modify the `COLORS` dictionary at the top of the file

### Add more scenes
Create new scene classes following the existing pattern

### Export individual frames
```bash
manim -pqh --format=png manim_crane_jib_anim.py Scene1_ImageCrane
# Frames saved to: media/images/manim_crane_jib_anim/
```

---

## Support

For Manim documentation: https://docs.manim.community/
For ffmpeg documentation: https://ffmpeg.org/documentation.html
