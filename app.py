import streamlit as st
import streamlit.components.v1 as components
import time
import os
import random
import shutil
import urllib.parse
from PIL import Image

# --- IMPORT BACKEND FUNCTIONS ---
from download_video import download_video
from extract import extract_frames
from detect import analyze_frames, cleanup_data

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FrameWise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded" # Forces it to open
)

# --- 1. MULTI-LANGUAGE DICTIONARY ---
TEXTS = {
    "English": {
        "title": "FrameWise",
        "subtitle": "Advanced AI Forensics & Reality Verification System",
        "tab_link": "🔗 Paste Link",
        "tab_upload": "📂 Upload Media",
        "input_placeholder": "Paste Instagram Reel or YouTube Shorts Link...",
        "upload_label": "Upload Video or Image (MP4, AVI, PNG, JPG)",
        "analyze_btn": "🚀 Analyze Footage",
        "downloading": "⬇️ Processing Media Source...",
        "extracting": "🎞️ Extracting Keyframes...",
        "processing_img": "🖼️ Processing Image...",
        "analyzing": "🧠 Running Multi-Modal AI Detection...",
        "verdict_fake": "SYNTHETIC / AI-GENERATED",
        "verdict_real": "AUTHENTIC MEDIA",
        "share_btn": "Share Warning on WhatsApp",
        "share_msg": "⚠️ Warning! I checked this content on FrameWise and it appears to be AI-Generated.",
        "sidebar_title": "🎓 Did You Know?",
        "error_no_input": "⚠️ Please provide a Link or Upload a File.",
        "error_download": "❌ Failed to process video.",
        "error_frames": "❌ No visual data extracted."
    },
    "Hindi": {
        "title": "फ्रेम-वाइज़ (FrameWise)",
        "subtitle": "AI वीडियो की सच्चाई जानने का आधुनिक टूल",
        "tab_link": "🔗 लिंक पेस्ट करें",
        "tab_upload": "📂 मीडिया अपलोड करें",
        "input_placeholder": "वीडियो का लिंक यहाँ पेस्ट करें...",
        "upload_label": "वीडियो या फोटो अपलोड करें (MP4, JPG, PNG)",
        "analyze_btn": "🚀 जांच शुरू करें",
        "downloading": "⬇️ मीडिया प्रोसेस हो रहा है...",
        "extracting": "🎞️ फोटो निकाले जा रहे हैं...",
        "processing_img": "🖼️ फोटो प्रोसेस हो रही है...",
        "analyzing": "🧠 AI जांच चल रही है...",
        "verdict_fake": "नकली / AI जनरेटेड",
        "verdict_real": "असली मीडिया (Authentic)",
        "share_btn": "वॉट्सऐप पर चेतावनी भेजें",
        "share_msg": "⚠️ सावधान! यह कंटेंट नकली (AI) लग रहा है।",
        "sidebar_title": "🎓 क्या आप जानते हैं?",
        "error_no_input": "⚠️ कृपया लिंक पेस्ट करें या फाइल अपलोड करें।",
        "error_download": "❌ प्रोसेस नहीं हो सका।",
        "error_frames": "❌ डेटा नहीं निकल सका।"
    },
    "Marathi": {
        "title": "फ्रेम-वाइज़ (FrameWise)",
        "subtitle": "AI कंटेंटची सत्यता तपासण्याचे प्रगत साधन",
        "tab_link": "🔗 लिंक पेस्ट करा",
        "tab_upload": "📂 मीडिया अपलोड करा",
        "input_placeholder": "लिंक येथे पेस्ट करा...",
        "upload_label": "व्हिडिओ किंवा फोटो अपलोड करा (MP4, JPG, PNG)",
        "analyze_btn": "🚀 तपासणी करा",
        "downloading": "⬇️ मीडिया प्रोसेस होत आहे...",
        "extracting": "🎞️ फोटो (Frames) काढले जात आहेत...",
        "processing_img": "🖼️ फोटो प्रोसेस होत आहे...",
        "analyzing": "🧠 AI तपासणी सुरू आहे...",
        "verdict_fake": "बनावट / AI जनरेटेड",
        "verdict_real": "खरे मीडिया (Authentic)",
        "share_btn": "वॉट्सअ‍ॅपवर चेतावणी पाठवा",
        "share_msg": "⚠️ सावधान! हा कंटेंट बनावट (AI) वाटत आहे.",
        "sidebar_title": "🎓 तुम्हाला माहित आहे का?",
        "error_no_input": "⚠️ कृपया लिंक द्या किंवा फाइल अपलोड करा.",
        "error_download": "❌ प्रोसेस होऊ शकला नाही.",
        "error_frames": "❌ डेटा काढता आला नाही."
    }
}

