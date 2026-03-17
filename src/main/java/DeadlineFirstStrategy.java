import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.time.LocalDate;

/**
 * Concrete Strategy that sorts tasks by deadline in ascending order (earliest first).
 *
 * <p>This strategy is designed for <strong>sprint planning and deadline-driven workflows</strong>
 * where time-sensitive tasks must be completed before their due dates. Tasks with the
 * earliest deadlines appear at the top of the list, enabling teams to plan their work
 * around approaching due dates and avoid missing commitments.</p>
 *
 * <p>Tasks with <strong>no deadline (null)</strong> are pushed to the end of the list,
 * since they have no time constraint and can be addressed after all time-bound work
 * is handled. This is a deliberate design choice: in sprint planning, unscheduled
 * tasks are lower priority than any task with a concrete due date.</p>
 *
 * <h2>Role in the Strategy Pattern</h2>
 * <p>This is a <strong>Concrete Strategy</strong>. It implements the {@link PriorityStrategy}
 * interface and provides deadline-based sorting. The TaskManager (Context) can inject
 * this strategy when the team enters a sprint planning phase or when working against
 * release milestones with firm deadlines.</p>
 *
 * <h2>SOLID Principles Demonstrated</h2>
 * <ul>
 *   <li><strong>Single Responsibility Principle (SRP):</strong> This class is solely
 *       responsible for deadline-based sorting logic. Changes to deadline handling
 *       (e.g., treating null deadlines differently) are the only reason this class
 *       would need modification.</li>
 *   <li><strong>Open/Closed Principle (OCP):</strong> This strategy can coexist with
 *       other strategies without any of them needing modification. The system is
 *       extended by adding new strategy classes, not by changing this one.</li>
 *   <li><strong>Liskov Substitution Principle (LSP):</strong> This class is fully
 *       substitutable for any {@link PriorityStrategy} reference, honoring the
 *       contract of returning a new sorted list without mutating the input.</li>
 *   <li><strong>Dependency Inversion Principle (DIP):</strong> Depends on the
 *       {@link Task} interface abstraction, not on any specific task implementation
 *       such as BugTask or FeatureTask.</li>
 * </ul>
 *
 * @see PriorityStrategy
 * @see UrgentFirstStrategy
 * @see SeverityFirstStrategy
 */
public class DeadlineFirstStrategy implements PriorityStrategy {

    /**
     * Sorts tasks by their deadline in ascending order (earliest deadline first).
     *
     * <p>Tasks with null deadlines are placed at the end of the sorted list using
     * {@link Comparator#nullsLast}, since tasks without a deadline are considered
     * less time-sensitive than those with explicit due dates.</p>
     *
     * <p><strong>Example ordering:</strong></p>
     * <pre>
     *   2026-03-18 (tomorrow)    -- appears first
     *   2026-03-25 (next week)
     *   2026-04-01 (two weeks)
     *   null (no deadline)       -- appears last
     *   null (no deadline)       -- appears last
     * </pre>
     *
     * @param tasks the list of tasks to sort; must not be null
     * @return a new list of tasks sorted by deadline ascending, with null deadlines last
     */
    @Override
    public List<Task> sort(List<Task> tasks) {
        // Create a new list to preserve the original input list's order
        List<Task> sorted = new ArrayList<>(tasks);

        // Build a comparator for LocalDate that handles null values gracefully.
        // Comparator.nullsLast() wraps the natural-order comparator so that:
        //   - Two non-null dates are compared normally (ascending: earlier dates first)
        //   - A null date is always considered "greater than" a non-null date
        //   - Two null dates are considered equal
        // This ensures tasks without deadlines sink to the bottom of the list.
        Comparator<LocalDate> dateComparator = Comparator.nullsLast(Comparator.naturalOrder());

        // Sort the list using the deadline field, delegating null-safety to the
        // dateComparator defined above. Each task's getDeadline() may return null,
        // which the nullsLast wrapper handles transparently.
        Collections.sort(sorted, new Comparator<Task>() {
            @Override
            public int compare(Task a, Task b) {
                // Extract deadlines (may be null) and delegate to the null-safe comparator
                return dateComparator.compare(a.getDeadline(), b.getDeadline());
            }
        });

        return sorted;
    }
}
