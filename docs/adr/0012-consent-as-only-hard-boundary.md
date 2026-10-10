# ADR-0012: Consent as the only hard boundary, bound to artifacts

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

The recovered concept declared consent the only hard boundary, and then described it as a feature —
a section listing consent levels, visibility rights and moderation, alongside fifteen other
sections describing other features.

That arrangement cannot hold. ADR-0005 removes editorial classification entirely, which means the
platform has no content-based control. If consent is the only rule, it has to be the only rule that
is *structurally enforced*, or the platform has no enforced rules at all.

The failure mode to avoid is specific and common: consent as a policy checked at request time. In
that design, an artifact is neutral and access is judged at the door — which means every new
endpoint, background job, cache, export path or derived artifact is a fresh opportunity to forget
the check, and forgetting it fails open.

## Decision

**Consent is bound to the artifact, not checked at the door.**

An artifact carries the terms under which it may be seen. Every path that could surface it resolves
those terms. There is no ingest path producing an unbound artifact "to be configured later",
because that is the path by which unbound artifacts get served.

Concretely:

1. **Binding at creation.** Nothing is stored without its consent grant.
2. **Derived artifacts inherit and are enumerated.** Transcodes, thumbnails, embeddings, graph
   edges, avatars, exports and caches are enumerated against their parent so that revocation has a
   complete list to act on.
3. **Resolution is unconditional and cheap.** If checking consent is expensive, some path will
   eventually skip it — so the cost of the check is itself a safety property.
4. **Scope is applied inside queries, not to results.** Post-filtering has already read what it
   removes, and counts, ranking and timing leak.
5. **Records are append-only.** A revoked grant is superseded, not deleted, because "was this
   permitted when it was shown" must remain answerable.
6. **Revocation propagates to derived data.** Every module holding derived data owes `consent` a
   deletion path.
7. **Operators are not exempt.** Privileged access is scoped, justified, externally audited and
   bounded.

Moderation, consequently, is narrow: it enforces consent, tag integrity and legal obligation, and
rules on nothing else.

## Consequences

The platform's single stated rule becomes mechanically enforced rather than aspirational, which is
what makes the refusal to classify content survivable — the consent attached to an artifact carries
the whole weight.

Moderation becomes resolution of something already recorded rather than adjudication of something
ambiguous, so the genuinely contested queue should be small. If it is large, the consent model
upstream is underspecified — a useful diagnostic.

Costs: every module must answer the derived-data deletion question, which is real work and is why
each module page carries a consent surface section. Enumeration of derivatives is bookkeeping that
must not be skipped.

Point 4 constrains query design throughout and is the most likely rule to be violated by an
otherwise reasonable implementation.

Two questions remain genuinely open. Whether revoking an experience report retracts its
contribution to a trained model, or only its displayable form — `OQ-005`, where retraining on
withdrawal is expensive and not retraining means withdrawn data still shapes predictions. And
whose consent governs a pair simulation, which has one output and two subjects — `OQ-006`.

## Alternatives considered

**Consent as request-time policy.** Conventional, simpler, and fails open on every forgotten path.
Rejected as the exact failure this ADR exists to prevent.

**Consent plus content-based restrictions as a second line of defence.** Would reintroduce the
editorial classification removed in ADR-0005, through enforcement rather than labelling — the more
damaging version, because it would be invisible.

## References

- `MASTER_CONCEPT.md` §0 (recovered draft): "Consent ist die einzige harte Grenze."
- `MASTER_CONCEPT.md` §1 (recovered draft): "Consent > Moral > Geschmack"
- `MASTER_CONCEPT.md` §10 (recovered draft): "Consent-Level / Sichtbarkeitsrechte / Moderation"
- ADR-0005 — no editorial classification, which makes consent load-bearing
- `docs/concept/l1-core/consent.md` — `OQ-005`, `OQ-006`
