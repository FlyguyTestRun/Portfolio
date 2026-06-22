#!/usr/bin/env python3
"""genesis.py -- extract falcon-grounds from the Portfolio branch into a target directory.

Usage:
    python genesis.py C:\\JLL_T          # Windows
    python genesis.py /path/to/target    # macOS / Linux
    python genesis.py                     # defaults to ./jll-t

Requires git. Clones the portfolio branch and extracts the jll-t/ subdirectory
into the target path.

After running:
    cd <target>
    git init
    git add .
    git commit -m "Add falcon-grounds: seven-layer cost-control governed agentic RAG"
    git push
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO = "https://github.com/FlyguyTestRun/Portfolio.git"
BRANCH = "claude/jll-ai-agent-job-plan-kqeri6"
SUBDIR = "jll-t"


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("jll-t")
    target = target.expanduser().resolve()
    print(f"Extracting falcon-grounds to {target}")

    tmp = target.parent / ".genesis_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)

    print(f"Cloning {REPO} (branch: {BRANCH})...")
    subprocess.run(
        [
            "git", "clone",
            "--depth=1",
            "--filter=blob:none",
            "--sparse",
            "--branch", BRANCH,
            REPO,
            str(tmp),
        ],
        check=True,
    )

    subprocess.run(
        ["git", "sparse-checkout", "set", SUBDIR],
        cwd=tmp,
        check=True,
    )

    src = tmp / SUBDIR
    if not src.exists():
        print(f"ERROR: {SUBDIR}/ not found in branch. Check BRANCH and SUBDIR constants.")
        sys.exit(1)

    if target.exists():
        shutil.rmtree(target)

    shutil.copytree(src, target)
    shutil.rmtree(tmp)

    file_count = sum(1 for _ in target.rglob("*") if _.is_file())
    print(f"Done. {file_count} files written to {target}")
    print()
    print("Next steps:")
    print(f"  cd {target}")
    print("  git init")
    print("  git add .")
    print('  git commit -m "Add falcon-grounds: seven-layer cost-control governed agentic RAG"')
    print("  git push")


if __name__ == "__main__":
    main()
