"""Render print/*.html to PDF with Chromium (Playwright), same pipeline as the poster PDF."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
with sync_playwright() as p:
    b = p.chromium.launch()
    for name in ("qr_card", "qr_card_a4"):
        pg = b.new_page()
        pg.goto((ROOT / "print" / f"{name}.html").as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(ROOT / f"{name}.pdf"), prefer_css_page_size=True, print_background=True)
        print(f"{name}.pdf")
    b.close()
