#!/usr/bin/env python3
"""word-template-gen — generador de plantillas Word y render PDF desde Markdown.

Un TEMA (themes/<name>.json) es la fuente única de verdad del diseño: fuentes,
paleta y tamaños. De él se derivan a la vez:
  - el CSS que se inyecta en el HTML (y por tanto en el PDF), y
  - la plantilla de referencia .docx de Word (vía python-docx).
Así, el mismo estilo del PDF es el que se incorpora al Word.

Usos:
  python wtg.py list
  python wtg.py template --theme <name> [--out salida.docx]                 # Uso 1
  python wtg.py render --md doc.md --theme <name> [--to pdf,docx,html] [--out DIR]  # Uso 2

Requiere: pandoc, python-docx y Chrome/Edge (solo para PDF).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.style import WD_STYLE_TYPE

SKILL_DIR = Path(__file__).resolve().parent
THEMES_DIR = SKILL_DIR / "themes"
PANDOC = "pandoc"


def _tmp(suffix):
    """Fichero temporal con el descriptor CERRADO (Windows no deja borrar si sigue abierto)."""
    fd, p = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return Path(p)

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


# ---------- temas ----------

def list_theme_names():
    return sorted(p.stem for p in THEMES_DIR.glob("*.json"))


def load_theme(name):
    f = THEMES_DIR / f"{name}.json"
    if not f.exists():
        sys.exit(f"Tema desconocido: {name!r}. Disponibles: {', '.join(list_theme_names())}")
    return json.loads(f.read_text(encoding="utf-8"))


def hex_rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# ---------- CSS (HTML/PDF) ----------

def css_for(t):
    p, s = t["palette"], t["sizes"]
    extra = p.get("extra", p["accent"])
    rule = p.get("rule", "#dddddd")
    bg = p.get("bg", "#ffffff")
    return f"""
@page {{ size: A4; margin: {t['page_margin_cm']}cm; }}
:root {{
  --ink:{p['ink']}; --accent:{p['accent']}; --muted:{p['muted']};
  --extra:{extra}; --rule:{rule}; --bg:{bg};
}}
body {{
  font-family: {t['css_body_stack']};
  font-size: {s['body']}pt; line-height: {t['line_spacing']};
  color: var(--ink); background: var(--bg);
  max-width: 40em; margin: 0 auto; padding: 2em 1.4em 4em;
  text-rendering: optimizeLegibility;
}}
h1, h2, h3, .title, .subtitle {{ font-family: {t['css_head_stack']}; line-height: 1.25; }}
.title {{ font-size: {s['title']}pt; font-weight: 700; color: var(--ink); margin: 0 0 .1em; }}
.subtitle {{ font-size: {s['subtitle']}pt; color: var(--accent); margin: 0 0 1.5em; font-weight: 600; }}
h1 {{ font-size: {s['h1']}pt; color: var(--ink); margin: 1.2em 0 .5em; }}
h2 {{ font-size: {s['h2']}pt; color: var(--accent); margin: 1.8em 0 .4em;
      padding-bottom: .2em; border-bottom: 1px solid var(--rule); }}
