#!/usr/bin/env python3
"""Export slide PDFs into zero-padded PNG folders."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_TOOLS = ("pdfinfo", "pdftocairo", "sips")


@dataclass
class ExportReport:
    pdf: Path
    output_dir: Path
    page_count: int
    png_count: int
    sample_dimensions: str
    failed_pages: list[int]

    @property
    def ok(self) -> bool:
        return not self.failed_pages and self.png_count == self.page_count


def run_command(args: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=False,
        text=True,
        capture_output=capture_output,
    )


def require_tools() -> None:
    missing = [tool for tool in REQUIRED_TOOLS if shutil.which(tool) is None]
    if missing:
        raise RuntimeError(f"Missing required tool(s): {', '.join(missing)}")


def discover_pdfs(input_path: Path) -> list[Path]:
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            raise ValueError(f"Input file is not a PDF: {input_path}")
        return [input_path.resolve()]

    pdfs = sorted(
        path.resolve()
        for path in input_path.iterdir()
        if path.is_file() and path.suffix.lower() == ".pdf"
    )
    if not pdfs:
        raise ValueError(f"No PDF files found in directory: {input_path}")
    return pdfs


def get_page_count(pdf_path: Path) -> int:
    result = run_command(["pdfinfo", str(pdf_path)], capture_output=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        raise RuntimeError(f"pdfinfo failed for {pdf_path}: {stderr}")

    match = re.search(r"^Pages:\s+(\d+)$", result.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Could not determine page count for {pdf_path}")
    return int(match.group(1))


def get_output_dir(pdf_path: Path, output_root: Path | None) -> Path:
    parent = output_root.resolve() if output_root else pdf_path.parent
    return parent / pdf_path.stem


def export_pdf(pdf_path: Path, output_dir: Path, page_count: int, dpi: int) -> list[int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    padding = max(3, len(str(page_count)))
    failed_pages: list[int] = []

    for page_number in range(1, page_count + 1):
        stem = output_dir / f"slide-{page_number:0{padding}d}"
        result = run_command(
            [
                "pdftocairo",
                "-png",
                "-singlefile",
                "-r",
                str(dpi),
                "-f",
                str(page_number),
                "-l",
                str(page_number),
                str(pdf_path),
                str(stem),
            ]
        )
        if result.returncode != 0:
            failed_pages.append(page_number)

    return failed_pages


def get_png_count(output_dir: Path) -> int:
    return sum(1 for path in output_dir.iterdir() if path.is_file() and path.suffix.lower() == ".png")


def get_sample_dimensions(output_dir: Path) -> str:
    first_png = next(
        (
            path
            for path in sorted(output_dir.iterdir())
            if path.is_file() and path.suffix.lower() == ".png"
        ),
        None,
    )
    if first_png is None:
        return "unavailable"

    result = run_command(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(first_png)],
        capture_output=True,
    )
    if result.returncode != 0:
        return "unavailable"

    width_match = re.search(r"pixelWidth:\s+(\d+)", result.stdout)
    height_match = re.search(r"pixelHeight:\s+(\d+)", result.stdout)
    if not width_match or not height_match:
        return "unavailable"
    return f"{width_match.group(1)}x{height_match.group(1)}"


def build_report(pdf_path: Path, output_dir: Path, page_count: int, failed_pages: list[int]) -> ExportReport:
    return ExportReport(
        pdf=pdf_path,
        output_dir=output_dir,
        page_count=page_count,
        png_count=get_png_count(output_dir),
        sample_dimensions=get_sample_dimensions(output_dir),
        failed_pages=failed_pages,
    )


def print_report(report: ExportReport) -> None:
    status = "OK" if report.ok else "ERROR"
    print(f"[{status}] {report.pdf}")
    print(f"  output_dir: {report.output_dir}")
    print(f"  pages: {report.page_count}")
    print(f"  png_count: {report.png_count}")
    print(f"  sample_dimensions: {report.sample_dimensions}")
    if report.failed_pages:
        failed = ", ".join(str(page) for page in report.failed_pages)
        print(f"  failed_pages: {failed}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export one PDF or a directory of PDFs into zero-padded PNG folders.",
    )
    parser.add_argument("input_path", help="Path to a PDF or a directory containing PDFs")
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Rasterization DPI for pdftocairo (default: 300)",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        help="Optional root directory for generated per-PDF folders",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        require_tools()
        pdfs = discover_pdfs(Path(args.input_path).expanduser())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    reports: list[ExportReport] = []
    for pdf_path in pdfs:
        try:
            page_count = get_page_count(pdf_path)
            output_dir = get_output_dir(pdf_path, args.output_root)
            failed_pages = export_pdf(pdf_path, output_dir, page_count, args.dpi)
            reports.append(build_report(pdf_path, output_dir, page_count, failed_pages))
        except Exception as exc:
            print(f"[ERROR] {pdf_path}", file=sys.stderr)
            print(f"  reason: {exc}", file=sys.stderr)
            return 1

    for report in reports:
        print_report(report)

    return 0 if all(report.ok for report in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
