# simulation

> **Layer:** L2 Intelligence · **Owner:** planned Rust `crates/embodied-sim`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

Predict fit, comfort and experience — for a single body and for a pairing — and say how much the
prediction is worth.

This is the concept's intellectual core and the part the recovered draft reduced to four words. It
is built at full ambition: **geometric, biomechanical and statistical together**, because each
alone is inadequate.

| Layer | What it contributes | What it cannot do alone |
| :--- | :--- | :--- |
| **Geometric** | Dimensional relationships — length, girth, depth, angle, accommodation envelope | Treats tissue as rigid, which it is not |
| **Biomechanical** | Tissue compliance, distension, pressure distribution, accommodation over time | Needs parameters the published literature largely does not contain |
| **Statistical** | Outcome distributions from comparable pairings via [`body-vector`](body-vector.md) neighbourhoods | Needs reported outcomes, which do not exist on day one |

The three are composed, not chosen between. Geometry provides structure, biomechanics provides
response, and the statistical layer corrects both against reality as
[`learning`](learning.md) accumulates it. Early on the geometric layer dominates and the model
says so; as outcomes arrive, the statistical layer takes weight.

## The honesty requirement

§1 states that simulation is orientation, not a promise. That principle has to be mechanical:

1. Every result carries an **interval**, never a point value.
2. Every result carries the **verification grade of its inputs**. A prediction from two
   self-reported measurements is labelled as such, prominently.
3. Every result carries its **model composition** — how much came from geometry, how much from
   biomechanics, how much from observed outcomes.
4. Where the model is extrapolating beyond its evidence, it **says so and declines** rather than
   producing a confident-looking number. `OQ-025` applies: an interval too wide to be useful is a
   correct answer, and must be rendered as one.

A simulation output that looks like a verdict has misled the user, whatever the disclaimer said.

## Biomechanical parameters

The known hard problem. Tissue compliance and accommodation parameters are not available at
population scale, which means the biomechanical layer starts with a small number of literature-
derived parameters and wide priors, and is refined by outcome data.

This is the principal reason the statistical layer is not optional: it is what converts a
physically plausible but under-parameterised model into a calibrated one.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `model_version` | Versioned composition of geometric, biomechanical and statistical layers. |
| `parameter_set` | Biomechanical parameters with their provenance — literature-derived or prior. |
| `simulation_result` | Output with interval, input verification grades and model composition. |
| `pairing` | A consented relation between two feature sets. Both-party consent is a precondition. |

A result stores the model version that produced it. Recomputing under a newer model produces a new
result rather than silently changing an old one — the same versioning discipline as
[`body-vector`](body-vector.md).

## Interfaces

- **Provides:** single-body simulation, pair simulation, envelope computation, confidence
  reporting.
- **Consumes:** [`measurement`](../l1-core/measurement.md), [`anatomy`](../l1-core/anatomy.md),
  [`verification`](../l1-core/verification.md), [`body-vector`](body-vector.md),
  [`knowledge-graph`](knowledge-graph.md), [`statistics-engine`](statistics-engine.md).
- **Consumed by:** [`visualizer`](../l3-expression/visualizer.md),
  [`embodiment`](../l4-presence/embodiment.md), [`learning`](learning.md).

Geometry is shared with [`visualizer`](../l3-expression/visualizer.md) — the same parametric model
compiled to WASM renders client-side and computes server-side, so that what a person is shown and
what the platform computed cannot diverge.

## Consent surface

Pair simulation is the sharpest consent question on the platform: one output, two subjects, and a
result that discloses something about both. Consent is required from both parties for a pairing to
be computed, and `OQ-006` asks what happens when one withdraws afterwards.

A pair simulation must never be computable against a profile that has not agreed to be paired.
Running one "privately" against someone else's public measurements is exactly the use this
subsystem must be structurally incapable of.

## Open questions

- `OQ-026` — Which biomechanical parameters are literature-derivable, and which are pure prior?
  The coverage map from [`reference`](../l1-core/reference.md) should extend to model parameters.
- `OQ-027` — How is the model-composition weighting decided, and is it visible to the user or only
  reported?
- `OQ-006` — Withdrawal semantics for a jointly-held pair result.
