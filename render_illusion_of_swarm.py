#!/usr/bin/env python3
"""
Render the final Illusion of Swarm video from prepared cues.
Run from project root: .venv/bin/python render_illusion_of_swarm.py
"""

from pathlib import Path
import sys

sys.path.insert(0, 'scripts')

from render_audio_slides_video import render_video

def main():
    cues_path = Path('publications/illusion-of-swarm/artifacts/video/illusion_of_swarm_final_cues.json')
    output_path = Path('publications/illusion-of-swarm/artifacts/video/Illusion_of_Swarm_video.mp4')

    print(f"Rendering video from: {cues_path}")
    print(f"Output will be: {output_path}")
    print("This will take ~30-60 minutes. Starting...")

    render_video(cues_path, output_path, fps=30, width=1920, height=1080)

    print(f"\n✅ Video rendered successfully to: {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")

if __name__ == '__main__':
    main()
