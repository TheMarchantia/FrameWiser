from transformers import CLIPProcessor, CLIPModel # type: ignore
from PIL import Image, ImageEnhance # pyright: ignore[reportMissingImports]
import glob
import os
import shutil
import torch # pyright: ignore[reportMissingImports]
import cv2 # pyright: ignore[reportMissingImports]
import numpy as np

print("🧠 Loading Visual Forensics Engine...")
model_id = "openai/clip-vit-base-patch32"
try:
    model = CLIPModel.from_pretrained(model_id)
    processor = CLIPProcessor.from_pretrained(model_id)
except Exception as e:
    print(f"❌ Error loading CLIP: {e}")
    exit()

def analyze_pixel_quality(image_path):
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        noise_sigma = np.std(gray)
        
        ratio = laplacian_var / (noise_sigma + 1)
        
        is_plastic = False
        if ratio > 20: 
            is_plastic = True
            
        return is_plastic, ratio
    except Exception:
        return False, 0

def analyze_visual_style(image_path):
    ai_style_prompts = [
        "hyper-realistic cgi render", "unreal engine 5 graphics",
        "midjourney v6 style", "plastic skin texture",
        "uncanny valley face", "glossy and smooth texture",
        "perfect studio lighting", "ai generated visual",
        "cinematic lighting exaggerated"
    ]
    
    real_style_prompts = [
        "shot on mobile phone", "surveillance camera footage",
        "grainy news footage", "imperfect lighting",
        "natural skin pores", "motion blur",
        "raw camera footage", "low resolution video"
    ]
    
    all_prompts = ai_style_prompts + real_style_prompts
    
    try:
        image = Image.open(image_path)
        inputs = processor(text=all_prompts, images=image, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)[0]
        
        values, indices = probs.topk(3)
        fake_score = 0.0
        top_match = all_prompts[indices[0]]
        
        for i in range(3):
            match_text = all_prompts[indices[i]]
            score = values[i].item()
            if match_text in ai_style_prompts:
                fake_score += score
                
        return fake_score, top_match
    except Exception as e:
        print(f"Error: {e}")
        return 0.0, "error"

def analyze_frames(frame_folder="temp_frames"):
    image_files = glob.glob(f"{frame_folder}/*.jpg")
    
    if not image_files:
        return 0, []

    print(f"🔍 Analyzing {len(image_files)} frames for Digital Artifacts...")
    
    total_fake_score = 0
    frames_count = 0
    frame_scores = [] # NEW: Keeps track of individual frames
    
    for img_path in image_files:
        style_score, top_match = analyze_visual_style(img_path)
        is_plastic, sharpness_ratio = analyze_pixel_quality(img_path)
        
        frame_fake_prob = style_score * 100
        if is_plastic:
            frame_fake_prob += 20
            
        total_fake_score += frame_fake_prob
        frames_count += 1
        
        # Save score for sorting later
        frame_scores.append((img_path, frame_fake_prob))

    if frames_count > 0:
        final_verdict = total_fake_score / frames_count
        
        if final_verdict > 40: 
            final_verdict = min(99.5, final_verdict + 15)
            
        # Sort frames from Highest Fake Score to Lowest
        frame_scores.sort(key=lambda x: x[1], reverse=True)
            
        print("-" * 30)
        print(f"📊 VISUAL FORENSICS SCORE: {final_verdict:.1f}%")
        
        # RETURN BOTH!
        return final_verdict, frame_scores
        
    return 0, []

def cleanup_data():
    folders = ["temp_videos", "temp_frames"]
    for folder in folders:
        if os.path.exists(folder):
            try: shutil.rmtree(folder)
            except: pass

if __name__ == "__main__":
    analyze_frames()