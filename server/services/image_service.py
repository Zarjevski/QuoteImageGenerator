import os
import uuid
import json
from PIL import Image, ImageDraw, ImageFont
from config import FONT_PATH, OUTPUT_DIR, INSTAGRAM_ICON_PATH, BRAND_NAME
from utils.text_utils import is_hebrew

def generate_image(data):
    quote = data.get("quote")
    thinker = data.get("thinker")
    image_name = data.get("image")
    image_path = os.path.join("data/images", thinker, image_name)

    background = Image.open(image_path).convert("RGBA")
    W, H = background.size
    padding = 60

    faded = Image.new("RGBA", background.size, (255, 255, 255, 230))
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
        draw.text((x, current_y), line, font=quote_font, fill="black", direction="rtl" if rtl else "ltr", features=["-liga"])
        current_y += line_heights[i] + line_spacing

    last_line_y = current_y + author_spacing

    # ✅ NEW: Try to read Hebrew display name from JSON key
    quote_path = os.path.join("data/quotes", f"{thinker}.json")
    if os.path.exists(quote_path):
        with open(quote_path, "r", encoding="utf-8") as f:
            try:
                content = json.load(f)
                if isinstance(content, dict):
                    display_name = list(content.keys())[0]
                else:
                    display_name = thinker
            except:
                display_name = thinker
    else:
        display_name = thinker

    name_text = f"— {display_name}"
    name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (W - name_width) // 2
    draw.text((name_x, last_line_y), name_text, font=name_font, fill="black")

    try:
        icon = Image.open(INSTAGRAM_ICON_PATH).convert("RGBA").resize((28, 28))
        overlay.paste(icon, (10, 10), icon)
        draw.text((48, 10), BRAND_NAME, font=brand_font, fill="black")
    except:
        draw.text((10, 10), BRAND_NAME, font=brand_font, fill="black")

    final = Image.alpha_composite(background, overlay)
    output_filename = f"preview_{uuid.uuid4().hex}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    final.convert("RGB").save(output_path)

    return {
        "preview_url": f"/preview/{output_filename}",
        "filename": output_filename
    }
