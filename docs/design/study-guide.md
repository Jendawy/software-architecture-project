# Study Guide — How to Explain This Project

> Read this before the presentation. The professor will ask questions.
> If you can answer these, you'll ace it.

## The 30-Second Pitch

"We built a Task Management System for software teams. It creates different types of tasks — bugs, features, and documentation — using the **Factory Method** pattern. It prioritizes those tasks using swappable algorithms with the **Strategy** pattern. The whole system follows SOLID principles, meaning you can add new task types or new sorting strategies without changing any existing code."

## What Each Class Does (Plain English)

| Class | What it does | One sentence |
|---|---|---|
| `Task` | Interface | "The contract — every task must have an ID, title, priority, status, etc." |
| `AbstractTask` | Base class | "Holds the common stuff — ID counter, title, description, status. All task types extend this." |
| `BugTask` | Bug report | "A task that also has severity (LOW to CRITICAL) and steps to reproduce." |
| `FeatureTask` | Feature request | "A task that also has estimated effort in hours and business value." |
| `DocumentationTask` | Doc task | "A task that also has document type (API, guide, tutorial) and target audience." |
| `TaskStatus` | State machine | "The 5 states a task can be in (OPEN, IN_PROGRESS, REVIEW, DONE, BLOCKED) and which transitions are allowed." |
| `TaskFactory` | Abstract factory | "Defines HOW tasks are created. Subclasses decide WHICH type to create." |
| `BugTaskFactory` | Bug creator | "Creates BugTask with default severity MEDIUM." |
| `FeatureTaskFactory` | Feature creator | "Creates FeatureTask with default 8 hours effort." |
| `DocumentationTaskFactory` | Doc creator | "Creates DocumentationTask with default type API." |
| `PriorityStrategy` | Sorting interface | "One method — sort() — that different strategies implement differently." |
| `UrgentFirstStrategy` | Sort by priority | "Highest priority number first. For emergencies." |
| `DeadlineFirstStrategy` | Sort by deadline | "Earliest deadline first. For sprint planning." |
| `SeverityFirstStrategy` | Sort by bug severity | "Bugs first (by CRITICAL→LOW), then non-bugs by priority." |
| `TaskManager` | Coordinator | "The brain — uses factories to create tasks, uses strategies to sort them." |
| `Main` | Demo/test | "Runs all tests and prints results." |

## How the Two Patterns Work

### Factory Method Pattern
**Problem it solves:** "If we used `new BugTask()` everywhere, adding a new task type would mean changing every place that creates tasks."

**How it works:**
1. `TaskFactory` is abstract — it says "I can create a Task, but I don't say which kind"
2. `BugTaskFactory` extends it — it says "When you ask me to create a task, I give you a BugTask"
3. `TaskManager` stores a map: "BUG" → BugTaskFactory, "FEATURE" → FeatureTaskFactory
4. When you call `manager.createTask("BUG", ...)`, it looks up the factory and delegates

**Key line of code:** `Task task = factory.createTask(title, description, priority);`
The caller gets a `Task` back — it never knows it's actually a `BugTask`.

### Strategy Pattern
**Problem it solves:** "If we hardcoded sorting logic with if-else, adding a new sorting method would mean modifying the TaskManager."

**How it works:**
1. `PriorityStrategy` is an interface with one method: `sort(List<Task>)`
2. Each strategy implements it differently (by priority, by deadline, by severity)
3. `TaskManager` holds a `currentStrategy` reference
4. You can swap it at runtime: `manager.setPriorityStrategy(new DeadlineFirstStrategy())`

**Key line of code:** `return currentStrategy.sort(tasks);`
The TaskManager doesn't know HOW the sorting works — it just delegates.

## SOLID Principles — What to Say

| Principle | What it means | Example from our code |
|---|---|---|
| **S**ingle Responsibility | Each class does one thing | "TaskFactory only creates tasks. PriorityStrategy only sorts. They don't mix." |
| **O**pen/Closed | Open for extension, closed for modification | "To add a ResearchTask, I create ResearchTask.java and ResearchTaskFactory.java. I don't touch any existing class." |
| **L**iskov Substitution | Subtypes can replace parent types | "I can use any TaskFactory where TaskFactory is expected — BugTaskFactory, FeatureTaskFactory, they all work the same way." |
| **I**nterface Segregation | Small, focused interfaces | "PriorityStrategy has ONE method. Task interface only has methods ALL tasks need. Severity is only on BugTask." |
| **D**ependency Inversion | Depend on abstractions | "TaskManager uses Task (interface), not BugTask (class). It uses PriorityStrategy (interface), not UrgentFirstStrategy (class)." |

## Professor Questions — Cheat Sheet

**Q: "Why Factory Method instead of Abstract Factory?"**
A: "Abstract Factory creates families of related objects. We only have one family — tasks. Factory Method is simpler and fits better. If we needed to create related objects like Task + TaskView + TaskValidator together, then Abstract Factory would make sense."

**Q: "Why not just use if-else instead of Strategy?"**
A: "If-else violates the Open/Closed Principle. Every time you add a new sorting algorithm, you'd modify the same if-else chain. With Strategy, you just create a new class that implements PriorityStrategy. Zero changes to existing code."

**Q: "What happens if I want to add a new task type?"**
A: "Three steps: 1) Create the new class extending AbstractTask. 2) Create its factory extending TaskFactory. 3) Register it in TaskManager. No existing code changes."

**Q: "Is this thread-safe?"**
A: "No. The static ID counter and the task list are not synchronized. For a multi-threaded version, we'd use AtomicInteger for IDs and CopyOnWriteArrayList or synchronized blocks for the task list."

**Q: "Why not use the State pattern for the task lifecycle?"**
A: "The State pattern would mean creating separate classes for each state (OpenState, InProgressState, etc.). Our lifecycle is simple enough that an enum with transition rules is cleaner and has less code. If states had complex behavior, State pattern would be better."

**Q: "How would you add persistence?"**
A: "We'd create a TaskRepository interface with save/load methods, then implement it for file storage or a database. TaskManager would depend on the repository interface (DIP), not the concrete implementation."

**Q: "What are the limitations?"**
A: "No persistence (data lost on exit), no GUI (console only), single-user (not thread-safe), no undo support. Future improvements could add Observer pattern for notifications, Command pattern for undo, and a persistence layer."

**Q: "How does the factory registry work?"**
A: "It's a HashMap mapping type strings to factory instances. When you call createTask('BUG'), it does factoryRegistry.get('BUG') to find BugTaskFactory, then calls createTask() on it. This is a simplified Service Locator pattern."

## Before the Presentation

- [ ] Run the program once to make sure it compiles and all tests pass
- [ ] Read through Main.java — understand what each test section does
- [ ] Read through TaskManager.java — understand how it coordinates everything
- [ ] Practice the 30-second pitch out loud
- [ ] Review the Q&A cheat sheet above
- [ ] Know where each SOLID principle is demonstrated
