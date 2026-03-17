import java.time.LocalDate;

/**
 * Abstract Creator in the Factory Method design pattern.
 *
 * <p>This abstract class defines the <em>factory method</em> {@link #createTask(String, String, int)}
 * that concrete subclasses must override to instantiate specific {@link Task} implementations.
 * By declaring the factory method as abstract, this class defers the decision of which concrete
 * {@code Task} to create to its subclasses, enabling polymorphic object creation.</p>
 *
 * <h2>Role in the Factory Method Pattern</h2>
 * <p>This is the <strong>Creator</strong> (also called Abstract Creator). It declares the factory
 * method signature but does not implement it. The Creator may also contain business logic that
 * relies on the product returned by the factory method, as demonstrated by
 * {@link #createTaskWithDeadline(String, String, int, LocalDate)}, which internally calls the
 * factory method and then configures the resulting task. This secondary method is an example of
 * the <em>Template Method</em> mini-pattern: it defines a skeleton algorithm (create + configure)
 * while letting subclasses supply the "create" step.</p>
 *
 * <h2>SOLID Principles Demonstrated</h2>
 * <ul>
 *   <li><strong>Open/Closed Principle (OCP):</strong> Adding a new task type (e.g., ResearchTask)
 *       requires only a new factory subclass. This class remains closed for modification but open
 *       for extension through inheritance.</li>
 *   <li><strong>Dependency Inversion Principle (DIP):</strong> Client code depends on this
 *       abstraction rather than on concrete factory classes, allowing the concrete factory to be
 *       swapped at runtime without affecting the client.</li>
 *   <li><strong>Single Responsibility Principle (SRP):</strong> This class has one responsibility:
 *       defining the contract for task creation. It does not contain task-specific logic such as
 *       severity levels or effort estimates.</li>
 * </ul>
 *
 * <h2>Usage Example</h2>
 * <pre>{@code
 *     // Client code works with the abstract type
 *     TaskFactory factory = new BugTaskFactory();
 *     Task task = factory.createTask("Fix NPE", "Null pointer in login", 1);
 *
 *     // Or with a deadline
 *     Task urgent = factory.createTaskWithDeadline(
 *         "Fix NPE", "Null pointer in login", 1, LocalDate.now().plusDays(3));
 * }</pre>
 *
 * @see Task
 * @see BugTaskFactory
 * @see FeatureTaskFactory
 * @see DocumentationTaskFactory
 */
public abstract class TaskFactory {

    /**
     * Factory method that concrete subclasses must implement to create a specific type of
     * {@link Task}.
     *
     * <p>This is the core of the Factory Method pattern. Each subclass decides which concrete
     * {@code Task} implementation to instantiate and return. The caller receives a {@code Task}
     * reference and remains decoupled from the concrete class, satisfying the Dependency
     * Inversion Principle.</p>
     *
     * <p>Subclass implementations may apply sensible defaults for parameters that are specific
     * to their task type (e.g., a default severity for bug tasks). For full control over all
     * parameters, subclasses typically offer an additional, more specific factory method.</p>
     *
     * @param title       a short, descriptive title for the task; must not be {@code null}
     * @param description a detailed explanation of what the task involves; must not be {@code null}
     * @param priority    an integer priority from 1 (lowest) to 5 (highest)
     * @return a new {@link Task} instance of the type determined by the concrete factory subclass
     */
    public abstract Task createTask(String title, String description, int priority);

    /**
     * Template method that creates a task and assigns a deadline to it.
     *
     * <p>This method demonstrates the <em>Template Method</em> mini-pattern within the Factory
     * Method pattern. It defines a two-step algorithm:</p>
     * <ol>
     *   <li>Delegate to the abstract {@link #createTask(String, String, int)} factory method
     *       to obtain a concrete {@code Task} instance.</li>
     *   <li>Set the provided deadline on the newly created task.</li>
     * </ol>
     *
     * <p>Because step 1 is abstract, each subclass controls which type of task is created,
     * while this method controls the post-creation configuration. This separation keeps
     * deadline-setting logic in one place (SRP) and avoids duplicating it across every
     * concrete factory.</p>
     *
     * @param title       a short, descriptive title for the task; must not be {@code null}
     * @param description a detailed explanation of what the task involves; must not be {@code null}
     * @param priority    an integer priority from 1 (lowest) to 5 (highest)
     * @param deadline    the date by which the task should be completed; must not be {@code null}
     * @return a new {@link Task} instance with its deadline set to the specified date
     */
    public Task createTaskWithDeadline(String title, String description, int priority,
                                       LocalDate deadline) {
        // Step 1: Delegate object creation to the subclass-provided factory method.
        Task task = createTask(title, description, priority);

        // Step 2: Apply the cross-cutting deadline concern. This logic lives here so
        // that every concrete factory benefits from it without repeating the code.
        task.setDeadline(deadline);

        return task;
    }
}
