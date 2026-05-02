import os
import cv2
import glob
import shutil

def extract_frames(video_path, output_dir="temp_frames", frame_interval=30, status_element=None):
    """
    Splits video into images with Smart Duration Detection AND Live UI Updates.
    """

    # Clean old frames
    if os.path.exists(output_dir):
        try:
            shutil.rmtree(output_dir)
        except Exception:
            pass
    os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"❌ Error opening {video_path}")
        return []

    # --- SMART OPTIMIZATION LOGIC ---
    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        if fps > 0:
            duration_sec = total_frames / fps
        else:
            duration_sec = 0

        print(f"📏 Video Duration: {duration_sec:.1f} seconds")

        # 🔥 Optimized sampling
        if duration_sec <= 30:
            print("⚡ Short video → every ~2 sec")
            frame_interval = int(fps * 2)

        elif duration_sec <= 90:
            print("⚡ Medium video → every ~3.5 sec")
            frame_interval = int(fps * 3.5)

        else:
            print("⚡ Long video → every ~5 sec")
            frame_interval = int(fps * 5)

        if frame_interval <= 0:
            frame_interval = 30

    except Exception as e:
        print(f"⚠️ Warning: Could not detect duration ({e}). Using default interval.")

    # --- EXTRACTION LOOP ---
    frame_count = 0
    saved = 0
    paths = []

    print(f"🎞️ Processing frames (Interval: every {frame_interval} frames)...")

    max_frames = 25  # 🔥 limit frames for speed

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            name = f"{output_dir}/frame_{saved}.jpg"
            cv2.imwrite(name, frame)
            paths.append(name)
            saved += 1

            if status_element:
                status_element.markdown(
                    f'<div class="frame-log">🎞️ Extracted Frame {saved}...</div>',
                    unsafe_allow_html=True
                )

            # 🔥 Stop early if enough frames
            if saved >= max_frames:
                print("⚡ Max frame limit reached.")
                break

        frame_count += 1

    cap.release()
    print(f"✅ Done. Extracted {saved} frames.")
    return paths


if __name__ == "__main__":
    videos = glob.glob("temp_videos/*.mp4")
    if videos:
        extract_frames(videos[0])
    else:
        print("No videos found to extract.")