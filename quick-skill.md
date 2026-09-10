# Quick Skill — Chuleta Operativa del Agente

> Catálogo de skills de Claude/Antigravity (`bernardo-skills`). Sin teoría ni preámbulos: qué pedir, qué dar de entrada y qué genera el agente.

---

## 1. Mapa de decisión rápida (Top)

| Entregable deseado | Prompt para el agente | Entrada necesaria | Salida generada |
| :--- | :--- | :--- | :--- |
| **Ingestar skill desde BACKLOG** | `"ingesta el skill X de BACKLOG"`, `"añade el skill X desde BACKLOG"` | Carpeta `./BACKLOG/<skill-name>` | Skill integrado en `skills/<category>/`, empaquetado y registrado en README, finder y quick-skill |
| **Actualizar chuleta operativa** | `"/quick-skill-md"`, `"actualiza quick-skill.md"`, `"regenera la chuleta"` | Repositorio actual y catálogo de skills | [`quick-skill.md`](quick-skill.md) actualizado y sincronizado en la raíz |
| **Sincronizar Skill Finder** | `"actualiza skill-finder.html"`, `"sincroniza el skill finder"` | Catálogo de skills en `skills/` | [`skill-finder.html`](skill-finder.html) actualizado con nuevos skills, iconos y rutas |
| **Migrar CLAUDE.md a AGENTS.md** | `"/claude-to-agents-md"`, `"migra CLAUDE.md a AGENTS.md"` | Archivo `CLAUDE.md` del proyecto | [`AGENTS.md`](AGENTS.md) canónico optimizado para Antigravity y multi-agente |
| **Alinear docs y código** | `"reconcilia el repo"`, `"actualiza el README"`, `"sync docs"` | Repositorio local con código y documentación | Informe de discrepancias por severidad + parches aplicados a docs/README |
| **Auditar fiabilidad de agente** | `"audita el agente"`, `"fitz esto"`, `"¿alucina el agente?"` | Respuesta o traza textual de un agente LLM | Veredicto FITZ (`SALUDABLE`, `ALUCINACIÓN`, `INYECCIÓN`, `DRIFT`) + señales + acción preventiva |
| **Registrar turnos de chat** | `"Vuelca esto al log"`, `"Log this turn"` *(o automático)* | Turnos de conversación de la sesión | Bloques `## Prompt N` / `## Response N` añadidos a `sessions/today-LOG.md` |
| **Reducir errores LLM (Karpathy)** | `"aplica karpathy-guidelines"`, `"revisa según karpathy"` | Tarea de diseño, implementación o refactor | Supuestos explicitados, cambios mínimos quirúrgicos y criterios de verificación |
| **Concisión de respuesta (Opus 5)** | `"aplica opus5-optim"`, `"hazlo más conciso"`, `"sin relleno"` | Respuesta a sintetizar o system prompt a editar | Respuesta directa sin boilerplate o bloque `<tone_preference>` en el prompt |
| **Validar autoría humana** | `"valida el artículo"`, `"revisa si parece IA"`, `"pásalo por el validador"` | Texto/borrador (Substack, LinkedIn, etc.) | Diagnóstico VIDAL (`VIVO`, `INTERVENIDO`, `DELEGADO`, `GHOST`) con % confianza |
| **Refinar texto en voz propia** | `"mejora el artículo"`, `"refina la voz"`, `"ponlo en mi voz"` | Borrador propio (frío o pre-validado) | Texto iterado hasta confianza ≥85% y ≤2 frases IA (Modelo A autónomo o B revisado) |
| **Matriz Slop vs Tesis (2×2)** | `"analiza slop de la digest"`, `"¿esto es slop?"`, `"pasa esto por el atlas"` | Newsletter, digest (HTML/MD/URLs) o artículo | Clasificación en 4 cuadrantes (texto/JSON) o mapa HTML interactivo |
| **LaTeX ↔ Markdown round-trip** | `"actualiza el LaTeX desde el MD"`, `"regenerate the paper"` | `SOURCE_TEX` (fresco) + `EDIT_MD` (editado) | `OUTPUT_TEX` compilable + `<OUTPUT_TEX>.diff` para revisión |
| **Exportar Markdown a PDF** | `"exportar a PDF"`, `"genera el PDF"`, `"render PDF"` | Fichero `.md` (con/sin fórmulas KaTeX) | Archivo `.pdf` vía Pandoc + Chrome headless (o WeasyPrint para bookmarks) |
| **Plantilla Word / PDF por tema** | `"genera una plantilla Word"`, `"renderiza este md con el estilo X"` | Markdown fuente + tema en `themes/*.json` | `reference.docx` / documento `.docx` y `.pdf` estilizados vía `wtg.py` |
| **Incrustar bookmarks a PDF** | `"añade bookmarks según el índice"`, `"genera el outline"` | Archivo `.pdf` + `.md` fuente o índice impreso | Nuevo PDF con jerarquía de marcadores navegables incrustados vía `pypdf` |
| **Guía práctica + Diagrama SVG** | `"haz una guía"`, `"genera una guía md"`, `"/md-guide-builder"` | Tema o notas en bruto | `guides/NN-TIPO-tema.md` con su diagrama autoexplicativo `.svg` (COIIAOC) |
| **Materiales docentes de lab** | `"convierte el notebook en material docente"`, `"pipeline completo"` | Notebook Jupyter resuelto (`.ipynb`) | Hasta 4 entregables: HTML interactivo, Word estudio, Word teórico, PPTX |
| **Ingesta / Consulta Wiki Karpathy**| `"add to wiki"`, `"what do I know about X"`, `"lint wiki"` | Fuentes crudas en `raw/<topic>/` | Artículos en `wiki/<topic>/`, `wiki/index.md` y registro en `wiki/log.md` |
| **Colores grafo Obsidian** | `"/graph-colors"`, `"colorear el grafo"`, `"grupos de color"` | Vault con `wiki/.obsidian/graph.json` | Reporte de anomalías + `graph.json` con paleta sincronizada |
| **Crear Vault Obsidian sin UI** | `"bootstrap vault"`, `"crear vault"`, `"nuevo vault obsidian"` | Directorio destino del vault | Carpeta `.obsidian/` completa con sus 5 ficheros JSON operativos |
| **Cierre y métricas de sesión** | `"registra la sesión"`, `"documenta esta sesión"`, pegar `/usage` | Salida de `/usage` de Claude Code | `USAGE.md` o `sessions/{fecha}-{slug}.md` con desglose de coste y scope |
| **Reconstruir razonamiento (CoT)** | `"escribe el CoT"`, `"documenta el razonamiento de la sesión"` | Sesión compleja de arquitectura/diseño | Markdown estructurado con Input / Razonamiento / Inferencia clave por paso |
| **Configurar Claude con MiniMax** | `"configurar Claude Code con MiniMax"`, `"quiero usar MiniMax"` | MiniMax API Key | Script lanzador `.bat` + configuración MCP lista |
| **Agente local offline (GPU)** | `"montar opencode local"`, `"configurar modelo local"` | GPU NVIDIA (RTX 2060+ / 6-8GB VRAM) | `opencode.json` configurado + runtime llama.cpp validado sin coste |
| **Proteger foco creativo (Flow)** | `"/flow"` (re-armar), `"/flow off"` (suspender) | Modo detectado (TOOL / STUCK / WORKSHOP) | Respuestas telegráficas sin charla meta para preservar la autoría |
| **Diagramar código en SVG** | `"explica este nodo"`, `"diagrama del nodo"`, `"explica visualmente"` | Código fuente (n8n, función, pipeline) | SVG autoexplicativo con control de flujo, ramas ✓/✗ y paleta COIIAOC v1.1 |
| **Diagramar texto en SVG** | `"convierte esto en diagrama"`, `"visualiza este apartado"` | Texto estructurado (prosa, método, flujo) | SVG autónomo que reemplaza el texto con jerarquía conceptual |
| **Escalera de pseudocódigo** | `"pasa esto por la escalera"` *(FORWARD)* o `"vault inverso"` *(INVERSO)* | Especificación de módulo o repo existente | Protocolo de 4 niveles con marcas [DELEGABLE]/[NO-DELEGABLE] o vault inverso |
| **Empaquetar skill para release** | Exec en shell: `python scripts/package_skill.py <path>` | Directorio `skills/<category>/<skill-name>` | Archivo `.skill` distribuible en `dist/<skill-name>.skill` |

