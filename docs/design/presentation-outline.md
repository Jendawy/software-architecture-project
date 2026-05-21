# Presentation Outline — Task Management System

**Course:** SEN3006 Software Architecture
**Project:** Task Management System (Base)
**Patterns:** Factory Method (Creational) + Strategy (Behavioral)
**Bonus pattern:** Lifecycle state machine encoded in `TaskStatus`
**Presenters:** Malak + Jindawi (co-presented) — speaker tags `[M]` / `[J]` per slide; final split TBD with the team.

Aligned to `docs/design/design-spec.md` and `docs/report/report.md`.
Target: ~10 min talk + 3 min live demo + 2–5 min Q&A.

The professor already knows what each pattern *is*. The presentation
spends its time on **why we chose it here** and **what it bought us in
this codebase**.

---

## Table of contents

1. Title + one-line pitch
2. The domain — what problem are we solving
3. What the system does (feature summary)
4. Architecture in one diagram
5. **Why Factory Method?** (creational rationale)
6. **Why Strategy?** (behavioral rationale)
7. Bonus — lifecycle state machine
8. SOLID quick pass
9. **Live demo** (the centerpiece)
10. Extension story — adding a task type / sort rule
11. What went well / what's next
12. Q&A

---

## Suggested speaker split (negotiate with Jindawi)

| Slide | Title | Suggested speaker | Rationale |
|---|---|---|---|
| 1 | Title | **Either** (open together) | Set the tone, hand off |
| 2 | Domain | **M** | Pitch — sets the "why-this-project" framing |
| 3 | What it does | **M** | Feature tour — natural follow-up from domain |
| 4 | Architecture | **J** | First technical slide — Jindawi anchors the code side |
| 5 | Why Factory Method | **J** | Whoever wrote the factory code should defend it |
| 6 | Why Strategy | **M** | Balances airtime; Strategy rationale is more conceptual than code-walk |
| 7 | Lifecycle | **J** | Continues the code-walk arc from slide 5 |
| 8 | SOLID | **M** | 10 seconds per principle — fast, conversational |
| 9 | Live demo | **J drives, M narrates** | One hand on keyboard, one voice explaining |
| 10 | Extension story | **M** | "Imagine adding X" — pitch-style, M lands the OCP payoff |
| 11 | Recap | **Either** (M recommended) | Whoever opened should close |
| 12 | Q&A | **Both** | Field questions on the part each presented |

Adjust based on who feels stronger on which topic. The
demo (slide 9) is the highest-stakes — pair-program it so the
keyboard-holder isn't also doing the talking.

---

## Slide-by-slide talking points

### 1. Title  [Either]

- "Task Management System — Factory Method + Strategy in pure Java."
- Course code, team names, deadline. Single-sentence pitch:
  > "Two design patterns made visible inside a working dev-team task tracker."

### 2. The domain — why a task tracker  [M]

- A software-team task tracker has two recurring problems:
  - **Tasks come in fundamentally different shapes.** A bug has severity and steps-to-reproduce; a feature has estimated effort and business value; documentation has document type and target audience. They share the `Task` interface but their construction rules differ. → Creational.
  - **The same list needs to be sorted by different rules in different moments.** By deadline during sprint planning, by severity during incident triage, by priority for the daily standup. The list doesn't change; the ordering does. → Behavioral.
- The domain was chosen *because the patterns map naturally to it*, not the other way around.

### 3. What the system does  [M]

- **3 task types:** `BugTask`, `FeatureTask`, `DocumentationTask` (all extend `AbstractTask`).
- **3 concrete factories:** `BugTaskFactory`, `FeatureTaskFactory`, `DocumentationTaskFactory` (each extends `TaskFactory`).
- **3 sort strategies:** `UrgentFirstStrategy`, `DeadlineFirstStrategy`, `SeverityFirstStrategy` (all implement `PriorityStrategy`).
- **5-state lifecycle:** `OPEN → IN_PROGRESS → REVIEW → DONE`, with a `BLOCKED` branch. `DONE` is terminal.
- **Three entry points** share the same engine:
  - `Main` — 5 self-checking scripted test sections.
  - `TaskManagementApp` — interactive console menu.
  - `gui.TaskManagerGUI` — Swing window with sort/filter dropdowns.

### 4. Architecture in one picture  [J]

