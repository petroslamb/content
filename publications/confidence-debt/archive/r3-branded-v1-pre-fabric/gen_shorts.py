import subprocess
import os

def render_short(name, start_time, slide_path, audio_path, output_path):
    # Short: 1080x1920, 30 fps, AAC audio
    ffmpeg_path = "/opt/homebrew/bin/ffmpeg"
    
    # 1. Slice 60s of audio
    # 2. Overlay slide on vertical canvas
    cmd = [
        ffmpeg_path, "-y",
        "-ss", start_time,
        "-t", "60",
        "-i", audio_path,
        "-loop", "1",
        "-i", slide_path,
        "-filter_complex", (
            "[1:v]scale=1080:607,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black[v]"
        ),
        "-map", "[v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-preset", "medium",
        "-shortest",
        output_path
    ]
    
    print(f"Rendering {name}...")
    subprocess.run(cmd, check=True)

def main():
    audio_path = "publications/confidence-debt/artifacts/notebooklm/confidence-debt-audio-r3.wav"
    slides_base = "publications/confidence-debt/artifacts/slides/confidence-debt-slides-r3/"
    os.makedirs("publications/confidence-debt/artifacts/shorts", exist_ok=True)
    
    shorts = [
        ("gate-1-auditability", "00:16:30.870", os.path.join(slides_base, "slide-008.png")),
        ("gate-2-reliability", "00:21:13.976", os.path.join(slides_base, "slide-010.png")),
        ("gate-3-co-audit", "00:28:18.635", os.path.join(slides_base, "slide-013.png"))
    ]
    
    for name, start, slide in shorts:
        output = f"publications/confidence-debt/artifacts/shorts/{name}-short-r3.mp4"
        render_short(name, start, slide, audio_path, output)

if __name__ == "__main__":
    main()
