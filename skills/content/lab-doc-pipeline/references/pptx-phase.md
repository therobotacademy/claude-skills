# Fase PPTX — Presentación de clase

Referencia completa para producir el PPTX del lab.
Leer este archivo antes de escribir una sola línea de JavaScript.

Consolidado a partir de la producción de LAB2_teoria_DAG_JAGS_MCMC.pptx
(32 diapositivas, mayo 2026).

---

## 1 · Stack técnico y setup

```bash
npm install -g pptxgenjs
# cairosvg y matplotlib ya instalados desde fases anteriores
```

```javascript
const pptxgen = require('pptxgenjs');
const fs = require('fs');

const pres = new pptxgen();
pres.layout  = 'LAYOUT_16x9';   // 10" × 5.625"
pres.author  = 'Bernardo Ronquillo Japón';
pres.title   = 'Título del lab';
pres.subject = 'Asignatura · UNIPRO';
```

Dimensiones de referencia: `W = 10`, `H = 5.625` (pulgadas).

---

## 2 · Paleta COIIAOC v1.1 — tokens para pptxgenjs

```javascript
const C = {
  azul:     '1E3A5F',   // azul-institucion — portadas, cabeceras, barras sección
  naranja:  'FF8C3B',   // naranja-luminoso — SOLO sobre azul
  naranjao: 'C2510A',   // naranja-oscuro   — SOLO sobre crema/blanco
  crema:    'FAFAF7',   // crema-tecnico    — fondo slides contenido
  teal:     '0D7C5A',   // outputs/teal     — sidebar secciones §2-3
  inputs:   '2E6B9E',   // inputs           — sidebar secciones §1, §4-5
  excepc:   'B91C1C',   // excepciones      — errores, no convergencia
  reglas:   'B45309',   // reglas           — advertencias
  texto:    '1C1C1C',
  sub:      '6B6B6B',
  dim:      '9B9B9B',
  borde:    'E8E3D8',
  blanco:   'FFFFFF',
  bgSoft:   'EFF3F8',   // fila alternada tabla
  bgTeal:   'E8F7F2',   // fondo caja teal
  bgRed:    'FDECEA',   // fondo caja red
};
```

**Regla crítica de contraste**:
- `naranja FF8C3B` → SOLO sobre `azul 1E3A5F` (ratio 4.97:1 ✅)
- `naranjao C2510A` → SOLO sobre `crema FAFAF7` o blanco (ratio 7.3:1 ✅)
- `C2510A` sobre `1E3A5F` → **PROHIBIDO** (ratio 2.45:1 ❌)

---

## 3 · Tipografía

```javascript
const F = {
  titulo: 'Syne',          // H1, títulos de sección, números grandes
  mono:   'IBM Plex Mono', // código, valores numéricos, badges
  cuerpo: 'IBM Plex Sans', // bullets, tablas, captions, cuerpo
};
```

| Elemento | Font | Size (pt) | Color |
|---|---|---|---|
| Título portada L1 | Syne | 38–40 | FFFFFF |
| Título portada L2 | Syne | 28–30 | FF8C3B |
| Número de sección | Syne | 64 | FF8C3B |
| Título slide contenido | Syne | 22–26 bold | 1E3A5F |
| Subtítulo sección | Syne/Cuerpo | 14–15 italic | FF8C3B |
| Bullets / cuerpo | IBM Plex Sans | 13–14 | 1C1C1C |
| Código inline | IBM Plex Mono | 11–12 | 1C1C1C |
| Caption / nota | IBM Plex Sans | 9–10 italic | 6B6B6B |
| Núm. de página | IBM Plex Mono | 9 | 9B9B9B |

---

## 4 · Los cuatro layouts — usar solo estos

### Layout 1: Portada

