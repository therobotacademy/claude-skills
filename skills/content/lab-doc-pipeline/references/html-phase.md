# Fase HTML — Interactivo para clase

Referencia completa para producir el HTML interactivo del lab.
Leer este archivo antes de escribir una sola línea de HTML.

---

## 1 · Arquitectura del archivo

```
LAB{N}_{asignatura}_{tema}_interactivo.html
│
├── <head>          Google Fonts + Chart.js CDN
├── <style>         Design system completo (CSS variables, componentes)
├── <nav>           Barra sticky con tabs numeradas
├── <section#sec0>  §0 visible por defecto
├── <section#sec1>  Oculta hasta activación
│   …
└── <script>        Datos constantes + lógica de todas las secciones
```

**Una sola página HTML autocontenida**. Sin iframes, sin módulos ES6,
sin build step. Todo funciona con `<script src="CDN">` + `<script>` plano.

---

## 2 · CDN permitidos (solo estos, CSP del sandbox)

```html
<!-- Chart.js — gráficos -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>

<!-- Google Fonts — tipografía -->
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

No usar unpkg, esm.sh ni otros CDN para el HTML del lab.

---

## 3 · Design system (CSS variables)

```css
:root {
  --bg:     #0f1117;   /* fondo principal */
  --bg2:    #161b27;   /* cards */
  --bg3:    #1e2535;   /* card secundaria */
  --bg4:    #252d42;   /* inputs, tracks */
  --border: rgba(100,120,180,0.18);
  --text:   #e8ecf4;   /* texto primario */
  --text2:  #9ba8c0;   /* texto secundario */
  --text3:  #6b7a96;   /* texto terciario / labels */
  --blue:   #4f8ef7;
  --blue2:  #7aaff9;
  --red:    #f76f6f;
  --green:  #4dbb8a;
  --amber:  #f0b44a;
  --purple: #a07cf5;
  --teal:   #38c9c0;
  --mono:   'IBM Plex Mono', monospace;
  --serif:  'DM Serif Display', serif;
  --sans:   'Inter', sans-serif;
}
```

**Tipografía**: `DM Serif Display` para títulos de sección, `Inter` para
cuerpo y UI, `IBM Plex Mono` para código y valores numéricos.

---

## 4 · Componentes reutilizables

### 4a · Nav bar sticky

```html
<nav class="nav">
  <div class="nav-logo">Lab<span>·</span>N</div>
  <div class="nav-tab active" onclick="showSection(0,this)">§0 Nombre</div>
  <div class="nav-tab" onclick="showSection(1,this)">§1 Nombre</div>
  ...
</nav>
```

```css
.nav { position: sticky; top: 0; z-index: 100;
       background: rgba(15,17,23,0.92); backdrop-filter: blur(12px);
       border-bottom: 1px solid var(--border); padding: 0 2rem;
       display: flex; align-items: center; overflow-x: auto; }
.nav-tab { padding: 0.9rem 1rem; font-size: 13px; font-weight: 500;
           color: var(--text3); cursor: pointer;
           border-bottom: 2px solid transparent; white-space: nowrap; }
.nav-tab.active { color: var(--blue2); border-bottom-color: var(--blue); }
```

```javascript
function showSection(i, el) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('visible'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('sec' + i).classList.add('visible');
  el.classList.add('active');
  // Lazy-init de gráficos pesados:
  if (i === 4) buildTraceplots();
  if (i === 5) buildDensCharts();
}
```

### 4b · Metric chips (KPIs)

```html
<div class="metrics">
  <div class="metric">
    <div class="metric-label">ETIQUETA</div>
    <div class="metric-value c-blue">valor</div>
    <div class="metric-sub">descripción</div>
  </div>
</div>
```

### 4c · Slider interactivo

```html
<div class="slider-row">
  <label>Nombre parámetro</label>
  <input type="range" min="0" max="10" step="0.1" value="1"
         id="mySlider" oninput="updateChart(this.value)">
  <span class="slider-val" id="myVal">1.0</span>
</div>
```

### 4d · Caja informativa (infobox)

```html
<!-- Tipos: infobox, infobox warn, infobox success, infobox purple -->
<div class="infobox warn">
  <div class="infobox-label">TÍTULO</div>
  Cuerpo del mensaje...
