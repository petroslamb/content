#!/usr/bin/env python3
"""
Batch update status.yaml files based on user's manual baseline.
"""

from pathlib import Path
import yaml
from datetime import datetime

YOUTUBE_DONE = ["autonomous-agents", "binding-gap", "illusion-of-swarm"]

def main():
    publications_dir = Path('publications')
    status_files = list(publications_dir.glob('*/status.yaml'))
    
    today = datetime.now().strftime("%Y-%m-%d")

    for sf in status_files:
        with open(sf, 'r') as f:
            data = yaml.safe_load(f)
        
        pub_name = data['publication']
        
        for stage_name, stage_data in data['stages'].items():
            if stage_name == 'youtube_production':
                if pub_name in YOUTUBE_DONE:
                    stage_data['done'] = True
                    stage_data['last_updated'] = today
                else:
                    stage_data['done'] = False
                    stage_data['last_updated'] = None
            else:
                # All other stages are done
                stage_data['done'] = True
                stage_data['last_updated'] = today
        
        with open(sf, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        
        print(f"Updated {sf}")

if __name__ == '__main__':
    main()
