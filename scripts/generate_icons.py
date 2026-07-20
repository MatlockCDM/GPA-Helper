"""Generate all platform icon formats from one programmatic design."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SIZE = 1024


def rounded_rectangle(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def make_icon():
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    rounded_rectangle(draw, (48, 48, 976, 976), 210, "#172A46")
    rounded_rectangle(draw, (132, 142, 892, 876), 94, "#FFFFFF")

    # Notebook binding and spaced-review markers.
    draw.rounded_rectangle((132, 142, 255, 876), radius=70, fill="#2563EB")
    for y in (292, 456, 620, 784):
        draw.ellipse((202, y - 25, 252, y + 25), fill="#F5B942")
        draw.rounded_rectangle((320, y - 18, 790, y + 18), radius=18, fill="#DCE3EC")
    draw.ellipse((696, 650, 864, 818), fill="#0F9F8F")

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 100)
    except OSError:
        font = ImageFont.load_default()
    draw.text((746, 730), "G", font=font, anchor="mm", fill="white")
    return image


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    icon = make_icon()
    icon.save(ASSETS / "icon.png")
    icon.resize((128, 128), Image.Resampling.LANCZOS).save(ASSETS / "icon-128.png")
    icon.resize((256, 256), Image.Resampling.LANCZOS).save(ASSETS / "icon-256.png")
    icon.save(
        ASSETS / "icon.ico",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    icon.save(ASSETS / "icon.icns")


if __name__ == "__main__":
    main()
