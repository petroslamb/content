from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

TIME_RE = re.compile(r"^\d+:\d{2}(?::\d{2})?$")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrape the visible YouTube watch-page transcript panel into a local JSON file."
    )
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the browser headless. Default is headed for reliability.",
    )
    return parser.parse_args()


def scrape(video_id: str, headless: bool) -> list[dict]:
    url = f"https://www.youtube.com/watch?v={video_id}"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        page.evaluate(
            """
            () => {
              const nodes = Array.from(document.querySelectorAll('button, tp-yt-paper-item, a'));
              const trigger = nodes.find((node) => {
                const text = (node.innerText || node.getAttribute('aria-label') || '').trim();
                return /Show transcript|Transcript|Εμφάνιση μεταγραφής|Μεταγραφή/i.test(text);
              });
              if (trigger) trigger.click();
            }
            """
        )
        page.wait_for_timeout(1500)

        transcript_selector = "yt-item-section-renderer #contents"
        page.wait_for_selector(transcript_selector)

        # Scroll the transcript container until the number of timestamped buttons stops growing.
        previous_count = -1
        stable_rounds = 0
        while stable_rounds < 3:
            count = page.evaluate(
                """
                (selector) => {
                  const node = document.querySelector(selector);
                  if (!node) return 0;
                  return (node.innerText || '')
                    .split('\\n')
                    .filter((line) => /^\\d+:\\d{2}(?::\\d{2})?$/.test(line.trim()))
                    .length;
                }
                """,
                transcript_selector,
            )
            if count == previous_count:
                stable_rounds += 1
            else:
                stable_rounds = 0
                previous_count = count
            page.evaluate(
                """
                () => {
                  const container = document.querySelector('ytd-transcript-search-panel-renderer');
                  if (container) container.scrollTop = container.scrollHeight;
                }
                """
            )
            page.wait_for_timeout(600)

        transcript_text = page.locator(transcript_selector).inner_text()
        rows = []
        lines = [line.strip() for line in transcript_text.splitlines() if line.strip()]
        index = 0
        while index < len(lines):
            if not TIME_RE.match(lines[index]):
                index += 1
                continue
            time = lines[index]
            index += 1
            text_lines: list[str] = []
            while index < len(lines) and not TIME_RE.match(lines[index]):
                if not re.search(r"(δευτερόλεπτα|λεπτό|seconds|minute)", lines[index], re.I):
                    text_lines.append(lines[index])
                index += 1
            text = " ".join(text_lines).strip()
            if text:
                rows.append({"time": time, "text": text})
        browser.close()
        return rows


def main():
    args = parse_args()
    rows = scrape(args.video_id, args.headless)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
