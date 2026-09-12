# Contrato de grafo y empaquetado

Este contrato local se conserva en v2. La capa adicional de identidad, revisión,
evidencia de nodos e interoperabilidad se define en `references/federation.md`.

## Ontología adaptada

Crear `Grafo/ontology.json` con este esquema (los valores son un ejemplo mínimo, no una ontología fija):

```json
{
  "domain": "Ingeniería de materiales",
  "problem": "Comparar procesos de fabricación para un requisito de resistencia",
  "audience": "Equipo técnico",
  "node_types": ["source", "process", "requirement", "map", "context"],
  "relation_types": {
    "satisfies": {"domain": ["process"], "range": ["requirement"]}
  }
}
```

Añadir solo tipos que ayuden a organizar el problema. No usar `satisfies` si la evidencia solo acredita una propuesta: elegir una relación y procedencia que expresen la incertidumbre.

## Notas

En cada Markdown, usar frontmatter YAML con al menos `id`, `type` y `origin`. Guardar los ids como cadenas escalares en una sola línea. Usar nombres únicos incluso sin distinguir mayúsculas, para portabilidad. Los títulos pueden estar en cualquier idioma; sanear nombres de archivo y usar aliases si hace falta. Evitar enlaces rotos, notas sin contenido y afirmaciones sin procedencia.

```yaml
---
id: process-01
type: process
origin: source_synthesis
---
```

## Fuentes

`Grafo/sources.json`:

```json
{
  "references": [
    {
      "id": "src-001",
      "url": "https://example.org/article",
      "title": "Artículo principal",
      "role": "primary",
      "depth": 0,
      "parent": null,
      "status": "ingested",
      "retrieved_at": "2026-09-10",
      "read_scope": "Texto completo del artículo",
      "note_id": "source-01",
      "retention": "summary_only",
      "reason": ""
    }
  ]
}
```

Valores `role`: `primary`, `reference`, `supplemental`. Conservar una entrada por fuente deduplicada; añadir `occurrences` para apariciones múltiples, `resolved_url`, `version`, `attempts` y `local_paths` cuando sean conocidos. Un archivo aportado puede tener `url: null` si no consta ninguna URL; identificarlo con `input_file` y huella. Cada referencia de primer nivel debe enlazar a su padre y tener profundidad 1. Referencias posteriores requieren `reason` de expansión. Todo elemento excluido, parcial, bloqueado o no disponible necesita `reason`. No inventar fechas o huellas.

## Grafo

`Grafo/graph.json`:

```json
{
  "nodes": [
    {"id": "source-01", "label": "Artículo principal", "type": "source", "path": "Fuentes/Articulo.md", "origin": "source_synthesis"},
    {"id": "process-01", "label": "Proceso A", "type": "process", "path": "Procesos/Proceso A.md", "origin": "source_synthesis"},
    {"id": "requirement-01", "label": "Requisito X", "type": "requirement", "path": "Requisitos/Requisito X.md", "origin": "source_synthesis"}
  ],
  "edges": [
    {"source": "process-01", "relation": "satisfies", "target": "requirement-01", "origin": "source_synthesis", "evidence": [{"source_id": "src-001", "locator": "Sección 3, tabla 2"}]}
  ]
}
```

Origins admitidos: `transcription`, `source_synthesis`, `inference`, `proposal`, `navigation`. Cada arista semántica necesita evidencia con fuente leída y localizador. En inferencias/propuestas, añadir `rationale`; la evidencia acredita las premisas, no la conclusión añadida. Registrar observaciones específicas y límites en las notas. No usar `navigation` para disfrazar una afirmación semántica.

El validador extrae wikilinks como `navigation_links` en una salida independiente; no inventar etiquetas semánticas a partir de proximidad textual. Registrar todas las notas Markdown como nodos, incluidos mapas, contexto y fuente.

## Validación

Ejecutar:

```bash
python3 scripts/validate_pack.py /ruta/al/vault --zip /ruta/entrega.zip
```

El script rechaza ids duplicados, rutas fuera del vault, nodos/relaciones no definidos por la ontología, dominios/rangos incorrectos, evidencia ausente o basada en fuentes no leídas, faltas de procedencia, notas no registradas y wikilinks rotos. Los wikilinks pueden tener alias, encabezado o ruta; los encabezados no se validan. No procesar enlaces dentro de código como wikilinks de navegación. Revisar manualmente enlaces Markdown externos y locales, citas, encabezados y diagramas.

Escribir `Grafo/validation.json` con contadores y estado de cobertura, `Grafo/navigation.json` y `Grafo/manifest.json` con SHA-256; empaquetar con carpeta raíz. El script no realiza recuperación web, no determina si una fuente fue realmente leída y no comprueba la veracidad. La síntesis semántica y la lectura son trabajo del asistente.

## Contexto y actualización

Limitar CONTEXTO a una entrada manejable: problema, alcance, principales hallazgos con ids, decisiones, discrepancias, huecos y recorridos de recuperación. No copiar todo el corpus. En actualizaciones, conservar ids de entidades y cambiar versiones de las fuentes; invalidar o revisar aristas dependientes cuando cambie la evidencia. Mantener un informe de cobertura actual y no prometer que el archivo cargue automáticamente en nuevas conversaciones.
