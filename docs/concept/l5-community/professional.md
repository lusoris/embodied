# professional

> **Layer:** L5 Community · **Owner:** Go `internal/professional`
> **Added by:** gap pass — closes recovered §12 "Erweiterte Nutzung"

## Purpose

Support people who use emBodied as part of their work — clinicians, therapists, sex educators,
researchers — without creating a class of user with privileged access to other people's bodies.

The recovered concept listed "Professionals" as a bullet under extended use and said nothing more.
It is a real use case: the platform's statistical and educational material is directly useful to
someone counselling a patient anxious about their body, and the reference catalogue is useful to a
researcher. Both are served by content the platform already produces.

## The hard constraint

**Professional status confers no additional access to user data. None.**

This is the entire design. A therapist, clinician or researcher on emBodied sees exactly what any
other user sees, subject to exactly the same consent resolution. There is no professional view, no
patient roster, no research cohort drawn from platform users, no elevated read.

The reasoning is that a professional tier with data access would be the most attractive attack
surface on the platform and the easiest to claim falsely — and verifying a professional credential
means holding identity documents, which ADR-0004 declined to do for exactly this class of reason.

What professional status may confer:

| May confer | May never confer |
| :--- | :--- |
| Citable export of reference data and coverage maps | Access to any user's body data |
| Attribution as a contributor to education material | A view of another person's profile |
| Bulk access to the published reference catalogue | Ability to invite, assess or manage another user |
| A stated role on a profile, self-described | Standing in moderation or verification |

A self-described professional role is exactly that — self-described, like every other role under
§3. The platform does not vouch for it, and must not display it in a way that implies it does.

## Research

Researchers are served by the reference repository, which is public, citable and versioned — and
by the coverage map, which is arguably more useful to a researcher than the data, since it states
where measured evidence does not exist.

Research on *platform users* is out of scope. The overlay described in
[`statistics`](../l1-core/statistics.md) is a display artifact, not a recruitable cohort, and there
is no mechanism for contacting users about a study.

## Creators

The recovered §12 also listed creator options. The **creator role** is in scope here: a person may
publish media, be followed, and have their work surfaced. Creator *earnings* are part of
monetisation and are deferred with the rest of the roadmap under `OQ-001`.

§7 of the recovered concept is explicit that there is no creator obligation, and that holds: the
platform must be fully usable by someone who publishes nothing.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `professional_role` | Self-described. Display only. Confers no access. |
| `catalogue_export` | Citable bulk export of reference data. No user data, ever. |
| `contribution` | Attribution for education material authored. |

## Interfaces

- **Provides:** role declaration, reference catalogue export, contribution attribution.
- **Consumes:** [`reference`](../l1-core/reference.md), [`education`](education.md),
  [`identity`](../l1-core/identity.md).
- **Consumed by:** nothing that grants access. This module deliberately has no consumers in the
  authorisation path.

## Consent surface

Minimal, because the module holds no user data and grants no access to any. Its consent relevance
is preventative: the absence of a professional access path is a property that must be actively
maintained, since "just for clinicians" is the most plausible-sounding route by which such a path
would be introduced later.

## Open questions

- `OQ-075` — Is a professional role displayed at all, given the platform cannot verify it and
  displaying an unverified credential invites its misuse as a trust signal?
- `OQ-076` — Does the citable export need attribution or usage terms beyond the reference
  repository's CC BY-SA 4.0 licence?
