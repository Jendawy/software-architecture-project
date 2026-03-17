# State Diagram

This diagram shows the valid **status transitions** for a Task in the system. Tasks start in OPEN, move through IN_PROGRESS and REVIEW, and end in DONE. Tasks can be BLOCKED from OPEN or IN_PROGRESS and can only return to OPEN when unblocked.

```mermaid
stateDiagram-v2
    [*] --> OPEN : Task created

    OPEN --> IN_PROGRESS : assign
    OPEN --> BLOCKED : block

    IN_PROGRESS --> REVIEW : submit for review
    IN_PROGRESS --> BLOCKED : block

    REVIEW --> DONE : approve
    REVIEW --> IN_PROGRESS : reject / request changes

    BLOCKED --> OPEN : unblock

    DONE --> [*]

    note right of DONE
        Final state:
        Task is complete
    end note

    note left of BLOCKED
        Blocked tasks can
        only return to OPEN
    end note
```
