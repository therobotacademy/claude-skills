# Contexto de creación de `build-obsidian-knowledge-vault`

**Propósito de este documento:** recuperar el razonamiento, las decisiones y los límites que originaron la habilidad, para continuar su evolución sin confundir el vault documental con una memoria automática del asistente.

## Punto de partida

El origen fue la preparación de materiales para clases de IA Generativa a partir de un artefacto de Claude, inicialmente accesible mediante URL. La URL no pudo recuperarse desde el entorno; se pidió una exportación. El archivo aportado —un WebArchive— sí permitió extraer el artículo **«El hueco del post-entrenamiento»** y catalogar 16 referencias enlazadas.

El material trataba, entre otros asuntos, RLVR, GRPO, razonamiento, evaluación, recompensas espurias, escalado en inferencia y modelos de imagen. Su uso previsto era docente: reorientar contenidos, ejemplos, prácticas y debates de la asignatura de IA Generativa.

## Problema que debía resolver la habilidad

No bastaba con guardar una página o producir un resumen. Se necesitaba transformar una fuente principal y sus referencias relevantes en un **grafo de conocimiento reutilizable**, adaptado al dominio y al problema del usuario, que pudiera:

- abrirse y editarse en Obsidian;
- conservar el original y la trazabilidad de cada afirmación;
- separar contenido extraído de inferencias y propuestas didácticas;
- localizar rápidamente conceptos, ejemplos, ejercicios, fuentes y huecos;
- servir como contexto recuperable para preparar una clase sin cargar el corpus entero en cada conversación;
- exportarse como ZIP portable.

La discusión distinguió explícitamente entre **conservar información** y **tenerla permanentemente en la ventana de contexto**. El vault debía ser una base documental persistente, no una promesa de memoria permanente, embeddings automáticos ni carga íntegra en conversaciones futuras.

## Decisiones de diseño originales

### El vault debía responder a un problema, no imponer una taxonomía

La ontología debía derivarse del dominio y de las preguntas que el vault ayuda a contestar. Se definieron ejemplos orientativos, no una plantilla universal:

| Contexto | Tipos útiles de nota |
|---|---|
| Docencia | conceptos, prerrequisitos, técnicas, ejercicios y competencias |
| Investigación | hipótesis, métodos, datos, resultados y limitaciones |
| Decisión | alternativas, requisitos, evidencias, costes y riesgos |

Para el primer caso de IA Generativa, la estructura incluyó conceptos, técnicas, modelos, recursos, prácticas y rutas docentes. En otro caso de fabricación se comprobó que el modelo debía conservar resultados aparentemente contradictorios bajo distintas condiciones, en vez de forzar una conclusión única.

### Las fuentes no son las afirmaciones

Se decidió separar las notas de fuente de las notas de conceptos y afirmaciones. Cada contenido derivado debía declarar su procedencia como una de estas categorías:

- `transcription`: extracto transcrito de la fuente.
- `source_synthesis`: síntesis de material realmente leído.
- `inference`: conclusión añadida a partir de evidencias declaradas.
- `proposal`: propuesta del asistente, por ejemplo un ejercicio o una reorganización docente.

Una fuente leída no convierte automáticamente todas sus afirmaciones en hechos comprobados. Las relaciones semánticas debían incorporar evidencia y localizador; las inferencias y propuestas, además, su razonamiento.

### La lectura de referencias era requisito, no adorno

La habilidad nació tras detectar que un listado de URLs no equivale a una ingesta. Debe:

1. enumerar los enlaces sustantivos de primer nivel de la fuente principal;
2. recuperar y leer su contenido antes de atribuir hallazgos;
3. registrar por cada referencia `ingested`, `partial`, `blocked`, `unavailable` o `excluded`;
4. documentar el motivo de cualquier alcance incompleto;
5. no rastrear recursivamente enlaces sin límite: ampliar a segundo nivel solo si resuelve una contradicción central, permite leer lo citado o el usuario lo pide.

En el ejemplo inicial, las 16 referencias quedaron correctamente catalogadas pero **no se declararon leídas**, porque el archivo no contenía sus textos externos. Esta limitación debía aparecer en el informe y en el contexto, no esconderse bajo la etiqueta de ingesta completa.

### El grafo debía ser portable y verificable

Los vaults se diseñaron con Markdown UTF-8 y enlaces Obsidian resolubles sin plugins comunitarios. Se definieron tres artefactos estructurados:

