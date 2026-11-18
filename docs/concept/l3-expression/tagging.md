# tagging

> **Layer:** L3 Expression · **Owner:** planned Go `internal/tagging`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet) · **ADR:**
> [0005](../../adr/0005-no-editorial-classification.md)

## Purpose

Let people control what they see, on a platform that refuses to rule on what anything *is*.

emBodied makes no pornographic / medical / educational / artistic judgement. That boundary does not
survive contact with reality — a well-lit anatomical photograph will be called pornography by
someone regardless of intent. So the platform describes rather than classifies, and viewers
compose their own filters from descriptors.

The consequence is severe and has to be faced directly: **descriptors are the only control surface
there is.** §11A promises protection from exposure, and with classification refused, that promise
rests entirely on tags being accurate. Tag integrity is therefore a safety system, not metadata
hygiene.

## Four mechanisms, together

The concept uses all of the available approaches rather than choosing one, because each covers a
different failure:

1. **Uploader descriptors.** Neutral anatomical and situational terms describing what is depicted.
   The uploader knows best; the uploader is also inconsistent and sometimes careless.
2. **Assisted tagging.** A classifier proposes descriptors on upload, which the uploader confirms
   or corrects. Covers uploader diligence. Is inevitably wrong sometimes, so it proposes and never
   decides.
3. **One legal gate.** A single binary flag existing solely to satisfy age-gating law where
   required. The platform states explicitly that this flag is a legal artifact with no editorial
   meaning — it is not a judgement about the content, it is a jurisdictional compliance marker.
4. **Context-scoped spaces.** Content lives in a [`space`](../l5-community/spaces.md) — education,
   experience, expression — and the space sets expectation independently of per-item descriptors.
   Coarse, robust, and it keeps working when tags fail.

Together: the space sets a floor, descriptors refine within it, assistance improves coverage, and
the legal flag satisfies law without pretending to be an opinion.

## Tag integrity

Because tags carry the whole burden, mis-tagging must be **actively detected rather than assumed
away**. This is the part of the module that is easy to leave for later and must not be.

| Signal | What it catches |
| :--- | :--- |
| Classifier disagreement | Uploader descriptors far from what the assisted model proposes |
| Viewer reports | Content surfacing through filters it should not have matched |
| Filter-escape detection | Systematic patterns of content reaching viewers who excluded it |
| Uploader history | Repeated divergence, distinguishing carelessness from deliberate evasion |

Detection routes to [`moderation`](moderation.md) for enforcement. Deliberate mis-tagging to reach
viewers who excluded that content is a consent violation — it defeats the only protection §11A
offers — and is treated as one rather than as a metadata error.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `descriptor` | Controlled vocabulary term. Neutral, anatomical or situational. |
| `assignment` | Descriptor on an asset, with source: uploader, assisted, corrected. |
| `legal_flag` | The single jurisdictional gate marker. |
| `filter` | A viewer's composed inclusion and exclusion set. Private. |
| `integrity_signal` | Evidence of possible mis-tagging, and its disposition. |

## Interfaces

- **Provides:** describe, propose, filter evaluation, integrity signalling.
- **Consumes:** [`media`](media.md), [`spaces`](../l5-community/spaces.md),
  [`moderation`](moderation.md).
- **Consumed by:** [`media`](media.md) delivery, [`search`](../cross-cutting/search.md),
  [`spaces`](../l5-community/spaces.md).

## Consent surface

A viewer's filter is private. What a person chooses not to see discloses a great deal about them,
and filters must never be visible to uploaders, to other viewers, or used for recommendation.

The vocabulary itself carries risk: a controlled vocabulary encodes assumptions about what is worth
distinguishing, and a careless one reintroduces exactly the categorisation the platform refused at
the level above. Vocabulary design is a first-class task, not a data-entry exercise.

## Open questions

- `OQ-038` — Who owns the controlled vocabulary and how does it change? An uncontrolled vocabulary
  makes filters unreliable; an over-controlled one cannot describe what people actually post.
- `OQ-039` — What does the assisted classifier run on, given it must process exactly the most
  sensitive material the platform holds? On-platform inference is the obvious answer and needs
  stating as a constraint.
- `OQ-040` — Filter defaults for a new account: restrictive defaults protect and also decide for
  the user what they should not see, which is close to the editorial judgement the platform
  declined.
