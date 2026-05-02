import yt_dlp # type: ignore
import os
import shutil
import re

def strip_ansi(text):
    """Removes weird terminal color codes (like [0;94m) from the text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def download_video(url, output_folder="temp_videos", status_element=None):
    # 1. Clean previous temp folder
    if os.path.exists(output_folder):
        try:
            shutil.rmtree(output_folder)
        except Exception:
            pass
    os.makedirs(output_folder)

    # 2. Define the Progress Hook
    def progress_hook(d):
        if d['status'] == 'downloading':
            if status_element:
                # Get raw values from yt-dlp
                raw_percent = d.get('_percent_str', '0%')
                raw_speed = d.get('_speed_str', '0MiB/s')
                
                # Clean the weird characters using regex
                percent = strip_ansi(raw_percent).strip()
                speed = strip_ansi(raw_speed).strip()
                
                # Create the clean text
                display_text = f"⬇️ {percent} (Speed: {speed})"
                
                # Update Streamlit UI with GREEN color (#4ade80 matches your other logs)
                status_element.markdown(
                    f'<div class="frame-log" style="color: #4ade80;">{display_text}</div>', 
                    unsafe_allow_html=True
                )

    # 3. Configuration for yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_folder}/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'noprogress': False,
        'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if not status_element:
                print(f"📥 Downloading from: {url}...")
            
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            
            return filename

    except Exception as e:
        print(f"❌ Error downloading: {e}")
        return None

if __name__ == "__main__":
    test_link = input("Paste a video link: ")
    download_video(test_link)