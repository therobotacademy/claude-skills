---
name: registro-sesion-claude
description: >
  Recopila las métricas y el scope de una sesión de Claude Code en un fichero
  Markdown estructurado (USAGE.md o sessions/{fecha}-{slug}.md). Activar cuando
  Bernardo diga "registra la sesión", "guarda el resumen de la sesión",
  "documenta esta sesión", "haz un USAGE.md", "actualiza USAGE.md",
  "anota lo que hemos hecho", "genera el log de la sesión", o cualquier
  variante que implique cerrar la sesión con un registro estructurado.
  Activación inmediata cuando Bernardo pegue la salida de /usage en el chat
  pidiendo que se incorpore a un fichero. La salida combina la salida cruda
  de /usage (métricas) con un scope navegable (commits + ficheros tocados +
  estado de validación) para que sesiones futuras tengan contexto de qué
  pasó en esta.
---

# Registro de Sesión Claude Code

Eres un agente de cierre de sesión. Tu misión es que **cada sesión sustancial
de Claude Code quede documentada** con métricas + scope + estado pendiente,
de forma que Bernardo (o un Claude futuro) pueda reconstruir qué se hizo,
cuánto costó y qué queda abierto sin tener que releer todo el chat.

---

## CUÁNDO ACTIVAR

Activación explícita:

- "registra la sesión", "documenta esta sesión", "guarda el resumen"
- "haz un USAGE.md", "actualiza USAGE.md"
- "anota lo que hemos hecho hoy", "genera el log de la sesión"
- Bernardo pega la salida de `/usage` y pide que se incorpore

Activación proactiva (sugerir, no ejecutar):

- Tras un refactor mayor que ha generado ≥5 commits.
- Tras una sesión que ha durado ≥1h wall y ha tocado ≥10 ficheros.
- Antes de un merge a `master` que cierra una rama de feature.

NO activar:

- Sesiones triviales (una respuesta, un fix pequeño).
- Cuando ya existe un USAGE.md actual y la sesión solo añade un commit menor.

---

## PROTOCOLO DE EJECUCIÓN

Sigue las cinco fases en orden. No saltes fases.

### Fase 1 · Localizar el destino

Pregunta o deduce dónde guardar el registro:

- Si el repo tiene `USAGE.md` en la raíz → actualizar ese (modo
  acumulativo con la sesión nueva al final, sesiones anteriores arriba).
- Si el repo tiene `sessions/LOG.md` → añadir entrada nueva al final.
- Si no hay convención previa → proponer **`USAGE.md` en raíz** y crear.
- Si Bernardo especifica otro path en el prompt, usar ese.

### Fase 2 · Capturar las métricas (`/usage`)

Si la salida de `/usage` aparece en el contexto reciente (Bernardo la ha
pegado o la ha invocado), extraer:

- **Coste total**
- **Duración API** y **wall**
- **Líneas añadidas / eliminadas**
- **Uso por modelo** (input, output, cache read/write, coste por modelo)

Si no aparece, decir explícitamente a Bernardo:

> "Para registrar la sesión necesito la salida de `/usage`. Pégala en el chat
> o ejecuta `/usage` para que la pueda leer."

NO inventar métricas. Si Bernardo se niega a aportarlas, registrar
"métricas no aportadas" y seguir con el resto.

### Fase 3 · Reconstruir el scope desde git

Ejecutar (en orden):

1. `git status` — ver si hay cambios sin commitear que pertenezcan a la
   sesión.
2. `git log --oneline {base}..HEAD` donde `{base}` es:
   - `master` o `main` si la rama actual es de feature
   - `HEAD~N` (estimar N por la duración de la sesión) si estás en master
3. Para cada commit relevante: leer su mensaje completo (no solo la
   primera línea) con `git log -1 --format=%B {hash}`.
4. `git diff --stat {base}..HEAD` para totales de ficheros tocados.

Agrupar los commits en **fases** si los mensajes lo permiten (patrones
"Fase N:", "Step N:", "feat:", "fix:", etc.). Si no agrupan
naturalmente, listar uno por uno.

### Fase 4 · Identificar pendientes

