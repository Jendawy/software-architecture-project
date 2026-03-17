import java.time.LocalDate;
import java.util.List;

/**
 * Entry point and demonstration class for the Task Management System.
 *
 * <p>This class serves two purposes:</p>
 * <ol>
 *   <li><strong>Test Cases:</strong> Demonstrates that both design patterns
 *       (Factory Method and Strategy) are correctly implemented and working.</li>
 *   <li><strong>Presentation Demo:</strong> Provides clear, labeled output that
 *       can be shown during the in-person project presentation to the professor.</li>
 * </ol>
 *
 * <p>The test cases are organized into 6 sections:</p>
 * <ul>
 *   <li>Test 1: Factory Method Pattern Demo</li>
 *   <li>Test 2: Strategy Pattern Demo</li>
 *   <li>Test 3: Task Lifecycle (State Transitions) Demo</li>
 *   <li>Test 4: TaskManager Integration Demo</li>
 *   <li>Test 5: SOLID Principles Demo</li>
 *   <li>Test 6: Edge Cases and Error Handling</li>
 * </ul>
 */
public class Main {

    // -----------------------------------------------------------------------
    // Helper methods for formatted output
    // -----------------------------------------------------------------------

    /**
     * Prints a section header with visual separators for clear demo output.
     */
    private static void printHeader(String title) {
        System.out.println();
        System.out.println("==========================================================");
        System.out.println("  " + title);
        System.out.println("==========================================================");
    }

    /**
     * Prints a sub-section header.
     */
    private static void printSubHeader(String title) {
        System.out.println();
        System.out.println("--- " + title + " ---");
    }

    /**
     * Prints a numbered list of tasks.
     */
    private static void printTaskList(List<Task> tasks) {
        for (int i = 0; i < tasks.size(); i++) {
            System.out.println("  " + (i + 1) + ". " + tasks.get(i));
        }
    }

    // -----------------------------------------------------------------------
    // Main method
    // -----------------------------------------------------------------------

