from flask import Blueprint, jsonify, send_from_directory
import os
import json
from config import QUOTES_DIR, IMAGES_DIR

quote_bp = Blueprint("quote", __name__)

import os
import json
from flask import Blueprint, jsonify
from config import QUOTES_DIR

quote_bp = Blueprint("quote", __name__)

@quote_bp.route("/thinkers/<lang>", methods=["GET"])
def get_thinkers_by_language(lang):
    folder = os.path.join(QUOTES_DIR, lang.lower())
    prefix = lang.upper() + "_"

    if not os.path.exists(folder):
        return jsonify([])

    thinkers = []
    for file in os.listdir(folder):
        if file.endswith(".json") and file.startswith(prefix):
            file_key = file.replace(".json", "").replace(prefix, "")
            display_name = " ".join(word.capitalize() for word in file_key.split("_"))
            thinkers.append(display_name)

    return jsonify(thinkers)


@quote_bp.route("/quotes/<lang>/<file_key>", methods=["GET"])
def get_quote_by_language(lang, file_key):
    prefix = lang.upper()
    file_name = f"{prefix}_{file_key}.json"
    file_path = os.path.join(QUOTES_DIR, lang.lower(), file_name)

    if not os.path.exists(file_path):
        return jsonify({"error": "Quote file not found"}), 404

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return jsonify(data)  # full dict with display name key
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return jsonify({"error": "Failed to read quote file"}), 500



@quote_bp.route("/images/<thinker>", methods=["GET"])
def get_images(thinker):
    folder = os.path.join(IMAGES_DIR, thinker)
    if not os.path.exists(folder):
        return jsonify([])
    return jsonify([
        f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

@quote_bp.route("/images/<thinker>/<filename>")
def serve_image_file(thinker, filename):
    folder = os.path.join(IMAGES_DIR, thinker)
    return send_from_directory(folder, filename)
