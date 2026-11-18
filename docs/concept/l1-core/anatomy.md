# anatomy

> **Layer:** L1 Core · **Owner:** planned Go `internal/anatomy`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet) · **ADR:**
> [0003](../../adr/0003-anatomy-first-feature-model.md)

## Purpose

Define what a body *is*, structurally, in a way that has no default case.

A profile is **a set of anatomical features**. Each feature carries its own measurement schema,
its own reference cohort and its own visualisation. Gender and identity are separate social
attributes that never gate which features a person may record.

This is simultaneously the inclusive model and the technically correct one, which is why it was
chosen over gendered profile types with variant handling. Under a gendered model, every intersex,
trans or post-surgical body is structurally a deviation — and a platform whose first principle is
"bodies are real, not idealised" cannot encode an ideal into its schema and expect the principle
to survive. Under the feature model there is nothing to deviate from.

It is also the only model in which pair simulation composes cleanly: a pairing is a relation
between feature sets, and needs no rule about which kinds of body may be paired.

**Presets** keep this usable. Common configurations are offered at signup so that ordinary use is
not a schema exercise. A preset is a starting point — freely editable, removable, never a
constraint, and never displayed as the correct answer.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `feature_type` | Catalogue entry: what can be recorded, and with what schema. |
| `feature_instance` | A feature present on a profile, with its state and history. |
| `preset` | A named starting set of feature types. Metadata only; confers nothing. |
| `feature_state` | Present, absent, post-surgical, in transition. A first-class property. |

`feature_state` matters more than it looks. A body changes — surgically, hormonally, with age. The
schema records state and history rather than assuming a static truth, which also makes §9 personal
progress expressible without competition.

## Interfaces

- **Provides:** feature catalogue, profile composition, preset application, schema resolution.
- **Consumes:** [`identity`](identity.md), [`consent`](consent.md).
- **Consumed by:** [`measurement`](measurement.md) (which schema applies),
  [`statistics`](statistics.md) (which cohort applies),
  [`visualizer`](../l3-expression/visualizer.md) and [`avatar`](../l3-expression/avatar.md)
  (what to render), [`simulation`](../l2-intelligence/simulation.md) (what can be paired).

## Consent surface

Feature presence is itself sensitive — that a profile records a given feature can disclose more
than the measurement does. Visibility applies at feature granularity, and the absence of a feature
must be indistinguishable from its being hidden.

## Open questions

- `OQ-007` — What is the initial feature catalogue, and what is the process for extending it?
  An under-specified catalogue silently reintroduces a default body.
- `OQ-008` — How is history exposed? Showing change over time serves progress and self-knowledge;
  it also builds a record that could out someone. Default is closed, but the design needs stating.
