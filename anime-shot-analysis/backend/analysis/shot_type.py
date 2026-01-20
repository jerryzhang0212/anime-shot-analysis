def classify_shot_type(bbox, H):
    if bbox is None:
        return "Unknown"

    x1, y1, x2, y2 = bbox
    subject_height = y2 - y1
    ratio = subject_height / H

    # More detailed, no abbreviations
    if ratio >= 0.85:
        return "Extreme Close-Up"
    if ratio >= 0.65:
        return "Close-Up"
    if ratio >= 0.50:
        return "Medium Close-Up"
    if ratio >= 0.35:
        return "Medium Shot"
    if ratio >= 0.20:
        return "Long Shot"
    return "Extreme Long Shot"