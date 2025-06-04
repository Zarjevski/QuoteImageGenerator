import random
import os
import json
from services.image_service import generate_image
from services.openai_service import generate_caption
from services.instagram_service import post_to_instagram

def get_random_thinker(lang="he"):
    folder = os.path.join("data/quotes", lang)
    files = [f for f in os.listdir(folder) if f.endswith(".json")]

    if not files:
        raise Exception("No quote files found")

    while True:
        chosen = random.choice(files)
        file_path = os.path.join(folder, chosen)

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
            thinker_name = list(data.keys())[0]
            quote_list = data[thinker_name]

        quote = random.choice(quote_list)
        file_key = chosen.replace(f"{lang.upper()}_", "").replace(".json", "")
        image_folder = " ".join(word.capitalize() for word in file_key.split("_"))
        image_path = os.path.join("data/images", image_folder)

        if not os.path.exists(image_path):
            print(f"⚠️ Skipping {thinker_name}: image folder not found ({image_folder})")
            continue

        images = [img for img in os.listdir(image_path) if img.lower().endswith((".png", ".jpg", ".jpeg"))]
        if not images:
            print(f"⚠️ Skipping {thinker_name}: no images in folder ({image_folder})")
            continue

        image = random.choice(images)

        return {
            "thinker": thinker_name,
            "imageFolder": image_folder,
            "image": image,
            "quote": quote,
        }

def run_scheduled_post():
    info = get_random_thinker()
    result = generate_image(info)

    caption = generate_caption(info["quote"], info["thinker"])
    post_to_instagram(image_path=f"output/{result['filename']}", caption=caption)
