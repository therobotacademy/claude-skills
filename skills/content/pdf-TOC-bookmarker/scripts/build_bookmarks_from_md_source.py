"""
Genera bookmarks para un PDF producido por el skill pdf-export (Pipeline A,
Chrome headless + KaTeX) parseando directamente los headings del .md FUENTE,
en vez de adivinarlos a partir del texto ya renderizado del PDF.

Por que este enfoque es mejor que inspeccionar extract_text() a mano:
- La jerarquia (#, ##, ###...) es exacta y completa -- no se pueden "perder"
  subtitulos que el ojo humano pasa por alto en un volcado de texto.
- Funciona para CUALQUIER .md exportado con pdf-export Pipeline A (el que se
  usa cuando el documento tiene formulas LaTeX y por tanto no puede pasar por
  Pipeline B / WeasyPrint, que ya genera bookmarks automaticos desde HTML).
- No hace falta regex de "titulo....numero_de_pagina": el .md no tiene
  paginacion, así que cada heading se localiza en el PDF buscando su texto
  normalizado a partir de la ultima pagina encontrada (los headings aparecen
  en el PDF en el mismo orden que en el .md).

Uso:
    python build_bookmarks_from_md_source.py <fuente.md> <pdf_generado.pdf> [salida.pdf]

Si no se aporta 'salida.pdf', se escribe '<pdf_generado>_bookmarked.pdf'.
"""
import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def parse_md_headings(md_path: Path):
    """Devuelve [(level0based, titulo_limpio), ...] en orden de aparicion.

    level0based: 0 para el heading de nivel minimo presente en el documento
    (normalmente '#' o '##' si el '#' es solo el titulo de portada), y crece
    con cada '#' adicional relativo a ese minimo -- así el outline no queda
    con un nivel superfluo si el .md no usa '#' para secciones reales.
    """
    raw = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        m = HEADING_RE.match(line)
        if not m:
            continue
        hashes, title = m.groups()
        raw.append((len(hashes), clean_title(title)))

    if not raw:
        return []

    min_level = min(lvl for lvl, _ in raw)
    return [(lvl - min_level, title) for lvl, title in raw]


def clean_title(title: str) -> str:
    # quita enfasis markdown, enlaces [texto](url) -> texto, y matematica inline
    title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", title)
    title = re.sub(r"[*_`]", "", title)
    title = re.sub(r"\$[^$]*\$", "", title)
    return title.strip().rstrip(":")


def normalize(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "", s.lower())
    return s


def locate_pages(reader: PdfReader, headings):
    """Empareja cada heading con el indice 0-based de la pagina del PDF donde
    aparece por primera vez, buscando desde la pagina del heading anterior en
    adelante (los headings son monotonos en el orden del documento)."""
    page_texts = [normalize(p.extract_text() or "") for p in reader.pages]
    results = []
    cursor = 0
    for level, title in headings:
        needle = normalize(title)
        # si el titulo es muy largo, basta con las primeras ~8 palabras --
        # el heading puede quedar cortado por saltos de pagina/columna
        if len(needle) > 60:
            short = normalize(" ".join(title.split()[:8]))
        else:
            short = needle

        found_page = None
        for i in range(cursor, len(page_texts)):
            if short and short in page_texts[i]:
                found_page = i
                break

        if found_page is None:
            print(f"  AVISO: no se localizo '{title}' desde pagina {cursor} en adelante")
            found_page = cursor  # fallback: no retroceder el cursor
        else:
            cursor = found_page

        results.append((level, title, found_page))
    return results


def build_outline(pdf_path: Path, dst_path: Path, entries):
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)

    stack = []  # [(level, ref), ...] pila de padres abiertos
    for level, title, page in entries:
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent = stack[-1][1] if stack else None
        ref = writer.add_outline_item(title, page, parent=parent)
        stack.append((level, ref))

    with open(dst_path, "wb") as f:
        writer.write(f)


def count_nodes(nodes):
    n = 0
    for item in nodes:
        n += count_nodes(item) if isinstance(item, list) else 1
    return n


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    md_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2])
    dst_path = Path(sys.argv[3]) if len(sys.argv) > 3 else pdf_path.with_name(
        pdf_path.stem + "_bookmarked.pdf"
    )

    headings = parse_md_headings(md_path)
    print(f"Headings en {md_path.name}: {len(headings)}")

    reader = PdfReader(str(pdf_path))
    if reader.outline:
        print("AVISO: el PDF ya tiene outline -- este script lo va a duplicar/sustituir en la copia de salida.")

    entries = locate_pages(reader, headings)

    build_outline(pdf_path, dst_path, entries)

    check = PdfReader(str(dst_path))
    total = count_nodes(check.outline)
    print(f"Bookmarks escritos: {total} (esperados: {len(entries)})")
    assert total == len(entries), "Descuadre en el numero de nodos del outline"

    print("\nMuestra de verificacion:")
    for level, title, page in entries[:5]:
        text = (check.pages[page].extract_text() or "")[:80].replace("\n", " ")
        print(f"  [{level}] page {page}: {title!r} -> {text!r}")

    print(f"\nOK -> {dst_path}")


if __name__ == "__main__":
    main()
