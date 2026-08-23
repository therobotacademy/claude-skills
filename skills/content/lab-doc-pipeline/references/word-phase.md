# Fase Word — Documento de estudio

Referencia completa para producir el Word (.docx) del lab.
Leer este archivo antes de escribir una sola línea de JavaScript.

---

## 1 · Stack técnico

```
matplotlib (Python)   → PNGs de gráficos de datos
cairosvg  (Python)   → SVGs de diagramas → PNGs
docx-js   (Node.js)  → ensamblado del .docx final
```

**Dependencias** (instalar si no están):

```bash
pip install matplotlib numpy scipy cairosvg --break-system-packages -q
npm install docx
```

---

## 2 · Secuencia de producción

```
1. Generar PNGs matplotlib  →  /home/claude/lab{N}_imgs/fig*.png
2. Generar SVGs de diagramas →  /home/claude/lab{N}_imgs/diag*.svg
3. Convertir SVGs a PNG via cairosvg
4. Ejecutar build_doc.js    →  /mnt/user-data/outputs/LAB{N}_estudio_*.docx
5. Verificar integridad ZIP
```

Nunca saltarse el paso de verificación. Un .docx corrompido no abre en Word.

---

## 3 · Configuración de página

```javascript
// A4 con márgenes 2.5 cm
const PAGE   = { width: 11906, height: 16838 };   // DXA
const MARGIN = { top: 1417, right: 1417, bottom: 1417, left: 1417 };
const CW     = 9072;  // content width = 11906 - 2×1417
```

**Recordatorio de unidades**: 1 pulgada = 1440 DXA. 1 cm ≈ 567 DXA.

---

## 4 · Paleta de colores estándar

```javascript
const COL = {
  blue:    '2E75B6', blue_l:  'EBF4FF', blue_m:  'B5D4F4',
  purple:  '534AB7', purple_l:'EEEDFE',
  green:   '1A7A4A', green_l: 'E1F5EE',
  amber:   'D4830A', amber_l: 'FAEEDA',
  red:     'C0392B', red_l:   'FFF5F5',
  teal:    '0F6E56', teal_l:  'E1F5EE',
  gray:    '5A6275', gray_l:  'F5F7FA', gray_ll: 'FAFBFC',
  dark:    '1C2A3A', mid:     '3D4F63', light:   '8898AA',
  white:   'FFFFFF', border:  'CBD2DC', border2: 'E0E4EA',
};
```

Semántica de colores:
- **blue** → información, hiperparámetros bien identificados, elementos principales
- **purple** → conceptos bayesianos, priors, elementos probabilísticos
- **green** → soluciones correctas, convergencia, resultados positivos
- **amber** → advertencias, trade-offs, elementos que dependen del prior
- **red** → errores, no convergencia, problemas críticos
- **teal** → elementos deterministas, derivados, computación

---

## 5 · Helpers JavaScript reutilizables

### 5a · Helpers de texto

```javascript
const run      = (t, o={}) => new TextRun({ text:t, font:'Arial', size:22, ...o });
const runMono  = (t, o={}) => new TextRun({ text:t, font:'Courier New', size:19, ...o });
const bold     = (t, c=COL.dark) => run(t, { bold:true, color:c });
const italic   = (t) => run(t, { italics:true });
const colored  = (t, c, b=false) => run(t, { color:c, bold:b });
```

### 5b · Párrafo con alineación

```javascript
function para(children, opts={}) {
  const { align='left', before=80, after=80 } = opts;
  const amap = { left: AlignmentType.LEFT, center: AlignmentType.CENTER,
                 right: AlignmentType.RIGHT, justify: AlignmentType.BOTH };
  return new Paragraph({
    alignment: amap[align],
    spacing: { before, after },
    children: Array.isArray(children) ? children : [children],
  });
}
```

### 5c · Headings

```javascript
function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 160 },
    children: [new TextRun({ text, font:'Arial', size:30, bold:true, color:COL.blue })]
  });
}
function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 260, after: 120 },
    children: [new TextRun({ text, font:'Arial', size:24, bold:true, color:COL.dark })]
  });
}
function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text, font:'Arial', size:21, bold:true, color:COL.mid })]
  });
}
```

