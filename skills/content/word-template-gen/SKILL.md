---
name: word-template-gen
description: "Generador de plantillas Word (.docx) y render PDF/HTML de documentos Markdown a partir de un CATÁLOGO DE TEMAS. Cada tema es la fuente única de diseño (fuentes, paleta, tamaños) de la que se derivan a la vez el CSS que se inyecta en el HTML/PDF y la plantilla de referencia de Word, de modo que el mismo estilo del PDF es el que se incorpora al Word. Activa este skill cuando Bernardo pida 'genera una plantilla Word', 'plantilla word', 'word-template-gen', 'nueva plantilla de estilo', 'crea un reference-doc', 'catálogo de estilos', 'renderiza este md con el estilo X', 'exporta el md a pdf/word con el tema Y', 'qué temas hay', o cualquier variante que implique (1) producir un fichero de plantilla Word nuevo o (2) producir un PDF/Word desde un Markdown seleccionando el estilo. Para una exportación puntual a PDF sin elegir tema, vale también el skill pdf-export."
---

# word-template-gen — plantillas Word + PDF por tema

Genera documentos con estilo a partir de Markdown. La idea central: **el diseño vive en un TEMA**, y de ese único tema se derivan a la vez el **CSS que se inyecta en el HTML** (y por tanto en el PDF, vía Chrome headless) y la **plantilla de referencia `.docx`** de Word (vía `python-docx` sobre el `reference.docx` de pandoc). Así, el estilo que ves en el PDF es exactamente el que se incorpora al Word.

```
TEMA (themes/<name>.json)  →  CSS  →  HTML  →  PDF
                           →  estilos Word  →  reference.docx  →  .docx
```

## Requisitos

`pandoc`, `python-docx` y, solo para PDF, Chrome o Edge. Motor: `wtg.py` (en este directorio).

## Catálogo de temas

Cada tema es un JSON en `themes/`. Listarlos:

```bash
python wtg.py list
```

Incluidos: `academico-brj` (estilo del ebook: Georgia + Arial, rojo tierra), `neutro` (Times, sobrio, interlineado doble), `moderno` (Segoe/Calibri, acento azul).

## Uso 1 — Producir una plantilla Word nueva

Genera un `.docx` de referencia (reutilizable con cualquier Markdown):

```bash
python wtg.py template --theme academico-brj --out plantilla.docx
```

Luego, con cualquier documento: `pandoc doc.md --reference-doc=plantilla.docx -o doc.docx`.

## Uso 2 — Producir PDF/Word desde un Markdown seleccionando el estilo

Renderiza un `.md` con el tema elegido. El mismo tema produce el CSS del PDF y la plantilla del Word:

```bash
# PDF (por defecto)
python wtg.py render --md doc.md --theme moderno

# Varios formatos a la vez
python wtg.py render --md doc.md --theme academico-brj --to pdf,docx,html --out salida/
```

- `--to`: lista separada por comas de `pdf`, `docx`, `html` (por defecto `pdf`).
- `--out`: directorio de salida (por defecto, el del `.md`).

## Mapa Markdown → estilo (común a HTML/PDF y Word)

| Markdown | HTML/PDF (CSS) | Word (estilo) |
|---|---|---|
| párrafo | body | Normal / Body Text |
| `# / ## / ###` | h1 / h2 / h3 | Heading 1 / 2 / 3 |
| título/subtítulo (metadato YAML `title:`/`subtitle:`) | `.title` / `.subtitle` | Title / Subtitle |
| `> cita` | blockquote | Block Text |
| `[texto]{custom-style="Resaltado"}` | `.Resaltado` | Resaltado (carácter) |
| `[texto]{.resaltado}` | `.resaltado` | — (solo HTML) |

Salto de página en Word: inserta un bloque raw OpenXML `<w:p><w:r><w:br w:type="page"/></w:r></w:p>` dentro de una valla ` ```{=openxml} `.

## Añadir un tema nuevo

Copia un JSON de `themes/` y ajusta:

```json
{
  "name": "mi-tema",
  "label": "Descripción corta",
  "body_font": "Georgia", "head_font": "Arial",
  "css_body_stack": "Georgia, serif", "css_head_stack": "Arial, sans-serif",
  "palette": { "ink": "#1c1b19", "accent": "#7a3b2e", "muted": "#6b6357",
               "extra": "#4a6b54", "rule": "#d9d2c7", "bg": "#fbf9f5" },
  "sizes": { "body": 11.5, "h1": 19, "h2": 14.5, "h3": 12, "title": 26, "subtitle": 14 },
  "line_spacing": 1.5, "page_margin_cm": 2.0
}
```

`body_font`/`head_font` son nombres de fuente de Word (deben existir en el sistema). `css_*_stack` son las pilas CSS equivalentes para HTML/PDF. Tras crearlo, aparece automáticamente en `wtg.py list`.

## Notas

- Para fórmulas LaTeX en el PDF, añade `--katex` al `pandoc` del render (ver skill `pdf-export`).
- Word aplica estilos vía pandoc `--reference-doc`; el `.docx` de referencia se regenera al vuelo en cada `render --to docx`, o se persiste con `template`.