---

## 2. Instrucciones operativas por familia de entregables

### ⚡ Familia 0: Meta-Skills del Repositorio (AGENTS.md & Ingesta BACKLOG)

#### `skill-ingest` (Ingesta bajo demanda desde `./BACKLOG`)
- **Disparador:** `"ingesta el skill X de BACKLOG"`, `"añade el skill X desde BACKLOG"`, `"incorpora BACKLOG/X"`.
- **Candidatos listos en `BACKLOG/`:** `compress`, `lesson-from-source`, `md-to-docx-rpa`.
- **Pasos autónomos:**
  1. Audita el candidato contra el checklist de `CONTRIBUTING.md` (`SKILL.md`, frontmatter YAML, longitud < 500 líneas, scripts y recursos).
  2. Determina la categoría (`dev`, `content`, `agentic`, `code`); si es ambigua, pregunta con `ask_question`.
  3. Mueve la carpeta a `skills/<category>/<skill-name>/` y prueba con `python scripts/package_skill.py skills/<category>/<skill-name>`.
  4. Sincroniza simultáneamente `README.md`, `quick-skill.md` y `skill-finder.html`.
- **Salida:** Skill plenamente integrado en el repositorio y distribuible como `.skill`.

#### `quick-skill-md`
- **Disparador:** `"/quick-skill-md"`, `"actualiza quick-skill.md"`, `"regenera la chuleta operativa"`.
- **Pasos autónomos:**
  1. Descubre reglas de agente, catálogo de skills, workflows y rutas de entrada/salida.
  2. Sintetiza la chuleta operativa de 3 secciones (Mapa rápido, Instrucciones por familia, Invariantes).
  3. Realiza verificación cruzada de rutas y scripts y actualiza `quick-skill.md`.
