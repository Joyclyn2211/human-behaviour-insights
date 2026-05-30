"""
Publishes the latest website changes to GitHub Pages.
Run automatically after the daily entry generator.

Usage: python publish.py
"""

import subprocess
import os
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, shell=True)

def main():
    # Stage everything
    run("git add -A")

    # Check if there's anything to commit
    status = run("git status --porcelain")
    if not status.stdout.strip():
        print("No changes to publish.")
        return

    # Commit and push
    msg = f"Daily update: {date.today().isoformat()}"
    run(f'git -c user.name="Human Behaviour Bot" -c user.email="bot@local" commit -m "{msg}"')
    result = run("git push origin main")

    if result.returncode == 0:
        print(f"Published successfully: {msg}")
    else:
        print(f"Push failed: {result.stderr}")

if __name__ == "__main__":
    main()
