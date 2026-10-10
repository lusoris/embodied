# ADR-0008: Population comparison framed as regional adaptation, not racial category

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

The recovered concept listed "ethnic and statistical comparison" as a body-data feature. This is
simultaneously something users genuinely want to know, and the single most reputationally hazardous
content the platform could publish.

The hazards are real and specific. The literature on population differences in genital dimensions
is thin and heavily contaminated by self-report. The topic carries obvious racial-stereotype
baggage, and any figure published will be quoted out of context. Framed as a fact about racial
categories, such a figure is both scientifically unsound — race is a poor proxy for the underlying
population genetics — and socially corrosive.

But the underlying phenomenon is not fictional. Human populations do differ measurably in many
anthropometric traits, and the mechanism is evolutionary and regional: climate, latitude, UV
exposure, founder effects, genetic drift. Deleting the topic entirely would be a defensible choice
and would also remove legitimate content from a platform whose premise is realism over comfort.

## Decision

Keep population comparison, and reframe it around **mechanism and geography** rather than racial
category.

Operational rules, enforced in `statistics`:

1. Cohorts are **geographic and study-defined** — WHO region, country, recruitment population.
   Never racial categories.
2. Where a difference is real, the platform explains the **mechanism** — regional and evolutionary
   pressures, climate and latitude, founder effects, drift. A difference without a mechanism is a
   stereotype with a number attached.
3. Every group statistic ships with sample size, measurement protocol, confidence interval and
   known limitations.
4. Every group comparison states that **individual variation dwarfs group means** — because it
   does, and because omitting it is how this material gets misused.
5. Where the literature is too thin to support a comparison, the platform shows the **coverage
   gap** rather than the comparison.

## Consequences

The legitimate content survives in a form that is scientifically defensible and explains rather
than merely asserts. The framing matches the better literature: region-stratified meta-analyses
already organise by WHO region rather than by race.

Rule 5 will delete many comparisons people actively want, because the data does not support them.
That is the correct outcome and it will be unpopular.

Rule 2 makes this expensive content to publish. Every comparison needs a mechanism explanation
written and sourced, which is a genuine editorial burden and the main cost of keeping the feature.

The material will still be quoted out of context. The rules reduce the damage and cannot eliminate
it; publishing it at all is a deliberate acceptance of that residual risk.

## Alternatives considered

**Keep as originally written.** Straightforward and would have produced exactly the race-fact
framing that is both unsound and damaging.

**Drop population comparison entirely.** Lowest risk, and arguably loses little given how large
individual variation is relative to group means. Rejected because the phenomenon is real and the
platform's premise is realism.

**Keep with evidence gating but no mechanism requirement.** Honest about uncertainty, and a bare
region-stratified number with an interval still reads as a fact about a group. The mechanism
requirement is what turns it into explanation.

## References

- User direction, 2026-09-16, on ethnic comparison (paraphrased): take the last option offered,
  with careful wording. The aim is not to attribute traits to an origin; evolution is driven
  mostly by region and sun exposure, and the differences follow from that.
- `MASTER_CONCEPT.md` §4 (recovered draft): "Ethnische & statistische Vergleiche"
- Veale D, Miles S, Bramley S, Muir G, Hodsoll J. *Am I normal? A systematic review and
  construction of nomograms for flaccid and erect penis length and circumference in up to 15 521
  men.* BJU Int 2015;115(6):978–986. doi:10.1111/bju.13010, PMID 25487360 — measured by health
  professionals to a standard procedure, minimum 50 participants per sample
- *A Systematic Review and Meta-Analysis of Penis Length and Circumference According to WHO
  Regions.* PMC11923605 — stratified by WHO region rather than racial category
- `docs/concept/l1-core/statistics.md` — `OQ-016`, `OQ-017`
