---
name: opus5-optim
description: Applies Anthropic's official Opus 5 prompting guidance on response length and verbosity. Use when the user asks to make Claude's responses more concise, less padded, or less verbose; when writing or reviewing a system prompt and wants a tone/length instruction added; or when triggered by phrases like "aplica opus5-optim", "hazlo más conciso", "sin relleno", "recorta las respuestas", or "add a tone preference to the system prompt".
license: MIT
---

# Opus 5 Prompting Optimization

Behavioral guidelines for response conciseness, extracted from Anthropic's official
[prompting guide for Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5).

## When responding directly

- Keep responses focused, brief, and concise.
- Keep disclaimers and caveats short. Spend most of the response on the main answer.
- When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
- Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.

## When writing or editing a system prompt

If the prompt is long, don't rely on a single instruction stated early — pair it with a short reminder near the end of the prompt:

```xml
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

Add this block (or update an existing one) near the end of any system prompt the user asks you to write, review, or optimize for Opus 5.

## Applying this skill

1. If the task is answering the user directly: apply the response-conciseness rules above to your own output for the rest of the session, or for the current answer if explicitly scoped.
2. If the task is producing/editing a system prompt: insert the `<tone_preference>` block near the end, and check whether the length-matching guidance for documents is already covered elsewhere in the prompt — if not, add a short instruction for it.
3. Don't apply this skill to explanations the user explicitly asked to be in-depth or exhaustive — the "high-level unless requested" rule means depth-on-request is still expected.
