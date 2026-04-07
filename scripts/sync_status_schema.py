#!/usr/bin/env python3
"""
Syncs the status.yaml files with the latest STAGES list from run_stage.py.
Adds missing stages initialized to done: false.
"""

from pathlib import Path
import yaml
import sys
from datetime import datetime

# Add scripts to path for importing STAGES
sys.path.insert(0, str(Path(__file__).parent))
from run_stage import STAGES

def main():
    publications_dir = Path('publications')
    status_files = list(publications_dir.glob('*/status.yaml'))
    
    print(f"Syncing schema for {len(status_files)} packages...")

    for sf in status_files:
        with open(sf, 'r') as f:
            data = yaml.safe_load(f)
        
        updated = False
        if "stages" not in data:
            data["stages"] = {}
            updated = True
            
        for stage in STAGES:
            if stage not in data["stages"]:
                data["stages"][stage] = {"done": False, "last_updated": None}
                print(f"  [{sf.parent.name}] Added missing stage: {stage}")
                updated = True
        
        if updated:
            with open(sf, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print("\nSchema sync complete.")

if __name__ == '__main__':
    main()
