# bernardo-skills — Instrucciones del Repositorio para Agentes (Antigravity)

> Fuente de verdad operativa para agentes autónomos (Google Antigravity, Claude Code y ecosistemas multi-agente) que operan sobre el repositorio `bernardo-skills`.

---

## 1. Misión Principal del Agente

El agente tiene dos objetivos operativos prioritarios:

1. **Ingesta bajo demanda de nuevos skills desde `./BACKLOG`:** Auditar, catalogar, empaquetar e incorporar skills situados en `BACKLOG/<skill-name>` hacia su categoría oficial en `skills/<category>/<skill-name>`.
2. **Sincronización documental y catálogo interactivo posterior:** Mantener automáticamente actualizados y coherentes tras cada ingesta:
   - [`quick-skill.md`](file:///C:/Users/brjap/Documents/__CODE_gpu/(claude-skills/quick-skill.md)) (chuleta operativa sin preámbulos).
   - [`skill-finder.html`](file:///C:/Users/brjap/Documents/__CODE_gpu/(claude-skills/skill-finder.html)) (catálogo interactivo y árbol de decisión).
   - [`README.md`](file:///C:/Users/brjap/Documents/__CODE_gpu/(claude-skills/README.md)) (tablas del catálogo y guía rápida por tarea).

---

## 2. Entorno de Ejecución y Convenciones Técnicas

- **Plataforma:** Google Antigravity (CLI / IDE / Desktop) y Claude Code.
- **Sistema Operativo y Shell:** Windows / PowerShell.
- **Herramientas nativas del agente:**
  - Emplear exclusivamente herramientas nativas de inspección y edición (`view_file`, `write_to_file`, `replace_file_content`, `run_command`, `ask_question`).
  - **Prohibido el uso de comandos `cd`** en PowerShell: ejecutar siempre comandos desde la raíz del workspace o pasando rutas relativas/absolutas.
  - Enlaces a archivos en Markdown: siempre en formato clickable `[texto](file:///ruta/normalizada)` con barras hacia adelante (`/`).
- **Codificación:** UTF-8 sin BOM en todos los ficheros generados o editados.

---

## 3. Procedimiento Paso a Paso: Ingesta de Skills desde `./BACKLOG`

Cuando el usuario pida *"ingesta el skill X de BACKLOG"*, *"añade el skill X desde BACKLOG"*, *"incorpora BACKLOG/X"*, o cualquier instrucción análoga, el agente debe ejecutar estrictamente este flujo:

```
[BACKLOG/<skill>] ──► [Auditoría & Checklist] ──► [skills/<category>/<skill>] ──► [Empaquetado test] ──► [Sincronización README + quick-skill + skill-finder]
```

### Paso 1: Auditoría de calidad del candidato en `./BACKLOG/<skill-name>`
Verificar que la carpeta candidata cumple la especificación de [`CONTRIBUTING.md`](file:///C:/Users/brjap/Documents/__CODE_gpu/(claude-skills/CONTRIBUTING.md):
- [ ] Existe `SKILL.md` obligatorio con frontmatter YAML válido:
  - `name`: en kebab-case, coincidente con el nombre de la carpeta.
  - `description`: explicita cuándo activarlo, qué hace y frases/prompts desencadenantes concretos.
- [ ] El cuerpo de `SKILL.md` es conciso (< 500 líneas). Si hay contenido extenso, debe modularizarse en `references/`, `scripts/` o `assets/`.
- [ ] Todos los scripts (`.py`, `.sh`, `.bat`) y recursos referenciados existen dentro de la carpeta del skill.

### Paso 2: Determinación de categoría destino
Clasificar el skill en una de las 4 categorías estándar:
| Categoría | Criterio |
| :--- | :--- |
| `skills/dev/` | Opera sobre código, repositorios, linters, auditores técnicos o herramientas de desarrollo. |
| `skills/content/` | Produce, valida o refina contenido escrito, papers, documentos Word/PDF o pipelines docentes. |
| `skills/agentic/` | Orquesta flujos multi-paso, control de sesión, contratos de flujo o setup de runtimes de agentes. |
| `skills/code/` | Genera diagramas SVG explicativos de código o texto estructurado, o protocolos de diseño en pseudocódigo. |

> [!IMPORTANT]
> Si la categoría resulta ambigua o el skill encaja en más de una, **no adivinar silenciosamente**: usar `ask_question` para consultar la preferencia del usuario antes de mover archivos.

### Paso 3: Traslado a `skills/` y prueba de empaquetado
1. Mover o copiar la carpeta desde `BACKLOG/<skill-name>` hacia `skills/<category>/<skill-name>/`.
2. Probar el empaquetado del skill ejecutando:
   ```powershell
   python scripts/package_skill.py skills/<category>/<skill-name>
   ```
3. Verificar que el comando finalice con código de salida `0` y genere `dist/<skill-name>.skill`. (Recordar que `dist/` está ignorado en git).

### Paso 4: Actualización obligatoria de índices y catálogo

#### A. Actualizar [`README.md`](file:///C:/Users/brjap/Documents/__CODE_gpu/(claude-skills/README.md)
1. Añadir una fila a la tabla `## Quick guide: pick a skill by task`:
   ```markdown
   | <Acción del usuario> | [`<skill-name>`](skills/<category>/<skill-name>/) |
   ```
2. Añadir una fila a la tabla correspondiente a su categoría (`### 🛠️ Dev`, `### ✍️ Content`, `### 🤖 Agentic`, o `### 📊 Code`).

#### B. Actualizar [`quick-skill.md`](file:///C:/Users/brjap/Documents/__CODE_gpu/(claude-skills/quick-skill.md)
1. **Sección 1 (Mapa de decisión rápida):** Insertar fila comparativa:
   ```markdown
   | **<Entregable deseado>** | `"<prompt 1>"`, `"<prompt 2>"` | <Entrada necesaria> | <Salida generada> |
   ```
2. **Sección 2 (Instrucciones operativas):** Añadir sub-bloque bajo la familia correspondiente con:
   - Disparador exacto.
   - Pasos autónomos del agente.
   - Formato y ubicación del entregable.

#### C. Actualizar [`skill-finder.html`](file:///C:/Users/brjap/Documents/__CODE_gpu/(claude-skills/skill-finder.html)
1. Añadir la entrada al objeto constante `SKILLS` dentro de la etiqueta `<script>`:
   ```javascript
   "<skill-name>": {
     name: "<skill-name>",
     category: "<Category>", // "Dev", "Content", "Agentic", o "Code"
     icon: "<icono>",        // "wrench", "pen", "doc", "robot", "graph", "diagram", "wave", "flask"
     desc: "<Descripción breve y concisa>",
     path: "skills/<category>/<skill-name>/"
   },
   ```
2. Si procede, añadir una opción de bifurcación o nodo en el árbol de decisión (`DECISION_TREE`).

---

## 4. Invariantes No Negociables del Repositorio

1. **Protección de material privado:**
   - Prohibido commitear o alterar carpetas personales de soporte ignoradas en `.gitignore`:
     - `ASIDE-Slack-Gitkraken/`
     - `BACKLOG/` (salvo lectura para ingesta)
     - Ficheros `.bat` personales locales.
2. **Estándares visuales inmutables:**
   - Diagramas SVG deben usar siempre la paleta oficial COIIAOC v1.1 (`#0B2545`, `#134074`, `#8DA9C4`, `#EE6C4D`, `#2A9D8F`) y tipografía V2 (Inter / system-ui).
   - Diagramas autoexplicativos: deben sustituir al texto, nunca decorarlo.
3. **Ingeniería quirúrgica (Karpathy Guidelines):**
   - Realizar modificaciones mínimas y verificables.
   - No añadir configuraciones ni abstracciones innecesarias.
   - Validar antes de dar por completada cualquier tarea (`verification-before-completion`).

---

## 5. Criterios de Aceptación (Definition of Done)

Una tarea de ingesta de skill desde `./BACKLOG` solo se considera terminada cuando:
- [ ] El skill está en `skills/<category>/<skill-name>/` con `SKILL.md` íntegro.
- [ ] `python scripts/package_skill.py skills/<category>/<skill-name>` ejecuta con éxito.
- [ ] `README.md` refleja el nuevo skill en su tabla de categoría y en la guía rápida.
- [ ] `quick-skill.md` tiene registrada la fila de decisión rápida y el bloque operativo.
- [ ] `skill-finder.html` incluye la entrada en su catálogo `SKILLS` y renderiza sin errores.
- [ ] `git status` muestra un árbol limpio tras commitear con mensaje semántico (`feat(<skill-name>): add skill from backlog and sync docs`).
