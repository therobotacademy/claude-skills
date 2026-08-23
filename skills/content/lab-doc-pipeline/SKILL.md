---
name: lab-doc-pipeline
description: >
  Pipeline completo de producción de materiales docentes a partir de un
  notebook Jupyter de solución. Genera hasta cuatro artefactos en cadena:

    1. HTML interactivo  — proyección en clase, sliders en tiempo real
    2. Word (.docx)      — documento de estudio autocontenido
    3. Word teórico      — fundamentos conceptuales orientados al notebook
    4. PPTX              — presentación de clase con notas del presentador

  Activa este skill SIEMPRE que el usuario entregue un notebook Jupyter
  (.ipynb) y pida cualquier combinación de: "crea materiales para clase",
  "genera el HTML interactivo", "produce el Word de estudio", "documento
  teórico DAG/MCMC/JAGS", "presentación PPTX", "convierte el notebook en
  material docente", "pipeline completo", o cualquier variante que implique
  transformar un lab resuelto en artefactos de enseñanza.

  Actívalo también cuando el usuario diga "siguiente paso del pipeline",
  "ahora el Word", "ahora el PPTX", "añade la fase de presentación" —
  el pipeline es incremental y cada fase se puede ejecutar independientemente.

  Si solo se pide una fase, ejecuta solo esa. Si se pide "pipeline completo",
  proponer estructura y ejecutar las cuatro fases en secuencia.
license: Proprietary — Bernardo Ronquillo Japón
---

# Lab Doc Pipeline — v2

Pipeline de cuatro fases para transformar un notebook de laboratorio resuelto
en materiales docentes de alta calidad, siguiendo la cadena:

```
Notebook (.ipynb) + teoría (.md)
    │
    ├─ Fase 1 ──▶  HTML interactivo      (clase, proyección)
    ├─ Fase 2 ──▶  Word estudio          (alumno, lectura)
    ├─ Fase 3 ──▶  Word teórico          (fundamentos conceptuales)
    └─ Fase 4 ──▶  PPTX presentación    (clase, 32 slides aprox.)
```

Cada fase es independiente. Se pueden ejecutar todas en secuencia o
cualquier subconjunto según lo que pida el usuario.

---

## 1 · Inputs y jerarquía de fuentes

| Input | Obligatorio | Descripción |
|---|---|---|
| Notebook solución `.ipynb` | ✓ | **Fuente canónica**. Todos los valores numéricos salen de aquí |
| Documento teórico `.md` | Recomendado | Teoría del lab — enriquece explicaciones, no las reemplaza |
| Notas auxiliares `.md` | Opcional | Q&A del alumno, apuntes de sesión, contexto adicional |

**Regla de oro**: ante cualquier discrepancia entre el notebook y los
documentos auxiliares, el notebook gana. Si la solución oficial tiene
errores, señalarlos explícitamente; nunca aceptarlos en silencio.

---

## 2 · Proceso obligatorio antes de producir nada

### Paso 1 — Leer el notebook completo

Extraer de cada celda:
- **Datos**: dataset, n, estadísticos clave, tipo de problema
- **Modelo**: distribuciones, hiperparámetros, código exacto
- **Pasos del lab**: numeración oficial del enunciado, preguntas a responder
- **Valores numéricos reales**: estimadores, IC, R̂, ESS, métricas
- **Conclusiones**: respuesta explícita del notebook a cada pregunta
- **Comparaciones**: si hay solución oficial vs notebook, ambas versiones

### Paso 2 — Plantear estructura y pedir confirmación

Presentar al usuario antes de producir nada:
1. Resumen del contenido extraído (datos, modelo, pasos, conclusiones)
2. Estructura propuesta de cada artefacto solicitado
3. Decisiones de diseño para contenido no trasladable directamente
   (sliders → tablas comparativas, traceplots animados → estáticos, etc.)

**No producir ningún archivo hasta recibir confirmación explícita.**

### Paso 3 — Ejecutar fases solicitadas en orden

```
HTML → Word estudio → Word teórico → PPTX
```

El PPTX siempre es la última fase porque reutiliza figuras de fases anteriores.

---

## 3 · Fase 1 — HTML interactivo

→ Leer `references/html-phase.md` antes de escribir código.

**Contrato de salida**:
- Archivo `.html` autocontenido, sin dependencias locales
- Navegación por tabs sticky, una por sección/paso del lab
- Gráficos con Chart.js 4.4.1 (CDN), inicialización lazy por tab
- Paleta oscura académica: fondo `#0f1117`, acento `#4f8ef7`
- Código JAGS/Python con coloreado sintáctico por rol semántico
- Funciona offline excepto CDN de Chart.js y Google Fonts