h3 {{ font-size: {s['h3']}pt; color: var(--muted); margin: 1.4em 0 .3em; }}
p {{ margin: 0 0 1em; }}
blockquote {{ margin: 1.1em 0; padding: .2em 0 .2em 1.1em; border-left: 3px solid var(--accent);
              color: var(--muted); font-style: italic; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
hr {{ border: 0; border-top: 1px solid var(--rule); margin: 2em 0; }}
table {{ border-collapse: collapse; width: 100%; margin: 1.2em 0; font-size: .95em; }}
th, td {{ border: 1px solid var(--rule); padding: 6px 10px; text-align: left; vertical-align: top; }}
th {{ background: var(--rule); }}
table, tr, td, th {{ page-break-inside: avoid; }}
code, pre {{ font-family: Consolas, "Courier New", monospace; font-size: .92em; }}
pre {{ background: #f3f1ec; padding: .8em 1em; border-radius: 4px; overflow-x: auto; }}
ul, ol {{ margin: 0 0 1em; padding-left: 1.4em; }}
.Resaltado, .resaltado {{ color: var(--extra); }}
h2, h3 {{ page-break-after: avoid; }}
"""


def write_header(t, path):
    path.write_text(f'<meta charset="utf-8">\n<style>{css_for(t)}</style>\n', encoding="utf-8")


# ---------- plantilla Word ----------

def _setf(style, *, font=None, size=None, color=None, bold=None, italic=None):
    f = style.font
    if font is not None:
        f.name = font
    if size is not None:
        f.size = Pt(size)
    if color is not None:
        f.color.rgb = color
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic


def make_word_template(t, out_path):
    out_path = Path(out_path)
    raw = subprocess.run([PANDOC, "--print-default-data-file", "reference.docx"],
                         capture_output=True, check=True).stdout
    tmp = _tmp(".docx")
    tmp.write_bytes(raw)

    doc = Document(str(tmp))
    S = doc.styles
    names = {s.name for s in S}
    body, head = t["body_font"], t["head_font"]
    s = t["sizes"]
    ink = hex_rgb(t["palette"]["ink"])
    accent = hex_rgb(t["palette"]["accent"])
    muted = hex_rgb(t["palette"]["muted"])
    extra = hex_rgb(t["palette"].get("extra", t["palette"]["accent"]))

    _setf(S["Normal"], font=body, size=s["body"], color=ink)
    S["Normal"].paragraph_format.line_spacing = t["line_spacing"]
    S["Normal"].paragraph_format.space_after = Pt(8)
    if "Body Text" in names:
        _setf(S["Body Text"], font=body, size=s["body"], color=ink)

    _setf(S["Title"], font=head, size=s["title"], color=ink, bold=True)
    _setf(S["Subtitle"], font=head, size=s["subtitle"], color=accent, bold=False, italic=False)
    if "Author" in names:
        _setf(S["Author"], font=head, size=s["body"], color=muted)
    if "Date" in names:
        _setf(S["Date"], font=head, size=s["body"], color=muted)

    _setf(S["Heading 1"], font=head, size=s["h1"], color=ink, bold=True)
    S["Heading 1"].paragraph_format.space_before = Pt(18)
    _setf(S["Heading 2"], font=head, size=s["h2"], color=accent, bold=True)
    S["Heading 2"].paragraph_format.space_before = Pt(14)
    _setf(S["Heading 3"], font=head, size=s["h3"], color=muted, bold=True)

    if "Block Text" in names:
        bt = S["Block Text"]
        _setf(bt, font=body, size=s["body"], color=muted, italic=True)
        bt.paragraph_format.left_indent = Inches(0.4)

    if "Resaltado" not in names:
        rs = S.add_style("Resaltado", WD_STYLE_TYPE.CHARACTER)
    else:
        rs = S["Resaltado"]
    _setf(rs, font=body, color=extra, italic=False)

    # Margenes de pagina
    cm = t.get("page_margin_cm", 2.0)
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Cm(cm)
        sec.left_margin = sec.right_margin = Cm(cm)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    tmp.unlink(missing_ok=True)
    return out_path


# ---------- render ----------

def find_chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    return None


def render(md, theme_name, targets, outdir):
    t = load_theme(theme_name)
    md = Path(md).resolve()
    if not md.exists():
        sys.exit(f"No existe el Markdown: {md}")
    outdir = Path(outdir).resolve() if outdir else md.parent
    outdir.mkdir(parents=True, exist_ok=True)
    stem = md.stem
    produced = []

    need_html = "html" in targets or "pdf" in targets
    html_path = outdir / f"{stem}.html"
    if need_html:
        hdr = _tmp(".html")
        write_header(t, hdr)
        subprocess.run([PANDOC, str(md), "--standalone", "-H", str(hdr),
                        "-V", f"pagetitle={stem}", "-M", "lang=es",
                        "-o", str(html_path)], check=True)
        hdr.unlink(missing_ok=True)
        if "html" in targets:
            produced.append(html_path)

    if "pdf" in targets:
        chrome = find_chrome()
        if not chrome:
            sys.exit("No se encontró Chrome/Edge para generar el PDF.")
        pdf_path = outdir / f"{stem}.pdf"
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-margins",
                        f"--print-to-pdf={pdf_path}", str(html_path)],
                       check=True, capture_output=True)
        produced.append(pdf_path)
        if "html" not in targets:
            html_path.unlink(missing_ok=True)

    if "docx" in targets:
        tpl = _tmp(".docx")
        make_word_template(t, tpl)
        docx_path = outdir / f"{stem}.docx"
        subprocess.run([PANDOC, str(md), "--reference-doc", str(tpl),
                        "-M", "lang=es", "-o", str(docx_path)], check=True)
        tpl.unlink(missing_ok=True)
        produced.append(docx_path)

    return produced


# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser(prog="wtg", description="Generador de plantillas Word / render PDF desde Markdown por tema.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="Lista los temas del catálogo.")

    pt = sub.add_parser("template", help="Uso 1: genera una plantilla Word (.docx) de un tema.")
    pt.add_argument("--theme", required=True)
    pt.add_argument("--out", default=None)

    pr = sub.add_parser("render", help="Uso 2: renderiza un Markdown a PDF/HTML/Word con un tema.")
    pr.add_argument("--md", required=True)
    pr.add_argument("--theme", required=True)
    pr.add_argument("--to", default="pdf", help="pdf,docx,html (lista separada por comas)")
    pr.add_argument("--out", default=None, help="directorio de salida (por defecto, el del .md)")

    a = ap.parse_args()

    if a.cmd == "list":
        print("Temas disponibles:")
        for n in list_theme_names():
            print(f"  - {n}: {load_theme(n).get('label','')}")
    elif a.cmd == "template":
        out = a.out or f"{a.theme}.docx"
        p = make_word_template(load_theme(a.theme), out)
        print(f"OK plantilla Word -> {p}")
    elif a.cmd == "render":
        targets = [x.strip() for x in a.to.split(",") if x.strip()]
        bad = [x for x in targets if x not in ("pdf", "docx", "html")]
        if bad:
            sys.exit(f"Formatos no válidos: {bad}. Usa pdf,docx,html.")
        for p in render(a.md, a.theme, targets, a.out):
            print(f"OK -> {p}")


if __name__ == "__main__":
    main()
