import os
from moviepy.editor import ImageClip
from PIL import Image

# ------------------------------------------------------------------
# 🧩 Pillow compatibility patch (for Pillow >=10)
# MoviePy 1.0.3 still expects Image.ANTIALIAS, which was removed.
# This ensures compatibility without downgrading Pillow.
# ------------------------------------------------------------------
if not hasattr(Image, "ANTIALIAS"):
    try:
        Image.ANTIALIAS = Image.Resampling.LANCZOS
    except Exception:
        pass

# ------------------------------------------------------------------
# 🖼️ Video generation function
# ------------------------------------------------------------------

OUTPUT_DIR = "output"

def generate_video_from_image(image_filename: str, duration: int = 30):
    """
    Generate a vertical 1080x1920 video from a still image with fade-in.
    Works cross-platform (Windows & Docker) using MoviePy.
    """

    # Validate input paths
    image_path = os.path.join(OUTPUT_DIR, image_filename)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    video_filename = image_filename.replace(".png", ".mp4")
    video_path = os.path.join(OUTPUT_DIR, video_filename)

    try:
        # Create the image clip
        clip = ImageClip(image_path)
        clip = clip.set_duration(duration)   # duration must come first
        clip = clip.fadein(1.0)              # 1-second fade-in animation
        clip = clip.resize(height=1920)      # maintain aspect ratio
        clip = clip.set_position("center")   # center on canvas

        # Export video
        clip.write_videofile(
            video_path,
            fps=30,
            codec="libx264",
            audio=False,
            threads=4,
            preset="medium"
        )

        clip.close()
        return video_filename

    except Exception as e:
        print(f"❌ Video generation error: {e}")
        raise
