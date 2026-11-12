# LoopScope: Infinite-Loop Detection and the Limits of Computation

**Formal Language and Automata — CLA-2 Assessment, Task 4**  
**Student:** Saffhrin  ·  **Registration number:** to be added

LoopScope demonstrates why no program can decide termination correctly for every possible program and input, then implements a small analyzer that can give exact answers on a clearly stated restricted language.

## What it demonstrates

| Part | Model or result | What LoopScope does |
| --- | --- | --- |
| General theory | `HALT_TM` is undecidable; it is recognizable by direct simulation | Explains the diagonal argument and why a timeout cannot prove a loop |
| Unrestricted practical code | No universal exact termination checker exists | Returns `UNKNOWN` when input is outside the supported grammar |
| Restricted integer loops | One variable, one comparison, one constant update | Uses arithmetic to prove `HALTS` or `LOOPS` |
| Finite-width machine | Unsigned `b`-bit value with wraparound | Detects a repeated configuration; repetition proves a loop in that model |

The implementation is intentionally small enough to inspect. It does **not** claim to analyze arbitrary Python or arbitrary Turing machines.

## Run it

Requires Python 3.10 or later. There are no third-party runtime dependencies.

```powershell
cd FLA-Task4-LoopScope
python -m loopguard
python -m loopguard --example countdown
python -m loopguard --example stuck --fixed-width 4
```

The examples report `HALTS`, `LOOPS`, or `UNKNOWN`, with a short reason. The CLI accepts its bundled examples; use `loopguard.analyze(source)` from Python to analyze a source string.

## Supported source form

```text
name = signed_integer
while name <comparison> signed_integer:
    name += signed_integer
```

`-=` is also supported. The condition operators are `<`, `<=`, `>`, `>=`, `==`, and `!=`. The same variable must appear in the initialization, guard, and update. The loop body must contain exactly one constant-step update. Every other program receives `UNKNOWN`.

Example:

```python
i = 6
while i > 0:
    i -= 1
```

The ordinary integer model proves this halts after six updates. If code is not in the grammar, LoopScope does not guess based on a short run.

## Finite-width mode

`simulate_fixed_width(program, bits)` uses unsigned values from `0` to `2**bits - 1` and wraps each update modulo `2**bits`. It checks the current value before each update. There are finitely many possible values; if one repeats while the guard is true, the deterministic run repeats forever. If the guard becomes false first, the run halts. The value of `bits` is limited to 1–20 in this teaching implementation.

This is a different semantics from unbounded mathematical integers. A loop can halt in one model and loop in another.

## Diagrams

### From the software question to the halting problem

![Diagram mapping a real program and input to the formal halting problem](docs/diagrams/problem_mapping.png)

*Figure 1. A program and input map to a Turing machine and input. A timeout is inconclusive, and no universal exact decider exists.*

[Open the editable problem mapping diagram](docs/diagrams/problem_mapping.dot) · [Open the vector version](docs/diagrams/problem_mapping.svg).

### Where the halting problem sits in the language classes

![Diagram of decidable and recognizable language classes](docs/diagrams/decidability_classes.png)

*Figure 2. `HALT_TM` is recognizable but undecidable; its complement `LOOP_TM` is not recognizable.*

[Open the editable language class diagram](docs/diagrams/decidability_classes.dot) · [Open the vector version](docs/diagrams/decidability_classes.svg).

### How LoopScope chooses its result

![LoopScope source analysis pipeline](docs/diagrams/loopscope_pipeline.png)

*Figure 3. Supported loops receive a proof under a named model; unsupported programs receive `UNKNOWN`.*

[Open the editable pipeline diagram](docs/diagrams/loopscope_pipeline.dot) · [Open the vector version](docs/diagrams/loopscope_pipeline.svg).

## Project contents

```text
loopguard/                 analyzer, CLI, and bundled examples
  analyzer.py              parser, proof rules, finite-width simulator
  cli.py                   command-line demonstration
  programs.py              sample-program catalogue
examples/                  readable example source files
docs/
  REPORT.md                 project report draft
  FORMAL_MODEL.md           grammar, transitions, proof rules, limitations
  diagrams/                 editable DOT plus PNG and SVG figures
tools/
  make_diagrams.py          rebuilds the PNG previews
```

The report, model notes, and diagrams are kept as separate files so each part is easy to find and update.

## Rebuild diagram previews

Install the optional image dependency, then run:

```powershell
python -m pip install -r requirements-diagrams.txt
python tools/make_diagrams.py
```

This rebuilds the three PNG previews from the diagram layouts in the script. Editable Graphviz source files are included beside each figure.

## Academic scope and individual work

The assignment brief describes Task 4 as team work. This repository records one student's implementation and report; confirm with the course faculty that an individual submission is acceptable. Add the registration number and any required contribution statement before submission.

The project is an original implementation and explanation. It uses the sample repository only as a reference for topic and presentation, not as source code or report text.

## License

For coursework and educational use. Add the license required by the course or institution if one is specified.