**Nombre de salida**: `LAB{N}_{asignatura}_{tema}_interactivo.html`

---

## 4 · Fase 2 — Word de estudio

→ Leer `references/word-phase.md` antes de escribir código.

**Contrato de salida**:
- Figuras: PNGs matplotlib en `/home/claude/lab{N}_imgs/`
- Diagramas: SVGs → PNG vía cairosvg en la misma carpeta
- Documento: docx-js (Node.js), A4, márgenes 2.5 cm, Arial
- Cabecera con asignatura/lab, pie con número de página, TOC automático
- Todo elemento interactivo del HTML tiene equivalente estático

**Tabla de adaptación HTML → Word** (ver §8 para tabla completa):
sliders → tablas comparativas de 3 valores · traceplots → PNGs estáticos ·
gauges R̂ → tablas con shading de celda · tabs → secciones con heading

**Nombre de salida**: `LAB{N}_estudio_{tema}.docx`

---

## 5 · Fase 3 — Word teórico

Documento de fundamentos conceptuales orientado al notebook. No copia el
Word de estudio: lo complementa explicando *por qué* el notebook hace lo
que hace.

→ Leer `references/word-phase.md` para la construcción técnica.

**Estructura canónica** (adaptar al tipo de lab):

| Sección | Pregunta que responde | Conexión al notebook |
|---|---|---|
| §1 Por qué [técnica] | ¿Por qué no basta un método analítico? | La integral/optimización intratable |
| §2 El modelo como grafo | ¿Qué representa el DAG / grafo de cómputo? | jags.model() / sklearn Pipeline |
| §3 El lenguaje de especificación | ¿Qué hace cada línea del código del modelo? | Bloque model{} / fit() anotado |
| §4 El algoritmo de inferencia | ¿Cómo funciona MCMC/GD/inferencia? | update() + coda.samples() / optimizer |
| §5 Los samplers / optimizadores | ¿Qué variantes usa el software y cuándo? | Gibbs/MH/Slice ó SGD/Adam/etc. |
| §6 Diagnóstico | ¿Cómo detectamos que algo va mal? | R̂+ESS / loss curves / métricas |
| §7 El problema técnico central | ¿Qué limitación específica tiene este lab? | Identificabilidad / overfitting / etc. |
| §8 Síntesis | ¿Cómo se conecta todo en el notebook? | Diagrama de flujo completo |

**Figuras requeridas** (generar con matplotlib, paleta COIIAOC):
- Fig 1: problema que motiva la técnica (por qué no analítico)
- Fig 2: ciclo del algoritmo (MH cycle, backprop, etc.)
- Fig 3: convergencia buena vs mala (traceplots, loss curves)
- Fig 4: diagnóstico (R̂ comparativo, curvas de validación)
- Fig 5: el problema técnico central (cresta de identificabilidad, overfitting)
- Fig 6: el diagnóstico clave (ESS, matriz de confusión, etc.)
- Fig 7: comparativa de variantes (samplers, optimizadores)
- Diag 1: DAG o grafo del modelo
- Diag 2: DAG con placa / grafo de cómputo expandido
- Diag 3: diagrama de flujo completo del notebook
- Diag 4: el algoritmo central ilustrado

**Nombre de salida**: `LAB{N}_teoria_{concepto}.docx`

---

## 6 · Fase 4 — PPTX de clase

→ Leer `references/pptx-phase.md` antes de escribir código.

**Contrato de salida**:
- ~32 diapositivas para 60–75 min de clase (adaptable)
- Paleta COIIAOC v1.1 estricta (ver design-system skill)
- Figuras matplotlib regeneradas con fondo `#FAFAF7` (crema-tecnico)
- Notas del presentador en todas las slides de contenido
- QA visual obligatorio vía LibreOffice → PDF → pdftoppm

**Los cuatro layouts** (únicos, no mezclar con otros):
1. **Portada** — dark navy `#1E3A5F`, franja naranja, chips de contenido
2. **Sección** — dark navy, número `§N` grande naranja, subtítulo
3. **Contenido** — fondo crema, barra lateral 0.12" de color semántico
4. **Figura full** — título 22pt arriba, imagen ocupa 85% del slide

**Secuencia de producción**:
1. Regenerar figuras matplotlib con paleta COIIAOC (`bg='#FAFAF7'`)
2. Copiar diagramas SVG→PNG de la fase Word (mismos archivos)
3. Construir PPTX con pptxgenjs
4. QA visual: LibreOffice → PDF → pdftoppm → inspeccionar slides críticos

**Nombre de salida**: `LAB{N}_{tema}.pptx`

---

## 7 · Reutilización entre fases

El pipeline es eficiente: los assets generados en fases anteriores se
reutilizan en fases posteriores.

