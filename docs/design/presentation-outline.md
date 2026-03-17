# SEN3006 Software Architecture -- Presentation Outline

**Project:** Task Management System (Factory Method + Strategy Patterns)
**Total Duration:** ~20 minutes + Q&A
**Format:** In-person presentation with live demo
**Class Count:** 16 (2 interfaces, 1 enum, 1 abstract class, 12 concrete classes including Main)

---

## Slide 1: Title Slide (1 min)

### On Screen
- Project title: "Task Management System"
- Course: SEN3006 Software Architecture
- Team member names
- Date
- Subtitle: "Factory Method + Strategy Design Patterns in Pure Java"

### Speaker Notes
- Greet the audience and introduce team members.
- State the project scope in one sentence: "We built a Task Management System in pure Java -- zero external dependencies -- that demonstrates two GoF design patterns: Factory Method for object creation and Strategy for runtime algorithm selection."
- Mention the system has 16 classes and is fully executable from a single Main.java.
- Transition: "Let me start by explaining the problem we set out to solve."

---

## Slide 2: Problem Definition (2 min)

### On Screen
- Problem statement in bold
- Three pain points as bullet list:
  1. Different task types (Bug, Feature, Documentation) require different data and creation logic
  2. Task prioritization needs change depending on context (urgency, deadlines, severity)
  3. The system must be extensible without modifying existing code
- Simple "before/after" comparison: monolithic if-else vs. pattern-based design

### Speaker Notes
- "In any real software team, you deal with different kinds of work items -- bugs have severity and reproduction steps, features have effort estimates, documentation tasks have target audiences."
- "If you hardcode task creation with if-else chains, adding a new type means modifying existing code -- violating the Open/Closed Principle."
- "Similarly, if prioritization logic is baked into one method, you cannot swap algorithms at runtime. A sprint planning meeting needs deadline-first ordering, but an incident response needs urgent-first."
- "Our goal was to solve both problems using established design patterns."
- Transition: "Let me now introduce the two patterns we selected and why."

---

## Slide 3: Design Patterns Overview (3 min)

### On Screen
- Split layout: Factory Method on the left, Strategy on the right
- Factory Method diagram:
  - Creator: `TaskFactory` (abstract class)
  - Concrete Creators: `BugTaskFactory`, `FeatureTaskFactory`, `DocumentationTaskFactory`
  - Product: `Task` (interface)
  - Concrete Products: `BugTask`, `FeatureTask`, `DocumentationTask`
- Strategy diagram:
  - Context: `TaskManager`
  - Strategy: `PriorityStrategy` (interface)
  - Concrete Strategies: `UrgentFirstStrategy`, `DeadlineFirstStrategy`, `SeverityFirstStrategy`

### Speaker Notes
- **Factory Method (Creational):**
  - "Factory Method defines an interface for creating objects but lets subclasses decide which class to instantiate."
  - "In our system, `TaskFactory` is the abstract creator with one abstract method: `createTask(title, description, priority)`. Each concrete factory -- `BugTaskFactory`, `FeatureTaskFactory`, `DocumentationTaskFactory` -- overrides this to return its specific task type."
  - "The client code never calls `new BugTask(...)` directly. It works through the `TaskFactory` reference, so the concrete class is hidden."
  - "We also added a template method `createTaskWithDeadline()` in `TaskFactory` that calls the abstract `createTask()` then sets the deadline -- combining Factory Method with a mini Template Method pattern."

- **Strategy (Behavioral):**
  - "Strategy defines a family of algorithms, encapsulates each one, and makes them interchangeable."
  - "Our `PriorityStrategy` interface has a single method: `sort(List<Task>)`. Three concrete strategies implement it differently:"
    - `UrgentFirstStrategy` -- sorts by priority descending (5 to 1)
    - `DeadlineFirstStrategy` -- sorts by deadline ascending (earliest first, null last)
    - `SeverityFirstStrategy` -- bugs first sorted by severity, then non-bugs by priority
  - "`TaskManager` holds a `PriorityStrategy` reference and delegates sorting to it. Calling `setPriorityStrategy()` swaps the algorithm at runtime."