</div>
```

### 4e · Código coloreado

```html
<div class="code-block">
  <span class="kw">model</span> {
    y[i] <span class="stoc">~</span> <span class="fn">dpois</span>(lam[i])
    alpha <span class="det">&lt;-</span> <span class="fn">pow</span>(mu, 2) / ...
    <span class="cm"># comentario</span>
  }
</div>
```

Clases de coloreado:
- `.kw` → `var(--purple)` — keywords (model, for, in)
- `.fn` → `var(--blue2)` — funciones (dpois, dgamma, pow)
- `.stoc` → `var(--red)` — operador estocástico (~)
- `.det` → `var(--teal)` — operador determinista (<-)
- `.str` → `var(--green)` — strings
- `.cm` → `var(--text3)` — comentarios

### 4f · Tabla de datos

```html
<table class="tbl">
  <thead><tr><th>Col A</th><th>Col B</th></tr></thead>
  <tbody id="myTbody"></tbody>
</table>
```

```javascript
// Construir filas dinámicamente
data.forEach((row, i) => {
  tbody.innerHTML += `<tr>
    <td class="year-col">${row.year}</td>
    <td class="c-blue">${row.val.toFixed(2)}</td>
  </tr>`;
});
```

### 4g · Chart.js — configuración estándar

```javascript
const C_BLUE = '#4f8ef7', C_RED = '#f76f6f',
      C_AMBER = '#f0b44a', C_GREEN = '#4dbb8a';
const C_GRID = 'rgba(255,255,255,0.07)';
const FONT = "'Inter', sans-serif";

new Chart(ctx, {
  type: 'bar',  // o 'line', 'scatter'
  data: { labels, datasets: [{ ... }] },
  options: {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { ticks: { color: 'rgba(255,255,255,0.4)', font: { family: FONT, size: 11 } },
           grid: { color: C_GRID } },
      y: { ticks: { color: 'rgba(255,255,255,0.4)', font: { family: FONT, size: 11 } },
           grid: { color: C_GRID } }
    }
  }
});
```

**Regla**: siempre `maintainAspectRatio: false` + wrapper div con altura
explícita. Nunca poner altura en el canvas directamente.

---

## 5 · Patrón de inicialización lazy

Los gráficos pesados se inicializan solo cuando el usuario activa su tab,
no al cargar la página. Usar un flag en el canvas:

```javascript
function buildDensCharts() {
  if (nav('densChart')._built) return;
  nav('densChart')._built = true;
  // ... inicializar Chart.js aquí
}
```

Llamar `buildDensCharts()` desde `showSection()` cuando `i === N`.

---

## 6 · Adaptación por tipo de lab

### Lab Bayesiano (MCMC, JAGS/Stan)

Secciones específicas a incluir:
- Selector de modelo (sin jerarquía / independientes / jerárquico)
- Slider del parámetro de dispersión (σ, τ, etc.) con actualización live
- Traceplots con 3 cadenas simuladas (o reales si disponibles)
- Panel R̂ con gauges de color (verde/amarillo/rojo)
- Barras ESS con umbral 400 marcado
- Densidades posteriores superpuestas

### Lab Machine Learning (sklearn, clasificación/regresión)

Secciones específicas a incluir:
- Selector de hiperparámetro (C, alpha, n_estimators, etc.) con actualización live
- Gráficos train vs test (curvas de aprendizaje, overfitting)
- Matrices de confusión coloreadas
- Curva ROC o precision-recall
- Importancia de features (barras horizontales)
- Comparativa de modelos en tabla

### Lab Estadística frecuentista (regresión, test de hipótesis)

Secciones específicas a incluir:
- Scatter del dataset con línea de regresión
- Slider de confianza (90%, 95%, 99%) que actualiza IC
- Tabla ANOVA o de coeficientes
- Gráficos de residuos (QQ-plot aproximado, residuos vs fitted)
- Interpretación de p-valores con contexto

---

## 7 · Errores frecuentes a evitar

1. **No leer el notebook antes de empezar** → valores numéricos incorrectos
2. **Hardcodear colores fuera de las variables CSS** → inconsistencia visual
3. **Inicializar todos los gráficos al cargar** → lentitud en el primer render
4. **Olvidar `maintainAspectRatio: false`** → chart desproporcionado
5. **Usar `position: fixed`** → el iframe colapsa a min-height
6. **Poner `display:none` en secciones durante streaming** → contenido invisible
7. **No diferenciar visualmente `~` de `<-` en código JAGS** → pérdida pedagógica clave
8. **Slider sin step explícito** → valores decimales sucios en el label