- **Salida:** `quick-skill.md` actualizado en la raíz del repositorio.

#### `skill-finder-sync`
- **Disparador:** `"actualiza skill-finder.html"`, `"sincroniza el skill finder"`.
- **Pasos autónomos:**
  1. Lee el catálogo de `skills/` y extrae nombre, categoría, icono sugerido, descripción y ruta.
  2. Registra o actualiza la entrada correspondiente en la constante `SKILLS` de `skill-finder.html`.
  3. Si aplica, enlaza la bifurcación correspondiente en `DECISION_TREE`.
- **Salida:** `skill-finder.html` actualizado.

---

### 🛠️ Familia 1: Calidad, Auditoría y Mantenimiento de Repositorios (Dev)

#### `repo-reconciler`
- **Disparador:** `"reconcilia el repo"`, `"actualiza el README"`, `"sync docs"`, `"comprueba coherencia"`.
- **Pasos autónomos:**
  1. Realiza inventario cruzado de código fuente vs documentación.
  2. Detecta funciones sin documentar, docs obsoletas, ejemplos rotos y desajustes de versiones.
  3. Genera un informe categorizado por severidad (`CRÍTICA`, `ALTA`, `MEDIA`, `BAJA`).
  4. Aplica directamente los parches correctivos a los documentos correspondientes.
