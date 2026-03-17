# Task Management System — Design Specification

## Problem Statement

Software development teams manage heterogeneous tasks (bugs, features, documentation) that require different creation workflows and flexible prioritization strategies. A rigid system forces teams into a single workflow; this system uses design patterns to allow extensibility without modifying existing code.

## Selected Design Patterns

### Factory Method (Creational)
- **Creator:** `TaskFactory` (abstract class)
- **Concrete Creators:** `BugTaskFactory`, `FeatureTaskFactory`, `DocumentationTaskFactory`
- **Product:** `Task` (interface)
- **Concrete Products:** `BugTask`, `FeatureTask`, `DocumentationTask`

### Strategy (Behavioral)
- **Context:** `TaskManager`
- **Strategy:** `PriorityStrategy` (interface)
- **Concrete Strategies:** `UrgentFirstStrategy`, `DeadlineFirstStrategy`, `SeverityFirstStrategy`

## State Machine — TaskStatus

```
OPEN ──────→ IN_PROGRESS ──────→ REVIEW ──────→ DONE (terminal)
  │               │                 │
  └──→ BLOCKED    └──→ BLOCKED      └──→ IN_PROGRESS (reject)
         │
         └──→ OPEN (unblock)
```

Allowed transitions:
- OPEN → IN_PROGRESS, BLOCKED
- IN_PROGRESS → REVIEW, BLOCKED
- REVIEW → DONE, IN_PROGRESS
- BLOCKED → OPEN
- DONE → (none — terminal state)

## Class Inventory

### TaskStatus.java (Enum)
```java
public enum TaskStatus {
    OPEN, IN_PROGRESS, REVIEW, DONE, BLOCKED;
    public boolean canTransitionTo(TaskStatus next) { ... }
}
```

### Task.java (Interface)
```java
public interface Task {
    int getId();
    String getTitle();
    String getDescription();
    TaskStatus getStatus();
    void setStatus(TaskStatus status);
    int getPriority();
    LocalDate getDeadline();
    void setDeadline(LocalDate deadline);
    String getType();
    LocalDateTime getCreatedAt();
}
```

### AbstractTask.java (Abstract Class)
- Implements `Task`
- Fields: `id` (auto-increment via static counter), `title`, `description`, `status`, `priority`, `deadline`, `createdAt`
- Provides `toString()` with common fields

### BugTask.java
- Extends `AbstractTask`
- Extra fields: `severity` (String: LOW/MEDIUM/HIGH/CRITICAL), `stepsToReproduce` (String)
- Getters + setters for extra fields

### FeatureTask.java
- Extends `AbstractTask`
- Extra fields: `estimatedEffort` (int, hours), `businessValue` (int, 1-10)

### DocumentationTask.java
- Extends `AbstractTask`
- Extra fields: `documentType` (String: API/USER_GUIDE/TUTORIAL), `targetAudience` (String)

### TaskFactory.java (Abstract Class)
```java
public abstract class TaskFactory {
    public abstract Task createTask(String title, String description, int priority);
    public Task createTaskWithDeadline(String title, String description, int priority, LocalDate deadline) {
        Task task = createTask(title, description, priority);
        task.setDeadline(deadline);
        return task;
    }
}
```

### BugTaskFactory.java
- `createTask()` returns `new BugTask(title, desc, priority, "MEDIUM", "")`

### FeatureTaskFactory.java
- `createTask()` returns `new FeatureTask(title, desc, priority, 8, 5)`

### DocumentationTaskFactory.java
- `createTask()` returns `new DocumentationTask(title, desc, priority, "API", "Developers")`

### PriorityStrategy.java (Interface)
```java
public interface PriorityStrategy {
    List<Task> sort(List<Task> tasks);
}
```

### UrgentFirstStrategy.java
- Sorts by `getPriority()` descending

### DeadlineFirstStrategy.java
- Sorts by `getDeadline()` ascending, nulls last

### SeverityFirstStrategy.java
- BugTasks sorted by severity rank first, then others by priority

### TaskManager.java
```java
public class TaskManager {
    private List<Task> tasks;
    private PriorityStrategy currentStrategy;
    private Map<String, TaskFactory> factoryRegistry;

    public Task createTask(String type, String title, String description, int priority) { ... }
    public void addTask(Task task) { ... }
    public void removeTask(int taskId) { ... }
    public Task getTask(int taskId) { ... }
    public List<Task> getAllTasks() { ... }
    public List<Task> getTasksByStatus(TaskStatus status) { ... }
    public void transitionTask(int taskId, TaskStatus newStatus) { ... }
    public void setPriorityStrategy(PriorityStrategy strategy) { ... }
    public List<Task> getPrioritizedTasks() { ... }
    public String getTaskSummary() { ... }
}
```

### Main.java
- Test 1: Factory Method Demo
- Test 2: Strategy Demo
- Test 3: Task Lifecycle Demo
- Test 4: TaskManager Integration
- Test 5: SOLID Principles Demo
