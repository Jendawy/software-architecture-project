import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * Concrete Strategy that sorts tasks by priority in descending order (highest first).
 *
 * <p>This strategy is designed for <strong>crisis and production-issue scenarios</strong>
 * where the most critical tasks must be addressed immediately. Tasks with a priority
 * of 5 (highest) appear at the top of the list, while tasks with a priority of 1
 * (lowest) appear at the bottom. This ensures that teams working under pressure can
 * instantly identify and focus on the most urgent work items.</p>
 *
 * <h2>Role in the Strategy Pattern</h2>
 * <p>This is a <strong>Concrete Strategy</strong>. It implements the {@link PriorityStrategy}
 * interface and provides one specific prioritization algorithm: sorting by the numeric
 * priority field in descending order. The TaskManager (Context) can swap this strategy
 * in at runtime whenever urgent-first ordering is needed, such as during incident
 * response or critical release periods.</p>
 *
 * <h2>SOLID Principles Demonstrated</h2>
 * <ul>
 *   <li><strong>Single Responsibility Principle (SRP):</strong> This class has exactly
 *       one reason to change -- if the rules for urgent-first sorting need to be
 *       modified. It does not handle deadline logic, severity logic, or task management.</li>
 *   <li><strong>Open/Closed Principle (OCP):</strong> This class is closed for
 *       modification but the overall system is open for extension. Adding a new
 *       strategy does not require changes here.</li>
 *   <li><strong>Liskov Substitution Principle (LSP):</strong> This class can be
 *       substituted anywhere a {@link PriorityStrategy} is expected without breaking
 *       the program's correctness.</li>
 *   <li><strong>Dependency Inversion Principle (DIP):</strong> This class depends on
 *       the {@link Task} abstraction (interface), not on concrete task implementations.</li>
 * </ul>
 *
 * @see PriorityStrategy
 * @see DeadlineFirstStrategy
 * @see SeverityFirstStrategy
 */
public class UrgentFirstStrategy implements PriorityStrategy {

    /**
     * Sorts tasks by their priority value in descending order (5 to 1).
     *
     * <p>A new list is created from the input to avoid mutating the original
     * collection. The sorting uses {@link Collections#sort} with a custom
     * {@link Comparator} that compares priority values in reverse natural order.</p>
     *
     * <p><strong>Example ordering:</strong></p>
     * <pre>
     *   Priority 5 (Critical)  -- appears first
     *   Priority 4 (High)
     *   Priority 3 (Medium)
     *   Priority 2 (Low)
     *   Priority 1 (Minimal)   -- appears last
     * </pre>
     *
     * @param tasks the list of tasks to sort; must not be null
     * @return a new list of tasks sorted by priority descending (highest priority first)
     */
    @Override
    public List<Task> sort(List<Task> tasks) {
        // Create a new list to avoid modifying the original input list
        List<Task> sorted = new ArrayList<>(tasks);

        // Sort by priority DESCENDING: compare b's priority to a's priority
        // so that higher numeric values (e.g., 5) come before lower ones (e.g., 1).
        // Integer.compare(b, a) returns positive when b > a, which places b before a,
        // effectively reversing the natural ascending order.
        Collections.sort(sorted, new Comparator<Task>() {
            @Override
            public int compare(Task a, Task b) {
                // Descending order: subtract a's priority from b's priority
                // If b has higher priority, result is positive, so b sorts first
                return Integer.compare(b.getPriority(), a.getPriority());
            }
        });

        return sorted;
    }
}