- **Salida:** Parches aplicados a `README.md` o documentación del proyecto.

#### `fitz-agent-auditor`
- **Disparador:** `"audita el agente"`, `"fitz esto"`, `"¿alucina el agente?"`, `"¿hay inyección?"`, `"¿está drifteando?"`.
- **Pasos autónomos:**
  1. Aplica lingüística forense sobre la respuesta del agente.
  2. Emite veredicto: `SALUDABLE`, `ALUCINACIÓN`, `INYECCIÓN` o `DRIFT`.
  3. Identifica señales lingüísticas exactas y propone medidas de mitigación operativa.
- **Salida:** Informe forense estructurado en el chat o en archivo de análisis.

#### `karpathy-guidelines`
- **Disparador:** `"aplica karpathy-guidelines"`, `"revisa según karpathy"`, o al escribir/refactorizar código.
- **Pasos autónomos:**
  1. Detiene la implementación prematura y explicita supuestos y tradeoffs.
  2. Garantiza la mínima cantidad de código sin abstracciones especulativas.
  3. Aplica cambios estrictamente quirúrgicos y define pruebas verificables antes de iterar.
- **Salida:** Código limpio, minimalista y verificado.

#### `opus5-optim`
- **Disparador:** `"aplica opus5-optim"`, `"hazlo más conciso"`, `"sin relleno"`, `"recorta las respuestas"`.
- **Pasos autónomos:**
  1. En respuestas directas: elimina preámbulos, advertencias redundantes y relleno.
  2. En system prompts: añade el bloque de concisión al final:
     ```xml
     <tone_preference>
     Keep outputs reasonably concise.
     </tone_preference>
     ```
- **Salida:** Respuestas compactas o prompt ajustado.

#### `quick-skill-md`
- **Disparador:** `"/quick-skill-md"`, `"actualiza quick-skill.md"`, `"regenera la chuleta operativa"`.
- **Pasos autónomos:**
  1. Audita el repositorio descubriendo reglas, catálogo de skills, workflows y rutas de entrada/salida.
  2. Sintetiza la chuleta operativa de 3 secciones (Mapa de decisión rápida, Instrucciones operativas por familia, Invariantes no negociables).
  3. Comprueba y enlaza rutas de scripts y archivos y escribe `quick-skill.md`.
- **Salida:** [`quick-skill.md`](quick-skill.md) en la raíz del repositorio.

---

### ✍️ Familia 2: Validación, Voz y Análisis Editorial (Content)

#### `authorship-validator`
- **Disparador:** `"valida el artículo"`, `"revisa si parece IA"`, `"pásalo por el validador"`, `"auditoría de autoría"`.
- **Pasos autónomos:**
  1. Analiza el texto con el marco VIDAL (fricción humana vs homogeneidad de LLM).
  2. Evalúa señales de voz, coherencia y contradicción productiva.
  3. Emite veredicto (`VIVO`, `INTERVENIDO`, `DELEGADO`, `GHOST`) y porcentaje de confianza.
- **Salida:** Diagnóstico detallado con frases señaladas y recomendación de publicación.

#### `voice-refiner`
- **Disparador:** `"mejora el artículo"`, `"refina la voz"`, `"ponlo en mi voz"`, `"limpia las frases IA"`.
- **Modos:**
  - **Modelo A (Autónomo, por defecto):** Itera internamente hasta alcanzar ≥85% confianza humana y ≤2 frases IA.
  - **Modelo B (Con revisión):** Pide confirmación al autor tras cada vuelta (`"modo iterativo"`).
- **Salida:** Versión final pulida con resumen de cambios efectuados.

