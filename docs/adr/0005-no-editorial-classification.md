# ADR-0005: No editorial content classification; descriptors with integrity watching

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

The recovered concept stated in §0 that pornographic content from private individuals was
permitted, and in §1 that pornography is expression rather than a special case. These contradict
each other: granting permission for something *is* treating it as a special case requiring
permission.

The deeper problem is that the porn / medical / educational / artistic boundary does not survive
contact with real content. A well-lit anatomical photograph will be called pornography by someone
regardless of intent, and a piece of pornography may be the most accurate anatomical reference a
person has seen. A platform whose entire subject is human bodies and sexuality would be making that
call constantly, arbitrarily, and to no one's benefit.

But §11A promises protection from exposure, and users legitimately need to control what they
encounter. Refusing to classify does not remove that need — it relocates it.

## Decision

**The platform makes no editorial classification of content.** It describes, and lets viewers
choose.

Four mechanisms together:

1. **Uploader descriptors** — neutral anatomical and situational terms for what is depicted.
2. **Assisted tagging** — a classifier proposes descriptors on upload; the uploader confirms or
   corrects. It proposes, never decides.
3. **One legal gate** — a single binary flag existing solely to satisfy age-gating law where
   required, explicitly a legal artifact with no editorial meaning.
4. **Context-scoped spaces** — content lives in a space whose kind sets expectation, independently
   of per-item descriptors.

Because descriptors are the only fine-grained control surface, **tag integrity is a safety system**.
Mis-tagging is actively detected — via classifier disagreement, viewer reports, filter-escape
patterns and uploader history — and deliberate mis-tagging to reach viewers who excluded that
content is treated as a consent violation, not a metadata error.

## Consequences

The platform never has to rule on what content *is*, which removes an unwinnable and endlessly
contested judgement, and keeps §1 internally consistent.

Moderation becomes narrow and defensible: consent violations, tag integrity failures, legal
obligations. Nothing about taste.

Costs: the entire protective burden of §11A rests on descriptors being accurate, which makes tag
integrity load-bearing infrastructure rather than metadata hygiene. This is more work than a
classification system, not less.

The assisted classifier must run over the most sensitive material the platform holds, which
constrains where inference may happen — `OQ-039`.

The controlled vocabulary itself encodes judgements about what is worth distinguishing. A careless
vocabulary reintroduces categorisation at the level below — `OQ-038`.

Filter defaults for new accounts are genuinely awkward: restrictive defaults protect and also
decide for the user what they should not see, which is close to the judgement just declined —
`OQ-040`.

## Alternatives considered

**Platform classifies explicit / non-explicit.** Conventional and operable, and it is exactly the
editorial judgement this ADR rejects, applied to a domain where the boundary is least meaningful.

**Descriptors alone, no assistance, no legal flag, no spaces.** Purest form and too fragile —
depends entirely on uploader diligence, with no coarse fallback when tags fail.

**Context-scoped spaces alone, no per-item descriptors.** Robust and too coarse for meaningful
viewer control within a space.

## References

- User direction, 2026-09-16 (paraphrased): the recovered concept is mistaken on this point.
  Pornographic content is permitted and is not the issue; a well-made medical image will be called
  pornography by some viewers regardless, so the distinction is not worth drawing.
- User decision, 2026-09-16, labelling (paraphrased): combine all of the proposed labelling
  mechanisms and watch for false tagging automatically. If tags are the only control, they have to
  stay clean and correct.
- `MASTER_CONCEPT.md` §0 (recovered draft): "Pornografische Inhalte von Privatpersonen sind
  erlaubt. Consent ist die einzige harte Grenze."
- `MASTER_CONCEPT.md` §1 (recovered draft): "Porn ist Ausdruck, kein Sonderfall"
- `docs/concept/l3-expression/tagging.md` — `OQ-038`, `OQ-039`, `OQ-040`
