#!/usr/bin/env python3
"""Build the Paper 9 arXiv source package."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper9_submission_source"
OUT = ROOT / "arxiv_submission_source.zip"

EXCLUDE_SUFFIXES = {
    ".aux",
    ".bbl",
    ".blg",
    ".log",
    ".out",
    ".pdf",
    ".toc",
    ".synctex.gz",
}


def include(path: Path) -> bool:
    if path.name.startswith("."):
        return False
    if path.name == "main.pdf":
        return False
    return not any(str(path).endswith(suffix) for suffix in EXCLUDE_SUFFIXES)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source directory: {SOURCE}")
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(SOURCE.rglob("*")):
            if path.is_file() and include(path):
                zf.write(path, path.relative_to(SOURCE))
    print(f"PAPER9_ARXIV_SOURCE_BUILT {OUT}")


if __name__ == "__main__":
    main()