- **Why these two patterns together:**
  - "Factory Method handles the creation dimension -- what objects we create."
  - "Strategy handles the behavioral dimension -- how we process those objects."
  - "Together they cover both creational and behavioral concerns, giving us a clean separation."

- Transition: "Now let us walk through the UML diagrams in detail."

---

## Slide 4: UML Walkthrough (3 min)

### On Screen
- Full class diagram showing all 16 classes with relationships:
  - `Task` (interface) <|.. `AbstractTask` (abstract) <|-- `BugTask`, `FeatureTask`, `DocumentationTask`
  - `TaskFactory` (abstract) <|-- `BugTaskFactory`, `FeatureTaskFactory`, `DocumentationTaskFactory`
  - `PriorityStrategy` (interface) <|.. `UrgentFirstStrategy`, `DeadlineFirstStrategy`, `SeverityFirstStrategy`
  - `TaskManager` --> `Task`, `TaskFactory`, `PriorityStrategy` (dependencies on abstractions)
  - `TaskStatus` (enum) used by `Task` and `AbstractTask`
- Sequence diagram for task creation flow

### Speaker Notes
- **Class Diagram walkthrough:**
  - "Starting from the top: `Task` is our Product interface with methods like `getId()`, `getTitle()`, `getStatus()`, `getPriority()`, `getDeadline()`, and `getType()`."
  - "`AbstractTask` implements `Task` and provides the shared state: id (auto-incremented via a static counter), title, description, status, priority, deadline, and createdAt timestamp. It also validates state transitions in `setStatus()` by delegating to `TaskStatus.canTransitionTo()`."
  - "The three concrete tasks -- `BugTask`, `FeatureTask`, `DocumentationTask` -- extend `AbstractTask` and add type-specific fields. For example, `BugTask` adds `severity` and `stepsToReproduce`."
  - "On the factory side, `TaskFactory` declares the abstract `createTask()` method plus a concrete `createTaskWithDeadline()` template method. Each concrete factory overrides `createTask()` to return its specific task type with sensible defaults."
  - "`TaskManager` is the central coordinator. It holds a `Map<String, TaskFactory>` as a factory registry (simplified Service Locator), a `List<Task>` for task storage, and a `PriorityStrategy` reference. Notice it depends only on abstractions -- `Task`, `TaskFactory`, `PriorityStrategy` -- never on concrete classes."

- **Sequence Diagram walkthrough (task creation):**
  - "1. Client calls `taskManager.createTask("BUG", "Fix crash", "App crashes", 5)`"
  - "2. TaskManager looks up `"BUG"` in the factory registry, gets `BugTaskFactory`"
  - "3. TaskManager calls `factory.createTask(title, description, priority)`"
  - "4. BugTaskFactory creates `new BugTask(...)` with default severity `"MEDIUM"`"
  - "5. The `BugTask` constructor calls `super()` on `AbstractTask`, which auto-assigns an ID and sets status to `OPEN`"
  - "6. The `Task` reference is returned to TaskManager, which adds it to its list"

- Transition: "Let me now show you this working live."

---

## Slide 5: Live Demo (5 min)

### On Screen
- Terminal/console showing Main.java output
- Run command: `javac *.java && java Main` (from src/main/java directory)

### Speaker Notes
Walk through each of the 6 test sections in the console output:

- **Test 1 -- Factory Method Pattern Demo:**
  - "Here we create three factories and use each one to create a task. Notice the output shows three different task types -- BUG, FEATURE, DOCUMENTATION -- all created through the same `TaskFactory` reference."
  - "We also demonstrate `createTaskWithDeadline()` -- the template method that wraps factory creation with deadline assignment."
  - "Finally, we show the specialized `createBugTask()` method that gives full control over severity and reproduction steps."
  - Point out: task IDs are auto-incremented, status defaults to OPEN.

