from flask import Blueprint, request, jsonify, send_file, send_from_directory
from services.image_service import generate_image
from config import OUTPUT_DIR
import os
import logging

logger = logging.getLogger(__name__)
generate_bp = Blueprint("generate", __name__)

@generate_bp.route("/generate-preview", methods=["POST"])
def preview():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ["quote", "thinker", "imageFolder", "image"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        result = generate_image(data)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error generating image: {e}", exc_info=True)
        return jsonify({"error": "Failed to generate image"}), 500

@generate_bp.route("/preview/<filename>")
def serve_preview(filename):
    # Security: prevent path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        return jsonify({"error": "Invalid filename"}), 400
    
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path) or not os.path.isfile(path):
        return jsonify({"error": "File not found"}), 404
    
    return send_from_directory(OUTPUT_DIR, filename)

@generate_bp.route("/download/<filename>")
def download(filename):
    # Security: prevent path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        return jsonify({"error": "Invalid filename"}), 400
    
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path) or not os.path.isfile(path):
        return jsonify({"error": "File not found"}), 404
    
    return send_file(path, mimetype="image/png", as_attachment=True, download_name="quote.png")
