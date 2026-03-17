import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


/**
 * Central coordinator for the Task Management System.
 *
 * <p>This class acts as the <strong>Client</strong> in both the Factory Method
 * and Strategy design patterns:</p>
 * <ul>
 *   <li><strong>Factory Method Client:</strong> Uses a registry of {@link TaskFactory}
 *       instances to create tasks by type string (e.g., "BUG", "FEATURE", "DOCUMENTATION").
 *       The manager never directly instantiates concrete task classes — it delegates
 *       creation to the appropriate factory, staying decoupled from concrete products.</li>
 *   <li><strong>Strategy Context:</strong> Holds a reference to a {@link PriorityStrategy}
 *       that can be swapped at runtime. When asked for a prioritized list, it delegates
 *       the sorting to whichever strategy is currently set, allowing the prioritization
 *       algorithm to change without modifying this class.</li>
 * </ul>
 *
 * <h2>Additional Pattern: Service Locator (Simplified)</h2>
 * <p>The internal {@code factoryRegistry} map acts as a simplified Service Locator,
 * mapping type strings to factory instances. This adds a creative twist beyond the
 * standard Factory Method pattern — clients can request task creation by name without
 * knowing which factory to use.</p>
 *
 * <h2>SOLID Principles Demonstrated</h2>
 * <ul>
 *   <li><strong>Single Responsibility (SRP):</strong> Manages the task collection and
 *       coordinates between factories and strategies. Does not contain creation logic
 *       (factories do that) or sorting logic (strategies do that).</li>
 *   <li><strong>Open/Closed (OCP):</strong> New task types or strategies can be added
 *       by registering new factories or setting a new strategy — no modification to
 *       this class is needed.</li>
 *   <li><strong>Dependency Inversion (DIP):</strong> Depends on abstractions
 *       ({@link Task}, {@link TaskFactory}, {@link PriorityStrategy}), not on concrete
 *       classes like {@link BugTask} or {@link UrgentFirstStrategy}.</li>
 * </ul>
 *
 * @see TaskFactory
 * @see PriorityStrategy
 * @see Task
 */
public class TaskManager {

    // -----------------------------------------------------------------------
    // Fields
    // -----------------------------------------------------------------------

    /** The collection of all tasks managed by this instance. */
    private final List<Task> tasks;

    /** The currently active prioritization strategy (Strategy pattern). */
    private PriorityStrategy currentStrategy;

    /**
     * Registry mapping task type strings (e.g., "BUG") to their corresponding
     * factory instances. Acts as a simplified Service Locator.
     */
    private final Map<String, TaskFactory> factoryRegistry;

    // -----------------------------------------------------------------------
    // Constructor
    // -----------------------------------------------------------------------

    /**
     * Creates a new TaskManager with all built-in factories registered and
     * the {@link UrgentFirstStrategy} as the default prioritization strategy.
     *
     * <p>The constructor pre-registers factories for BUG, FEATURE, and
     * DOCUMENTATION task types. Additional factories can be registered later
     * via {@link #registerFactory(String, TaskFactory)}.</p>
     */
    public TaskManager() {
        this.tasks = new ArrayList<>();
        this.factoryRegistry = new HashMap<>();

        // Register all built-in factories — this is the Service Locator setup.
        // Each type string maps to its corresponding concrete factory.
        factoryRegistry.put("BUG", new BugTaskFactory());
        factoryRegistry.put("FEATURE", new FeatureTaskFactory());
        factoryRegistry.put("DOCUMENTATION", new DocumentationTaskFactory());

        // Default strategy: urgent-first (highest priority number first)
        this.currentStrategy = new UrgentFirstStrategy();
    }

    // -----------------------------------------------------------------------
    // Factory Method integration
    // -----------------------------------------------------------------------

    /**
     * Creates a task using the registered factory for the given type.
     *
     * <p>This method demonstrates the Factory Method pattern in action: the caller
     * specifies a type string and task details, and the appropriate factory handles
     * the actual object creation. The caller never needs to know which concrete
     * class is instantiated.</p>
     *
     * @param type        the task type key (e.g., "BUG", "FEATURE", "DOCUMENTATION")
     * @param title       a short title for the task
     * @param description detailed task description
     * @param priority    priority from 1 (lowest) to 5 (highest)
     * @return the newly created and registered {@link Task}
     * @throws IllegalArgumentException if the type is not registered
     */
    public Task createTask(String type, String title, String description, int priority) {
        // Look up the factory for this type in the registry
        TaskFactory factory = factoryRegistry.get(type.toUpperCase());
        if (factory == null) {
            throw new IllegalArgumentException(
                    "No factory registered for task type: " + type
                    + ". Available types: " + factoryRegistry.keySet());
        }

        // Delegate creation to the factory (Factory Method pattern)
        Task task = factory.createTask(title, description, priority);

        // Add the new task to our managed collection
        tasks.add(task);
        return task;
    }

