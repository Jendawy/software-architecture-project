"""Build the up-to-date submission bundle, excluding ALL Claude/Agent files."""
import os, zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "SEN3006_Task_Management_System.zip")

# Top-level files to include (mirrors the established committed bundle)
TOP_FILES = [
    "README.md", "SUBMISSION_README.md",
    "build-jar.sh", "build-jar.bat",
    "run-gui.sh", "run-gui.bat",
    "TaskManagerGUI.jar",
]

# Directories included recursively
INCLUDE_DIRS = ["src", "docs"]

# Hard exclusions: anything Claude/Agent/VCS/IDE/build/verify-artifact related.
DENY_DIRS = {".git", ".claude", ".agents", ".vscode", "bin",
             ".edge-print-tmp", "superpowers", "__pycache__"}
DENY_BASENAMES = {
    # Claude / Agent / config
    "CLAUDE.md", "AGENTS.md", ".mcp.json", ".gitignore",
    # report build / verification artifacts (not deliverables)
    "report-print.css", "_verify_titlepage.png", "SEN3006_Final_Report.html",
    # builder + helper scripts
    "_build_submission_zip.py", "generate-pdf-report.py",
}

def keep(rel):
    parts = rel.replace("\\", "/").split("/")
    if any(p in DENY_DIRS for p in parts):
        return False
    if os.path.basename(rel) in DENY_BASENAMES:
        return False
    return True

added = []
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for f in TOP_FILES:
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            z.write(p, f)
            added.append(f)
    for d in INCLUDE_DIRS:
        base = os.path.join(ROOT, d)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [dn for dn in dirnames if dn not in DENY_DIRS]
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT)
                if keep(rel):
                    z.write(full, rel.replace("\\", "/"))
                    added.append(rel.replace("\\", "/"))

print(f"Wrote {OUT}")
print(f"Total entries: {len(added)}")
size = os.path.getsize(OUT)
print(f"Zip size: {size} bytes ({round(size/1024)} KB)")
# Safety scan: assert no Claude/Agent leakage
bad = [a for a in added if any(t in a.lower() for t in
       ["claude", "agent", ".mcp", "/.git", "superpowers"])]
print("LEAK CHECK -> offending entries:", bad if bad else "NONE (clean)")
