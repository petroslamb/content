from __future__ import annotations

import argparse
import json
import re
import time
from copy import deepcopy
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Callable
from urllib.parse import quote, unquote

from markdown_it import MarkdownIt
from PIL import Image
from playwright.sync_api import sync_playwright
import substack
from substack.exceptions import SubstackAPIException


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COOKIE_PATH = Path("/tmp/substack_cookie_string.txt")
KEEP_COOKIE_NAMES = {
    "substack.sid",
    "cf_clearance",
    "__cf_bm",
    "substack.lli",
    "ajs_anonymous_id",
    "ab_experiment_sampled",
    "ab_testing_id",
    "visit_id",
    "cookie_storage_key",
    "_ga",
    "_ga_TLW0DF6G5V",
    "_gcl_au",
    "_dd_s",
    "AWSALBTG",
    "AWSALBTGCORS",
    "muxData",
}

MD = MarkdownIt()
INLINE_MD = MarkdownIt("commonmark")


@dataclass(frozen=True)
class SyncConfig:
    publication_url: str
    post_id: int
    markdown_path: Path
    publish: bool


def run_with_retry(fn: Callable, *args, **kwargs):
    delay = 5
    for attempt in range(6):
        try:
            return fn(*args, **kwargs)
        except SubstackAPIException as exc:
            if "APIError(code=429)" not in str(exc) or attempt == 5:
                raise
            time.sleep(delay)
            delay *= 2


