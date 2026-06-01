"""
Publishes the latest website changes to GitHub Pages.
Run automatically after the daily entry generator.

Writes a log to publish.log so scheduled-task runs can be diagnosed.

Usage: python publish.py
"""

import subprocess
import os
import sys
from datetime import datetime, date

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(ROOT, 'publish.log')

# Make sure the GitHub CLI (used by the git credential helper) is on PATH
GH_DIR = r"C:\Program Files\GitHub CLI"
if os.path.isdir(GH_DIR) and GH_DIR not in os.environ.get("PATH", ""):
    os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + GH_DIR


def log(msg):
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line)
    try:
        with open(LOGFILE, 'a', encoding='utf-8') as f:
            f.write(line + "\n")
    except Exception:
        pass


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, shell=True)


def main():
    run("git add -A")

    status = run("git status --porcelain")
    has_local_changes = bool(status.stdout.strip())

    if has_local_changes:
        msg = f"Daily update: {date.today().isoformat()}"
        c = run(f'git -c user.name="Human Behaviour Bot" -c user.email="bot@local" commit -m "{msg}"')
        if c.returncode == 0:
            log(f"Committed: {msg}")
        else:
            log(f"Commit note: {c.stdout.strip() or c.stderr.strip()}")

    # Always attempt to push — covers the case where a previous commit never pushed
    ahead = run("git rev-list --count origin/main..HEAD")
    n_ahead = ahead.stdout.strip() or "?"

    if not has_local_changes and n_ahead in ("0", ""):
        log("Nothing to publish (working tree clean, in sync with remote).")
        return

    result = run("git push origin main")
    if result.returncode == 0:
        log(f"Push OK ({n_ahead} commit(s) ahead pushed).")
    else:
        # Retry once
        log(f"Push failed, retrying. Error: {result.stderr.strip()[:300]}")
        result2 = run("git push origin main")
        if result2.returncode == 0:
            log("Push OK on retry.")
        else:
            log(f"PUSH FAILED AGAIN: {result2.stderr.strip()[:300]}")


if __name__ == "__main__":
    main()
