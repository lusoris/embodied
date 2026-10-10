# emBodied for users

What the platform does, what it will not do, and what it holds about you.

This is a **view** into the canonical concept, not a second source. Where this page and
[MASTER_CONCEPT.md](../MASTER_CONCEPT.md) disagree, the concept wins.

## What you can do without an account

Everything educational. Read material, browse reference statistics, and use the visualizer against
reference distributions — with **your measurements never leaving your browser**.

You are not asked to register, and you should not be repeatedly prompted to. If you are, that is a
bug against [identity](../concept/l1-core/identity.md).

## What an account adds

Body data, media, texts, preferences and community presence — always under a pseudonym. It is a
deliberate step, and the platform must not attempt to link it to anything you did anonymously.

## What the platform promises

| Promise | Where it is enforced |
| :--- | :--- |
| Consent is the only hard rule, and it is bound to each thing you upload — not checked at the door | [consent](../concept/l1-core/consent.md), [ADR-0012](../adr/0012-consent-as-only-hard-boundary.md) |
| No judgement about whether your content is pornographic, medical or artistic | [tagging](../concept/l3-expression/tagging.md), [ADR-0005](../adr/0005-no-editorial-classification.md) |
| No default body — your anatomy is a set of features, not a type with variants | [anatomy](../concept/l1-core/anatomy.md), [ADR-0003](../adr/0003-anatomy-first-feature-model.md) |
| Every number comes with its sample size and uncertainty | [statistics](../concept/l1-core/statistics.md) |
| No rankings, no scores, no leaderboards, no streaks | [progress](../concept/l5-community/progress.md) |
| Nothing exists to lure you back — no engagement notifications | [notification](../concept/cross-cutting/notification.md) |
| Operators cannot routinely see your body data, media or reports | [admin](../concept/cross-cutting/admin.md) |

## What the platform will not claim

**Simulation is orientation, not a promise.** Predictions carry an interval and tell you how well
established their inputs were. A result built from two self-reported measurements says so.

**Where nobody has measured something properly, we say so** rather than filling the gap.

**Population differences are explained, not asserted.** Comparisons are by region and study cohort,
with the mechanism stated and with individual variation noted — because individual variation is far
larger than any group difference.

**Exported data has left.** We can stop future exports; we cannot recall a download.

**Live video cannot be unseen or made unrecordable.** We will not imply otherwise.

## Your controls

- **Visibility** is granular and defaults closed.
- **Filters** are yours, private, and never visible to anyone else or used to recommend.
- **Revocation** works, and propagates to derived things — thumbnails, embeddings, avatars.
- **Export, correction and deletion** are self-service, not support tickets.

## Things not decided yet

Payments, launch, jurisdiction and age verification are open. See
[OPEN-QUESTIONS.md](../design-basis/OPEN-QUESTIONS.md).
