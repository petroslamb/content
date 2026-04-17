import json
import os

def generate_r3_cues():
    total_duration = 2406.40
    num_slides = 17
    slide_duration = total_duration / num_slides
    
    slides_dir = "publications/confidence-debt/artifacts/slides/confidence-debt-slides-r3/"
    
    cues = []
    for i in range(1, num_slides + 1):
        slide_file = f"slide-{i:03d}.png"
        start_time = (i - 1) * slide_duration
        
        # Format start_time as HH:MM:SS.mmm
        hours = int(start_time // 3600)
        minutes = int((start_time % 3600) // 60)
        seconds = int(start_time % 60)
        millis = int((start_time * 1000) % 1000)
        timestamp = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"
        
        cues.append({
            "start": timestamp,
            "image": slide_file
        })
        
    data = {
        "audio": "publications/confidence-debt/artifacts/notebooklm/confidence-debt-audio-r3.wav",
        "slides_dir": slides_dir,
        "segments": cues
    }
    
    output_path = "publications/confidence-debt/artifacts/cue_sheet_r3_final.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    generate_r3_cues()
