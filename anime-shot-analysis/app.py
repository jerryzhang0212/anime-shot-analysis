# app.py
# type: ignore
# pyright: reportMissingImports=false
# pylint: skip-file

from __future__ import annotations

import os
import uuid
import logging
from typing import Tuple, Any

import cv2
from flask import Flask, render_template, request, send_from_directory, abort
from werkzeug.utils import secure_filename

# Import analysis modules
from backend.analysis.grid_overlay import draw_rule_of_thirds_grid
from backend.analysis.subject_detection import detect_main_subject
from backend.analysis.shot_type import classify_shot_type
from backend.analysis.color_palette import (
    extract_color_palette,
    save_palette_image,
    analyze_emotion_tone,
)
from backend.analysis.composition import (
    compute_subject_size_ratio,
    classify_subject_scale,
    compute_composition_bias,
)
from backend.analysis.text_report import generate_shot_explanation


# -------------------------
# App / Config
# -------------------------
app = Flask(__name__, template_folder="frontend/templates")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "uploads")
app.config["OUTPUT_FOLDER"] = os.path.join(BASE_DIR, "analysis_outputs")

# Upload safety: 10MB max (adjust as needed)
app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_UPLOAD_MB", "10")) * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

# -------------------------
# Logging (replace print)
# -------------------------
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("anime-shot-analysis")


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def make_unique_filename(original_name: str) -> str:
    safe = secure_filename(original_name)  # removes weird chars + path tricks
    if not safe:
        safe = "upload.jpg"

    name, ext = os.path.splitext(safe)
    ext = ext.lower() if ext else ".jpg"

    # If someone uploads "file.PNG", keep it consistent
    if ext.replace(".", "") not in ALLOWED_EXTENSIONS:
        ext = ".jpg"

    uid = uuid.uuid4().hex[:8]
    return f"{name}__{uid}{ext}"


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("image")
    if not file or file.filename is None or file.filename.strip() == "":
        return "No file uploaded.", 400

    if not allowed_file(file.filename):
        return "Invalid file type. Please upload PNG/JPG/JPEG.", 400

    # Unique run folder keeps outputs organized and prevents collisions
    run_id = uuid.uuid4().hex[:10]
    run_output_dir = os.path.join(app.config["OUTPUT_FOLDER"], run_id)
    ensure_dir(run_output_dir)

    filename = make_unique_filename(file.filename)
    original_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        file.save(original_path)

        img = cv2.imread(original_path)
        if img is None:
            return "Error reading image file (OpenCV failed).", 400

        H, W, C = img.shape
        logger.info("Uploaded %s (%dx%dx%d) run_id=%s", filename, W, H, C, run_id)

        # 1) Rule of Thirds
        grid_name = f"grid_{filename}"
        grid_path = os.path.join(run_output_dir, grid_name)
        draw_rule_of_thirds_grid(original_path, grid_path)

        # 2) Subject Detection
        subject_name = f"subject_{filename}"
        subject_path = os.path.join(run_output_dir, subject_name)
        subject_pos, subject_bbox, _ = detect_main_subject(original_path, subject_path)

        # Defensive: if detection fails, keep the app alive with a fallback bbox
        if not subject_bbox or len(subject_bbox) != 4:
            logger.warning("Subject detection failed. Using fallback bbox. run_id=%s", run_id)
            subject_bbox = (int(W * 0.25), int(H * 0.25), int(W * 0.75), int(H * 0.75))
            subject_pos = "center"

        # 3) Composition metrics
        ratio = compute_subject_size_ratio(subject_bbox, W, H)
        scale = classify_subject_scale(ratio)
        comp = compute_composition_bias(subject_bbox, W, H)

        # 4) Color palette
        palette = extract_color_palette(original_path, 5)
        palette_name = f"palette_{filename}"
        palette_path = os.path.join(run_output_dir, palette_name)
        save_palette_image(palette, palette_path)
        emotion = analyze_emotion_tone(palette)

        # 5) Shot type
        shot_type = classify_shot_type(subject_bbox, H)

        # 6) Director interpretation
        explanation = generate_shot_explanation(
            shot_type, subject_pos, scale, emotion, comp, palette
        )

        return render_template(
            "result.html",
            image_filename=filename,
            grid_image=f"{run_id}/{grid_name}",
            subject_image=f"{run_id}/{subject_name}",
            palette_image=f"{run_id}/{palette_name}",
            width=W,
            height=H,
            channels=C,
            subject_position=subject_pos,
            subject_bbox=subject_bbox,
            subject_ratio=ratio,
            subject_scale=scale,
            composition=comp,
            shot_type=shot_type,
            emotion_tone=emotion,
            shot_explanation=explanation,
        )

    except Exception as e:
        logger.exception("Upload/analyze failed: %s", e)
        return "Server error while analyzing image. Check terminal logs.", 500


@app.route("/show_image/<path:filename>")
def show_image(filename):
    # This only serves files from upload folder
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/show_output/<path:filename>")
def show_output(filename):
    """
    filename is a path like: "<run_id>/grid_xxx.jpg"
    We keep outputs inside analysis_outputs/<run_id>/...
    """
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)


# -------------------------
# Entrypoint
# -------------------------
if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"

    logger.info("Running at http://%s:%d (debug=%s)", host, port, debug)
    app.run(host=host, port=port, debug=debug)