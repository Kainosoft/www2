from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

root = Path(__file__).resolve().parents[1]
width, height = 1200, 630
image = Image.new("RGB", (width, height), "#07172d")
pixels = image.load()
for y in range(height):
    for x in range(width):
        distance = math.hypot(x - 1010, y - 250)
        glow = max(0, 1 - distance / 760) * 30
        pixels[x, y] = (7 + int(glow * .45), 23 + int(glow * .35), 45 + int(glow))

draw = ImageDraw.Draw(image, "RGBA")
gradient = [(44, 227, 232, 210), (65, 133, 255, 210), (140, 85, 255, 210), (236, 61, 183, 210)]
orbits = [(1000, 314, 790, 364, -18, 3), (1000, 314, 644, 516, 34, 3), (1000, 314, 920, 216, 61, 2)]
for cx, cy, ow, oh, rotation, line_width in orbits:
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    orbit = ImageDraw.Draw(layer, "RGBA")
    box = (cx - ow // 2, cy - oh // 2, cx + ow // 2, cy + oh // 2)
    for inset, color in enumerate(gradient):
        orbit.arc(tuple(v + (inset * 2 if i < 2 else -inset * 2) for i, v in enumerate(box)), 0, 90, fill=color, width=line_width)
        orbit.arc(tuple(v + (inset * 2 if i < 2 else -inset * 2) for i, v in enumerate(box)), 90, 180, fill=color, width=line_width)
        orbit.arc(tuple(v + (inset * 2 if i < 2 else -inset * 2) for i, v in enumerate(box)), 180, 270, fill=color, width=line_width)
        orbit.arc(tuple(v + (inset * 2 if i < 2 else -inset * 2) for i, v in enumerate(box)), 270, 360, fill=color, width=line_width)
    layer = layer.rotate(rotation, center=(cx, cy), resample=Image.Resampling.BICUBIC)
    image.paste(layer, (0, 0), layer)

draw = ImageDraw.Draw(image, "RGBA")
draw.ellipse((991, 305, 1009, 323), fill=(97, 217, 242, 255))
logo = Image.open(root / "Kainosoft_Vector_System_v1/kainosoft-logo-horizontal-reversed-transparent.png").convert("RGBA")
logo.thumbnail((418, 99), Image.Resampling.LANCZOS)
image.paste(logo, (92, 115 + (99 - logo.height) // 2), logo)
draw.rounded_rectangle((94, 277, 160, 281), radius=2, fill=(65, 133, 255, 255))
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
medium = ImageFont.truetype(font_path, 35)
small = ImageFont.truetype(font_path, 27)
draw.text((94, 303), "AI-Powered Software Product Company", font=medium, fill="#ffffff")
draw.text((94, 374), "Build Scalable Software Products with AI", font=small, fill="#b9c9df")
image.save(root / "images/og/kainosoft-og.png", format="PNG", optimize=True, compress_level=9)
