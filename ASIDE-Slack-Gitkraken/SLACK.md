# Notificaciones de Claude Code en Slack

## Qué hace

Cada vez que Claude termina de responder, envía un mensaje automático al canal `#notifications` de Slack.

## Requisitos

- Plugin de Slack instalado en Claude Code
- Cuenta de Slack conectada al plugin

## Instalación del plugin

```
/plugin install slack
```

Si el navegador no abre automáticamente:

```
/install-slack-app
```

Sigue el flujo de autorización OAuth en el navegador.

## Configuración del hook

El hook vive en `~/.claude/settings.json` (configuración global de usuario), dentro del evento `Stop`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "mcp_tool",
            "server": "claude_ai_Slack",
            "tool": "slack_send_message",
            "input": {
              "channel": "#notifications",
              "text": "✅ Claude ha terminado"
            }
          }
        ]
      }
    ]
  }
}
```

Cambia `#notifications` por el canal o DM que prefieras.

## Activar tras editar settings.json

El fichero de settings se carga al inicio de sesión. Para aplicar cambios sin reiniciar:

1. Abre `/hooks` en Claude Code — eso fuerza la recarga de configuración.

## Cambiar el canal o el mensaje

Edita directamente `~/.claude/settings.json` y modifica los campos `channel` y `text` dentro del hook.

## Desactivar

Elimina el bloque `mcp_tool` del array `hooks` dentro de `Stop` en `~/.claude/settings.json`.

## Limitación conocida: "MCP server not connected"

Al usar `"type": "mcp_tool"` en un hook de `Stop`, Claude Code puede lanzar este error:

```
Stop hook error: MCP server 'claude_ai_Slack' not connected
```

**Causa:** cuando el hook se dispara, la sesión ya está terminando y el servidor MCP ya no está disponible — el MCP solo existe dentro de la conversación activa, no en el contexto en que corren los hooks.

**Solución alternativa:** reemplazar el hook `mcp_tool` por un `command` que llame directamente a la API de Slack mediante una **Incoming Webhook URL** (sin depender del MCP):

```json
{
  "type": "command",
  "command": "curl -s -X POST -H 'Content-type: application/json' --data '{\"text\":\"✅ Claude ha terminado\"}' https://hooks.slack.com/services/TU/WEBHOOK/URL"
}
```

Para obtener la Incoming Webhook URL: Slack → Apps → Incoming Webhooks → Add New Webhook to Workspace.

# SLACK WEBHOOKS

Para habilitar una Incoming Webhook (webhook entrante) en Slack y enviar mensajes desde servicios externos, sigue estos pasos:

1. Crea una App de Slack: Ve a la página de [Slack API Apps](https://api.slack.com/apps) y haz clic en "Create New App". Puedes crearla desde cero ("From scratch").
2. Activa los Webhooks: En el panel lateral izquierdo, bajo la sección "Features", selecciona "Incoming Webhooks". Cambia el interruptor a "On" para activarlos.
3. Añade un nuevo Webhook: Haz clic en el botón "Add New Webhook to Workspace" al final de la página.
4. Selecciona el canal: Elige el canal específico de tu espacio de trabajo donde quieres que se publiquen los mensajes y haz clic en "Allow" (Permitir).
5. Copia la URL: Slack generará una URL única. Cópiala; esta es la dirección a la que deberás enviar tus peticiones HTTP POST con datos en formato JSON para publicar mensajes

```
https://hooks.slack.com/services/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
```

## Ejemplo de uso rápido

Una vez tengas tu URL, puedes probarla desde una terminal usando `curl`:

```bash
curl -X POST -H 'Content-type: application/json' --data '{"text":"¡Hola desde el Webhook!"}' https://hooks.slack.com/services/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
```

Nota: Si necesitas enviar información *desde* Slack hacia otro sistema, deberás configurar "Outgoing Webhooks" (en desuso a favor de la [Events API](https://api.slack.com/apis/connections/events-api)) o usar el Slack App Directory para buscar integraciones ya existentes. [7, 8]
