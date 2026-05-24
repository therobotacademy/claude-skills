"""
Pipeline: cap*.md → HTML (Pandoc) → PDF (Chrome) → bookmarks (PyMuPDF)
Extra step vs skill: concatena todos los MD en un único documento.
"""
import subprocess, sys, glob, os, re
import fitz  # PyMuPDF

BASE    = r"C:\Users\brjap\Mi unidad\__Active-AGENTS\(claude-skills\skills\content\pdf-export"
CAP_DIR = os.path.join(BASE, "capitulos")
CHROME  = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CSS = """\
body      { font-family: "Georgia", serif; font-size: 12pt; line-height: 1.65;
            max-width: 720px; margin: 40px auto; color: #1c1b19; }
h1        { font-family: "Arial", sans-serif; font-size: 1.55em;
            break-before: page; margin-top: 2em; padding-top: 0.8em;
            border-bottom: 2px solid #7a3b2e; color: #7a3b2e; }
h2        { font-family: "Arial", sans-serif; font-size: 1.15em;
            margin-top: 1.8em; color: #333; }
h3        { font-size: 1em; margin-top: 1.4em; color: #555; }
blockquote{ border-left: 3px solid #bbb; margin-left: 0; padding-left: 1em;
            color: #6b6357; font-style: italic; }
p         { margin: 0.8em 0; }
em        { font-style: italic; }
"""

# ── 1. Archivos en orden ──────────────────────────────────────────────────────
md_files = sorted(glob.glob(os.path.join(CAP_DIR, "cap*.md")))
if not md_files:
    print("ERROR: no se encontraron cap*.md en", CAP_DIR); sys.exit(1)
print(f"Capítulos: {len(md_files)}")

# ── 2. Extraer estructura de headings desde los .md ──────────────────────────
headings = []
for f in md_files:
    with open(f, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^(#{1,3})\s+(.+)$", line.rstrip())
            if m:
                headings.append((len(m.group(1)), m.group(2).strip()))
print(f"Headings extraídos: {len(headings)}")

# ── 3. CSS → archivo temporal ────────────────────────────────────────────────
css_path = os.path.join(CAP_DIR, "_estilo.css")
with open(css_path, "w", encoding="utf-8") as f:
    f.write(CSS)

# ── 4. Pandoc: todos los .md → HTML autocontenido ────────────────────────────
html_path = os.path.join(CAP_DIR, "_combined.html")
cmd = (["pandoc"] + md_files +
       ["--standalone", "--embed-resources",
        f"--css={css_path}",
        "-M", "title=Ética y IA en la Investigación",
        "-M", "author=Bernardo Ronquillo Japón",
        "-M", "date=2026", "-M", "lang=es",
        "-o", html_path])
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("ERROR Pandoc:\n", r.stderr); sys.exit(1)
print("HTML:", html_path)

# ── 5. Chrome headless: HTML → PDF ───────────────────────────────────────────
pdf_path = os.path.join(BASE, "capitulos-completo.pdf")
r = subprocess.run(
    [CHROME, "--headless=new",
     f"--print-to-pdf={os.path.abspath(pdf_path)}",
     "--no-margins",
     os.path.abspath(html_path)],
    capture_output=True, text=True)
if r.returncode != 0:
    print("ERROR Chrome:\n", r.stderr); sys.exit(1)
print("PDF (sin bookmarks):", pdf_path)

# ── 6. PyMuPDF: inyectar bookmarks ───────────────────────────────────────────
doc   = fitz.open(pdf_path)
pages = len(doc)
print(f"Páginas: {pages}")

def make_needle(title: str) -> str:
    """Extrae un fragmento buscable: sin Markdown, sin puntuación especial,
    deteniéndose antes del primer carácter no-ASCII para evitar fallos de
    búsqueda por comillas tipográficas, puntos medios, etc."""
    clean = re.sub(r"[*_`]", "", title).strip()
    # Cortar en el primer carácter que no sea ASCII imprimible
    safe = re.match(r"^[\x20-\x7e]+", clean)
    fragment = safe.group(0).rstrip() if safe else clean
    # Si el fragmento es muy corto (< 4 chars), usar los primeros 20 chars del clean
    if len(fragment) < 4:
        fragment = clean[:20]
    return fragment[:30]

toc, misses = [], []
for level, title in headings:
    needle = make_needle(title)
    found  = None
    for pno in range(pages):
        if doc[pno].search_for(needle, quads=False):
            found = pno + 1; break
    if found:
        toc.append([level, title, found])
    else:
        misses.append(f"{title!r} (needle={needle!r})")

doc.set_toc(toc)
doc.save(pdf_path)
doc.close()

# ── 7. Limpieza de temporales ────────────────────────────────────────────────
os.remove(html_path)
os.remove(css_path)

# ── Informe ───────────────────────────────────────────────────────────────────
size_kb = os.path.getsize(pdf_path) / 1024
print(f"\n✅ {pdf_path}")
print(f"   Tamaño : {size_kb:.0f} KB")
print(f"   Páginas: {pages}")
print(f"   Bookmarks insertados: {len(toc)}/{len(headings)}")
if misses:
    print("   ⚠ No encontrados:", misses)
