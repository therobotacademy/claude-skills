# 📊 Code — visual explanation skills

Skills that turn something hard to scan at a glance — source code or a
block of structured prose — into a self-contained SVG diagram. Both share
the COIIAOC v1.1 palette, the `visualize:show_widget` rendering path, and
the `sendPrompt` click-to-ask interaction pattern, but they start from
different inputs and are not interchangeable.

| Skill                                                          | Starts from             | Description                                                                                                                                                                                                                     |
| ---------------------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`code-diagram-explainer`](code-diagram-explainer/) | Source code               | Generates inline SVG diagrams explaining a code fragment — n8n nodes, functions, pipelines, classes — with literal pseudo-code extracted from source, control flow with ✓/✗ branches, and didactic click-to-ask annotations. |
| [`text-to-diagram`](text-to-diagram/)               | Structured prose          | Converts a section of structured text (methodology, process, architecture, conceptual framework) into an SVG diagram meant to *replace* the text, not decorate it — readable without going back to the original prose.      |

## Which one to use

- Explaining a function, an n8n node, or any other code artifact → `code-diagram-explainer`.
- Illustrating a section of a document, report, or thesis that describes a process/architecture in prose → `text-to-diagram`.
- If the input is code, always use `code-diagram-explainer`, even if the code implements something that *sounds* like a methodology — the "read the real source, never paraphrase" rule only makes sense there.

## Shared conventions

- **Palette**: COIIAOC v1.1 semantic color classes (`c-blue`, `c-purple`, `c-teal`, `c-amber`, `c-red`, `c-gray`) — see either `SKILL.md` for the exact fill/stroke tokens.
- **Rendering**: always via `visualize:show_widget`; never write a standalone `.svg` file to disk as the deliverable.
- **Interactivity**: each major node/block carries `onclick="sendPrompt('...')"` with a "why", not "what", question (≤12 words), connecting the diagram to the surrounding course/project concepts.
- **Prose after the diagram**: 2–4 short paragraphs at the abstraction level *above* the diagram — never repeating what's already visible in the SVG.
- **`samples/` and `svg/` folders**: reference diagrams from the sessions each skill was consolidated from, kept for calibration, not meant to be regenerated on every use.
- **`thread.txt`**: a pointer to the source Claude.ai conversation the skill was distilled from — provenance, not part of the skill's runtime behavior.
