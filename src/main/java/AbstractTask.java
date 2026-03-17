import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Provides a skeletal implementation of the {@link Task} interface, reducing
 * boilerplate in concrete task classes.
 *
 * <h3>Design Pattern Roles</h3>
 * <ul>
 *   <li><strong>Factory Method -- Abstract Product:</strong> Sits between the
 *       {@link Task} Product interface and the Concrete Products ({@link BugTask},
 *       {@link FeatureTask}, {@link DocumentationTask}). It consolidates shared
 *       state and behaviour so that each concrete product only needs to supply
 *       type-specific fields and implement {@link #getType()}.</li>
 *   <li><strong>Template Method (mini-pattern):</strong> The {@link #toString()}
 *       method acts as a template method. It builds a common string representation
 *       of shared fields, and subclasses extend it by appending their own
 *       type-specific details. The "hook" is simply calling {@code super.toString()}
 *       and concatenating additional information.</li>
 * </ul>
 *
 * <h3>SOLID Principles Demonstrated</h3>
 * <ul>
 *   <li><strong>Single Responsibility Principle (SRP)</strong> -- This class is
 *       responsible only for managing the common task data (id, title, description,
 *       status, priority, deadline, creation timestamp). It does not handle
 *       persistence, presentation, or business rules beyond basic state-transition
 *       validation.</li>
 *   <li><strong>Open/Closed Principle (OCP)</strong> -- New task types can be added
 *       by extending this class without modifying it. The abstract {@link #getType()}
 *       method is the only contract subclasses must fulfill.</li>
 *   <li><strong>Liskov Substitution Principle (LSP)</strong> -- All subclasses
 *       inherit and honor the base contract defined by {@link Task}, so they can
 *       be used interchangeably wherever a {@code Task} is expected.</li>
 * </ul>
 *
 * @see Task
 * @see BugTask
 * @see FeatureTask
 * @see DocumentationTask
 */
public abstract class AbstractTask implements Task {

    // -----------------------------------------------------------------------
    // Auto-increment ID generator
    // -----------------------------------------------------------------------

    /**
     * Shared counter for generating unique task IDs across all task types.
     * Each new task increments this counter and claims the next value.
     * Note: not thread-safe; in a concurrent environment a thread-safe
     * counter (e.g., AtomicInteger) would be required.
     */
    private static int idCounter = 0;

    // -----------------------------------------------------------------------
    // Instance fields
    // -----------------------------------------------------------------------

    /** Unique identifier assigned at construction time. */
    private final int id;

    /** Short, human-readable summary of the task. */
    private final String title;

    /** Detailed description of what the task involves. */
    private final String description;

    /** Current lifecycle state; defaults to {@link TaskStatus#OPEN}. */
    private TaskStatus status;

    /** Priority level from 1 (lowest) to 5 (highest). */
    private final int priority;

    /** Optional deadline; may be {@code null} if no deadline is set. */
    private LocalDate deadline;

    /** Timestamp captured automatically when the task is created. */
    private final LocalDateTime createdAt;

    // -----------------------------------------------------------------------
    // Constructor
    // -----------------------------------------------------------------------

    /**
     * Constructs a new task with the given core properties.
     *
     * <p>The {@code id} is auto-assigned from a shared counter, the
     * {@code status} defaults to {@link TaskStatus#OPEN}, and
     * {@code createdAt} is set to the current date-time.</p>
     *
     * @param title       a short summary of the task (must not be {@code null})
     * @param description a detailed description (must not be {@code null})
     * @param priority    priority from 1 (low) to 5 (high)
     * @throws IllegalArgumentException if priority is outside the 1-5 range
     */
    protected AbstractTask(String title, String description, int priority) {
        if (title == null || title.isBlank()) {
            throw new IllegalArgumentException("Title must not be null or blank.");
        }
        if (description == null) {
            throw new IllegalArgumentException("Description must not be null.");
        }
        if (priority < 1 || priority > 5) {
            throw new IllegalArgumentException(
                    "Priority must be between 1 and 5, got: " + priority);
        }

        this.id = ++idCounter;   // Auto-increment: first task gets ID 1
        this.title = title;
        this.description = description;
        this.status = TaskStatus.OPEN;
        this.priority = priority;
        this.deadline = null;    // No deadline by default
        this.createdAt = LocalDateTime.now();
    }

    // -----------------------------------------------------------------------
    // Task interface implementation
    // -----------------------------------------------------------------------

    /** {@inheritDoc} */
    @Override
    public int getId() {
        return id;
    }

    /** {@inheritDoc} */
    @Override
    public String getTitle() {
        return title;
    }

    /** {@inheritDoc} */
    @Override
    public String getDescription() {
        return description;
    }

    /** {@inheritDoc} */
    @Override
    public TaskStatus getStatus() {
        return status;
    }

    /**
     * {@inheritDoc}
     *
     * <p>This implementation validates the transition using
     * {@link TaskStatus#canTransitionTo(TaskStatus)} and throws an
     * {@link IllegalArgumentException} if the transition is not allowed
     * by the state machine rules.</p>
     */
    @Override
    public void setStatus(TaskStatus status) {
        // Guard: ensure the transition is valid before applying it
        if (!this.status.canTransitionTo(status)) {
            throw new IllegalArgumentException(
                    "Cannot transition from " + this.status + " to " + status);
        }
        this.status = status;
    }

    /** {@inheritDoc} */
    @Override
    public int getPriority() {
        return priority;
    }

    /** {@inheritDoc} */
    @Override
    public LocalDate getDeadline() {
        return deadline;
    }

    /** {@inheritDoc} */
    @Override
    public void setDeadline(LocalDate deadline) {
        this.deadline = deadline;
    }

    /** {@inheritDoc} */
    @Override
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    // -----------------------------------------------------------------------
    // toString -- serves as a "template method" for subclasses
    // -----------------------------------------------------------------------

    /**
     * Returns a formatted string with all common task fields.
     *
     * <p>Subclasses should call {@code super.toString()} and append their
     * own type-specific details, following the Template Method mini-pattern.</p>
     *
     * @return a multi-field string representation of this task
     */
    @Override
    public String toString() {
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");
        return String.format(
                "Task[id=%d, type=%s, title='%s', status=%s, priority=%d, deadline=%s, created=%s]",
                id,
                getType(),
                title,
                status,
                priority,
                deadline != null ? deadline.toString() : "none",
                createdAt.format(dtf)
        );
    }
}
