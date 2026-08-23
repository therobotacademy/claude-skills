# 📊 Code — code-focused skills

Skills that work directly with code artifacts. Two of them turn something
hard to scan at a glance — source code or a block of structured prose —
into a self-contained SVG diagram, sharing the COIIAOC v1.1 palette, the
`visualize:show_widget` rendering path, and the `sendPrompt` click-to-ask
interaction pattern. The third, `pseudocode-ladder`, is a design-checkpoint
protocol rather than a diagram generator — it doesn't follow those
rendering conventions, but it belongs here because it also gates real code
generation, not written prose.

| Skill                                                          | Starts from             | Description                                                                                                                                                                                                                     |
| ---------------------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`code-diagram-explainer`](code-diagram-explainer/) | Source code               | Generates inline SVG diagrams explaining a code fragment — n8n nodes, functions, pipelines, classes — with literal pseudo-code extracted from source, control flow with ✓/✗ branches, and didactic click-to-ask annotations. |
| [`text-to-diagram`](text-to-diagram/)               | Structured prose          | Converts a section of structured text (methodology, process, architecture, conceptual framework) into an SVG diagram meant to *replace* the text, not decorate it — readable without going back to the original prose.      |
| [`pseudocode-ladder`](pseudocode-ladder/)           | A module about to be written (or an existing repo) | 4-level protocol (logic → classes → function pseudo-code → optional near-Python) inserted before real code is generated, marking each decision as delegable or non-delegable and requiring explicit sign-off per level. INVERSE mode reconstructs the ladder from an existing repo instead. |

## Which one to use

- Explaining a function, an n8n node, or any other code artifact → `code-diagram-explainer`.
- Illustrating a section of a document, report, or thesis that describes a process/architecture in prose → `text-to-diagram`.
- If the input is code, always use `code-diagram-explainer`, even if the code implements something that *sounds* like a methodology — the "read the real source, never paraphrase" rule only makes sense there.
- Before writing a new non-trivial module, or auditing an existing one for undocumented decisions → `pseudocode-ladder`.

## Shared conventions

The two diagram skills only — `pseudocode-ladder` has its own conventions, documented in its `SKILL.md`.

- **Palette**: COIIAOC v1.1 semantic color classes (`c-blue`, `c-purple`, `c-teal`, `c-amber`, `c-red`, `c-gray`) — see either `SKILL.md` for the exact fill/stroke tokens.
- **Rendering**: always via `visualize:show_widget`; never write a standalone `.svg` file to disk as the deliverable.
- **Interactivity**: each major node/block carries `onclick="sendPrompt('...')"` with a "why", not "what", question (≤12 words), connecting the diagram to the surrounding course/project concepts.
- **Prose after the diagram**: 2–4 short paragraphs at the abstraction level *above* the diagram — never repeating what's already visible in the SVG.
- **`samples/` and `svg/` folders**: reference diagrams from the sessions each skill was consolidated from, kept for calibration, not meant to be regenerated on every use.
- **`thread.txt`**: a pointer to the source Claude.ai conversation the skill was distilled from — provenance, not part of the skill's runtime behavior.
