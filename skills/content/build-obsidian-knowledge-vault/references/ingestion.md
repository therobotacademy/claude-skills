# Recuperación y cobertura

## Inventario

Registrar antes de sintetizar cada referencia sustantiva de la principal: id, URL original, URL resuelta cuando exista, título, profundidad, fuente padre, localizador del enlace, estado y alcance leído. Conservar todos los enlaces excluidos de contenido en el registro con una razón; no es necesario inventariar scripts, fuentes tipográficas o CSS como referencias bibliográficas.

Normalizar host y fragmento para deduplicar documentos; mantener el fragmento original como localizador. No eliminar parámetros semánticos ni versiones. Una URL de PDF y una página de abstract pueden ser el mismo trabajo, pero reflejar versiones distintas: comprobar antes de fusionar. Una búsqueda temática adicional es `supplemental`, no una referencia originalmente citada.

## Lectura según soporte

- HTML: identificar artículo o área de contenido; conservar títulos, tablas, enlaces y límites de extracción. Contenido dinámico omitido implica `partial` si no se recupera.
- WebArchive aportado: usar el script para inventariar todos los marcos, texto y enlaces. Elegir el artículo leyendo sus contenidos; un título coincidente en el marco exterior no basta. El script conserva el archivo aportado y extrae HTML sin ejecutarlo. No interpreta el diseño de tablas o SVG: inspeccionarlos con herramientas apropiadas si aportan evidencia.
- PDF: usar el flujo PDF disponible; verificar tablas/figuras por página si la síntesis depende de ellas. Abstract sin cuerpo = `partial`, con ese alcance explícito.
- GitHub: leer README y los archivos o documentación pertinentes al contenido citado; fijar commit cuando sea posible. No instalar ni ejecutar código ajeno por el hecho de ingerirlo. No afirmar haber auditado todo el repositorio.
- Libro/curso: declarar capítulos o unidades leídos. No convertir una portada, índice o ficha editorial en lectura del libro o del curso.
- Datos: leer descripción, esquema y condiciones relevantes; descargar o procesar el conjunto solo si la tarea lo necesita. Distinguir análisis de datos de lectura de su ficha.

## Estados

`ingested`: contenido citado leído con el alcance registrado y suficiente para la síntesis; no significa que todo un sitio/repositorio/libro esté ingerido.
`partial`: contenido recuperado incompleto respecto del objeto citado; especificar qué falta.
`blocked`: acceso o capacidad impide leerlo; no implica que la fuente no exista.
`unavailable`: recurso no localizado tras intentos permitidos.
`excluded`: no es referencia sustantiva o queda fuera del alcance acordado; registrar motivo.

No dar una referencia por leída porque exista un archivo vacío, una URL o una ficha. Cada `ingested`/`partial` debe tener texto o extracción realmente inspeccionada, fecha, localizador y una síntesis sustantiva en el vault. El validador comprueba estructura y no puede certificar lectura.

## Copias y derechos

Conservar íntegros los archivos aportados por el usuario y materiales cuya licencia o autorización permita reproducirlos. Para fuentes web, respetar las reglas de reproducción y límites de cada herramienta: preferir síntesis con citas y localizadores, evitando incrustar textos o libros completos sin autorización. Leer y sintetizar no obliga a redistribuir el original. Registrar `retention` como `user_supplied_copy`, `licensed_copy`, `summary_only` o `metadata_only`. No descargar contenido protegido para eludir límites de citas. No empaquetar cookies, credenciales o URLs temporales firmadas como referencias permanentes.

## Ejemplo de criterio aprendido

Un WebArchive puede contener una página de interfaz casi vacía y un iframe con el artículo íntegro y su bibliografía. Recuperar las nueve secciones y 16 URL de ese artículo acredita la ingesta de la principal, no la de los 16 trabajos. En la modalidad de esta habilidad hay que abrirlos y producir síntesis con evidencia, o registrar cada limitación. Las cifras de coste citadas siguen siendo estimaciones de la fuente hasta verificar tarifas y supuestos; dos fuentes que discrepan no deben fusionarse en una falsa cifra única.
