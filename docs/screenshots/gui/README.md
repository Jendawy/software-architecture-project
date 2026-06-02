# GUI Screenshots — SEN3006 Task Manager

Screenshots of the Swing GUI (`TaskManagerGUI`, the third entry point alongside
`Main` and `TaskManagementApp`), captured from the live running window. Every
shot is the real app driven through the state named in the filename — no mockups.

| File | What it shows |
| --- | --- |
| `01-launch-empty.png` | Fresh launch: Create-Task form, empty task table, disabled action buttons, status bar. |
| `02-strategy-demo-urgent-first.png` | Strategy demo loaded (5 tasks), default **Urgent First** ordering. |
| `03-strategy-demo-deadline-first.png` | Same tasks re-sorted by **Deadline First** — Strategy pattern swapping the order live. |
| `04-strategy-demo-severity-first.png` | Same tasks re-sorted by **Severity First**. |
| `05-lifecycle-demo.png` | Lifecycle demo: a single OPEN task, ready for status transitions. |
| `06-integration-demo.png` | Integration demo: mixed task types with colour-coded statuses (IN_PROGRESS, REVIEW). |
| `07-task-selected-actions.png` | A task selected — the **Selected Task Actions** buttons enable per the legal transitions. |
| `08-filter-in-progress.png` | View-side filter narrowing the table to **IN_PROGRESS** rows. |
| `09-create-task-form-filled.png` | The Create-Task form filled in (Factory Method input: type → factory). |
| `10-demo-menu-open.png` | The **Demo** menu open, showing the three Main.java-mirrored scenarios + Clear All. |
| `11-about-dialog.png` | The Help → About dialog (patterns + engine summary). |

## How they were produced

Captured by launching the real `TaskManagerGUI` and driving its live components
(load demos, switch the Sort strategy, select a row, open menus/dialogs), then
screen-capturing the window with `java.awt.Robot`. Run with:

```bash
javac -d bin src/main/java/*.java src/main/java/gui/*.java
java -jar TaskManagerGUI.jar   # to launch the GUI interactively
```
