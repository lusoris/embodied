# progress

> **Layer:** L5 Community · **Owner:** planned Go `internal/progress`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

Support personal development without creating competition.

§9 of the recovered concept states this as three bullets — personal development, no rankings, no
competition — and it is the hardest constraint in the document to actually honour. **emBodied is a
platform built around measuring bodies and placing them in distributions. Comparison is its core
mechanic.** Adding progress tracking to that without producing a leaderboard requires the
constraint to be defended actively, in the design, rather than asserted once and forgotten.

## What is forbidden, structurally

Not by policy but by having no data path that would permit it:

- **No inter-person comparison of progress.** Progress is computed against a person's own history
  and against reference distributions, never against other users.
- **No rankings, percentile-of-percentile, or "better than X% of users" framings.** The platform
  places a body in a distribution; it does not rank persons within its membership.
- **No streaks, no scores, no achievement points.** Mechanics that reward frequency of measurement
  encourage measuring for the mechanic, which corrupts the data and is unkind to anyone anxious
  about their body.
- **No progress feed.** Other people's development is not content.

If a proposed feature requires comparing two users' progress, it is out of scope by construction,
not by review.

## What progress actually is here

| Form | Notes |
| :--- | :--- |
| **Change over time** | Your own measurements, honestly presented, with measurement uncertainty shown so that noise is not read as change. |
| **Knowledge** | What you have learned, what you have explored. Self-reported, private. |
| **Self-determination** | Goals a person set for themselves, in their own terms, including goals the platform has no opinion about. |

The third is the one §11A's self-empowerment theme actually means. A goal the platform did not
suggest, cannot evaluate and does not score.

**Measurement noise is the specific technical risk.** Two measurements of the same body differ by
protocol variance alone; presenting that difference as change would manufacture progress and
anxiety in equal measure. Change is only reported where it exceeds the measurement uncertainty
that [`statistics-engine`](../l2-intelligence/statistics-engine.md) computes — and where it does
not, the honest display is "no detectable change", not a flat line implying precision.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `trajectory` | A person's own measurement history for a feature, with intervals. |
| `goal` | Self-set, self-described, self-evaluated. Private by default. |
| `milestone` | A personally meaningful point, marked by the person, not awarded. |

## Interfaces

- **Provides:** trajectory, change detection, goal tracking.
- **Consumes:** [`measurement`](../l1-core/measurement.md),
  [`statistics-engine`](../l2-intelligence/statistics-engine.md) for uncertainty-aware change
  detection, [`anatomy`](../l1-core/anatomy.md) for feature state history.
- **Consumed by:** [`visualizer`](../l3-expression/visualizer.md).

Deliberately consumed by very little. Progress data that flows outward becomes comparable, and
comparable progress is a ranking waiting to be computed.

## Consent surface

Private by default and private as the expected steady state. Sharing a trajectory is possible and
should stay unusual.

Progress history is also transition history — for a trans or post-surgical user, a trajectory is a
record of a change that may be deeply private. `OQ-008` in [`anatomy`](../l1-core/anatomy.md)
applies with full force here.

## Open questions

- `OQ-064` — Is any progress sharing supported at all? Any sharing mechanism creates the
  comparison this module exists to prevent, and total prohibition denies people a legitimate wish
  to be seen.
- `OQ-065` — How is "no detectable change" presented over long periods without reading as failure?
