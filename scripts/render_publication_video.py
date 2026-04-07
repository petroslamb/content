#!/usr/bin/env python3
"""
Render the final publication video from prepared cues.
Run from project root: .venv/bin/python scripts/render_publication_video.py --package <package_name>
"""

import sys
import argparse
from pathlib import Path

# Add the scripts directory to path
sys.path.insert(0, 'scripts')

try:
    from render_audio_slides_video import render_video
except ImportError:
    print("ERROR: Could not import render_video from scripts. Make sure you are running from the project root.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Render the final publication video.")
    parser.add_argument("--package", required=True, help="Package name (e.g., illusion-of-swarm)")
    parser.add_argument("--cues", help="Override cues path (relative to package artifacts/video/)")
    parser.add_argument("--output", help="Override output filename (relative to package artifacts/video/)")
    parser.add_argument("--fps", type=int, default=5, help="FPS for rendering (default: 5)")
    args = parser.parse_args()

    package_path = Path('publications') / args.package
    if not package_path.exists():
        print(f"ERROR: Package {args.package} not found in publications/")
        sys.exit(1)

    artifacts_dir = package_path / 'artifacts' / 'video'
    
    # Default paths
    cues_filename = args.cues if args.cues else f"{args.package.replace('-', '_')}_final_cues.json"
    output_filename = args.output if args.output else f"{args.package.replace('-', '_').title()}_video.mp4"
    
    cues_path = artifacts_dir / cues_filename
    output_path = artifacts_dir / output_filename

    if not cues_path.exists():
        print(f"ERROR: Cues file not found at {cues_path}")
        # Try a fallback if final_cues doesn't exist
        fallback_cues = list(artifacts_dir.glob("*_cues.json"))
        if fallback_cues:
            print(f"Available cue files: {[f.name for f in fallback_cues]}")
        sys.exit(1)

    print(f"Rendering video from: {cues_path}")
    print(f"Output will be: {output_path}")
    print(f"FPS: {args.fps}")
    print("This will take some time. Starting...")

    render_video(cues_path, output_path, fps=args.fps, width=1920, height=1080)

    print(f"\n✅ Video rendered successfully to: {output_path}")
    if output_path.exists():
        print(f"File size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")

if __name__ == '__main__':
    main()
