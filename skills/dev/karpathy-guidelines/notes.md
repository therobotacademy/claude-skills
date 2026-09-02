
The `karpathy-guidelines` explicitly state their fundamental trade-off at the top: **they bias toward caution over speed**.

Applying them indiscriminately creates friction in five specific scenarios:

### 1. Exploratory Spikes and Rapid Prototyping

* **The Conflict**: The guidelines mandate *"Think Before Coding"* (stopping to clarify all ambiguity) and *"Goal-Driven Execution"* (defining strict success criteria and tests before coding).
* **Why to skip**: When exploring whether a library works, testing a model's raw capabilities, or experimenting with visual layouts, the goal is discovery, not stability. Requiring pre-flight clarification, test harnesses, and surgical precision kills the rapid feedback loop needed to understand an unknown problem space.

### 2. Framework, SDK, and Public API Design

* **The Conflict**: The guidelines mandate *"No abstractions for single-use code"* and *"No 'flexibility' or 'configurability' that wasn't requested"*.
* **Why to skip**: When building reusable platforms, SDKs, or protocols (like `ErpConnector` or `BaseAuthoritySpec` in this project), you **must** think speculatively about extension points, generic interfaces, and future pluggability. Enforcing strict minimalism here leads to rigid, tightly coupled code that requires breaking rewrites as soon as a second consumer arrives.

### 3. Hardened Production & Defensive Systems

* **The Conflict**: The guidelines mandate *"No error handling for impossible scenarios"*.
* **Why to skip**: In enterprise systems, distributed pipelines, and financial or security engines, defensive programming is essential. Circuit breakers, corruption fallbacks, dead-letter queues, and assertion guards against "impossible" states prevent catastrophic data loss. Stripping defensive guards in the name of simplicity leaves production code fragile.

### 4. Dedicated Refactoring & Technical Debt Sessions

* **The Conflict**: The guidelines mandate *"Touch only what you must"*, *"Don't 'improve' adjacent code, comments, or formatting"*, and *"Don't remove pre-existing dead code"*.
* **Why to skip**: When your task is explicitly architectural cleanup, codebase modernization, or applying the "Boy Scout Rule" (leaving files cleaner than you found them), surgical isolation is counterproductive. These tasks specifically require touching adjacent modules, deleting orphans, and updating stale documentation.

### 5. Trivial One-Offs and Disposable Automation

* **The Conflict**: Multi-step plans, stopping to question assumptions, and strict test-looping.
* **Why to skip**: Writing a quick script to inspect a directory, reformat a text dump, or parse a one-time log file does not warrant the overhead of formal verification criteria. The cost of a bug in a throwaway script is near zero.

### Summary Rule of Thumb

| Situation                                         | Apply Karpathy Guidelines? | Priority                                        |
| :------------------------------------------------ | :------------------------- | :---------------------------------------------- |
| **Modifying existing, critical core code**  | **Yes**              | Surgical safety & regression prevention         |
| **Bug fixing & targeted feature additions** | **Yes**              | Test-driven reproduction & minimal blast radius |
| **Refactoring & Debt Reduction**            | **No / Relaxed**     | Systemic cleanup & broader scope                |
| **Framework & Protocol Architecture**       | **No / Relaxed**     | Long-term extensibility & abstraction           |
| **Spikes, POCs & Disposable Scripts**       | **No**               | Speed of iteration & discovery                  |