#### `atlas-slop-ai`
- **Disparador:** `"analiza slop de la digest"`, `"¿esto es slop?"`, `"pasa esto por el atlas de slop"`.
- **Pasos autónomos:**
  1. Cruza los dos ejes independientes: Autoría (Humano vs IA) × Sustancia (Tesis propia vs Slop).
  2. Clasifica en 4 cuadrantes: `HUM·NO-SLOP` (Navy), `IA·NO-SLOP` (Verde), `HUM·SLOP` (Naranja), `IA·SLOP` (Rojo).
  3. Genera clasificación tabular/JSON o mapa visual interactivo HTML.
- **Salida:** Tabla de triaje o visor interactivo HTML.

---

### 📄 Familia 3: Generación de Documentos y Formatos Técnicos (PDF, Word, LaTeX, Docencia)

#### `pdf-export`
- **Disparador:** `"exportar a PDF"`, `"genera el PDF"`, `"render PDF"`, `"pdf-export"`.
- **Pipelines disponibles:**
  - **Pipeline A (Por defecto / con fórmulas LaTeX):** Pandoc (KaTeX) → HTML → Chrome headless.
  - **Pipeline B (Sin fórmulas / con marcadores automáticos):** Pandoc → HTML → WeasyPrint.
- **Salida:** Archivo `.pdf` compilado con estilos tipográficos limpios.

#### `pdf-TOC-bookmarker`
- **Disparador:** `"añade bookmarks según el índice"`, `"genera el outline"`, `"pon marcadores de navegación"`.
- **Flujo:**
  - Si el PDF proviene de `pdf-export` (Pipeline A): corre directamente `skills/content/pdf-TOC-bookmarker/scripts/build_bookmarks_from_md_source.py` leyendo los headings `#`/`##`/`###`.
  - Si proviene de escaneo/externo: parsea la página de "Contents" impresa, calcula el offset y escribe el árbol con `pypdf`.
- **Salida:** `<nombre>_con_marcadores.pdf` con índice navegable.

#### `word-template-gen`
- **Disparador:** `"genera una plantilla Word"`, `"renderiza este md con el estilo X"`, `"catálogo de estilos"`.
- **Motor:** `python skills/content/word-template-gen/wtg.py list|build|render`.
- **Flujo:** Toma un tema JSON en `themes/` y deriva simétricamente el CSS (HTML/PDF) y los estilos de `reference.docx`.
- **Salida:** Plantilla `.docx` o render final `.docx` y `.pdf`.

#### `latex-md-roundtrip`
- **Disparador:** `"actualiza el LaTeX desde el MD"`, `"regenerate the paper"`, `"verify roundtrip"`.
- **Flujo:** Congela `SOURCE_TEX` (solo lectura), genera `BASELINE_MD`, permite editar libremente en `EDIT_MD` y regenera `OUTPUT_TEX` junto con su `<OUTPUT_TEX>.diff`.
- **Salida:** Archivo `.tex` listo para subir y diff de control.

#### `md-guide-builder`
- **Disparador:** `"haz una guía"`, `"genera una guía md"`, `"/md-guide-builder"`.
- **Convención:** Estilo `core-human-knowledge` (`NN-TIPO-tema.md` con idea rectora, reglas numeradas y chuleta) + diagrama SVG obligatorio (paleta COIIAOC v1.1).
- **Salida:** `guides/NN-TIPO-tema.md` y `guides/NN-TIPO-tema.svg`.

#### `lab-doc-pipeline`
- **Disparador:** `"convierte el notebook en material docente"`, `"pipeline completo"`.
- **Entrada:** Notebook Jupyter resuelto (`.ipynb`).
- **Fases independientes o encadenadas:**
  1. HTML interactivo para proyección con sliders en tiempo real.
  2. Word (`.docx`) de estudio autocontenido con ejercicios.
  3. Word teórico centrado en fundamentos conceptuales (DAG, MCMC, etc.).
  4. PPTX para clase con notas para el profesor.
- **Salida:** Artefactos docentes listos para el aula.

---

### 🧠 Familia 4: Gestión de Conocimiento y Obsidian

