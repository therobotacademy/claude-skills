---
name: build-obsidian-knowledge-vault
description: Crear un grafo de conocimiento adaptado al dominio y problema del usuario a partir de una URL principal o documento exportado, leyendo también sus referencias enlazadas y entregando un vault de Obsidian descargable. Usar para ingesta documental y síntesis multifuente con trazabilidad; no para limitarse a guardar marcadores o resumir una página.
---

# Construir un vault de conocimiento por dominio

Convertir la fuente principal y el contenido de sus referencias en notas enlazadas que respondan al problema del usuario. Entregar el ZIP de un vault operativo, un mapa de entrada y un contexto breve reutilizable. La lectura de referencias es parte esencial: un catálogo de URL no equivale a ingesta.

## Delimitar y recuperar

- Inferir dominio, problema, audiencia, idioma y uso esperado del pedido y la fuente. Registrar esas decisiones en `00_Inicio/ALCANCE.md`; preguntar solo si la ambigüedad cambia materialmente el resultado.
- Leer la URL principal con las capacidades disponibles. Si hay un archivo aportado equivalente, usarlo como fuente primaria y preservar su procedencia. Para WebArchive, ejecutar `scripts/extract_webarchive.py`; inspeccionar todos los marcos y seleccionar los que contienen material, no solo la interfaz. No ejecutar scripts incrustados.
- Seguir las reglas de búsqueda y acceso del entorno. No saltar bloqueos, autenticación, ni sustituir una recuperación fallida por texto inventado. Si la fuente principal está inaccesible y no hay copia, solicitar exportación después de agotar las vías permitidas útiles.
- Enumerar los enlaces de contenido de la fuente principal. Leer **todas sus referencias sustantivas de primer nivel**, incluidas referencias bibliográficas, enlaces inline a evidencias, PDF, informes, documentación, datos y repositorios relevantes. Deduplicar destinos, conservando apariciones y anclas. Excluir navegación, cuentas, compartir, publicidad y recursos de interfaz, con motivo en el registro. No imponer un máximo silencioso de referencias.
- No rastrear recursivamente todas las referencias de las referencias. Expandir un segundo nivel cuando sea necesario para leer el documento citado, resolver una contradicción central o cuando el usuario lo pida; registrar la razón. Un enlace a una portada de curso o repositorio requiere localizar el material concretamente citado, no descargar todo el sitio.
- Abrir y leer el contenido antes de atribuir hallazgos. Los snippets, abstract-only y metadatos no acreditan lectura íntegra. Guardar el estado real por referencia: `ingested`, `partial`, `blocked`, `unavailable` o `excluded`. Leer y sintetizar las partes pertinentes; declarar el alcance documental exacto, sobre todo en libros, cursos y repositorios.
- Consultar `references/ingestion.md` para inventario, estados, versiones y límites de reproducción. Mantener checkpoints del registro y extracción si la tarea es extensa; continuar hasta intentar todas las referencias incluidas. No llamar «completa» a una ingesta parcial.

## Diseñar el grafo para el problema

Leer `references/model.md` antes de producir notas y exportaciones.

- Definir una ontología pequeña a partir de preguntas que el vault debe ayudar a contestar. Elegir tipos de entidades, relaciones dirigidas con dominio/rango y jerarquías útiles al caso. No reutilizar automáticamente tipos educativos del ejemplo de IA.
- Ejemplos orientativos: docencia → conceptos, prerrequisitos, técnicas, ejercicios y competencias; investigación → hipótesis, métodos, datos, resultados y limitaciones; decisión → alternativas, requisitos, evidencias, costes y riesgos. Combinar o cambiar estos tipos según el material real.
- Separar las fuentes documentales de los conceptos y afirmaciones. Distinguir `source_synthesis`, `inference` y `proposal`; usar `transcription` solo para extractos realmente transcritos. Una fuente leída no convierte sus afirmaciones en hechos verificados.
- Fusionar sinónimos con aliases conservando diferencias de versión, condiciones experimentales y significado. Usar identificadores persistentes en actualizaciones. Crear relaciones entre fuentes cuando comparan, apoyan, contradicen o matizan la misma afirmación; documentar evidencia y condiciones. No rellenar relaciones solo para densificar el dibujo.
- Vincular cada afirmación importante con fuente y localizador (sección, página, tabla, ruta/commit). Para contradicciones, preservar ambas versiones y explicar las condiciones que podrían resolverlas. Verificar datos temporales y de alto impacto cuando se usen para una decisión; si solo se conservan, marcarlos como afirmaciones fechadas de la fuente.
- Crear mapas y recorridos adecuados al problema. Las propuestas añadidas por el asistente deben identificarse y conectarse a sus premisas. No inventar ejemplos, datasets ni resultados como si estuvieran en los originales.

