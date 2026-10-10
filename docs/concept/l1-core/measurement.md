# measurement

> **Layer:** L1 Core · **Owner:** Go `internal/measurement`

## Purpose

Capture body data in a form that can actually carry statistical weight — which means the
measurement *protocol* is part of the datum, not an instruction that precedes it.

This is the single most common failure in existing body-measurement data, and the reason §5 of the
concept insists that reference literature use measured rather than self-reported protocols. Two
numbers for the same quantity are not comparable if one was taken along the dorsal surface to the
pubic bone and the other was not. A platform that stores the number and discards the method has
built a statistics product on sand.

So every measurement records what was measured, how, with what, and under what conditions. The
protocol is versioned. Changing a protocol does not silently reinterpret existing data.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `protocol` | Versioned definition: landmarks, instrument, posture, state, conditions. |
| `measurement` | Value, unit, protocol version, timestamp, feature instance. |
| `plausibility_assessment` | Outcome of checking a value against distribution and internal consistency. |
| `measurement_session` | A set taken together; supports internal cross-checks. |

Units are stored canonically and displayed by preference. Never store what the user typed.

## Interfaces

- **Provides:** capture, protocol resolution, plausibility assessment, history.
- **Consumes:** [`anatomy`](anatomy.md) for the applicable schema,
  [`verification`](verification.md) for grading, [`statistics-engine`](../l2-intelligence/statistics-engine.md)
  for plausibility mathematics.
- **Consumed by:** [`statistics`](statistics.md), [`body-vector`](../l2-intelligence/body-vector.md),
  [`visualizer`](../l3-expression/visualizer.md), [`avatar`](../l3-expression/avatar.md),
  [`simulation`](../l2-intelligence/simulation.md).

## Plausibility, and what it must not become

Plausibility checking exists to catch unit confusion, typos and impossible values. It must not
become a mechanism that tells people their body is wrong.

An implausible value is flagged as *unlikely given the reference distribution* and the person is
invited to re-check the protocol — never rejected, never corrected, never quietly clamped. Real
bodies occupy the tails of every distribution, and the platform's first principle commits it to
believing them. A flagged measurement is still recorded; it simply carries its flag, and
[`statistics`](statistics.md) decides what to do with it.

## Consent surface

Measurement is the most identifying non-media data on the platform. Capture is consented per
feature, storage is consented separately from contribution to aggregate statistics, and the
distinction is meaningful: a person may record their body for their own use and never feed the
reference overlay.

## Open questions

- `OQ-009` — Which protocols ship initially, and are they drawn from the same literature that
  supplies the reference baseline? Protocol drift between reference and user data destroys
  comparability. See [`reference`](reference.md).
- `OQ-010` — Guided capture: how much does the platform assist (instructions, imagery, a
  measuring aid) before assistance becomes pressure?