- **Test 2 -- Strategy Pattern Demo:**
  - "Same 5 tasks, three completely different orderings."
  - "UrgentFirstStrategy: tasks ordered 5, 4, 3, 2, 1 by priority."
  - "DeadlineFirstStrategy: tasks ordered by earliest deadline, with null-deadline tasks pushed to the end."
  - "SeverityFirstStrategy: bugs sorted first by severity (CRITICAL before MEDIUM), then non-bugs by priority."
  - "Key point: we swapped algorithms at runtime with `setPriorityStrategy()` -- no if-else, no code changes."

- **Test 3 -- Task Lifecycle Demo:**
  - "Walk through OPEN -> IN_PROGRESS -> REVIEW -> DONE (valid path)."
  - "Show BLOCKED path: OPEN -> BLOCKED -> OPEN -> IN_PROGRESS."
  - "Demonstrate invalid transition: OPEN -> DONE throws `IllegalArgumentException` -- the state machine enforces valid workflows."
  - "Show terminal state: once DONE, no further transitions allowed."

- **Test 4 -- TaskManager Integration:**
  - "Full workflow: create tasks, transition states, filter by status, generate summary, remove a task."
  - "This shows the TaskManager coordinating factories, tasks, and strategies together."

- **Test 5 -- SOLID Principles Demo:**
  - "OCP: we create an anonymous `PriorityStrategy` inline (lowest-first for backlog grooming) and plug it in with zero changes to existing code."
  - "LSP: all three factories are used through a `TaskFactory[]` array -- fully interchangeable."
  - "DIP: TaskManager fields are all abstractions: `List<Task>`, `PriorityStrategy`, `TaskFactory`."

- **Test 6 -- Edge Cases and Error Handling:**
  - "We test 6 edge cases: invalid priority, null title, unknown task type, non-existent task ID, null strategy, and case-insensitive type lookup."
  - "Every invalid input is caught with a clear error message -- no crashes, no silent failures."
  - "All 6/6 edge cases pass."

- Transition: "Let me now zoom into the code for the three most important classes."

---

## Slide 6: Code Walkthrough (3 min)

### On Screen
- Show source code for three key classes (side by side or sequentially):
  1. `TaskFactory.java` -- the abstract creator
  2. `PriorityStrategy.java` -- the strategy interface
  3. `TaskManager.java` -- the context/client that ties both patterns together

### Speaker Notes

- **TaskFactory (abstract creator):**
  - "Two methods: the abstract `createTask()` that subclasses override, and the concrete `createTaskWithDeadline()` that calls `createTask()` then sets the deadline."
  - "This is Factory Method + Template Method combined. The template method defines the skeleton (create then configure), and subclasses supply the creation step."
  - "Note the return type is `Task` (interface), not a concrete class. The caller never knows what they get."

- **PriorityStrategy (strategy interface):**
  - "Single method: `List<Task> sort(List<Task> tasks)`. This is ISP in action -- the interface is as small as possible."
  - "Contract: return a NEW sorted list, do NOT modify the original. This preserves immutability."
  - "Any class that implements this interface can be plugged into TaskManager."

- **TaskManager (coordinator):**
  - "The `factoryRegistry` is a `Map<String, TaskFactory>` initialized with three built-in factories. The `registerFactory()` method allows extension at runtime (OCP)."
  - "`createTask(type, title, desc, priority)` looks up the factory by type string, delegates creation, and adds the result to the task list."
  - "`setPriorityStrategy(strategy)` swaps the algorithm. `getPrioritizedTasks()` delegates to `currentStrategy.sort(tasks)`."
  - "Notice: all field types are abstractions -- `List<Task>`, `PriorityStrategy`, `Map<String, TaskFactory>`. No concrete product or strategy class is referenced. This is DIP."

- Transition: "This brings us to how the system satisfies each SOLID principle."

---

## Slide 7: SOLID Principles (2 min)

### On Screen
- Table with 5 rows (one per principle), each with:
  - Principle name and abbreviation
  - How the project satisfies it
  - Specific class/example

### Speaker Notes

