#!/usr/bin/env python3
"""Upload arbitrary local portrait clips as public or scheduled Shorts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from convert_landscape_videos_to_portrait import collect_inputs, convert_video
from probe_shorts_media import probe_files
from upload_publication_shorts import (
    build_report,
    find_playlist_entries,
    normalize_title,
    readback_videos,
    upload_shorts,
    write_report,
)

sys.path.insert(0, str(Path(__file__).parent.parent / "workflows" / "skills" / "youtube-data-api" / "scripts"))

try:
    from youtube_common import build_youtube
except ImportError:
    print("ERROR: Could not import YouTube client libraries. Make sure you are running from the project root.")
    sys.exit(1)


def load_manifest(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path:
        return {}
    data = json.loads(path.read_text())
    entries = data.get("clips", data if isinstance(data, list) else [])
    return {entry["file"]: entry for entry in entries}


def title_from_stem(path: Path) -> str:
    title = path.stem.replace("_portrait", "").replace("_", " ").replace("-", " ")
    title = re.sub(r"^\d+\s+", "", title)
    return " ".join(word.capitalize() for word in title.split())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Upload arbitrary local clips as Shorts. Inputs may be portrait masters, or landscape clips "
            "when --convert-from-landscape and --work-dir are provided."
        )
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="MP4 files or directories.")
    parser.add_argument("--main-video-id", required=True, help="Main long-form video ID for the related-video field.")
    parser.add_argument("--playlist-id", required=True, help="Target Shorts playlist ID.")
    parser.add_argument("--full-video-url", required=True, help="Public URL for the long-form video.")
    parser.add_argument("--manifest", type=Path, help="Optional JSON with clips: [{file,title,summary,publish_at}].")
    parser.add_argument("--report-file", type=Path, required=True, help="Where to write the upload report.")
    parser.add_argument("--convert-from-landscape", action="store_true", help="Convert 16:9 inputs to portrait before upload.")
    parser.add_argument("--work-dir", type=Path, help="Directory for converted portrait outputs.")
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"])
    parser.add_argument("--essay-url", help="Optional essay URL. Use none, skip, or omit to leave it out.")
    parser.add_argument("--tldr-url", help="Optional TL;DR video URL.")
    parser.add_argument("--hashtag", default="adhocshorts", help="Primary description hashtag without #.")
    parser.add_argument("--tag", action="append", default=[], help="Additional YouTube tag. May be repeated.")
    parser.add_argument("--max-duration", type=float, default=180.0)
    parser.add_argument("--skip-probe", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Upload and mutate YouTube state. Without this, print the plan only.")
    return parser.parse_args()


def prepare_inputs(args: argparse.Namespace) -> list[Path]:
    inputs = collect_inputs(args.inputs)
    if not args.convert_from_landscape:
        return inputs
    if not args.work_dir:
        raise ValueError("--work-dir is required with --convert-from-landscape")
    outputs: list[Path] = []
    for input_path in inputs:
        output_path = args.work_dir / f"{input_path.stem}_portrait.mp4"
        convert_video(
            input_path=input_path,
            output_path=output_path,
            width=1080,
            height=1920,
            fps=24,
            video_bitrate="6M",
            audio_bitrate="192k",
        )
        outputs.append(output_path)
    return outputs


def main() -> None:
    args = parse_args()
    videos = prepare_inputs(args)
    manifest = load_manifest(args.manifest)
    planned_items: list[dict[str, Any]] = []
    for video_path in videos:
        entry = manifest.get(video_path.name) or manifest.get(video_path.stem) or {}
        planned_items.append(
            {
                "video_path": video_path,
                "title": entry.get("title", title_from_stem(video_path)),
                "summary": entry.get("summary", ""),
                "publish_at": entry.get("publish_at"),
            }
        )

    probes = [] if args.skip_probe else probe_files(videos, max_duration=args.max_duration)
    failed_probes = [item for item in probes if not item["ok"]]
    if failed_probes:
        print("ERROR: Shorts preflight failed:")
        for item in failed_probes:
            print(f" - {item['path']}: {'; '.join(item['errors'])}")
        sys.exit(1)

    print(f"Found {len(planned_items)} short(s) to upload")
    print(f"Target playlist: {args.playlist_id}")
    print(f"Related long-form video: https://www.youtube.com/watch?v={args.main_video_id}")
    print(f"Upload report: {args.report_file}")
    if not args.apply:
        print("\nDry run only. Add --apply to upload and write YouTube state.")
        for item in planned_items:
            schedule_suffix = f" @ {item['publish_at']}" if item["publish_at"] else ""
            print(f" - {normalize_title(item['title'])} <- {Path(item['video_path']).name}{schedule_suffix}")
        return

    youtube = build_youtube()
    upload_results = upload_shorts(
        youtube=youtube,
        planned_items=planned_items,
        playlist_id=args.playlist_id,
        main_video_id=args.main_video_id,
        privacy=args.privacy,
        full_video_url=args.full_video_url,
        tldr_url=args.tldr_url,
        essay_url=args.essay_url,
        package_hashtag=args.hashtag,
        tags=["AI", "research", "shorts", *args.tag],
    )
    video_ids = [item["video_id"] for item in upload_results]
    report = build_report(
        workflow="ad_hoc_shorts",
        playlist_id=args.playlist_id,
        main_video_id=args.main_video_id,
        full_video_url=args.full_video_url,
        planned_items=planned_items,
        probes=probes,
        upload_results=upload_results,
        readback=readback_videos(youtube, video_ids),
        playlist_entries=find_playlist_entries(youtube, args.playlist_id, video_ids),
        privacy=args.privacy,
    )
    write_report(args.report_file, report)
    print(f"All ad hoc shorts upload complete. Report written to: {args.report_file}")


if __name__ == "__main__":
    main()