```javascript
const s = pres.addSlide();
s.background = {color: C.azul};
// Franja naranja izquierda
s.addShape(pres.shapes.RECTANGLE,{x:0,y:0,w:0.36,h:H,
  fill:{color:C.naranja},line:{color:C.naranja,width:0}});
// Kicker (asignatura)
s.addText('NOMBRE ASIGNATURA',{x:0.52,y:0.32,w:W-0.7,h:0.38,
  fontSize:10,fontFace:F.mono,color:C.naranja,bold:true,charSpacing:3});
// Título L1
s.addText('Título principal',{x:0.52,y:0.72,w:W-0.7,h:0.85,
  fontSize:38,fontFace:F.titulo,bold:true,color:C.blanco});
// Título L2 / subtítulo
s.addText('Subtítulo o tema',{x:0.52,y:1.55,w:W-0.7,h:0.65,
  fontSize:28,fontFace:F.titulo,bold:true,color:C.naranja});
// Copyright
s.addText('© 2025 Bernardo Ronquillo Japón · asignatura · UNIPRO',{
  x:0.52,y:H-0.28,w:W-0.7,h:0.22,fontSize:8.5,fontFace:F.mono,color:C.dim});
addFooter(s, 1);
```

### Layout 2: Sección

```javascript
function sectionSlide(num, secNum, title, subtitle='') {
  const s = pres.addSlide();
  s.background = {color: C.azul};
  s.addShape(pres.shapes.RECTANGLE,{x:0,y:0,w:0.28,h:H,
    fill:{color:C.naranja},line:{color:C.naranja,width:0}});
  s.addText(`§${secNum}`,{x:0.38,y:0.9,w:1.2,h:1.2,
    fontSize:64,fontFace:F.titulo,bold:true,color:C.naranja,align:'left',valign:'middle'});
  s.addText(title,{x:0.38,y:2.0,w:W-0.6,h:1.1,
    fontSize:34,fontFace:F.titulo,bold:true,color:C.blanco,valign:'middle'});
  if(subtitle) s.addText(subtitle,{x:0.38,y:3.1,w:W-0.6,h:0.6,
    fontSize:15,fontFace:F.cuerpo,color:C.naranja,italic:true});
  addFooter(s, num);
  return s;
}
```

### Layout 3: Contenido (el más frecuente)

Fondo crema + barra lateral izquierda de color semántico + título + cuerpo.

```javascript
function addSidebar(slide, color=C.teal) {
  slide.addShape(pres.shapes.RECTANGLE,{
    x:0,y:0,w:0.12,h:H,fill:{color},line:{color,width:0}
  });
}
// Uso:
const s = pres.addSlide();
s.background = {color: C.crema};
addSidebar(s, C.inputs);   // azul inputs para §1, §4-5
// o addSidebar(s, C.teal)  para §2-3
// o addSidebar(s, C.naranjao) para §3 (BUGS)
addTitle(s, 'Título del slide');
// ... bullets, tablas, código
```

**Asignación de colores de sidebar por sección**:
- `C.inputs` (azul `2E6B9E`): §1 por qué MCMC, §4 algoritmo, §5 samplers
- `C.teal` (verde `0D7C5A`): §2 DAG, §3 placa, §6 diagnóstico
- `C.naranjao` (naranja `C2510A`): §3 BUGS (especificación del modelo)
- `C.azul` (navy `1E3A5F`): síntesis, slides de cierre

### Layout 4: Figura full

Título en 22pt (no más — wrappea en LibreOffice), imagen ocupa 85%.

```javascript
// CRÍTICO: fontSize 22 máximo para títulos en figura-full
// Si el título tiene más de ~55 caracteres, acortarlo
function addTitle(slide, text, color=C.azul, fontSize=26) {
  slide.addText(text, {
    x:0.22, y:0.18, w:W-0.4, h:0.62,
    fontSize, fontFace:F.titulo, bold:true, color,
    valign:'middle'
  });
}
// Para layout figura-full: siempre pasar fontSize=22
addTitle(s, 'Título corto del slide', C.azul, 22);
s.addImage({data: imgData('fig_nombre.png'),
  x:0.22, y:0.76, w:W-0.44, h:H-0.99,
  altText:'Descripción accesible'});
```

---

## 5 · Helpers reutilizables

### Footer estándar

```javascript
function addFooter(slide, num, total=32) {
  slide.addText(`${num} / ${total}`, {
    x:W-0.7, y:H-0.28, w:0.6, h:0.22,
    fontSize:9, fontFace:F.mono, color:C.dim, align:'right'
  });
  slide.addText('© 2025 Bernardo Ronquillo Japón · upbcida17 · UNIPRO', {
    x:0.18, y:H-0.28, w:5, h:0.22,
    fontSize:8.5, fontFace:F.mono, color:C.dim
  });
}
```

