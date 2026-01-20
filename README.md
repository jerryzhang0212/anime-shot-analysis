# Anime Shot Analysis

**Anime Shot Analysis** is a computer vision–based analysis tool designed to bridge **film language** and **AI-assisted animation workflows**.

This project analyzes a single anime frame and extracts cinematic features such as composition, subject scale, shot type, and emotional tone.  
It serves as an exploratory step toward building AI tools that assist **2D animation creation**, especially for reducing manual workload in complex scenes.

---

## Motivation

Traditional 2D animation relies heavily on manual experience to determine:
- Shot scale and composition  
- Subject importance  
- Emotional tone conveyed by color and framing  

This project explores whether **computer vision models** can help quantify these cinematic decisions, forming a foundation for future tools such as:
- AI-assisted keyframe analysis  
- Animation interpolation guidance  
- Intelligent shot consistency checking  

---

## System Overview

### 1. Upload Interface

The user uploads a single anime frame (PNG / JPG) for analysis.

![Upload Interface](anime%20shot%20sample/01_upload_interface.png)

---

### 2. Original Frame

The original input image is displayed before analysis.

![Original Frame](anime%20shot%20sample/02_original_frame.png)

---

### 3. Visual Analysis

The system performs multiple visual analyses, including:
- **Rule of Thirds grid**
- **Main subject detection**
- **Color palette extraction**

![Visual Analysis](anime%20shot%20sample/03_visual_analysis.png)

---

### 4. Shot Metrics

Quantitative metrics are extracted from the frame, including:
- Subject position  
- Bounding box  
- Subject size ratio  
- Shot type  
- Composition bias  
- Emotion tone  

![Shot Metrics](anime%20shot%20sample/04_shot_metrics.png)

---

### 5. Interpretation Output

Based on the extracted features, the system generates a natural-language interpretation describing the cinematic intent of the shot.

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
