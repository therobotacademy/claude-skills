---
name: pseudocode-ladder
description: Protocolo de 4 niveles (lógica general → clases → pseudo-código de función → casi-Python opcional) antes de generar código real — modo FORWARD. Modo INVERSO: dado un repo existente, reconstruye la escalera desde el código y genera el vault Obsidian equivalente, auditando decisiones no-delegables implícitas o sin marcar. Usa FORWARD antes de implementar un módulo nuevo o no trivial en Loyola-Gym, el surrogate de soldadura, o cualquier repo con Decision Log activo, o con "valida el pseudo-código de X", "pasa esto por la escalera", "dame los niveles antes de implementar". Usa INVERSO con "genera el vault de pseudo-código de este repo", "reconstruye los niveles desde el código", "auditar el código existente", "documentar hacia atrás", "vault inverso", o al pedir documentar retroactivamente un repo ya implementado. Ofrece FORWARD si piden construir un módulo sin pasar antes por esta validación. No activar para cambios triviales, fixes ya diagnosticados, o scripts desechables sin impacto en el Decision Log.
---

# Pseudocode Ladder

Protocolo de 4 niveles para insertar un checkpoint de auditoría humana entre
"petición de código" y "código ejecutándose", evitando que Claude Code tome
decisiones científicas o de schema de forma implícita mientras genera
infraestructura aparentemente rutinaria.

## Por qué existe

Con acceso directo a ejecutar y editar, Claude Code tiende a saltar de
petición → código funcionando sin pasar por un punto donde el autor audite
la lógica antes de comprometerse a una implementación concreta
(Tool-Induced Myopia). Cada nivel de esta escalera baja de abstracto a
concreto, y en cada nivel se hace explícita la distinción entre:

- **Delegable**: Claude puede resolverlo sin consultar (infraestructura,
  estilo, I/O, logging).
- **No-delegable**: decisión científica, de schema, o de interpretación que
  requiere la firma del autor antes de seguir. Se marca explícitamente en el
  pseudo-código — nunca se resuelve con un default silencioso.

Corregir un error de diseño en Nivel 1 cuesta una frase. Corregir el mismo
error ya materializado en Nivel 4/código real cuesta reescribir función y
tests. El coste de la corrección crece con cada nivel — por eso no se
avanza de nivel sin aprobación explícita del anterior.

## Cuándo usar cada nivel

No todos los módulos necesitan los 4 niveles completos. Como regla general:

- Un módulo de infraestructura pura y bien acotado (una función utilitaria,
  un wrapper de I/O) puede saltar directo a Nivel 3.
- Un módulo que toca schema de datos, invariantes científicas, o el límite
  entre fuente-de-verdad y proyección desechable, debe pasar por los 4
  niveles completos.
- Nivel 4 es siempre opcional: solo se hace si el autor quiere bajar más
  antes de que Claude Code toque el archivo real.

Si hay duda sobre el nivel de entrada, pregunta al autor en qué nivel quiere
empezar en vez de asumir.

## Modo FORWARD: los 4 niveles

### Nivel 1 — Lógica general / arquitectura del módulo

Qué responsabilidad tiene el módulo dentro del pipeline completo, qué entra
y qué sale, con qué otros módulos habla, y qué fronteras debe respetar
(p. ej. patrón fuente-de-verdad → proyección desechable). Formato:

```
MÓDULO: <nombre>

RESPONSABILIDAD:
  <una frase — qué hace y qué NO hace>

POSICIÓN EN EL PIPELINE:
  <upstream> → [ESTE MÓDULO] → <downstream>

FRONTERAS QUE DEBE RESPETAR:
  - NO debe <acoplamiento prohibido 1>
  - NO debe <acoplamiento prohibido 2>
  - SÍ debe <propiedad garantizada, p. ej. determinismo>

DEPENDENCIAS DECLARADAS:
  - <config, módulos previos ya cerrados en el Decision Log>

NO-DELEGABLE EN ESTE NIVEL:
  - <decisión de arquitectura que condiciona todo lo de abajo>
```

