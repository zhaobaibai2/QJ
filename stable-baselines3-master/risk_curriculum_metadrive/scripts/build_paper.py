#!/usr/bin/env python
"""Compile the Chinese paper draft when a TeX toolchain is available."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=PAPER, check=True)


def main() -> None:
    if shutil.which("xelatex") is None:
        raise RuntimeError("xelatex is not installed; paper PDF was not rebuilt.")
    run(["xelatex", "-interaction=nonstopmode", "main_zh.tex"])
    if shutil.which("bibtex") is not None:
        run(["bibtex", "main_zh"])
        run(["xelatex", "-interaction=nonstopmode", "main_zh.tex"])
        run(["xelatex", "-interaction=nonstopmode", "main_zh.tex"])
    print(f"saved_pdf={PAPER / 'main_zh.pdf'}")


if __name__ == "__main__":
    main()
