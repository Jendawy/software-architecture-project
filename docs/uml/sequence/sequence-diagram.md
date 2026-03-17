# Sequence Diagram

This diagram illustrates the runtime interactions for **creating a Bug task** and **prioritizing tasks** using the Deadline-First strategy. It shows how the Project Manager's request flows through Main, TaskManager, the factory registry, BugTaskFactory, and the strategy object.

```mermaid
sequenceDiagram
    actor PM as Project Manager
    participant Main
    participant TM as TaskManager
    participant Registry as factoryRegistry<br/>Map~String,TaskFactory~
    participant BTF as BugTaskFactory
    participant BT as BugTask
    participant DFS as DeadlineFirstStrategy

    rect rgb(240, 248, 255)
        Note over PM, BT: Task Creation
        PM->>Main: createTask("BUG", "Fix login", "Login fails", 1)
        activate Main
        Main->>TM: createTask("BUG", "Fix login", "Login fails", 1)
        activate TM
        TM->>Registry: get("BUG")
        activate Registry
        Registry-->>TM: bugTaskFactory
        deactivate Registry
        TM->>BTF: createTask("Fix login", "Login fails", 1)
        activate BTF
        BTF->>BT: new BugTask("Fix login", "Login fails", 1, "MEDIUM", "")
        activate BT
        BT-->>BTF: bugTask
        deactivate BT
        BTF-->>TM: bugTask
        deactivate BTF
        TM->>TM: tasks.add(bugTask)
        TM-->>Main: bugTask
        deactivate TM
        Main-->>PM: Task created successfully
        deactivate Main
    end

    rect rgb(245, 255, 245)
        Note over PM, DFS: Prioritization
        PM->>Main: setPriorityStrategy(new DeadlineFirstStrategy())
        activate Main
        Main->>TM: setPriorityStrategy(deadlineFirstStrategy)
        activate TM
        TM->>TM: currentStrategy = deadlineFirstStrategy
        TM-->>Main: void
        deactivate TM

        PM->>Main: getPrioritizedTasks()
        Main->>TM: getPrioritizedTasks()
        activate TM
        TM->>DFS: sort(tasks)
        activate DFS
        DFS->>DFS: sort by deadline (earliest first)
        DFS-->>TM: sortedTasks
        deactivate DFS
        TM-->>Main: sortedTasks
        deactivate TM
        Main-->>PM: Display prioritized task list
        deactivate Main
    end
```