### Nivel 2 — Generación de clases / componentes

Qué clases o estructuras de datos existen, qué responsabilidad tiene cada
una, y qué invariantes mantiene. Las invariantes científicas (p. ej.
isolation principle) se expresan aquí como propiedades de la clase — algo
que el constructor garantiza o rechaza — no como comentarios sueltos en
funciones. Formato:

```
class <Nombre>:
  - <qué representa>
  - Atributos: <...>
  - Invariante: <qué garantiza o qué rechaza, y con qué severidad —
    excepción dura vs warning>

DECISIÓN DE DISEÑO NO-DELEGABLE EN ESTE NIVEL:
  - <p. ej. dónde vive una validación: fallo temprano por instancia vs
    fallo tardío sobre el batch completo — no es solo estilo, cambia
    cuándo se detecta una fuga>
```

### Nivel 3 — Pseudo-código a nivel función

Ramas, excepciones y reglas, con las decisiones delegables y no-delegables
marcadas explícitamente. Formato:

```
FUNCTION <nombre>(<inputs>) -> <output>

INPUTS:
  - <input>: <tipo/formato — marcar con CONFIRMAR si no está cerrado>

REGLAS:
  1. <paso>
  2. FOR each <...>:
       a. <paso>
       b. ASSERT <invariante> # <- razón, no solo qué

EXCEPCIONES:
  - <caso límite> → <acción> [NO-DELEGABLE si afecta validez científica]
  - <input inesperado> → ESCALAR (fail loud, nunca fallback silencioso)

DECISIONES DELEGABLES:
  - <...>

DECISIONES NO-DELEGABLES (requieren firma del autor antes de generar código):
  - <...>
```

### Nivel 4 — Casi-Python (opcional)

Pseudo-código con nombres reales del repo, firmas de función reales, y las
decisiones no-delegables representadas como `NotImplementedError` o
excepciones explícitas en vez de resolverse — de forma que el código
"casi-real" no compile ni corra hasta que el autor las cierre. Este nivel
solo se hace si Nivel 3 ya fue aprobado y el autor quiere bajar más antes
de pasarle el archivo real a Claude Code.

## Reglas de proceso

1. **No se avanza de nivel sin aprobación explícita.** Un "aprobado" o
   equivalente del autor es lo que habilita generar el nivel siguiente.
2. **Cada nivel completado que tenga decisiones no-delegables abiertas
   debe listarlas al final**, igual que se acumulan en el Decision Log del
   proyecto — no se resuelven por default ni se posponen silenciosamente.
3. **Si en un nivel se descubre que una decisión "de infraestructura"
   esconde una decisión científica** (como el umbral de tamaño de aula
   apareciendo dentro de lo que parecía solo I/O), se marca no-delegable
   inmediatamente, aunque rompa la clasificación inicial del módulo.
4. **El código real solo se genera después del último nivel aprobado**
   (Nivel 3 o Nivel 4), nunca en paralelo ni "mientras se valida".
5. Al cerrar la escalera completa para un módulo, las decisiones
   no-delegables que quedaron abiertas pasan a ser candidatas directas
   para el Decision Log del proyecto correspondiente.

## Persistencia como manual Obsidian

Cada módulo que completa la escalera deja una nota física en el repo, no
solo una conversación aprobada. El vault resultante es, por construcción,
el manual de estudio del proyecto: quien lo abre en Obsidian navega de la
arquitectura general a la implementación real siguiendo el mismo camino
que se usó para diseñarla.

### Dónde vive

```
docs/design/
├── _index.md                  ← mapa general (agrega Nivel 1 de cada módulo)
├── build-slots.md              ← niveles 1-4 de ESTE módulo, en orden
├── slot-builder-gates.md
└── era-orchestrator.md
```

