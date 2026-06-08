#!/usr/bin/env python3
"""One-command reproduction check for Paper 9."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper9_submission_source"


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("$ " + " ".join(cmd) + f"  # cwd={cwd}")
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "1767225600")
    subprocess.run(cmd, cwd=cwd, check=True, env=env)


def main() -> None:
    run(["tectonic", "main.tex"], cwd=SOURCE)
    run([sys.executable, "scripts/build_arxiv_source.py"])
    run([sys.executable, "-m", "pytest", "-q"])
    print("PAPER9_REPRODUCTION_COMPLETE")


if __name__ == "__main__":
    main()
