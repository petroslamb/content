#!/usr/bin/env python3
"""
Initialize status.yaml for all publications with all stages set to done: false.
Run from project root: .venv/bin/python scripts/init_status.py
"""

import os
from pathlib import Path
import yaml

STAGES = [
    "paper_intake",
    "research",
    "essay_iteration",
    "notebooklm_artifacts",
    "article_polish",
    "substack_publishing",
    "archive_sync",
    "youtube_production"
]

def main():
    publications_dir = Path('publications')
    if not publications_dir.exists():
        print("ERROR: publications/ directory not found.")
        return

    # Get all subdirectories that have a README.md (assuming they are packages)
    packages = [d for d in publications_dir.iterdir() if d.is_dir() and (d / 'README.md').exists()]
    
    print(f"Initializing status for {len(packages)} packages...")

    for package in packages:
        status_file = package / 'status.yaml'
        
        # We don't overwrite if it already exists, unless forced (not implemented here)
        if status_file.exists():
            print(f"  Skipping {package.name} (status.yaml already exists)")
            continue

        status_data = {
            "publication": package.name,
            "stages": {stage: {"done": False, "last_updated": None} for stage in STAGES}
        }

        with open(status_file, 'w') as f:
            yaml.dump(status_data, f, default_flow_style=False, sort_keys=False)
        
        print(f"  Initialized {package.name}/status.yaml")

    print("\nInitialization complete.")

if __name__ == '__main__':
    main()
