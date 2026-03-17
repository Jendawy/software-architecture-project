# Submission Guide

## What to Submit

Per the assignment guide (Section 5.1), you must submit:

1. **Report** — PDF format
2. **Java source code** — Single ZIP file

## Step-by-Step Submission Instructions

### Step 1: Convert Report to PDF

The report is at: `docs/report/SEN3006_Task_Management_System_Report.md`

**Option A — GitHub (easiest):**
1. Open the report on GitHub (all diagrams render automatically)
2. Print to PDF from your browser (Ctrl+P → Save as PDF)

**Option B — VS Code:**
1. Open the report in VS Code
2. Install "Markdown PDF" extension (already installed: `yzane.markdown-pdf`)
3. Right-click the file → "Markdown PDF: Export (pdf)"

**Option C — Online:**
1. Go to https://markdownlivepreview.com/ or https://dillinger.io/
2. Paste the report content
3. Export as PDF

### Step 2: Create the ZIP File

The ZIP should contain ONLY the Java source files:

```
SEN3006_Task_Management_System.zip
├── AbstractTask.java
├── BugTask.java
├── BugTaskFactory.java
├── DeadlineFirstStrategy.java
├── DocumentationTask.java
├── DocumentationTaskFactory.java
├── FeatureTask.java
├── FeatureTaskFactory.java
├── Main.java
├── PriorityStrategy.java
├── SeverityFirstStrategy.java
├── Task.java
├── TaskFactory.java
├── TaskManager.java
├── TaskStatus.java
└── UrgentFirstStrategy.java
```

**To create the ZIP:**

On Windows (PowerShell):
```powershell
Compress-Archive -Path "src\main\java\*.java" -DestinationPath "SEN3006_Task_Management_System.zip"
```

On Git Bash:
```bash
cd src/main/java && zip ../../../SEN3006_Task_Management_System.zip *.java
```

### Step 3: Verify Before Submitting

Before you upload:

- [ ] Report is in PDF format
- [ ] PDF has all 7 UML diagrams visible
- [ ] PDF has all 9 sections (Introduction through References)
- [ ] ZIP contains all 16 .java files
- [ ] Code compiles: `javac -d bin *.java` (extract ZIP, run this)
- [ ] Code runs: `java -cp bin Main` → shows "ALL TESTS PASSED"

### Step 4: Submit

Upload both files to the submission portal before **June 05, 2026, 23:59**.

## For the Presentation

Review these files before your presentation:
- `docs/design/study-guide.md` — Every class explained + Q&A cheat sheet
- `docs/design/presentation-outline.md` — Slide-by-slide plan
- `docs/design/test-documentation.md` — What each test proves

Show the professor:
1. The GitHub repo (diagrams render visually in the .md files)
2. Run `Main.java` live and walk through the output
3. Point to specific classes when explaining patterns
