import os
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageOps, features
from config import OUTPUT_DIR, FONT_PATH, INSTAGRAM_ICON_PATH, BRAND_NAME
from utils.text_utils import is_hebrew


def generate_image(data):
    quote = data.get("quote")
    thinker_display_name = data.get("thinker")
    image_folder = data.get("imageFolder")
    image_name = data.get("image")

    if not all([quote, thinker_display_name, image_folder, image_name]):
        raise ValueError("Missing required fields")

    image_path = os.path.join("data/images", image_folder, image_name)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Open image and apply dark overlay
    background = Image.open(image_path).convert("RGBA")
    W, H = background.size
    padding = 60

    faded = Image.new("RGBA", background.size, (0, 0, 0, 230))
    background = Image.alpha_composite(background, faded)
    overlay = Image.new("RGBA", background.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Fonts
    try:
        quote_font = ImageFont.truetype(FONT_PATH, size=56)
        name_font = ImageFont.truetype(FONT_PATH, size=36)
        brand_font = ImageFont.truetype(FONT_PATH, size=24)
    except Exception as e:
        print("Font load error:", e)
        quote_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()

    # --- RTL/LTR handling ---
    rtl = is_hebrew(quote)
    has_raqm = features.check("raqm")

    def rtl_safe_text(text):
        # Reverse only if Hebrew and no libraqm
        return text[::-1] if (rtl and not has_raqm) else text

    max_width = W - 2 * padding
    words = quote.split()
    wrapped_lines = []
    current_line = ""

    # --- Word wrapping ---
    for word in words:
        test_line = (current_line + " " + word).strip()
        test_safe = rtl_safe_text(test_line)
        try:
            bbox = draw.textbbox((0, 0), test_safe, font=quote_font,
                                 direction="rtl" if rtl and has_raqm else "ltr")
        except Exception:
            bbox = draw.textbbox((0, 0), test_safe, font=quote_font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word

    if current_line:
        wrapped_lines.append(current_line)

    # --- Measure total text height ---
    line_heights = []
    for line in wrapped_lines:
        test_safe = rtl_safe_text(line)
        try:
            bbox = draw.textbbox((0, 0), test_safe, font=quote_font,
                                 direction="rtl" if rtl and has_raqm else "ltr")
        except Exception:
            bbox = draw.textbbox((0, 0), test_safe, font=quote_font)
        line_heights.append(bbox[3])

    line_spacing = 12
    author_spacing = 50
    total_height = sum(line_heights) + (len(line_heights) - 1) * line_spacing
    start_y = (H - total_height) // 2
    current_y = start_y

    # --- Draw wrapped lines centered ---
    for i, line in enumerate(wrapped_lines):
        line_safe = rtl_safe_text(line)
        try:
            bbox = draw.textbbox((0, 0), line_safe, font=quote_font,
                                 direction="rtl" if rtl and has_raqm else "ltr")
        except Exception:
            bbox = draw.textbbox((0, 0), line_safe, font=quote_font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]

        # Alignment logic
        if rtl and not has_raqm:
            # Simulated RTL: align right but visually centered
            x = (W + line_width) // 2 - line_width
        else:
            x = (W - line_width) // 2

        # Draw the text
        try:
            draw.text((x, current_y), line_safe, font=quote_font, fill="#CDB8A2",
                      direction="rtl" if rtl and has_raqm else "ltr")
        except Exception:
            draw.text((x, current_y), line_safe, font=quote_font, fill="#CDB8A2")

        current_y += line_height + line_spacing

    # --- Author name centered properly ---
    name_text = f"— {thinker_display_name}"
    name_safe = rtl_safe_text(name_text)
    name_bbox = draw.textbbox((0, 0), name_safe, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_height = name_bbox[3] - name_bbox[1]
    name_y = current_y + author_spacing

    if rtl and not has_raqm:
        name_x = (W + name_width) // 2 - name_width
    else:
        name_x = (W - name_width) // 2

    draw.text((name_x, name_y), name_safe, font=name_font, fill="#CDB8A2")

    # --- Instagram brand ---
    try:
        icon = Image.open(INSTAGRAM_ICON_PATH).convert("RGBA").resize((28, 28))
        r, g, b, alpha = icon.split()
        gold_layer = Image.new("RGBA", icon.size, "#CDB8A2")
        gold_layer.putalpha(alpha)
        overlay.paste(gold_layer, (10, 10), mask=alpha)
        draw.text((48, 10), BRAND_NAME, font=brand_font, fill="#CDB8A2")
    except Exception as e:
        print("Instagram icon error:", e)
        draw.text((10, 10), BRAND_NAME, font=brand_font, fill="#CDB8A2")

    # --- Save output ---
    final = Image.alpha_composite(background, overlay)
    output_filename = f"preview_{uuid.uuid4().hex}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    final.convert("RGB").save(output_path)

    return {
        "preview_url": f"/preview/{output_filename}",
        "filename": output_filename
    }