- Class diagram (Mermaid render from `docs/uml/`).
- Three layers:
  - **Product layer** — `Task` interface, `AbstractTask`, 3 concrete tasks.
  - **Pattern layer** — `TaskFactory` abstract + 3 concrete factories; `PriorityStrategy` interface + 3 concrete strategies.
  - **Coordination + entry-points** — `TaskManager` (holds `Map<String, TaskFactory> factoryRegistry` and the current `PriorityStrategy`); `Main`, `TaskManagementApp`, `TaskManagerGUI`.
- Arrows only ever point *toward* abstractions — DIP made visible.

### 5. Why Factory Method? (rationale — most important slide)  [J]

- **The pain it solves here:** each task type has a different constructor signature (bug needs severity + repro; feature needs effort + business value; doc needs type + audience). Without a factory, every entry point that creates a task names the concrete class — `new BugTask(title, priority, "MEDIUM", "")` in the console driver, again in the GUI driver, again in the scripted demo. Adding a `ResearchTask` means hunting down N call sites.
- **Why an abstract `TaskFactory` class instead of a single static helper?** Each subclass owns its own defaults (bug defaults to severity `"MEDIUM"`; feature defaults to effort `8`, business value `5`; doc defaults to `"API"` for developers). A static factory becomes a giant `switch` over a type string. Polymorphic factories let each subclass own its defaults and validation.
- **Why `TaskFactory.createTaskWithDeadline(...)` as a non-abstract method?** It's a Template Method on top of Factory Method: subclasses only override `createTask(...)`, the deadline-attaching variant is reused. Adding a new deadline-aware constructor variant later means editing one base class, not three.
- **Why `Map<String, TaskFactory> factoryRegistry` on the manager?** It turns "which factory" into a runtime lookup keyed by string command (`"BUG"` → factory). The GUI's *Type* dropdown and the console menu both just iterate the registry. Adding a new type registers it once; every entry point picks it up automatically.
- **The payoff:** `manager.createTask("BUG", title, desc, 5)`. The manager never names a concrete `Task` subclass — DIP made visible.

### 6. Why Strategy? (rationale — most important slide)  [M]

- **The pain it solves here:** sorting needs **context**. By deadline for sprint planning, by severity during incidents, by priority for standup. Hard-coding one comparator inside `TaskManager` means rewriting the manager every time the workflow shifts. Hard-coding a `switch (sortMode)` inside `getPrioritizedTasks()` violates Open/Closed.
- **Why `PriorityStrategy` interface instead of raw `Comparator<Task>`?** Strategy *is* Comparator with intent. The interface name advertises the **role** the algorithm plays in the system — readers see "swappable ordering policy", not "anonymous comparator hidden in a util class." It also lets a strategy do more than pairwise comparison: `SeverityFirstStrategy` partitions `BugTask`s by severity rank, then orders the rest by priority — that's stateful work a raw `Comparator` would awkwardly handle.
- **Why runtime-swappable instead of constructor-injected?** Users change the sort live (GUI dropdown). `TaskManager.setPriorityStrategy(...)` is a one-line setter; the next `getPrioritizedTasks()` call uses the new strategy. Adding a fourth strategy is one new file + zero edits to the manager.
- **The payoff:** the GUI dropdown is a one-line wire to `manager.setPriorityStrategy(new SeverityFirstStrategy())`. Flip the dropdown, the table reorders.

### 7. Bonus — lifecycle as a state machine  [J]

- `TaskStatus` enum encodes its own transition table:
  - `OPEN → IN_PROGRESS, BLOCKED`
  - `IN_PROGRESS → REVIEW, BLOCKED`
  - `REVIEW → DONE, IN_PROGRESS` (reject path back to in-progress)
  - `BLOCKED → OPEN` (unblock)
  - `DONE` — terminal
- `AbstractTask.setStatus(...)` rejects illegal moves with `IllegalArgumentException`.
- Third pattern (State) for **zero extra files** — a single enum.
- Compile-time guarantee: cannot reach `DONE` from `BLOCKED` without going through `IN_PROGRESS → REVIEW`.

### 8. SOLID quick pass (10 seconds each)  [M]

- **S**RP — factories build, strategies sort, manager coordinates. One job per class.
- **O**CP — new task type = new file + one `registerFactory(...)`. New sort = one file + one `setPriorityStrategy(...)`. **Zero edits** to existing classes.
- **L**SP — every factory works through the abstract reference; every strategy through the interface.
- **I**SP — `PriorityStrategy` has one method; `Task` interface is minimal.
- **D**IP — manager fields are all interfaces / abstract classes.