    /**
     * Registers a new factory for a given task type, extending the system
     * without modifying existing code (OCP in action).
     *
     * @param type    the type key to register
     * @param factory the factory instance for that type
     */
    public void registerFactory(String type, TaskFactory factory) {
        factoryRegistry.put(type.toUpperCase(), factory);
    }

    // -----------------------------------------------------------------------
    // Task collection management
    // -----------------------------------------------------------------------

    /**
     * Adds an externally created task to the managed collection.
     *
     * @param task the task to add; must not be {@code null}
     */
    public void addTask(Task task) {
        if (task == null) {
            throw new IllegalArgumentException("Task must not be null.");
        }
        tasks.add(task);
    }

    /**
     * Removes a task by its unique ID.
     *
     * @param taskId the ID of the task to remove
     * @return {@code true} if a task was found and removed, {@code false} otherwise
     */
    public boolean removeTask(int taskId) {
        return tasks.removeIf(task -> task.getId() == taskId);
    }

    /**
     * Finds a task by its unique ID.
     *
     * @param taskId the ID to search for
     * @return the matching {@link Task}
     * @throws IllegalArgumentException if no task with the given ID exists
     */
    public Task getTask(int taskId) {
        for (Task task : tasks) {
            if (task.getId() == taskId) {
                return task;
            }
        }
        throw new IllegalArgumentException("No task found with ID: " + taskId);
    }

    /**
     * Returns an unmodifiable view of all managed tasks.
     *
     * @return an unmodifiable list of all tasks
     */
    public List<Task> getAllTasks() {
        return Collections.unmodifiableList(tasks);
    }

    /**
     * Returns all tasks that have the given status.
     *
     * @param status the status to filter by
     * @return a new list containing only tasks with the matching status
     */
    public List<Task> getTasksByStatus(TaskStatus status) {
        List<Task> filtered = new ArrayList<>();
        for (Task task : tasks) {
            if (task.getStatus() == status) {
                filtered.add(task);
            }
        }
        return filtered;
    }

    // -----------------------------------------------------------------------
    // State transition management
    // -----------------------------------------------------------------------

    /**
     * Transitions a task to a new status, validating against the state machine.
     *
     * <p>If the transition is not allowed by {@link TaskStatus#canTransitionTo(TaskStatus)},
     * an {@link IllegalArgumentException} is thrown. This prevents invalid state changes
     * and ensures data integrity.</p>
     *
     * @param taskId    the ID of the task to transition
     * @param newStatus the target status
     * @throws IllegalArgumentException if the task is not found or the transition is invalid
     */
    public void transitionTask(int taskId, TaskStatus newStatus) {
        Task task = getTask(taskId);
        // setStatus() on AbstractTask validates the transition internally
        task.setStatus(newStatus);
    }

    // -----------------------------------------------------------------------
    // Strategy Pattern integration
    // -----------------------------------------------------------------------

    /**
     * Swaps the current prioritization strategy at runtime.
     *
     * <p>This is the core of the Strategy pattern: the algorithm for sorting tasks
     * is encapsulated in strategy objects that can be exchanged freely. After calling
     * this method, all subsequent calls to {@link #getPrioritizedTasks()} will use
     * the new strategy.</p>
     *
     * @param strategy the new strategy to use; must not be {@code null}
     */
    public void setPriorityStrategy(PriorityStrategy strategy) {
        if (strategy == null) {
            throw new IllegalArgumentException("Strategy must not be null.");
        }
        this.currentStrategy = strategy;
    }

    /**
     * Returns the current strategy name for display purposes.
     *
     * @return the simple class name of the current strategy
     */
    public String getCurrentStrategyName() {
        return currentStrategy.getClass().getSimpleName();
    }

    /**
     * Returns all tasks sorted according to the current prioritization strategy.
     *
     * <p>Delegates to {@link PriorityStrategy#sort(List)}, which returns a new
     * sorted list without modifying the original collection.</p>
     *
     * @return a new list of tasks sorted by the current strategy
     */
    public List<Task> getPrioritizedTasks() {
        // Delegate sorting to the current strategy (Strategy pattern in action)
        return currentStrategy.sort(tasks);
    }

    // -----------------------------------------------------------------------
    // Reporting
    // -----------------------------------------------------------------------

    /**
     * Returns a summary of all tasks grouped by status.
     *
     * <p>Useful for dashboards and presentation demonstrations.</p>
     *
     * @return a formatted string with task counts per status
     */
    public String getTaskSummary() {
        StringBuilder sb = new StringBuilder();
        sb.append("=== Task Summary ===\n");
        sb.append(String.format("  Total tasks: %d\n", tasks.size()));

        // Count tasks per status
        for (TaskStatus status : TaskStatus.values()) {
            long count = 0;
            for (Task task : tasks) {
                if (task.getStatus() == status) {
                    count++;
                }
            }
            if (count > 0) {
                sb.append(String.format("  %s: %d\n", status, count));
            }
        }

        sb.append(String.format("  Current strategy: %s\n", getCurrentStrategyName()));
        return sb.toString();
    }
}
