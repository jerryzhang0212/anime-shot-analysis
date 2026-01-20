def compute_subject_size_ratio(bbox, W, H):
    if bbox is None: return None
    x1,y1,x2,y2 = bbox
    return ((x2-x1)*(y2-y1)) / (W*H)

def classify_subject_scale(ratio):
    if ratio is None: return None
    if ratio > 0.25: return "Large"
    if ratio > 0.08: return "Medium"
    return "Small"

def compute_composition_bias(bbox, W, H):
    if bbox is None: return None
    x1,y1,x2,y2 = bbox
    cx = (x1+x2)/2
    if cx < W/3: return "Left"
    if cx < 2*W/3: return "Middle"
    return "Right"