#!/usr/bin/env python3
"""
Interactive terminal menu for Crystal Bank Starter Kit.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CLI = HERE / "crystal_bank_cli.py"
DEFAULT_BANK = HERE / "sample_bank.json"


def run_cli(args: list[str]) -> int:
    cmd = [sys.executable, str(CLI)] + args
    return subprocess.run(cmd, check=False).returncode


def ensure_demo_bank() -> None:
    if DEFAULT_BANK.exists():
        return
    run_cli(["demo", "--bank", str(DEFAULT_BANK)])


def prompt(msg: str, default: str) -> str:
    value = input(f"{msg} [{default}]: ").strip()
    return value if value else default


def menu() -> None:
    ensure_demo_bank()
    while True:
        print("\n=== Crystal Bank Starter Kit Menu ===")
        print("1) Run full demo (PASS/FAIL)")
        print("2) Show bank summary")
        print("3) Run query")
        print("4) Show contradiction trace")
        print("5) Run system benchmark")
        print("6) Run large-scale synthetic benchmark")
        print("7) Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_cli(["demo", "--bank", str(DEFAULT_BANK)])
        elif choice == "2":
            run_cli(["summary", "--bank", str(DEFAULT_BANK)])
        elif choice == "3":
            subject = prompt("Subject", "Whale")
            relation = prompt("Relation", "is_a")
            object_ = prompt("Object", "Warm-blooded")
            polarity = prompt("Polarity (true/false)", "true")
            run_cli([
                "query",
                "--bank",
                str(DEFAULT_BANK),
                "--subject",
                subject,
                "--relation",
                relation,
                "--object",
                object_,
                "--polarity",
                polarity,
            ])
        elif choice == "4":
            run_cli([
                "trace",
                "--bank",
                str(DEFAULT_BANK),
                "--crystal",
                "whale_contradictory_en",
                "--a",
                "Whale",
                "--b",
                "Mammal",
                "--c",
                "Warm-blooded",
                "--rel-ab",
                "is_a",
                "--rel-bc",
                "is_a",
                "--rel-ac",
                "is_a",
            ])
        elif choice == "5":
            queries = prompt("Queries", "20000")
            run_cli([
                "system-benchmark",
                "--bank",
                str(DEFAULT_BANK),
                "--queries",
                queries,
            ])
        elif choice == "6":
            run_cli([
                "scale-benchmark",
                "--tier",
                "small:1000",
                "--tier",
                "medium:5000",
                "--tier",
                "large:15000",
                "--query-count",
                "2000",
            ])
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid choice, try again.")


def main() -> int:
    try:
        menu()
        return 0
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
