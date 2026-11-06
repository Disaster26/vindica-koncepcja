"""Zdjęcia do assets/img: python -I _src/obrazy.py"""
from PIL import Image, ImageEnhance
from pathlib import Path
R = Path(__file__).resolve().parent.parent
O = R / "_src/orig"; A = R / "assets/img"
z = Image.open(O / "zlota7.jpg").convert("RGB")
z = ImageEnhance.Contrast(z).enhance(1.06)
# szeroki (bez szyldów parteru)
z.crop((0, 30, 1920, 880)).save(A / "zlota7-2000.webp", quality=82)
z.crop((0, 30, 1920, 880)).resize((1200, 531)).save(A / "zlota7-1200.webp", quality=80)
# pion: wykusze
z.crop((520, 100, 1420, 860)).resize((900, 760)).save(A / "zlota7-tel.webp", quality=80)
# kontakt: detal wykuszy
z.crop((780, 150, 1260, 760)).save(A / "zlota7-detal.webp", quality=82)
for n in ["09488", "09491", "09505", "09516", "09518", "09524"]:
    Image.open(O / f"k{n}.jpg").convert("RGB").save(A / f"kamienica-{n}.webp", quality=82)
for f in sorted(A.glob("*.webp")):
    print(f.name, Image.open(f).size, f.stat().st_size // 1024, "kB")
