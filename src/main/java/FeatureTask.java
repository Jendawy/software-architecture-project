/**
 * Represents a feature request task in the Task Management System.
 *
 * <p>A feature task captures a new piece of functionality to be built,
 * along with an effort estimate (in hours) and a business value score
 * that helps product owners prioritize the backlog.</p>
 *
 * <h3>Design Pattern Role</h3>
 * <p>This is a <strong>Concrete Product</strong> in the <strong>Factory Method</strong>
 * pattern. A task factory can create {@code FeatureTask} instances and return them
 * through the {@link Task} interface, decoupling client code from this specific
 * implementation.</p>
 *
 * <h3>SOLID Principles Demonstrated</h3>
 * <ul>
 *   <li><strong>Single Responsibility Principle (SRP)</strong> -- This class is
 *       responsible only for feature-specific data (estimated effort, business value).
 *       All common task behaviour is inherited from {@link AbstractTask}.</li>
 *   <li><strong>Liskov Substitution Principle (LSP)</strong> -- A {@code FeatureTask}
 *       can be used anywhere a {@link Task} is expected without altering program
 *       correctness.</li>
 *   <li><strong>Open/Closed Principle (OCP)</strong> -- This class was added as a
 *       new concrete product without modifying {@link AbstractTask} or {@link Task}.</li>
 * </ul>
 *
 * @see Task
 * @see AbstractTask
 * @see BugTask
 * @see DocumentationTask
 */
public class FeatureTask extends AbstractTask {

    // -----------------------------------------------------------------------
    // Feature-specific fields
    // -----------------------------------------------------------------------

    /**
     * The estimated development effort in hours.
     * Used for sprint planning and capacity allocation.
     */
    private final int estimatedEffort;

    /**
     * A business value score from 1 (low value) to 10 (high value).
     * Combined with effort, this enables ROI-based prioritization
     * (value / effort ratio).
     */
    private final int businessValue;

    // -----------------------------------------------------------------------
    // Constructor
    // -----------------------------------------------------------------------

    /**
     * Creates a new feature task with the specified details.
     *
     * @param title           a short summary of the feature
     * @param description     a detailed description of the desired functionality
     * @param priority        priority from 1 (low) to 5 (high)
     * @param estimatedEffort estimated hours to implement this feature
     * @param businessValue   business value score from 1 (low) to 10 (high)
     * @throws IllegalArgumentException if businessValue is outside the 1-10 range
     */
    public FeatureTask(String title, String description, int priority,
                       int estimatedEffort, int businessValue) {
        super(title, description, priority);

        if (estimatedEffort < 0) {
            throw new IllegalArgumentException(
                    "Estimated effort must be non-negative, got: " + estimatedEffort);
        }
        if (businessValue < 1 || businessValue > 10) {
            throw new IllegalArgumentException(
                    "Business value must be between 1 and 10, got: " + businessValue);
        }

        this.estimatedEffort = estimatedEffort;
        this.businessValue = businessValue;
    }

    // -----------------------------------------------------------------------
    // Task interface -- type identifier
    // -----------------------------------------------------------------------

    /**
     * {@inheritDoc}
     *
     * @return {@code "FEATURE"} for all feature task instances
     */
    @Override
    public String getType() {
        return "FEATURE";
    }

    // -----------------------------------------------------------------------
    // Feature-specific accessors
    // -----------------------------------------------------------------------

    /**
     * Returns the estimated effort in hours to implement this feature.
     *
     * @return estimated hours of work
     */
    public int getEstimatedEffort() {
        return estimatedEffort;
    }

    /**
     * Returns the business value score for this feature.
     *
     * @return an integer from 1 (low) to 10 (high)
     */
    public int getBusinessValue() {
        return businessValue;
    }

    // -----------------------------------------------------------------------
    // toString -- extends the template from AbstractTask
    // -----------------------------------------------------------------------

    /**
     * Returns a string representation that includes both the common task
     * fields (via {@code super.toString()}) and feature-specific details.
     *
     * @return a formatted string with all feature task information
     */
    @Override
    public String toString() {
        // Build on the base representation and append feature-specific fields
        return super.toString()
                + String.format(" | FeatureDetails[estimatedEffort=%dh, businessValue=%d/10]",
                        estimatedEffort, businessValue);
    }
}
