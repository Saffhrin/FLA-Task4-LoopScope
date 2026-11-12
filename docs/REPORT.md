# LoopScope: Infinite-Loop Detection and the Limits of Computation

**Course:** 21CSC301T Formal Language and Automata  
**Assessment:** CLA-2, Task 4  
**Student:** Saffhrin  
**Registration number:** To be added  
**Faculty:** Dr. C. Gunasundari  
**Institution:** SRM Institute of Science and Technology, Tiruchirappalli

## Abstract

This project studies the problem of deciding whether a program will halt or run forever on a given input. The general problem is undecidable: no algorithm can always return the correct answer for every program and input. The project explains this limit using the halting problem and a diagonal argument, then builds LoopScope, a small analyzer for a restricted one-variable loop language. For programs in that grammar, it proves termination or nontermination using integer arithmetic. Programs outside the grammar receive `UNKNOWN`. A separate finite-width mode shows how cycle detection can decide behavior when the machine state space is finite.

## 1. Problem statement

Given a program `P` and input `w`, determine whether `P` eventually halts on `w` or continues forever. In a real system, a watchdog timeout can stop a long-running job, but it cannot establish that the job would never finish. Static analysis can prove termination or nontermination for useful restricted cases, while returning an inconclusive result on other programs.

### Real-world and formal mapping

| Software question | Formal representation |
| --- | --- |
| Program source | A description of a Turing machine `M` |
| Input data | A finite input string `w` on the tape |
| “Does this run eventually stop?” | Membership of `⟨M,w⟩` in `HALT_TM` |
| “Does this run forever?” | Membership of `⟨M,w⟩` in the complement of `HALT_TM` |
| A timeout expires | No proof either way; the run may halt later |

See [the mapping diagram](diagrams/problem_mapping.svg).

## 2. Formal language and undecidability

Define

`HALT_TM = { ⟨M,w⟩ : Turing machine M halts on input w }`.

`HALT_TM` is recognizable: simulate `M` on `w`; accept when the simulation halts. If `M` runs forever, this recognizer also runs forever. Recognition is therefore not the same as deciding.

Assume for contradiction that a decider `H(⟨M,w⟩)` always answers correctly whether `M` halts on `w`. Construct a machine `D` that takes a machine description `x`, runs `H(⟨x,x⟩)`, loops if `H` says “halts,” and halts if `H` says “loops.” Now run `D` on its own description `d`:

- If `H(⟨d,d⟩)` says that `D(d)` halts, the construction makes `D(d)` loop.
- If `H(⟨d,d⟩)` says that `D(d)` loops, the construction makes `D(d)` halt.

Both answers contradict the assumed correctness of `H`, so no such general decider exists. Consequently, the complement language `LOOP_TM` is not recognizable: if both it and `HALT_TM` were recognizable, running their recognizers in alternation would decide `HALT_TM`.

## 3. LoopScope design

LoopScope restricts the program language to an integer initialization followed by one `while` guard and one constant update to the same variable. It supports `<`, `<=`, `>`, `>=`, `==`, and `!=`, plus `+=` and `-=`. The full grammar and implementation are in `loopguard/analyzer.py`.

The analyzer returns one of three outcomes:

- **HALTS** — arithmetic establishes that the guard becomes false, or is false initially.
- **LOOPS** — the supported update cannot make the active guard false, or the `!=` sequence cannot reach its bound.
- **UNKNOWN** — the program is outside the grammar, so this analyzer makes no claim.

For example, `i = 6; while i > 0: i -= 1` halts after six updates. `i = 4; while i < 9: i -= 2` loops because the value decreases while the guard requires it to rise. For `!=`, the analyzer checks whether the bound lies on the arithmetic progression from the initial value in the direction of the update.

The arithmetic model uses unbounded mathematical integers. It does not include exceptions, input, multiple variables, function calls, or other statements. Extending the grammar would require new proof rules.

## 4. Finite-width machine model

The optional finite-width simulator interprets the loop variable as an unsigned `b`-bit value. An update wraps modulo `2**b`. The complete configuration for this restricted deterministic program is its current variable value. If a value repeats while the guard is true, the same future transitions repeat, proving nontermination. If the guard becomes false first, the run halts.

This result is exact for the specified unsigned finite-width semantics. It may differ from the unbounded integer result because overflow changes the sequence of values. The diagram [Analyzer pipeline](diagrams/loopscope_pipeline.svg) shows how inputs receive a supported-model proof, a finite-state result, or `UNKNOWN`.

## 5. Limits and practical meaning

| Method | What it can establish | Limitation |
| --- | --- | --- |
| General simulation | A halt once it occurs | An execution that has not halted yet may still halt later |
| Timeout | That a time budget expired | Cannot prove a run is infinite |
| Restricted arithmetic analysis | Exact result for the supported loop grammar | Other control flow and state are outside the model |
| Finite-state cycle detection | Exact result for the stated finite deterministic machine | State spaces can become large; model assumptions matter |

The central lesson is that an honest analyzer must state its model and scope. A proof-backed `UNKNOWN` is more accurate than treating a timeout as a proof of an infinite loop.

## 6. Implementation and use

LoopScope is implemented in Python 3 with no third-party runtime dependencies. Run the examples from the repository root:

```powershell
python -m loopguard
python -m loopguard --example countdown
python -m loopguard --example stuck --fixed-width 4
```

The command-line output includes a verdict and its reason. The source examples are in `examples/`; diagrams are SVG files in `docs/diagrams/`.

## 7. Conclusion

The general halting problem has no always-correct decider. Useful exact analysis remains possible when a program family has enough structure to support a proof, or when the machine model has a finite state space that can be explored. LoopScope makes this distinction explicit: it proves results only within stated models and returns `UNKNOWN` outside them.

## Individual contribution statement

Student: Saffhrin. Contribution: formal problem formulation, literature-free course-theory explanation, restricted-language design, Python implementation, diagrams, and report preparation. Confirm the course's individual-submission requirement with the faculty because the assignment brief labels Task 4 as team work.
