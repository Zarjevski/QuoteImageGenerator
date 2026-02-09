import os
import json
import re
from flask import Blueprint, request, jsonify
from config import IMAGES_DIR, QUOTES_DIR, OUTPUT_DIR
from werkzeug.utils import secure_filename
import logging

logger = logging.getLogger(__name__)
manage_bp = Blueprint("manage", __name__)

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
ALLOWED_JSON_EXTENSIONS = {'.json'}

def allowed_file(filename, allowed_extensions):
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def sanitize_filename(filename):
    """Sanitize filename to prevent path traversal and other security issues"""
    filename = secure_filename(filename)
    # Remove any remaining dangerous characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    return filename

@manage_bp.route("/upload/image/<thinker>", methods=["POST"])
def upload_image(thinker):
    try:
        image = request.files.get("image")
        if not image or not image.filename:
            return jsonify({"error": "No image file provided"}), 400

        # Validate file extension
        if not allowed_file(image.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({"error": "Invalid file type. Only images are allowed"}), 400

        # Sanitize thinker name and filename
        thinker = sanitize_filename(thinker)
        safe_filename = sanitize_filename(image.filename)
        
        if not thinker or not safe_filename:
            return jsonify({"error": "Invalid filename"}), 400

        thinker_folder = os.path.join(IMAGES_DIR, thinker)
        os.makedirs(thinker_folder, exist_ok=True)
        path = os.path.join(thinker_folder, safe_filename)
        
        # Check file size (16MB limit is set in app.py, but double-check)
        image.seek(0, os.SEEK_END)
        file_size = image.tell()
        image.seek(0)
        if file_size > 16 * 1024 * 1024:
            return jsonify({"error": "File too large. Maximum size is 16MB"}), 413
        
        image.save(path)
        logger.info(f"Image uploaded: {thinker}/{safe_filename}")
        return jsonify({"message": f"Image uploaded for {thinker}", "filename": safe_filename})
    except Exception as e:
        logger.error(f"Error uploading image: {e}", exc_info=True)
        return jsonify({"error": "Failed to upload image"}), 500


@manage_bp.route("/upload/quote/<thinker>", methods=["POST"])
def upload_quote(thinker):
    try:
        new_quote = request.json.get("quote")
        if not new_quote or not isinstance(new_quote, str) or not new_quote.strip():
            return jsonify({"error": "No valid quote provided"}), 400

        # Sanitize thinker name
        thinker = sanitize_filename(thinker)
        if not thinker:
            return jsonify({"error": "Invalid thinker name"}), 400

        # Ensure quotes directory exists
        os.makedirs(QUOTES_DIR, exist_ok=True)
        file_path = os.path.join(QUOTES_DIR, f"{thinker}.json")

        display_key = thinker
        quotes = []

        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                    if isinstance(existing_data, dict) and len(existing_data) == 1:
                        display_key = list(existing_data.keys())[0]
                        quotes = existing_data[display_key] if isinstance(existing_data[display_key], list) else []
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Error loading existing quotes file: {e}")

        quotes.append(new_quote.strip())

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({display_key: quotes}, f, ensure_ascii=False, indent=2)

        logger.info(f"Quote added to {display_key}")
        return jsonify({"message": f"Quote added to {display_key}"})
    except Exception as e:
        logger.error(f"Error uploading quote: {e}", exc_info=True)
        return jsonify({"error": "Failed to upload quote"}), 500


@manage_bp.route("/upload/quote-file/<thinker>", methods=["POST"])
def upload_quote_file(thinker):
    try:
        file = request.files.get("file")
        if not file or not file.filename:
            return jsonify({"error": "No file uploaded"}), 400

        if not allowed_file(file.filename, ALLOWED_JSON_EXTENSIONS):
            return jsonify({"error": "Invalid file type. Only JSON files are allowed"}), 400

        # Sanitize thinker name
        thinker = sanitize_filename(thinker)
        if not thinker:
            return jsonify({"error": "Invalid thinker name"}), 400

        # Ensure quotes directory exists
        os.makedirs(QUOTES_DIR, exist_ok=True)
        save_path = os.path.join(QUOTES_DIR, f"{thinker}.json")
        
        # Validate JSON before saving
        try:
            content = file.read()
            json.loads(content.decode('utf-8'))
            file.seek(0)  # Reset file pointer
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON file"}), 400
        except Exception as e:
            logger.error(f"Error validating JSON: {e}")
            return jsonify({"error": "Failed to validate JSON file"}), 400

        file.save(save_path)
        logger.info(f"Quote file saved: {thinker}.json")
        return jsonify({"message": f"Quote file saved as {thinker}.json"})
    except Exception as e:
        logger.error(f"Error uploading quote file: {e}", exc_info=True)
        return jsonify({"error": "Failed to upload quote file"}), 500


@manage_bp.route("/history", methods=["GET"])
def list_history():
    try:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            return jsonify({"files": []})
        
        files = [f for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f))]
        return jsonify({"files": files})
    except Exception as e:
        logger.error(f"Error listing history: {e}", exc_info=True)
        return jsonify({"error": "Failed to list history"}), 500

@manage_bp.route("/history/<filename>", methods=["DELETE"])
def delete_single_file(filename):
    try:
        # Security: prevent path traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            return jsonify({"error": "Invalid filename"}), 400
        
        file_path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({"error": "File not found"}), 404

        os.remove(file_path)
        logger.info(f"File deleted: {filename}")
        return jsonify({"message": f"Deleted {filename}"})
    except Exception as e:
        logger.error(f"Error deleting file: {e}", exc_info=True)
        return jsonify({"error": "Failed to delete file"}), 500

@manage_bp.route("/history", methods=["DELETE"])
def clear_history():
    try:
        if not os.path.exists(OUTPUT_DIR):
            return jsonify({"message": "Output folder is already empty"})
        
        deleted_count = 0
        for f in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_count += 1
        
        logger.info(f"Cleared {deleted_count} files from output folder")
        return jsonify({"message": f"Output folder cleared. Deleted {deleted_count} file(s)."})
    except Exception as e:
        logger.error(f"Error clearing history: {e}", exc_info=True)
        return jsonify({"error": "Failed to clear history"}), 500
