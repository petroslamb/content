#!/usr/bin/env python3
"""Convert a paper source into repo-standard Markdown.

PDFs use OpenDataLoader PDF first. The output is a single Markdown file with
page separators and image extraction disabled. MarkItDown remains the fallback.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_PAGE_SEPARATOR = "\n\n<!-- page %page-number% -->\n\n"


class ConversionError(RuntimeError):
    """Raised when a converter fails with diagnostic output."""


def sibling_binary(name: str) -> str | None:
    """Resolve a console script next to the active Python, then on PATH."""

    for candidate in (
        Path(sys.executable).with_name(name),
        Path(sys.executable).resolve().with_name(name),
    ):
        if candidate.exists():
            return str(candidate)
    return shutil.which(name)


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True)


def output_excerpt(result: subprocess.CompletedProcess[str], limit: int = 4000) -> str:
    combined = (result.stdout or "") + (result.stderr or "")
    if len(combined) <= limit:
        return combined.strip()
    return combined[-limit:].strip()


def write_atomic(target: Path, content: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=target.parent,
        prefix=f".{target.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        tmp_path = Path(handle.name)
        handle.write(content)
        if content and not content.endswith("\n"):
            handle.write("\n")
    tmp_path.replace(target)


def convert_with_opendataloader(source: Path, target: Path, page_separator: str) -> None:
    binary = sibling_binary("opendataloader-pdf")
    if binary is None:
        raise ConversionError("opendataloader-pdf is not available")

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{target.name}.opendataloader-",
        dir=target.parent,
    ) as tmp_dir:
        command = [
            binary,
            str(source),
            "--format",
            "markdown",
            "--image-output",
            "off",
            "--markdown-page-separator",
            page_separator,
            "--output-dir",
            tmp_dir,
            "--quiet",
        ]
        result = run_command(command)
        if result.returncode != 0:
            raise ConversionError(
                "opendataloader-pdf failed"
                + (f": {output_excerpt(result)}" if output_excerpt(result) else "")
            )

        output_dir = Path(tmp_dir)
        expected_output = output_dir / f"{source.stem}.md"
        markdown_outputs = sorted(output_dir.glob("*.md"))
        generated = expected_output if expected_output.exists() else None
        if generated is None and len(markdown_outputs) == 1:
            generated = markdown_outputs[0]
        if generated is None:
            names = ", ".join(path.name for path in markdown_outputs) or "none"
            raise ConversionError(f"opendataloader-pdf did not create one markdown file; found: {names}")

        markdown = generated.read_text(encoding="utf-8")
        if not markdown.strip():
            raise ConversionError("opendataloader-pdf produced empty markdown")
        write_atomic(target, markdown)


def convert_with_markitdown(source: Path, target: Path) -> None:
    binary = sibling_binary("markitdown")
    if binary is None:
        raise ConversionError("markitdown fallback is not available")

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{target.name}.markitdown-",
        dir=target.parent,
    ) as tmp_dir:
        tmp_target = Path(tmp_dir) / target.name
        result = run_command([binary, str(source), "-o", str(tmp_target)])
        if result.returncode != 0:
            raise ConversionError(
                "markitdown fallback failed"
                + (f": {output_excerpt(result)}" if output_excerpt(result) else "")
            )
        if not tmp_target.exists() or not tmp_target.read_text(encoding="utf-8").strip():
            raise ConversionError("markitdown fallback produced empty markdown")
        tmp_target.replace(target)


def convert(source: Path, target: Path, page_separator: str, no_fallback: bool) -> str:
    if source.suffix.lower() != ".pdf":
        convert_with_markitdown(source, target)
        return "markitdown"

    try:
        convert_with_opendataloader(source, target, page_separator)
        return "opendataloader-pdf"
    except ConversionError as primary_error:
        if no_fallback:
            raise
        print(f"[WARN] {primary_error}; trying markitdown fallback.", file=sys.stderr)
        convert_with_markitdown(source, target)
        return "markitdown"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a paper source to Markdown with OpenDataLoader PDF first and markitdown fallback.",
    )
    parser.add_argument("source_path", help="PDF or source file to convert")
    parser.add_argument("markdown_path", help="Markdown output path")
    parser.add_argument(
        "--page-separator",
        default=DEFAULT_PAGE_SEPARATOR,
        help="OpenDataLoader Markdown page separator. Use %%page-number%% for the page number.",
    )
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Fail instead of falling back to markitdown when OpenDataLoader fails.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    source = Path(args.source_path).expanduser()
    target = Path(args.markdown_path).expanduser()

    if not source.exists():
        print(f"[ERROR] source file does not exist: {source}", file=sys.stderr)
        return 2

    try:
        converter = convert(source, target, args.page_separator, args.no_fallback)
    except ConversionError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 1

    print(f"[OK] converted {source} -> {target} with {converter}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
