# media

> **Layer:** L3 Expression · **Owner:** Go `internal/media`

## Purpose

Carry images, video and text — upload, transcode, store, deliver — with **consent bound to every
asset as a structural property**, not attached as metadata and hoped for.

The platform does not curate and does not classify. What it does is guarantee that nothing is
shown to anyone the uploader did not agree to show it to, and that withdrawal actually works. That
guarantee is this module's entire reason to exist; everything else here is plumbing.

There is no creator obligation. A person may use emBodied entirely without publishing anything —
§7 of the recovered concept was right about that, and it follows from the two-tier identity model.

## Consent binding

An asset is never stored without its consent grant. There is no ingest path that produces an
unbound asset "to be configured later", because that path is how unbound assets get served.

Every derived artifact — transcode, thumbnail, preview frame, extracted still — inherits the
binding and is enumerated, so that revocation has a complete list to act on. Derived media is the
most likely place for revocation to leak, and the enumeration exists specifically to close it.

Delivery resolves consent at request time. A signed URL that outlives a revocation is a revocation
that did not happen.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `asset` | Original upload, immutable, consent-bound from creation. |
| `derivative` | Transcode or extract. Enumerated against its parent for revocation. |
| `delivery_grant` | Short-lived, consent-resolved access to a specific asset. |
| `depiction_claim` | Who is depicted, and their consent — distinct from who uploaded. |

`depiction_claim` is the one that carries the platform's hardest guarantee. The uploader is not
necessarily the subject, and consent to publish belongs to the person depicted. An asset depicting
someone other than the uploader requires that person's consent, and the platform needs an answer
for the case where they are not a user — which is `OQ-035`.

## Interfaces

- **Provides:** upload, transcode, store, deliver, enumerate derivatives, revoke.
- **Consumes:** [`consent`](../l1-core/consent.md), [`identity`](../l1-core/identity.md),
  [`tagging`](tagging.md) for descriptors, [`moderation`](moderation.md) for enforcement.
- **Consumed by:** [`spaces`](../l5-community/spaces.md),
  [`education`](../l5-community/education.md), [`live`](../l4-presence/live.md),
  [`search`](../cross-cutting/search.md).

## Storage

Content-addressed, encrypted at rest, with the reference-data separation principle applying here
too: media never shares a store with reference material, and never shares a store with
verification evidence — which has a shorter retention and a different threat model entirely.

## Consent surface

This module is one of the two places (with [`learning`](../l2-intelligence/learning.md)) where the
platform holds material whose exposure would be seriously harmful. Its obligations:

- Consent bound at creation, never retrofitted.
- Derivatives enumerated, so revocation is complete.
- Delivery resolved per request, never pre-authorised beyond a short window.
- Depiction consent distinct from upload consent.
- Deletion means deletion, including from backups within a stated window — and the window is
  stated rather than left implicit.

## Open questions

- `OQ-035` — Consent for a depicted person who is not a platform user. Either the platform refuses
  such uploads, or it builds a claim-and-verify path that itself requires identifying a
  non-user. Both have real costs and one must be chosen.
- `OQ-036` — Backup and deletion window: how long until deletion is genuinely complete, and is
  that window acceptable to state publicly?
- `OQ-037` — Does the anonymous tier see any user media at all, or only reference and education
  material? This determines whether media delivery needs an unauthenticated path.
