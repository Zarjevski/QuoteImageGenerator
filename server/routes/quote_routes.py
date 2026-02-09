from flask import Blueprint, jsonify, send_from_directory
import os
import json
from config import QUOTES_DIR, IMAGES_DIR
import logging

logger = logging.getLogger(__name__)
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
    try:
        # Security: sanitize inputs
        lang = lang.lower()
        file_key = file_key.replace("..", "").replace("/", "").replace("\\", "")
        
        prefix = lang.upper()
        file_name = f"{prefix}_{file_key}.json"
        file_path = os.path.join(QUOTES_DIR, lang, file_name)

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({"error": "Quote file not found"}), 404

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return jsonify(data)  # full dict with display name key
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error reading {file_path}: {e}")
        return jsonify({"error": "Invalid JSON file"}), 500
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}", exc_info=True)
        return jsonify({"error": "Failed to read quote file"}), 500



@quote_bp.route("/images/<thinker>", methods=["GET"])
def get_images(thinker):
    try:
        # Security: sanitize thinker name
        thinker = thinker.replace("..", "").replace("/", "").replace("\\", "")
        folder = os.path.join(IMAGES_DIR, thinker)
        
        if not os.path.exists(folder) or not os.path.isdir(folder):
            return jsonify([])
        
        images = [
            f for f in os.listdir(folder) 
            if os.path.isfile(os.path.join(folder, f)) and 
            f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))
        ]
        return jsonify(images)
    except Exception as e:
        logger.error(f"Error getting images for {thinker}: {e}", exc_info=True)
        return jsonify({"error": "Failed to get images"}), 500

@quote_bp.route("/images/<thinker>/<filename>")
def serve_image_file(thinker, filename):
    try:
        # Security: prevent path traversal
        thinker = thinker.replace("..", "").replace("/", "").replace("\\", "")
        filename = filename.replace("..", "").replace("/", "").replace("\\", "")
        
        folder = os.path.join(IMAGES_DIR, thinker)
        file_path = os.path.join(folder, filename)
        
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({"error": "Image not found"}), 404
        
        return send_from_directory(folder, filename)
    except Exception as e:
        logger.error(f"Error serving image {thinker}/{filename}: {e}", exc_info=True)
        return jsonify({"error": "Failed to serve image"}), 500