Un archivo por módulo, nombrado en kebab-case igual que el módulo que
documenta. Se escribe (o actualiza) en el mismo momento en que el autor
aprueba un nivel — nunca se genera todo de golpe al final, para que la
nota crezca en sincronía con el proceso real de decisión.

### Frontmatter canónico

```yaml
---
uid: build-slots
tipo: MODULO
proyecto: loyola-gym
niveles_completados: [1, 2, 3, 4]   # actualizar según se aprueban
decisiones_pendientes: [DL-XXX]      # ids del Decision Log aún sin resolver
tags: [pipeline, schema, dp-bridge]
resumen: >
  Puente unidireccional entre el output del DP y slots.json, el schema
  que consume el loader de PyG.
---
```

- `uid` = nombre del módulo, inmutable, usado para referenciarlo desde
  otras notas y desde el índice.
- `decisiones_pendientes` se vacía a medida que el autor cierra cada
  decisión no-delegable en el Decision Log — la nota nunca queda con una
  decisión resuelta pero con el id todavía listado ahí.

### Cuerpo de la nota

Los cuatro niveles aprobados, en orden, exactamente como se validaron —
sin reescribir ni resumir. Cada decisión no-delegable que en el pseudo-
código llevaba una marca `[NO-DELEGABLE]` se convierte aquí en un
wikilink al Decision Log:

```markdown
- umbral mínimo de estudiantes por classroom → [[DECISION-LOG#DL-042]]
```

Al final de la nota, una sección `## Ver también` con wikilinks a los
módulos upstream/downstream declarados en el Nivel 1 (`POSICIÓN EN EL
PIPELINE`):

```markdown
## Ver también

[[dp-output-loader]]
[[pyg-slot-dataset]]
```

### El índice como mapa de arquitectura

`docs/design/_index.md` se regenera (no se edita a mano) cada vez que se
añade o actualiza un módulo. Su contenido es, básicamente, la
concatenación de los Nivel 1 de todos los módulos ya documentados — el
diagrama de arquitectura completo emerge sin tener que escribirlo aparte:

```markdown
---
tipo: INDEX
proyecto: loyola-gym
total_modulos: <N>
---

# Arquitectura · Loyola-Gym

## Pipeline
SQLite → DP → [[build-slots]] → slots.json → [[pyg-slot-dataset]] → R-GCN

## Módulos documentados
- [[build-slots]] — puente DP → slots.json (niveles 1-4)
- [[slot-builder-gates]] — validación de invariantes por batch (niveles 1-3)

## Decisiones no-delegables aún abiertas
- [[DECISION-LOG#DL-042]] — umbral mínimo de estudiantes
- [[DECISION-LOG#DL-043]] — política ST_x incompletos
```

### Reglas de la persistencia

1. **Escribir al aprobar, no al terminar.** Si el autor aprueba solo
   Nivel 1 y 2 en una sesión, la nota se crea igualmente con esos dos
   niveles y `niveles_completados: [1, 2]` — no se espera a tener los 4.
2. **Nunca transcribir código fuente real dentro de la nota.** El Nivel 4
   (casi-Python) sí vive en la nota porque es pseudo-código de diseño,
   pero una vez que Claude Code genera el archivo `.py` real, la nota no
   se actualiza para reflejarlo línea a línea — el código es la
   implementación; la nota es el diseño que la originó.
3. **Wikilinks solo hacia Decision Log y módulos relacionados**, nunca
   hacia secciones internas de la misma nota — mantiene el grafo de
   Obsidian limpio y evita enlaces circulares triviales.
4. **El índice se regenera, no se parchea a mano.** Al añadir un módulo
   nuevo, reescribe `_index.md` completo a partir de los Nivel 1 de todas
   las notas existentes en `docs/design/`.

## Modo INVERSO: reconstruir la escalera desde código existente

