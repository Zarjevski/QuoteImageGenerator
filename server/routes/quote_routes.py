from flask import Blueprint, jsonify, send_from_directory
import os
import json
from config import QUOTES_DIR, IMAGES_DIR

quote_bp = Blueprint("quote", __name__)

@quote_bp.route("/thinkers", methods=["GET"])
def get_thinkers():
    thinkers = [
        f.replace(".json", "")
        for f in os.listdir(QUOTES_DIR)
        if f.endswith(".json")
    ]
    return jsonify(thinkers)

@quote_bp.route("/quotes/<thinker>", methods=["GET"])
def get_quotes(thinker):
    path = os.path.join(QUOTES_DIR, f"{thinker}.json")
    if not os.path.exists(path):
        return jsonify([])

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return jsonify(data)
            elif isinstance(data, dict):
                first_key = list(data.keys())[0]
                return jsonify(data.get(first_key, []))
        except Exception as e:
            print(f"Error reading quotes for {thinker}: {e}")
            return jsonify([])

    return jsonify([])

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
