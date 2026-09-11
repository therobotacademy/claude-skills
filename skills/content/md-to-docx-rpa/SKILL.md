---
name: md-to-docx-rpa
description: Emula un proceso RPA para generar o actualizar propuestas y documentos Word (.docx) a partir de plantillas corporativas preservando al 100% la identidad gráfica, maquetación de portada, tablas-ficha, encabezados dinámicos y tipografías exactas (Verdana, Poppins, Segoe UI, Calibri), eliminando la regresión a Times New Roman que introduce Pandoc o el uso ingenuo de python-docx.
---

# MD to DOCX RPA — Generación Fiel de Documentos Word sobre Plantillas Corporativas

## 1. Cuándo usar esta habilidad

Activa esta habilidad cuando Bernardo o el proyecto requiera:
* Generar una propuesta comercial, técnica o académica en formato **Word (.docx)** a partir de un Markdown (`.md`) o de contenidos estructurados, utilizando una plantilla corporativa de referencia.
* Preservar íntegramente la **maquetación visual**: portada de diseño, encabezados y pies de página con número dinámico, tablas-tarjeta de módulos y alineaciones.
* Evitar el fallo crítico de **Times New Roman**: Word degrada automáticamente cualquier fragmento de texto a Times New Roman si se sobreescriben párrafos con la API estándar o si se usa Pandoc con `--reference-doc`.

---

## 2. Por qué Pandoc y la API básica de docx fallan

### El fallo de Pandoc (`--reference-doc`)
Pandoc solo lee la tipografía asociada a los nombres de los estilos de párrafo (`Normal`, `Heading 1`). Por especificación, Pandoc **descarta por completo**:
* La portada completa (logos, cuadros de texto, metadatos, autor).
* Encabezados y pies de página de la plantilla.
* Tablas formateadas y márgenes de sección.

### El fallo de `python-docx` básico (`paragraph.text = "..."`)
En Word OpenXML, cada párrafo contiene fragmentos (`<w:r>`) con propiedades de fuente directas (`<w:rPr><w:rFonts w:ascii="Verdana".../>`).
Cuando un script ejecuta `p.text = "Nuevo texto"`:
1. Elimina todos los `runs` existentes y sus propiedades tipográficas.
2. Crea un único run sin atributos `w:rFonts`.
3. Word busca la fuente de reserva en `<w:docDefaults>` dentro de `word/styles.xml`. Si este valor es *Times New Roman* (muy común en plantillas de Word antiguas), **todo el texto nuevo se convierte en Times New Roman**.

---

## 3. El Patrón RPA de Emulación Humana

Para actuar como un operador RPA que teclea dentro de Word preservando la identidad gráfica, la habilidad aplica cuatro principios:

### 3.1. Clonación Directa
Nunca se crea un documento en blanco. Se hace una copia exacta del archivo `.docx` de referencia (`shutil.copyfile`).

### 3.2. Parcheo Preventivo de `docDefaults`
Antes de editar el contenido, se descomprime temporalmente el archivo Word y se sustituye en `word/styles.xml`:
```python
xml_str = xml_str.replace('w:ascii="Times New Roman"', 'w:ascii="Verdana"')
xml_str = xml_str.replace('w:hAnsi="Times New Roman"', 'w:hAnsi="Verdana"')
xml_str = xml_str.replace('w:cs="Times New Roman"', 'w:cs="Verdana"')
```
Esto asegura que, incluso si un fragmento carece de fuente explícita, Word jamás recurra a Times New Roman.

### 3.3. Inyección de Fuente por Fragmento (`w:rFonts`)
Toda inserción de texto nuevo se realiza forzando explícitamente los atributos en el XML:
```python
def set_run_font(run, font_name="Verdana", size_pt=9.5, bold=None, italic=None, color_rgb=None):
    run.font.name = font_name
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    if size_pt is not None:
        run.font.size = Pt(size_pt)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color_rgb is not None:
        run.font.color.rgb = color_rgb
```