| Asset | Generado en | Reutilizado en |
|---|---|---|
| PNGs matplotlib (fondo blanco) | Fase 2 (Word estudio) | Fase 3 (Word teórico) |
| Diagramas SVG → PNG | Fase 2 | Fases 3 y 4 |
| PNGs matplotlib (fondo crema COIIAOC) | Fase 4 (PPTX) | Solo PPTX |
| Valores numéricos del notebook | Fase 1 (HTML) | Todas |

**Las figuras para el PPTX siempre se regeneran** con paleta COIIAOC
aunque existan versiones de fondo blanco de fases anteriores. Son archivos
distintos: `/home/claude/lab{N}_imgs/pptx/fig{N}_{nombre}.png`.

---

## 8 · Tabla maestra de adaptación entre formatos

| Elemento original | HTML | Word | PPTX |
|---|---|---|---|
| Slider de σ / hiperparámetro | Slider live → actualiza Chart.js | Tabla 3 valores (mín/típico/máx) | Diapositiva dedicada: tabla comparativa |
| Selector de modelo (pooling) | Botones con feedback dinámico | Tabla pros/contras 3 opciones | Bullets con colores semánticos |
| Traceplot MCMC | Canvas simulado, 3 cadenas | PNG matplotlib estático | Fig full slide: 2 paneles |
| Gauge R̂ | Chips coloreados (verde/rojo) | Tabla con ShadingType.CLEAR | Tabla izquierda + ESS tabla derecha |
| Barras ESS | Barras HTML con umbral 400 | Tabla con estado OK/BAJO | Misma tabla que R̂ |
| DAG interactivo | SVG inline con onclick | PNG vía cairosvg | PNG mismo archivo |
| Código anotado | Div con coloreado CSS | PNG `code-diagram-explainer` + literal mono | Código block + anotaciones derecha |
| Density plots superpuestos | Chart.js multi-dataset | PNG matplotlib colormap | Fig full slide |
| Tabs / stepper | Navegación nav sticky | Headings H1/H2 + TOC | Slides de sección dark |
| Tabla de resultados | Tabla HTML con colores | `dataTable()` helper docx-js | `addTable()` helper pptxgenjs |
| Caja informativa | `div.infobox` con accent | `colorBox()` barra lateral 210 DXA | `addInfoBox()` barra 0.24" |

---

## 9 · Invariantes de calidad — aplican a las cuatro fases

**Contenido (todas las fases)**
- Valores numéricos idénticos a los del notebook en todas las fases
- Conclusiones responden exactamente las preguntas del enunciado
- Los errores de la solución oficial se señalan, no se copian

**HTML (Fase 1)**
- Cada tab accesible sin scroll; gráficos lazy-init por tab
- Sin `position: fixed`; sin `display:none` durante streaming
- `~` vs `<-` diferenciados visualmente en código JAGS

**Word (Fases 2 y 3)**
- `WidthType.DXA` siempre (no PERCENTAGE)
- `ShadingType.CLEAR` siempre (no SOLID)
- `ImageRun` con `type`, `altText` los tres campos
- `columnWidths` suman exactamente el ancho de contenido
- TOC, cabecera y pie presentes; figuras con caption

**PPTX (Fase 4)**
- Colores sin `#` (hex 6 dígitos puros, no 8)
- No reutilizar objetos de opciones entre llamadas pptxgenjs
- `ROUNDED_RECTANGLE` sin accent overlays (usar `RECTANGLE`)
- QA visual ejecutado: ningún título wrappea sobre la imagen
- Notas del presentador en todas las slides de contenido

---

## 10 · Nombres de archivo y rutas

```
Carpeta de trabajo:    /home/claude/lab{N}_imgs/
PNGs Word/HTML:        fig{N}_{nombre}.png   (fondo blanco #FAFBFC)
PNGs PPTX:             pptx/fig{N}_{nombre}.png  (fondo crema #FAFAF7)
SVG diagrams:          diag_{nombre}.svg
PNG diagrams:          diag_{nombre}.png  (reutilizados en Word y PPTX)

Salidas:
  LAB{N}_{asignatura}_{tema}_interactivo.html
  LAB{N}_estudio_{tema}.docx
  LAB{N}_teoria_{concepto}.docx
  LAB{N}_{tema}.pptx
```

---

## 11 · Reference files — cuándo leer cada uno

| Archivo | Leer cuando |
|---|---|
| `references/html-phase.md` | Vas a producir el HTML (Fase 1) |
| `references/word-phase.md` | Vas a producir cualquier Word (Fases 2 o 3) |
| `references/pptx-phase.md` | Vas a producir el PPTX (Fase 4) |

Leer el reference file completo antes de escribir la primera línea de
código de cada fase. Nunca producir de memoria.