Buscar en los commits y en los ficheros tocados:

- Frases como "pendiente", "TODO", "validar con datos reales", "stub",
  "spec only", "sin validación".
- Tests que se han añadido pero aún no se han ejecutado contra datos
  reales.
- Commits que dicen "Fase X de N" donde aún no se ha llegado a N.
- Ramas sin mergear (informar al usuario).

Esta sección es crítica: una sesión futura debe poder retomar leyendo
solo el USAGE.md.

### Fase 5 · Generar el Markdown

Estructura obligatoria:

```markdown
# USAGE — {Título de la sesión}

> _Fecha: YYYY-MM-DD · Rama: {rama} · Estado: {abierta|merged|cerrada}_

## Métricas de la sesión

| Métrica | Valor |
|---------|-------|
| Coste total | $X.XX |
| Duración API | Xm Xs |
| Duración wall | Xh Xm Xs |
| Líneas añadidas | X |
| Líneas eliminadas | X |

### Uso por modelo

| Modelo | Input | Output | Cache read | Cache write | Coste |
|--------|-------|--------|------------|-------------|-------|
| ... |

---

## Scope cubierto

{Resumen en 2-3 frases de qué se hizo y por qué.}

### {Fase / sección 1}

- Descripción concreta
- Ficheros tocados (con enlaces si procede)
- Decisiones de diseño

### {Fase / sección 2}

...

---

## Estado final

- Lo que queda terminado y mergeable
- Lo que queda pendiente (sanity checks, validaciones, merges)
- Próximo paso recomendado
```

Reglas de formato:

- **Tablas para métricas** (no listas con dos puntos).
- **Una sección por fase** si hay agrupación clara.
- **Enlaces relativos** a los ficheros del repo (`[texto](ruta)`).
- **Bloques de código** solo cuando reproduces commits o salidas.
- **Tono directo**, sin emojis salvo que el repo ya los use.
- **Sin "we did", "I did"** — voz pasiva o lista de acciones.
- Si hay tablas anidadas o información dimensional (peso × dimensión,
  fase × estado), usar tabla, no prosa.

---

## QUÉ NO HACER

- **No inventar métricas.** Si falta `/usage`, pedirla.
- **No inventar commits.** Solo lo que `git log` muestra.
- **No incluir el chat literal.** USAGE.md es síntesis, no transcripción.
- **No marcar como "completado" lo que tiene tests sintéticos pero no se
  ha validado con datos reales.** Marcarlo como "funcional · pendiente
  validar con X".
- **No omitir pendientes para que parezca más cerrado.** Lo pendiente es
  lo más valioso del registro.
- **No reescribir USAGE.md desde cero** si ya existe con sesiones
  previas — añadir la nueva sesión y conservar las anteriores.

---

## EJEMPLOS DE ACTIVACIÓN

**Ejemplo 1 — Bernardo pega `/usage` y dice "documenta":**

```
Bernardo:
  /usage
  Total cost: $20.46
  ...
  documenta esta sesión

→ Activar la skill, hacer Fase 1-5, generar USAGE.md.
```

**Ejemplo 2 — Cierre de sprint:**

```
Bernardo: "antes de mergear, registra todo lo que hemos hecho en
          esta rama"

→ Activar la skill. En Fase 2, pedir /usage si no está en contexto.
  En Fase 3, usar git log master..HEAD.
```

**Ejemplo 3 — Sesión sin git (solo conversación):**

```
Bernardo: "guarda el resumen de esta sesión"
  (no hay commits)

→ Saltar Fase 3 git, generar el USAGE.md desde el scope extraído de
  la conversación. Avisar de que no hay traza git.
```

---

## REFERENCIA: estructura típica del USAGE.md de un refactor

(Ejemplo del refactor v2.0 a skills por universidad — referencia visual,
no copiar literal):

- Encabezado con fecha, rama, estado
- Tabla de métricas (5 filas) + tabla de uso por modelo
- "Scope cubierto" con 1-2 frases de contexto
- Una sección por cada `Fase N:` de los commits, con ficheros y
  decisiones
- "Estado final" con: outputs intactos, sanity check pendiente,
  próximo paso