**CRÍTICO**: usar siempre `heading: HeadingLevel.HEADING_N` para que el
TOC automático funcione. Los `outlineLevel` deben estar en los estilos
del documento.

### 5d · Imagen embebida

```javascript
function imgPara(name, widthPx, heightPx, caption, altText='') {
  const data = fs.readFileSync(`${IMGS_DIR}/${name}`);
  const content = [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 60 },
      children: [new ImageRun({
        type: 'png', data,
        transformation: { width: widthPx, height: heightPx },
        altText: { title: altText, description: altText, name: altText }
      })]
    }),
  ];
  if (caption) content.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 140 },
    children: [new TextRun({ text: caption, font:'Arial', size:18, italics:true, color:COL.light })]
  }));
  return content;
}
```

**Dimensiones de imagen recomendadas** para A4 con márgenes 2.5cm:
- Figura ancha (gráfico temporal, shrinkage): `widthPx: 575, heightPx: 230`
- Figura cuadrada (diagrama DAG): `widthPx: 560, heightPx: 315`
- Figura alta (traceplots 3 paneles): `widthPx: 575, heightPx: 340`
- Figura comparativa (3 columnas): `widthPx: 575, heightPx: 280`
- Figura de densidades: `widthPx: 575, heightPx: 255`

### 5e · Tabla de datos con encabezado coloreado

```javascript
function dataTable(headers, rows, colWidths) {
  return new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      // Header row
      new TableRow({ children: headers.map((h, i) =>
        new TableCell({
          width: { size: colWidths[i], type: WidthType.DXA },
          shading: { fill: COL.blue_l, type: ShadingType.CLEAR },
          borders: allBorders(COL.blue_m),
          margins: { top:80, bottom:80, left:120, right:120 },
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text:h, font:'Arial', size:19, bold:true, color:COL.blue })]
          })]
        })
      )}),
      // Data rows (alternating background)
      ...rows.map((row, ri) => new TableRow({
        children: row.map((cell_text, ci) =>
          new TableCell({
            width: { size: colWidths[ci], type: WidthType.DXA },
            shading: { fill: ri%2===0 ? COL.white : COL.gray_ll, type: ShadingType.CLEAR },
            borders: allBorders(COL.border2, 3),
            margins: { top:72, bottom:72, left:120, right:120 },
            children: [new Paragraph({
              children: [new TextRun({ text: String(cell_text), font:'Arial', size:20 })]
            })]
          })
        )
      }))
    ]
  });
}
```

**CRÍTICO**: `columnWidths` deben sumar exactamente `CW = 9072`.
Usar `WidthType.DXA` siempre (no PERCENTAGE — rompe en Google Docs).

### 5f · Caja de color (infobox)

```javascript
function colorBox(label, bodyRuns, accentColor, bgColor) {
  return new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: [200, CW - 200],
    rows: [new TableRow({ children: [
      new TableCell({  // Etiqueta lateral coloreada
        width: { size: 200, type: WidthType.DXA },
        shading: { fill: accentColor, type: ShadingType.CLEAR },
        borders: noBorders(),
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text:label, font:'Arial', size:17, bold:true, color:'FFFFFF' })]
        })]
      }),
      new TableCell({  // Cuerpo del mensaje
        width: { size: CW-200, type: WidthType.DXA },
        shading: { fill: bgColor, type: ShadingType.CLEAR },
        borders: noBorders(),
        children: [new Paragraph({ children: bodyRuns })]
      }),
    ]})]
  });
}
```

Uso típico:
```javascript
colorBox('NOTA', [bold('Texto clave: '), run('explicación...')], COL.blue, COL.blue_l)
colorBox('AVISO', [...], COL.amber, COL.amber_l)
colorBox('LECCIÓN', [...], COL.purple, COL.purple_l)
colorBox('PROBLEMA', [...], COL.red, COL.red_l)
colorBox('SOLUCIÓN', [...], COL.green, COL.green_l)
```

---

## 6 · Generación de PNGs con matplotlib

### 6a · Configuración estándar

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = '/home/claude/lab{N}_imgs'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.facecolor': '#FAFBFC', 'figure.facecolor': 'white',
    'axes.grid': True, 'grid.alpha': 0.35, 'grid.color': '#C8CDD6',
    'grid.linewidth': 0.5,
    'axes.labelsize': 10, 'axes.titlesize': 11,
    'xtick.labelsize': 9, 'ytick.labelsize': 9,
})