### 3.4. Jerarquía Tipográfica Estándar
| Elemento | Tipografía | Tamaño | Peso / Estilo |
| :--- | :--- | :---: | :--- |
| **Portada · Título Principal** | `Calibri` | 36–40 pt | Negrita |
| **Portada · Subtítulo** | `Calibri` | 13 pt | Cursiva |
| **Portada · Metadatos / Cliente** | `Calibri` | 11 pt | Regular |
| **Encabezado Superior** | `Calibri` | 9 pt | Regular (preservando tabulación y campo `PAGE`) |
| **Títulos de Sección (H1)** | `Segoe UI` | 16 pt | Negrita |
| **Subtítulos de Sección (H2)** | `Poppins` | 12 pt | Negrita |
| **Encabezados de Nivel 3 (H3)** | `Poppins` | 10 pt | Negrita |
| **Tablas-Ficha · Título Módulo** | `Poppins` | 11 pt | Negrita |
| **Tablas-Ficha · Subtítulo** | `Verdana` | 9 pt | Negrita / Cursiva |
| **Cuerpo de Texto y Viñetas** | `Verdana` | 9,5 pt | Regular |
| **Tablas Resumen / Datos** | `Verdana` | 9,0–9,5 pt | Regular |

### 3.5. Motor de Ritmo Vertical y Geometría de Listas (Estilo Personal Corporativo)
Para replicar con exactitud el estilo editorial del autor y garantizar cohesión visual, el agente debe aplicar las siguientes reglas micro-tipográficas a nivel de párrafo (`w:pPr`):

| Elemento | Estilo Párrafo | Espaciado Anterior (`w:before`) | Espaciado Posterior (`w:after`) | Interlineado (`w:line`) | Sangría (`w:ind`) | Mecanismo de Viñeta |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Cuerpo Estándar** | `Normal` | 0 pt | 8 pt (160 twips) | 1,15 (276) | Ninguna | N/A |
| **Párrafo Puente (Lead-in a lista)** | `Normal` | 0 pt | 6 pt (120 twips) | 1,15 (276) | Ninguna | N/A |
| **Cierre de Subsección** | `Normal` | 0 pt | 12 pt (240 twips) | 1,15 (276) | Ninguna | N/A |
| **Viñeta Intermedia (Cuerpo)** | `List Paragraph` | 0 pt | 3 pt (60 twips) | 1,15 (276) | left: 714, hang: 357 | `numPr` (`numId=14`) |
| **Última Viñeta (Cuerpo)** | `List Paragraph` | 0 pt | 8 pt (160 twips) | 1,15 (276) | left: 714, hang: 357 | `numPr` (`numId=14`) |
| **Lista Numerada (Cuerpo)** | `List Paragraph` | 0 pt | 3 pt interm. / 8 pt fin | 1,15 (276) | left: 714, hang: 357 | `numPr` (`numId=16`) |
| **Viñeta en Tabla-Ficha** | `Normal` / Celda | 0 pt | 4 pt (80 twips) | 1,15 (276) | Ninguna | Literal `• ` |
| **Heading 1** | `Heading 1` | 16 pt (320 twips) | 10 pt (200 twips) | Auto | Ninguna | N/A |
| **Heading 2** | `Heading 2` | 16 pt (320 twips) | 7 pt (140 twips) | Auto | Ninguna | N/A |
| **Heading 3** | `Heading 3` | 12 pt (240 twips) | 5 pt (100 twips) | Auto | Ninguna | N/A |

#### Reglas de Implementación en OpenXML:
1. **Agrupación cohesiva de listas:** Los ítems intermedios de una lista en cuerpo llevan solo 3 pt (`w:after="60"`), mientras que el último ítem recupera los 8 pt (`w:after="160"`), delimitando el bloque frente al siguiente párrafo.
2. **Viñetas nativas en cuerpo:** En el cuerpo se usa `w:numPr` sin carácter literal `• ` en el run.
### 3.6. Arquitectura de Paginación Ejecutiva y Saltos de Bloque Temático

