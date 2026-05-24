---
name: pdf-export
description: "Exporta documentos Markdown a PDF usando el pipeline confirmado en este proyecto: Pandoc (KaTeX para fórmulas LaTeX) → HTML → Chrome headless (por defecto) o WeasyPrint (cuando se piden marcadores/bookmarks/PDF navegable). Activa este skill cuando Bernardo pida 'exportar a PDF', 'genera el PDF', 'convierte a PDF', 'render PDF', 'pdf-export', o cualquier variante que implique producir un PDF desde un fichero Markdown o contenido con fórmulas. También actívalo cuando mencione 'pandoc', 'chrome headless', 'marcadores', 'bookmarks', 'PDF navegable', o pida ajustar márgenes/estilos del PDF."
---

# PDF Export — Pipeline Pandoc + KaTeX + Chrome headless

Pipeline verificado en este equipo (2026-05-23). No requiere LaTeX ni wkhtmltopdf.

## Herramientas disponibles

| Herramienta | Ruta / Comando | Cuándo usarla |
|---|---|---|
| Pandoc 3.9.0.2 | `C:\Users\brjap\AppData\Local\Pandoc\pandoc` | Siempre (conversión MD → HTML) |
| Chrome | `C:\Program Files\Google\Chrome\Application\chrome.exe` | Pipeline por defecto (sin marcadores) |
| WeasyPrint | `weasyprint` (en PATH si instalado) | Pipeline con marcadores/bookmarks |

> **WeasyPrint no instalado?** Instalar con: `pip install weasyprint`
> Limitación: fórmulas LaTeX complejas pueden no renderizarse — usar solo cuando no hay fórmulas o son simples.

Referencia completa: `pdf-guide.md` en la raíz del proyecto.

---

## Verificación del setup

Ejecuta estas comprobaciones **siempre que se invoque el skill por primera vez en una sesión**. Si alguna dependencia falta, reporta al usuario antes de continuar con cualquier exportación.

### Comandos de verificación

```powershell
# Pandoc — requerido siempre
pandoc --version

# Chrome — requerido para Pipeline A
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"

# WeasyPrint — requerido solo para Pipeline B (marcadores)
weasyprint --version

# Python/pip — necesario para instalar WeasyPrint si falta
python --version
pip --version
```

### Tabla de dependencias

