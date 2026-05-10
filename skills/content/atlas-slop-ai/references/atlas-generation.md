# Generación del Atlas HTML — Guía operativa

Esta referencia explica cómo producir el artefacto HTML interactivo a partir de los artículos clasificados. Léela solo cuando vayas a generar formato ATLAS o AMBOS.

---

## Cuándo generar el atlas

El HTML interactivo aporta valor real solo a partir de cierto volumen. Reglas:

- **<8 artículos**: no generes atlas. Una clasificación textual es más útil. Si Bernardo lo pide explícitamente, hazlo, pero advierte que con pocas entradas la matriz queda casi vacía.
- **8–15 artículos**: genera atlas si Bernardo lo pide; si no, ofrécelo al final de la clasificación textual ("¿quieres también el atlas interactivo?").
- **>15 artículos**: genera atlas por defecto (modo AMBOS) salvo que Bernardo pida solo clasificación.

---

## Pasos para generar

### 1. Lee la plantilla

```
view /mnt/skills/user/slop-atlas/assets/atlas-template.html
```

La plantilla contiene marcadores claros para los puntos de inyección:

- `<!-- @TITLE -->` — el `<title>` del documento
- `<!-- @MASTHEAD_DATE -->` — la fecha que aparece en el masthead derecho
- `<!-- @SOURCE_LABEL -->` — el subtítulo de la fuente (e.g. "Newsletter Digest 2026-05-09 11:00")
- `<!-- @ARTICLES_DATA -->` — el array JS de artículos (donde va la mayor parte del trabajo)

### 2. Construye el array de artículos

Cada artículo es un objeto JS con esta estructura:

```javascript
{
  id: 1,                              // entero único
  date: "09 May",                     // formato corto, igual al digest original
  time: "01:08",                      // HH:MM 24h
  source: "Latent Space / AINews",    // fuente legible
  title: "Anthropic growing 10x/year while everyone else is laying off",
  abstract: "Anthropic alcanza valoración de $1–1.2T...",  // copiado del digest
  ai: true,                           // clasificación eje 1
  slop: false,                        // clasificación eje 2
  rationale: "AI-assisted aggregation con datos primarios verificables...",  // 1-2 frases
  url: "https://www.latent.space/p/ainews-anthropic-growing-10xyear"  // o ""
}
```

**Reglas para los campos**:

- **`abstract`**: usa el del digest original sin reescribir. Si es muy largo (>400 chars), trúncalo con `…` al final.
- **`rationale`**: 1-2 frases que expliquen *por qué* ese cuadrante. Estilo: específico, evita generalidades. Mal: "Tiene tesis y datos." Bien: "Cifras concretas verificables (latencias, contexto, benchmarks externos). Síntesis con sustrato real."
- **`url`**: usa la URL del enlace "Artículo" del digest si existe. Si solo hay enlace de Gmail, deja `""` (la plantilla maneja el caso vacío).
- **`ai` y `slop`**: booleanos sin matices intermedios. Si tu confianza es <60% declárala en el `rationale` ("Clasificación tentativa: ..."), pero el booleano debe ser firme.

### 3. Sustituye en la plantilla

Reemplaza:
- `<!-- @TITLE -->` por `Slop Atlas · Newsletter Digest <YYYY-MM-DD>`
- `<!-- @MASTHEAD_DATE -->` por `Bernardo · <YYYY-MM-DD>`
- `<!-- @SOURCE_LABEL -->` por `Newsletter Digest <YYYY-MM-DD> <HH:MM>`
- `<!-- @ARTICLES_DATA -->` por el array completo

### 4. Guarda y presenta

```
write /mnt/user-data/outputs/slop_atlas_<YYYY-MM-DD>.html
```

Después llama a `present_files` con esa ruta.

---

## Manejo de casos especiales

### Abstract ausente

Si Bernardo pega solo títulos + fuentes sin abstract, genera un placeholder:
```
abstract: "[Sin abstract en el digest. Clasificación basada solo en título y fuente — confianza reducida.]"
```
Y baja explícitamente la confianza del rationale.

### URL ausente

Deja `url: ""`. La plantilla muestra automáticamente "— sin enlace directo —" con opacidad reducida.

### Caracteres especiales

Los abstracts del digest original pueden tener entidades HTML (`&aacute;`, `&iacute;`, `&mdash;`). Decodifícalas a UTF-8 antes de inyectar. La plantilla usa UTF-8 nativo.

### Strings con comillas

Si un título o abstract contiene comillas dobles, escápalas en el JS:
```javascript
title: "\"Chrome Is a Surveillance Platform\" and 4 more"
```

O usa template literals con backticks si el contenido es simple (sin backticks internos).

### Más de 100 artículos

La plantilla está optimizada hasta ~80 artículos. Si el digest tiene más, considera dividir en dos atlas (e.g. "principal" y "archivo") o avisa a Bernardo de que puede haber lentitud al filtrar.

---

## Después de generar

Tras presentar el archivo, escribe en chat 2-4 observaciones que emerjan del análisis agregado, no de artículos individuales. Ejemplos del tipo de observación útil:

- **Patrones por autor**: "Mehul Gupta divide su producción entre IA·NO-SLOP (los técnicos con cifras) e IA·SLOP (los listicles 'I Actually Use')."
- **Patrones por género**: "Todos los HUM·SLOP de hoy son listicles de wellness o resiliencia laboral con gancho IA decorativo."
- **Anomalías interesantes**: "Único artículo en IA·NO-SLOP que se autodeclara: 'In Defense of AI Slop' — la transparencia es la fricción que lo saca del cuadrante slop."
- **Implicaciones para suscripciones**: "El cuadrante IA·NO-SLOP captura los roundups útiles. Si quisieras reducir suscripciones, los HUM·SLOP son los primeros candidatos para cancelar."

No repitas el contenido de la matriz — ya está en el HTML. Las observaciones agregan lo que la matriz por sí sola no revela.

---

## Anti-patrones en la generación

**No reescribas la plantilla CSS**. Está calibrada para coherencia con el resto de artefactos editoriales de Bernardo (IBM Plex Serif + Mono, paleta neutra, estructura editorial). Cualquier cambio estético debe ser una decisión consciente, no una "mejora" arbitraria.

**No traduzcas los abstracts**. Si el digest los tiene en español, mantenlos. Si en inglés, mantenlos. La consistencia del input es valor.

**No inventes URLs**. Si no hay URL en el digest original, deja `""`. No completes con búsquedas web ni con suposiciones.

**No clasifiques sobre el placeholder**. Si Bernardo manda un digest incompleto sin abstracts, no rellenes con clasificaciones inventadas. Marca explícitamente la falta de información en cada `rationale`.

**No mezcles formatos en la salida**. Si el modo es ATLAS, todo va al HTML. Si es CLASIFICACIÓN, todo va al chat. Si es AMBOS, primero la clasificación textual breve en chat, después el HTML como archivo. No empieces a redactar análisis extensos en chat antes del archivo — Bernardo abrirá el archivo y querrá ver el resumen ahí.
