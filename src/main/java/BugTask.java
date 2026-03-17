/**
 * Represents a bug report task in the Task Management System.
 *
 * <p>A bug task captures a software defect along with its severity and
 * reproduction steps, enabling developers and testers to triage, reproduce,
 * and resolve issues systematically.</p>
 *
 * <h3>Design Pattern Role</h3>
 * <p>This is a <strong>Concrete Product</strong> in the <strong>Factory Method</strong>
 * pattern. A task factory can instantiate {@code BugTask} objects and return
 * them through the {@link Task} interface, so client code works with tasks
 * polymorphically without coupling to this concrete class.</p>
 *
 * <h3>SOLID Principles Demonstrated</h3>
 * <ul>
 *   <li><strong>Single Responsibility Principle (SRP)</strong> -- This class is
 *       solely responsible for bug-specific data (severity, steps to reproduce).
 *       Common task behaviour is inherited from {@link AbstractTask}.</li>
 *   <li><strong>Liskov Substitution Principle (LSP)</strong> -- A {@code BugTask}
 *       can replace any {@link Task} reference without breaking the program,
 *       because it fully honors the {@link Task} contract.</li>
 *   <li><strong>Open/Closed Principle (OCP)</strong> -- Adding this bug-specific
 *       subclass required no changes to {@link AbstractTask} or {@link Task}.</li>
 * </ul>
 *
 * @see Task
 * @see AbstractTask
 * @see FeatureTask
 * @see DocumentationTask
 */
public class BugTask extends AbstractTask {

    // -----------------------------------------------------------------------
    // Bug-specific fields
    // -----------------------------------------------------------------------

    /**
     * The severity of the bug. Expected values: LOW, MEDIUM, HIGH, CRITICAL.
     * Severity helps the team prioritize which bugs to fix first.
     */
    private String severity;

    /**
     * A textual description of the steps required to reproduce the bug.
     * Clear reproduction steps are essential for efficient debugging.
     */
    private final String stepsToReproduce;

    // -----------------------------------------------------------------------
    // Constructor
    // -----------------------------------------------------------------------

    /**
     * Creates a new bug task with the specified details.
     *
     * @param title            a short summary of the bug
     * @param description      a detailed description of the defect
     * @param priority         priority from 1 (low) to 5 (high)
     * @param severity         severity level: LOW, MEDIUM, HIGH, or CRITICAL
     * @param stepsToReproduce step-by-step instructions to reproduce the bug
     */
    public BugTask(String title, String description, int priority,
                   String severity, String stepsToReproduce) {
        super(title, description, priority);
        this.severity = severity;
        this.stepsToReproduce = stepsToReproduce;
    }

    // -----------------------------------------------------------------------
    // Task interface -- type identifier
    // -----------------------------------------------------------------------

    /**
     * {@inheritDoc}
     *
     * @return {@code "BUG"} for all bug task instances
     */
    @Override
    public String getType() {
        return "BUG";
    }

    // -----------------------------------------------------------------------
    // Bug-specific accessors
    // -----------------------------------------------------------------------

    /**
     * Returns the severity of this bug.
     *
     * @return the severity string (e.g., LOW, MEDIUM, HIGH, CRITICAL)
     */
    public String getSeverity() {
        return severity;
    }

    /**
     * Updates the severity of this bug.
     * This is useful when triage reveals the bug is more or less severe
     * than initially reported.
     *
     * @param severity the new severity level
     */
    public void setSeverity(String severity) {
        this.severity = severity;
    }

    /**
     * Returns the steps to reproduce this bug.
     *
     * @return a textual description of reproduction steps
     */
    public String getStepsToReproduce() {
        return stepsToReproduce;
    }

    // -----------------------------------------------------------------------
    // toString -- extends the template from AbstractTask
    // -----------------------------------------------------------------------

    /**
     * Returns a string representation that includes both the common task
     * fields (via {@code super.toString()}) and bug-specific details.
     *
     * @return a formatted string with all bug task information
     */
    @Override
    public String toString() {
        // Build on the base representation and append bug-specific fields
        return super.toString()
                + String.format(" | BugDetails[severity=%s, stepsToReproduce='%s']",
                        severity, stepsToReproduce);
    }
}
