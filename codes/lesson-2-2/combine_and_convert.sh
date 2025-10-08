#!/bin/bash
# Script to combine Manim scenes and create lightweight GIF

# Configuration
QUALITY="1080p60"  # Options: 480p15, 720p30, 1080p60, 2160p60
VIDEO_DIR="media/videos/manim_crane_jib_anim/$QUALITY"
OUTPUT_NAME="crane_jib_complete"

# Step 1: Render all scenes in high quality
echo "Step 1: Rendering all scenes..."
manim -pqh manim_crane_jib_anim.py Scene1_ImageCrane Scene2_LoadingDiagram Scene3_ShearDiagram Scene4_MomentDiagram

# Step 2: Combine all MP4s into one
echo ""
echo "Step 2: Combining all MP4 files..."
cd "$VIDEO_DIR" || exit

ffmpeg -y -i Scene1_ImageCrane.mp4 -i Scene2_LoadingDiagram.mp4 -i Scene3_ShearDiagram.mp4 -i Scene4_MomentDiagram.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[outv]" \
  -map "[outv]" \
  "${OUTPUT_NAME}.mp4"

echo "Combined MP4 created: ${VIDEO_DIR}/${OUTPUT_NAME}.mp4"

# Step 3: Create lightweight GIF
echo ""
echo "Step 3: Creating lightweight GIF..."

# Method 1: High quality, smaller file (recommended)
ffmpeg -y -i "${OUTPUT_NAME}.mp4" \
  -vf "fps=10,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  -loop 0 \
  "${OUTPUT_NAME}_light.gif"

echo "Lightweight GIF created: ${VIDEO_DIR}/${OUTPUT_NAME}_light.gif"

# Optional: Create even smaller GIF (very light)
echo ""
echo "Step 4 (optional): Creating ultra-light GIF..."
ffmpeg -y -i "${OUTPUT_NAME}.mp4" \
  -vf "fps=8,scale=400:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" \
  -loop 0 \
  "${OUTPUT_NAME}_ultralight.gif"

echo "Ultra-light GIF created: ${VIDEO_DIR}/${OUTPUT_NAME}_ultralight.gif"

# Show file sizes
echo ""
echo "=== File Sizes ==="
ls -lh "${OUTPUT_NAME}"*

echo ""
echo "=== Done! ==="
echo "All files are in: ${VIDEO_DIR}/"
