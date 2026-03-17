# Component Diagram

This diagram shows the high-level **module structure** of the Task Management System and the dependencies between components. The UI Module depends on the Manager, which in turn delegates to the Factory and Strategy modules and manages Domain Model entities.

```mermaid
flowchart TB
    subgraph UI_Module["UI Module"]
        Main["Main"]
    end

    subgraph Manager_Module["Manager Module"]
        MGR["TaskManager"]
    end

    subgraph Factory_Module["Factory Module"]
        TF["TaskFactory"]
        BTF["BugTaskFactory"] -->|extends| TF
        FTF["FeatureTaskFactory"] -->|extends| TF
        DTF["DocumentationTaskFactory"] -->|extends| TF
    end

    subgraph Strategy_Module["Strategy Module"]
        PS["PriorityStrategy"]
        UFS["UrgentFirstStrategy"] -->|implements| PS
        DFS["DeadlineFirstStrategy"] -->|implements| PS
        SFS["SeverityFirstStrategy"] -->|implements| PS
    end

    subgraph Domain_Model["Domain Model"]
        T["Task"]
        AT["AbstractTask"] -->|implements| T
        BT["BugTask"] -->|extends| AT
        FT["FeatureTask"] -->|extends| AT
        DT["DocumentationTask"] -->|extends| AT
        TS["TaskStatus"]
        AT --> TS
    end

    Main -->|uses| MGR
    MGR -->|creates tasks via| TF
    MGR -->|delegates sorting to| PS
    MGR -->|manages| T
    TF -->|produces| T
```
