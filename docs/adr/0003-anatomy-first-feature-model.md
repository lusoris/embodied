# ADR-0003: Anatomy-first, gender-independent feature model with presets

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

emBodied's first principle is that bodies are real rather than idealised, and the platform is
required to be inclusive. On a body-measurement platform, inclusivity is not a policy statement —
it is a schema decision, made once, and very expensive to reverse.

The choice is whether a profile has a *type* (with variants for bodies that do not fit it) or a
*composition* (with no type at all). Under a typed model, every intersex, trans and post-surgical
body is structurally a deviation from a default. That encodes an ideal into the schema, which
contradicts the first principle directly and would surface in every downstream feature — which
measurements are offered, which reference cohort applies, what the visualizer renders.

There is also a technical consequence. Pair simulation must relate two bodies. Under a typed model
this requires rules about which types may be paired; under a composition model a pairing is simply a
relation between feature sets and needs no such rule.

## Decision

A profile is **a set of anatomical features**. Each feature carries its own measurement schema, its
own reference cohort and its own visualisation. Gender and identity are separate social attributes
that never gate which features a person may record.

`feature_state` — present, absent, post-surgical, in transition — is a first-class property, and
features carry history rather than assuming a static truth.

**Presets** make this usable: common configurations are offered at signup as starting points.
A preset confers nothing, constrains nothing, is freely editable, and is never presented as the
correct answer.

## Consequences

Intersex, trans and post-surgical bodies need no special case, because there is no default case.
The inclusivity requirement is satisfied structurally rather than by accommodation.

Pair simulation composes cleanly. Feature state and history make personal change expressible, which
`progress` needs.

Costs: the schema is more abstract than a typed model, and signup would be an unpleasant
configuration exercise without presets — so presets are load-bearing rather than convenience.

The feature catalogue becomes a significant design artifact. An under-specified catalogue
reintroduces a default body through the back door, by making some bodies easy to describe and
others awkward. Recorded as `OQ-007`.

Feature history is disclosive — for a trans user, a trajectory is a record of transition.
Visibility must apply at feature granularity, and absence must be indistinguishable from
concealment. Recorded as `OQ-008`.

## Alternatives considered

**Gendered profile types with variant handling.** Simpler for the common case and familiar to
users. Rejected: every variant is structurally a deviation, which is precisely what the platform
says it is against, and it forces pairing rules that the feature model does not need.

**Anatomy-first with no presets.** Purest form of the model and a poor first experience — signup
becomes a schema exercise. Presets were added specifically to avoid this.

## References

- User decision, 2026-09-16, anatomy model (paraphrased): anatomy-first, with presets.
- User direction, 2026-09-16, on requirements (paraphrased): license under EUPL, conform fully to
  the adopted standards, be inclusive, and keep a professional register while remaining openly
  erotic in intent.
- `MASTER_CONCEPT.md` §1 (recovered draft): "Körper sind real, nicht idealisiert"
- `MASTER_CONCEPT.md` §3 (recovered draft): "Körperdaten, Medien, Texte, Präferenzen / Rollen:
  sexuell, psychologisch, sozial, kontextuell"
- `docs/concept/l1-core/anatomy.md` — `OQ-007`, `OQ-008`