- `Grafo/ontology.json`: dominio, problema, audiencia, tipos de nodo y relaciones admitidas;
- `Grafo/graph.json`: nodos, aristas tipadas, origen y evidencia;
- `Grafo/sources.json`: fuentes, jerarquía, estado de lectura, alcance y retención.

El validador debía comprobar identidades, notas registradas, rutas seguras, tipos, dominios/rangos de relaciones, enlaces internos y evidencia basada únicamente en fuentes leídas o parcialmente leídas. También generaría manifiesto de integridad, informe de validación y navegación extraída.

La validación estructural no acredita veracidad, calidad de la ontología, lectura real de una fuente ni fidelidad de la síntesis. Es una barrera contra errores mecánicos, no una prueba epistemológica.

## Entregables fijados

Cada ejecución de la habilidad debía producir:

| Ruta | Función |
|---|---|
| `00_Inicio/INICIO.md` | propósito, alcance, navegación y cobertura |
| `00_Inicio/ALCANCE.md` | dominio, problema, audiencia y profundidad de la ingesta |
| `Fuentes/` | notas de fuentes realmente leídas, con limitaciones |
| Carpetas temáticas | notas propias del dominio y de sus preguntas |
| `Contexto/CONTEXTO.md` | entrada compacta para reanudar el trabajo y recuperar evidencia |
| `Grafo/` | ontología, grafo, fuentes y resultados de validación |
| ZIP | vault listo para abrir en Obsidian |

El informe de entrega debía indicar número de notas y relaciones, cobertura de fuentes, huecos y el grado de personalización del grafo.

## Validación que motivó la reutilización

La primera aplicación sobre el WebArchive de IA Generativa produjo un vault con **52 notas y 38 relaciones semánticas**. El contexto docente, el informe de ingesta y las referencias pendientes se guardaron junto a la exportación.

La habilidad también se comprobó en un caso sintético de fabricación. La prueba conservó por separado resultados en seco y en humedad, dejó una decisión abierta cuando faltaban datos, y rechazó una relación sin evidencia. Esa prueba confirmó dos principios:

- el grafo debe representar condiciones y discrepancias, no homogeneizar resultados;
- el validador debe impedir relaciones que parezcan informativas pero carezcan de soporte documental.

## Límites de alcance originales

- No sortear autenticación, bloqueos ni restricciones de acceso.
- No atribuir contenido no recuperado a una URL ni inventar referencias, resultados o datasets.
- No llamar completa a una ingesta parcial.
- No mezclar contenido de otras conversaciones sin autorización contextual.
- No incluir credenciales, cachés o material que no pueda redistribuirse.
- No prometer que abrir el vault active automáticamente un RAG, cree embeddings, cargue el contenido en ChatGPT o sustituya el juicio docente.

## Evolución posterior relevante

La habilidad original se amplió con una exportación federada v2 para un **swarm de vaults**. Esa capa añadió un UUID persistente por vault, revisión criptográfica, cobertura y una identidad global formada por `(vault_id, node_id)`. También separó la evidencia de una nota de la evidencia de una relación, para que una arista no acredite indebidamente todo el contenido de sus extremos.

Posteriormente se construyó un servicio local de consulta: catálogo común, índice incremental, búsqueda textual y semántica opcional, expansión controlada por grafo y respuestas con paquetes de evidencias. Se añadió un trabajador de arXiv con descubrimiento, selección de vault, deduplicación por versión, bandeja de revisión e ingesta declarada como parcial cuando solo existe abstract o extracción HTML incompleta.

Estas extensiones no alteran el objetivo original: el vault sigue siendo la autoridad documental legible y portable; el índice y los modelos son derivados reemplazables.

## Cómo retomar el trabajo

1. Abrir `Contexto/CONTEXTO.md` y `00_Inicio/ALCANCE.md`.
2. Recuperar las notas y fuentes pertinentes a la tarea concreta, no el corpus entero.
3. Tratar como evidencia únicamente las fuentes y localizadores registrados como leídos.
4. Señalar con claridad cualquier síntesis, inferencia o propuesta nueva.
5. Al actualizar, preservar identidades y revisar las relaciones afectadas.

La evolución hacia OKF se planteó para hacer aún más explícitos procedencia, generación, verificación, ciclo de vida y vigencia de cada concepto, preservando los controles de evidencia y federación propios de esta habilidad.