# --- TIPS DATABASE ---
TIPS = {
    "English": [
        "👀 **Look at the hands:** AI often struggles with fingers, giving people 6 fingers.",
        "👀 **Check the text:** AI generators often write gibberish on signboards.",
        "👀 **Skin Texture:** Real skin has pores. AI skin often looks too smooth (plastic).",
        "👀 **Blinking:** Watch if the person blinks naturally.",
        "👀 **Background:** Look for weird warping or blurry objects behind the person."
    ],
    "Hindi": [
        "👀 **हाथों को देखें:** AI अक्सर उंगलियों को सही नहीं बना पाता (6 उंगलियां)।",
        "👀 **टेक्स्ट चेक करें:** वीडियो में पीछे लिखे बोर्ड पर अक्सर अजीब भाषा होती है।",
        "👀 **त्वचा (Skin):** AI की त्वचा अक्सर प्लास्टिक जैसी बहुत चिकनी लगती है।",
        "👀 **पलकें:** देखें कि क्या व्यक्ति स्वाभाविक रूप से पलकें झपक रहा है।",
        "👀 **बैकग्राउंड:** पीछे की चीजें अजीब तरह से मुड़ी हुई तो नहीं हैं?"
    ],
    "Marathi": [
        "👀 **हातांकडे लक्ष द्या:** AI ला बोटे बनवताना चूक होते (6 बोटे).",
        "👀 **मजकूर तपासा:** मागच्या पाट्यांवरील मजकूर वाचता येत नाही.",
        "👀 **त्वचा:** AI ची त्वचा प्लॅस्टिकसारखी खूप गुळगुळीत दिसते.",
        "👀 **पापण्या:** व्यक्ती नैसर्गिकरित्या पापण्या मिटवत आहे का ते पहा.",
        "👀 **बॅकग्राउंड:** मागील भागात काही वस्तू विचित्रपणे वाकड्या आहेत का?"
    ]
}

