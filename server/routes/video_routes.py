# server/routes/video_routes.py
from flask import Blueprint, jsonify, request, send_file
import os
from services.video_service import generate_video_from_image

video_bp = Blueprint("video", __name__)

@video_bp.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.json
    image_filename = data.get("filename")

    if not image_filename:
        return jsonify({"error": "Missing filename"}), 400

    try:
        video_filename = generate_video_from_image(image_filename, duration=30)

        return jsonify({
            "video_url": f"/videos/{video_filename}",
            "filename": video_filename
        })
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        print(f"❌ Video generation error: {e}")
        return jsonify({"error": "Failed to generate video"}), 500


@video_bp.route("/videos/<filename>", methods=["GET"])
def serve_video(filename):
    video_path = os.path.join("output", filename)

    if not os.path.exists(video_path):
        return jsonify({"error": "Video not found"}), 404

    # Safe CORS headers for browser access
    response = send_file(
        video_path,
        mimetype="video/mp4",
        as_attachment=False,  # False = stream in browser instead of forcing download
        download_name=filename
    )
    response.headers["Access-Control-Allow-Origin"] = "*"  # allow access from client
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response
