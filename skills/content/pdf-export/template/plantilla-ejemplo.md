:::: {custom-style="Title"}
[Título del trabajo]
::::

:::: {custom-style="Subtitle"}
[Subtítulo opcional]
::::

[Autor] · [Fecha]

## Cómo usar esta plantilla

Este documento es la **plantilla de estilo** `plantilla-academica-brj.docx` mostrada en funcionamiento. No contiene un trabajo real: contiene las instrucciones de uso y una galería de cada estilo. Bórralo de contenido y escribe el tuyo, o copia los bloques que necesites.

La plantilla no se usa abriéndola en Word y escribiendo encima (aunque puedes). Su uso previsto es como **referencia de estilos de pandoc**: escribes en Markdown y pandoc aplica estos estilos al convertir a Word.

```bash
pandoc tu-documento.md \
  --reference-doc="$HOME/.claude/skills/pdf-export/plantilla-academica-brj.docx" \
  -M lang=es \
  -o tu-documento.docx
```

Para varios ficheros en un solo Word: `pandoc cap*.md --reference-doc=... -o libro.docx`.

### Qué Markdown produce qué estilo

| En tu Markdown | Estilo en Word |
|---|---|
| Texto de párrafo | Normal / Body Text (Georgia 11,5 pt) |
| `# Encabezado` | Heading 1 (Arial 19 pt) |
| `## Encabezado` | Heading 2 (Arial, acento rojo tierra) |
| `### Encabezado` | Heading 3 (Arial, apagado) |
| `> Texto citado` | Block Text (Georgia cursiva, sangrado) |
| `- ítem` / `1. ítem` | listas con viñeta / numeradas |
| `[texto]{custom-style="VaultRef"}` | VaultRef (verde) — para términos destacados |

### Portada, saltos de página y estilos de carácter

- **Título y subtítulo de portada:** envuélvelos en una *fenced div* con el estilo:

  ```text
  ::: {custom-style="Title"}
  Mi título
  :::
  ```

- **Salto de página** (Word nativo): inserta un bloque OpenXML donde quieras cortar:

  ```text
  ```{=openxml}
  <w:p><w:r><w:br w:type="page"/></w:r></w:p>
  ```
  ```

- **Resaltar un término** con un estilo de carácter propio: `[término]{custom-style="VaultRef"}`.

### Cambiar fuentes o colores de la plantilla

Dos vías: (1) abrir `plantilla-academica-brj.docx` en Word → *Inicio → Estilos* → modificar; o (2) editar las constantes de paleta en `make_template.py` y re-ejecutarlo. La paleta actual: tinta `#1c1b19`, acento `#7a3b2e`, apagado `#6b6357`, vault `#4a6b54`.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Galería de estilos

Esta sección muestra cada estilo aplicado. Úsala como referencia visual y bórrala en tu documento final.

## Encabezado de nivel 2

Párrafo de cuerpo en estilo Normal: Georgia a 11,5 puntos con interlineado de 1,5. Aquí va el grueso del texto. Las **negritas** y las *cursivas* funcionan con la sintaxis Markdown habitual.

### Encabezado de nivel 3

Otro párrafo de cuerpo. Un término del vault se resalta así: [identidad-investigadora]{custom-style="VaultRef"} (estilo de carácter VaultRef, en verde).

> Esto es una cita en bloque (estilo Block Text): Georgia en cursiva, con sangría a la izquierda y color apagado. Útil para la idea-ancla de un capítulo o una cita textual destacada.

Lista con viñetas:

- Primer punto.
- Segundo punto.
- Tercer punto.

Lista numerada:

1. Primer paso.
2. Segundo paso.
3. Tercer paso.

Una tabla:

| Columna A | Columna B |
|---|---|
| Celda 1 | Celda 2 |
| Celda 3 | Celda 4 |

Un enlace externo: [ejemplo de enlace](https://example.org).

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Tu contenido empieza aquí

Borra la galería y las instrucciones anteriores y escribe tu trabajo a partir de este punto, usando los encabezados y estilos descritos.

## Sección 1

[Reemplaza este texto por el tuyo.]

## Sección 2

[Reemplaza este texto por el tuyo.]
