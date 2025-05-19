from flask import Blueprint, request, jsonify, send_file, send_from_directory
from services.image_service import generate_image
from config import OUTPUT_DIR
import os

generate_bp = Blueprint("generate", __name__)

@generate_bp.route("/generate-preview", methods=["POST"])
def preview():
    data = request.json
    result = generate_image(data)
    return jsonify(result)

@generate_bp.route("/preview/<filename>")
def serve_preview(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@generate_bp.route("/download/<filename>")
def download(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    return send_file(path, mimetype="image/png", as_attachment=True, download_name="quote.png")
