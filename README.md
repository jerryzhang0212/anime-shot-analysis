# Anime Shot Analysis

Anime Shot Analysis is a computer vision–based tool for analyzing **single anime frames** and extracting basic cinematic features.

The project focuses on understanding how visual elements such as composition, subject scale, and color distribution appear in anime still images, using computational methods rather than manual judgment.

---

## Motivation

In traditional 2D animation and film analysis, shot composition and visual intent are usually evaluated through experience and intuition.

This project explores whether **basic computer vision techniques** can be used to:
- Identify the main subject in a frame
- Measure subject scale and position
- Analyze composition patterns
- Extract dominant color tones

The goal is not to replace artistic judgment, but to experiment with **quantifying visual features** in anime imagery.

---

## System Overview

### 1. Upload Interface

The user uploads a single anime frame (PNG / JPG) for analysis.

![Upload Interface](anime%20shot%20sample/01_upload_interface.png)

---

### 2. Original Frame

The original input image is displayed before any processing.

![Original Frame](anime%20shot%20sample/02_original_frame.png)

---

### 3. Visual Analysis

The system performs several visual analyses, including:
- Rule of Thirds grid overlay
- Main subject detection
- Color palette extraction

![Visual Analysis](anime%20shot%20sample/03_visual_analysis.png)

---

### 4. Shot Metrics

Quantitative information is extracted from the frame, such as:
- Subject position
- Bounding box
- Subject size ratio
- Shot type
- Composition bias
- Emotion tone (based on color characteristics)

![Shot Metrics](anime%20shot%20sample/04_shot_metrics.png)

---

### 5. Interpretation Output

Based on the extracted features, the system generates a short textual description summarizing the visual characteristics of the frame.

![Interpretation Output](anime%20shot%20sample/05_interpretation_output.png)

---

## Technical Stack

- **Python**
- **Flask** (backend server)
- **YOLOv8** (main subject detection)
- **OpenCV / NumPy** (image processing)
- **HTML + CSS** (frontend visualization)

---

## Project Structure

```text
anime-shot-analysis/
├── backend/          # Core analysis logic
├── frontend/         # HTML templates and styles
├── app.py            # Flask application entry point
├── requirements.txt  # Python dependencies
