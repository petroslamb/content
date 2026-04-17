#!/usr/bin/env python3
"""
Upload publication Shorts from a package portrait folder, add them to a target
playlist, and set the related long-form video reference when possible.

Run from project root:
  .venv/bin/python scripts/upload_publication_shorts.py \
    --package <package_name> \
    --main-video-id <main_video_id> \
    --playlist-id <shorts_playlist_id> \
    --essay-url <canonical_essay_url|none> \
    --full-video-url <longform_video_url> \
    [--tldr-url <tldr_video_url>] \
    [--apply]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from probe_shorts_media import probe_files

# Add the youtube skill scripts directory to path.
sys.path.insert(0, str(Path(__file__).parent.parent / "workflows" / "skills" / "youtube-data-api" / "scripts"))

try:
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    from youtube_common import build_youtube
except ImportError:
    print("ERROR: Could not import YouTube client libraries. Make sure you are running from the project root.")
    sys.exit(1)


OMIT_ESSAY_VALUES = {"none", "skip", "omit"}


def normalize_title(title: str) -> str:
    return title if "#shorts" in title.lower() else f"{title} #shorts"


def default_report_path(package: str) -> Path:
    return Path("publications") / package / "artifacts" / "video" / "shorts" / "shorts_upload_report.json"


def readback_videos(youtube: Any, video_ids: list[str]) -> dict[str, dict[str, Any]]:
    if not video_ids:
        return {}
    response = youtube.videos().list(
        part="snippet,status,contentDetails",
        id=",".join(video_ids),
    ).execute()
    return {item["id"]: item for item in response.get("items", [])}


def find_playlist_entries(youtube: Any, playlist_id: str, video_ids: list[str]) -> dict[str, dict[str, Any]]:
    wanted = set(video_ids)
    found: dict[str, dict[str, Any]] = {}
    page_token = None
    while wanted:
        response = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token,
        ).execute()
        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            video_id = snippet.get("resourceId", {}).get("videoId")
            if video_id in wanted:
                found[video_id] = {
                    "playlist_item_id": item.get("id"),
                    "position": snippet.get("position"),
                    "title": snippet.get("title"),
                }
                wanted.remove(video_id)
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return found


def write_report(report_path: Path, payload: dict[str, Any]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, indent=2) + "\n")


def build_description(
    *,
    title: str,
    summary: str,
    package_hashtag: str,
    essay_url: str | None,
    full_video_url: str,
    tldr_url: str | None,
) -> str:
    description_lines = [
        title,
        "",
        "Short clip from a Rooted Layers long-form research video.",
        "",
    ]
    if summary:
        description_lines.extend([summary, ""])
    if essay_url and essay_url.lower() not in OMIT_ESSAY_VALUES:
        description_lines.append(f"Original essay: {essay_url}")
    description_lines.append(f"Full visual deep dive: {full_video_url}")
    if tldr_url:
        description_lines.append(f"TL;DR video: {tldr_url}")
    description_lines.extend(["", f"#{package_hashtag} #ai #research #shorts"])
    return "\n".join(description_lines)


def upload_shorts(
    *,
    youtube: Any,
    planned_items: list[dict[str, Any]],
    playlist_id: str,
    main_video_id: str,
    privacy: str,
    full_video_url: str,
    tldr_url: str | None,
    essay_url: str | None,
    package_hashtag: str,
    tags: list[str],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in planned_items:
        video_path = Path(item["video_path"])
        title = item["title"]
        full_title = normalize_title(title)
        publish_at = item.get("publish_at")
        upload_privacy = "private" if publish_at else privacy
        description = build_description(
            title=title,
            summary=item.get("summary", ""),
            package_hashtag=package_hashtag,
            essay_url=essay_url,
            full_video_url=full_video_url,
            tldr_url=tldr_url,
        )

        print(f"Uploading: {full_title}")
        print(f"From: {video_path}")

        body: dict[str, Any] = {
            "snippet": {
                "title": full_title,
                "description": description,
                "tags": tags,
                "categoryId": "27",
                "defaultLanguage": "en",
            },
            "status": {
                "privacyStatus": upload_privacy,
                "selfDeclaredMadeForKids": False,
            },
        }
        if publish_at:
            body["status"]["publishAt"] = publish_at

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=MediaFileUpload(str(video_path), mimetype="video/mp4", chunksize=-1, resumable=True),
        )

        response = None
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    print(f"  Upload progress: {int(status.progress() * 100)}%")
            except HttpError as exc:
                print(f"  Upload failed: {exc}")
                raise

        video_id = response["id"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"  Uploaded! Video ID: {video_id}")
        print(f"  URL: {url}")

        playlist_status: dict[str, Any]
        try:
            playlist_response = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video_id},
                    }
                },
            ).execute()
            playlist_status = {"ok": True, "playlist_item_id": playlist_response.get("id")}
            print(f"  Added to playlist: {playlist_id}")
        except HttpError as exc:
            playlist_status = {"ok": False, "error": str(exc)}
            print(f"  Could not add to playlist: {exc}")

        related_status: dict[str, Any]
        try:
            youtube.videos().update(
                part="status",
                body={
                    "id": video_id,
                    "status": {
                        "privacyStatus": upload_privacy,
                        "selfDeclaredMadeForKids": False,
                        "relatedVideoIds": [main_video_id],
                        **({"publishAt": publish_at} if publish_at else {}),
                    },
                },
            ).execute()
            related_status = {"ok": True, "relatedVideoIds": [main_video_id]}
            print(f"  Set related video: {main_video_id}")
        except HttpError as exc:
            related_status = {"ok": False, "error": str(exc)}
            print(f"  Could not set related video: {exc}")

        results.append(
            {
                "video_path": str(video_path),
                "title": full_title,
                "summary": item.get("summary", ""),
                "publish_at": publish_at,
                "video_id": video_id,
                "url": url,
                "playlist": playlist_status,
                "related_video": related_status,
            }
        )
        print()
        time.sleep(1)
    return results


def build_report(
    *,
    workflow: str,
    playlist_id: str,
    main_video_id: str,
    full_video_url: str,
    planned_items: list[dict[str, Any]],
    probes: list[dict[str, Any]],
    upload_results: list[dict[str, Any]],
    readback: dict[str, dict[str, Any]],
    playlist_entries: dict[str, dict[str, Any]],
    privacy: str,
) -> dict[str, Any]:
    probe_by_path = {item["path"]: item for item in probes}
    items: list[dict[str, Any]] = []
    for result in upload_results:
        video_id = result["video_id"]
        remote = readback.get(video_id, {})
        items.append(
            {
                **result,
                "probe": probe_by_path.get(result["video_path"]),
                "youtube_readback": {
                    "upload_status": remote.get("status", {}).get("uploadStatus"),
                    "privacy_status": remote.get("status", {}).get("privacyStatus"),
                    "duration": remote.get("contentDetails", {}).get("duration"),
                    "definition": remote.get("contentDetails", {}).get("definition"),
                    "title": remote.get("snippet", {}).get("title"),
                    "published_at": remote.get("snippet", {}).get("publishedAt"),
                },
                "playlist_readback": playlist_entries.get(video_id),
            }
        )
    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "workflow": workflow,
        "playlist_id": playlist_id,
        "related_longform": {
            "id": main_video_id,
            "url": full_video_url,
        },
        "privacy": privacy,
        "planned_count": len(planned_items),
        "uploaded_count": len(upload_results),
        "items": items,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload publication shorts to YouTube.")
    parser.add_argument("--package", required=True, help="Package path under publications, e.g. confidence-debt")
    parser.add_argument("--main-video-id", required=True, help="Main long-form video ID for the Shorts related-video field")
    parser.add_argument("--playlist-id", required=True, help="Target Shorts playlist ID")
    parser.add_argument(
        "--essay-url",
        required=True,
        help="Canonical essay URL. Use none, skip, or omit to leave this line out of descriptions.",
    )
    parser.add_argument("--full-video-url", required=True, help="Public URL for the long-form video")
    parser.add_argument("--tldr-url", help="Optional public URL for the TL;DR companion")
    parser.add_argument("--manifest", type=Path, help="Optional manifest JSON to control titles, summaries, ordering, and scheduling.")
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"], help="Privacy status (default: public)")
    parser.add_argument("--report-file", type=Path, help="Where to write the upload report. Defaults to the package shorts folder.")
    parser.add_argument("--skip-probe", action="store_true", help="Skip local 1080x1920/audio/duration preflight checks.")
    parser.add_argument("--max-duration", type=float, default=180.0, help="Maximum allowed local clip duration in seconds.")
    parser.add_argument("--apply", action="store_true", help="Upload and mutate YouTube state. Without this, print the plan only.")
    return parser.parse_args()


def collect_planned_items(args: argparse.Namespace, shorts_dir: Path) -> list[dict[str, Any]]:
    planned_items: list[dict[str, Any]] = []
    if args.manifest:
        manifest = json.loads(args.manifest.read_text())
        for index, clip in enumerate(manifest.get("clips", []), start=1):
            video_path = shorts_dir / f"{index:02d}-{clip['slug']}_portrait.mp4"
            if not video_path.exists():
                print(f"WARNING: Missing portrait clip for manifest entry, skipping: {video_path}")
                continue
            planned_items.append(
                {
                    "video_path": video_path,
                    "title": clip["title"],
                    "summary": clip.get("summary", ""),
                    "publish_at": clip.get("publish_at"),
                }
            )
    else:
        for video_path in sorted(shorts_dir.glob("*.mp4")):
            planned_items.append(
                {
                    "video_path": video_path,
                    "title": video_path.stem.replace("_portrait", "").replace("_", " "),
                    "summary": "",
                    "publish_at": None,
                }
            )
    return planned_items


def main() -> None:
    args = parse_args()
    youtube = build_youtube()
    shorts_dir = Path("publications") / args.package / "artifacts" / "video" / "shorts" / "portrait"
    if not shorts_dir.exists():
        print(f"ERROR: Shorts directory not found: {shorts_dir}")
        sys.exit(1)

    planned_items = collect_planned_items(args, shorts_dir)
    if not planned_items:
        print(f"No .mp4 files found in {shorts_dir}")
        sys.exit(0)

    video_paths = [Path(item["video_path"]) for item in planned_items]
    probes = [] if args.skip_probe else probe_files(video_paths, max_duration=args.max_duration)
    failed_probes = [item for item in probes if not item["ok"]]
    if failed_probes:
        print("ERROR: Shorts preflight failed:")
        for item in failed_probes:
            print(f" - {item['path']}: {'; '.join(item['errors'])}")
        sys.exit(1)

    print(f"Found {len(planned_items)} short(s) to upload")
    print(f"Target playlist: {args.playlist_id}")
    print(f"Related long-form video: https://www.youtube.com/watch?v={args.main_video_id}")
    report_path = args.report_file or default_report_path(args.package)
    print(f"Upload report: {report_path}")

    if not args.apply:
        print("\nDry run only. Add --apply to upload and write YouTube state.")
        for item in planned_items:
            schedule_suffix = f" @ {item['publish_at']}" if item["publish_at"] else ""
            print(f" - {normalize_title(item['title'])} <- {Path(item['video_path']).name}{schedule_suffix}")
        return

    tags = ["AI", "research", "shorts", *args.package.split("-")]
    package_hashtag = args.package.replace("-", "").replace("/", "")
    upload_results = upload_shorts(
        youtube=youtube,
        planned_items=planned_items,
        playlist_id=args.playlist_id,
        main_video_id=args.main_video_id,
        privacy=args.privacy,
        full_video_url=args.full_video_url,
        tldr_url=args.tldr_url,
        essay_url=args.essay_url,
        package_hashtag=package_hashtag,
        tags=tags,
    )
    video_ids = [item["video_id"] for item in upload_results]
    readback = readback_videos(youtube, video_ids)
    playlist_entries = find_playlist_entries(youtube, args.playlist_id, video_ids)
    report = build_report(
        workflow="publication_shorts",
        playlist_id=args.playlist_id,
        main_video_id=args.main_video_id,
        full_video_url=args.full_video_url,
        planned_items=planned_items,
        probes=probes,
        upload_results=upload_results,
        readback=readback,
        playlist_entries=playlist_entries,
        privacy=args.privacy,
    )
    write_report(report_path, report)
    print(f"All shorts upload complete. Report written to: {report_path}")


if __name__ == "__main__":
    main()