Para lograr un acabado visual directivo, los documentos no fluyen como un texto continuo indiferenciado, sino articulados en **bloques ejecutivos autocontenidos**:

| Bloque / Hito | Salto de Página (`<w:br w:type="page"/>`) | Propósito y Comportamiento Visual |
| :--- | :---: | :--- |
| **Portada Institucional** | **Sí** (tras autoría/disclaimer) | Aísla la portada como página noble independiente; la página 2 arranca limpia con `Heading 1: 1 Descripción General`. |
| **Cuadrícula Curricular (Sección 2)** | **NO partir** | Las tablas-ficha de sesiones (Sesiones 1 a 4) y `Casos prácticos` deben fluir de forma continua sin saltos manuales forzados entre sesiones (purgar cualquier salto residual de plantillas base). |
| **Ficha Logística (Sección 3)** | **Sí** (antes de `Heading 1: 3 Planificación...`) | Asegura que la tabla de planificación (3x2), material y perfiles de requisitos previos conformen una página operativa autocontenida. |
| **Hoja Económica (Sección 4)** | **Sí** (antes de `Heading 1: 4 Condiciones...`) | Convierte la propuesta comercial (precio, exención IVA Art. 20.Uno.9º, facturación, IBAN y pie de firma) en una hoja de encargo/presupuesto independiente. |

#### Reglas de Paginación en OpenXML:
1. **Salto de página limpio:** Insertar `<w:r><w:br w:type="page"/></w:r>` en un párrafo vacío precedente o configurar `w:pageBreakBefore` en el `<w:pPr>` del título de sección.
2. **Purgado de saltos huérfanos:** Al clonar un documento base, inspeccionar y eliminar cualquier `<w:br w:type="page"/>` intercalado entre tablas de sesión o dentro de listas de objetivos.

---

## 4. Plantilla Genérica por Defecto (`templates/`)


La habilidad incluye una plantilla limpia con textos `Lorem ipsum...`:
* **Ruta:** `templates/plantilla_propuesta_lorem.docx`
* **Características:**
  * Portada formal con placeholders parametrizables (`[Cliente]`, `[Título]`, `[Subtítulo]`).
  * Sección 1 con estructura de descripción, placeholder de imagen/diagrama y tabla de fases.
  * Sección 2 con 5 tablas-ficha modulares pre-maquetadas.
  * Sección 3 con tabla de planificación (Duración, Estructura, Modalidad), material y requisitos.
  * Sección 4 con condiciones económicas oficiales (Precio, exención IVA Art. 20.Uno.9º, facturación y cuenta bancaria).

---

## 5. Script Utilitario (`scripts/fill_docx_template.py`)

Para ejecuciones rápidas por línea de comandos:

```powershell
python skills/content/md-to-docx-rpa/scripts/fill_docx_template.py `
  --output "PROPUESTA_FINAL.docx" `
  --client "COIIAOC" `
  --title "Programa de Píldoras de Nivelación en Vídeo" `
  --subtitle "Preparación para el Curso de Pensamiento Estratégico" `
  --image "diagrama.png" `
  --price "600"
```

---

## 6. Checklist de Verificación de Salida

Tras generar cualquier archivo `.docx`:
- [ ] Ejecutar el comprobador de fuentes:
  ```python
  import docx
  doc = docx.Document("archivo.docx")
  fonts = {r._r.xpath('.//w:rFonts/@w:ascii')[0] for p in doc.paragraphs for r in p.runs if r._r.xpath('.//w:rFonts/@w:ascii')}
  assert not any('times' in f.lower() for f in fonts), f"Error: detectado Times New Roman: {fonts}"
  print("OK: Tipografías conformes:", fonts)
  ```
- [ ] Comprobar que la portada mantiene los márgenes y que el título no desborda.
- [ ] Verificar que el encabezado mantiene el número de página dinámico.
- [ ] Validar que las imágenes insertadas respetan el ancho máximo (máx. `5.6 in` para márgenes de 1 pulgada).
