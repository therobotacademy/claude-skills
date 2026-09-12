# Exportación federada v2

Leer al producir o actualizar cualquier vault destinado a consultas conjuntas.
El formato es aditivo: no reemplazar `ontology.json`, `graph.json`, `sources.json`
ni los identificadores locales. Los vaults canónicos anteriores siguen siendo v1.

## Identidad y contrato

Crear `Grafo/federation.json` con `scripts/prepare_federation.py VAULT` después de
completar las notas y los tres JSON. El script valida primero el contrato local.
Genera `schema_version: "2.0"`, un `vault_id` UUID persistente, `revision` SHA-256,
`title`, `domain`, `problem`, `languages`, `topics`, `coverage`, `files`,
`source_identities` y `type_mappings`. Declarar idiomas y temas con argumentos
`--language es --language en --topic RLVR`; no inferir cobertura por el nombre.

La identidad de una nota es la pareja `(vault_id, node_id)`; las fuentes usan
`(vault_id, source_id)`. No concatenar identificadores con delimitadores ambiguos.
Conservar el UUID al mover, renombrar, copiar para actualizar o reindexar el vault.
Usar `--fork` solo al crear una derivación que deba evolucionar independientemente.
Las rutas locales y las URI de Obsidian son localizadores, no identidades.

`revision` cubre los bytes de notas registradas y los tres JSON canónicos; excluye
el propio sidecar, informes, índices y adjuntos. El manifiesto de empaquetado
sigue cubriendo también los adjuntos. Si cambian fuentes, notas o relaciones,
revisar sus derivados y volver a preparar/exportar. Nunca presentar un hash
coincidente como comprobación de verdad o vigencia externa.

## Evidencia y compatibilidad semántica

Añadir `evidence: [{"source_id": "src-001", "locator": "Sección 3"}]` a los
nodos que sintetizan afirmaciones. La evidencia de un nodo acredita la nota;
la de una arista acredita solo esa relación, no todas las frases de sus extremos.
Una referencia parcial conserva `read_scope` y `reason`. Fuentes bloqueadas,
no disponibles o excluidas no pueden acreditar nodos ni aristas.
La evidencia de nota es de grano grueso: dividir afirmaciones en notas o aportar
localizadores precisos si se necesita atribución a nivel de afirmación.

Mantener las ontologías locales. `type_mappings` es un objeto opcional
`{"tecnica": "method"}` para correspondencias de tipos aprobadas al diseñar el
vault. No supone equivalencia entre entidades. Dejarlo vacío si no hay una
correspondencia defendible. No convertir similitud vectorial en `same_as`.

Las identidades documentales se proponen por DOI, huella o URL conservadora;
preservar versión, condiciones y todas las apariciones. URL sin versión es un
candidato a duplicado, no prueba de que los contenidos coincidan.

## Relaciones externas

Mantener las relaciones entre vaults en un registro de federación externo, para
que los wikilinks y el validador local no dependan de otros vaults. Cada entrada:

```json
{
  "id": "bridge-001",
  "source": {"vault_id": "urn:uuid:…", "node_id": "method-01", "revision": "sha256…"},
  "target": {"vault_id": "urn:uuid:…", "node_id": "method-02", "revision": "sha256…"},
  "relation": "compares_with",
  "origin": "inference",
  "rationale": "Comparación propuesta a partir de las condiciones documentadas.",
  "evidence": [{"vault_id": "urn:uuid:…", "source_id": "src-001", "revision": "sha256…", "locator": "Tabla 2"}]
}
```

El registro declara `relation_types` con dominio/rango de tipos locales
cualificados por vault. Su consumidor comprueba extremos, tipos, evidencia y
revisiones contra el catálogo registrado. Invalidar conservadoramente puentes
si cambia cualquiera de las revisiones fijadas; revisarlos antes de reactivarlos.
No activar relaciones externas pendientes ni derivarlas de enlaces de navegación.

## Orden de entrega

1. En actualizaciones, trabajar sobre copia preservando identidades.
2. Revisar evidencia de nodos y aristas; conservar huecos reales.
3. Ejecutar `prepare_federation.py`, luego `validate_pack.py VAULT --zip SALIDA.zip`.
4. Informar UUID, revisión y cobertura en el informe si es útil para el servicio.

No incluir bases de datos de búsqueda, embeddings, tokens ni credenciales dentro
del vault. El servicio de consulta construye derivados aparte y debe declarar
si usa solo texto, búsqueda híbrida o generación con LLM. Esta exportación no
despliega un servicio ni conecta automáticamente el vault a ChatGPT.
