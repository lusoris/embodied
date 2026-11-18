# reference

> **Layer:** L1 Core · **Owner:** planned Go `internal/reference` + repository
> `lusoris/embodied-reference-data` ([ADR-0001](../../adr/0001-go-rust-svelte-split.md),
> [ADR-0007](../../adr/0007-user-reference-data-separation.md); no code exists yet)
> **ADR:** [0007](../../adr/0007-user-reference-data-separation.md)

## Purpose

Supply the distributions everything statistical is measured against, with a citation trail strong
enough that any number on the platform can be traced to the study that produced it.

Reference data is **physically separated from user data** — not merely a different schema but a
different repository with its own release cadence, its own review and its own version history.
The separation is structural because the two kinds of data have incompatible properties: reference
data is public, citable, immutable once released and slow-moving; user data is private,
revocable, mutable and fast. A boundary that exists only as a table prefix will eventually be
crossed by a convenient join.

## The baseline

Published literature using **measured rather than self-reported** protocols. The criterion is not
a preference; self-reported anthropometric data is known to be inflated, and a reference curve
built on it would make every user comparison wrong in the same direction.

Two anchor sources for the initial catalogue:

- Veale D, Miles S, Bramley S, Muir G, Hodsoll J. *Am I normal? A systematic review and
  construction of nomograms for flaccid and erect penis length and circumference in up to 15 521
  men.* BJU International 2015;115(6):978–986. [doi:10.1111/bju.13010](https://doi.org/10.1111/bju.13010),
  PMID 25487360. — 17 studies, measurement by health professionals to a standard procedure,
  minimum 50 participants per sample, with congenital abnormality, prior surgery, small-penis
  complaint and erectile dysfunction excluded. The nomograms are the reference implementation of
  what this module should produce.
- *A Systematic Review and Meta-Analysis of Penis Length and Circumference According to WHO
  Regions.* [PMC11923605](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11923605/). — Relevant
  because it is stratified by **WHO region** rather than by racial category, which is precisely
  the framing [ADR-0008](../../adr/0008-population-comparison-as-regional-adaptation.md) commits
  the platform to.

The catalogue beyond these is thin, and for most features outside male genital dimensions it is
close to absent. That is a finding, not an obstacle to route around: where no defensible reference
exists, the platform says so. The **coverage map is itself a visible feature** — showing where
knowledge runs out is more honest than interpolating over it, and more useful.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `source` | Study: citation, DOI, cohort, protocol, sample size, exclusions, limitations. |
| `distribution` | Derived reference distribution, bound to source and protocol version. |
| `cohort` | Population descriptor — region, age band, recruitment. Never a racial category. |
| `release` | Immutable versioned snapshot of the catalogue. |
| `coverage_gap` | An explicit record of what has no defensible reference. |

## Interfaces

- **Provides:** distribution lookup by feature and cohort, citation resolution, coverage map,
  release pinning.
- **Consumes:** nothing from user data. This direction is enforced — the module has no read path
  into the user database.
- **Consumed by:** [`statistics`](statistics.md), [`measurement`](measurement.md) (plausibility),
  [`body-vector`](../l2-intelligence/body-vector.md) (bootstrap structure),
  [`visualizer`](../l3-expression/visualizer.md).

Consumers pin a release. A reference update never silently changes what a user was shown
yesterday; it produces a new release, and the change is visible.

## Consent surface

None directly — this module holds no personal data, which is the point. Its consent relevance is
inverse: the **user overlay** described in [`statistics`](statistics.md) is a separate dataset,
contributed under separate consent, and never merged into a release.

## Open questions

- `OQ-013` — What is the ingestion process for a new source, and who reviews methodology? An
  unreviewed citation trail is decorative.
- `OQ-014` — Does the separate repository hold derived distributions only, or the extracted source
  data as well? The latter is more useful and raises redistribution questions per source licence.
- `OQ-015` — How is the protocol in a published study mapped onto a platform protocol version when
  they do not match exactly? See `OQ-009`.
