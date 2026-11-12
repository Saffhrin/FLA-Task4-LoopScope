"""Command line examples for LoopScope."""

from __future__ import annotations

import argparse

from .analyzer import analyze, parse_program, simulate_fixed_width
from .programs import EXAMPLES


def _show(label: str, source: str) -> None:
    result = analyze(source)
    print(f"{label:14} {result.verdict.value:7}  {result.explanation}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sound termination analysis for a small loop language")
    parser.add_argument("--example", choices=(*EXAMPLES, "all"), default="all")
    parser.add_argument("--fixed-width", type=int, metavar="BITS", help="also model the selected supported example with unsigned wraparound")
    args = parser.parse_args()

    names = EXAMPLES if args.example == "all" else {args.example: EXAMPLES[args.example]}
    print("LoopScope — restricted loop termination analyzer")
    for label, source in names.items():
        _show(label, source)
        if args.fixed_width and (program := parse_program(source)) is not None:
            result = simulate_fixed_width(program, args.fixed_width)
            print(f"  {args.fixed_width}-bit: {result.verdict.value} — {result.explanation}")


if __name__ == "__main__":
    main()
