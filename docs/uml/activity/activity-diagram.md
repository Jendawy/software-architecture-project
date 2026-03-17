# Activity Diagram

This diagram models the **task lifecycle** from creation through prioritization to completion. It shows the decision points for task type selection, the parallel choice of priority strategy, and the review/rework loop.

```mermaid
flowchart TD
    Start([Start]) --> SelectType["Select Task Type"]

    SelectType --> TypeCheck{"Task Type?"}
    TypeCheck -->|Bug| BugFactory["Create via BugTaskFactory"]
    TypeCheck -->|Feature| FeatureFactory["Create via FeatureTaskFactory"]
    TypeCheck -->|Documentation| DocFactory["Create via DocumentationTaskFactory"]

    BugFactory --> AddTask["Add Task to TaskManager"]
    FeatureFactory --> AddTask
    DocFactory --> AddTask

    AddTask --> SelectStrategy["Select Priority Strategy"]

    SelectStrategy --> Urgent["UrgentFirstStrategy"]
    SelectStrategy --> Deadline["DeadlineFirstStrategy"]
    SelectStrategy --> Severity["SeverityFirstStrategy"]

    Urgent --> GetPrioritized["Get Prioritized Task List"]
    Deadline --> GetPrioritized
    Severity --> GetPrioritized

    GetPrioritized --> ProcessTask["Process Task"]

    ProcessTask --> NeedsReview{"Needs Review?"}

    NeedsReview -->|Yes| SubmitReview["Submit for Review"]
    SubmitReview --> ReviewTask["Review Task"]
    ReviewTask --> Approved{"Approved?"}

    Approved -->|Yes| MarkDone1["Mark as DONE"]
    Approved -->|No| ReturnIP["Return to IN_PROGRESS"]
    ReturnIP --> ProcessTask

    NeedsReview -->|No| MarkDone2["Mark as DONE"]

    MarkDone1 --> Stop([End])
    MarkDone2 --> Stop
```
