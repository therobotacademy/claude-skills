# GitKraken CLI — Integración con Claude Code

## Qué hace

GitKraken CLI (`gk.exe`) se engancha a **todos** los eventos del ciclo de vida de Claude Code para que la aplicación GitKraken pueda observar y reaccionar a lo que Claude hace en cada sesión (commits sugeridos, cambios de directorio, uso de herramientas, etc.).

## El comando hook

```
"C:/Users/Bernardo/AppData/Local/GitKrakenCLI/gk.exe" ai hook run --host claude-code
```

- `gk.exe` — GitKraken CLI, instalado en el perfil de usuario de Windows
- `ai hook run` — subcomando que procesa un evento del agente de IA
- `--host claude-code` — indica que el host es Claude Code (no otro agente)

El comando recibe el payload del evento por stdin (JSON) y lo envía a GitKraken.

## Eventos suscritos

La integración cubre la totalidad de los eventos disponibles de Claude Code:

| Evento | Cuándo se dispara |
|---|---|
| `SessionStart` | Al iniciar una sesión |
| `SessionEnd` | Al cerrar una sesión |
| `UserPromptSubmit` | Cuando el usuario envía un mensaje |
| `PreToolUse` | Antes de que Claude use una herramienta |
| `PostToolUse` | Después de que Claude use una herramienta con éxito |
| `PostToolUseFailure` | Después de que una herramienta falle |
| `Stop` | Cuando Claude termina de responder |
| `StopFailure` | Cuando Claude termina con error |
| `PermissionRequest` | Cuando Claude pide permiso para una acción |
| `PermissionDenied` | Cuando el usuario deniega un permiso |
| `PreCompact` | Antes de compactar el contexto |
| `PostCompact` | Después de compactar el contexto |
| `Notification` | Cuando Claude emite una notificación |
| `Elicitation` | Cuando Claude solicita información al usuario |
| `ElicitationResult` | Cuando el usuario responde a una elicitación |
| `InstructionsLoaded` | Cuando se cargan las instrucciones (CLAUDE.md, etc.) |
| `ConfigChange` | Cuando cambia la configuración |
| `CwdChanged` | Cuando cambia el directorio de trabajo |
| `SubagentStart` | Cuando arranca un subagente |
| `SubagentStop` | Cuando para un subagente |
| `TaskCompleted` | Cuando se completa una tarea |
| `TeammateIdle` | Cuando un compañero de equipo queda inactivo |

## Dónde vive la configuración

`~/.claude/settings.json` — configuración global de usuario. Aplica a todas las sesiones de Claude Code en este equipo.

## Cómo se instaló

GitKraken inyecta estos hooks automáticamente al conectar Claude Code desde la aplicación GitKraken (menú de integración con agentes de IA). No se configuran a mano.

## Desactivar sin borrar

Para deshabilitar temporalmente la integración sin eliminar los hooks, renombra o mueve `gk.exe`. Los hooks seguirán existiendo en `settings.json` pero fallarán silenciosamente.

Para desactivar permanentemente, elimina todos los bloques con `"command": "...gk.exe ai hook run..."` de `settings.json`.