| Principle | How Satisfied | Example |
|-----------|--------------|---------|
| **S -- Single Responsibility** | Each class has exactly one reason to change. | `BugTaskFactory` only creates bugs. `UrgentFirstStrategy` only sorts by priority. `TaskStatus` only defines states and transitions. `TaskManager` only coordinates. |
| **O -- Open/Closed** | New task types and strategies are added by creating new classes, not modifying existing ones. | Adding a `ResearchTask` requires only `ResearchTask.java` + `ResearchTaskFactory.java` + one `registerFactory()` call. Zero changes to TaskManager, TaskFactory, or any strategy. |
| **L -- Liskov Substitution** | All subtypes are fully interchangeable through their base type references. | A `TaskFactory[]` array holds all three factories and each is used identically. Any `PriorityStrategy` works in TaskManager. Any `Task` subtype works in any list. |
| **I -- Interface Segregation** | Interfaces are focused and minimal. No client depends on methods it does not use. | `PriorityStrategy` has a single method: `sort()`. `Task` interface has only methods common to ALL task types. Type-specific methods like `getSeverity()` live on the concrete class, not the interface. |
| **D -- Dependency Inversion** | High-level modules depend on abstractions, not concrete classes. | `TaskManager` depends on `Task` (interface), `TaskFactory` (abstract class), and `PriorityStrategy` (interface). It never references `BugTask`, `FeatureTask`, `UrgentFirstStrategy`, etc. |

- Transition: "Finally, let us discuss the strengths and limitations of our approach."

---

## Slide 8: Advantages and Improvements (1 min)

### On Screen
- Two columns: Strengths | Limitations & Future Work

### Speaker Notes

**Strengths:**
- Zero external dependencies -- compiles and runs with just `javac` and `java`.
- Clean pattern implementation that directly maps GoF terminology to code (Creator, Product, Context, Strategy).
- Factory registry enables runtime extensibility without recompilation.
- Strategies are swappable at runtime with a single method call.
- State machine in `TaskStatus` prevents invalid lifecycle transitions.
- Comprehensive self-testing: Main.java serves as both demo and validation.

**Limitations:**
- Not thread-safe: the static `idCounter` in `AbstractTask` and the `ArrayList` in `TaskManager` are not synchronized.
- No persistence: tasks exist only in memory for the duration of the program.
- No composite/chain strategy: cannot combine strategies (e.g., sort by priority, then by deadline as tiebreaker).
- Severity in `BugTask` uses raw `String` -- could be an enum for type safety.
- No unit test framework (JUnit) -- tests are in Main.java as print-and-verify.

**Future Work:**
- Add `AtomicInteger` for thread-safe ID generation and `CopyOnWriteArrayList` or synchronization for the task list.
- Implement a `CompositeStrategy` that chains multiple strategies with tiebreaking.
- Add persistence via serialization or file I/O (still zero-dependency).
- Introduce the Observer pattern to notify listeners on task state changes.
- Migrate tests to JUnit 5 for automated regression testing.
- Consider the State pattern (full class-per-state) if lifecycle logic grows more complex.

- Close: "Thank you. We are happy to take your questions."

---

## Q&A Preparation

### Q1: "Why Factory Method instead of Abstract Factory?"

**Model Answer:**
Abstract Factory is for creating *families* of related objects (e.g., a Windows GUI factory that creates Windows buttons, Windows menus, Windows scrollbars together). Our system creates individual task objects one at a time -- there is no family relationship between a BugTask and an UrgentFirstStrategy. Factory Method is the right choice because we need polymorphic creation of a single product type (Task) through subclass-specific factories. Each factory is independent and responsible for exactly one task type. If we later needed to create coordinated sets of objects (e.g., a task + its default workflow + its default notification template as a bundle), Abstract Factory would become relevant.

---

### Q2: "Why Strategy instead of just if-else?"

**Model Answer:**
An if-else chain in `getPrioritizedTasks()` would work for three strategies, but it violates OCP -- every new strategy requires modifying the method. It also violates SRP because the TaskManager would contain all sorting algorithms. With Strategy, each algorithm is in its own class (SRP), new algorithms are added without touching TaskManager (OCP), and algorithms can be swapped at runtime (flexibility). In Test 5, we demonstrated creating an anonymous strategy inline and plugging it in -- impossible with if-else without modifying the TaskManager source code. Strategy also makes each algorithm independently testable.

---

