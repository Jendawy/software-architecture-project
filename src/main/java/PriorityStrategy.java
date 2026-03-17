import java.util.List;

/**
 * Strategy interface for the Strategy design pattern applied to task prioritization.
 *
 * <p>This interface defines a family of prioritization algorithms that can be used
 * interchangeably by the TaskManager (the Context in Strategy pattern terminology).
 * Each concrete implementation encapsulates a different sorting algorithm, allowing
 * the system to switch between prioritization approaches at runtime without altering
 * the TaskManager's code.</p>
 *
 * <h2>Role in the Strategy Pattern</h2>
 * <p>This is the <strong>Strategy</strong> (abstract strategy) role. It declares the
 * common interface that all concrete strategies must implement. The TaskManager holds
 * a reference to this interface and delegates sorting to whichever concrete strategy
 * has been injected, decoupling the algorithm selection from the algorithm usage.</p>
 *
 * <h2>SOLID Principles Demonstrated</h2>
 * <ul>
 *   <li><strong>Interface Segregation Principle (ISP):</strong> This interface contains
 *       a single method, {@code sort}, providing a minimal and focused contract. Clients
 *       are not forced to depend on methods they do not use.</li>
 *   <li><strong>Open/Closed Principle (OCP):</strong> New prioritization strategies can
 *       be added by creating new implementations of this interface, without modifying
 *       the TaskManager or any existing strategy classes.</li>
 *   <li><strong>Dependency Inversion Principle (DIP):</strong> The TaskManager (a
 *       high-level module) depends on this abstraction rather than on concrete sorting
 *       implementations. Concrete strategies (low-level modules) also depend on this
 *       abstraction, inverting the traditional dependency direction.</li>
 *   <li><strong>Single Responsibility Principle (SRP):</strong> Each concrete strategy
 *       is solely responsible for one prioritization algorithm, and this interface is
 *       solely responsible for defining the sorting contract.</li>
 * </ul>
 *
 * @see UrgentFirstStrategy
 * @see DeadlineFirstStrategy
 * @see SeverityFirstStrategy
 */
public interface PriorityStrategy {

    /**
     * Sorts a list of tasks according to this strategy's prioritization algorithm.
     *
     * <p>Implementations <strong>must return a new sorted list</strong> and must
     * <strong>not modify</strong> the original input list. This preserves immutability
     * of the caller's data and avoids unexpected side effects.</p>
     *
     * @param tasks the list of tasks to be sorted; must not be null
     * @return a new {@link List} containing the same tasks, ordered according to
     *         this strategy's prioritization rules
     */
    List<Task> sort(List<Task> tasks);
}
