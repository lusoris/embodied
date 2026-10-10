# consent

> **Layer:** L1 Core · **Owner:** Go `internal/consent` · **ADR:** [0012](../../adr/0012-consent-as-only-hard-boundary.md)

## Purpose

Consent is the platform's only hard boundary, which means it cannot be a policy document — it has
to be a running subsystem that other modules are structurally unable to bypass.

The design rule is that **consent is bound to the artifact, not checked at the door**. A photograph
does not become viewable because the request reached a permissive endpoint; it carries the terms
under which it may be seen, and every path that could surface it resolves those terms. Moderation
then becomes enforcement of something already recorded rather than after-the-fact judgement.

This is what makes the platform's refusal to classify content (see
[`tagging`](../l3-expression/tagging.md)) survivable. If the platform will not rule on whether
something is pornographic, the consent attached to it has to carry the entire weight.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `consent_grant` | Subject, artifact, scope, expiry, revocation state. Append-only. |
| `visibility_rule` | Who may see what, under which context and tier. Defaults closed. |
| `consent_receipt` | Immutable evidence of what was agreed, when, and in what wording. |
| `revocation` | Withdrawal is always available and always propagates. |

Consent records are append-only. A revoked grant is not deleted — it is superseded, because the
question "was this permitted at the time it was shown" must remain answerable.

## Interfaces

- **Provides:** grant, revoke, resolve-visibility, receipt lookup.
- **Consumes:** [`identity`](identity.md) for subject and tier.
- **Consumed by:** [`media`](../l3-expression/media.md), [`moderation`](../l3-expression/moderation.md),
  [`learning`](../l2-intelligence/learning.md), [`rooms`](../l4-presence/rooms.md),
  [`device`](../l4-presence/device.md), [`statistics`](statistics.md).

Resolution must be cheap enough to be unconditional. If checking consent is expensive, some path
will eventually skip it — so the cost of the check is a safety property.

## Consent surface

This module *is* the consent surface. Two obligations specific to it:

**Granularity without paralysis.** §3 demands granular visibility; a settings page with forty
toggles achieves granularity and destroys comprehension. Sensible composed defaults, with the
granular layer available beneath.

**Revocation propagates everywhere.** Withdrawn consent must reach derived artifacts — a
transcoded variant, a cached thumbnail, an avatar built from verified measurements, an embedding
computed from a report. Any module holding derived data owes this module a deletion path. This is
the single most likely place for the architecture to leak, and it is called out here so that every
module page has to answer it.

## Open questions

- `OQ-005` — Does revocation of an experience report retract its contribution to the learned
  model, or only to displayable data? Retraining on withdrawal is expensive; not retraining means
  a withdrawn report still shapes predictions. See [`learning`](../l2-intelligence/learning.md).
- `OQ-006` — Consent for pair simulation involves two people and one result. Whose consent governs
  the output, and what happens when one withdraws?
