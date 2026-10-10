# emBodied for moderators

A **view** into the canonical concept. Where this disagrees with
[MASTER_CONCEPT.md](../MASTER_CONCEPT.md) or [moderation](../concept/l3-expression/moderation.md),
those win.

## Your mandate is narrow, deliberately

You enforce consent. That is the whole job.

**You act on exactly three things:**

1. **Consent violations** — content published without the depicted person's consent, content
   surviving a revocation, depiction claims that do not hold.
2. **Tag integrity failures** — deliberate mis-tagging that defeats viewer filters. This is a
   consent violation by another route: it puts content in front of someone who excluded it.
3. **Legal obligations** — material that must be removed regardless of consent, and the
   jurisdictional age gate.

**You do not act on anything else.** Not on how explicit something is, not on whether it is crude,
strange, distasteful or not to your taste. Those are filter questions and they belong to the
viewer. The platform makes no editorial judgement about what content *is*
([ADR-0005](../adr/0005-no-editorial-classification.md)), and moderation is not the back door
through which that judgement returns.

The grounds for action are a **closed set** (`rule`). If it is not listed, it is not grounds.
Adding one is a deliberate, visible change — never a moderator's discretion.

## Most cases are not judgement calls

Consent is bound to each artifact at creation, so "was this permitted?" is usually answerable from
the record rather than argued about. What reaches you as genuinely ambiguous — a contested
depiction claim, a disputed revocation, a mis-tagging pattern that might be carelessness — should
be a small queue.

If that queue is large, the consent model upstream is underspecified. Say so; it is a design
signal, not a staffing problem.

## What the platform owes you

You view the most sensitive material here, repeatedly, by job description. The design owes you the
same seriousness it owes users:

- **Minimum necessary exposure.** A case tells you what needs checking, not "look at everything".
- **No unbounded queues** of unclassified material.
- **Your views are logged** — every moderator view of an asset is recorded. This protects users and
  it protects you.

Moderator access is a standing exception to the platform's only real rule, and is treated as the
exception it is rather than as a perk of the role.

## Appeals

Both sides can appeal: the uploader whose content was removed, and the person whose consent was
allegedly violated. A one-sided appeal path favours whoever is already on the platform.

## Open questions that affect you

- `OQ-041` — who moderates at all, and how the wellbeing problem is handled
- `OQ-042` — the closed rule set must be written before launch, since its closure is the guarantee
- `OQ-035` — consent for a depicted person who is not a platform user
- `OQ-055` — whether live streams are recorded for moderation

See [OPEN-QUESTIONS.md](../design-basis/OPEN-QUESTIONS.md).