### Q3: "How does this follow OCP?"

**Model Answer:**
The system is open for extension and closed for modification in two dimensions. First, adding a new task type (e.g., ResearchTask) requires only two new classes: `ResearchTask extends AbstractTask` and `ResearchTaskFactory extends TaskFactory`. Then call `manager.registerFactory("RESEARCH", new ResearchTaskFactory())`. Zero lines of existing code are modified. Second, adding a new prioritization strategy requires only one new class implementing `PriorityStrategy`, then calling `manager.setPriorityStrategy(new MyNewStrategy())`. Again, no existing class changes. We demonstrated this in Test 5 by creating an anonymous inline strategy at runtime.

---

### Q4: "What happens if you need a new task type?"

**Model Answer:**
Three steps, all additive:
1. Create `ResearchTask extends AbstractTask` -- add type-specific fields (e.g., `researchArea`, `hypothesis`), override `getType()` to return `"RESEARCH"`.
2. Create `ResearchTaskFactory extends TaskFactory` -- override `createTask()` to return a new `ResearchTask` with sensible defaults.
3. Register it: `manager.registerFactory("RESEARCH", new ResearchTaskFactory())`.

No existing file is modified. The `TaskManager`, `Task` interface, `AbstractTask`, all existing factories, and all strategies remain untouched. This is OCP in action.

---

### Q5: "What if you want to combine strategies?"

**Model Answer:**
Currently, strategies are mutually exclusive -- you set one at a time. To combine them, we would implement the Composite pattern on strategies: create a `CompositeStrategy implements PriorityStrategy` that takes a list of strategies and applies them as tiebreakers. For example: sort by priority first (UrgentFirstStrategy), and for tasks with equal priority, sort by deadline (DeadlineFirstStrategy). The `CompositeStrategy.sort()` method would use a `Comparator` chain. This is a natural evolution that requires no changes to TaskManager -- it would just receive a `CompositeStrategy` via `setPriorityStrategy()`.

---

### Q6: "Is this thread-safe?"

**Model Answer:**
No, and this is a known limitation. Two specific issues:
1. The `idCounter` in `AbstractTask` is a plain `static int`. Concurrent task creation could produce duplicate IDs. Fix: replace with `private static final AtomicInteger idCounter = new AtomicInteger(0)`.
2. The `tasks` ArrayList in `TaskManager` is not synchronized. Concurrent reads and writes could cause `ConcurrentModificationException`. Fix: use `Collections.synchronizedList()` or `CopyOnWriteArrayList`, and synchronize iteration blocks.

Thread safety was not a requirement for this project, but these are the changes needed for a concurrent environment.

---

### Q7: "Why not use the State pattern for lifecycle?"

**Model Answer:**
We considered it. The full State pattern would mean creating a class for each state (`OpenState`, `InProgressState`, `ReviewState`, `DoneState`, `BlockedState`), each with methods defining what actions are allowed. For our 5 states with simple transition rules, the `TaskStatus` enum with `canTransitionTo()` achieves the same validation with far less code -- 5 enum constants vs. 5 separate classes, each with their own file and boilerplate.

However, if lifecycle behavior grows complex -- for example, entering IN_PROGRESS sends a notification, entering REVIEW triggers a code review request, entering BLOCKED logs to an audit system -- then the State pattern becomes justified because each state would encapsulate its own behavior. Our enum approach would require if-else chains for that, violating OCP. So the State pattern is a logical next step if the system grows.

---

### Q8: "How would you add persistence?"

**Model Answer:**
Since we target zero dependencies, we have two pure-Java options:
1. **Java Serialization:** Make `AbstractTask` implement `Serializable`, then use `ObjectOutputStream`/`ObjectInputStream` to save and load the task list. Quick but fragile across code changes.
2. **File I/O with CSV or JSON:** Write a `TaskRepository` class that serializes tasks to a structured text format. This follows SRP (persistence is separated from domain logic) and DIP (TaskManager depends on a `TaskRepository` interface, not a concrete file implementation).

Either way, the design patterns are not affected. The factories still create tasks, the strategies still sort them. Persistence is an orthogonal concern.

