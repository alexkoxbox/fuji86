# fuji86 — 1000km FUJI ’86

Japanese story page for the Porsche 956B / taka-Q "1000km FUJI '86" poster, plus the QR that points at it.

- **QR URL (printed, never change):** https://alexkoxbox.github.io/fuji86/
- **Story page:** https://alexkoxbox.github.io/fuji86/story/

The QR points at the site root, which is a stub (`site/index.html`, meta-refresh). To move the story
elsewhere, edit the two URLs in that stub — the printed QR keeps working.
It only stays valid while this repo and its GitHub Pages site exist under the
`alexkoxbox` account (renaming the account or the repo breaks it).

## Layout

| Path | What |
|---|---|
| `source/porsche_956_fuji_1986.pdf` | the print layout — **source of truth** for the text |
| `porsche_956_fuji_1986.md` | the same text extracted from that PDF |
| `site/story/index.html` | the mobile page (same text) |
| `site/story/poster.webp`, `poster.png` | poster image (WebP + PNG fallback) |
| `site/index.html` | site root = QR stub → redirect to the story |
| `.github/workflows/pages.yml` | deploys `site/` to GitHub Pages on push to `main` |
| `qr.svg`, `qr.png` | QR, level H, 4-module quiet zone, PNG 1200 px |
| `print/qr_card.html` → `qr_card.pdf` | A6 card (105×148 mm) |
| `print/qr_card_a4.html` → `qr_card_a4.pdf` | A4 sheet |
| `print/qr_card_L.html`, `print/qr_sticker.html` → `konbini/*.jpg` | konbini prints: L判 photo (89×127) and square sticker, 300 dpi; `konbini/fuji86_A4.pdf` = A4 sheet |
| `tools/` | QR generator, PDF renderer, text check |

## Update the page

```sh
uv venv .venv && uv pip install --python .venv/bin/python "qrcode[pil]" pyzbar playwright pillow
.venv/bin/python -m playwright install chromium     # once; also: brew install zbar poppler

# edit site/story/index.html, then check the text against the print PDF:
.venv/bin/python tools/check_text.py site/story/index.html source/porsche_956_fuji_1986.pdf
git commit -am "..." && git push                    # Pages redeploys in ~1 min
```

Regenerate QR / cards (only needed if the QR URL itself changes — then reprint):

```sh
.venv/bin/python tools/make_qr.py [URL]   # writes qr.svg, qr.png and verifies both decode
.venv/bin/python tools/render_print.py    # writes qr_card.pdf, qr_card_a4.pdf
.venv/bin/python tools/render_konbini.py  # writes konbini/fuji86_L.jpg, fuji86_sticker.jpg (copy qr_card_a4.pdf → konbini/fuji86_A4.pdf)
```

Print the cards at 100 % (no "fit to page"); keep the white margin around the code.

## One-time setup (already done)

```sh
gh repo create alexkoxbox/fuji86 --public --source . --push
gh api -X POST repos/alexkoxbox/fuji86/pages -f build_type=workflow
```
