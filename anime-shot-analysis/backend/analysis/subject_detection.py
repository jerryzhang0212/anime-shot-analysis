# backend/analysis/subject_detection.py
# type: ignore
# pyright: reportMissingImports=false
# pylint: skip-file

from __future__ import annotations

import os
import logging
from typing import Optional, Tuple, Any

import cv2

logger = logging.getLogger("anime-shot-analysis")


# Lazy-loaded global model (loaded only when needed)
_MODEL = None


def _get_model(weights_path: Optional[str] = None):
    """
    Load YOLO model lazily to avoid heavy import-time costs and path issues.
    """
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    try:
        from ultralytics import YOLO  # import here to avoid hard dependency at import-time
    except Exception as e:
        raise RuntimeError(
            "ultralytics is not installed. Run: pip install ultralytics"
        ) from e

    if weights_path is None:
        # Resolve yolov8n.pt relative to project root (two levels up from this file)
        # .../backend/analysis/subject_detection.py -> project_root/yolov8n.pt
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        weights_path = os.path.join(project_root, "yolov8n.pt")

    if not os.path.exists(weights_path):
        raise FileNotFoundError(
            f"YOLO weights not found at: {weights_path}. "
            "Make sure yolov8n.pt exists in the project root."
        )

    logger.info("Loading YOLO weights: %s", weights_path)
    _MODEL = YOLO(weights_path)
    return _MODEL


def _pick_best_box(results, min_conf: float = 0.25):
    """
    Pick the best detection box.
    Strategy:
      1) filter by confidence >= min_conf
      2) choose highest confidence; if tie, choose largest area
    """
    boxes = results.boxes
    if boxes is None or len(boxes) == 0:
        return None

    # xyxy: (N,4), conf: (N,)
    xyxy = boxes.xyxy.cpu().numpy()
    conf = boxes.conf.cpu().numpy()

    best_idx = None
    best_score = -1.0
    best_area = -1.0

    for i in range(len(conf)):
        if conf[i] < min_conf:
            continue
        x1, y1, x2, y2 = xyxy[i]
        area = max(0.0, (x2 - x1)) * max(0.0, (y2 - y1))

        # primary: confidence, secondary: area
        if conf[i] > best_score or (conf[i] == best_score and area > best_area):
            best_score = float(conf[i])
            best_area = float(area)
            best_idx = i

    if best_idx is None:
        return None

    return xyxy[best_idx].astype(int), best_score


def detect_main_subject(
    input_path: str,
    output_path: str,
    min_conf: float = 0.25,
    device: Optional[str] = None,
) -> Tuple[str, Optional[Tuple[int, int, int, int]], Optional[Any]]:
    """
    Detect the main subject using YOLO, draw the bbox, and return:
      (position, (x1,y1,x2,y2) or None, raw_box_array or None)

    position: "left" | "center" | "right" | "none"
    """
    img = cv2.imread(input_path)
    if img is None:
        logger.warning("OpenCV failed to read image: %s", input_path)
        return "none", None, None

    model = _get_model()

    # Run inference
    try:
        # Ultralytics accepts device like "cpu", "0" (GPU id), etc.
        # Passing device=None is fine.
        preds = model.predict(source=input_path, device=device, verbose=False)
        results = preds[0]
    except Exception as e:
        logger.exception("YOLO inference failed: %s", e)
        # Save original so UI still shows something
        cv2.imwrite(output_path, img)
        return "none", None, None

    picked = _pick_best_box(results, min_conf=min_conf)
    if picked is None:
        cv2.imwrite(output_path, img)
        return "none", None, None

    box_int, score = picked
    x1, y1, x2, y2 = [int(v) for v in box_int]

    # Clamp bbox to image bounds
    h, w = img.shape[:2]
    x1 = max(0, min(x1, w - 1))
    x2 = max(0, min(x2, w - 1))
    y1 = max(0, min(y1, h - 1))
    y2 = max(0, min(y2, h - 1))

    # If bbox collapses, treat as none
    if x2 <= x1 or y2 <= y1:
        cv2.imwrite(output_path, img)
        return "none", None, None

    # Draw bbox
    img2 = img.copy()
    cv2.rectangle(img2, (x1, y1), (x2, y2), (255, 0, 0), 3)
    # Optional: draw confidence text (kept minimal)
    cv2.putText(
        img2,
        f"{score:.2f}",
        (x1, max(0, y1 - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 0, 0),
        2,
    )
    cv2.imwrite(output_path, img2)

    # Position classification
    cx = (x1 + x2) / 2.0
    if cx < w / 3:
        pos = "left"
    elif cx > 2 * w / 3:
        pos = "right"
    else:
        pos = "center"

    return pos, (x1, y1, x2, y2), box_int