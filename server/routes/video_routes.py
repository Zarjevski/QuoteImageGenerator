from flask import Blueprint, jsonify, request, send_file
import os
import ffmpeg

video_bp = Blueprint("video", __name__)

@video_bp.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.json
    image_filename = data.get("filename")

    if not image_filename:
        return jsonify({"error": "Missing filename"}), 400

    image_path = os.path.join("output", image_filename)
    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    video_filename = image_filename.replace(".png", ".mp4")
    video_path = os.path.join("output", video_filename)

    try:
        # Scale and crop image to fill 1080x1920 (no black bars)
        (
            ffmpeg
            .input(image_path, loop=1, t=30)  # loop image for 30s
            .filter('scale', '1080:1920', force_original_aspect_ratio='increase')  # scale up
            .filter('crop', 1080, 1920)  # crop center
            .filter('fade', type='in', start_time=0, duration=0.8)  # fast fade-in
            .output(video_path, vcodec='libx264', pix_fmt='yuv420p', r=30)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )

        return jsonify({
            "video_url": f"/videos/{video_filename}",
            "filename": video_filename
        })
    except ffmpeg.Error as e:
        print(f"❌ FFmpeg stderr:\n{e.stderr.decode('utf8')}")
        return jsonify({"error": "Failed to generate video"}), 500

@video_bp.route("/videos/<filename>", methods=["GET"])
def serve_video(filename):
    video_path = os.path.join("output", filename)
    if not os.path.exists(video_path):
        return jsonify({"error": "Video not found"}), 404
    return send_file(video_path, mimetype="video/mp4")
