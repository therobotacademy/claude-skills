Under Windows you can directly copy & paste `claude-minimax.bat`

- This script is what builds the skill when you run it

Then run the script from the folder you want to work in:

```PowerShell
.\claude-minimax.bat
```

## Tabla de Modelos de MiniMax y Equivalencias

Dependiendo de la pasarela o proxy que utilices (como OpenRouter, LiteLLM o la API nativa de MiniMax), los identificadores de la API pueden requerir el prefijo del proveedor (ej. `minimax/`). Aquí tienes el desglose actual:

| Modelo MiniMax                               | ID de API Común                                                | Ventana de Contexto           | Enfoque Principal                                                                                                                                                       | Equivalente Claude Sugerido                                      |
| -------------------------------------------- | --------------------------------------------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **MiniMax M3**                         | `minimax/minimax-m3`                                          | **1 Millón de tokens** | El modelo insignia actual. Multimodal nativo (procesa texto, imagen y video), extraordinario en razonamiento lógico y flujos de agentes autónomos de larga duración. | **Claude 3.5 Sonnet / Claude 3 Opus**                      |
| **MiniMax M2.7**                       | `minimax/minimax-m2.7`                                        | 200K tokens                   | Optimizado para flujos autónomos multi-agente, análisis de datos complejos y tareas complejas de ofimática.                                                          | **Claude 3.5 Sonnet**                                      |
| **MiniMax M2.5**                       | `minimax/minimax-m2.5`                                        | 200K tokens                   | Modelo de alta eficiencia entrenado fuertemente con aprendizaje por refuerzo. Destaca de forma masiva en ingeniería de software y generación de código.              | **Claude 3.5 Sonnet** (Excelente relación calidad/precio) |
| **MiniMax M2.5 Lightning / Highspeed** | `minimax/minimax-m2.5-lightning` o `minimax-m2.5-highspeed` | 200K tokens                   | Variante de velocidad optimizada. Ofrece respuestas fluidas con una latencia mínima sacrificando muy poco razonamiento.                                                | **Claude 3.5 Haiku**                                       |
| **abab 6.5s**                          | `abab6.5s-chat`                                               | 192K tokens                   | Modelo de la generación anterior enfocado en procesamiento de texto rápido y económico.                                                                              | **Claude 3 Haiku**                                         |

---

## Configuración recomendada para tus Variables

Si estás mapeando estas variables para entornos como **Claude Code** u otras interfaces de desarrollo guiado, lo ideal es emparejar la velocidad y la potencia de manera equilibrada para no disparar los costes ni ralentizar los comandos simples:

### 1. Para el modelo rápido (Haiku)

Asigna un modelo ágil, de baja latencia y económico para las operaciones sencillas de la CLI:

```cmd
set ANTHROPIC_DEFAULT_HAIKU_MODEL=minimax/minimax-m2.5-lightning
```

### 2. Para el modelo inteligente (Sonnet / Opus)

Asigna el modelo con mayor capacidad de resolución de problemas complejos, manejo de dependencias y lectura de código estructurado:

```cmd
set ANTHROPIC_DEFAULT_SONNET_MODEL=minimax/minimax-m3
set ANTHROPIC_DEFAULT_OPUS_MODEL=minimax/minimax-m3
set ANTHROPIC_MODEL=minimax/minimax-m3
```

> ⚠️ **Nota sobre los corchetes `[1m]`:** Como vimos antes, el sufijo `[1m]` es un añadido que inyecta el entorno de desarrollo para forzar el contexto de un millón de tokens en Claude. Si tu proxy traduce directamente el ID limpio (`minimax/minimax-m3`), introduce los nombres tal y como aparecen en la tabla para evitar errores de ruta no encontrada (404).
