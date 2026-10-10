# spaces

> **Layer:** L5 Community · **Owner:** Go `internal/spaces`

## Purpose

Provide context. A space sets what a person should expect to encounter, independently of per-item
descriptors.

The recovered concept had themed rooms, learning rooms and experience rooms as three separate
section bullets. They are one mechanism: **a bounded context with an expectation attached**.

| Space kind | Expectation |
| :--- | :--- |
| **Education** | Material intended to inform. Reachable from the anonymous tier. |
| **Experience** | People describing what happened to them. Personal, not instructional. |
| **Expression** | Media and presentation of self. |

The kinds are expectations, not classifications — a space does not rule on what its content *is*,
it tells you what you are walking into. That distinction is what keeps spaces compatible with
[ADR-0005](../../adr/0005-no-editorial-classification.md).

## Why context matters alongside tags

[`tagging`](../l3-expression/tagging.md) carries the fine-grained control surface and is,
necessarily, fallible — it depends on uploader diligence, classifier accuracy and integrity
watching. Spaces are the coarse layer that keeps working when tags fail.

A person in an education space who encounters something they did not expect has been failed by
tags; a person who wandered into an expression space has not been failed by anything. Spaces make
the difference between those two cases legible, which is what lets tag-integrity signals mean
something.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `space` | Kind, description, expectation, membership model, tier access. |
| `membership` | Who participates, at what tier, with what standing. |
| `space_policy` | Filter floor, retention, whether anonymous-tier readable. |
| `placement` | An artifact's space, which composes with its descriptors. |

## Interfaces

- **Provides:** space resolution, placement, membership, expectation reporting.
- **Consumes:** [`identity`](../l1-core/identity.md), [`consent`](../l1-core/consent.md),
  [`tagging`](../l3-expression/tagging.md), [`media`](../l3-expression/media.md),
  [`live`](../l4-presence/live.md).
- **Consumed by:** [`education`](education.md), [`search`](../cross-cutting/search.md),
  [`moderation`](../l3-expression/moderation.md).

A space's filter floor composes with a viewer's filter. The floor may be more restrictive than a
viewer's settings; it may never be less. A space cannot opt its members out of their own filters.

## Consent surface

**Membership is disclosive.** That a person is in a given space says something about them, often
more than anything they post there. Membership visibility is therefore a per-space property that
defaults closed, and a space must be able to have members whose presence is visible to nobody.

**The floor composes, it never overrides.** A space's filter floor may be more restrictive than a
viewer's own settings and may never be less. A space cannot opt its members out of their own
filters.

**Protected spaces.** §11A requires spaces where participation does not create exposure. These are
a property of the space rather than a separate module: anonymous-tier readable, no membership
disclosure, no presence signalling, retention-limited.

The people who most need these spaces are the least able to risk being seen in them, which means
the protection has to be structural — a protected space that quietly records who read what has
protected nobody.

## Open questions

- `OQ-058` — Are the three kinds fixed, or may spaces be created with new expectations? User-created
  spaces are the obvious growth path and they make the expectation contract unenforceable.
- `OQ-059` — How does a person move between spaces without the transition itself disclosing
  something? Moving from education to expression is a signal, if anyone is watching.
- `OQ-060` — Does `spaces` subsume [`live`](../l4-presence/live.md) channels, or do channels live
  inside spaces? Overlap flagged for the deduplication pass.
