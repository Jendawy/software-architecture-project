# Class Diagram

This diagram shows the full class hierarchy of the Task Management System, including the **Domain Model** (Task interface, AbstractTask, and concrete task types), the **Factory Module** (Factory Method pattern for task creation), the **Strategy Module** (Strategy pattern for prioritization), and the **TaskManager** that orchestrates everything.

```mermaid
classDiagram
    direction TB

    class TaskStatus {
        <<enumeration>>
        OPEN
        IN_PROGRESS
        REVIEW
        DONE
        BLOCKED
        +canTransitionTo(status TaskStatus) boolean
    }

    class Task {
        <<interface>>
        +getId() int
        +getTitle() String
        +getDescription() String
        +getStatus() TaskStatus
        +setStatus(status TaskStatus) void
        +getPriority() int
        +getDeadline() LocalDate
        +setDeadline(deadline LocalDate) void
        +getType() String
        +getCreatedAt() LocalDateTime
    }

    class AbstractTask {
        <<abstract>>
        -id : int
        -title : String
        -description : String
        -status : TaskStatus
        -priority : int
        -deadline : LocalDate
        -createdAt : LocalDateTime
        +toString() String
    }

    class BugTask {
        -severity : String
        -stepsToReproduce : String
        +getType() String
        +getSeverity() String
        +setSeverity(severity String) void
        +getStepsToReproduce() String
    }

    class FeatureTask {
        -estimatedEffort : int
        -businessValue : int
        +getType() String
        +getEstimatedEffort() int
        +getBusinessValue() int
    }

    class DocumentationTask {
        -documentType : String
        -targetAudience : String
        +getType() String
        +getDocumentType() String
        +getTargetAudience() String
    }

    class TaskFactory {
        <<abstract>>
        +createTask(title String, description String, priority int) Task*
        +createTaskWithDeadline(title String, description String, priority int, deadline LocalDate) Task
    }

    class BugTaskFactory {
        +createTask(title String, description String, priority int) Task
        +createBugTask(title String, description String, priority int, severity String, steps String) BugTask
    }

    class FeatureTaskFactory {
        +createTask(title String, description String, priority int) Task
        +createFeatureTask(title String, description String, priority int, effort int, value int) FeatureTask
    }

    class DocumentationTaskFactory {
        +createTask(title String, description String, priority int) Task
        +createDocTask(title String, description String, priority int, docType String, audience String) DocumentationTask
    }

    class PriorityStrategy {
        <<interface>>
        +sort(tasks List~Task~) List~Task~
    }

    class UrgentFirstStrategy {
        +sort(tasks List~Task~) List~Task~
    }

    class DeadlineFirstStrategy {
        +sort(tasks List~Task~) List~Task~
    }

    class SeverityFirstStrategy {
        +sort(tasks List~Task~) List~Task~
    }

    class TaskManager {
        -tasks : List~Task~
        -currentStrategy : PriorityStrategy
        -factoryRegistry : Map~String, TaskFactory~
        +createTask(type String, title String, description String, priority int) Task
        +addTask(task Task) void
        +removeTask(taskId int) boolean
        +getTask(taskId int) Task
        +getAllTasks() List~Task~
        +getTasksByStatus(status TaskStatus) List~Task~
        +transitionTask(taskId int, newStatus TaskStatus) void
        +setPriorityStrategy(strategy PriorityStrategy) void
        +getPrioritizedTasks() List~Task~
        +getTaskSummary() String
        +registerFactory(type String, factory TaskFactory) void
    }

    Task <|.. AbstractTask : implements
    AbstractTask <|-- BugTask
    AbstractTask <|-- FeatureTask
    AbstractTask <|-- DocumentationTask
    AbstractTask --> TaskStatus : uses

    TaskFactory <|-- BugTaskFactory
    TaskFactory <|-- FeatureTaskFactory
    TaskFactory <|-- DocumentationTaskFactory
    TaskFactory ..> Task : creates

    PriorityStrategy <|.. UrgentFirstStrategy
    PriorityStrategy <|.. DeadlineFirstStrategy
    PriorityStrategy <|.. SeverityFirstStrategy

    TaskManager o-- "0..*" Task : aggregation
    TaskManager *-- "1" PriorityStrategy : composition
    TaskManager ..> TaskFactory : uses
```
