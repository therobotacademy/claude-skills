---
name: log-turn
description: Automatically append every conversation turn to `sessions/today-LOG.md` in the `## Prompt N: <Title>` / `## Response N` format. Fires proactively after every assistant response. Switch to on-demand mode only if the user explicitly says "only fire on demand" (or equivalent) in the current session.
---
# log-turn

Append the current conversation exchange (and any prior unlogged exchanges) to `sessions/today-LOG.md` using the established `## Prompt N: <Title>` / `## Response N` format.

## When to invoke

**Always active by default.** Fire automatically after every assistant response — no explicit user request is needed.

Exception: if the user states in the current session something like "only fire on demand", "solo cuando te lo pida", or any clear equivalent, switch to on-demand mode for the remainder of that session. In on-demand mode, fire only when explicitly asked. Common on-demand phrasings:

- "Vuelca todas tus respuestas a sessions/today-LOG.md"
- "Vuelca esto al log"
- "Log this turn"
- "Hazlo con esta última" (when the previous turn already invoked this skill)

## Target file

`sessions/today-LOG.md` (relative to repo root). If the file does not exist, create it with a timestamp header as the very first line (see below). If it exists, append.

## Required format

Every appended turn is one `## Prompt N` block followed by one `## Response N` block, separated from prior content by a blank line, a horizontal rule, and a blank line:

```markdown

---

## Prompt N: <Title>

<verbatim user prompt — preserve formatting, code fences, line breaks>

## Response N

**<one-sentence bold summary of the response>**

<rest of the response body>
```

Rules:

1. **N** is monotonically increasing across the whole file. Find the highest existing `## Prompt (\d+)` heading (grep the file) and use `max + 1` for the next entry. If the file is empty/missing, start at `1`.
2. **Title** comes immediately after the colon. It is 2–5 words capturing the topic of the prompt (e.g., `Classical ML baseline`, `Discretization verification`, `MD conversion`, `Plan v3`). If the prompt is a short meta-command (`commit`, `vuelca al log`), use one short literal token as title (e.g., `Commit attempt`, `Log dump`).
3. The **verbatim prompt** preserves the exact user text. Do not paraphrase. Keep markdown formatting, accents, code fences, and line breaks. Strip leading shell-prompt glyphs like `❯ ` only if they were not actually typed by the user (when in doubt, keep them).
4. The **bold summary** is the first paragraph of the Response, wrapped in `**...**`. One sentence, declarative, ≤ 30 words. It states what the response did or concluded, not the topic. Example: `**Verifico contra `categorize_st.py `: la discretización es equal-width fija (cortes 4 y 7), no tertile; v2.2 está correcto.**`
5. The **response body** is the full Claude reply that followed the user prompt in the conversation. Reproduce headings, lists, tables, code blocks verbatim. Do **not** re-derive a summary from scratch — copy what was sent.

## Timestamp header

When creating the file from scratch, write this as the very first line before any turn blocks:

```markdown
# Session log — YYYY-MM-DD HH:MM
```

Use the current local date and time (24 h). Example: `# Session log — 2026-05-19 14:37`. Leave one blank line after the header before the first turn block. **Never** inject this header into an existing file.

## Procedure

1. Read `sessions/today-LOG.md` end-to-end (or check it doesn't exist).
2. If it doesn't exist, create it and write the timestamp header as the first line (see above).
3. Identify the highest `## Prompt N` heading already in the file — call it `last_logged_N`.
4. Walk the conversation forward from `last_logged_N + 1` through the current invocation:
   - For each user prompt with a matching assistant response (and which is not yet in the file), append one `## Prompt N: <Title>` / `## Response N` block as specified above. Increment N.
   - The dump invocation itself is the last block appended. Its Response is a short confirmation of what was logged (e.g., `**Anexados Prompts 4–8 al final de `sessions/today-LOG.md `.**` + 1–2 lines of detail).
5. If a prior turn was interrupted (no assistant response was produced or the assistant only ran tools and stopped), still log the prompt; in the Response section write `_(interrupted — no response delivered)_` or summarize what was attempted before interruption.
6. **Do not include** system reminders, tool call payloads, or hidden injected context in either the prompt or the response. Only the user-visible prompt text and the user-visible assistant text.
7. After appending, output a one-sentence confirmation to the user. Do not re-paste the appended content.

## Append mechanics

- Prefer `Edit` with a unique tail anchor (the last few lines of the existing file) to avoid rewriting the whole file.
- If anchoring fails (e.g., the file ends with text that appears earlier too), `Read` the file, then `Write` it back with the new blocks appended. Never use `Write` without first reading.
- The file must end with a single trailing newline after the final block. Do not leave dangling `---` separators at the very end.

## Title heuristic (when in doubt)

Scan the user prompt for the most concrete noun phrase and use it. Examples:

| Prompt opening                                                                 | Title                           |
| ------------------------------------------------------------------------------ | ------------------------------- |
| "Regarding decision point 3. Classical ML baseline..."                         | `Classical ML baseline`       |
| "Explain more in depth 5. Discretization method..."                            | `Discretization verification` |
| "Vamos a hacer la edición de la nueva versión en MD. Para ello convierte..." | `MD conversion`               |
| "commit"                                                                       | `Commit attempt`              |
| "Traza los comentarios en docs\\... ESCRIBE UN DOCUMENTO MD..."                | `Peer-review tracing plan`    |
| "Vuelca todas tus respuestas..."                                               | `Log dump`                    |

Avoid generic titles like `Question`, `Task`, or `Request`. The title must let a reader skimming the log understand the topic without opening the body.

## Summary heuristic

The bold summary opens the Response so a skimming reader can extract the decision/outcome without reading the full body. Patterns that work:

- For analyses: `**<verb> + <object> + <verdict>**` — e.g., `**Verifico la discretización contra el código y confirmo que es equal-width fija; v2.2 está correcto.**`
- For deliverables: `**<verb> <artifact> en <path>**` — e.g., `**Plan escrito en `docs/5-Review-by-peers/PLAN_v3_modifications.md `.**`
- For meta-confirmations: `**<participle> <what> en <where>**` — e.g., `**Anexados Prompts 4–8 al final de `sessions/today-LOG.md `.**`

Do not start the summary with hedges (`Creo que...`, `Posiblemente...`). State the result.
