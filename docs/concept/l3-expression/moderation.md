# moderation

> **Layer:** L3 Expression · **Owner:** planned Go `internal/moderation`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

Enforce consent. That is the whole mandate, and stating it narrowly is the point.

On a platform that refuses editorial classification, moderation is **not** a taste committee and
not a content-quality function. It does not decide whether something is too explicit, too crude or
too strange. It acts on exactly three things:

1. **Consent violations** — content published without the depicted person's consent, content
   surviving a revocation, depiction claims that do not hold.
2. **Tag integrity failures** — deliberate mis-tagging that defeats viewer filters, routed from
   [`tagging`](tagging.md). A consent violation by another route: it puts content in front of
   someone who excluded it.
3. **Legal obligations** — material the platform is required to remove regardless of consent, and
   the jurisdictional age gate.

Everything else is a filter question, and belongs to the viewer.

This narrowness is what makes moderation compatible with §1. A moderation function that ruled on
what content *is* would smuggle the classification the platform rejected back in through
enforcement, and it would be the more damaging version because it would be invisible.

## Enforcement, not judgement

Because [`consent`](../l1-core/consent.md) binds terms to artifacts at creation, most moderation is
resolution of something already recorded rather than adjudication of something ambiguous. "Was
this permitted?" is usually answerable from the consent record.

The residue that is genuinely ambiguous — a contested depiction claim, a disputed revocation, a
mis-tagging pattern that might be carelessness — is where human judgement goes, and that queue
should be small. If it is large, the consent model upstream is underspecified.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `case` | A reported or detected issue, its evidence, and its disposition. |
| `action` | What was done, by whom, under which rule. Append-only. |
| `appeal` | Challenge to an action, and its outcome. |
| `rule` | The enumerated grounds for action. Closed set — if it is not listed, it is not grounds. |

`rule` being a closed set is the structural guarantee against mandate creep. Adding a ground is a
deliberate, visible change, not a moderator's discretion.

## Interfaces

- **Provides:** report intake, case handling, enforcement, appeal.
- **Consumes:** [`consent`](../l1-core/consent.md), [`media`](media.md),
  [`tagging`](tagging.md) integrity signals, [`identity`](../l1-core/identity.md).
- **Consumed by:** [`admin`](../cross-cutting/admin.md), [`rooms`](../l4-presence/rooms.md),
  [`live`](../l4-presence/live.md).

## Moderator exposure

Moderators view the most sensitive material on the platform, repeatedly, by job description. The
design owes them the same seriousness it owes users:

- Minimum necessary exposure — the case says what needs checking, not "look at everything".
- No unbounded queues of unclassified material.
- Every moderator view of an asset is itself logged, because access to this content is a
  privilege that must be auditable.

Moderator access is a standing consent exception and should be treated as the exception it is. A
platform whose only real rule is consent cannot be casual about the one role that routinely sees
past it.

## Consent surface

Moderation reads material its subjects did not consent to share with moderators. That is
unavoidable and is therefore made explicit in the consent wording at upload rather than buried:
people should know that a consent dispute can be reviewed.

Appeals are available to both sides — the uploader whose content was removed, and the person whose
consent was allegedly violated. A one-sided appeal path favours whoever is already on the platform.

## Open questions

- `OQ-041` — Who moderates? A solo or small operator reviewing this material at volume is a
  serious wellbeing problem, and outsourcing means handing the platform's most sensitive assets to
  a third party.
- `OQ-042` — What is the closed rule set, precisely? It must be written before launch, since its
  closure is the guarantee.
- `OQ-035` — Non-user depiction consent, shared with [`media`](media.md), lands here for
  enforcement.
