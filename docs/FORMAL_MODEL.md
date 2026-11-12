# Formal model and analysis rules

## General halting problem

`HALT_TM = {⟨M,w⟩ : M halts on input w}` is Turing-recognizable: simulate `M` on `w`, accepting if it halts. It is undecidable by the diagonal contradiction described in [the report](REPORT.md). Its complement is not Turing-recognizable; otherwise recognizers for the language and its complement could be run in parallel to decide it.

## Restricted loop language

LoopScope accepts one integer assignment followed by a one-statement `while` loop:

```text
x = n
while x op b:
    x += d
```

Here `n`, `b`, and `d` are signed integer constants, and `op` is one of `<`, `<=`, `>`, `>=`, `==`, or `!=`. A `-=` body is normalized to a negative step. There are no side effects, I/O, exceptions, or other variables in this model. The mathematical-integer model has no overflow.

At each iteration, the machine tests the guard. If it is false, it halts. Otherwise it replaces `x` with `x + d` and returns to the guard. An unrecognized source program receives `UNKNOWN` because it has no transition system in this subset.

## Why the arithmetic rules are exact

- For `<` and `<=`, a true guard can move toward becoming false only when `d > 0`. The distance to the first false value gives the finite number of updates. If `d <= 0`, the guard remains true forever.
- For `>` and `>=`, the symmetric argument applies: a negative step reaches a false guard; a nonnegative step preserves a true guard.
- For `==`, the active guard with `d = 0` repeats forever; with a nonzero step it becomes false after one update.
- For `!=`, a zero step preserves the true guard. A nonzero step halts exactly when the bound lies on the forward arithmetic progression from the initial value; otherwise equality is never reached.

The parser and implementation of these rules are in [`loopguard/analyzer.py`](../loopguard/analyzer.py).

## Finite-width semantics

For a `b`-bit unsigned model, the configuration is the current value in `{0,…,2^b−1}`. The transition updates the value modulo `2^b`. There are finitely many configurations. If a configuration repeats while the guard is true, determinism implies that all subsequent configurations repeat, proving a loop. If a false guard is reached first, the execution halts. This finite-width result may differ from the unbounded-integer result.
