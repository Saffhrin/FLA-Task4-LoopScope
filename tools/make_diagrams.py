"""Create PNG previews for the three LoopScope theory diagrams.

The editable Graphviz sources live beside the committed SVG and PNG versions.
Install Pillow only if you want to rebuild the PNG previews.
"""

from math import atan2, cos, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "diagrams"
COLORS = {
    "ink": "#172033",
    "blue": "#2563eb",
    "blue_bg": "#eff6ff",
    "green": "#16a34a",
    "green_bg": "#dcfce7",
    "amber": "#d97706",
    "amber_bg": "#fef3c7",
    "red": "#dc2626",
    "red_bg": "#fee2e2",
    "line": "#475569",
    "muted": "#334155",
    "white": "#ffffff",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    candidates = (Path("C:/Windows/Fonts") / filename, Path("C:/Windows/Fonts/arial.ttf"))
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


def canvas(size: tuple[int, int], title: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", size, COLORS["white"])
    draw = ImageDraw.Draw(image)
    draw.text((size[0] // 2, 42), title, anchor="mt", font=font(34, True), fill=COLORS["ink"])
    return image, draw


def box(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], text: str,
        fill: str, outline: str, size: int = 24, radius: int = 24, width: int = 4) -> None:
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=width)
    x = (rect[0] + rect[2]) // 2
    y = (rect[1] + rect[3]) // 2
    draw.multiline_text((x, y), text, anchor="mm", align="center", spacing=8,
                        font=font(size), fill=COLORS["ink"])


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int],
          label: str | None = None, label_at: tuple[int, int] | None = None) -> None:
    draw.line((start, end), fill=COLORS["line"], width=4)
    angle = atan2(end[1] - start[1], end[0] - start[0])
    length, half = 18, 10
    base = (end[0] - length * cos(angle), end[1] - length * sin(angle))
    left = (base[0] + half * sin(angle), base[1] - half * cos(angle))
    right = (base[0] - half * sin(angle), base[1] + half * cos(angle))
    draw.polygon((end, left, right), fill=COLORS["line"])
    if label and label_at:
        draw.text(label_at, label, anchor="mm", font=font(18, True), fill=COLORS["muted"])


def save(image: Image.Image, name: str) -> None:
    image.save(OUT / f"{name}.png", optimize=True)


def problem_mapping() -> None:
    image, draw = canvas((1500, 920), "From software behavior to the halting problem")
    box(draw, (410, 120, 1090, 245), "REAL-WORLD QUESTION\nWill program P stop on input w?", COLORS["blue_bg"], COLORS["blue"], 27)
    box(draw, (410, 320, 1090, 445), "FORMAL ENCODING\nTuring machine M + input w", COLORS["blue_bg"], COLORS["blue"], 27)
    arrow(draw, (750, 245), (750, 310), "encode", (820, 276))
    box(draw, (390, 530, 1110, 650), "HALT_TM membership: does M halt on w?\nRecognizable by simulation, but undecidable", COLORS["amber_bg"], COLORS["amber"], 24)
    arrow(draw, (750, 445), (750, 520), "ask membership", (850, 480))
    box(draw, (85, 735, 660, 850), "TIMEOUT\nNo proof: the run may halt later", COLORS["red_bg"], COLORS["red"], 23)
    box(draw, (840, 735, 1415, 850), "RESTRICTED MODEL\nProof-backed result or UNKNOWN", COLORS["green_bg"], COLORS["green"], 23)
    arrow(draw, (570, 650), (400, 725), "finite wait", (470, 685))
    arrow(draw, (930, 650), (1100, 725), "analyzable subset", (1040, 685))
    save(image, "problem_mapping")


def decidability_classes() -> None:
    image, draw = canvas((1500, 920), "Where the halting problem sits")
    draw.rounded_rectangle((55, 115, 1445, 860), radius=34, fill=COLORS["white"], outline="#94a3b8", width=5)
    draw.text((750, 145), "ALL LANGUAGES", anchor="mt", font=font(24, True), fill=COLORS["muted"])
    draw.rounded_rectangle((465, 205, 1385, 790), radius=30, fill=COLORS["blue_bg"], outline=COLORS["blue"], width=5)
    draw.text((925, 225), "TURING-RECOGNIZABLE (RE)", anchor="mt", font=font(25, True), fill="#1e3a8a")
    box(draw, (535, 320, 890, 650), "DECIDABLE\n\nA decider halts on\nevery input", COLORS["green_bg"], COLORS["green"], 25)
    box(draw, (980, 345, 1315, 625), "HALT_TM\n\nRecognizable by\nsimulation\n\nUndecidable", COLORS["amber_bg"], COLORS["amber"], 25)
    box(draw, (100, 350, 390, 625), "LOOP_TM\n\nComplement of HALT_TM\n\nNot recognizable", COLORS["red_bg"], COLORS["red"], 23)
    draw.text((750, 820), "Every decidable language is recognizable. HALT_TM is recognizable but not decidable.",
              anchor="mm", font=font(20), fill=COLORS["ink"])
    save(image, "decidability_classes")


def pipeline() -> None:
    image, draw = canvas((1500, 970), "LoopScope analysis pipeline")
    box(draw, (470, 120, 1030, 235), "PROGRAM SOURCE + INTEGER MODEL", COLORS["blue_bg"], COLORS["blue"], 25)
    box(draw, (390, 320, 1110, 445), "CHECK RESTRICTED GRAMMAR\none variable · one guard · one constant update", "#f8fafc", COLORS["line"], 24)
    arrow(draw, (750, 235), (750, 310))
    box(draw, (55, 610, 465, 755), "UNKNOWN\nUnsupported source form", COLORS["red_bg"], COLORS["red"], 24)
    box(draw, (545, 610, 955, 755), "UNBOUNDED INTEGER PROOF\nHALTS or LOOPS", COLORS["green_bg"], COLORS["green"], 22)
    box(draw, (1035, 610, 1445, 755), "FINITE-WIDTH MODEL\nHALTS or repeated-state LOOPS", COLORS["amber_bg"], COLORS["amber"], 22)
    arrow(draw, (510, 445), (260, 600), "no match", (345, 505))
    arrow(draw, (750, 445), (750, 600), "match", (790, 520))
    arrow(draw, (990, 445), (1240, 600), "separate semantics", (1150, 505))
    box(draw, (355, 830, 1145, 910), "Each verdict names the model and the evidence supporting it", "#e0e7ff", COLORS["blue"], 22)
    arrow(draw, (260, 755), (500, 820))
    arrow(draw, (750, 755), (750, 820))
    arrow(draw, (1240, 755), (1000, 820))
    save(image, "loopscope_pipeline")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    problem_mapping()
    decidability_classes()
    pipeline()
    print("Created three PNG diagram previews in docs/diagrams/")


if __name__ == "__main__":
    main()
