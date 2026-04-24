# Reconcile Targets por Tipo de Proyecto

Este fichero define qué pares fichero↔fichero vigilar según el tipo de proyecto detectado.

---

## Python Package / Library

| Fuente de verdad (código) | Debe estar sincronizado con (docs) |
|---|---|
| `pyproject.toml` → `version` | README badge de versión, CHANGELOG entrada |
| `pyproject.toml` → `[dependencies]` | README sección "Installation" |
| Funciones públicas en `src/` | Docstrings, README sección "Usage", ejemplos en `examples/` |
| `__init__.py` exports | README "API Reference" |
| `cli.py` o `__main__.py` argumentos | README sección "CLI Usage" |
| `.env.example` claves | README sección "Configuration" o "Environment Variables" |

**Señales de alerta típicas:**
- `from modulo_viejo import X` en ejemplos del README
- Argumento `--flag` que ya no existe en `argparse` / `click` / `typer`
- Versión en README != versión en `pyproject.toml`

---

## Agente IA (nanobot / Google ADK / LangChain)

| Fuente de verdad (código) | Debe estar sincronizado con (docs) |
|---|---|
| Nombres de agentes/tools registrados | README lista de capacidades del agente |
| Prompts del sistema en ficheros `.txt`/`.md` | README descripción del comportamiento del agente |
| Configuración de herramientas (tools, callbacks) | README sección "Herramientas disponibles" |
| Variables de entorno para API keys | README sección "Configuración" |
| Modos de ejecución (presets, profiles) | README sección "Modos de uso" |
| Ficheros de configuración YAML/TOML del agente | README sección "Configuración" |

**Señales de alerta típicas:**
- Tool registrada en código sin mención en docs
- API key requerida en código pero no documentada en "Setup"
- Flujo de conversación rediseñado pero diagrama/descripción en README sin actualizar

---

## Script CLI standalone

| Fuente de verdad (código) | Debe estar sincronizado con (docs) |
|---|---|
| `argparse` / `click` flags y subcomandos | README sección "Uso" o "Commands" |
| `--help` output implícito | README ejemplos de invocación |
| Ficheros de entrada/salida esperados | README sección "Input/Output" |
| Dependencias en `requirements.txt` | README sección "Instalación" |
| Versión en script o `__version__` | README header |

**Señales de alerta típicas:**
- Ejemplo en README con flag renombrado o eliminado
- Fichero de salida con extensión diferente a la documentada
- Dependencia nueva en `requirements.txt` sin instrucción de instalación

---

## App Streamlit

| Fuente de verdad (código) | Debe estar sincronizado con (docs) |
|---|---|
| `st.sidebar` controles (sliders, selects) | README descripción de controles disponibles |
| Páginas / secciones de la app | README descripción de funcionalidades |
| `requirements.txt` | README sección "Instalación" |
| Variables de entorno / `st.secrets` | README sección "Configuración" |
| Ficheros de datos esperados en `data/` | README sección "Datos de entrada" |

**Señales de alerta típicas:**
- Nuevo filtro o panel sin mención en README
- `st.secrets["KEY"]` sin instrucción en docs de cómo configurarlo
- Screenshots en README desactualizados (no detectables automáticamente — avisar)

---

## Laboratorio Académico (Jupyter / scripts de entrega)

| Fuente de verdad (código) | Debe estar sincronizado con (docs) |
|---|---|
| Parámetros de experimentos | README o enunciado reproducido en doc |
| Algoritmos implementados | README lista de algoritmos |
| Dependencias / módulos especiales (PyArmor) | README instrucciones de instalación especiales |
| Resultados producidos | README o notebook con resultados esperados |
| Estructura de entrega de ficheros | README sección "Estructura del proyecto" |

**Señales de alerta típicas:**
- Algoritmo nuevo implementado sin entrada en README "Algoritmos incluidos"
- Módulo cifrado (PyArmor) sin instrucciones especiales de instalación
- Versión de Python requerida no documentada (ej: Python 3.14 específico)