Dado un módulo ya implementado, reconstruye los niveles 1-3 leyendo el
código real y genera la nota Obsidian equivalente. **El objetivo no es
documentar lo que hace el código — es auditar qué decisiones quedaron sin
marcar como tales.** Narrar neutralmente "esto es lo que hace la función"
disfraza defaults silenciosos como si hubieran sido validados; el modo
inverso tiene que hacer lo contrario a eso.

### Principio rector

Todo lo que en modo forward se marca `[NO-DELEGABLE]` *antes* de escribir
código, en modo inverso hay que encontrarlo *dentro* del código ya
escrito — con la sospecha activa de que nunca fue marcado ni decidido
conscientemente. El modo inverso asume que el código puede contener
decisiones científicas disfrazadas de detalles de implementación, y su
trabajo es sacarlas a la luz, no darles legitimidad retroactiva.

### Proceso, en orden (Nivel 4 se omite: el código real ya lo es)

**Paso 0 — Lectura previa.** Antes de reconstruir nada, lee el código del
módulo completo, su historial de commits si está disponible, y cualquier
`DECISION-LOG.md` o equivalente del repo — para saber qué decisiones ya
están documentadas y cuáles no.

**Nivel 3 primero (el más fiable).** Traduce el control de flujo real —
ramas, excepciones, bucles — a pseudo-código, en el mismo formato que el
modo forward. Por cada valor hardcodeado, condición sin comentario
explicativo, o rama sin justificación en código/commits, márcalo:

```
❓ DECISIÓN-IMPLÍCITA-DETECTADA: <qué valor/condición> — sin evidencia de
   haber sido una elección consciente; podría ser arbitraria o un
   placeholder que nadie revisó.
```

No asumas intención donde no hay evidencia. Un `if len(x) < 5` sin
comentario ni test que lo justifique es una decisión implícita detectada,
no "el umbral que el autor decidió usar".

**Nivel 2 después.** Reconstruye las clases reales con sus invariantes
*tal como el código las hace cumplir* — si hay un `assert` o excepción,
esa es la invariante real. Si el forward hubiera esperado una invariante
que el código no implementa (p. ej. no hay ningún control de isolation
principle donde debería haberlo), márcalo:

```
⚠️ INVARIANTE AUSENTE: se esperaría <invariante>, pero el código no la
   verifica en ningún punto. Riesgo: <qué podría fallar silenciosamente>.
```

No rellenes esta sección como si la invariante existiera solo porque
"tendría sentido" que estuviera ahí.

**Nivel 1 al final.** Aquí se detectan violaciones de frontera respecto a
patrones ya cerrados del proyecto (p. ej. SQLite fuente-de-verdad /
proyecciones desechables). Si el módulo importa algo que no debería, o
escribe donde solo debería leer, márcalo:

```
🚫 VIOLACIÓN DE FRONTERA: el módulo <hace X>, lo cual contradice
   <patrón/decisión cerrada de referencia>.
```

No lo documentes neutralmente como si fuera parte del diseño acordado.

### Comportamiento a escala (repos grandes)

Auditoría profunda (Nivel 1-3 con los tres marcadores) es cara en tiempo y
contexto. En un repo con muchos módulos, no se audita todo a ciegas en una
pasada — se hace en dos:

**Pasada 1 — Inventario ligero (barato, cubre todo el repo).** Para cada
módulo, sin generar la nota completa, solo se extraen señales de riesgo:

- ¿Toca schema de datos, serialización, o un límite ya cerrado en el
  Decision Log (p. ej. SQLite fuente-de-verdad / proyección desechable)?
- ¿Tiene literales numéricos sin nombrar (`< 5`, `== 3`) sin test que
  los cubra?
- ¿Tiene `assert`/`raise` (posibles invariantes) o carece de ellos donde
  el nombre o la posición en el pipeline sugeriría que debería tenerlos?
- ¿Aparece ya referenciado como decisión abierta en el Decision Log?

El resultado es una **tabla de triaje**, no notas Obsidian:

```
| módulo             | LOC | toca schema | literales sin nombrar | invariantes | prioridad |
|--------------------|-----|-------------|------------------------|-------------|-----------|
| build_slots.py     | 80  | sí          | 2                      | 1           | alta      |
| logging_utils.py   | 40  | no          | 0                      | 0           | baja      |
```

**Priorización — decisión del autor, no del triaje.** El triaje sugiere,
no decide. Presenta la tabla y pregunta qué módulos entran en pasada 2 en
vez de auditar automáticamente todo lo marcado "alta" — la prioridad
sugerida es una señal, no una orden.

**Pasada 2 — Auditoría profunda, solo donde el autor la pidió.** Se
ejecuta el proceso completo (Nivel 3 → 2 → 1, con ❓/⚠️/🚫) módulo por
módulo, escribiendo cada nota a disco inmediatamente al terminarla —
nunca se acumulan varios módulos en memoria/contexto antes de persistir.
Esto permite que el proceso escale a repos grandes sin depender de cuánto
quepa en una sola respuesta.

**Módulos no auditados a fondo no se omiten del vault — se marcan como
superficiales.** Reciben una nota con solo Nivel 1 (reconstrucción rápida
de responsabilidad + posición en pipeline) y este campo:

```yaml
profundidad: superficial   # vs "completa" para los que pasaron por auditoría de 3 niveles
```

Así el vault queda completo y navegable desde el primer momento — el
índice lista todos los módulos — pero es honesto sobre cuáles tienen
auditoría real de decisiones implícitas y cuáles son solo un mapa
provisional.



```yaml
---
uid: <nombre-del-módulo>
tipo: MODULO
proyecto: <nombre>
origen: reverse-engineered          # marca que esto se reconstruyó, no se diseñó así
profundidad: completa                # completa (3 niveles auditados) | superficial (solo Nivel 1)
niveles_completados: [1, 2, 3]      # Nivel 4 no aplica en modo inverso
decisiones_pendientes: []           # las YA cerradas y documentadas en el Decision Log
decisiones_implicitas_detectadas:   # las que el código toma sin haber sido validadas
  - "umbral hardcodeado en línea 47, sin justificación en código ni Decision Log"
invariantes_ausentes: []            # lista de ⚠️ encontrados, si los hay
violaciones_frontera: []            # lista de 🚫 encontrados, si los hay
tags: [reverse-engineered, ...]
resumen: >
  Reconstrucción retroactiva. <N> decisiones implícitas detectadas sin
  documentar; requieren revisión y, si corresponde, alta en el Decision Log.
---
```

La distinción entre `decisiones_pendientes` (ya identificadas y en
proceso normal de cierre) y `decisiones_implicitas_detectadas` (encontradas
por auditoría, sin que nadie las hubiera señalado antes) debe mantenerse
siempre separada — mezclar ambas listas oculta cuáles son hallazgos nuevos
de la auditoría.

### Entregable de cierre

Al terminar la auditoría de un módulo, antes de escribir la nota, presenta
al autor un resumen corto de:

1. Cuántas `❓ DECISIÓN-IMPLÍCITA-DETECTADA`, `⚠️ INVARIANTE AUSENTE`, y
   `🚫 VIOLACIÓN DE FRONTERA` se encontraron.
2. Cuáles de ellas, a tu juicio, tienen impacto potencial sobre validez
   científica o resultados (Recall@3/HitRate@3, o el claim relevante del
   proyecto) — para que el autor decida cuáles promueve al Decision Log
   como entradas nuevas.

No promuevas automáticamente ningún hallazgo al Decision Log — esa
decisión, como todas las no-delegables, es del autor.

## Ejemplo de referencia

Ver `references/build_slots_example.md` para el recorrido completo de los
4 niveles en modo forward aplicado a `build_slots.py` (Loyola-Gym, Phase
3: bridging DP output → `slots.json`), incluyendo el Nivel 4 en casi-Python
y el formato final de la nota Obsidian correspondiente.
