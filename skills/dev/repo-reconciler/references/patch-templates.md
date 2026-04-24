# Patch Templates

Plantillas para los parches más frecuentes. Adapta según el contenido real detectado.

---

## 🔴 Función pública nueva sin documentar

### Parche: añadir a sección "Usage" del README

```markdown
### `nombre_funcion(param1, param2, ...)` 

Descripción breve de lo que hace.

**Parámetros:**
- `param1` (`tipo`): descripción
- `param2` (`tipo`, opcional): descripción. Por defecto: `valor`.

**Devuelve:** `tipo` — descripción del valor de retorno.

**Ejemplo:**
\```python
from modulo import nombre_funcion

resultado = nombre_funcion(valor1, valor2)
print(resultado)
\```
```

---

## 🔴 Argumento CLI nuevo sin documentar

### Parche: añadir a sección "CLI" del README

```markdown
| Flag | Tipo | Por defecto | Descripción |
|------|------|-------------|-------------|
| `--nuevo-flag` | `str` | `None` | Descripción del flag. |
```

O en formato narrativo:

```markdown
- `--nuevo-flag <valor>`: Descripción del comportamiento que activa.
```

---

## 🔴 Variable de entorno nueva sin documentar

### Parche: añadir a sección "Configuration" / ".env" del README

```markdown
| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| `NOMBRE_VAR` | ✅ Sí | Descripción. Obtener en: [URL o instrucción]. |
| `NOMBRE_VAR_OPCIONAL` | ⬜ No | Descripción. Por defecto: `valor_default`. |
```

---

## 🔴 Modo de agente nuevo sin documentar

### Parche: añadir a sección "Modos" del README

```markdown
### Modo `nombre_modo`

Descripción de cuándo usar este modo y qué hace diferente al comportamiento base.

**Activación:**
\```bash
python agente.py --mode nombre_modo
\```

**Comportamiento:**
- Paso 1 del flujo
- Paso 2 del flujo
```

---

## 🟡 Firma de función cambiada

### Parche: diff de ejemplo en README

```
ANTES (línea N de README.md):
  resultado = nombre_funcion(param_viejo)

DESPUÉS:
  resultado = nombre_funcion(param_nuevo, extra_param=valor)
```

---

## 🟡 Flag CLI renombrado/eliminado

### Parche: actualizar tabla o lista en README

```
ANTES:
  --viejo-flag    Descripción

DESPUÉS (si renombrado):
  --nuevo-flag    Descripción

DESPUÉS (si eliminado):
  [eliminar la fila/línea]
```

---

## 🟡 Import path incorrecto en ejemplo

### Parche: corregir línea de import

```
ANTES:
  from modulo_viejo.submodulo import Clase

DESPUÉS:
  from modulo_nuevo.submodulo import Clase
```

---

## 🟡 Dependencia nueva no documentada en instalación

### Parche: añadir a sección "Installation" del README

```markdown
\```bash
pip install nombre-paquete
\```
```

O si hay `requirements.txt` referenciado:

```markdown
Las dependencias se instalan automáticamente con:
\```bash
pip install -r requirements.txt
\```
```

---

## 🟢 Versión desincronizada

### Parche: actualizar badge/mención en README

```
ANTES (README.md, línea N):
  Versión: 1.0.0

DESPUÉS:
  Versión: [valor de pyproject.toml/package.json]
```

---

## 🟢 CHANGELOG sin entrada para versión actual

### Parche: añadir entrada al inicio de CHANGELOG.md

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added
- [describir nuevas funcionalidades]

### Changed
- [describir cambios en funcionalidades existentes]

### Fixed
- [describir bugs corregidos]
```

---

## Plantilla README base (para proyectos SIN documentación)

Usar cuando el proyecto no tiene ningún fichero de doc:

```markdown
# [Nombre del Proyecto]

Descripción breve de una o dos líneas.

## Instalación

\```bash
pip install -r requirements.txt
\```

## Uso

\```python
# Ejemplo mínimo funcional
\```

## Configuración

| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| `VAR` | ✅ | Descripción |

## Algoritmos / Módulos incluidos

- **NombreClase**: descripción breve
- **OtraClase**: descripción breve

## Estructura del proyecto

\```
proyecto/
├── main.py
├── modulo/
│   └── ...
└── README.md
\```

## Requisitos

- Python X.Y+
- [otras dependencias especiales]
```
