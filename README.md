# AI Property Video Generator

A Python-based real estate promotional video generator that transforms property details and uploaded images into a professional promotional video.

## Project Overview

The AI Property Video Generator helps real estate businesses create promotional videos for property listings. Users provide property information and upload property images. The application arranges the images into scenes and adds text overlays, transitions, and a luxury-inspired visual design to generate an MP4 video.

## Features

- User-friendly web interface built with Streamlit.
- Property information input, including name, location, price, type, and key features.
- Upload multiple property images.
- Automatically generate promotional text using template-based logic.
- Create visually appealing scenes with text overlays.
- Luxury-inspired design with elegant colors and typography.
- Smooth transitions between scenes.
- Export the generated video in MP4 format.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| MoviePy | Video generation and editing |
| Pillow (PIL) | Image processing and text rendering |
| NumPy | Image and frame processing |
| ImageIO-FFmpeg | Video encoding support |

## Project Structure

```text
AI-Property-Video-Generator/
│
├── app.py                  # Streamlit application
├── video_generator.py      # Video generation logic
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── assets/                 # Sample property images
└── output/                 # Generated MP4 videos
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/HarshBardhan571/AI-Property-Video-Generator.git
```

### 2. Navigate to the project directory

```bash
cd AI-Property-Video-Generator
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## How to Use

1. Launch the application.
2. Enter the property name and location.
3. Provide the property price and type.
4. Add key property features.
5. Enter the contact information or call-to-action.
6. Upload the property images.
7. Generate the promotional video.
8. Preview and save the generated MP4 video.

## Video Generation Approach

The current implementation uses rule-based promotional text generation rather than an external generative AI model.

The video-generation pipeline includes:

1. Collecting property information and images.
2. Preparing promotional captions using predefined templates.
3. Processing images and creating visually designed scenes.
4. Adding text overlays and transitions.
5. Combining scenes into a final MP4 video.

## AI Model / API

The current prototype does not depend on an external AI model or paid AI API. It uses predefined template logic to generate promotional text based only on the information supplied by the user.

## Limitations and Future Improvements

- Integrate an LLM API for more dynamic promotional scripts.
- Add AI-powered text-to-speech narration.
- Include background music.
- Add advanced cinematic image animations.
- Provide multiple video themes and templates.

## Author

**Harsh Bardhan Singh**

GitHub: [HarshBardhan571](https://github.com/HarshBardhan571)

---

*Developed as a prototype for automated real estate promotional video generation.*