# --- CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 10%, #1f2937 0%, #000000 60%);
        font-family: 'Inter', sans-serif;
    }
    
    /* 🚀 FIXED: Shifts UI up but keeps the sidebar toggle accessible */
    .block-container {
        padding-top: 2rem !important; 
        padding-bottom: 1rem !important;
    }
    header { background-color: transparent !important; }
    #MainMenu, footer {visibility: hidden;}
    
    .hero-title {
        font-size: 4rem !important;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-top: 0px !important;
        margin-top: -30px; 
    }
    .hero-subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #9CA3AF;
        margin-bottom: 25px; 
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 15px; /* Restored safe spacing */
        border-bottom: none; 
    }
    .stTabs [data-baseweb="tab"] { 
        flex: 1; /* THE MAGIC FIX: Makes both tabs exactly equal width */
        height: 45px; 
        background-color: #111827; 
        border-radius: 10px; 
        color: #9CA3AF; 
        outline: none; 
        border: none; 
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { 
        background-color: #4F46E5; 
        color: white; 
    }
    
    /* 🚀 The Red Slider (Perfectly Aligned) */
    .stTabs [data-baseweb="tab-highlight"] { 
        background-color: #ef4444 !important; /* Bright Red */
        height: 3px !important; 
        border-radius: 5px; 
    }
    
    /* Hide the ugly grey track underneath */
    .stTabs [data-baseweb="tab-border"] { 
        display: none !important; 
        background-color: transparent !important; 
    }
    
    /* Input & Upload Styling */
    .stTextInput > div > div > input { background-color: #111827; color: white; border: 1px solid #374151; border-radius: 50px; padding: 15px 25px; text-align: center; }
    .stFileUploader { text-align: center; }
    section[data-testid="stFileUploaderDropzone"] { background-color: #111827; border: 1px dashed #374151; border-radius: 15px; padding: 10px; }

    /* Button */
    .stButton { display: flex; justify-content: center; }
    .stButton > button { width: 100%; background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%); color: white; border: none; padding: 12px 30px; border-radius: 50px; font-weight: 600; margin-top: 5px; box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.4); }
    .stButton > button:hover { transform: scale(1.02); }
    
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #1f2937; }
    
    .tip-box { background: linear-gradient(145deg, #1e1e24, #23232b); border: 2px solid transparent; border-image: linear-gradient(to right, #4F46E5, #9333EA) 1; padding: 20px; border-radius: 15px; margin-top: 15px; color: #ffffff; font-weight: 800; font-size: 1.05rem; box-shadow: 0 0 15px rgba(79, 70, 229, 0.2); animation: glow 3s infinite alternate; text-shadow: 0px 0px 10px rgba(0,0,0,0.5); }
    @keyframes glow { from { box-shadow: 0 0 5px rgba(79, 70, 229, 0.2); } to { box-shadow: 0 0 20px rgba(147, 51, 234, 0.4); } }

    .frame-log { font-family: 'Courier New', monospace; color: #4ade80; font-size: 0.9rem; text-align: center; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ Settings / सेटिंग्स")
    lang_choice = st.radio("Language / भाषा", ["English", "Hindi", "Marathi"])
    t = TEXTS[lang_choice]
    
    st.markdown("---")
    st.markdown(f"#### 💡 {t['sidebar_title']}")
    random_tip = random.choice(TIPS[lang_choice])
    st.markdown(f'<div class="tip-box">{random_tip}</div>', unsafe_allow_html=True)

# --- HERO SECTION ---
c1, c2, c3 = st.columns([1, 6, 1])
with c2:
    st.markdown(f'<div class="hero-title">{t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-subtitle">{t["subtitle"]}</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs([t['tab_link'], t['tab_upload']])
    with tab1:
        url_input = st.text_input("", placeholder=t['input_placeholder'], label_visibility="collapsed", key="url_input")
    with tab2:
        uploaded_file = st.file_uploader(t['upload_label'], type=["mp4", "mov", "avi", "png", "jpg", "jpeg"], label_visibility="collapsed")

    b1, b2, b3 = st.columns([1.5, 2, 1.5]) 
    with b2:
        analyze_btn = st.button(t['analyze_btn'], use_container_width=True)

# --- MAIN LOGIC ---
if analyze_btn:
    video_source = None
    is_upload = False
    is_image = False 

    if uploaded_file is not None:
        video_source = uploaded_file
        is_upload = True
        if uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            is_image = True
    elif url_input:
        video_source = url_input
        is_upload = False
    
    if not video_source:
        st.warning(t['error_no_input'])
    else:
        with st.container():
            progress_bar = st.progress(0)
            status_area = st.empty()
            download_log = st.empty() 
            extraction_log = st.empty() 
            analysis_log = st.empty() 
            
            try:
                status_area.info(f"**{t['downloading']}**")
                cleanup_data() 
                progress_bar.progress(10)
                
                final_path = None
                frame_paths = []

                if is_image:
                    if not os.path.exists("temp_frames"): os.makedirs("temp_frames")
                    save_path = os.path.join("temp_frames", "frame_0.jpg")
                    image = Image.open(uploaded_file).convert('RGB')
                    image.save(save_path)
                    frame_paths = [save_path]
                    status_area.info(f"**{t['processing_img']}**")
                    time.sleep(0.5) 
                    progress_bar.progress(60)
                else:
                    if is_upload:
                        if not os.path.exists("temp_videos"): os.makedirs("temp_videos")
                        save_path = os.path.join("temp_videos", "upload.mp4")
                        with open(save_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        final_path = save_path
                    else:
                        final_path = download_video(video_source, status_element=download_log)
                        time.sleep(0.5)
                        download_log.empty()

                    if not final_path:
                        status_area.error(t['error_download'])
                        st.stop()
                    
                    progress_bar.progress(30)
                    status_area.info(f"**{t['extracting']}**")
                    frame_paths = extract_frames(final_path, frame_interval=30, status_element=extraction_log)
                    
                    time.sleep(0.5)
                    extraction_log.empty()
                    
                    if not frame_paths:
                        status_area.error(t['error_frames'])
                        st.stop()
                    
                    progress_bar.progress(60)

                status_area.info(f"**{t['analyzing']}**")
                
                total_frames = len(frame_paths)
                for i in range(total_frames):
                    analysis_log.markdown(f'<div class="frame-log">🔍 Scanning Frame {i+1}/{total_frames} for Artifacts...</div>', unsafe_allow_html=True)
                    time.sleep(0.05) 
                
                ai_score, sorted_frames = analyze_frames()
                
                progress_bar.progress(100)
                time.sleep(0.5)
                status_area.empty()
                progress_bar.empty()
                analysis_log.empty() 

                # --- RESULTS ---
                res_c1, res_c2 = st.columns([1.3, 1])
                
                with res_c1:
                    if ai_score > 50:
                        verdict_color = "#ef4444" # Red
                        verdict_text = t['verdict_fake']
                        icon = "🚨"
                        
                        if not is_upload and video_source:
                            final_msg = f"{t['share_msg']} {video_source}"
                        else:
                            final_msg = t['share_msg']
                            
                        encoded_msg = urllib.parse.quote(final_msg)
                        wa_html = f"""<a href="https://wa.me/?text={encoded_msg}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:50px; font-weight:bold; cursor:pointer; font-size:0.9rem; box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);">📱 {t['share_btn']}</button></a>"""
                    else:
                        verdict_color = "#10b981" # Green
                        verdict_text = t['verdict_real']
                        icon = "✅"
                        wa_html = ""

                    # Calculate needle rotation (-90 points left for 0%, 90 points right for 100%)
                    rotation_deg = (ai_score / 100.0) * 180 - 90
                    
                    # COMPACT HTML CARD
                    html_card = f"""<div style="background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 15px; text-align: center; margin-top: 0px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
<div style="font-size: 1.6rem; font-weight: 800; color: {verdict_color}; margin-bottom: 0px;">{icon} {verdict_text}</div>
<div style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 0px; margin-top: 5px;">AI Confidence Score</div>
<div style="font-size: 3.5rem; font-weight: 900; color: {verdict_color}; margin-bottom: 10px;">{ai_score:.1f}%</div>
<div style="display: flex; justify-content: center; align-items: flex-end; gap: 15px; margin-bottom: 15px;">
<div style="font-weight: 900; color: #10b981; font-size: 1rem; padding-bottom: 5px; letter-spacing: 1px;">REAL</div>
<div style="position: relative; width: 160px; height: 80px; overflow: hidden;">
<div style="position: absolute; top: 0; left: 0; width: 160px; height: 160px; border-radius: 50%; background: conic-gradient(from 270deg, #10b981 0deg, #10b981 72deg, #f59e0b 72deg, #f59e0b 108deg, #ef4444 108deg, #ef4444 180deg, transparent 180deg);"></div>
<div style="position: absolute; top: 20px; left: 20px; width: 120px; height: 120px; border-radius: 50%; background-color: #111827;"></div>
<div style="position: absolute; bottom: 0; left: calc(50% - 2px); width: 4px; height: 75px; background: #ffffff; transform-origin: bottom center; transform: rotate({rotation_deg}deg); border-radius: 4px 4px 0 0; box-shadow: 0 0 5px rgba(0,0,0,0.5); transition: transform 1s ease-out;"></div>
<div style="position: absolute; bottom: -8px; left: calc(50% - 8px); width: 16px; height: 16px; background: #ffffff; border-radius: 50%; box-shadow: 0 0 5px rgba(0,0,0,0.5);"></div>
</div>
<div style="font-weight: 900; color: #ef4444; font-size: 1rem; padding-bottom: 5px; letter-spacing: 1px;">FAKE</div>
</div>
{wa_html}
</div>"""
                    st.markdown(html_card, unsafe_allow_html=True)
                    
                    # COMPACT FEEDBACK LOOP
                    feedback_html = """
                    <html>
                    <head>
                    <style>
                        body { background-color: transparent; margin: 0; font-family: 'Inter', sans-serif; text-align: center; }
                        .btn { border: none; color: white; padding: 6px 20px; border-radius: 50px; cursor: pointer; font-weight: bold; font-size: 0.9rem; transition: transform 0.2s; }
                        .btn:hover { transform: scale(1.05); }
                        .btn-yes { background: #10b981; margin-right: 15px; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3); }
                        .btn-no { background: #ef4444; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3); }
                    </style>
                    </head>
                    <body>
                    <div style="margin-top: 10px;">
                        <p style="color: #9ca3af; font-size: 0.95rem; margin-bottom: 8px; font-weight: 600;">Did we get this right?</p>
                        <button class="btn btn-yes" onclick="document.getElementById('fb-msg').innerHTML = '✅ Thank you! Your feedback helps train our AI.'; this.style.display='none'; document.getElementById('btn-no').style.display='none';">👍 Yes</button>
                        <button id="btn-no" class="btn btn-no" onclick="document.getElementById('fb-msg').innerHTML = '🛠️ Flagged! We will review this to improve our model.'; this.style.display='none'; this.previousElementSibling.style.display='none';">👎 No</button>
                        <p id="fb-msg" style="color: #d1d5db; font-size: 0.85rem; margin-top: 10px; font-weight: 600;"></p>
                    </div>
                    </body>
                    </html>
                    """
                    # Height reduced to exactly fit the elements without overflow
                    components.html(feedback_html, height=90)

                with res_c2:
                    if len(frame_paths) == 1:
                        st.markdown("### 🔍 Forensic Frame")
                        st.image(frame_paths[0], use_container_width=True)
                    else:
                        if ai_score > 50:
                            st.markdown("### 🚨 Top Suspicious Frames")
                            st.caption("Frames with highest AI artifacts & plastic textures.")
                            frames_to_show = [f[0] for f in sorted_frames[:4]]
                        else:
                            st.markdown("### ✅ Verified Authentic Frames")
                            st.caption("Frames demonstrating authentic camera noise and natural flaws.")
                            frames_to_show = [f[0] for f in sorted_frames[-4:]]
                            
                        if len(frames_to_show) >= 4:
                            c_img1, c_img2 = st.columns(2)
                            c_img1.image(frames_to_show[0], use_container_width=True)
                            c_img2.image(frames_to_show[1], use_container_width=True)
                            c_img1.image(frames_to_show[2], use_container_width=True)
                            c_img2.image(frames_to_show[3], use_container_width=True)
                        elif len(frames_to_show) > 0:
                            st.image(frames_to_show[0], width=200)

            except Exception as e:
                st.error(f"System Error: {e}")
            finally:
                cleanup_data()