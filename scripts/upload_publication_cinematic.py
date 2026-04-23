#!/usr/bin/env python3
"""
Upload one manifest-driven cinematic companion, create or reuse the shared
cinematic playlist, and write the upload report into the publication artifact
surface.

Run from project root:
  .venv/bin/python scripts/upload_publication_cinematic.py \
    --manifest experiments/youtube-cinematic-pilot/pilot_manifest.yaml \
    --publication neural_architecture
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# Add the youtube skill scripts directory to path.
sys.path.insert(0, str(Path(__file__).parent.parent / "workflows" / "skills" / "youtube-data-api" / "scripts"))

try:
    from googleapiclient.http import MediaFileUpload
    from youtube_common import build_youtube
except ImportError:
    print("ERROR: Could not import YouTube client libraries. Make sure you are running from the project root.")
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload one cinematic publication companion from the experiment manifest.")
    parser.add_argument("--manifest", type=Path, required=True, help="Pilot manifest YAML, e.g. experiments/youtube-cinematic-pilot/pilot_manifest.yaml")
    parser.add_argument("--publication", required=True, help="Publication key inside the manifest, e.g. neural_architecture")
    parser.add_argument("--report-file", type=Path, help="Optional report-file override. Defaults to the publication-local upload_report path.")
    parser.add_argument("--apply", action="store_true", help="Upload and mutate YouTube state. Without this, print the plan only.")
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: Expected a mapping at {path}")
    return data


def get_required(mapping: dict[str, Any], key: str, context: str) -> Any:
    value = mapping.get(key)
    if value in (None, ""):
        raise SystemExit(f"ERROR: Missing required field '{key}' in {context}")
    return value


def playlist_url(playlist_id: str | None, playlist_title: str) -> str:
    if playlist_id:
        return f"https://www.youtube.com/playlist?list={playlist_id}"
    return f"<playlist-url for '{playlist_title}'>"


def render_generation_command(notebook_id: str, prompt_file: Path) -> str:
    return (
        ".venv/bin/notebooklm generate video "
        f"-n {notebook_id} --retry 3 --json --format cinematic "
        f'"$(cat {prompt_file})"'
    )


def render_description(
    *,
    template_path: Path,
    title: str,
    hook: str,
    summary: str,
    essay_url: str,
    secondary_link_url: str,
    cinematic_playlist_url: str,
) -> str:
    template = template_path.read_text(encoding="utf-8")
    return template.format(
        title=title,
        hook=hook.strip(),
        summary=summary.strip(),
        essay_url=essay_url.strip(),
        baseline_longform_url=secondary_link_url.strip(),
        cinematic_playlist_url=cinematic_playlist_url.strip(),
    ).strip()


def find_playlist_by_title(youtube: Any, title: str) -> str | None:
    page_token = None
    while True:
        response = youtube.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=page_token,
        ).execute()
        for item in response.get("items", []):
            if item.get("snippet", {}).get("title") == title:
                return item["id"]
        page_token = response.get("nextPageToken")
        if not page_token:
            return None


def create_playlist(youtube: Any, title: str, description: str, privacy_status: str) -> str:
    response = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
            },
            "status": {
                "privacyStatus": privacy_status,
            },
        },
    ).execute()
    return response["id"]


def upload_video(
    *,
    youtube: Any,
    file_path: Path,
    title: str,
    description: str,
    privacy_status: str,
    publish_at: str | None,
    tags: list[str],
) -> str:
    body: dict[str, Any] = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27",
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,
        },
    }
    if publish_at:
        body["status"]["publishAt"] = publish_at

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(file_path), mimetype="video/mp4", chunksize=-1, resumable=True),
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading {file_path.name}: {int(status.progress() * 100)}%")
    return response["id"]


def add_to_playlist(youtube: Any, playlist_id: str, video_id: str) -> str:
    response = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    ).execute()
    return response["id"]


def readback_video(youtube: Any, video_id: str) -> dict[str, Any]:
    response = youtube.videos().list(part="snippet,status,contentDetails", id=video_id).execute()
    items = response.get("items", [])
    return items[0] if items else {}


def readback_playlist_item(youtube: Any, playlist_id: str, video_id: str) -> dict[str, Any] | None:
    page_token = None
    while True:
        response = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token,
        ).execute()
        for item in response.get("items", []):
            if item.get("snippet", {}).get("resourceId", {}).get("videoId") == video_id:
                return {
                    "playlist_item_id": item.get("id"),
                    "position": item.get("snippet", {}).get("position"),
                    "title": item.get("snippet", {}).get("title"),
                }
        page_token = response.get("nextPageToken")
        if not page_token:
            return None


def default_report_path(package: str) -> Path:
    return Path("publications") / package / "artifacts" / "video" / "cinematic_upload_report.json"


def write_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    manifest = load_manifest(args.manifest)

    experiment = get_required(manifest, "experiment", str(args.manifest))
    publications = get_required(manifest, "publications", str(args.manifest))
    if args.publication not in publications:
        raise SystemExit(f"ERROR: Publication key '{args.publication}' not found in {args.manifest}")

    publication = publications[args.publication]
    package = get_required(publication, "package", f"{args.publication}")
    notebook_id = get_required(publication, "notebook_id", f"{args.publication}")
    essay_url = get_required(publication, "essay_url", f"{args.publication}")
    secondary_link = publication.get("secondary_link") or {}
    secondary_link_label = secondary_link.get("label") or "Full research breakdown"
    secondary_link_video_id = publication.get("baseline_longform_video_id") or secondary_link.get("video_id")
    secondary_link_url = publication.get("baseline_longform_url") or secondary_link.get("url") or essay_url

    cinematic = get_required(publication, "cinematic", f"{args.publication}")
    title = get_required(cinematic, "title", f"{args.publication}.cinematic")
    hook = get_required(cinematic, "hook", f"{args.publication}.cinematic")
    summary = get_required(cinematic, "summary", f"{args.publication}.cinematic")
    video_file = Path(get_required(cinematic, "video_file", f"{args.publication}.cinematic"))
    output_srt = Path(get_required(cinematic, "output_srt", f"{args.publication}.cinematic"))
    report_path = args.report_file or Path(cinematic.get("upload_report") or default_report_path(package))
    publish_at = cinematic.get("publish_at")

    templates = get_required(experiment, "templates", f"{args.manifest}:experiment")
    description_template = Path(get_required(templates, "cinematic_description", f"{args.manifest}:experiment.templates"))
    prompt_file = Path(get_required(templates, "cinematic_prompt", f"{args.manifest}:experiment.templates"))

    experiment_playlist = get_required(get_required(experiment, "playlists", f"{args.manifest}:experiment"), "cinematic", f"{args.manifest}:experiment.playlists")
    playlist_config = {**experiment_playlist, **(cinematic.get("playlist") or {})}
    playlist_title = get_required(playlist_config, "title", f"{args.publication}.cinematic.playlist")
    playlist_id = playlist_config.get("id")
    playlist_description = playlist_config.get("description") or experiment_playlist.get("description", "")
    playlist_privacy = playlist_config.get("privacy_status") or experiment_playlist.get("privacy_status", "public")
    create_if_missing = playlist_config.get("create_if_missing", experiment_playlist.get("create_if_missing", True))

    defaults = experiment.get("defaults", {})
    upload_privacy = "private" if publish_at else defaults.get("upload_privacy", "public")
    tags = [str(tag) for tag in cinematic.get("tags", ["AI", "research", "cinematic", *package.split("-")])]

    placeholder_playlist_url = playlist_url(playlist_id, playlist_title)
    description_preview = render_description(
        template_path=description_template,
        title=title,
        hook=hook,
        summary=summary,
        essay_url=essay_url,
        secondary_link_url=secondary_link_url,
        cinematic_playlist_url=placeholder_playlist_url,
    )

    generation_command = render_generation_command(notebook_id, prompt_file)
    plan = {
        "publication": args.publication,
        "package": package,
        "notebook_id": notebook_id,
        "video_file": str(video_file),
        "video_file_exists": video_file.exists(),
        "output_srt": str(output_srt),
        "title": title,
        "secondary_link": {
            "label": secondary_link_label,
            "video_id": secondary_link_video_id,
            "url": secondary_link_url,
        },
        "essay_url": essay_url,
        "playlist": {
            "id": playlist_id,
            "title": playlist_title,
            "description": playlist_description,
            "privacy_status": playlist_privacy,
            "create_if_missing": create_if_missing,
        },
        "publish_at": publish_at,
        "upload_privacy": upload_privacy,
        "report_file": str(report_path),
        "description_preview": description_preview,
        "generation_command": generation_command,
    }

    print(json.dumps({"plan": plan}, indent=2))
    if not video_file.exists():
        print("\nWARNING: Cinematic video file does not exist yet.")
        print("Generate it with:")
        print(generation_command)

    if not args.apply:
        return

    if not video_file.exists():
        raise SystemExit(f"ERROR: Missing cinematic video file: {video_file}")

    youtube = build_youtube()
    playlist_created = False
    if not playlist_id:
        playlist_id = find_playlist_by_title(youtube, playlist_title)
        if not playlist_id and create_if_missing:
            playlist_id = create_playlist(youtube, playlist_title, playlist_description, playlist_privacy)
            playlist_created = True
        elif not playlist_id:
            raise SystemExit(f"ERROR: Playlist '{playlist_title}' not found and create_if_missing is false.")

    final_description = render_description(
        template_path=description_template,
        title=title,
        hook=hook,
        summary=summary,
        essay_url=essay_url,
        secondary_link_url=secondary_link_url,
        cinematic_playlist_url=playlist_url(playlist_id, playlist_title),
    )
    video_id = upload_video(
        youtube=youtube,
        file_path=video_file,
        title=title,
        description=final_description,
        privacy_status=upload_privacy,
        publish_at=publish_at,
        tags=tags,
    )
    public_url = f"https://www.youtube.com/watch?v={video_id}"
    playlist_item_id = add_to_playlist(youtube, playlist_id, video_id)
    remote = readback_video(youtube, video_id)
    playlist_item = readback_playlist_item(youtube, playlist_id, video_id)

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "workflow": "publication_cinematic",
        "publication": args.publication,
        "package": package,
        "notebook_id": notebook_id,
        "video_source_file": str(video_file),
        "caption_output": str(output_srt),
        "title": title,
        "description": final_description,
        "publish_at": publish_at,
        "upload_privacy": upload_privacy,
        "playlist": {
            "id": playlist_id,
            "title": playlist_title,
            "description": playlist_description,
            "created_in_run": playlist_created,
            "playlist_item_id": playlist_item_id,
            "readback": playlist_item,
        },
        "secondary_link": {
            "label": secondary_link_label,
            "id": secondary_link_video_id,
            "url": secondary_link_url,
        },
        "essay_url": essay_url,
        "video": {
            "id": video_id,
            "url": public_url,
            "youtube_readback": {
                "upload_status": remote.get("status", {}).get("uploadStatus"),
                "privacy_status": remote.get("status", {}).get("privacyStatus"),
                "duration": remote.get("contentDetails", {}).get("duration"),
                "definition": remote.get("contentDetails", {}).get("definition"),
                "published_at": remote.get("snippet", {}).get("publishedAt"),
            },
        },
    }
    write_report(report_path, report)
    print(json.dumps({"video_id": video_id, "url": public_url, "playlist_id": playlist_id, "report_file": str(report_path)}, indent=2))


if __name__ == "__main__":
    main()
