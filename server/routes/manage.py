import os
import json
from flask import Blueprint, request, jsonify
from config import IMAGES_DIR, QUOTES_DIR, OUTPUT_DIR

manage_bp = Blueprint("manage", __name__)

@manage_bp.route("/upload/image/<thinker>", methods=["POST"])
def upload_image(thinker):
    image = request.files.get("image")
    if not image:
        return jsonify({"error": "No image file provided"}), 400

    thinker_folder = os.path.join(IMAGES_DIR, thinker)
    os.makedirs(thinker_folder, exist_ok=True)
    path = os.path.join(thinker_folder, image.filename)
    image.save(path)

    return jsonify({"message": f"Image uploaded for {thinker}", "filename": image.filename})


@manage_bp.route("/upload/quote/<thinker>", methods=["POST"])
def upload_quote(thinker):
    new_quote = request.json.get("quote")
    if not new_quote:
        return jsonify({"error": "No quote provided"}), 400

    file_path = os.path.join(QUOTES_DIR, f"{thinker}.json")

    display_key = thinker
    quotes = []

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                if isinstance(existing_data, dict) and len(existing_data) == 1:
                    display_key = list(existing_data.keys())[0]
                    quotes = existing_data[display_key]
            except Exception as e:
                print("load error:", e)

    quotes.append(new_quote)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({display_key: quotes}, f, ensure_ascii=False, indent=2)

    return jsonify({"message": f"Quote added to {display_key}"})


@manage_bp.route("/upload/quote-file/<thinker>", methods=["POST"])
def upload_quote_file(thinker):
    file = request.files.get("file")
    if not file or not file.filename.endswith(".json"):
        return jsonify({"error": "No JSON file uploaded"}), 400

    save_path = os.path.join(QUOTES_DIR, f"{thinker}.json")
    file.save(save_path)

    return jsonify({"message": f"Quote file saved as {thinker}.json"})


@manage_bp.route("/history", methods=["GET"])
def list_history():
    files = os.listdir(OUTPUT_DIR)
    return jsonify({"files": files})

@manage_bp.route("/history/<filename>", methods=["DELETE"])
def delete_single_file(filename):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    os.remove(file_path)
    return jsonify({"message": f"Deleted {filename}"})


@manage_bp.route("/history", methods=["DELETE"])
def clear_history():
    for f in os.listdir(OUTPUT_DIR):
        os.remove(os.path.join(OUTPUT_DIR, f))
    return jsonify({"message": "Output folder cleared."})