---

### Q9: "What are the limitations?"

**Model Answer:**
1. **No thread safety** -- static ID counter and unsynchronized list (as discussed).
2. **No persistence** -- tasks are lost when the program exits.
3. **No composite strategies** -- cannot chain or combine sorting algorithms.
4. **Severity is a raw String** -- should be an enum (`BugSeverity.CRITICAL`, etc.) for type safety and exhaustive switch checking.
5. **No Observer/event system** -- state transitions do not notify external listeners (useful for logging, notifications, dashboards).
6. **Tests are in Main.java** -- no JUnit, no automated pass/fail assertions, no CI integration.
7. **No input validation on type strings** -- `createTask("BUGG", ...)` fails at runtime with an exception rather than being caught at compile time.

---

### Q10: "How does the factory registry work?"

**Model Answer:**
The `TaskManager` constructor initializes a `HashMap<String, TaskFactory>`:
```
factoryRegistry.put("BUG", new BugTaskFactory());
factoryRegistry.put("FEATURE", new FeatureTaskFactory());
factoryRegistry.put("DOCUMENTATION", new DocumentationTaskFactory());
```
When `createTask("BUG", title, desc, priority)` is called, the manager does `factoryRegistry.get("BUG")`, which returns the `BugTaskFactory` instance. It then calls `factory.createTask(title, desc, priority)`, and the factory returns a `BugTask` through the `Task` interface.

This is a simplified Service Locator pattern layered on top of Factory Method. The key benefit is extensibility: calling `registerFactory("RESEARCH", new ResearchTaskFactory())` adds a new type at runtime without modifying any existing code. The registry decouples the type string from the factory class.

---

### Q11: "Why is TaskFactory an abstract class instead of an interface?"

**Model Answer:**
Because `TaskFactory` contains a concrete method: `createTaskWithDeadline()`. This template method calls the abstract `createTask()` and then sets the deadline. If `TaskFactory` were an interface, we could use a Java 8+ default method, but an abstract class makes the template method relationship more explicit and is the classic GoF approach. It also allows us to add shared state or utility methods to the creator hierarchy in the future without breaking existing concrete factories. In Java, an abstract class is the standard choice for the Creator role in Factory Method when the creator has shared behavior.

---

### Q12: "What is the role of AbstractTask?"

**Model Answer:**
`AbstractTask` is the skeletal implementation between the `Task` interface and the concrete task classes. It serves three purposes:
1. **Eliminates boilerplate** -- all shared fields (id, title, description, status, priority, deadline, createdAt) and their getters are implemented once.
2. **Enforces the state machine** -- `setStatus()` validates transitions via `TaskStatus.canTransitionTo()` before applying the change.
3. **Provides a toString() template** -- concrete tasks call `super.toString()` and append their type-specific details.

This is the standard "abstract class in between" approach from the GoF Factory Method pattern. Concrete products (`BugTask`, `FeatureTask`, `DocumentationTask`) only need to provide `getType()` and their own fields.

---

### Q13: "Could you use generics or Java streams more?"

**Model Answer:**
Yes. The current implementation avoids streams and advanced generics intentionally to keep the code accessible and focused on the design patterns. However, in production:
- `TaskManager.getTasksByStatus()` could use `tasks.stream().filter(t -> t.getStatus() == status).collect(Collectors.toList())`.
- Strategy implementations could use `Comparator.comparing()` chains instead of anonymous `Comparator` classes.
- The factory registry could be typed as `Map<String, TaskFactory>` with bounded wildcards if we added generics to the factory hierarchy.

We chose clarity over conciseness for a teaching/presentation context.

---

## Presentation Checklist

- [ ] All team members have assigned speaking parts
- [ ] Slide deck is prepared matching this outline
- [ ] Main.java compiles and runs cleanly on the presentation machine
- [ ] UML class diagram and sequence diagram are exported as images
- [ ] Terminal font size is large enough for the audience to read
- [ ] Backup: screenshots of demo output in case of live demo failure
- [ ] Timer: practice run completed within 20 minutes
- [ ] Q&A: each team member has reviewed all 13 model answers
