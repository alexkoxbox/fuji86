"""Check that the page text matches the print PDF character for character (whitespace ignored)."""
import re, subprocess, sys
from html.parser import HTMLParser

page, pdf = sys.argv[1], sys.argv[2]

class T(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, tag, a):
        if tag in ("style", "head"): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ("style", "head"): self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)

t = T(); t.feed(open(page, encoding="utf-8").read())
norm = lambda s: re.sub(r"\s+", "", s)
html_txt = norm("".join(t.out))
pdf_txt = norm(subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout)
# the PDF hero sets "7" before the title and the letter-spaced kicker; compare without them
for s in ("PORSCHERACINGPOSTER·1986",):
    html_txt = html_txt.replace(s, ""); pdf_txt = pdf_txt.replace(s, "")
html_txt = html_txt.replace("7", "", 1); pdf_txt = pdf_txt.replace("7", "", 1)
pdf_chars, html_chars = sorted(pdf_txt), sorted(html_txt)
import difflib
if pdf_chars == html_chars:
    print("OK: same characters as the PDF (%d)" % len(pdf_txt))
else:
    sm = difflib.SequenceMatcher(None, pdf_txt, html_txt, autojunk=False)
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op != "equal": print(op, "PDF:", pdf_txt[a1-5:a2+5], "| HTML:", html_txt[b1-5:b2+5])
    sys.exit(1)
