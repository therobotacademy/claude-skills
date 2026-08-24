---
name: pdf-toc-bookmarker
description: Genera bookmarks (outline/marcadores de navegación) para un PDF que no trae outline embebido. Si el PDF fue generado con el skill pdf-export (Pipeline A, Chrome headless) a partir de un .md fuente, parsea directamente los headings Markdown (#, ##, ###) y los localiza en el PDF — sin necesidad de índice impreso. Si no hay .md fuente, extrae el texto de las páginas de "Contents"/"Índice" impreso, parsea la jerarquía (Partes > Capítulos > Secciones), calcula el offset entre número de página impreso y el índice real de página del PDF, y escribe un nuevo PDF con marcadores anidados usando pypdf. Activa este skill cuando el usuario suba un PDF (libro, manual, tesis, paper) y pida "añade bookmarks/marcadores según el índice", "genera el outline", "pon marcadores de navegación", o cualquier variante que implique convertir un índice (impreso o Markdown) en marcadores navegables de PDF. No lo actives para anotaciones/highlights sueltos ni para PDFs que ya traen outline (comprobar primero con reader.outline).
license: Proprietary. LICENSE.txt has complete terms
---
# PDF TOC → Bookmarks

## Cuándo se necesita

Muchos PDFs (libros escaneados/exportados, papers largos, manuales) tienen una página de "Contents" / "Índice" **impresa como texto** pero no tienen un outline (`/Outlines`) embebido en la estructura del PDF, así que el panel de marcadores del lector queda vacío. Este skill reconstruye ese outline a partir del texto del índice.

Antes de nada, comprobar si el PDF ya tiene outline (si lo tiene, no hace falta este proceso):

```python
from pypdf import PdfReader
r = PdfReader("input.pdf")
print(bool(r.outline))  # True si ya hay marcadores
```

## Atajo: PDF generado con el skill `pdf-export`

Si el PDF viene de `pdf-export` **Pipeline A** (Chrome headless + KaTeX — el que se usa cuando el documento tiene fórmulas LaTeX, porque Pipeline B/WeasyPrint no las renderiza), **no hace falta parsear nada a mano**: Pipeline A es precisamente el único de los dos pipelines de `pdf-export` que no genera bookmarks (Pipeline B/WeasyPrint ya los genera automáticamente desde los headings HTML). Y como el PDF nace de un `.md` con headings `#`/`##`/`###`, esos headings **son** el índice de contenidos — no hay que adivinarlo ni del texto renderizado ni de una página "Contents" que no existe.

Usar directamente el script empaquetado `examples/build_bookmarks_from_md_source.py`:

```bash
python build_bookmarks_from_md_source.py <fuente.md> <pdf_generado.pdf> [salida.pdf]
```

Qué hace:

1. Parsea los headings del `.md` fuente (nivel = número de `#`, normalizado para que el nivel mínimo presente sea 0).
2. Localiza cada heading en el PDF buscando su texto normalizado, avanzando un cursor de página (los headings aparecen en el mismo orden en el `.md` y en el PDF, así que nunca hay que retroceder).
3. Construye el outline anidado con pypdf respetando la jerarquía de `#`.
4. Verifica: cuenta nodos, imprime muestra de páginas, avisa (`AVISO: no se localizo...`) si algún heading no se pudo emparejar (revisar manualmente esos casos — normalmente indica que el heading fue reescrito/roto en el HTML intermedio).

Válido para **cualquier** `.md` exportado con `pdf-export` Pipeline A, no solo para el caso concreto con el que se validó (`DIRICHLET_ENERGY_EDUCATION_PAPER.md`, 18 headings capturados correctamente incluyendo un `####` que un parseo manual del PDF renderizado había pasado por alto — ver commit de referencia). Si el PDF **no** tiene un `.md` fuente disponible (viene de un escaneo, de un tercero, o el `.md` se perdió), usar el procedimiento estándar de más abajo.

## Procedimiento estándar (sin fuente Markdown disponible) — 5 pasos

### 1. Localizar y extraer las páginas del índice

El índice suele estar en las primeras 10-20 páginas. Extraer texto página a página hasta encontrar el bloque "Contents"/"Índice" y seguir hasta que termine (normalmente reconocible porque después empieza "Preface"/"Prólogo" o el capítulo 1).

```python
full = ""
for i in range(START, END):
    full += reader.pages[i].extract_text() + "\n"
```

Guardar en un fichero intermedio (`toc_raw.txt`) para poder iterar el parseo sin re-extraer.

### 2. Limpiar y re-unir líneas partidas

`extract_text()` corta cada línea del PDF, así que un título largo que ocupa dos líneas en el índice llega partido en dos strings. Además suele haber "running headers" tipo `vi Contents` o `Contents vii` intercalados que hay que descartar.

Heurística que funciona bien: una entrada del índice **siempre termina en un número de página** (o número romano). Ir concatenando líneas hasta que la línea acumulada termine en dígitos/números romanos, momento en el que se cierra la entrada:

```python
import re
merged, buf = [], ""
for s in clean_lines:
    buf = (buf + " " + s).strip() if buf else s
    if re.search(r'\d+$', buf):   # ajustar si el índice usa numeración romana para el frontmatter
        merged.append(buf)
        buf = ""
```

### 3. Parsear la jerarquía con regex

Diseñar un regex por nivel jerárquico. Para un libro típico con Partes/Capítulos/Secciones:

```python
# Parte:    "Part I: Introduction  1"
re.match(r'^Part\s+([IVX]+):\s*(.+?)\s+(\d+)$', line)
# Capítulo: "3   Interpreting and Asking Questions...  31"  (número SIN punto)
re.match(r'^(\d{1,3})\s+(.+?)\s+(\d+)$', line)
# Sección:  "3.4 How to View and Interpret...  38"  (número.número)
re.match(r'^(\d{1,3}\.\d{1,2})\s+(.+?)\s+(\d+)$', line)
```

Importante: probar el regex de **sección** (con punto) antes que el de **capítulo** (sin punto) si se aplican en cascada, porque un número de capítulo de una cifra podría hacer falso-match; en la práctica basta con que el regex de capítulo exija que tras el/los dígitos venga un espacio y no un punto, ya que `\s+` no casa con `.`.

Adaptar los patrones al idioma/formato real (p. ej. "Chapter 3", "Cap. 3", numeración con guiones, etc.) — inspeccionar primero 20-30 líneas del índice ya limpio antes de fijar los regex.

Imprimir cualquier línea que no matchee ningún patrón (`UNMATCHED: ...`) y no continuar hasta que la lista esté vacía o las líneas restantes sean basura conocida (paginación residual, etc.).

### 4. Calcular el offset página-impresa → índice-real-del-PDF

El número de página impreso en el libro casi nunca coincide con el índice 0-based de `reader.pages`. Calcularlo empíricamente, NO asumirlo:

1. Elegir 2-3 puntos de referencia fáciles de verificar: el inicio del Capítulo 1 (que suele coincidir con el final del índice) y algo cerca del final (Referencias/Índice alfabético).
2. Extraer texto de páginas candidatas del PDF hasta encontrar el título exacto y anotar su índice real.
3. `offset = pdf_index - printed_page` para la numeración arábiga del cuerpo.
4. El frontmatter con numeración romana (Prefacio, Agradecimientos) casi siempre tiene **offset 0** contando desde la primera página del PDF como "i" — pero verificarlo igual con el mismo método.
5. Verificar el offset en un tercer punto lejano (p. ej. las últimas páginas) para confirmar que es constante en todo el documento — algunos PDFs cambian de numeración a mitad (láminas, anexos) y necesitan más de un offset.

```python
roman_map = {'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000}
def roman_to_int(s):
    s = s.lower(); total = prev = 0
    for ch in reversed(s):
        val = roman_map[ch]
        total += val if val >= prev else -val
        prev = val
    return total
```

### 5. Construir el outline anidado con pypdf

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()
writer.append(reader)

part_ref = chapter_ref = None
for level, title, pdf_page in entries:   # level: 0=Parte, 1=Capítulo, 2=Sección
    if level == 0:
        part_ref = writer.add_outline_item(title, pdf_page)
        chapter_ref = None
    elif level == 1:
        chapter_ref = writer.add_outline_item(title, pdf_page, parent=part_ref)
    elif level == 2:
        writer.add_outline_item(title, pdf_page, parent=chapter_ref or part_ref)

with open("output_bookmarked.pdf", "wb") as f:
    writer.write(f)
```

Si el libro no tiene "Partes" (solo Capítulos y Secciones), usar solo 2 niveles y omitir `part_ref`.

## Verificación obligatoria antes de entregar

1. Releer el PDF generado con `PdfReader` y recorrer `reader.outline` recursivamente contando nodos — el total debe coincidir con el número de entradas parseadas.
2. Imprimir el árbol (al menos los 2 primeros niveles) y revisar visualmente que la jerarquía Parte→Capítulo→Sección es correcta.
3. Verificar 3-4 entradas al azar abriendo `reader.pages[pdf_index].extract_text()[:150]` y comprobando que el contenido de esa página corresponde al título del marcador (no a la página siguiente/anterior — un offset mal calculado se nota inmediatamente aquí).

## Errores comunes

- **Offset off-by-one o off-by-N**: sale de calcularlo solo con un punto de referencia. Usar siempre ≥2 puntos y, si el libro es largo (>300 páginas), un tercero cerca del final.
- **Confundir número de sección con número de página** en títulos que empiezan por dígitos (p. ej. "1/f Power Scaling", "3D reconstruction..."): el regex de captura de página debe anclarse al **final** de la línea (`\s+(\d+)$`), nunca buscar el primer número.
- **Runing headers colándose como entradas**: filtrar líneas tipo `^[ivxlc]+\s+Contents$` o `^Contents\s+[ivxlc]+$` antes de parsear.
- **No comprobar si ya existe outline**: perder tiempo reconstruyendo algo que el PDF ya trae.

## Variante: documento corto SIN página de índice impresa NI `.md` fuente disponible

Papers académicos, informes o exports HTML→PDF cortos (normalmente <15 páginas) a menudo **no tienen ninguna página "Contents"**: los encabezados de sección (`1. Introduction`, `2.1. Subsección`, ...) están incrustados directamente en el cuerpo del texto, mezclados con el contenido. Si **sí** hay un `.md` fuente disponible (típico si el PDF salió de `pdf-export`), usar el atajo de la sección anterior — es estrictamente más fiable, porque un parseo manual del texto ya renderizado puede saltarse subtítulos (p. ej. un `####` perdido entre fórmulas). Este procedimiento manual es el **último recurso**, solo cuando no existe `.md` fuente y tampoco hay TOC impreso:

1. **Confirmar que no hay TOC impreso ni `.md` fuente**: extraer y ojear el texto completo (no solo las primeras páginas) — si con `len(reader.pages) < ~15` y no aparece ningún bloque "Contents"/"Índice", se trata de este caso.
2. **Volcar el texto completo a un fichero intermedio**, página por página con marcador `=== PAGE N ===`, y leerlo entero (no solo los primeros 500 caracteres — los encabezados de sección pueden aparecer en cualquier punto de la página, y `extract_text()` en PDFs exportados desde HTML/MathML puede intercalar fórmulas entre el título y el resto del párrafo).
3. **Identificar manualmente los encabezados de sección** por su patrón numérico (`N.`, `N.N.`, `N.N.N.`) al inicio de línea, ignorando números que en realidad son resultados/estadísticas dentro del cuerpo (distinguibles porque no van seguidos de un título en mayúscula/Title Case coherente con las demás secciones).
4. **No hay offset que calcular**: al no existir paginación impresa independiente, el índice de página real de pypdf (0-based) coincide con la página física en la que aparece cada encabezado — anotar directamente `pdf_page` al leer el volcado.
5. Construir el outline igual que en el paso 5 del procedimiento estándar (`writer.add_outline_item`), respetando la jerarquía por el número de puntos en la numeración (`N.` = nivel 0, `N.N.` = nivel 1, `N.N.N.` = nivel 2).
6. Verificación: igual que el procedimiento estándar (contar nodos, revisar árbol, comprobar 3-4 páginas al azar con `extract_text()[:150]`).

Script de referencia QUE DEBE EJECUTAR este skill si el PDF procede de una fuente Markdown: `examples/build_bookmarks_from_md_source.py`

En otro caso, se proporciona el ejemplo `examples/build_bookmarks_no_toc_example.py` (entradas hardcodeadas, sin regex de parseo). Úsalo como plantilla solo si de verdad no hay `.md` fuente — en su momento se usó para `DIRICHLET_ENERGY_EDUCATION_PAPER.pdf` antes de descubrir que sí existía el `.md` fuente, y el parseo manual efectivamente se saltó un heading `####` que el script `build_bookmarks_from_md_source.py` sí capturó correctamente (18 headings vs. 16). Caso real ya resuelto con el atajo Markdown.
