#!/usr/bin/env python3
"""
Convenience runner for the Crystal Bank Starter Kit demo.
"""

from pathlib import Path
import subprocess
import sys


def main() -> int:
    here = Path(__file__).resolve().parent
    cli = here / "crystal_bank_cli.py"
    bank_path = here / "sample_bank.json"

    cmd = [sys.executable, str(cli), "demo", "--bank", str(bank_path)]
    completed = subprocess.run(cmd, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