def cookie_string_from_cdp(chrome_debug_url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(chrome_debug_url)
        if not browser.contexts:
            raise RuntimeError(f"No browser contexts found at {chrome_debug_url}")
        cookies = browser.contexts[0].cookies()
    parts = []
    for cookie in cookies:
        if "substack" in cookie.get("domain", "") and cookie["name"] in KEEP_COOKIE_NAMES:
            parts.append(f"{cookie['name']}={cookie['value']}")
    if not parts:
        raise RuntimeError(f"No reusable Substack cookies found at {chrome_debug_url}")
    return "; ".join(parts)


def load_cookie_string(cookie_path: Path | None, chrome_debug_url: str | None) -> str:
    if chrome_debug_url:
        cookie_string = cookie_string_from_cdp(chrome_debug_url)
        if cookie_path is not None:
            cookie_path.write_text(cookie_string)
        return cookie_string
    if cookie_path is None:
        raise ValueError("Provide --cookie-path or --chrome-debug-url for Substack auth.")
    cookie = cookie_path.read_text().strip()
    if not cookie:
        raise ValueError(f"Cookie file is empty: {cookie_path}")
    return cookie


def normalize_path_target(markdown_path: Path, target: str) -> str:
    if re.match(r"^[a-z]+://", target):
        return target
    resolved = (markdown_path.parent / unquote(target)).resolve()
    rel = resolved.relative_to(REPO_ROOT).as_posix()
    return f"https://github.com/petroslamb/content/blob/main/{quote(rel)}"


def parse_inline(markdown_path: Path, text: str) -> list[dict]:
    tokens = INLINE_MD.parseInline(text)
    children = tokens[0].children if tokens else []
    output: list[dict] = []
    mark_stack: list[dict] = []

    def append_text(value: str) -> None:
        if not value:
            return
        node = {"type": "text", "text": value}
        if mark_stack:
            node["marks"] = [mark.copy() for mark in mark_stack]
        output.append(node)

    for token in children:
        if token.type == "text":
            append_text(token.content)
        elif token.type == "softbreak":
            append_text("\n")
        elif token.type == "code_inline":
            output.append({"type": "text", "text": token.content, "marks": [{"type": "code"}]})
        elif token.type == "em_open":
            mark_stack.append({"type": "em"})
        elif token.type == "em_close":
            if mark_stack:
                mark_stack.pop()
        elif token.type == "strong_open":
            mark_stack.append({"type": "strong"})
        elif token.type == "strong_close":
            if mark_stack:
                mark_stack.pop()
        elif token.type == "link_open":
            href = normalize_path_target(markdown_path, token.attrGet("href") or "")
            mark_stack.append(
                {
                    "type": "link",
                    "attrs": {
                        "href": href,
                        "target": "_blank",
                        "rel": "noopener noreferrer nofollow",
                        "class": None,
                    },
                }
            )
        elif token.type == "link_close":
            if mark_stack:
                mark_stack.pop()
        elif token.type == "image":
            append_text(token.content or token.attrGet("alt") or "")

    return output


def paragraph_node(markdown_path: Path, text: str) -> dict:
    return {
        "type": "paragraph",
        "attrs": {"textAlign": None},
        "content": parse_inline(markdown_path, text),
    }


def heading_node(markdown_path: Path, text: str, level: int) -> dict:
    return {
        "type": "heading",
        "attrs": {"textAlign": None, "level": level},
        "content": parse_inline(markdown_path, text),
    }


class MarkdownPostSync:
    def __init__(self, api: substack.Api, publication_url: str):
        self.api = api
        self.publication_url = publication_url
        self.image_cache: dict[Path, dict] = {}

    def upload_image(self, image_path: Path, alt: str) -> dict:
        image_path = image_path.resolve()
        cached = self.image_cache.get(image_path)
        if cached is not None:
            return cached

        with Image.open(image_path) as img:
            rgb = img.convert("RGB")
            orig_width, orig_height = rgb.size
            buffer = BytesIO()
            rgb.save(buffer, format="JPEG", quality=92)
            payload = buffer.getvalue()

        tmp_path = image_path.with_suffix(".codex-upload.jpg")
        tmp_path.write_bytes(payload)
        try:
            upload = run_with_retry(self.api.get_image, str(tmp_path))
        finally:
            tmp_path.unlink(missing_ok=True)

        display_width = min(1456, orig_width)
        display_height = round(orig_height * display_width / orig_width)
        node = {
            "type": "captionedImage",
            "content": [
                {
                    "type": "image2",
                    "attrs": {
                        "src": upload["url"],
                        "srcNoWatermark": None,
                        "fullscreen": False,
                        "imageSize": "normal",
                        "height": display_height,
                        "width": display_width,
                        "resizeWidth": 728 if display_width >= 728 else display_width,
                        "bytes": upload["bytes"],
                        "alt": alt or None,
                        "title": None,
                        "type": "captionedImage",
                        "href": None,
                        "belowTheFold": False,
                        "topImage": False,
                        "internalRedirect": None,
                        "isProcessing": False,
                        "align": None,
                        "offset": False,
                    },
                }
            ],
        }
        self.image_cache[image_path] = node
        return node

    def video_node_from_draft(self, draft: dict, existing_doc: dict) -> dict | None:
        for node in existing_doc.get("content", []):
            if node.get("type") == "video":
                return deepcopy(node)
        media_upload_id = draft.get("draft_video_upload_id") or draft.get("video_upload_id")
        if media_upload_id:
            return {"type": "video", "attrs": {"mediaUploadId": media_upload_id, "duration": None}}
        return None

    def markdown_to_doc(self, markdown_path: Path, video_node: dict | None) -> tuple[str, str]:
        text = markdown_path.read_text()
        lines = text.splitlines()
        if not lines or not lines[0].startswith("# "):
            raise ValueError(f"Expected H1 title in {markdown_path}")
        title = lines[0][2:].strip()
        content: list[dict] = []

        body = "\n".join(lines[1:])
        tokens = MD.parse(body)

        idx = 0
        while idx < len(tokens):
            token = tokens[idx]
            if token.type == "hr":
                idx += 1
                continue
            if token.type == "heading_open":
                inline = tokens[idx + 1]
                level = int(token.tag[1])
                text_content = inline.content.strip()
                if level == 4 and text_content.lower() == "video tl;dr":
                    content.append(heading_node(markdown_path, text_content, 4))
                    if video_node is None:
                        raise ValueError(
                            "Markdown requests a Video TL;DR block but the draft has no uploaded video."
                        )
                    content.append(deepcopy(video_node))
                    idx += 3
                    if idx + 2 < len(tokens) and tokens[idx].type == "paragraph_open":
                        paragraph_inline = tokens[idx + 1]
                        children = paragraph_inline.children or []
                        if (
                            len(children) == 3
                            and children[0].type == "link_open"
                            and children[1].type == "text"
                            and children[2].type == "link_close"
                            and (children[0].attrGet("href") or "").endswith(".mp4")
                        ):
                            idx += 3
                    continue
                if level == 1:
                    idx += 3
                    continue
                content.append(heading_node(markdown_path, text_content, level))
                idx += 3
                continue

            if token.type == "paragraph_open":
                inline = tokens[idx + 1]
                children = inline.children or []
                if len(children) == 1 and children[0].type == "image":
                    child = children[0]
                    src = child.attrGet("src") or ""
                    alt = child.content or child.attrGet("alt") or ""
                    image_path = (markdown_path.parent / unquote(src)).resolve()
                    content.append(self.upload_image(image_path, alt))
                else:
                    node = paragraph_node(markdown_path, inline.content)
                    if node.get("content"):
                        content.append(node)
                idx += 3
                continue

            if token.type == "fence":
                content.append(
                    {
                        "type": "code_block",
                        "attrs": {"language": token.info.strip() or None},
                        "content": [{"type": "text", "text": token.content.rstrip("\n")}],
                    }
                )
                idx += 1
                continue

            idx += 1

        doc = {"type": "doc", "content": content}
        return title, json.dumps(doc, ensure_ascii=False)

    def sync_post(self, config: SyncConfig) -> dict:
        draft = run_with_retry(self.api.get_draft, config.post_id)
        body = draft.get("draft_body") or draft.get("body")
        existing_doc = json.loads(body) if isinstance(body, str) else body
        video_node = self.video_node_from_draft(draft, existing_doc)
        title, body_json = self.markdown_to_doc(config.markdown_path, video_node)
        put_kwargs = {
            "draft_title": title,
            "draft_body": body_json,
        }
        if draft.get("draft_video_upload_id") is not None:
            put_kwargs["draft_video_upload_id"] = draft["draft_video_upload_id"]
        updated = run_with_retry(self.api.put_draft, config.post_id, **put_kwargs)
        if config.publish:
            run_with_retry(
                self.api.publish_draft,
                config.post_id,
                send=False,
                share_automatically=False,
            )
        return updated


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sync a local markdown essay into an existing Substack draft, upload local images, "
            "and optionally preserve or inject the draft's uploaded video block."
        )
    )
    parser.add_argument("--publication-url", required=True)
    parser.add_argument("--post-id", required=True, type=int)
    parser.add_argument("--markdown", required=True, type=Path)
    parser.add_argument("--cookie-path", type=Path, default=DEFAULT_COOKIE_PATH)
    parser.add_argument(
        "--chrome-debug-url",
        help="Reuse an already logged-in Chrome session over CDP, for example http://127.0.0.1:9222.",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish the updated draft after syncing. Default behavior only updates the draft.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cookie_string = load_cookie_string(args.cookie_path, args.chrome_debug_url)
    api = substack.Api(cookies_string=cookie_string, publication_url=args.publication_url)
    sync = MarkdownPostSync(api, args.publication_url)
    updated = sync.sync_post(
        SyncConfig(
            publication_url=args.publication_url,
            post_id=args.post_id,
            markdown_path=args.markdown.resolve(),
            publish=args.publish,
        )
    )
    print(
        json.dumps(
            {
                "post_id": args.post_id,
                "title": updated.get("draft_title"),
                "published": bool(args.publish),
                "markdown": str(args.markdown.resolve()),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