### Imagen desde archivo

```javascript
function imgData(name) {
  const buf = fs.readFileSync(`${IMGS_DIR}/${name}`);
  return 'image/png;base64,' + buf.toString('base64');
}
// Uso:
s.addImage({data: imgData('fig1_why_mcmc.png'), x:0.22, y:0.76,
  w:W-0.44, h:H-0.99, altText:'Descripción'});
```

### Lista de bullets

```javascript
function addBullets(slide, items, opts={}) {
  const {x=0.22,y=0.9,w=W-0.44,h=H-1.15,size=14} = opts;
  const runs = items.flatMap((item, i) => {
    const last = i === items.length-1;
    const text = typeof item === 'string' ? item : item.text;
    const color = typeof item === 'object' ? (item.color||C.texto) : C.texto;
    const bold  = typeof item === 'object' ? !!item.bold : false;
    return [{text, options:{bullet:true, breakLine:!last, fontSize:size,
      fontFace:F.cuerpo, color, bold, paraSpaceAfter:4}}];
  });
  slide.addText(runs, {x,y,w,h});
}
```

### Tabla de datos

```javascript
function addTable(slide, headers, rows, colW, opts={}) {
  const {x=0.22, y=0.88} = opts;
  const hRow = headers.map(h=>({
    text:h, options:{fill:{color:C.azul}, color:C.blanco, bold:true,
      fontSize:10.5, fontFace:F.cuerpo, align:'center', valign:'middle',
      margin:[4,6,4,6]}
  }));
  const dRows = rows.map((row,ri)=>row.map((cell)=>({
    text: typeof cell==='object'?cell.text:cell,
    options:{
      fill:{color: ri%2===0?C.crema:C.bgSoft},
      color: typeof cell==='object'?(cell.color||C.texto):C.texto,
      bold: typeof cell==='object'?!!cell.bold:false,
      fontSize:10, fontFace:F.cuerpo, valign:'middle', margin:[3,6,3,6]
    }
  })));
  slide.addTable([hRow,...dRows],{x, y, colW, border:{pt:0.5,color:C.borde}});
}
```

### Caja informativa (infobox)

```javascript
function addInfoBox(slide, label, text, accent, bg, opts={}) {
  const {x=0.22, y=3.5, w=W-0.44, h=0.9} = opts;
  slide.addShape(pres.shapes.RECTANGLE,{x,y,w:0.24,h,
    fill:{color:accent},line:{color:accent,width:0}});
  slide.addShape(pres.shapes.RECTANGLE,{x:x+0.24,y,w:w-0.24,h,
    fill:{color:bg},line:{color:C.borde,width:0.5}});
  slide.addText(label,{x:x+0.02,y:y+0.02,w:0.2,h:h-0.04,
    fontSize:8,fontFace:F.mono,color:C.blanco,bold:true,
    align:'center',valign:'middle',rotate:270});
  slide.addText(text,{x:x+0.32,y:y+0.08,w:w-0.44,h:h-0.16,
    fontSize:12,fontFace:F.cuerpo,color:C.texto,valign:'middle',wrap:true});
}
// Colores por tipo:
// NOTA/INFO:    accent=C.inputs,  bg='EBF3FA'
// ADVERTENCIA:  accent=C.reglas,  bg='FDF3E3'
// LECCIÓN/CLAVE:accent=C.teal,    bg=C.bgTeal
// PROBLEMA:     accent=C.excepc,  bg=C.bgRed
// SOLUCIÓN:     accent=C.teal,    bg=C.bgTeal
```

### Código block

```javascript
function addCode(slide, lines, opts={}) {
  const {x=0.22,y=0.9,w=W-0.44,h=H-1.2} = opts;
  slide.addShape(pres.shapes.RECTANGLE,{x,y,w,h,
    fill:{color:'EDF0F5'},line:{color:C.borde,width:0.5}});
  const runs = lines.flatMap((line,i)=>[
    {text:line, options:{breakLine: i<lines.length-1,
      fontSize:11.5, fontFace:F.mono, color:C.texto}}
  ]);
  slide.addText(runs,{x:x+0.18,y:y+0.12,w:w-0.36,h:h-0.24,valign:'top'});
}
```

