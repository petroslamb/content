from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Callable, Iterable, TypeVar
from urllib.parse import quote, unquote

from markdown_it import MarkdownIt
from markdown_it.token import Token
from PIL import Image
import substack
from substack.exceptions import SubstackAPIException


REPO_ROOT = Path(__file__).resolve().parents[1]
GITHUB_BLOB_ROOT = "https://github.com/petroslamb/content/blob/main"
COOKIE_PATH = Path("/tmp/substack_cookie_string.txt")
PUBLICATION_URL = "https://lambpetros.substack.com"
T = TypeVar("T")


@dataclass(frozen=True)
class PostSpec:
    slug: str
    markdown_path: Path


POST_SPECS = [
    PostSpec(
        slug="operating-agents-preface-a-field",
        markdown_path=REPO_ROOT
        / "autonomous-agent-blueprint/essays/launch-note/preface.md",
    ),
    PostSpec(
        slug="operating-agents-i-when-language",
        markdown_path=REPO_ROOT
        / "autonomous-agent-blueprint/essays/action/01-action-tool-use.md",
    ),
    PostSpec(
        slug="operating-agents-ii-memory-needs",
        markdown_path=REPO_ROOT
        / "autonomous-agent-blueprint/essays/memory/02-memory-systems-and-authority.md",
    ),
    PostSpec(
        slug="operating-agents-iii-diagnose-the",
        markdown_path=REPO_ROOT
        / "autonomous-agent-blueprint/essays/reasoning/03-reasoning-scaffolds-and-planning.md",
    ),
    PostSpec(
        slug="operating-agents-iv-the-second-agent",
        markdown_path=REPO_ROOT
        / "autonomous-agent-blueprint/essays/multi-agent/04-multi-agent-boundaries-and-handoffs.md",
    ),
    PostSpec(
        slug="operating-agents-v-the-attack-surface",
        markdown_path=REPO_ROOT
        / "autonomous-agent-blueprint/essays/safety/05-trust-boundaries-and-agent-safety.md",
    ),
    PostSpec(
        slug="operating-agents-bonus-the-workflow",
        markdown_path=REPO_ROOT
        / "autonomous-agent-blueprint/essays/optimization/06-workflow-optimization-and-evaluation.md",
    ),
]

PUBLISHED_MARKDOWN_TO_SUBSTACK_URL = {
    spec.markdown_path.resolve(): f"{PUBLICATION_URL}/p/{spec.slug}" for spec in POST_SPECS
}


MD = MarkdownIt()
INLINE_MD = MarkdownIt("commonmark")


def normalize_path_target(markdown_path: Path, target: str) -> str:
    if re.match(r"^[a-z]+://", target):
        return target
    resolved = (markdown_path.parent / unquote(target)).resolve()
    published_url = PUBLISHED_MARKDOWN_TO_SUBSTACK_URL.get(resolved)
    if published_url is not None:
        return published_url
    rel = resolved.relative_to(REPO_ROOT).as_posix()
    return f"{GITHUB_BLOB_ROOT}/{quote(rel)}"


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
            node["marks"] = [m.copy() for m in mark_stack]
        output.append(node)

    for tok in children:
        if tok.type == "text":
            append_text(tok.content)
        elif tok.type == "softbreak":
            append_text("\n")
        elif tok.type == "code_inline":
            output.append({"type": "text", "text": tok.content, "marks": [{"type": "code"}]})
        elif tok.type == "em_open":
            mark_stack.append({"type": "em"})
        elif tok.type == "em_close":
            if mark_stack:
                mark_stack.pop()
        elif tok.type == "strong_open":
            mark_stack.append({"type": "strong"})
        elif tok.type == "strong_close":
            if mark_stack:
                mark_stack.pop()
        elif tok.type == "link_open":
            href = normalize_path_target(markdown_path, tok.attrGet("href") or "")
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
        elif tok.type == "link_close":
            if mark_stack:
                mark_stack.pop()
        elif tok.type == "image":
            # Standalone markdown images are handled at block level.
            append_text(tok.content or tok.attrGet("alt") or "")

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


class SubstackSync:
    def __init__(self, api: substack.Api):
        self.api = api
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
            tmp_bytes = buffer.getvalue()

        tmp_path = image_path.with_suffix(".codex-upload.jpg")
        tmp_path.write_bytes(tmp_bytes)
        try:
            upload = self.call_with_retry(self.api.get_image, str(tmp_path))
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

    def call_with_retry(self, fn, *args, **kwargs):
        delay = 5
        for attempt in range(6):
            try:
                return fn(*args, **kwargs)
            except SubstackAPIException as exc:
                if "APIError(code=429)" not in str(exc) or attempt == 5:
                    raise
                time.sleep(delay)
                delay *= 2

    def markdown_to_doc(self, markdown_path: Path, existing_video_node: dict | None) -> tuple[str, str]:
        text = markdown_path.read_text()
        lines = text.splitlines()
        if not lines or not lines[0].startswith("# "):
            raise ValueError(f"Expected H1 title in {markdown_path}")
        title = lines[0][2:].strip()
        content: list[dict] = []

        body = "\n".join(lines[1:])
        tokens = MD.parse(body)

        idx = 0
        inserted_video = False
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
                    if existing_video_node is not None:
                        content.append(existing_video_node)
                        inserted_video = True
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
                elif (
                    len(children) == 3
                    and children[0].type == "link_open"
                    and children[1].type == "text"
                    and children[2].type == "link_close"
                    and (children[0].attrGet("href") or "").endswith(".mp4")
                ):
                    pass
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

        if existing_video_node is not None and not inserted_video:
            content.insert(0, existing_video_node)

        doc = {"type": "doc", "content": content}
        return title, json.dumps(doc, ensure_ascii=False)

    def sync_post(self, spec: PostSpec, post_id: int) -> None:
        draft = self.api.get_draft(post_id)
        existing_doc = json.loads(draft["body"])
        existing_video_node = next(
            (node for node in existing_doc.get("content", []) if node.get("type") == "video"),
            None,
        )
        title, body_json = self.markdown_to_doc(spec.markdown_path, existing_video_node)
        self.call_with_retry(
            self.api.put_draft,
            post_id,
            draft_title=title,
            draft_body=body_json,
        )
        self.call_with_retry(
            self.api.publish_draft,
            post_id,
            send=False,
            share_automatically=False,
        )


def load_cookie_string() -> str:
    cookie = COOKIE_PATH.read_text().strip()
    if not cookie:
        raise ValueError(f"Cookie file is empty: {COOKIE_PATH}")
    return cookie


def retry_substack_call(fn: Callable[[], T]) -> T:
    delay = 5
    for attempt in range(6):
        try:
            return fn()
        except SubstackAPIException as exc:
            if "APIError(code=429)" not in str(exc) or attempt == 5:
                raise
            print(f"rate limited by Substack, retrying in {delay}s", flush=True)
            time.sleep(delay)
            delay *= 2


def post_id_by_slug(api: substack.Api) -> dict[str, int]:
    published = retry_substack_call(lambda: api.get_published_posts(limit=50))["posts"]
    return {post["slug"]: post["id"] for post in published}


def main() -> None:
    api = retry_substack_call(
        lambda: substack.Api(
            cookies_string=load_cookie_string(),
            publication_url=PUBLICATION_URL,
        )
    )
    slug_map = post_id_by_slug(api)
    sync = SubstackSync(api)
    for spec in POST_SPECS:
        post_id = slug_map[spec.slug]
        print(f"syncing {spec.slug} -> {post_id}", flush=True)
        sync.sync_post(spec, post_id)


if __name__ == "__main__":
    main()
