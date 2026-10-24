"""Render JPGs for konbini photo / sticker printing (300 dpi) into konbini/."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
MM = 96 / 25.4                      # CSS px per mm
DPR = 300 / 96                      # 300 dpi
JOBS = {"qr_card_L": (89, 127, "fuji86_L.jpg"), "qr_sticker": (80, 80, "fuji86_sticker.jpg")}

(ROOT / "konbini").mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, (w, h, out) in JOBS.items():
        pg = b.new_page(viewport={"width": round(w * MM), "height": round(h * MM)}, device_scale_factor=DPR)
        pg.goto((ROOT / "print" / f"{name}.html").as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(ROOT / "konbini" / out), type="jpeg", quality=95)
        print(out)
    b.close()
