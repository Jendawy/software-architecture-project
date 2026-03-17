import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * Concrete Strategy that sorts tasks using a two-tier approach: bug severity first,
 * then general priority for non-bug tasks.
 *
 * <p>This strategy is designed for <strong>risk-based prioritization</strong>, commonly
 * used during QA phases, maintenance windows, and post-release stabilization periods.
 * The core idea is that bugs -- especially severe ones -- represent active risk to the
 * system and must be addressed before feature work or documentation tasks.</p>
 *
 * <h2>Two-Tier Sorting Logic</h2>
 * <ol>
 *   <li><strong>Tier 1 -- Bug Tasks:</strong> All tasks that are instances of
 *       {@link BugTask} are placed at the top of the list, sorted by severity rank
 *       in descending order (CRITICAL first, then HIGH, MEDIUM, LOW).</li>
 *   <li><strong>Tier 2 -- Non-Bug Tasks:</strong> All remaining tasks (features,
 *       documentation, etc.) are placed after bugs, sorted by their numeric priority
 *       in descending order (5 first, 1 last).</li>
 * </ol>
 *
 * <p>This guarantees that even a LOW-severity bug appears before a priority-5 feature
 * task, reflecting the principle that known defects should be triaged before new work
 * is started.</p>
 *
 * <h2>Role in the Strategy Pattern</h2>
 * <p>This is a <strong>Concrete Strategy</strong>. It implements the {@link PriorityStrategy}
 * interface with the most specialized sorting algorithm of the three strategies. The
 * TaskManager (Context) can inject this strategy when the team transitions into a
 * bug-fixing or stabilization phase, such as before a major release or during
 * incident post-mortem follow-ups.</p>
 *
 * <h2>SOLID Principles Demonstrated</h2>
 * <ul>
 *   <li><strong>Single Responsibility Principle (SRP):</strong> This class is solely
 *       responsible for risk-based, severity-aware sorting. It encapsulates the
 *       knowledge of severity rankings and the two-tier ordering rule.</li>
 *   <li><strong>Open/Closed Principle (OCP):</strong> If new severity levels are
 *       introduced, only the {@code getSeverityRank} helper needs updating. Other
 *       strategies and the TaskManager remain untouched.</li>
 *   <li><strong>Liskov Substitution Principle (LSP):</strong> This class honors the
 *       {@link PriorityStrategy} contract -- it returns a new sorted list and does
 *       not modify the input. It can replace any other strategy without side effects.</li>
 *   <li><strong>Dependency Inversion Principle (DIP):</strong> While this strategy
 *       uses {@code instanceof BugTask} to detect bugs (a minor coupling), it still
 *       operates through the {@link Task} interface for all non-bug operations,
 *       keeping the overall dependency on abstractions.</li>
 * </ul>
 *
 * @see PriorityStrategy
 * @see UrgentFirstStrategy
 * @see DeadlineFirstStrategy
 * @see BugTask
 */
public class SeverityFirstStrategy implements PriorityStrategy {

    /**
     * Sorts tasks using a two-tier approach: bugs by severity first, then non-bugs
     * by priority.
     *
     * <p>The sorting algorithm works as follows:</p>
     * <ol>
     *   <li>If both tasks are BugTasks, compare by severity rank (CRITICAL &gt; HIGH
     *       &gt; MEDIUM &gt; LOW).</li>
     *   <li>If only one task is a BugTask, it always comes first.</li>
     *   <li>If neither task is a BugTask, compare by priority descending.</li>
     * </ol>
     *
     * <p><strong>Example ordering:</strong></p>
     * <pre>
     *   BugTask (CRITICAL)       -- tier 1, severity rank 4
     *   BugTask (HIGH)           -- tier 1, severity rank 3
     *   BugTask (MEDIUM)         -- tier 1, severity rank 2
     *   BugTask (LOW)            -- tier 1, severity rank 1
     *   FeatureTask (priority 5) -- tier 2, sorted by priority
     *   DocTask (priority 3)     -- tier 2, sorted by priority
     * </pre>
     *
     * @param tasks the list of tasks to sort; must not be null
     * @return a new list with bugs sorted by severity first, then non-bugs by priority
     */
    @Override
    public List<Task> sort(List<Task> tasks) {
        // Create a new list to avoid modifying the original input
        List<Task> sorted = new ArrayList<>(tasks);

        Collections.sort(sorted, new Comparator<Task>() {
            @Override
            public int compare(Task a, Task b) {
                // --- Step 1: Determine whether each task is a BugTask ---
                boolean aIsBug = a instanceof BugTask;
                boolean bIsBug = b instanceof BugTask;

                // --- Step 2: Handle the case where BOTH tasks are BugTasks ---
                // When both are bugs, sort by severity rank in DESCENDING order
                // so that CRITICAL (rank 4) comes before LOW (rank 1).
                if (aIsBug && bIsBug) {
                    // Cast to BugTask to access getSeverity()
                    BugTask bugA = (BugTask) a;
                    BugTask bugB = (BugTask) b;

                    // Convert severity strings to numeric ranks for comparison
                    int rankA = getSeverityRank(bugA.getSeverity());
                    int rankB = getSeverityRank(bugB.getSeverity());

                    // Descending: higher rank (CRITICAL=4) should come first
                    // So we compare rankB to rankA (reversed order)
                    return Integer.compare(rankB, rankA);
                }

                // --- Step 3: Handle the case where only ONE task is a BugTask ---
                // Bugs always take precedence over non-bugs in this strategy.
                // If 'a' is a bug but 'b' is not, 'a' should come first (return -1).
                // If 'b' is a bug but 'a' is not, 'b' should come first (return +1).
                if (aIsBug) {
                    // 'a' is a bug, 'b' is not -- 'a' comes first
                    return -1;
                }
                if (bIsBug) {
                    // 'b' is a bug, 'a' is not -- 'b' comes first
                    return 1;
                }

                // --- Step 4: Handle the case where NEITHER task is a BugTask ---
                // For non-bug tasks, fall back to priority-based sorting in
                // DESCENDING order (priority 5 before priority 1), which mirrors
                // the UrgentFirstStrategy behavior for the non-bug tier.
                return Integer.compare(b.getPriority(), a.getPriority());
            }
        });

        return sorted;
    }

    /**
     * Converts a severity string to a numeric rank for comparison purposes.
     *
     * <p>The ranking scale is:</p>
     * <ul>
     *   <li>{@code CRITICAL} = 4 (most severe, sorted first)</li>
     *   <li>{@code HIGH}     = 3</li>
     *   <li>{@code MEDIUM}   = 2</li>
     *   <li>{@code LOW}      = 1 (least severe among bugs)</li>
     * </ul>
     *
     * <p>If an unrecognized severity string is provided, it defaults to rank 0,
     * which places it after all known severity levels. This defensive approach
     * prevents unexpected exceptions from corrupting the sort order.</p>
     *
     * @param severity the severity string (e.g., "CRITICAL", "HIGH", "MEDIUM", "LOW")
     * @return an integer rank where higher values indicate greater severity
     */
    private int getSeverityRank(String severity) {
        // Map each known severity level to a numeric rank.
        // Higher ranks represent more severe bugs that should appear first.
        switch (severity) {
            case "CRITICAL":
                return 4;  // Highest severity -- system down or data loss
            case "HIGH":
                return 3;  // Major functionality broken
            case "MEDIUM":
                return 2;  // Moderate impact, workaround may exist
            case "LOW":
                return 1;  // Minor issue, cosmetic or edge case
            default:
                return 0;  // Unknown severity, treat as lowest rank
        }
    }
}
