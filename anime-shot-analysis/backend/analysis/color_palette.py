# type: ignore
# pyright: reportMissingImports=false
# pylint: skip-file

import numpy as np
import cv2
from sklearn.cluster import KMeans

def extract_color_palette(path, n):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1,3)

    kmeans = KMeans(n_clusters=n, n_init=3)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int).tolist()
    return colors

def save_palette_image(palette, path):
    swatch = np.zeros((100, 500, 3), dtype=np.uint8)

    w = 500 // len(palette)
    for i, rgb in enumerate(palette):
        swatch[:, i*w:(i+1)*w] = rgb

    swatch = cv2.cvtColor(swatch, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, swatch)

def analyze_emotion_tone(palette):
    avg_b = np.mean([c[2] for c in palette])
    avg_r = np.mean([c[0] for c in palette])
    if avg_b > avg_r+20: return "cool"
    if avg_r > avg_b+20: return "warm"
    return "neutral"