---

## 6 · Regenerar figuras matplotlib con paleta COIIAOC

Las figuras para el PPTX se regeneran aunque existan versiones de fondo
blanco de fases anteriores. El fondo crema `#FAFAF7` es la diferencia visual
clave que hace que las imágenes encajen en el slide sin parecen incrustadas.

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Carpeta específica para PPTX
OUT = f'/home/claude/lab{N}_imgs/pptx'
os.makedirs(OUT, exist_ok=True)

BG      = '#FAFAF7'  # crema-tecnico
AZUL    = '#1E3A5F'
NARANJA = '#C2510A'  # naranja-oscuro (sobre crema)
TEAL    = '#0D7C5A'
INPUTS  = '#2E6B9E'
EXCEPC  = '#B91C1C'
REGLAS  = '#B45309'
SUB     = '#6B6B6B'
BORDE   = '#E8E3D8'

plt.rcParams.update({
    'font.family':        'DejaVu Sans',
    'figure.facecolor':   BG,
    'axes.facecolor':     BG,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.edgecolor':     BORDE,
    'axes.grid':          True,
    'grid.alpha':         0.45,
    'grid.color':         BORDE,
    'axes.labelcolor':    AZUL,
    'xtick.color':        SUB,
    'ytick.color':        SUB,
    'axes.titleweight':   'bold',
})

def save(name):
    plt.savefig(f'{OUT}/{name}.png', dpi=160,
                facecolor=BG, edgecolor='none', bbox_inches='tight')
    plt.close()
```

**Copiar los diagramas SVG→PNG** (ya existen de la fase Word):
```python
import shutil
for name in ['diag_dag_basic','diag_dag_plate','diag_pipeline','diag_gibbs']:
    shutil.copy(f'/home/claude/lab{N}_imgs/{name}.png',
                f'/home/claude/lab{N}_imgs/pptx/{name}.png')
```

---

## 7 · Estructura de diapositivas canónica

32 slides para 60–75 min. Adaptar según el contenido del lab.

| Bloque | Slides | Layout | Contenido |
|---|---|---|---|
| Portada | 1 | Portada | Título, chips de 4 secciones |
| §1 Por qué la técnica | 2–6 | Sección + 4×Contenido/Fig | El problema, tabla analítica vs técnica, figura comparativa, intuición |
| §2 El modelo (DAG) | 7–10 | Sección + 3×Contenido | Tipos de nodo, DAG básico, placa/for loop |
| §3 Especificación | 11–14 | Sección + 3×Contenido | Código anotado, tabla ~ vs <-, distribuciones |
| §4 El algoritmo | 15–18 | Sección + 3×Fig/Cont | Monte Carlo, ciclo MH, traceplots |
| §5 Variantes | 19–22 | Sección + 3×Contenido | Sampler 1, comparativa samplers, tabla |
| §6 Diagnóstico | 23–26 | Sección + 3×Fig/Cont | R̂ figura, tabla umbrales+ESS, ESS figura |
| §7 Problema técnico | 27–29 | Sección + 2×Fig/Cont | Figura problema, tabla solución |
| §8 Síntesis | 30–32 | Sección + 2×Cont | Diagrama flujo, tabla correspondencias, cierre |

---

## 8 · Notas del presentador

**Obligatorias** en todas las slides de contenido (no en sección ni portada).

```javascript
s.addNotes('Texto del guión...');
```

Estructura recomendada de cada nota:
1. **Qué señalar** en la figura o tabla (si la hay): "Señalar la cresta roja..."
2. **La conexión al notebook**: "Esto corresponde a la línea update(modelo, 5000)..."
3. **Error frecuente del alumno** (si aplica): "Confunden ~ con <-..."
4. **Frase de cierre** para transición al siguiente slide

No repetir el texto visible en el slide. Las notas son el nivel de
abstracción superior: el por qué y el contexto.

---

## 9 · QA visual — obligatorio antes de entregar

```bash
# 1. Convertir a PDF
python /mnt/skills/public/pptx/scripts/office/soffice.py \
  --headless --convert-to pdf output.pptx