### 9. Live demo (≈3 min)  [J drives · M narrates]

1. **Scripted demo.** `java -cp bin Main`. Scroll past sections; point at one `[PASS]` per section, with explicit pauses on Test 1 (Factory) and Test 2 (Strategy).
2. **Open the GUI.** `java -jar TaskManagerGUI.jar`. Load *Strategy demo* from the menu.
3. **Swap the strategy.** Cycle the *Sort by* dropdown through all three options. Table reorders live.
4. **Trigger factory error.** Type a task with type `"FOO"`. Engine throws, dialog explains why.
5. **Trigger an illegal transition.** Pick an `OPEN` task and try to mark it `DONE` directly. Engine refuses with the exact "Cannot transition from OPEN to DONE" message.

> Validation lives in the engine, not the GUI. The GUI just surfaces the message.

### 10. Extension story — zero-edit demonstration  [M]

- Adding a `ResearchTask`:
  - `ResearchTask.java` (extends `AbstractTask`).
  - `ResearchTaskFactory.java` (extends `TaskFactory`).
  - One `manager.registerFactory("RESEARCH", new ResearchTaskFactory())`.
- Adding a `CheapestFirstStrategy`:
  - `CheapestFirstStrategy.java` (implements `PriorityStrategy`).
  - One `manager.setPriorityStrategy(...)` call.
- **Zero edits** to any existing class. That is the OCP payoff.

### 11. What went well / what's next  [Either]

- **Worked well**
  - Both patterns map cleanly to real workflow concerns — no contrived plumbing.
  - Factory registry means every entry point auto-discovers new task types.
  - Strategy swap is one line — GUI dropdown proves it live.
  - Lifecycle enum proves correctness without an extra class.
- **What's next**
  - Persistence (Repository pattern).
  - Filtering and tags (Specification pattern).
  - Async dispatch for long-running task operations.

### 12. Q&A — likely questions  [Both]

- "Why an abstract factory class instead of an interface?" → per-subclass defaults + Template Method on `createTaskWithDeadline`. **[J]**
- "Why a `PriorityStrategy` interface instead of raw `Comparator<Task>`?" → role advertisement + stateful sorting. **[M]**
- "Why the string-keyed registry?" → runtime lookup from any entry point without hard-coding types. **[J]**
- "Why no JUnit?" → zero-dependency academic project; `Main` is the test harness. **[Either]**
- Backup cheat-sheet: `docs/design/study-guide.md`.

---

## Timing budget

| Slide | Time | Speaker |
|---|---|---|
| 1 — Title | 0:30 | Either |
| 2 — Domain | 1:00 | M |
| 3 — What it does | 1:00 | M |
| 4 — Architecture | 0:45 | J |
| 5 — Why Factory Method | 1:30 | J |
| 6 — Why Strategy | 1:30 | M |
| 7 — Lifecycle | 0:45 | J |
| 8 — SOLID | 0:50 | M |
| 9 — Live demo | 3:00 | J drives · M narrates |
| 10 — Extension | 0:45 | M |
| 11 — Recap | 0:30 | Either |
| 12 — Q&A | 2–5:00 | Both |
| **Total** | **~13 min + Q&A** | |

If short on time: cut slide 8 (SOLID) and shorten slide 11.

Rough airtime: **M ≈ 5:30** · **J ≈ 5:15** · shared **3:30**.
Adjust slide 8 → J or slide 7 → M if the split feels off.

---

## Pre-demo checklist

- [ ] `javac -d bin src/main/java/*.java src/main/java/gui/*.java` runs clean.
- [ ] `java -cp bin Main` — all 5 sections finish with `[PASS]`.
- [ ] `java -jar TaskManagerGUI.jar` opens; table renders; sort dropdown works.
- [ ] Have a known-bad input ready: type `"FOO"` for factory failure; `OPEN → DONE` for transition failure.
- [ ] Backup screenshots in case the projector dies.
- [ ] Confirm who drives the keyboard in the demo and who narrates.

---

## Rendered slide deck

The actual slide deck is generated from `PRESENTATION.md` at the
project root via Marp:

```bash
npx -y @marp-team/marp-cli PRESENTATION.md -o PRESENTATION.pptx
```

That produces `PRESENTATION.pptx` — editable in PowerPoint / Google
Slides / Keynote. Use this outline as the speaker-notes companion.
