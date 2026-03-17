# Test Documentation — Task Management System

## How to Compile and Run

### Prerequisites
- Java 8 or later (JDK) installed
- Terminal / Command Prompt access

### Steps

```bash
# Step 1: Navigate to the project directory
cd "Software Architecture"

# Step 2: Create the output directory
mkdir -p bin

# Step 3: Compile all Java source files
javac -d bin src/main/java/*.java

# Step 4: Run the program
java -cp bin Main
```

If you see `ALL TESTS PASSED` at the end, the system is working correctly.

---

## Test Sections Explained

The `Main.java` file contains 5 test sections that demonstrate the system works correctly. Each test prints `[PASS]` when successful.

### Test 1: Factory Method Pattern Demo
**What it tests:** That each factory creates the correct task type without the caller knowing which concrete class is used.

**What you should see:**
- A BugTask created via `BugTaskFactory` → type shows "BUG", has severity field
- A FeatureTask created via `FeatureTaskFactory` → type shows "FEATURE", has effort/value fields
- A DocumentationTask created via `DocumentationTaskFactory` → type shows "DOCUMENTATION", has docType field
- A task created with a deadline using the template method `createTaskWithDeadline()`
- A task created with full custom parameters via specialized factory method

**Why this matters:** Proves the Factory Method pattern works — client code uses `TaskFactory` (abstract) and gets the right concrete product back.

### Test 2: Strategy Pattern Demo
**What it tests:** That the same list of tasks is sorted differently depending on which strategy is active.

**What you should see:**
- **UrgentFirstStrategy:** Tasks ordered by priority (5 first, 1 last)
- **DeadlineFirstStrategy:** Tasks ordered by deadline (earliest date first, no-deadline tasks at the end)
- **SeverityFirstStrategy:** Bug tasks appear first (CRITICAL before MEDIUM), then non-bug tasks by priority

**Why this matters:** Proves the Strategy pattern works — swapping the strategy at runtime changes behavior without modifying any code.

### Test 3: Task Lifecycle (State Transitions) Demo
**What it tests:** That the TaskStatus state machine correctly allows valid transitions and blocks invalid ones.

**What you should see:**
- Valid path: OPEN → IN_PROGRESS → REVIEW → DONE (all succeed)
- Blocked path: OPEN → BLOCKED → OPEN → IN_PROGRESS (unblocking works)
- Invalid transition: OPEN → DONE → throws `IllegalArgumentException` with message "Cannot transition from OPEN to DONE"
- Terminal state: DONE → OPEN → throws `IllegalArgumentException` (DONE is final, no transitions out)

**Why this matters:** Proves the state machine prevents invalid workflows and enforces business rules.

### Test 4: TaskManager Integration Demo
**What it tests:** The full workflow — creating, filtering, transitioning, and summarizing tasks.

**What you should see:**
- 5 tasks created via `TaskManager.createTask()` using the factory registry
- Tasks filtered by status (OPEN, IN_PROGRESS, REVIEW)
- A task summary showing counts per status
- A task removed by ID, remaining count decreases

**Why this matters:** Proves all components work together as a system.

### Test 5: SOLID Principles Demo
**What it tests:** That each SOLID principle is satisfied by the implementation.

**What you should see:**
- **OCP:** A new anonymous strategy added at runtime without modifying any existing class
- **LSP:** All three factories used through a `TaskFactory[]` array — all substitutable
- **DIP:** TaskManager's field types are all abstractions (Task, PriorityStrategy, TaskFactory)
- **SRP:** Each class has exactly one responsibility
- **ISP:** Interfaces are minimal (PriorityStrategy has one method, Task has only common methods)

**Why this matters:** Proves the code follows software engineering best practices required by the project.

---

## Edge Cases Handled

| Edge Case | How It's Handled | Where |
|---|---|---|
| Invalid priority (0 or 6) | `IllegalArgumentException` thrown | `AbstractTask` constructor |
| Null or blank title | `IllegalArgumentException` thrown | `AbstractTask` constructor |
| Null description | `IllegalArgumentException` thrown | `AbstractTask` constructor |
| Invalid state transition | `IllegalArgumentException` thrown | `AbstractTask.setStatus()` |
| Transition from terminal DONE state | Blocked, exception thrown | `TaskStatus.DONE.canTransitionTo()` |
| Unknown task type in factory registry | `IllegalArgumentException` with available types listed | `TaskManager.createTask()` |
| Task not found by ID | `IllegalArgumentException` thrown | `TaskManager.getTask()` |
| Null task added | `IllegalArgumentException` thrown | `TaskManager.addTask()` |
| Null strategy set | `IllegalArgumentException` thrown | `TaskManager.setPriorityStrategy()` |
| Null deadline in sorting | Pushed to end of list | `DeadlineFirstStrategy.sort()` |
| Case-insensitive task type | `.toUpperCase()` applied | `TaskManager.createTask()` |

---

## Expected Console Output

Running `java -cp bin Main` produces approximately 150 lines of formatted output. The output ends with:

```
##########################################################
#                  ALL TESTS PASSED                      #
##########################################################
```

If any test fails, the specific `[PASS]` marker will be missing and an error message will indicate what went wrong.

---

## Verification Checklist

After running the program, verify:

- [ ] All 5 test sections show `[PASS]`
- [ ] Test 1 creates 3 different task types correctly
- [ ] Test 2 shows 3 different orderings of the same 5 tasks
- [ ] Test 3 catches 2 expected exceptions (invalid transition + terminal state)
- [ ] Test 4 shows filtered views and task removal
- [ ] Test 5 demonstrates all 5 SOLID principles
- [ ] Final summary shows "ALL TESTS PASSED"
- [ ] No compilation warnings or errors