#### `karpathy-llm-wiki`
- **Disparador:** `"add to wiki"`, `"what do I know about X"`, `"lint wiki"`.
- **Estructura fija:**
  - `raw/<topic>/`: fuentes inmutables (solo lectura para el agente).
  - `wiki/<topic>/<article>.md`: síntesis compilada (propiedad del agente).
  - `wiki/index.md`: índice global con enlaces y fechas.
  - `wiki/log.md`: registro cronológico de operaciones.
- **Salida:** Artículos interconectados y base de conocimiento acumulativa.

#### `obsidian-vault-builder`
- **Disparador:** `"bootstrap vault"`, `"crear vault"`, `"nuevo vault obsidian"`.
- **Acción:** Crea de forma autónoma los 5 archivos JSON de `.obsidian/` (`app`, `appearance`, `core-plugins`, `graph`, `workspace`) sin requerir abrir Obsidian.
- **Salida:** Directorio `.obsidian/` completamente inicializado.

#### `obsidian-graph-colors`
- **Disparador:** `"/graph-colors"`, `"colorear el grafo"`, `"grupos de color"`.
- **Script:** `python skills/content/karpathy-wiki/obsidian-graph-colors/audit.py` (o `python .claude/skills/obsidian-graph-colors/audit.py` si está instalado).
- **Acción:** Audita tags huérfanos, sin color o duplicados y sincroniza `graph.json`.
- **Salida:** `wiki/.obsidian/graph.json` saneado y coloreado.

---

### 📊 Familia 5: Diagramación y Arquitectura Visual (Code)

#### `code-diagram-explainer`
- **Disparador:** `"explica este nodo"`, `"diagrama del nodo"`, `"explica visualmente"`.
- **Estándar:** Paleta COIIAOC v1.1, pseudocódigo extraído fielmente del código, flujo con ramas ✓/✗ y anotaciones explicativas.
- **Salida:** Diagrama SVG inline o archivo `.svg`.

#### `text-to-diagram`
- **Disparador:** `"convierte esto en diagrama"`, `"visualiza este apartado"`, `"ilustra la metodología"`.
- **Principio:** El diagrama sustituye a la prosa; debe comprenderse por completo de manera independiente.
- **Salida:** Archivo SVG autocontenido.

#### `pseudocode-ladder`
- **Disparador:** `"pasa esto por la escalera"` *(FORWARD)*, `"reconstruye los niveles desde el código"` *(INVERSO)*.
- **Niveles:**
  - Nivel 1: Lógica general en prosa técnica.
  - Nivel 2: Clases, interfaces y contratos.
  - Nivel 3: Pseudocódigo de funciones marcando explícitamente `[DELEGABLE]` vs `[NO-DELEGABLE]`.
  - Nivel 4 (Opcional): Casi-Python ejecutable.
- **Salida:** Especificación validada paso a paso o vault Obsidian inverso (`docs/design/`).

---

### 🤖 Familia 6: Agéntica, Control de Sesión y Runtimes (Agentic)

#### `flow`
- **Disparador:** `"/flow"` (re-armar), `"/flow off"` (suspender sesión).
- **Detección continua:** Evalúa en cada turno el modo del usuario:
  - `TOOL`: el usuario produce; responde con código/acción inmediata sin explicaciones.
  - `STUCK`: el usuario se bloquea; ofrece 2-3 opciones concretas con tradeoffs.
  - `WORKSHOP`: debate abierto; co-diseña sin imponer soluciones completas que diluyan la autoría.
- **Salida:** Respuestas con longitud y registro estrictamente calibrados.

#### `log-turn`
- **Disparador:** `"Vuelca esto al log"`, `"Log this turn"`. Activo por defecto en cada turno de asistente.
- **Acción:** Apendea al final de `sessions/today-LOG.md` el bloque:
  ```markdown
  ---
  ## Prompt N: <Título>
  <prompt del usuario>
  ## Response N
  **<resumen en negrita>**
  <cuerpo de la respuesta>
  ```
