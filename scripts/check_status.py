#!/usr/bin/env python3
"""
Display a status table for all publications based on status.yaml files.
Run from project root: .venv/bin/python scripts/check_status.py
"""

import os
from pathlib import Path
import yaml
from datetime import datetime

def main():
    publications_dir = Path('publications')
    if not publications_dir.exists():
        print("ERROR: publications/ directory not found.")
        return

    # Find all packages with status.yaml
    status_files = sorted(publications_dir.glob('*/status.yaml'))
    
    if not status_files:
        print("No status.yaml files found in publications/ subdirectories.")
        return

    # Load all status data
    all_status = []
    for sf in status_files:
        with open(sf, 'r') as f:
            all_status.append(yaml.safe_load(f))

    if not all_status:
        return

    # Get all stage names (from the first one)
    stages = list(all_status[0]['stages'].keys())
    
    # Header
    pkg_name_width = max(len(s['publication']) for s in all_status)
    pkg_name_width = max(pkg_name_width, 14)
    
    header = f"{'Publication':<{pkg_name_width}} | rev | "
    subheader = f"{'-' * pkg_name_width}-|-----|--"
    for stage in stages:
        short_name = "".join([w[0] for w in stage.split('_')])
        header += f"{short_name:^3} | "
        subheader += f"{'-' * 3}-|-"
    
    print(header)
    print(subheader)

    for status in all_status:
        rev = status.get('revision', 1)
        row = f"{status['publication']:<{pkg_name_width}} | {rev:>3} | "
        for stage in stages:
            done = status['stages'][stage].get('done', False)
            icon = " [x]" if done else " [ ]"
            row += f"{icon:^3} | "
        print(row)

    print("\nLegend:")
    for stage in stages:
        short_name = "".join([w[0] for w in stage.split('_')])
        print(f"  {short_name}: {stage.replace('_', ' ').title()}")

if __name__ == '__main__':
    main()
