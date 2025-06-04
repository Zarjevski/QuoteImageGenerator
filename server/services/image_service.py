import os
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageOps
from config import OUTPUT_DIR, FONT_PATH, INSTAGRAM_ICON_PATH, BRAND_NAME
from utils.text_utils import is_hebrew

def generate_image(data):
    quote = data.get("quote")
    thinker_display_name = data.get("thinker")           # Hebrew/English author name for text
    image_folder = data.get("imageFolder")               # English folder name for loading
    image_name = data.get("image")

    if not all([quote, thinker_display_name, image_folder, image_name]):
        raise ValueError("Missing required fields")

    image_path = os.path.join("data/images", image_folder, image_name)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    background = Image.open(image_path).convert("RGBA")
    W, H = background.size
    padding = 60

    faded = Image.new("RGBA", background.size, (0, 0, 0, 230))
    background = Image.alpha_composite(background, faded)
    overlay = Image.new("RGBA", background.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        quote_font = ImageFont.truetype(FONT_PATH, size=56)
        name_font = ImageFont.truetype(FONT_PATH, size=36)
        brand_font = ImageFont.truetype(FONT_PATH, size=24)
    except:
        quote_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()

    max_width = W - 2 * padding
    rtl = is_hebrew(quote)
    words = quote.split()
    line = ""
    wrapped_lines = []

    for word in words:
        test_line = (line + " " + word) if line else word
        bbox = draw.textbbox((0, 0), test_line, font=quote_font, direction="rtl" if rtl else "ltr", features=["-liga"])
        line_width = bbox[2] - bbox[0]
        if line_width <= max_width:
            line = test_line
        else:
            wrapped_lines.append(line.strip())
            line = word
    if line:
        wrapped_lines.append(line.strip())

    line_heights = [draw.textbbox((0, 0), line, font=quote_font, direction="rtl" if rtl else "ltr", features=["-liga"])[3]
                    for line in wrapped_lines]
    line_spacing = 10
    author_spacing = 40
    total_quote_height = sum(line_heights) + (len(line_heights) - 1) * line_spacing
    start_y = (H - total_quote_height) // 2
    current_y = start_y

    for i, line in enumerate(wrapped_lines):
        bbox = draw.textbbox((0, 0), line, font=quote_font, direction="rtl" if rtl else "ltr", features=["-liga"])
        line_width = bbox[2] - bbox[0]
        x = (W - line_width) // 2
        draw.text((x, current_y), line, font=quote_font, fill="#CDB8A2", direction="rtl" if rtl else "ltr", features=["-liga"])
        current_y += line_heights[i] + line_spacing

    last_line_y = current_y + author_spacing

    # Draw thinker name (from JSON key)
    name_text = f"— {thinker_display_name}"
    name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (W - name_width) // 2
    draw.text((name_x, last_line_y), name_text, font=name_font, fill="#CDB8A2")

    # Instagram icon + brand name
    try:
        icon = Image.open(INSTAGRAM_ICON_PATH).convert("RGBA").resize((28, 28))
        r, g, b, alpha = icon.split()

        # Replace color using gold fill and original alpha
        gold_layer = Image.new("RGBA", icon.size, "#CDB8A2")
        gold_layer.putalpha(alpha)

        overlay.paste(gold_layer, (10, 10), mask=alpha)

        draw.text((48, 10), BRAND_NAME, font=brand_font, fill="#CDB8A2")
    except Exception as e:
        print("Instagram icon error:", e)
        draw.text((10, 10), BRAND_NAME, font=brand_font, fill="#CDB8A2")

    final = Image.alpha_composite(background, overlay)
    output_filename = f"preview_{uuid.uuid4().hex}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    final.convert("RGB").save(output_path)

    return {
        "preview_url": f"/preview/{output_filename}",
        "filename": output_filename
    }
