# education

> **Layer:** L5 Community · **Owner:** planned Go `internal/education`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

Answer the questions people are too embarrassed to ask, without requiring them to identify
themselves to ask.

This is §11A, and it is the module with the strongest claim to being the reason the platform
should exist. The core statistical capability — here is what bodies actually look like, here is
where you fall, here is the uncertainty — is genuinely useful to people who have been told
otherwise by pornography, advertising and playground mythology.

**Anonymous-tier reachable by design.** The people who most need to know what an ordinary body
looks like are the least willing to expose their own, and a platform that demands a profile before
answering has failed exactly the population it would help most. This constraint propagates
downward: it is why [`visualizer`](../l3-expression/visualizer.md) must render client-side against
reference distributions, and why [`statistics`](../l1-core/statistics.md) must be queryable without
a subject.

## What education material must carry

Everything this module publishes inherits the platform's honesty commitments, because material
that gets quoted, screenshotted and believed is exactly where overstatement does damage:

1. Claims are sourced to [`reference`](../l1-core/reference.md), with the citation visible.
2. Figures carry sample size, protocol and interval — the `presentation_contract` applies here as
   much as to a chart.
3. Where evidence is thin or absent, the material says so. The coverage map is educational content
   in its own right: "nobody has measured this properly" is a true and useful answer.
4. Individual variation is stated wherever a group figure appears.
5. Nothing is framed as a norm to meet. Distributions describe; they do not prescribe.

Point 5 is the one that takes active defence. A percentile chart is a comparison device, and on a
platform about bodies, comparison slides into evaluation unless the presentation resists it.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `article` | Educational material, versioned, sourced. |
| `claim_binding` | Links a statement to the reference source supporting it. |
| `question` | Anonymously askable; answers become material. |
| `coverage_note` | An explicit statement of what is not known. |

## Interfaces

- **Provides:** material retrieval, claim sourcing, anonymous question intake.
- **Consumes:** [`reference`](../l1-core/reference.md), [`statistics`](../l1-core/statistics.md),
  [`spaces`](spaces.md), [`media`](../l3-expression/media.md),
  [`live`](../l4-presence/live.md) for education channels.
- **Consumed by:** [`search`](../cross-cutting/search.md), the anonymous tier directly.

## Consent surface

Minimal by construction, which is the point. Anonymous reading leaves no subject, and anonymous
questions must be genuinely unattributable — not merely displayed without a name.

A question is often more disclosing than an answer. Someone asking about a specific anatomical
concern has revealed something, and the platform must not accumulate those into a profile of an
anonymous session. Question intake is deliberately amnesic.

## Open questions

- `OQ-061` — Who writes the material, and what review does a claim get before publication? Sourced
  claims are only as good as the sourcing, and this is medical-adjacent content that people will
  act on.
- `OQ-062` — Where is the boundary with medical advice? The platform describes distributions; it
  must not diagnose, and the line between "you are in the 3rd percentile" and a clinical
  implication is thinner than it looks.
- `OQ-063` — Anonymous questions are an abuse vector as well as a safety feature. What limits
  exist that do not require identifying the asker?
