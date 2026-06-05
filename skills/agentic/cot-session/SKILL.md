---
name: session-cot
description: |
  Genera un documento Chain of Thought (CoT) que reconstruye el hilo de razonamiento seguido durante una sesión de trabajo compleja: qué inferencias se hicieron, por qué se tomaron las decisiones de diseño, qué patrones de razonamiento se repitieron, y qué hallazgos resultaron de búsquedas o verificaciones externas.

  Activa este skill SIEMPRE que Bernardo diga "escribe el CoT", "documenta el razonamiento de la sesión", "genera el chain of thought", "registra cómo razonaste", "CoT de la sesión", o cualquier variante que implique reconstruir el proceso de pensamiento de una conversación. También actívalo al final de sesiones largas de diseño arquitectónico, especificación de sistemas, o resolución de problemas complejos cuando Bernardo pida "cierra la sesión" o "consolida lo que hicimos".

  El output es un documento markdown estructurado por pasos numerados, cada uno con: Input (qué llegó), Razonamiento (cómo se procesó), e Inferencia clave (qué conclusión no-obvia emergió). Termina con una sección de patrones recurrentes observados en la sesión. No es un resumen del output — es la traza del proceso.
---

# Session CoT

Genera un Chain of Thought que reconstruye el razonamiento de una sesión.

## Diferencia crítica con un resumen

Un resumen describe **qué** se produjo. El CoT describe **cómo** se llegó ahí: qué inferencias se hicieron, qué se verificó antes de responder, qué decisiones de diseño se tomaron y por qué, qué alternativas se descartaron, qué patrón de razonamiento conectó ideas que parecían inconexas.

## Estructura del documento

```
# Chain of Thought — {título de sesión}
{contexto, fecha}

## Resumen del razonamiento
1 párrafo que encuadra el arco de la sesión.

## Paso N — {nombre del paso}
**Input:** qué llegó (documento, pregunta, idea)
**Razonamiento:** cómo se procesó — qué se verificó, qué se descartó, qué tradeoffs se evaluaron
**Inferencia clave:** la conclusión no-obvia que no estaba en el input (si existe)

[repetir por cada decisión significativa]

## Patrones de razonamiento que se repiten en esta sesión
Lista de los 3-5 heurísticas que atravesaron toda la sesión.
```

## Criterios para incluir un paso

Incluir: decisiones de diseño con alternativas evaluadas, verificaciones externas (búsquedas, fetches) que cambiaron el rumbo, inferencias que conectaron contexto de sesiones pasadas con el problema actual, diagnósticos de "hueco de mercado" o "ya lo tienes construido".

Excluir: pasos mecánicos sin decisión (e.g., "descargué el documento"), outputs puramente ejecutivos sin razonamiento asociado.

## Patrones de razonamiento a identificar

Los siguientes aparecen con frecuencia en el trabajo de Bernardo — señalarlos cuando aparezcan:

- **Verify before generating** — búsqueda o fetch antes de responder sobre estado externo
- **Converge sobre el hueco** — análisis orientado a encontrar el espacio vacío, no a listar todo
- **Stubs como contratos** — código incompleto con interfaz definida vs. trabajo diferido sin dueño
- **Separación operativo/identidad/conocimiento** — `CLAUDE.md` / `SOUL.md` / `workspace/`
- **Boundary = interfaz humana** — diseñar lo que el usuario NO tiene que tocar como decisión de producto
- **70% certainty threshold** — actuar sobre inferencia suficientemente confiada sin esperar certeza total
- **DÉDALO aplicado** — perspectivas múltiples antes de consolidar una posición
- **Spec-Driven discipline** — constitution → spec → clarification → plan → tasks → implement, en orden

## Output

Respuesta directa en la conversación (markdown). No crear fichero a menos que Bernardo lo pida explícitamente con "guárdalo" o "en un fichero".

El tono es técnico-analítico, primera persona desde la perspectiva del agente que razonó. No es un log ni una auditoría — es una traza de pensamiento legible por un colaborador humano que quiera entender por qué el sistema tomó las decisiones que tomó.
