"""Generate qr.svg + qr.png (1200 px) for the QR stub URL and verify both decode."""
import subprocess, sys
import qrcode, qrcode.image.svg
from PIL import Image

URL = sys.argv[1] if len(sys.argv) > 1 else "https://alexkoxbox.github.io/posters/fuji86/"

def make():
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=4, box_size=10)
    q.add_data(URL); q.make(fit=True)
    return q

q = make()
modules = q.modules_count + 2 * q.border
q.box_size = 1200 // modules
img = q.make_image(fill_color="black", back_color="white").get_image().convert("L")
img.resize((1200, 1200), Image.NEAREST).save("qr.png", optimize=True)

svg = make().make_image(image_factory=qrcode.image.svg.SvgPathFillImage)
svg.save("qr.svg")
print(f"version {q.version}, {q.modules_count} modules + {q.border}-module quiet zone, level H")

for f in ("qr.png", "qr.svg"):
    path = f
    if f.endswith(".svg"):  # zbar can't read SVG: rasterize through Playwright-free route (cairosvg not needed): use Chromium
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 600, "height": 600})
            pg.goto("file://" + __import__("os").path.abspath(f)); pg.screenshot(path=__import__("tempfile").gettempdir() + "/_qr_svg_check.png"); b.close()
        path = __import__("tempfile").gettempdir() + "/_qr_svg_check.png"
    out = subprocess.run(["zbarimg", "--quiet", "--raw", path], capture_output=True, text=True).stdout.strip()
    assert out == URL, f"{f}: decoded {out!r}"
    print(f"{f}: decodes to {out}")