- **Salida:** `sessions/today-LOG.md` actualizado.

#### `registro-sesion-claude` & `session-cot`
- **Disparador:** `"registra la sesión"`, pegar `/usage`, `"escribe el CoT"`, `"documenta el razonamiento"`.
- **Salida:**
  - `USAGE.md`: métricas de consumo, commits realizados y tareas pendientes.
  - `sessions/{fecha}-cot.md`: traza de pensamiento (Input → Razonamiento → Inferencia).

#### `setup-minimax` & `setup-opencode-local`
- **Disparador:** `"configurar Claude Code con MiniMax"`, `"montar opencode local"`.
- **Salida:** Entornos de ejecución asistida configurados (remoto MiniMax o local privado en GPU con `llama.cpp` + `opencode`).

#### `claude-to-agents-md`
- **Disparador:** `"/claude-to-agents-md"`, `"migra CLAUDE.md a AGENTS.md"`, `"adapta las instrucciones a Antigravity"`.
- **Pasos autónomos:**
  1. Audita el `CLAUDE.md` original extrayendo rol, modelo de carpetas, convenciones, estilo visual e invariantes.
  2. Detecta el entorno (OS Windows/PowerShell, herramientas nativas sin `cd`, rutas directas a skills).
  3. Redacta el `AGENTS.md` canónico en 5 secciones preservando íntegro el `CLAUDE.md` fuente.
  4. Valida enlaces clickables `file:///` con barras normales y comprueba criterios de aceptación (DoD).
- **Salida:** [`AGENTS.md`](AGENTS.md) generado en la raíz del repositorio.

---

## 3. Invariantes no negociables (Bottom)

1. **Estructura estricta de skills en el repositorio:**
   - Todo skill debe residir exclusivamente en `skills/<categoría>/<nombre-kebab>/` (`dev`, `content`, `agentic`, `code`).
   - Todo skill requiere un `SKILL.md` con frontmatter YAML válido (`name` y `description` detallada con triggers precisos) y un cuerpo menor a 500 líneas (usar `references/` para material extenso).
   - Al agregar o modificar un skill, es obligatorio registrarlo en las tablas de `README.md` y en el catálogo/árbol de `skill-finder.html`.

2. **Empaquetado y distribución:**
   - El empaquetado de skills se realiza mediante el script estándar:
     ```bash
     python scripts/package_skill.py skills/<categoria>/<nombre-skill> [--output dist/]
     ```
   - Los archivos generados `.skill` y la carpeta `dist/` están ignorados en git y nunca deben commitearse.

3. **Inviolabilidad de carpetas privadas e ignoradas:**
   - Nunca commitear ni tocar material de referencia personal o de trabajo en curso no publicado:
     - `ASIDE-Slack-Gitkraken/`
     - `BACKLOG/`
     - Scripts personales como `claude-minimax.bat`.

4. **Estándares visuales y tipográficos:**
   - **Diagramas SVG:** Obligatorio utilizar la paleta corporativa COIIAOC v1.1 (`#0B2545`, `#134074`, `#8DA9C4`, `#EE6C4D`, `#2A9D8F`) y tipografía V2 (Inter / system-ui).
   - **Renders PDF:** Si el documento contiene fórmulas matemáticas o notación científica, utilizar obligatoriamente el Pipeline A (`Pandoc` + `KaTeX` + `Chrome headless`).

5. **Disciplina de ingeniería y Karpathy Guidelines:**
   - No asumir intenciones ambiguas: explicitar supuestos y preguntar antes de actuar.
   - Modificaciones quirúrgicas: tocar únicamente lo necesario sin introducir abstracciones o configuraciones no solicitadas.
   - En commits relevantes, mantener sincronizados los logs de sesión (`/log-turn` en `sessions/today-LOG.md` o `/usage`).
