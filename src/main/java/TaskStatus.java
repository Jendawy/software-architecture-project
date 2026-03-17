import java.util.EnumSet;
import java.util.Set;

/**
 * Represents the lifecycle states of a task in the Task Management System.
 *
 * <p>This enum models a <strong>finite state machine</strong> where each state defines
 * a set of valid transitions. The state machine enforces the following workflow:</p>
 *
 * <pre>
 *   OPEN ---------> IN_PROGRESS ---------> REVIEW ---------> DONE (terminal)
 *     |                 |                     |
 *     v                 v                     v
 *   BLOCKED <-------- BLOCKED            IN_PROGRESS
 *     |
 *     v
 *    OPEN
 * </pre>
 *
 * <h3>Design Pattern Role</h3>
 * <p>Acts as the <strong>State</strong> component in a lightweight State pattern.
 * Rather than creating separate state classes, the enum encapsulates transition
 * rules directly, keeping the design simple while still enforcing valid workflows.</p>
 *
 * <h3>SOLID Principles Demonstrated</h3>
 * <ul>
 *   <li><strong>Single Responsibility (SRP)</strong> -- This enum is solely responsible
 *       for defining task states and their valid transitions. It does not handle
 *       task data, persistence, or business logic beyond state transitions.</li>
 *   <li><strong>Open/Closed Principle (OCP)</strong> -- New states can be added to the
 *       enum with their own transition rules without modifying the transition logic
 *       of existing states, since each state declares its own allowed targets.</li>
 * </ul>
 *
 * @see Task
 * @see AbstractTask
 */
public enum TaskStatus {

    /**
     * The task has been created but work has not yet started.
     * Can transition to IN_PROGRESS (work begins) or BLOCKED (impediment found).
     */
    OPEN {
        @Override
        protected Set<TaskStatus> allowedTransitions() {
            return EnumSet.of(IN_PROGRESS, BLOCKED);
        }
    },

    /**
     * The task is actively being worked on.
     * Can transition to REVIEW (work complete, awaiting review) or BLOCKED (impediment found).
     */
    IN_PROGRESS {
        @Override
        protected Set<TaskStatus> allowedTransitions() {
            return EnumSet.of(REVIEW, BLOCKED);
        }
    },

    /**
     * The task work is complete and is under review.
     * Can transition to DONE (approved) or back to IN_PROGRESS (changes requested).
     */
    REVIEW {
        @Override
        protected Set<TaskStatus> allowedTransitions() {
            return EnumSet.of(DONE, IN_PROGRESS);
        }
    },

    /**
     * The task is fully complete. This is a <strong>terminal state</strong> with
     * no outgoing transitions.
     */
    DONE {
        @Override
        protected Set<TaskStatus> allowedTransitions() {
            // Terminal state -- no further transitions are permitted.
            return EnumSet.noneOf(TaskStatus.class);
        }
    },

    /**
     * The task is blocked by an external impediment.
     * Can only transition back to OPEN once the impediment is resolved.
     */
    BLOCKED {
        @Override
        protected Set<TaskStatus> allowedTransitions() {
            return EnumSet.of(OPEN);
        }
    };

    // -----------------------------------------------------------------------
    // Transition logic
    // -----------------------------------------------------------------------

    /**
     * Returns the set of states that this state is allowed to transition to.
     * Each enum constant overrides this method to declare its own rules.
     *
     * @return an unmodifiable {@link EnumSet} of valid target states
     */
    protected abstract Set<TaskStatus> allowedTransitions();

    /**
     * Checks whether a transition from this state to the given {@code next} state
     * is permitted by the workflow rules.
     *
     * <p>Example usage:</p>
     * <pre>
     *   if (currentStatus.canTransitionTo(TaskStatus.IN_PROGRESS)) {
     *       task.setStatus(TaskStatus.IN_PROGRESS);
     *   }
     * </pre>
     *
     * @param next the target state to transition to
     * @return {@code true} if the transition is valid, {@code false} otherwise
     */
    public boolean canTransitionTo(TaskStatus next) {
        // Delegate to the per-constant set of allowed transitions.
        return allowedTransitions().contains(next);
    }
}
