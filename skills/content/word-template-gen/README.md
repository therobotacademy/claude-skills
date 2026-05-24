# word-template-gen

Generador de **plantillas Word (.docx)** y render a **PDF / HTML** de documentos escritos en **Markdown**, a partir de un **catálogo de temas**.

La idea central: el diseño vive en un **tema** (un JSON con fuentes, paleta y tamaños), y de ese único tema se derivan a la vez:

- el **CSS** que se inyecta en el HTML (y por tanto en el PDF, vía Chrome headless), y
- la **plantilla de referencia `.docx`** de Word (vía `python-docx` sobre el `reference.docx` de pandoc).

Así, el estilo que ves en el PDF es exactamente el que se incorpora al Word.

```
TEMA (themes/<name>.json) ──► CSS ──► HTML ──► PDF
                          └─► estilos Word ──► reference.docx ──► .docx
```

---

## Requisitos

| Herramienta | Para qué | Obligatorio |
|---|---|---|
| [pandoc](https://pandoc.org) | Markdown → HTML / .docx | sí |
| `python-docx` (`pip install python-docx`) | restilar la plantilla Word | sí |
| Chrome o Edge | HTML → PDF (headless) | solo para PDF |

El motor detecta Chrome/Edge en las rutas habituales de Windows. Pandoc debe estar en el `PATH`.

---

## Uso

### Ver el catálogo

```bash
python wtg.py list
```

### Uso 1 — Producir una plantilla Word nueva

Genera un `.docx` de referencia reutilizable con cualquier Markdown:

```bash
python wtg.py template --theme academico-brj --out plantilla.docx
```

Después, con tu documento:

```bash
pandoc doc.md --reference-doc=plantilla.docx -o doc.docx
```

### Uso 2 — Render de un Markdown con el estilo elegido

El mismo tema produce el CSS del PDF y la plantilla del Word:

```bash
# PDF (formato por defecto)
python wtg.py render --md doc.md --theme moderno

# Varios formatos y carpeta de salida
python wtg.py render --md doc.md --theme academico-brj --to pdf,docx,html --out salida/
```

- `--to` — lista separada por comas de `pdf`, `docx`, `html` (por defecto `pdf`).
- `--out` — directorio de salida (por defecto, el del `.md`).

---

## Catálogo de temas

| Tema | Cuerpo / Títulos | Acento | Uso típico |
|---|---|---|---|
| `academico-brj` | Georgia / Arial | rojo tierra `#7a3b2e` | ensayos, ebook (estilo de la casa) |
| `neutro` | Times New Roman | negro | entregas académicas formales (interlineado doble) |
| `moderno` | Calibri / Segoe UI | azul `#2563eb` | informes, documentación |

---

## Mapa Markdown → estilo (común a HTML/PDF y Word)

| Markdown | HTML/PDF (CSS) | Word (estilo) |
|---|---|---|
| párrafo | `body` | Normal / Body Text |
| `#` / `##` / `###` | `h1` / `h2` / `h3` | Heading 1 / 2 / 3 |
| metadato YAML `title:` / `subtitle:` | `.title` / `.subtitle` | Title / Subtitle |
| `> cita` | `blockquote` | Block Text |
| `[texto]{custom-style="Resaltado"}` | `.Resaltado` | Resaltado (estilo de carácter) |

**Salto de página en Word:** inserta un bloque raw OpenXML dentro de una valla ` ```{=openxml} `:

````text
```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
````

**Fórmulas LaTeX en PDF:** añade `--katex` al `pandoc` del paso de render (ver skill `pdf-export`).

---

## Añadir un tema

Copia un JSON de `themes/` y ajústalo. Aparece automáticamente en `wtg.py list`.

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

- `body_font` / `head_font` — nombres de fuente **de Word** (deben existir en el sistema).
- `css_body_stack` / `css_head_stack` — pilas CSS equivalentes para HTML/PDF.
- `palette` — `ink` (texto), `accent` (H2/subtítulo), `muted` (H3/citas), `extra` (resaltado), `rule` (líneas/bordes), `bg` (fondo).

---

## Estructura

```
word-template-gen/
├── README.md            ← este archivo
├── SKILL.md             ← instrucciones y triggers del skill (Claude)
├── wtg.py               ← motor: catálogo + generadores
├── themes/
│   ├── academico-brj.json
│   ├── neutro.json
│   └── moderno.json
└── _test/
    └── muestra.md       ← Markdown de ejemplo para probar el render
```

---

## Solución de problemas

| Síntoma | Causa | Acción |
|---|---|---|
| `Tema desconocido` | nombre mal escrito | `python wtg.py list` para ver los válidos |
| PDF no se genera | no hay Chrome/Edge | instala uno, o usa `--to docx,html` |
| La fuente no cambia en Word | la fuente no existe en el sistema | usa una fuente instalada en `body_font`/`head_font` |
| Fórmulas sin renderizar en PDF | falta KaTeX | añade `--katex` al pandoc del render |

---

*Generaliza el pipeline del skill `pdf-export` (export puntual a PDF/Word) hacia un sistema multi-tema reutilizable.*
