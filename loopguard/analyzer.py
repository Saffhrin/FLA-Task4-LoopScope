"""Exact reasoning for constant-step, one-variable loops.

This deliberately small language makes its scope visible: supported loops are
decided by integer arithmetic; source outside the grammar receives UNKNOWN.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


class Verdict(str, Enum):
    HALTS = "HALTS"
    LOOPS = "LOOPS"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class LoopProgram:
    variable: str
    initial: int
    operator: str
    bound: int
    step: int


@dataclass(frozen=True)
class AnalysisResult:
    verdict: Verdict
    explanation: str
    program: LoopProgram | None = None
    iterations: int | None = None


_PROGRAM = re.compile(
    r"\A\s*(?P<var>[A-Za-z_]\w*)\s*=\s*(?P<initial>-?\d+)\s*\n"
    r"\s*while\s+(?P=var)\s*(?P<op><=|>=|==|!=|<|>)\s*(?P<bound>-?\d+)\s*:\s*\n"
    r"\s+(?P=var)\s*(?:(?:\+=\s*(?P<plus>-?\d+))|(?:-=\s*(?P<minus>-?\d+)))\s*\Z"
)


def parse_program(source: str) -> LoopProgram | None:
    """Parse exactly an assignment and a one-line constant-step while body."""
    match = _PROGRAM.fullmatch(source)
    if not match:
        return None
    step_text = match.group("plus")
    step = int(step_text) if step_text is not None else -int(match.group("minus"))
    return LoopProgram(
        variable=match.group("var"),
        initial=int(match.group("initial")),
        operator=match.group("op"),
        bound=int(match.group("bound")),
        step=step,
    )


def _holds(value: int, operator: str, bound: int) -> bool:
    return {
        "<": value < bound,
        "<=": value <= bound,
        ">": value > bound,
        ">=": value >= bound,
        "==": value == bound,
        "!=": value != bound,
    }[operator]


def _classify(program: LoopProgram) -> tuple[Verdict, str, int | None]:
    x, b, d, op = program.initial, program.bound, program.step, program.operator
    if not _holds(x, op, b):
        return Verdict.HALTS, f"The guard is false initially, so the body runs zero times.", 0

    if op in ("<", "<="):
        if d <= 0:
            return Verdict.LOOPS, f"The guard is true and an update of {d} cannot increase {x} toward {b}."
        distance = b - x + (1 if op == "<=" else 0)
        count = max(0, (distance + d - 1) // d)
        return Verdict.HALTS, f"Each update increases the value by {d}; after {count} update(s), the guard is false.", count

    if op in (">", ">="):
        if d >= 0:
            return Verdict.LOOPS, f"The guard is true and an update of {d} cannot decrease {x} toward {b}."
        distance = x - b + (1 if op == ">=" else 0)
        count = max(0, (distance + (-d) - 1) // (-d))
        return Verdict.HALTS, f"Each update decreases the value by {-d}; after {count} update(s), the guard is false.", count

    if op == "==":
        if d == 0:
            return Verdict.LOOPS, "The equality guard stays true because the body leaves the value unchanged."
        return Verdict.HALTS, "The equality guard is true for the current value; one nonzero update makes it false.", 1

    # x != b
    if d == 0:
        return Verdict.LOOPS, "The value never changes, so it never reaches the value that would make != false."
    difference = b - x
    if difference % d == 0 and difference // d > 0:
        count = difference // d
        return Verdict.HALTS, f"The repeated update reaches {b} after {count} update(s), making != false.", count
    return Verdict.LOOPS, "The constant-step sequence never lands on the bound, so != remains true forever."


def analyze(source: str) -> AnalysisResult:
    """Return a proof-backed verdict for the supported one-loop language."""
    program = parse_program(source)
    if program is None:
        return AnalysisResult(
            Verdict.UNKNOWN,
            "Outside the supported grammar. This analyzer does not infer a verdict for arbitrary programs.",
        )
    verdict, explanation, iterations = _classify(program)
    return AnalysisResult(verdict, explanation, program, iterations)


def simulate_fixed_width(program: LoopProgram, bits: int = 4) -> AnalysisResult:
    """Decide the loop under unsigned b-bit wraparound semantics.

    The finite configuration is the current value. Repetition proves an
    infinite run because both the guard and update are deterministic.
    """
    if bits < 1 or bits > 20:
        return AnalysisResult(Verdict.UNKNOWN, "bits must be between 1 and 20.", program)
    modulus = 1 << bits
    value = program.initial % modulus
    bound = program.bound % modulus
    seen: set[int] = set()
    steps = 0
    while _holds(value, program.operator, bound):
        if value in seen:
            return AnalysisResult(
                Verdict.LOOPS,
                f"Unsigned {bits}-bit execution repeated value {value}; determinism makes the future repeat forever.",
                program,
            )
        seen.add(value)
        value = (value + program.step) % modulus
        steps += 1
    return AnalysisResult(
        Verdict.HALTS,
        f"Unsigned {bits}-bit execution made the guard false after {steps} update(s).",
        program,
        steps,
    )
