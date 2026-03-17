import java.time.LocalDate;

/**
 * Concrete Creator for {@link BugTask} instances in the Factory Method pattern.
 *
 * <p>This class extends the abstract {@link TaskFactory} (the Creator) and provides a concrete
 * implementation of the factory method {@link #createTask(String, String, int)}. When invoked,
 * the factory method returns a new {@link BugTask} with sensible default values for
 * bug-specific fields: a severity of {@code "MEDIUM"} and an empty steps-to-reproduce string.</p>
 *
 * <h2>Role in the Factory Method Pattern</h2>
 * <p>This is a <strong>Concrete Creator</strong>. Its sole purpose is to decide <em>which</em>
 * concrete product ({@link BugTask}) to instantiate. By encapsulating the {@code new BugTask(...)}
 * call inside this factory, client code never needs to reference {@code BugTask} directly.
 * Instead, clients program against the {@link TaskFactory} abstraction and receive a {@link Task}
 * interface reference.</p>
 *
 * <p>This class also exposes a more specific method,
 * {@link #createBugTask(String, String, int, String, String)}, which gives callers full control
 * over every bug-specific parameter. This is a common extension in real-world factory
 * implementations: the pattern-mandated factory method provides convenience defaults, while
 * a richer method caters to advanced use cases.</p>
 *
 * <h2>SOLID Principles Demonstrated</h2>
 * <ul>
 *   <li><strong>Single Responsibility Principle (SRP):</strong> This class is responsible only
 *       for creating {@code BugTask} objects. It contains no business logic for features or
 *       documentation tasks.</li>
 *   <li><strong>Open/Closed Principle (OCP):</strong> Adding this factory required zero
 *       modifications to {@link TaskFactory} or any existing factory. The system was extended
 *       purely by addition.</li>
 *   <li><strong>Liskov Substitution Principle (LSP):</strong> An instance of
 *       {@code BugTaskFactory} can be used anywhere a {@code TaskFactory} is expected without
 *       altering program correctness.</li>
 * </ul>
 *
 * <h2>Default Values</h2>
 * <table>
 *   <tr><th>Parameter</th><th>Default</th><th>Rationale</th></tr>
 *   <tr><td>severity</td><td>{@code "MEDIUM"}</td><td>Assumes moderate impact until triaged</td></tr>
 *   <tr><td>stepsToReproduce</td><td>{@code ""}</td><td>Not always known at creation time</td></tr>
 * </table>
 *
 * <h2>Usage Example</h2>
 * <pre>{@code
 *     // Through the abstract factory interface (polymorphic)
 *     TaskFactory factory = new BugTaskFactory();
 *     Task bug = factory.createTask("Login crash", "App crashes on empty password", 1);
 *
 *     // Through the specific method (full control)
 *     BugTaskFactory bugFactory = new BugTaskFactory();
 *     BugTask detailed = bugFactory.createBugTask(
 *         "Login crash", "App crashes on empty password", 1,
 *         "CRITICAL", "1. Open app\n2. Leave password blank\n3. Click Login");
 * }</pre>
 *
 * @see TaskFactory
 * @see BugTask
 * @see Task
 */
public class BugTaskFactory extends TaskFactory {

    /**
     * Default severity assigned to bug tasks when created through the generic factory method.
     * "MEDIUM" is chosen as a safe middle-ground; the bug can be re-classified after triage.
     */
    private static final String DEFAULT_SEVERITY = "MEDIUM";

    /**
     * Default steps-to-reproduce string. An empty string indicates that reproduction steps
     * have not yet been documented.
     */
    private static final String DEFAULT_STEPS_TO_REPRODUCE = "";

    /**
     * Creates a new {@link BugTask} with default bug-specific parameters.
     *
     * <p>This is the Factory Method implementation required by the pattern. It satisfies the
     * contract defined in {@link TaskFactory#createTask(String, String, int)} by returning a
     * {@code BugTask} with a default severity of {@code "MEDIUM"} and empty reproduction steps.
     * Callers who need to specify these values should use
     * {@link #createBugTask(String, String, int, String, String)} instead.</p>
     *
     * @param title       a short, descriptive title for the bug; must not be {@code null}
     * @param description a detailed explanation of the bug's symptoms; must not be {@code null}
     * @param priority    an integer priority (1 = critical, 5 = low)
     * @return a new {@link BugTask} instance with default severity and empty steps-to-reproduce
     */
    @Override
    public Task createTask(String title, String description, int priority) {
        // Delegate to the BugTask constructor with sensible defaults for fields
        // that are bug-specific but not part of the generic Task creation contract.
        return new BugTask(title, description, priority, DEFAULT_SEVERITY, DEFAULT_STEPS_TO_REPRODUCE);
    }

    /**
     * Creates a fully specified {@link BugTask} with explicit severity and reproduction steps.
     *
     * <p>This method extends the factory's capabilities beyond the basic factory method contract.
     * It is intended for use cases where the caller already knows the severity classification and
     * has documented the steps needed to reproduce the bug. Unlike
     * {@link #createTask(String, String, int)}, this method returns the concrete {@code BugTask}
     * type so that callers can access bug-specific methods without casting.</p>
     *
     * <p>Note: This method returns {@code BugTask} rather than {@code Task} intentionally. When
     * a caller uses this method directly, they already know they want a bug task and benefit from
     * the richer type. This does not violate DIP because the caller has consciously chosen the
     * concrete factory.</p>
     *
     * @param title            a short, descriptive title for the bug; must not be {@code null}
     * @param description      a detailed explanation of the bug's symptoms; must not be {@code null}
     * @param priority         an integer priority (1 = critical, 5 = low)
     * @param severity         the severity classification (e.g., "LOW", "MEDIUM", "HIGH",
     *                         "CRITICAL"); must not be {@code null}
     * @param stepsToReproduce step-by-step instructions to reproduce the bug; may be empty but
     *                         must not be {@code null}
     * @return a new {@link BugTask} instance configured with all provided parameters
     */
    public BugTask createBugTask(String title, String description, int priority,
                                 String severity, String stepsToReproduce) {
        // Full-control creation: every parameter is explicitly provided by the caller,
        // so no defaults are applied.
        return new BugTask(title, description, priority, severity, stepsToReproduce);
    }
}
