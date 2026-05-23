---
name: pdf-export
description: "Exporta documentos Markdown a PDF usando el pipeline confirmado en este proyecto: Pandoc (KaTeX para fórmulas LaTeX) → HTML → Chrome headless. Activa este skill cuando Bernardo pida 'exportar a PDF', 'genera el PDF', 'convierte a PDF', 'render PDF', 'pdf-export', o cualquier variante que implique producir un PDF desde un fichero Markdown o contenido con fórmulas. También actívalo cuando mencione 'pandoc', 'chrome headless', o pida ajustar márgenes/estilos del PDF."
---

# PDF Export — Pipeline Pandoc + KaTeX + Chrome headless

Pipeline verificado en este equipo (2026-05-23). No requiere LaTeX ni wkhtmltopdf.

## Herramientas disponibles

| Herramienta | Ruta |
|---|---|
| Pandoc 3.9.0.2 | `C:\Users\brjap\AppData\Local\Pandoc\pandoc` |
| Chrome | `C:\Program Files\Google\Chrome\Application\chrome.exe` |

Referencia completa: `pdf-guide.md` en la raíz del proyecto.

---

## Protocolo de ejecución

### Paso 1 — Recibir el input

Identifica qué quiere exportar Bernardo:

- **Fichero existente**: ruta relativa o absoluta al `.md`
- **Contenido inline**: Bernardo pega el contenido en el chat → escríbelo a un `.md` temporal
- **Directorio**: múltiples `.md` → pregunta si quiere un PDF por fichero o concatenado

Si no hay ruta explícita, pregunta antes de asumir.

### Paso 2 — Determinar opciones de salida

Pregunta solo si no está claro en el contexto:

- **Destino del PDF**: mismo directorio que el fuente (por defecto) o ruta específica
- **Metadatos**: título, autor, fecha (usa los del frontmatter YAML si los tiene el `.md`)
- **CSS personalizado**: si existe `estilo.css` en el directorio, úsalo automáticamente
- **Márgenes**: `--no-margins` por defecto; ajusta si Bernardo especifica

### Paso 3 — Ejecutar

```bash
# Pandoc: Markdown → HTML con KaTeX embebido
pandoc <input.md> \
  --standalone \
  --katex \
  [-M title="<título>" -M author="<autor>" -M date="<fecha>"] \
  [--css=<estilo.css>] \
  -o <output.html>

# Chrome headless: HTML → PDF
"/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --headless=new \
  --print-to-pdf=<output.pdf> \
  --no-margins \
  <output.html>
```

Elimina el `.html` intermedio después del PDF salvo que Bernardo lo pida explícitamente.

### Paso 4 — Verificar y abrir

Comprueba que el PDF se generó (tamaño > 0). Ábelo con Chrome para que Bernardo lo revise:

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" <output.pdf> &
```

Informa del tamaño del fichero y la ruta de salida.

---

## Opciones frecuentes

### Metadatos desde frontmatter YAML

Si el `.md` tiene frontmatter, extrae `title`, `author`, `date` automáticamente:

```yaml
---
title: "Ética y Misión"
author: "Bernardo Ronquillo"
date: "2026"
lang: es
---
```

Pandoc los consume directamente con `--standalone`; no hace falta `-M`.

### CSS de estilo académico

Si no hay `estilo.css` en el directorio, usa este mínimo inline vía archivo temporal:

```css
body {
  font-family: "Georgia", serif;
  font-size: 12pt;
  line-height: 1.6;
  max-width: 700px;
  margin: 40px auto;
  color: #111;
}
h1, h2, h3 { font-family: "Helvetica Neue", sans-serif; }
h1 { font-size: 1.8em; border-bottom: 1px solid #ccc; padding-bottom: 0.3em; }
h2 { font-size: 1.3em; margin-top: 2em; }
blockquote {
  border-left: 3px solid #aaa;
  margin-left: 0;
  padding-left: 1em;
  color: #555;
  font-style: italic;
}
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 6px 10px; }
th { background: #f0f0f0; }
```

### Márgenes personalizados

Pasa las opciones directamente a Chrome:

```bash
--margin-top=2cm --margin-bottom=2cm --margin-left=2.5cm --margin-right=2cm
```

### Múltiples ficheros → un PDF

Concatena con Pandoc antes de convertir:

```bash
pandoc doc1.md doc2.md doc3.md --standalone --katex -o combined.html
```

---

## Fórmulas LaTeX — referencia rápida

| Tipo | Sintaxis |
|---|---|
| Inline | `$E = mc^2$` |
| Block | `$$\int_0^\infty e^{-x^2}dx = \frac{\sqrt{\pi}}{2}$$` |
| Fracción | `\frac{a}{b}` |
| Raíz | `\sqrt{x}`, `\sqrt[n]{x}` |
| Sumatorio | `\sum_{i=1}^{n} x_i` |
| Integral | `\int_a^b f(x)\,dx` |
| Límite | `\lim_{x \to 0} f(x)` |
| Matriz | `\begin{pmatrix} a & b \\ c & d \end{pmatrix}` |
| Conjuntos | `\mathbb{R}`, `\mathbb{N}`, `\mathbb{Z}` |
| Norma | `\|x\|`, `\langle x, y \rangle` |

---

## Manejo de errores

| Síntoma | Causa probable | Acción |
|---|---|---|
| PDF de 0 bytes | Chrome no encontró el HTML | Verifica la ruta absoluta del HTML |
| Fórmulas sin renderizar | KaTeX no embebido | Confirma que pandoc usó `--katex`, no `--mathjax` |
| Salto de página en tabla | CSS no aplicado | Añade `page-break-inside: avoid` a `table` en el CSS |
| Texto cortado en márgenes | `--no-margins` activo con contenido ancho | Ajusta `max-width` en CSS o añade márgenes explícitos a Chrome |
