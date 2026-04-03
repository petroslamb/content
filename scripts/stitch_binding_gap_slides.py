from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE = Path(
    "../publications/binding-gap/essays/the-binding-gap/artifacts/slides"
)
PRESENTER = BASE / "The_Binding_Gap_presenter"
DETAILED = BASE / "The_Binding_Gap_detailed"
STITCHED = BASE / "stitched"

MAPPING = [
    ("01_binding-gap-thesis", "slide-001.png", "slide-001.png"),
    ("02_relation-reversal-anomaly", "slide-002.png", "slide-002.png"),
    ("03_defining-the-binding-gap", "slide-003.png", "slide-003.png"),
    ("04_neighboring-failures-diagnostic-matrix", "slide-004.png", "slide-008.png"),
    ("05_binding-as-manipulable-circuitry", "slide-005.png", "slide-004.png"),
    ("06_fragility-of-thematic-roles", "slide-006.png", "slide-005.png"),
    ("07_meta-analysis-load-collapse", "slide-007.png", "slide-007.png"),
    ("08_mirage-of-surface-correctness", "slide-008.png", "slide-009.png"),
    ("09_attachment-first-architecture", "slide-009.png", "slide-010.png"),
    ("10_architectural-pressures-and-binding-wager", "slide-010.png", "slide-006.png"),
]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def ensure_semantic_copies() -> None:
    for name, presenter_src, detailed_src in MAPPING:
        presenter_in = PRESENTER / presenter_src
        detailed_in = DETAILED / detailed_src
        presenter_out = PRESENTER / f"{name}.png"
        detailed_out = DETAILED / f"{name}.png"

        if presenter_in.exists() and not presenter_out.exists():
            presenter_out.write_bytes(presenter_in.read_bytes())
        if detailed_in.exists() and not detailed_out.exists():
            detailed_out.write_bytes(detailed_in.read_bytes())

    for folder in [PRESENTER, DETAILED]:
        for path in folder.glob("slide-*.png"):
            path.unlink()


def stitch_pairs() -> None:
    STITCHED.mkdir(exist_ok=True)
    font = load_font(40)

    for name, _, _ in MAPPING:
        left = Image.open(PRESENTER / f"{name}.png").convert("RGB")
        right = Image.open(DETAILED / f"{name}.png").convert("RGB")

        if left.height != right.height:
            target = max(left.height, right.height)
            left = left.resize(
                (round(left.width * target / left.height), target), Image.LANCZOS
            )
            right = right.resize(
                (round(right.width * target / right.height), target), Image.LANCZOS
            )

        gap = 40
        header = 88
        canvas = Image.new(
            "RGB",
            (left.width + right.width + gap, header + max(left.height, right.height)),
            "white",
        )
        draw = ImageDraw.Draw(canvas)
        draw.rectangle((0, 0, canvas.width, header), fill=(245, 245, 245))

        canvas.paste(left, (0, header))
        canvas.paste(right, (left.width + gap, header))

        left_label = "Presenter: The LLM Binding Gap"
        right_label = "Detailed: The Binding Gap"
        draw.text((30, 24), left_label, fill="black", font=font)
        right_bbox = draw.textbbox((0, 0), right_label, font=font)
        draw.text(
            (canvas.width - (right_bbox[2] - right_bbox[0]) - 30, 24),
            right_label,
            fill="black",
            font=font,
        )

        out = STITCHED / f"{name}.png"
        canvas.save(out)
        print(out)


if __name__ == "__main__":
    ensure_semantic_copies()
    stitch_pairs()
