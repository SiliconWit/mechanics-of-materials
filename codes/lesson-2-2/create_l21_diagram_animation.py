#!/usr/bin/env python3
"""
General-purpose script to create animated GIFs alternating between text and images.
Supports PNG and SVG image formats.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import cairosvg
from io import BytesIO


def get_font(font_size):
    """
    Get a font object with the specified size.

    Args:
        font_size: Font size in points

    Returns:
        PIL ImageFont object
    """
    # Get the path to the IBM Plex Sans fonts
    # Navigate up from the current script to the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '../../../../../..'))

    font_paths = [
        # IBM Plex Sans fonts (SemiBold for headings as per typography.css)
        os.path.join(project_root, 'public/fonts/IBM_Plex_Sans/static/IBMPlexSans-SemiBold.ttf'),
        os.path.join(project_root, 'public/fonts/IBM_Plex_Sans/static/IBMPlexSans-Bold.ttf'),
        os.path.join(project_root, 'public/fonts/IBM_Plex_Sans/static/IBMPlexSans-Medium.ttf'),
        # Fallback to system fonts if IBM Plex is not found
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ]

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            continue

    return ImageFont.load_default()


def create_text_frame(text, width=1920, height=1080, bg_color="#F8FAFC",
                      text_color="black", font_size=None, show_cursor=False):
    """
    Create a frame with centered, styled text on a colored background.

    Args:
        text: Text to display
        width: Frame width in pixels
        height: Frame height in pixels
        bg_color: Background color
        text_color: Text color
        font_size: Font size in points (if None, auto-calculated based on frame size)
        show_cursor: Whether to show a blinking cursor at the end

    Returns:
        PIL Image object
    """
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Auto-calculate font size based on frame dimensions if not specified
    if font_size is None:
        font_size = int(min(width, height) * 0.08)  # 8% of smaller dimension

    font = get_font(font_size)

    # Get full text bounding box for centering (even when showing partial text)
    # We'll center based on the full text to avoid shifting
    full_text = text if text else " "
    bbox = draw.textbbox((0, 0), full_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate position to center text
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Draw subtle shadow for depth (offset by 3 pixels)
    shadow_color = "#CCCCCC"
    shadow_offset = 3
    if text:
        draw.text((x + shadow_offset, y + shadow_offset), text, fill=shadow_color, font=font)

    # Draw main text
    if text:
        draw.text((x, y), text, fill=text_color, font=font)

    # Draw cursor if requested
    if show_cursor and text:
        cursor_bbox = draw.textbbox((0, 0), text, font=font)
        cursor_x = x + (cursor_bbox[2] - cursor_bbox[0]) + 5
        cursor_y1 = y
        cursor_y2 = y + text_height
        draw.line([(cursor_x, cursor_y1), (cursor_x, cursor_y2)], fill=text_color, width=4)

    return img


def create_typing_animation_frames(text, width=1920, height=1080, bg_color="#F8FAFC",
                                   text_color="black", font_size=None,
                                   chars_per_frame=1, final_pause_frames=3):
    """
    Create multiple frames showing a typing animation effect.

    Args:
        text: Full text to type out
        width: Frame width in pixels
        height: Frame height in pixels
        bg_color: Background color
        text_color: Text color
        font_size: Font size in points (if None, auto-calculated)
        chars_per_frame: Number of characters to reveal per frame
        final_pause_frames: Number of frames to pause on final text

    Returns:
        List of PIL Image objects
    """
    frames = []

    # Auto-calculate font size if not specified
    if font_size is None:
        font_size = int(min(width, height) * 0.08)

    # Create frames for typing animation
    for i in range(0, len(text) + 1, chars_per_frame):
        partial_text = text[:i]
        show_cursor = i < len(text)
        frame = create_text_frame(
            partial_text,
            width=width,
            height=height,
            bg_color=bg_color,
            text_color=text_color,
            font_size=font_size,
            show_cursor=show_cursor
        )
        frames.append(frame)

    # Add pause frames at the end with full text (no cursor)
    final_frame = create_text_frame(
        text,
        width=width,
        height=height,
        bg_color=bg_color,
        text_color=text_color,
        font_size=font_size,
        show_cursor=False
    )
    for _ in range(final_pause_frames):
        frames.append(final_frame)

    return frames


def get_image_dimensions(filepath):
    """
    Get the dimensions of an image file without loading the full image.

    Args:
        filepath: Path to the image file

    Returns:
        Tuple of (width, height)
    """
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == '.svg':
        # For SVG, we need to convert to get actual dimensions
        png_data = cairosvg.svg2png(url=filepath)
        img = Image.open(BytesIO(png_data))
        return img.size
    else:
        # For other formats, just open and get size
        with Image.open(filepath) as img:
            return img.size


def load_image(filepath, target_width=1920, target_height=1080, bg_color="#F8FAFC",
               scale_small_images=True):
    """
    Load an image file (PNG or SVG) and fit to target dimensions with specified background.

    Args:
        filepath: Path to the image file
        target_width: Target width in pixels
        target_height: Target height in pixels
        bg_color: Background color for padding
        scale_small_images: If True, scale up images that are much smaller than target

    Returns:
        PIL Image object
    """
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == '.svg':
        # Convert SVG to PNG in memory
        png_data = cairosvg.svg2png(url=filepath)
        img = Image.open(BytesIO(png_data))
    else:
        # Load PNG or other formats directly
        img = Image.open(filepath)

    # Handle transparency by compositing onto white background
    if img.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', img.size, bg_color)
        if img.mode == 'P':
            img = img.convert('RGBA')
        # Paste image onto white background using alpha channel as mask
        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Scale image to better fill the frame if it's significantly smaller
    if scale_small_images:
        # Calculate how much smaller the image is compared to target
        width_ratio = img.width / target_width
        height_ratio = img.height / target_height

        # If image is less than 40% of target dimensions, scale it up
        # Scale to use about 80% of the available space
        if width_ratio < 0.4 or height_ratio < 0.4:
            scale = min(target_width * 0.8 / img.width, target_height * 0.8 / img.height)
            new_width = int(img.width * scale)
            new_height = int(img.height * scale)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a canvas with target dimensions
    result = Image.new('RGB', (target_width, target_height), color=bg_color)

    # Center the image on the canvas
    x_offset = (target_width - img.width) // 2
    y_offset = (target_height - img.height) // 2
    result.paste(img, (x_offset, y_offset))

    return result


def add_watermark(img, text="SiliconWit.COM", opacity=0.15, font_size=None):
    """
    Add a semi-transparent watermark to an image.

    Args:
        img: PIL Image object
        text: Watermark text
        opacity: Opacity level (0.0 = fully transparent, 1.0 = fully opaque)
        font_size: Font size (if None, auto-calculated based on image size)

    Returns:
        PIL Image object with watermark
    """
    # Create a copy to work with
    watermarked = img.copy()

    # Create a transparent overlay
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Auto-calculate font size if not specified
    if font_size is None:
        font_size = int(min(img.width, img.height) * 0.05)  # 5% of smaller dimension

    # Get font
    font = get_font(font_size)

    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (img.width - text_width) / 2
    y = (img.height - text_height) / 2

    # Calculate alpha value (0-255)
    alpha = int(255 * opacity)

    # Draw watermark text with transparency
    draw.text((x, y), text, fill=(128, 128, 128, alpha), font=font)

    # Convert original image to RGBA for compositing
    if watermarked.mode != 'RGBA':
        watermarked = watermarked.convert('RGBA')

    # Composite the overlay onto the image
    watermarked = Image.alpha_composite(watermarked, overlay)

    # Convert back to RGB
    watermarked = watermarked.convert('RGB')

    return watermarked


def add_border(img, border_width=10, border_color="teal"):
    """
    Add a border around an image.

    Args:
        img: PIL Image object
        border_width: Width of the border in pixels
        border_color: Color of the border

    Returns:
        PIL Image object with border
    """
    # Create a new image with border
    new_width = img.width + 2 * border_width
    new_height = img.height + 2 * border_width
    bordered = Image.new('RGB', (new_width, new_height), color=border_color)

    # Paste original image in the center
    bordered.paste(img, (border_width, border_width))

    return bordered


def create_animation(frames_config, output_path, duration=2000, loop=0,
                     width=None, height=None, typing_animation=True,
                     typing_frame_duration=100, border_width=0, border_color="teal",
                     watermark_text=None, watermark_opacity=0.15):
    """
    Create an animated GIF from a sequence of text and image frames.

    Args:
        frames_config: List of dictionaries, each with 'type' ('text' or 'image')
                      and corresponding 'text' or 'path' key
        output_path: Path to save the output GIF
        duration: Duration of each image frame in milliseconds
        loop: Number of loops (0 = infinite)
        width: Frame width in pixels (if None, auto-detect from images)
        height: Frame height in pixels (if None, auto-detect from images)
        typing_animation: Whether to animate text with typing effect
        typing_frame_duration: Duration of each typing frame in milliseconds
        border_width: Width of border around entire GIF in pixels (0 = no border)
        border_color: Color of the border
        watermark_text: Text for watermark (None = no watermark)
        watermark_opacity: Opacity of watermark (0.0 to 1.0)
    """
    # Auto-detect dimensions from all images if not specified
    if width is None or height is None:
        print("Detecting maximum dimensions from all images...")
        max_width = 0
        max_height = 0

        for config in frames_config:
            if config['type'] == 'image':
                img_width, img_height = get_image_dimensions(config['path'])
                max_width = max(max_width, img_width)
                max_height = max(max_height, img_height)
                print(f"  {os.path.basename(config['path'])}: {img_width}x{img_height}")

        width = max_width
        height = max_height
        print(f"Using dimensions: {width}x{height}\n")

    frames = []
    frame_durations = []
    frame_watermarks = []  # Track which frames should have watermarks

    for i, config in enumerate(frames_config):
        print(f"Processing frame {i+1}/{len(frames_config)}: ", end="")
        should_watermark = config.get('watermark', True)  # Default to True if not specified

        if config['type'] == 'text':
            print(f"Text - '{config['text']}'")
            if typing_animation:
                # Create typing animation frames
                text_frames = create_typing_animation_frames(
                    config['text'],
                    width=width,
                    height=height,
                    bg_color=config.get('bg_color', 'white'),
                    text_color=config.get('text_color', 'black'),
                    font_size=config.get('font_size', None),
                    chars_per_frame=config.get('chars_per_frame', 1),
                    final_pause_frames=config.get('final_pause_frames', 3)
                )
                frames.extend(text_frames)
                # Add durations for each typing frame
                frame_durations.extend([typing_frame_duration] * len(text_frames))
                # Track watermark for all typing frames
                frame_watermarks.extend([should_watermark] * len(text_frames))
                print(f" ({len(text_frames)} typing frames)")
            else:
                frame = create_text_frame(
                    config['text'],
                    width=width,
                    height=height,
                    bg_color=config.get('bg_color', 'white'),
                    text_color=config.get('text_color', 'black'),
                    font_size=config.get('font_size', None)
                )
                frames.append(frame)
                frame_durations.append(duration)
                frame_watermarks.append(should_watermark)
        elif config['type'] == 'image':
            print(f"Image - {os.path.basename(config['path'])}")
            frame = load_image(
                config['path'],
                target_width=width,
                target_height=height,
                bg_color=config.get('bg_color', 'white'),
                scale_small_images=config.get('scale_small_images', True)
            )
            frames.append(frame)
            frame_durations.append(duration)
            frame_watermarks.append(should_watermark)
        else:
            raise ValueError(f"Unknown frame type: {config['type']}")

    # Add watermark to frames selectively if requested
    if watermark_text:
        watermarked_count = sum(frame_watermarks)
        print(f"\nAdding watermark '{watermark_text}' (opacity: {watermark_opacity}) to {watermarked_count}/{len(frames)} frames...")
        frames = [add_watermark(frame, watermark_text, watermark_opacity) if should_wm else frame
                  for frame, should_wm in zip(frames, frame_watermarks)]

    # Add border to all frames if requested
    if border_width > 0:
        print(f"\nAdding {border_width}px {border_color} border to all frames...")
        frames = [add_border(frame, border_width, border_color) for frame in frames]

    # Save as animated GIF with per-frame durations
    print(f"\nSaving animation to {output_path}...")
    print(f"Total frames: {len(frames)}")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_durations,
        loop=loop,
        optimize=False
    )
    print(f"Animation saved successfully!")


def main():
    """Main function to create the crane jib analysis animation."""

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the sequence of frames
    bg_color = '#F8FAFC'  # Light grayish-blue background
    frames = [
        {'type': 'text', 'text': 'Real World System', 'text_color': '#405ab9', 'watermark': False, 'bg_color': bg_color},
        {'type': 'image', 'path': os.path.join(script_dir, 'conveyor-beam-loads.png'), 'watermark': False, 'bg_color': bg_color},
        {'type': 'text', 'text': 'Equivalent System Model', 'text_color': '#405ab9', 'watermark': False, 'bg_color': bg_color},
        {'type': 'image', 'path': os.path.join(script_dir, 'conveyor-beam-supports-spaced-boxes.png'), 'watermark': True, 'bg_color': bg_color},
        {'type': 'text', 'text': 'Shear Force Plot', 'text_color': '#405ab9', 'watermark': False, 'bg_color': bg_color},
        {'type': 'image', 'path': os.path.join(script_dir, 'conveyor_beam_shear_diagram.svg'), 'watermark': True, 'bg_color': bg_color},
        {'type': 'text', 'text': 'Bending Moment Plot', 'text_color': '#405ab9', 'watermark': False, 'bg_color': bg_color},
        {'type': 'image', 'path': os.path.join(script_dir, 'conveyor_beam_moment_diagram.svg'), 'watermark': True, 'bg_color': bg_color},
    ]

    # Output path
    output_path = os.path.join(script_dir, 'conveyor-beam-analysis-animation.gif')

    # Create the animation (width and height auto-detected from images)
    create_animation(
        frames_config=frames,
        output_path=output_path,
        duration=2000,  # 2 seconds per frame
        loop=0,  # Infinite loop
        border_width=15,  # 15px border
        border_color="#40E0D0",  # Bright turquoise/teal
        watermark_text="SiliconWit.COM",  # Centered watermark
        watermark_opacity=0.15  # Almost transparent (15% opacity)
    )


if __name__ == '__main__':
    main()
