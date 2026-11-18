# statistics

> **Layer:** L1 Core · **Owner:** planned Go `internal/statistics`, computing via
> `crates/embodied-stats` ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)
> **ADR:** [0008](../../adr/0008-population-comparison-as-regional-adaptation.md)

## Purpose

Place a body in a real distribution, and be honest about how well it is placed.

This is the module most likely to be quoted, screenshotted and argued with, so its output format
matters as much as its mathematics. **A number without a sample size and an interval is a claim
the platform will not make.** Percentiles are always accompanied by the source release, the cohort,
the protocol and the uncertainty.

## Two curves, never merged

| Curve | Source | Status |
| :--- | :--- | :--- |
| **Reference** | Published, measured-protocol literature | Citable, versioned, authoritative |
| **User overlay** | Platform measurements at or above a verification threshold | Larger, broader, self-selected |

Both may be shown; they are always labelled; they are never combined into a single curve. The
overlay is self-selected by definition — people who join a body-measurement platform are not a
random sample of humanity — and presenting it as equivalent to clinical data would be the exact
dishonesty §5 exists to prevent.

The overlay's inclusion threshold is a [`verification`](verification.md) grade, set here as
policy rather than hard-coded.

## Population comparison

The concept keeps population comparison and reframes it. The reasoning is in
[ADR-0008](../../adr/0008-population-comparison-as-regional-adaptation.md); the operational rules
are:

1. Cohorts are **geographic and study-defined** — WHO region, country, recruitment population —
   never racial categories.
2. Where a difference is real, the platform explains the **mechanism**: evolutionary and regional
   pressures, climate and latitude, founder effects, genetic drift. A difference without a
   mechanism is a stereotype with a number attached.
3. Every group statistic ships with sample size, protocol, confidence interval and its known
   limitations.
4. Every group comparison states that **individual variation dwarfs group means**, because it
   does, and because omitting it is how this material gets misused.
5. Where the literature is too thin to support a comparison, the platform shows the coverage gap
   rather than the comparison.

Rule 5 will delete a lot of comparisons people want. That is the correct outcome.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `placement` | A measurement's position in a named distribution, with interval. |
| `cohort_selection` | Which cohort a comparison was run against, and why. |
| `overlay_policy` | Verification threshold and exclusion rules for the user curve. |
| `presentation_contract` | What must accompany a figure before it may be rendered. |

`presentation_contract` is deliberately data. The rule that a percentile cannot be displayed
without its uncertainty should be enforceable by the system, not left to each UI author.

## Interfaces

- **Provides:** placement, comparison, cohort selection, coverage reporting.
- **Consumes:** [`reference`](reference.md), [`measurement`](measurement.md),
  [`verification`](verification.md), [`statistics-engine`](../l2-intelligence/statistics-engine.md).
- **Consumed by:** [`visualizer`](../l3-expression/visualizer.md),
  [`simulation`](../l2-intelligence/simulation.md), [`education`](../l5-community/education.md).

## Consent surface

Contributing to the overlay is consented separately from recording a measurement. A person may
keep their body data entirely private and still use every comparison feature — the platform takes
from the commons without requiring payment into it.

Aggregates must resist re-identification: small cohorts are suppressed rather than shown with a
wide interval, because a sufficiently narrow cohort is a person.

## Open questions

- `OQ-016` — What is the minimum cohort size for display, and how is suppression communicated
  without implying the data is hidden for another reason?
- `OQ-017` — Does the user overlay feed back into anything other than display? If it influences
  plausibility checking, self-selection bias becomes self-reinforcing.
