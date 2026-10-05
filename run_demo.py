"""Run from a repository checkout without installing the package itself."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from hrcev_lite.cli import main

if __name__ == "__main__":
    main(["demo", "--examples", str(ROOT / "examples"), "--output", str(ROOT / "outputs/demo"), *sys.argv[1:]])
