import java.time.LocalDate;

/**
 * Concrete Creator for {@link FeatureTask} instances in the Factory Method pattern.
 *
 * <p>This class extends the abstract {@link TaskFactory} (the Creator) and overrides the
 * factory method {@link #createTask(String, String, int)} to produce {@link FeatureTask}
 * objects. When the generic factory method is used, sensible defaults are applied for
 * feature-specific parameters: an estimated effort of 8 hours and a business value score of 5.</p>
 *
 * <h2>Role in the Factory Method Pattern</h2>
 * <p>This is a <strong>Concrete Creator</strong>. It encapsulates the instantiation logic for
 * {@code FeatureTask} objects, ensuring that client code working with the {@link TaskFactory}
 * abstraction never needs to know about this class or the {@code FeatureTask} constructor
 * signature. The factory method returns a {@link Task} reference, preserving polymorphism.</p>
 *
 * <p>An additional method,
 * {@link #createFeatureTask(String, String, int, int, int)}, is provided for callers who need
 * explicit control over effort estimation and business value scoring. This is a pragmatic
 * extension beyond the core pattern, commonly seen in production codebases.</p>
 *
 * <h2>SOLID Principles Demonstrated</h2>
 * <ul>
 *   <li><strong>Single Responsibility Principle (SRP):</strong> This class has exactly one
 *       reason to change: if the way feature tasks are constructed changes. It knows nothing
 *       about bugs or documentation tasks.</li>
 *   <li><strong>Open/Closed Principle (OCP):</strong> This factory was added to the system
 *       without modifying {@link TaskFactory}, {@link BugTaskFactory}, or any other existing
 *       class. The architecture is open for extension via new subclasses.</li>
 *   <li><strong>Liskov Substitution Principle (LSP):</strong> This factory can replace any
 *       {@code TaskFactory} reference. The returned {@code Task} objects satisfy the full
 *       {@code Task} interface contract, so clients behave correctly regardless of which
 *       concrete factory is in use.</li>
 * </ul>
 *
 * <h2>Default Values</h2>
 * <table>
 *   <tr><th>Parameter</th><th>Default</th><th>Rationale</th></tr>
 *   <tr><td>estimatedEffort</td><td>8 (hours)</td><td>Represents a standard one-day task, a
 *       common baseline in agile estimation</td></tr>
 *   <tr><td>businessValue</td><td>5</td><td>Mid-range on a 1-10 scale, indicating moderate
 *       value until properly scored during backlog refinement</td></tr>
 * </table>
 *
 * <h2>Usage Example</h2>
 * <pre>{@code
 *     // Polymorphic usage through the abstract factory
 *     TaskFactory factory = new FeatureTaskFactory();
 *     Task feature = factory.createTask("Dark mode", "Add dark theme support", 3);
 *
 *     // Direct usage with full parameter control
 *     FeatureTaskFactory featureFactory = new FeatureTaskFactory();
 *     FeatureTask detailed = featureFactory.createFeatureTask(
 *         "Dark mode", "Add dark theme support", 3, 40, 8);
 * }</pre>
 *
 * @see TaskFactory
 * @see FeatureTask
 * @see Task
 */
public class FeatureTaskFactory extends TaskFactory {

    /**
     * Default estimated effort in hours for a feature task. A value of 8 represents one
     * standard working day, which serves as a reasonable initial estimate before sprint
     * planning refines it.
     */
    private static final int DEFAULT_ESTIMATED_EFFORT = 8;

    /**
     * Default business value on a 1-10 scale. A mid-range value of 5 is assigned so that
     * the feature is neither deprioritized nor over-prioritized before the product owner
     * scores it during backlog refinement.
     */
    private static final int DEFAULT_BUSINESS_VALUE = 5;

    /**
     * Creates a new {@link FeatureTask} with default effort and business value parameters.
     *
     * <p>This is the Factory Method implementation required by the pattern. It fulfills the
     * contract from {@link TaskFactory#createTask(String, String, int)} by instantiating a
     * {@code FeatureTask} with a default estimated effort of {@value #DEFAULT_ESTIMATED_EFFORT}
     * hours and a default business value of {@value #DEFAULT_BUSINESS_VALUE}. These defaults
     * provide a reasonable starting point that can be adjusted later.</p>
     *
     * @param title       a short, descriptive title for the feature; must not be {@code null}
     * @param description a detailed explanation of the feature's requirements; must not be
     *                    {@code null}
     * @param priority    an integer priority (1 = critical, 5 = low)
     * @return a new {@link FeatureTask} instance with default effort and business value,
     *         returned as a {@link Task} reference to maintain abstraction
     */
    @Override
    public Task createTask(String title, String description, int priority) {
        // Apply default values for feature-specific fields that are not part of the
        // generic Task creation contract. This keeps the factory method signature simple
        // while still producing a fully initialized FeatureTask.
        return new FeatureTask(title, description, priority,
                DEFAULT_ESTIMATED_EFFORT, DEFAULT_BUSINESS_VALUE);
    }

    /**
     * Creates a fully specified {@link FeatureTask} with explicit effort and business value.
     *
     * <p>This method complements the generic factory method by accepting all feature-specific
     * parameters directly. It is useful when the product owner has already estimated the
     * business value and the development team has sized the effort during sprint planning.</p>
     *
     * <p>The return type is {@code FeatureTask} rather than {@code Task}, giving callers
     * access to feature-specific methods (e.g., retrieving effort or business value) without
     * requiring a downcast. This is acceptable because callers using this method have already
     * committed to working with feature tasks specifically.</p>
     *
     * @param title           a short, descriptive title for the feature; must not be {@code null}
     * @param description     a detailed explanation of the feature's requirements; must not be
     *                        {@code null}
     * @param priority        an integer priority (1 = critical, 5 = low)
     * @param estimatedEffort the estimated development effort in hours; must be positive
     * @param businessValue   the business value score (typically 1-10); must be positive
     * @return a new {@link FeatureTask} instance configured with all provided parameters
     */
    public FeatureTask createFeatureTask(String title, String description, int priority,
                                         int estimatedEffort, int businessValue) {
        // All parameters are caller-supplied, so no defaults are needed.
        // This gives the caller complete control over the feature task configuration.
        return new FeatureTask(title, description, priority, estimatedEffort, businessValue);
    }
}