C_BLUE  = '#2E75B6'
C_RED   = '#C0392B'
C_AMBER = '#D4830A'
C_GREEN = '#1A7A4A'
C_GRAY  = '#5A6275'
```

### 6b · Guardar con resolución correcta

```python
plt.savefig(f'{OUT}/fig{N}_{nombre}.png', dpi=160, bbox_inches='tight')
plt.close()
```

`dpi=160` produce imágenes nítidas en Word sin exceder el tamaño del documento.

### 6c · Figuras estándar por tipo de lab

**Serie temporal con IC** (aplica a bayesiano, estadística):
```python
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.errorbar(x, medias, yerr=[medias-ic_lo, ic_hi-medias],
            fmt='o-', elinewidth=1.8, capsize=4)
ax.scatter(x, y_obs, marker='x', color=C_RED, s=60)
ax.axhline(mu_hat, linestyle='--', color=C_AMBER)
```

**Comparativa de K valores de parámetro** (para sustituir sliders):
```python
fig, axes = plt.subplots(1, K, figsize=(4*K+1, 4), sharey=True)
for ax, val in zip(axes, param_vals):
    # graficar versión del modelo con ese valor del parámetro
```

**Traceplots MCMC** (3 cadenas, M parámetros):
```python
fig, axes = plt.subplots(M, 1, figsize=(11, 2.5*M), sharex=True)
chain_colors = ['#2E75B6', '#D4830A', '#1A7A4A']
for ax, (name, mean, sd) in zip(axes, params):
    for ci, col in enumerate(chain_colors):
        chain = simulate_convergent_chain(mean, sd, N_ITER, seed=ci*7)
        ax.plot(chain, color=col, linewidth=0.9, alpha=0.82)
```

**Densidades superpuestas** (16 lambdas, K clases, etc.):
```python
cmap = plt.cm.plasma
for i, (mu_i, col) in enumerate(zip(mus, [cmap(i/N) for i in range(N)])):
    x = np.linspace(mu_i - 4*sd, mu_i + 4*sd, 300)
    ax.plot(x, norm.pdf(x, mu_i, sd), color=col, linewidth=1.4, alpha=0.75)
```

---

## 7 · Generación de SVGs de diagramas

Los diagramas conceptuales se escriben como SVG y se convierten a PNG:

```python
import cairosvg

svg_content = '''<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 680 H" width="680" height="H">
  <rect width="680" height="H" fill="white"/>
  ...
</svg>'''

with open(f'{OUT}/diag_{nombre}.svg', 'w') as f:
    f.write(svg_content)