| Herramienta | Pipeline | Verificación | Resultado esperado | Cómo instalar si falta |
|---|---|---|---|---|
| **Pandoc** | A y B | `pandoc --version` | `pandoc 3.x.x` | [pandoc.org/installing.html](https://pandoc.org/installing.html) — descarga el instalador `.msi` |
| **Chrome** | A (por defecto) | `Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"` | `True` | Instalar Google Chrome desde chrome.google.com |
| **WeasyPrint** | B (marcadores) | `weasyprint --version` | `WeasyPrint x.x` | `pip install weasyprint` |
| **Python + pip** | Prerequisito de WeasyPrint | `python --version` / `pip --version` | `Python 3.x` | [python.org/downloads](https://www.python.org/downloads/) — marcar "Add to PATH" en el instalador |

### Cómo reportar al usuario

Tras ejecutar las comprobaciones, muestra un bloque de estado claro:

**Setup completo (ejemplo):**
```
✅ Setup verificado
   Pandoc 3.9.0.2 — OK
   Chrome — OK
   WeasyPrint — OK (Pipeline B disponible)
```

**Setup parcial (ejemplo — WeasyPrint ausente):**
```
⚠️  Setup parcial — dependencia faltante:

   ✅ Pandoc 3.9.0.2 — OK
   ✅ Chrome — OK
   ❌ WeasyPrint — no encontrado
      → Instalar: pip install weasyprint
      → Verificar tras instalar: weasyprint --version

   Pipeline A (Chrome headless, sin marcadores) disponible.
   Pipeline B (marcadores) no disponible hasta instalar WeasyPrint.
   ¿Continuar con Pipeline A?
```

**Setup roto (Pandoc o Chrome ausente):**
```
🚫 No se puede exportar — dependencia crítica faltante:

   ❌ Pandoc — no encontrado
      → Instalar: https://pandoc.org/installing.html

   Deteniéndose. Instala Pandoc y vuelve a intentarlo.
```

Si falta Pandoc o Chrome, **detenerse completamente** — no intentar la exportación.
Si solo falta WeasyPrint, ofrecer continuar con Pipeline A.

---

## Protocolo de ejecución

### Paso 0 — Verificar setup

Ejecuta los comandos de la sección [Verificación del setup](#verificación-del-setup) y reporta el resultado al usuario. Si hay dependencias críticas ausentes, detente aquí.

### Paso 1 — Recibir el input

Identifica qué quiere exportar Bernardo:

- **Fichero existente**: ruta relativa o absoluta al `.md`
- **Contenido inline**: Bernardo pega el contenido en el chat → escríbelo a un `.md` temporal
- **Directorio**: múltiples `.md` → pregunta si quiere un PDF por fichero o concatenado

Si no hay ruta explícita, pregunta antes de asumir.

### Paso 2 — Elegir pipeline

Detecta si Bernardo pide **marcadores**, **bookmarks**, **PDF navegable**, o **outline**:

| Condición | Pipeline |
|---|---|
| Sin mención de marcadores | **Chrome headless** (por defecto) |
| Pide marcadores / PDF navegable / outline | **WeasyPrint** |
| Hay fórmulas LaTeX **y** pide marcadores | Avisa del conflicto; pregunta si prioriza fórmulas o marcadores |

### Paso 3 — Determinar opciones de salida

Pregunta solo si no está claro en el contexto:

- **Destino del PDF**: mismo directorio que el fuente (por defecto) o ruta específica
- **Metadatos**: título, autor, fecha (usa los del frontmatter YAML si los tiene el `.md`)
- **CSS personalizado**: si existe `estilo.css` en el directorio, úsalo automáticamente
- **Márgenes**: `--no-margins` por defecto; ajusta si Bernardo especifica

### Paso 4 — Ejecutar

#### Pipeline A — Chrome headless (por defecto, con KaTeX)

```bash
# Pandoc: Markdown → HTML con KaTeX embebido
pandoc <input.md> \
  --standalone \
  --katex \
  [-M title="<título>" -M author="<autor>" -M date="<fecha>"] \
  [--css=<estilo.css>] \
  -o <output.html>

# Chrome headless: HTML → PDF (sin marcadores)
"/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --headless=new \
  --print-to-pdf=<output.pdf> \
  --no-margins \
  <output.html>
```

#### Pipeline B — WeasyPrint (con marcadores automáticos)

```bash
# Pandoc: Markdown → HTML (sin KaTeX; WeasyPrint no lo interpreta)
pandoc <input.md> \
  --standalone \
  [-M title="<título>" -M author="<autor>" -M date="<fecha>"] \
  [--css=<estilo.css>] \
  -o <output.html>

# WeasyPrint: HTML → PDF con bookmarks desde los headings H1-H6
weasyprint <output.html> <output.pdf>
```

> WeasyPrint genera el árbol de marcadores automáticamente a partir de los headings del HTML — no requiere configuración adicional.

Elimina el `.html` intermedio después del PDF salvo que Bernardo lo pida explícitamente.

### Paso 5 — Verificar y abrir

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
| Fórmulas rotas con WeasyPrint | WeasyPrint no interpreta KaTeX/MathML | Usa pipeline A (Chrome headless) si el doc tiene fórmulas |
| Marcadores no aparecen | Pipeline A (Chrome) usado por error | Cambia a pipeline B (WeasyPrint) |
| `weasyprint` no encontrado | No instalado | Ejecuta `pip install weasyprint` |
