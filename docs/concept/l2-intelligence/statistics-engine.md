# statistics-engine

> **Layer:** L2 Intelligence · **Owner:** planned Rust `crates/embodied-stats`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

The mathematics behind [`statistics`](../l1-core/statistics.md) and the plausibility assessment in
[`measurement`](../l1-core/measurement.md). Percentile placement, interval estimation,
distribution fitting, cohort weighting, suppression thresholds.

This is a separate crate from the policy module above it for one reason: **the mathematics must be
testable in isolation and identical everywhere it runs**. A percentile computed for a chart, for a
plausibility flag and for a simulation input must be the same number by construction, not by three
implementations agreeing.

## What it owns

| Capability | Notes |
| :--- | :--- |
| Percentile placement | Value into a named distribution, with interval. |
| Interval estimation | Propagating sample size, protocol variance and measurement grade. |
| Distribution fitting | Deriving a distribution from a source's summary statistics. |
| Pooling | Weighted means and pooled standard deviations across studies, as Veale et al. do. |
| Plausibility | Distance from distribution plus internal-consistency checks across a session. |
| Suppression | Minimum cohort size enforcement before a figure may be released. |

Uncertainty propagation is the part that must not be treated as decoration. A percentile derived
from a `self-reported` measurement placed against a pooled distribution from seventeen studies has
two distinct uncertainty sources, and the output interval has to carry both. §5's commitment that
uncertainty is shown, never hidden, is implemented here or nowhere.

## Implementation

Pure computation — no I/O, no storage, no state. Deterministic given inputs, which is what makes
HISS-15 three-dimensional testing (positive, negative, boundary) tractable: boundary cases are the
tails, empty cohorts, single-sample distributions and values outside any observed range, and all of
them have defined correct answers.

HISS-04 caps apply (McCabe ≤ 10, ≤ 75 LOC per function), which for numerical code means
decomposition into named, individually testable steps rather than one long formula.

No `unwrap`, no panic paths: a distribution with insufficient data returns a typed insufficiency,
because "we cannot say" is a legitimate and frequently correct answer on this platform.

## Interfaces

- **Provides:** placement, interval, fit, pool, plausibility, suppression check.
- **Consumes:** nothing. Inputs are passed in; the crate reads no store.
- **Consumed by:** [`statistics`](../l1-core/statistics.md),
  [`measurement`](../l1-core/measurement.md), [`simulation`](simulation.md),
  [`body-vector`](body-vector.md) for bootstrap normalisation.

## Consent surface

None. The crate never sees an identity — it receives values and distributions. Keeping it that way
is a deliberate boundary: statistical code that cannot identify anyone cannot leak anyone.

## Open questions

- `OQ-024` — Which distribution families are supported, and what happens when a source's summary
  statistics do not support the assumed family? Veale et al. simulate from the normal; not every
  feature will be normal.
- `OQ-025` — How are intervals combined when a simulation input is itself an estimate? Naive
  propagation will produce intervals so wide as to be useless, and narrowing them by assumption
  would be dishonest.