cairosvg.svg2png(
    url=f'{OUT}/diag_{nombre}.svg',
    write_to=f'{OUT}/diag_{nombre}.png',
    output_width=900
)
```

### Diagramas canónicos por tipo de lab

**DAG del modelo jerárquico** (bayesiano):
- 3 niveles verticales con línea divisoria entre cada nivel
- Colores por rol: purple=hiperpriors, teal=derivados, blue=prior jerárquico, amber=datos
- Borde discontinuo para nodos deterministas (`<-`)
- Leyenda al pie con los 4 tipos de nodo

**Fases MCMC / fases de entrenamiento ML**:
- Flowchart vertical: 4 cajas apiladas con flechas entre ellas
- Colores por fase: blue=compilar, amber=adaptar, red=burn-in, purple=muestrear
- Anotaciones laterales con parámetros concretos (n.chains, n.iter, etc.)

**Código anotado** (JAGS, sklearn pipeline, etc.):
- Contenedor azul principal con el bloque completo
- Sub-bloques de color por nivel o función
- Badges de color sólido para badges de rol (estocástico/determinista)
- Anotaciones en columna derecha conectadas con líneas punteadas

---

## 8 · Estructura del Document en docx-js

```javascript
const doc = new Document({
  numbering: { config: [{ reference:'bullets', levels:[{
    level:0, format:LevelFormat.BULLET, text:'•',
    alignment:AlignmentType.LEFT,
    style:{ paragraph:{ indent:{ left:720, hanging:360 } } }
  }] }] },
  styles: {
    default: { document: { run: { font:'Arial', size:22 } } },
    paragraphStyles: [
      { id:'Heading1', name:'Heading 1', basedOn:'Normal', next:'Normal',
        run:{ size:30, bold:true, font:'Arial', color:COL.blue },
        paragraph:{ spacing:{ before:360, after:160 }, outlineLevel:0 } },
      { id:'Heading2', name:'Heading 2', basedOn:'Normal', next:'Normal',
        run:{ size:24, bold:true, font:'Arial', color:COL.dark },
        paragraph:{ spacing:{ before:260, after:120 }, outlineLevel:1 } },
      { id:'Heading3', name:'Heading 3', basedOn:'Normal', next:'Normal',
        run:{ size:21, bold:true, font:'Arial', color:COL.mid },
        paragraph:{ spacing:{ before:200, after:80 }, outlineLevel:2 } },
    ]
  },
  sections: [{
    properties: { page: { size: PAGE, margin: MARGIN } },
    headers: { default: headerContent },
    footers: { default: footerContent },
    children: [ ...portada, ...toc, ...s0, ...s1, ...s2, ..., ...appendix ]
  }]
});
```

### Cabecera estándar

```javascript
new Header({ children: [new Paragraph({
  border: { bottom: { style:BorderStyle.SINGLE, size:6, color:COL.blue, space:1 } },
  children: [
    new TextRun({ text:'Asignatura · código · institución', font:'Arial', size:17, color:COL.light }),
    new TextRun({ text:'\t', font:'Arial', size:17 }),
    new TextRun({ text:'LAB N — Título del lab', font:'Arial', size:17, color:COL.mid }),
  ],
  tabStops:[{ type:'right', position: CW }],
})] })
```

### Pie estándar

```javascript
new Footer({ children: [new Paragraph({
  border: { top: { style:BorderStyle.SINGLE, size:4, color:COL.border, space:1 } },
  spacing: { before:60, after:0 },
  children: [
    new TextRun({ text:'Documento de estudio autocontenido', font:'Arial', size:16, color:COL.light }),
    new TextRun({ text:'\t', font:'Arial', size:16 }),
    new TextRun({ text:'Página ', font:'Arial', size:16, color:COL.mid }),
    new TextRun({ children:[PageNumber.CURRENT], font:'Arial', size:16, color:COL.mid }),
    new TextRun({ text:' de ', font:'Arial', size:16, color:COL.mid }),
    new TextRun({ children:[PageNumber.TOTAL_PAGES], font:'Arial', size:16, color:COL.mid }),
  ],
  tabStops:[{ type:'right', position: CW }],
})] })
```

---

## 9 · Verificación de integridad

```python
import zipfile, os

f = '/mnt/user-data/outputs/LAB{N}_estudio_*.docx'
size = os.path.getsize(f)
with zipfile.ZipFile(f) as z:
    names = z.namelist()

