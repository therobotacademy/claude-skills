#!/usr/bin/env python3
"""
concat_md.py — Une varios archivos Markdown en un único fichero.

Paso previo al pipeline de exportación PDF cuando el contenido está
repartido en múltiples .md (capítulos, secciones, módulos...).

USO
----
  # Glob de archivos (se ordenan por nombre)
  python concat_md.py capitulos/cap*.md -o combined.md

  # Directorio completo
  python concat_md.py --dir capitulos/ -o combined.md

  # Con metadatos para el frontmatter YAML
  python concat_md.py cap*.md -o combined.md \\
      --title "Mi Libro" --author "Bernardo Ronquillo" --date "2026"

  # Separador explícito entre capítulos (útil con Chrome/Pipeline A)
  python concat_md.py cap*.md -o combined.md --pagebreaks

SALIDA
------
El .md combinado se pasa directamente a Pandoc (Workflow A o B de pdf-export):

  pandoc combined.md --standalone --embed-resources --css=estilo.css -o out.html
  # luego Chrome o WeasyPrint según el pipeline elegido
"""

import argparse
import glob
import os
import re
import sys

_FRONTMATTER = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", re.DOTALL)
_PAGE_BREAK   = '\n<div style="page-break-after: always;"></div>\n'


def _parse_frontmatter(text: str) -> tuple:
    """Devuelve (dict_meta, cuerpo_sin_frontmatter)."""
    m = _FRONTMATTER.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"\'')
    return meta, text[m.end():]


def _build_frontmatter(title=None, author=None, date=None, lang="es") -> str:
    if not any([title, author, date]):
        return ""
    lines = ["---"]
    if title:  lines.append(f'title: "{title}"')
    if author: lines.append(f'author: "{author}"')
    if date:   lines.append(f'date: "{date}"')
    lines.append(f"lang: {lang}")
    lines.append("---\n")
    return "\n".join(lines)


def _resolve_files(patterns, directory) -> list:
    result = []
    if directory:
        result = sorted(glob.glob(os.path.join(directory, "*.md")))
    for pat in patterns:
        expanded = sorted(glob.glob(pat))
        result += expanded if expanded else [pat]
    # Eliminar duplicados preservando orden
    seen, unique = set(), []
    for f in result:
        if f not in seen:
            seen.add(f); unique.append(f)
    return unique


def main():
    ap = argparse.ArgumentParser(
        prog="concat_md.py",
        description="Une varios .md en un único fichero, paso previo al pipeline pdf-export.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ver SKILL.md / README.md del skill pdf-export para el pipeline completo.",
    )
    ap.add_argument("files", nargs="*",
                    help="Archivos .md o patrones glob (p.ej. cap*.md)")
    ap.add_argument("--dir", metavar="DIR",
                    help="Directorio con .md; se concatenan ordenados por nombre")
    ap.add_argument("-o", "--output", required=True, metavar="SALIDA",
                    help="Archivo .md de salida (p.ej. combined.md)")
    ap.add_argument("--title",  metavar="TEXTO", help="Título para el frontmatter YAML")
    ap.add_argument("--author", metavar="TEXTO", help="Autor para el frontmatter YAML")
    ap.add_argument("--date",   metavar="TEXTO", help="Fecha para el frontmatter YAML")
    ap.add_argument("--lang",   metavar="CÓDIGO", default="es",
                    help="Código de idioma ISO (default: es)")
    ap.add_argument("--pagebreaks", action="store_true",
                    help="Insertar <div page-break> entre secciones "
                         "(útil con Chrome/Pipeline A; con CSS h1 break-before no es necesario)")
    ap.add_argument("--keep-frontmatter", action="store_true",
                    help="No eliminar el frontmatter YAML de cada archivo fuente")
    args = ap.parse_args()

    # ── Resolver lista de archivos ────────────────────────────────────────────
    sources = _resolve_files(args.files, args.dir)
    if not sources:
        print("ERROR: no se encontraron archivos .md.", file=sys.stderr)
        sys.exit(1)
    missing = [f for f in sources if not os.path.isfile(f)]
    if missing:
        for f in missing:
            print(f"ERROR: no existe: {f}", file=sys.stderr)
        sys.exit(1)

    print(f"Concatenando {len(sources)} archivo(s):")
    for f in sources:
        print(f"  {f}")

    # ── Leer y procesar cada archivo ─────────────────────────────────────────
    parts = []
    first_meta = {}
    for i, path in enumerate(sources):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if args.keep_frontmatter:
            body = text
        else:
            meta, body = _parse_frontmatter(text)
            if i == 0:
                first_meta = meta
        parts.append(body.strip())

    sep = (_PAGE_BREAK + "\n") if args.pagebreaks else "\n\n"
    combined = sep.join(parts) + "\n"

    # ── Frontmatter del documento combinado ──────────────────────────────────
    title  = args.title  or first_meta.get("title")
    author = args.author or first_meta.get("author")
    date   = args.date   or first_meta.get("date")
    header = _build_frontmatter(title, author, date, args.lang)

    # ── Escribir salida ───────────────────────────────────────────────────────
    with open(args.output, "w", encoding="utf-8") as fh:
        if header:
            fh.write(header)
        fh.write(combined)

    size_kb = os.path.getsize(args.output) // 1024
    print(f"\n✅  {args.output}  ({size_kb} KB, {len(sources)} secciones)")
    print(f"    Siguiente paso:")
    print(f"      pandoc {args.output} --standalone --embed-resources --css=estilo.css -o out.html")


if __name__ == "__main__":
    main()