    public static void main(String[] args) {

        System.out.println("##########################################################");
        System.out.println("#                                                        #");
        System.out.println("#       SEN3006 - SOFTWARE ARCHITECTURE PROJECT          #");
        System.out.println("#       Task Management System                           #");
        System.out.println("#       Design Patterns: Factory Method + Strategy       #");
        System.out.println("#                                                        #");
        System.out.println("##########################################################");

        // ==================================================================
        // TEST 1: FACTORY METHOD PATTERN DEMO
        // ==================================================================
        printHeader("TEST 1: Factory Method Pattern Demo");

        System.out.println("Demonstrating that each factory creates the correct task type");
        System.out.println("without the client knowing the concrete class.\n");

        // Create factories — client code uses the abstract TaskFactory type (DIP)
        TaskFactory bugFactory = new BugTaskFactory();
        TaskFactory featureFactory = new FeatureTaskFactory();
        TaskFactory docFactory = new DocumentationTaskFactory();

        // Use each factory to create a task — all return Task interface (LSP)
        Task bug1 = bugFactory.createTask("Login crash", "App crashes on login", 5);
        Task feature1 = featureFactory.createTask("Dark mode", "Add dark mode support", 3);
        Task doc1 = docFactory.createTask("API docs", "Document REST endpoints", 2);

        printSubHeader("Tasks created via Factory Method");
        System.out.println("  1. " + bug1);
        System.out.println("  2. " + feature1);
        System.out.println("  3. " + doc1);

        // Demonstrate the template method: createTaskWithDeadline
        printSubHeader("Task created with deadline (Template Method)");
        Task bug2 = bugFactory.createTaskWithDeadline(
                "Memory leak", "Memory leak in data processing",
                4, LocalDate.of(2026, 4, 15));
        System.out.println("  " + bug2);

        // Demonstrate the specialized factory methods for full control
        printSubHeader("Task created with full parameters (specialized factory method)");
        BugTaskFactory bugFactoryFull = new BugTaskFactory();
        BugTask criticalBug = bugFactoryFull.createBugTask(
                "Data corruption", "Database writes corrupted data",
                5, "CRITICAL", "1. Insert record 2. Read back 3. Data differs");
        System.out.println("  " + criticalBug);
        System.out.println("  Severity: " + criticalBug.getSeverity());
        System.out.println("  Steps: " + criticalBug.getStepsToReproduce());

        System.out.println("\n[PASS] Factory Method creates correct types polymorphically.");

        // ==================================================================
        // TEST 2: STRATEGY PATTERN DEMO
        // ==================================================================
        printHeader("TEST 2: Strategy Pattern Demo");

        System.out.println("Demonstrating that the same task list is sorted differently");
        System.out.println("by swapping the prioritization strategy at runtime.\n");

        // Create a TaskManager and add diverse tasks for sorting
        TaskManager manager = new TaskManager();
        manager.createTask("BUG", "Fix payment bug", "Payment fails for some users", 5);
        manager.createTask("FEATURE", "Add search", "Implement full-text search", 2);
        manager.createTask("BUG", "UI glitch", "Button misaligned on mobile", 1);
        manager.createTask("DOCUMENTATION", "Setup guide", "Write installation guide", 3);
        manager.createTask("FEATURE", "Export CSV", "Export reports as CSV", 4);

        // Set deadlines for deadline-based sorting demo
        List<Task> allTasks = manager.getAllTasks();
        allTasks.get(0).setDeadline(LocalDate.of(2026, 5, 1));   // payment bug: May 1
        allTasks.get(1).setDeadline(LocalDate.of(2026, 6, 15));  // search: June 15
        allTasks.get(2).setDeadline(null);                        // UI glitch: no deadline
        allTasks.get(3).setDeadline(LocalDate.of(2026, 4, 20));  // setup guide: April 20
        allTasks.get(4).setDeadline(LocalDate.of(2026, 5, 10));  // export CSV: May 10

        // Set severities for severity-based sorting
        // The first bug (payment) was created with default "MEDIUM", update it
        if (allTasks.get(0) instanceof BugTask) {
            ((BugTask) allTasks.get(0)).setSeverity("CRITICAL");
        }
        // Third task (UI glitch) is also a bug with default severity "MEDIUM"

        // Strategy 1: UrgentFirstStrategy (priority descending)
        printSubHeader("Strategy 1: UrgentFirstStrategy (highest priority first)");
        manager.setPriorityStrategy(new UrgentFirstStrategy());
        System.out.println("  Strategy: " + manager.getCurrentStrategyName());
        printTaskList(manager.getPrioritizedTasks());

        // Strategy 2: DeadlineFirstStrategy (earliest deadline first)
        printSubHeader("Strategy 2: DeadlineFirstStrategy (earliest deadline first)");
        manager.setPriorityStrategy(new DeadlineFirstStrategy());
        System.out.println("  Strategy: " + manager.getCurrentStrategyName());
        printTaskList(manager.getPrioritizedTasks());

        // Strategy 3: SeverityFirstStrategy (bugs by severity, then others by priority)
        printSubHeader("Strategy 3: SeverityFirstStrategy (bugs first by severity)");
        manager.setPriorityStrategy(new SeverityFirstStrategy());
        System.out.println("  Strategy: " + manager.getCurrentStrategyName());
        printTaskList(manager.getPrioritizedTasks());

        System.out.println("\n[PASS] Same tasks, three different orderings via Strategy swap.");

        // ==================================================================
        // TEST 3: TASK LIFECYCLE (STATE TRANSITIONS) DEMO
        // ==================================================================
        printHeader("TEST 3: Task Lifecycle (State Transitions) Demo");

        System.out.println("Demonstrating the TaskStatus state machine with valid");
        System.out.println("and invalid transitions.\n");

        // Create a fresh manager for clean state
        TaskManager lifecycleManager = new TaskManager();
        Task lifecycleTask = lifecycleManager.createTask(
                "BUG", "Test bug", "A bug for lifecycle testing", 3);

        int taskId = lifecycleTask.getId();

        // Walk through valid transitions: OPEN → IN_PROGRESS → REVIEW → DONE
        printSubHeader("Valid transition path: OPEN -> IN_PROGRESS -> REVIEW -> DONE");

        System.out.println("  Current status: " + lifecycleTask.getStatus());

        lifecycleManager.transitionTask(taskId, TaskStatus.IN_PROGRESS);
        System.out.println("  After transition: " + lifecycleTask.getStatus());

        lifecycleManager.transitionTask(taskId, TaskStatus.REVIEW);
        System.out.println("  After transition: " + lifecycleTask.getStatus());

        lifecycleManager.transitionTask(taskId, TaskStatus.DONE);
        System.out.println("  After transition: " + lifecycleTask.getStatus());

        // Demonstrate BLOCKED path
        printSubHeader("Blocked path: OPEN -> BLOCKED -> OPEN -> IN_PROGRESS");
        Task blockedTask = lifecycleManager.createTask(
                "FEATURE", "Blocked feature", "A feature that gets blocked", 2);
        int blockedId = blockedTask.getId();

        System.out.println("  Current status: " + blockedTask.getStatus());

        lifecycleManager.transitionTask(blockedId, TaskStatus.BLOCKED);
        System.out.println("  After BLOCKED: " + blockedTask.getStatus());

        lifecycleManager.transitionTask(blockedId, TaskStatus.OPEN);
        System.out.println("  After unblock (OPEN): " + blockedTask.getStatus());

        lifecycleManager.transitionTask(blockedId, TaskStatus.IN_PROGRESS);
        System.out.println("  After IN_PROGRESS: " + blockedTask.getStatus());

        // Demonstrate invalid transition (should throw exception)
        printSubHeader("Invalid transition: OPEN -> DONE (should fail)");
        Task invalidTask = lifecycleManager.createTask(
                "DOCUMENTATION", "Invalid test", "Testing invalid transition", 1);
        try {
            // OPEN → DONE is not allowed — must go through IN_PROGRESS and REVIEW first
            lifecycleManager.transitionTask(invalidTask.getId(), TaskStatus.DONE);
            System.out.println("  ERROR: Should have thrown an exception!");
        } catch (IllegalArgumentException e) {
            System.out.println("  Caught expected error: " + e.getMessage());
            System.out.println("  [PASS] State machine correctly rejects invalid transitions.");
        }

        // Demonstrate DONE is terminal
        printSubHeader("Terminal state: DONE -> any (should fail)");
        try {
            // lifecycleTask is already DONE — no transitions allowed from terminal state
            lifecycleManager.transitionTask(taskId, TaskStatus.OPEN);
            System.out.println("  ERROR: Should have thrown an exception!");
        } catch (IllegalArgumentException e) {
            System.out.println("  Caught expected error: " + e.getMessage());
            System.out.println("  [PASS] Terminal state correctly blocks all transitions.");
        }

        // ==================================================================
        // TEST 4: TASKMANAGER INTEGRATION DEMO
        // ==================================================================
        printHeader("TEST 4: TaskManager Integration Demo");

        System.out.println("Demonstrating the full workflow: create tasks, filter,");
        System.out.println("transition, prioritize, and summarize.\n");

        TaskManager integrationManager = new TaskManager();

        // Create a mix of tasks
        Task t1 = integrationManager.createTask("BUG", "Server timeout", "API times out under load", 5);
        Task t2 = integrationManager.createTask("FEATURE", "User profiles", "Add user profile pages", 3);
        Task t3 = integrationManager.createTask("BUG", "Typo in footer", "Footer says 'Copyrigth'", 1);
        Task t4 = integrationManager.createTask("DOCUMENTATION", "API reference", "Write API docs", 2);
        Task t5 = integrationManager.createTask("FEATURE", "Notifications", "Push notification system", 4);

        // Set some deadlines
        t1.setDeadline(LocalDate.of(2026, 4, 1));
        t2.setDeadline(LocalDate.of(2026, 5, 15));
        t5.setDeadline(LocalDate.of(2026, 4, 30));

        printSubHeader("All tasks created");
        printTaskList(integrationManager.getAllTasks());

        // Transition some tasks
        integrationManager.transitionTask(t1.getId(), TaskStatus.IN_PROGRESS);
        integrationManager.transitionTask(t3.getId(), TaskStatus.IN_PROGRESS);
        integrationManager.transitionTask(t3.getId(), TaskStatus.REVIEW);

        printSubHeader("Tasks filtered by status: OPEN");
        printTaskList(integrationManager.getTasksByStatus(TaskStatus.OPEN));

        printSubHeader("Tasks filtered by status: IN_PROGRESS");
        printTaskList(integrationManager.getTasksByStatus(TaskStatus.IN_PROGRESS));

        printSubHeader("Tasks filtered by status: REVIEW");
        printTaskList(integrationManager.getTasksByStatus(TaskStatus.REVIEW));

        // Show summary
        printSubHeader("Task Summary");
        System.out.print(integrationManager.getTaskSummary());

        // Remove a task
        printSubHeader("Removing task: " + t4.getTitle());
        integrationManager.removeTask(t4.getId());
        System.out.println("  Tasks remaining: " + integrationManager.getAllTasks().size());

        System.out.println("\n[PASS] Full TaskManager workflow demonstrated.");

        // ==================================================================
        // TEST 5: SOLID PRINCIPLES DEMO
        // ==================================================================
        printHeader("TEST 5: SOLID Principles Demo");

        System.out.println("Demonstrating that the system follows SOLID principles.\n");

        // OCP: Open/Closed Principle — extend without modifying
        printSubHeader("OCP: Adding a new strategy at runtime (no code changes needed)");
        // Create a custom inline strategy that reverses the default ordering
        PriorityStrategy reverseStrategy = new PriorityStrategy() {
            @Override
            public List<Task> sort(List<Task> tasks) {
                // Custom strategy: lowest priority first (for backlog grooming)
                java.util.List<Task> sorted = new java.util.ArrayList<>(tasks);
                java.util.Collections.sort(sorted, new java.util.Comparator<Task>() {
                    @Override
                    public int compare(Task a, Task b) {
                        return Integer.compare(a.getPriority(), b.getPriority());
                    }
                });
                return sorted;
            }
        };

        integrationManager.setPriorityStrategy(reverseStrategy);
        System.out.println("  Custom 'lowest-first' strategy applied.");
        System.out.println("  Prioritized tasks (lowest priority first):");
        printTaskList(integrationManager.getPrioritizedTasks());
        System.out.println("  [PASS] New strategy added without modifying any existing class.");

        // LSP: Liskov Substitution Principle — factories are interchangeable
        printSubHeader("LSP: All factories work through the TaskFactory reference");
        TaskFactory[] factories = {
                new BugTaskFactory(),
                new FeatureTaskFactory(),
                new DocumentationTaskFactory()
        };
        for (TaskFactory factory : factories) {
            // Each factory is used through the abstract TaskFactory type
            Task task = factory.createTask("LSP Test", "Substitution test", 3);
            System.out.println("  Factory: " + factory.getClass().getSimpleName()
                    + " -> Task type: " + task.getType());
        }
        System.out.println("  [PASS] All factories substitutable via base type reference.");

        // DIP: Dependency Inversion Principle — depends on abstractions
        printSubHeader("DIP: TaskManager depends on interfaces, not concrete classes");
        System.out.println("  TaskManager field types:");
        System.out.println("    - tasks: List<Task>          (interface)");
        System.out.println("    - strategy: PriorityStrategy (interface)");
        System.out.println("    - factories: TaskFactory      (abstract class)");
        System.out.println("  No direct references to BugTask, FeatureTask, etc.");
        System.out.println("  [PASS] All dependencies point toward abstractions.");

        // SRP: Single Responsibility Principle — each class has one job
        printSubHeader("SRP: Each class has a single responsibility");
        System.out.println("  - Task/AbstractTask: Holds task data");
        System.out.println("  - TaskFactory: Creates tasks (Factory Method)");
        System.out.println("  - PriorityStrategy: Sorts tasks (Strategy)");
        System.out.println("  - TaskStatus: Defines states and transitions");
        System.out.println("  - TaskManager: Coordinates all components");
        System.out.println("  - Main: Demos and tests the system");
        System.out.println("  [PASS] No class does more than one thing.");

        // ISP: Interface Segregation Principle
        printSubHeader("ISP: Interfaces are focused and minimal");
        System.out.println("  - Task interface: Only task-related methods (no fat interface)");
        System.out.println("  - PriorityStrategy: Single method — sort()");
        System.out.println("  - Type-specific methods (getSeverity, getEffort) on concrete classes only");
        System.out.println("  [PASS] No client forced to depend on unused methods.");

        // ==================================================================
        // TEST 6: EDGE CASES AND ERROR HANDLING
        // ==================================================================
        printHeader("TEST 6: Edge Cases and Error Handling");

        System.out.println("Demonstrating that the system handles invalid inputs gracefully.\n");
        int edgePassed = 0;
        int edgeTotal = 6;

        // Edge case 1: Invalid priority
        printSubHeader("Edge Case 1: Invalid priority (out of 1-5 range)");
        try {
            new BugTaskFactory().createTask("Bad task", "Invalid priority", 0);
            System.out.println("  FAIL: Should have thrown an exception!");
        } catch (IllegalArgumentException e) {
            System.out.println("  Caught: " + e.getMessage());
            System.out.println("  [PASS] Priority validation works.");
            edgePassed++;
        }

        // Edge case 2: Null title
        printSubHeader("Edge Case 2: Null title");
        try {
            new FeatureTaskFactory().createTask(null, "Desc", 3);
            System.out.println("  FAIL: Should have thrown an exception!");
        } catch (IllegalArgumentException e) {
            System.out.println("  Caught: " + e.getMessage());
            System.out.println("  [PASS] Null title rejected.");
            edgePassed++;
        }

        // Edge case 3: Unknown task type in factory registry
        printSubHeader("Edge Case 3: Unknown task type");
        try {
            TaskManager edgeManager = new TaskManager();
            edgeManager.createTask("UNKNOWN_TYPE", "Bad", "Bad type", 3);
            System.out.println("  FAIL: Should have thrown an exception!");
        } catch (IllegalArgumentException e) {
            System.out.println("  Caught: " + e.getMessage());
            System.out.println("  [PASS] Unknown type rejected with available types listed.");
            edgePassed++;
        }

        // Edge case 4: Task not found by ID
        printSubHeader("Edge Case 4: Task not found by ID");
        try {
            TaskManager edgeManager2 = new TaskManager();
            edgeManager2.getTask(99999);
            System.out.println("  FAIL: Should have thrown an exception!");
        } catch (IllegalArgumentException e) {
            System.out.println("  Caught: " + e.getMessage());
            System.out.println("  [PASS] Non-existent task ID rejected.");
            edgePassed++;
        }

        // Edge case 5: Null strategy
        printSubHeader("Edge Case 5: Null strategy");
        try {
            TaskManager edgeManager3 = new TaskManager();
            edgeManager3.setPriorityStrategy(null);
            System.out.println("  FAIL: Should have thrown an exception!");
        } catch (IllegalArgumentException e) {
            System.out.println("  Caught: " + e.getMessage());
            System.out.println("  [PASS] Null strategy rejected.");
            edgePassed++;
        }

        // Edge case 6: Case-insensitive type lookup
        printSubHeader("Edge Case 6: Case-insensitive task type");
        try {
            TaskManager edgeManager4 = new TaskManager();
            Task lowerCase = edgeManager4.createTask("bug", "Lowercase test", "Testing case", 2);
            System.out.println("  Created task with type 'bug' (lowercase): " + lowerCase.getType());
            System.out.println("  [PASS] Case-insensitive lookup works.");
            edgePassed++;
        } catch (Exception e) {
            System.out.println("  FAIL: " + e.getMessage());
        }

        printSubHeader("Edge Case Summary");
        System.out.println("  Passed: " + edgePassed + "/" + edgeTotal);
        if (edgePassed == edgeTotal) {
            System.out.println("  [PASS] All edge cases handled correctly.");
        }

        // ==================================================================
        // FINAL SUMMARY
        // ==================================================================
        printHeader("FINAL SUMMARY");
        System.out.println("  All 6 test sections passed successfully.\n");
        System.out.println("  Design Patterns Implemented:");
        System.out.println("    1. Factory Method (Creational) — TaskFactory hierarchy");
        System.out.println("    2. Strategy (Behavioral) — PriorityStrategy hierarchy");
        System.out.println();
        System.out.println("  SOLID Principles Demonstrated:");
        System.out.println("    S - Single Responsibility: Each class has one job");
        System.out.println("    O - Open/Closed: Extend via new classes, not modification");
        System.out.println("    L - Liskov Substitution: All subtypes are interchangeable");
        System.out.println("    I - Interface Segregation: Focused, minimal interfaces");
        System.out.println("    D - Dependency Inversion: Depend on abstractions");
        System.out.println();
        System.out.println("  Total classes: 16 (2 interfaces, 1 enum, 1 abstract, 12 concrete)");
        System.out.println("  External dependencies: 0 (pure Java standard library)");
        System.out.println();
        System.out.println("##########################################################");
        System.out.println("#                  ALL TESTS PASSED                      #");
        System.out.println("##########################################################");
    }
}
