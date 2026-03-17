/**
 * Represents a documentation task in the Task Management System.
 *
 * <p>A documentation task tracks the creation or update of written material
 * such as API references, user guides, or tutorials. It records the type
 * of document and the intended audience so writers can tailor the content
 * appropriately.</p>
 *
 * <h3>Design Pattern Role</h3>
 * <p>This is a <strong>Concrete Product</strong> in the <strong>Factory Method</strong>
 * pattern. A task factory can instantiate {@code DocumentationTask} objects and
 * return them through the {@link Task} interface, allowing client code to handle
 * all task types uniformly.</p>
 *
 * <h3>SOLID Principles Demonstrated</h3>
 * <ul>
 *   <li><strong>Single Responsibility Principle (SRP)</strong> -- This class manages
 *       only documentation-specific data (document type, target audience). Shared
 *       task behaviour lives in {@link AbstractTask}.</li>
 *   <li><strong>Liskov Substitution Principle (LSP)</strong> -- A {@code DocumentationTask}
 *       can substitute for any {@link Task} reference without breaking expectations.</li>
 *   <li><strong>Open/Closed Principle (OCP)</strong> -- This concrete product was
 *       introduced without any modifications to {@link AbstractTask} or {@link Task}.</li>
 * </ul>
 *
 * @see Task
 * @see AbstractTask
 * @see BugTask
 * @see FeatureTask
 */
public class DocumentationTask extends AbstractTask {

    // -----------------------------------------------------------------------
    // Documentation-specific fields
    // -----------------------------------------------------------------------

    /**
     * The category of document to be produced.
     * Expected values: API, USER_GUIDE, or TUTORIAL.
     * This helps assign the task to a writer with the right expertise.
     */
    private final String documentType;

    /**
     * A description of who the document is intended for
     * (e.g., "backend developers", "end users", "new hires").
     * Knowing the audience shapes the writing style and level of detail.
     */
    private final String targetAudience;

    // -----------------------------------------------------------------------
    // Constructor
    // -----------------------------------------------------------------------

    /**
     * Creates a new documentation task with the specified details.
     *
     * @param title          a short summary of the documentation work
     * @param description    a detailed description of what needs to be documented
     * @param priority       priority from 1 (low) to 5 (high)
     * @param documentType   the type of document: API, USER_GUIDE, or TUTORIAL
     * @param targetAudience a description of the intended readership
     */
    public DocumentationTask(String title, String description, int priority,
                             String documentType, String targetAudience) {
        super(title, description, priority);
        this.documentType = documentType;
        this.targetAudience = targetAudience;
    }

    // -----------------------------------------------------------------------
    // Task interface -- type identifier
    // -----------------------------------------------------------------------

    /**
     * {@inheritDoc}
     *
     * @return {@code "DOCUMENTATION"} for all documentation task instances
     */
    @Override
    public String getType() {
        return "DOCUMENTATION";
    }

    // -----------------------------------------------------------------------
    // Documentation-specific accessors
    // -----------------------------------------------------------------------

    /**
     * Returns the type of document to be produced.
     *
     * @return the document type string (e.g., API, USER_GUIDE, TUTORIAL)
     */
    public String getDocumentType() {
        return documentType;
    }

    /**
     * Returns a description of the intended audience for this document.
     *
     * @return the target audience description
     */
    public String getTargetAudience() {
        return targetAudience;
    }

    // -----------------------------------------------------------------------
    // toString -- extends the template from AbstractTask
    // -----------------------------------------------------------------------

    /**
     * Returns a string representation that includes both the common task
     * fields (via {@code super.toString()}) and documentation-specific details.
     *
     * @return a formatted string with all documentation task information
     */
    @Override
    public String toString() {
        // Build on the base representation and append documentation-specific fields
        return super.toString()
                + String.format(" | DocDetails[documentType=%s, targetAudience='%s']",
                        documentType, targetAudience);
    }
}