# 2. Convertir PDF a imágenes
rm -f /tmp/slide-*.jpg
pdftoppm -jpeg -r 130 /tmp/output.pdf /tmp/slide

# 3. Inspeccionar las slides críticas:
#    - Portada (slide 1)
#    - Primera slide de contenido (slide 3)
#    - Una slide de figura full (slide 5 aprox.)
#    - Una slide de código (slide 12 aprox.)
#    - Una slide de dos tablas (slide 25 aprox.)
#    - Última slide (slide 32)
```

**Defectos a corregir antes de entregar** (los únicos que importan):
- Título wrappea a 2 líneas y se solapa con la imagen → reducir a 22pt o acortar texto
- Dos tablas se solapan en layout de dos columnas → usar layout izquierda/derecha con x distinto
- Texto overflow en celda de tabla → reducir fontSize o aumentar colW
- Slide en blanco o vacía → el bloque JavaScript lanzó error silencioso

**Parar después de un ciclo fix+verificar** a menos que aparezca un
defecto nuevo visible para el usuario. No iterar sobre posicionamiento de
sub-píxeles.

---

## 10 · Pitfalls críticos pptxgenjs

1. **NUNCA `#` en colores** → corrompe el archivo
   ```javascript
   color: 'FF0000'   // ✅
   color: '#FF0000'  // ❌ CORROMPE
   ```

2. **NUNCA colores de 8 dígitos** → opacity en hex corrompe el archivo
   ```javascript
   fill:{color:'0D7C5A18'}  // ❌ CORROMPE (8 dígitos)
   fill:{color:'E8F7F2'}    // ✅ Usar el color sólido equivalente
   ```

3. **NUNCA reutilizar objetos de opciones** → pptxgenjs los muta
   ```javascript
   const shadow = makeShadow();  // ✅ función que devuelve objeto nuevo
   slide1.addShape(pres.shapes.RECTANGLE, {shadow: makeShadow(), ...});
   slide2.addShape(pres.shapes.RECTANGLE, {shadow: makeShadow(), ...});
   ```

4. **`ROUNDED_RECTANGLE` sin accent overlays** → las esquinas redondeadas
   no quedan cubiertas. Usar `RECTANGLE` cuando se añade una barra lateral.

5. **Bullets: usar `bullet:true`**, nunca `•` unicode
   ```javascript
   {text:'Item', options:{bullet:true, breakLine:true}}  // ✅
   {text:'• Item'}  // ❌ doble bullet
   ```

6. **`paraSpaceAfter` para bullets**, nunca `lineSpacing`
   ```javascript
   {bullet:true, paraSpaceAfter:4}  // ✅
   {bullet:true, lineSpacing:20}    // ❌ gaps excesivos
   ```

---

## 11 · Adaptación por tipo de lab

### Lab Bayesiano MCMC (JAGS/Stan)
Secciones específicas: por qué no analítico → DAG + BUGS → MH cycle →
traceplots → samplers Gibbs/MH/Slice → R̂+ESS → identificabilidad+reparametrización → síntesis.
Sidebar colors: inputs§1 → teal§2 → naranjao§3 → inputs§4-5 → teal§6 → teal§7 → azul§8.

### Lab Machine Learning (sklearn)
Secciones específicas: bias-variance tradeoff → pipeline de datos →
código sklearn anotado → training loop / gradient descent → variantes del
optimizador → curvas de aprendizaje+overfitting → regularización → síntesis.
Cambiar traceplots por loss curves, R̂ por métricas train/val, samplers por
optimizadores (SGD/Adam/RMSprop).

### Lab Estadística frecuentista
Secciones específicas: por qué regresión/ANOVA → modelo lineal → ajuste OLS →
residuos y supuestos → contraste de hipótesis → intervalos de confianza →
comparación de modelos → síntesis.
Cambiar traceplots por gráficos de residuos, R̂ por p-valores, samplers por
estimadores (OLS/GLS/WLS).
