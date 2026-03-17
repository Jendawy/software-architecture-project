import java.time.LocalDate;

/**
 * Concrete Creator for {@link DocumentationTask} instances in the Factory Method pattern.
 *
 * <p>This class extends the abstract {@link TaskFactory} (the Creator) and provides a concrete
 * implementation of the factory method {@link #createTask(String, String, int)} that returns
 * {@link DocumentationTask} objects. When the generic factory method is used, the task is
 * configured with default documentation parameters: a document type of {@code "API"} and a
 * target audience of {@code "Developers"}.</p>
 *
 * <h2>Role in the Factory Method Pattern</h2>
 * <p>This is a <strong>Concrete Creator</strong>. Together with {@link BugTaskFactory} and
 * {@link FeatureTaskFactory}, it forms the family of concrete creators that the system supports.
 * Each concrete creator encapsulates the construction of a specific {@link Task} subtype,
 * keeping instantiation details hidden from client code that works through the
 * {@link TaskFactory} abstraction.</p>
 *
 * <p>The additional method {@link #createDocTask(String, String, int, String, String)} provides
 * full control over documentation-specific parameters. This two-tier API (generic factory method
 * plus specific creation method) is a recurring idiom in factory implementations, balancing
 * simplicity for common cases with flexibility for advanced ones.</p>
 *
 * <h2>SOLID Principles Demonstrated</h2>
 * <ul>
 *   <li><strong>Single Responsibility Principle (SRP):</strong> This factory is solely
 *       responsible for creating {@code DocumentationTask} instances. Changes to how
 *       documentation tasks are constructed affect only this class.</li>
 *   <li><strong>Open/Closed Principle (OCP):</strong> This class was introduced without
 *       modifying any existing factory or the abstract {@code TaskFactory}. The system
 *       accommodated a new task type purely through extension.</li>
 *   <li><strong>Liskov Substitution Principle (LSP):</strong> Any code expecting a
 *       {@code TaskFactory} can receive a {@code DocumentationTaskFactory} and function
 *       correctly. The {@code Task} objects it produces fully satisfy the {@code Task}
 *       interface contract.</li>
 *   <li><strong>Dependency Inversion Principle (DIP):</strong> Client code that receives
 *       this factory through a {@code TaskFactory} reference depends on the abstraction,
 *       not on this concrete class.</li>
 * </ul>
 *
 * <h2>Default Values</h2>
 * <table>
 *   <tr><th>Parameter</th><th>Default</th><th>Rationale</th></tr>
 *   <tr><td>documentType</td><td>{@code "API"}</td><td>API documentation is the most common
 *       type in software projects and a sensible starting default</td></tr>
 *   <tr><td>targetAudience</td><td>{@code "Developers"}</td><td>Most documentation in a task
 *       management system targets the development team</td></tr>
 * </table>
 *
 * <h2>Usage Example</h2>
 * <pre>{@code
 *     // Polymorphic usage: client only knows about TaskFactory
 *     TaskFactory factory = new DocumentationTaskFactory();
 *     Task doc = factory.createTask("REST API guide", "Document all endpoints", 2);
 *
 *     // With a deadline, using the inherited template method
 *     Task urgent = factory.createTaskWithDeadline(
 *         "REST API guide", "Document all endpoints", 2, LocalDate.of(2026, 4, 1));
 *
 *     // Direct usage with full parameter control
 *     DocumentationTaskFactory docFactory = new DocumentationTaskFactory();
 *     DocumentationTask userGuide = docFactory.createDocTask(
 *         "User Guide", "End-to-end usage instructions", 3,
 *         "USER_GUIDE", "End Users");
 * }</pre>
 *
 * @see TaskFactory
 * @see DocumentationTask
 * @see Task
 */
public class DocumentationTaskFactory extends TaskFactory {

    /**
     * Default document type applied when using the generic factory method.
     * "API" is chosen because API documentation is the most frequently created
     * documentation type in software development projects.
     */
    private static final String DEFAULT_DOCUMENT_TYPE = "API";

    /**
     * Default target audience applied when using the generic factory method.
     * "Developers" is the most common audience for technical documentation in
     * a task management context.
     */
    private static final String DEFAULT_TARGET_AUDIENCE = "Developers";

    /**
     * Creates a new {@link DocumentationTask} with default document type and target audience.
     *
     * <p>This is the Factory Method implementation required by the pattern. It satisfies the
     * contract defined in {@link TaskFactory#createTask(String, String, int)} by returning a
     * {@code DocumentationTask} with a default document type of {@code "API"} and a default
     * target audience of {@code "Developers"}. These defaults are appropriate for the most
     * common documentation scenario in software projects.</p>
     *
     * <p>For documentation tasks requiring different types (e.g., user guides, tutorials,
     * architecture documents) or targeting different audiences (e.g., end users, stakeholders),
     * use {@link #createDocTask(String, String, int, String, String)} instead.</p>
     *
     * @param title       a short, descriptive title for the documentation task; must not be
     *                    {@code null}
     * @param description a detailed explanation of what needs to be documented; must not be
     *                    {@code null}
     * @param priority    an integer priority (1 = critical, 5 = low)
     * @return a new {@link DocumentationTask} instance with default document type and audience,
     *         returned as a {@link Task} reference to maintain abstraction
     */
    @Override
    public Task createTask(String title, String description, int priority) {
        // Use default values for documentation-specific fields. These defaults
        // target the most common use case (API docs for developers) and can be
        // overridden by using the more specific createDocTask method.
        return new DocumentationTask(title, description, priority,
                DEFAULT_DOCUMENT_TYPE, DEFAULT_TARGET_AUDIENCE);
    }

    /**
     * Creates a fully specified {@link DocumentationTask} with explicit document type and
     * target audience.
     *
     * <p>This method provides complete control over all documentation-specific parameters,
     * making it suitable for creating diverse documentation tasks such as:</p>
     * <ul>
     *   <li>User guides targeting end users</li>
     *   <li>Architecture documents for the development team</li>
     *   <li>Onboarding tutorials for new team members</li>
     *   <li>Release notes for stakeholders</li>
     * </ul>
     *
     * <p>The return type is {@code DocumentationTask} rather than {@code Task}, allowing
     * callers to access documentation-specific methods directly. Callers who use this
     * method have consciously chosen to work with documentation tasks, so exposing the
     * concrete type is appropriate and avoids unnecessary downcasting.</p>
     *
     * @param title          a short, descriptive title for the documentation task; must not be
     *                       {@code null}
     * @param description    a detailed explanation of what needs to be documented; must not be
     *                       {@code null}
     * @param priority       an integer priority (1 = critical, 5 = low)
     * @param documentType   the category of document being created (e.g., "API", "USER_GUIDE",
     *                       "TUTORIAL", "ARCHITECTURE"); must not be {@code null}
     * @param targetAudience the intended readers of the document (e.g., "Developers",
     *                       "End Users", "Stakeholders"); must not be {@code null}
     * @return a new {@link DocumentationTask} instance configured with all provided parameters
     */
    public DocumentationTask createDocTask(String title, String description, int priority,
                                           String documentType, String targetAudience) {
        // All parameters are explicitly provided by the caller, giving full control
        // over the documentation task's configuration without relying on any defaults.
        return new DocumentationTask(title, description, priority, documentType, targetAudience);
    }
}