print(f'Size: {size/1024:.0f} KB')
print(f'Media files: {len([n for n in names if "media" in n])}')
print('Core OK:', all(x in names for x in [
    'word/document.xml', '[Content_Types].xml', 'word/_rels/document.xml.rels'
]))
```

El número de archivos de media debe coincidir con el número de imágenes
embebidas. Si hay 11 PNGs, debe haber 11 entradas en media/.

---

## 10 · Errores frecuentes a evitar

1. **`WidthType.PERCENTAGE` en tablas** → columnas desalineadas en Google Docs
2. **`ShadingType.SOLID`** → fondo negro en celdas con color
3. **ImageRun sin `type`** → documento corrupto que no abre
4. **PageBreak fuera de Paragraph** → XML inválido
5. **Bullets con carácter unicode (`•`)** → usar `LevelFormat.BULLET`
6. **Sumar mal los columnWidths** → tabla que desborda el margen
7. **outlineLevel omitido en estilos** → TOC vacío
8. **`\n` dentro de TextRun** → usar Paragraph separados
9. **Imágenes demasiado grandes (>700px width)** → usar máx 575px para caber en A4
10. **Olvidar `bbox_inches='tight'` en matplotlib** → recorte de labels

---

## 11 · Figuras adicionales para el Word teórico (Fase 3)

El Word teórico necesita figuras que explican *mecanismos*, no resultados.
Distintas a las figuras del Word de estudio (que muestran los datos del lab).

### Tipos de figura para el Word teórico

**Fig "por qué la técnica"**: dos paneles comparativos.
Izquierda: el caso simple/analítico (buen aspecto, solución cerrada).
Derecha: el caso complejo/intratable (cresta, superficie difícil).
```python
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), facecolor=BG)
# Panel izquierdo: posterior analítica limpia
# Panel derecho: superficie con cresta o región compleja
```

**Fig "ciclo del algoritmo"**: diagrama de cajas y flechas sobre matplotlib.
No usar SVG para esto — el layout de cajas con flechas curvas funciona mejor
en matplotlib con `mpatches.FancyBboxPatch` y `ax.annotate`.
```python
fig, ax = plt.subplots(figsize=(10, 4.6), facecolor=BG)
ax.axis('off')
# Cajas con FancyBboxPatch, flechas con annotate arrowstyle
```

**Fig "convergencia comparativa"**: dos paneles verticales sharex=False.
Panel superior: buena convergencia (3 cadenas mezcladas).
Panel inferior: no convergencia (3 cadenas separadas, con fill_betweenx).
```python
fig, axes = plt.subplots(2, 1, figsize=(11, 5.8), facecolor=BG, sharex=False)
```

**Fig "diagnóstico R̂"**: dos paneles horizontales.
Izquierda: varianza entre cadenas ≈ dentro → R̂≈1.
Derecha: varianza entre cadenas >> dentro → R̂≫1.
Incluir anotación de texto con la fórmula y los valores.

**Fig "problema técnico central"**: dos paneles con contourf.
Izquierda: espacio problemático (cresta, over-parametrized, etc.).
Derecha: espacio solucionado (reparametrizado, regularizado, etc.).
Usar `plt.cm.Blues` izquierda, `plt.cm.Greens` derecha.

**Fig "comparativa de variantes"**: 3 paneles horizontales sharey=True.
Un panel por variante (Gibbs/MH/Slice, SGD/Adam/RMSprop, OLS/GLS/WLS).
Mismo dataset/distribución objetivo en los tres.

### Regla de paleta para el Word teórico

Misma paleta que el Word de estudio:
```python
C_BLUE  = '#2E75B6'   # información principal, hiperparámetros bien identificados
C_RED   = '#C0392B'   # errores, no convergencia, problemas
C_AMBER = '#D4830A'   # advertencias, trade-offs
C_GREEN = '#1A7A4A'   # soluciones, convergencia, resultados correctos
C_GRAY  = '#5A6275'   # neutros, referencia
```

Fondo `white` (no crema) para el Word teórico — diferente del PPTX.
```python
plt.rcParams.update({'figure.facecolor': 'white', 'axes.facecolor': '#FAFBFC'})
```

---

## 12 · Diagramas SVG para el Word teórico

Los diagramas del Word teórico son más conceptuales que los del Word de
estudio. Estructura SVG estándar:

```python
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 680 H" width="680" height="H">
<rect width="680" height="H" fill="white"/>
...
</svg>'''
```

**Paleta SVG para el Word teórico**:
- Nodos estocásticos: `fill="#E6F1FB" stroke="#185FA5"` (azul claro)
- Nodos deterministas: `fill="#E1F5EE" stroke="#0F6E56" stroke-dasharray="6 3"` (verde claro discontinuo)
- Datos observados: `fill="#2C3E50" stroke="#1C2A3A"` (oscuro relleno)
- Hiperpriors: `fill="#EEEDFE" stroke="#534AB7"` (púrpura claro)
- Anotaciones/cajas laterales: `fill="#F8F9FB" stroke="#CBD2DC"` (gris muy suave)

**Marcador de flecha estándar**:
```svg
<marker id="a" viewBox="0 0 10 10" refX="8" refY="5"
        markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M2 1L8 5L2 9" fill="none" stroke="#555"
        stroke-width="1.5" stroke-linecap="round"/>
</marker>
```

**Etiquetas de nivel** (para DAG multi-nivel):
```svg
<text x="340" y="66" text-anchor="middle"
      font-family="Arial" font-size="10" fill="#AAA"
      letter-spacing="2">NIVEL N — NOMBRE</text>
<line x1="40" y1="72" x2="640" y2="72"
      stroke="#E0E3EA" stroke-width="0.8" stroke-dasharray="4 3"/>
```
