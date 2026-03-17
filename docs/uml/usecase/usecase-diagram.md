# Use Case Diagram

This diagram shows the use cases available to the **Project Manager** actor in the Task Management System. Task creation use cases include validation, and changing task status may trigger invalid-transition handling.

```mermaid
flowchart LR
    PM(("Project Manager"))

    subgraph Task Management System
        UC_Bug["Create Bug Task"]
        UC_Feature["Create Feature Task"]
        UC_Doc["Create Documentation Task"]
        UC_Validate["Validate Task Data"]
        UC_ViewAll["View All Tasks"]
        UC_ViewStatus["View Tasks by Status"]
        UC_Prioritize["Prioritize Tasks\n(with Strategy)"]
        UC_ChangeStatus["Change Task Status"]
        UC_InvalidTransition["Handle Invalid\nTransition"]
        UC_Remove["Remove Task"]
        UC_SwitchStrategy["Switch Priority\nStrategy"]
    end

    PM --> UC_Bug
    PM --> UC_Feature
    PM --> UC_Doc
    PM --> UC_ViewAll
    PM --> UC_ViewStatus
    PM --> UC_Prioritize
    PM --> UC_ChangeStatus
    PM --> UC_Remove
    PM --> UC_SwitchStrategy

    UC_Bug -.->|include| UC_Validate
    UC_Feature -.->|include| UC_Validate
    UC_Doc -.->|include| UC_Validate

    UC_ChangeStatus -.->|extend| UC_InvalidTransition
```