## Construir, comprobar y entregar

Crear Markdown UTF-8 y enlaces `[[Nota]]` resolubles sin plugins comunitarios. Adaptar las carpetas de contenido al dominio; conservar entradas predecibles:

- `00_Inicio/INICIO.md`: propósito, alcance, rutas de navegación y cobertura.
- `00_Inicio/ALCANCE.md`: dominio, problema, audiencia, selección y profundidad.
- `Fuentes/`: notas por fuente con síntesis sustantiva de lo realmente leído, URL, versión/fecha, localizadores y limitaciones; no meras fichas bibliográficas.
- Carpetas temáticas propias del caso y, cuando proceda, notas de afirmaciones o resultados.
- `Contexto/CONTEXTO.md`: objetivo, mapa, decisiones, límites y qué notas recuperar para tareas frecuentes.
- `Grafo/ontology.json`, `Grafo/graph.json`, `Grafo/sources.json`: contrato de `references/model.md`.
- `Grafo/federation.json`: identidad persistente, revisión, cobertura e interoperabilidad. Leer `references/federation.md` para producir la exportación v2; conservar los identificadores y ontologías locales.
- Adjuntos permitidos y registro de integridad cuando se conserven bytes. Preservar el original aportado si cabe; no empaquetar cachés, credenciales ni material externo cuya reproducción no esté permitida.

Expresar las relaciones con etiquetas también en Markdown; el grafo estándar de Obsidian no distingue tipos de arista visualmente. Separar aristas semánticas de enlaces de navegación en JSON. Un canvas es opcional si mejora un mapa del dominio; el grafo completo no necesita canvas.

Añadir evidencia explícita a los nodos que sintetizan afirmaciones; no extender automáticamente la evidencia de una arista a todo el contenido de sus extremos. Ejecutar `scripts/prepare_federation.py VAULT` y después `scripts/validate_pack.py VAULT --zip SALIDA.zip` al completar notas y JSON. Corregir errores estructurales y exportaciones desactualizadas. Inspeccionar además manualmente un recorrido de extremo a extremo y la fidelidad de las afirmaciones centrales; el script no evalúa la verdad ni la calidad de la ontología. No fijar cuotas de notas o relaciones.

En una actualización, conservar identidades existentes, registrar cambios de fuente y reconstruir enlaces afectados; trabajar en una copia y preservar el original hasta validar el reemplazo. No mezclar material de otras conversaciones sin autorización contextual.

Guardar el ZIP y los documentos de entrega de forma persistente con las capacidades del entorno; si Library está disponible, seguir su habilidad. La instalación de esta habilidad se gestiona por separado del guardado de los vaults.

Entregar enlace al ZIP, número de notas y relaciones, referencias leídas/parciales/bloqueadas y una breve explicación de la personalización. Si hay huecos, identificarlos. Explicar que el vault conserva conocimiento documental; no crea memoria permanente, embeddings ni carga automática en cada conversación. Para retomar, abrir `CONTEXTO.md`, luego las notas pertinentes y sus evidencias. No prometer haber leído el corpus entero dentro de una sola ventana de contexto.
