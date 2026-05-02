# 🛡️ FrameWise – AI Media Forensics Tool

An AI-powered web application that detects synthetic or AI-generated content in images and videos using computer vision and deep learning.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-Educational-green.svg)]()

---

## 🎯 What It Does

FrameWise analyzes videos and images to identify AI-generated content by:
- Comparing visual styles against known AI generation patterns (CLIP model)
- Detecting unnatural textures and "plastic skin" artifacts (OpenCV analysis)
- Providing a confidence score (0-100%) with supporting evidence frames

**Live Demo:** Upload a video/image or paste an Instagram Reel/YouTube Shorts link → Get instant AI detection results

---

## ✨ Key Features

- 🔗 **Social Media Support** – Analyze Instagram Reels & YouTube Shorts via link
- 📂 **Local Upload** – Support for MP4, AVI, PNG, JPG files
- 🧠 **Multi-Modal Detection** – CLIP-based semantic analysis + pixel-level forensics
- 🌍 **Multi-Language** – English, Hindi, and Marathi interface
- 📊 **Visual Results** – Confidence gauge + suspicious/authentic frames preview
- 📱 **Quick Share** – WhatsApp integration for sharing warnings

---

## 🛠️ Tech Stack

**Frontend:** Streamlit (custom dark theme UI)  
**ML/AI:** PyTorch, Transformers (CLIP: `openai/clip-vit-base-patch32`)  
**Computer Vision:** OpenCV, PIL/Pillow  
**Video Processing:** yt-dlp, FFmpeg  

---

## 🚀 Quick Start

### 1. Install Prerequisites
```bash
# Install FFmpeg (required for video download)
# Windows:
winget install Gyan.FFmpeg

# macOS:
brew install ffmpeg

# Linux:
sudo apt install ffmpeg
```

### 2. Install Dependencies
```bash
pip install streamlit yt-dlp opencv-python transformers torch torchvision pillow
```

### 3. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
FrameWise/
├── app.py              # Main UI and orchestration
├── detect.py           # AI detection engine (CLIP + pixel analysis)
├── download_video.py   # Video downloader (yt-dlp wrapper)
├── extract.py          # Smart frame extraction
└── README.md           # You are here
```

---

## 🎬 How to Use

1. **Choose Input Method:**
   - Paste a social media link (Instagram/YouTube Shorts)
   - Upload a local video or image file

2. **Click "Analyze Footage"**

3. **View Results:**
   - AI confidence score (>50% = likely fake)
   - Visual gauge meter (Green → Real | Red → Fake)
   - Supporting frames showing detected artifacts

---

## 💡 Key Highlights

- **Smart Sampling:** Automatically adjusts frame extraction based on video length for optimal speed
- **Educational Focus:** Includes sidebar tips on spotting deepfakes manually (hands, backgrounds, skin texture)
- **~70% Accuracy:** Prototype-level detection suitable for awareness and learning
- **First Analysis:** Downloads ~500MB AI model once (cached locally thereafter)

---

## ⚠️ Disclaimer

This is an **educational prototype** with ~70% accuracy. It should be used for:
- ✅ Learning about AI detection techniques
- ✅ Raising awareness about synthetic media

**NOT for:**
- ❌ Legal evidence or official verification
- ❌ Absolute proof of authenticity

AI detection is rapidly evolving—results should be cross-referenced with other sources.

---

## 🤝 Contributing

Contributions welcome! Feel free to open issues or submit pull requests.

**Potential Improvements:**
- Additional detection models
- Temporal consistency analysis
- Batch processing
- API endpoints

---

## 📧 Contact

For questions or collaboration: [Open an issue](../../issues)

---

**Built for media literacy and digital awareness** 🎓
