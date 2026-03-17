import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Defines the contract for all task types in the Task Management System.
 *
 * <h3>Design Pattern Role</h3>
 * <p>This is the <strong>Product</strong> interface in the
 * <strong>Factory Method</strong> pattern. Concrete products such as
 * {@link BugTask}, {@link FeatureTask}, and {@link DocumentationTask} implement
 * this interface (via {@link AbstractTask}). A factory class can create any of
 * these concrete products and return them through this common interface,
 * allowing client code to work with tasks polymorphically without knowing
 * the concrete type.</p>
 *
 * <h3>SOLID Principles Demonstrated</h3>
 * <ul>
 *   <li><strong>Interface Segregation Principle (ISP)</strong> -- Every method
 *       declared here is relevant to <em>all</em> task types. There are no
 *       "fat interface" methods that only some implementations need. Type-specific
 *       behaviour (e.g., severity for bugs, estimated effort for features) is
 *       kept on the concrete classes, not forced into this interface.</li>
 *   <li><strong>Dependency Inversion Principle (DIP)</strong> -- High-level modules
 *       (services, repositories, UI layers) depend on this abstraction rather
 *       than on concrete task classes, making the system easier to extend and test.</li>
 *   <li><strong>Liskov Substitution Principle (LSP)</strong> -- Any concrete Task
 *       implementation can be used wherever a {@code Task} reference is expected
 *       without altering the correctness of the program.</li>
 * </ul>
 *
 * @see AbstractTask
 * @see BugTask
 * @see FeatureTask
 * @see DocumentationTask
 * @see TaskStatus
 */
public interface Task {

    /**
     * Returns the unique identifier for this task.
     * IDs are auto-generated and monotonically increasing.
     *
     * @return the task ID
     */
    int getId();

    /**
     * Returns the short, human-readable title of this task.
     *
     * @return the task title, never {@code null}
     */
    String getTitle();

    /**
     * Returns a detailed description of what this task involves.
     *
     * @return the task description, never {@code null}
     */
    String getDescription();

    /**
     * Returns the current lifecycle status of this task.
     *
     * @return the current {@link TaskStatus}
     */
    TaskStatus getStatus();

    /**
     * Updates the lifecycle status of this task.
     * Implementations should validate that the transition is allowed
     * by the {@link TaskStatus} state machine.
     *
     * @param status the new status to set
     * @throws IllegalArgumentException if the transition is not permitted
     */
    void setStatus(TaskStatus status);

    /**
     * Returns the priority level of this task.
     * Priority ranges from 1 (lowest) to 5 (highest).
     *
     * @return an integer between 1 and 5 inclusive
     */
    int getPriority();

    /**
     * Returns the deadline for this task, or {@code null} if no deadline is set.
     *
     * @return the deadline date, or {@code null}
     */
    LocalDate getDeadline();

    /**
     * Sets or clears the deadline for this task.
     *
     * @param deadline the new deadline, or {@code null} to remove the deadline
     */
    void setDeadline(LocalDate deadline);

    /**
     * Returns a string identifier for the concrete task type.
     * Expected values are {@code "BUG"}, {@code "FEATURE"}, or {@code "DOCUMENTATION"}.
     *
     * @return the task type string
     */
    String getType();

    /**
     * Returns the timestamp when this task was created.
     *
     * @return the creation timestamp, never {@code null}
     */
    LocalDateTime getCreatedAt();
}
