# social-vr

> **Layer:** L4 Presence · **Owner:** unassigned · **Status:** Long-term goal, not designed

## Purpose

Open, persistent shared space where people move as their verified real bodies, meet, talk and
interact.

This is the stated long-term ambition. It is recorded here as a destination so that the modules
below it are built in a direction that can reach it — and it is **explicitly not designed in this
pass**, because designing it now would be guessing.

## Why it is deferred

Honest accounting: this is by a wide margin the largest module on the platform. It is a networked
multiplayer engine with persistence, presence, avatars, physics, spatial voice, discovery and
moderation at scale — each of which is a substantial system, and all of which must work together
under the platform's consent model.

It is also the module whose requirements are least knowable in advance. Nearly everything that
determines its design — how the avatar pipeline performs at scale, whether verified real bodies
change how people behave in shared space, what safety problems arise between people who are not
pretending to be someone else — is answered by [`embodiment`](embodiment.md) and
[`rooms`](rooms.md) first.

Building it before those answers exist would produce a world designed around assumptions nobody
has tested.

## What must be true before it is designed

| Precondition | Owner |
| :--- | :--- |
| Avatar fidelity is good enough that people accept it as themselves | [`avatar`](../l3-expression/avatar.md) |
| Authenticity grading is meaningful and legible to other participants | [`verification`](../l1-core/verification.md), `OQ-050` |
| Multi-party consent composition works in practice, not just on paper | [`rooms`](rooms.md) |
| Moderation has a workable answer for real-time embodied interaction | [`moderation`](../l3-expression/moderation.md), `OQ-041` |
| Discovery can exist without destroying the invitation model's safety properties | this module |

The last is the genuine open problem. [`rooms`](rooms.md) is safe largely *because* there is no
discovery — invitation is its access control. Open social space removes that, and needs a
replacement that is not simply "moderate harder".

## Direction constraints on modules built now

So that this remains reachable:

- [`avatar`](../l3-expression/avatar.md) must produce avatars that work at distance and in motion,
  not only in close inspection.
- [`rooms`](rooms.md)'s per-scope grant model must not assume small participant counts in its data
  model, even though it assumes them in its safety model.
- [`device`](device.md)'s bounded-command interface must hold with parties who are not known to
  each other.
- [`consent`](../l1-core/consent.md) resolution must stay cheap enough to run per-interaction in
  real time.

These are the load-bearing ones. Meeting them costs little now and is expensive to retrofit.

## Owned data

**None yet, deliberately.** Inventing a schema for a system whose requirements are answered by
[`embodiment`](embodiment.md) and [`rooms`](rooms.md) would be guessing, and a guessed schema is
harder to discard than no schema.

The one constraint carried forward: [`rooms`](rooms.md)'s per-scope grant model must not assume
small participant counts in its **data model**, even though it assumes them in its safety model.

## Interfaces

**Not defined.** This module would consume [`avatar`](../l3-expression/avatar.md),
[`embodiment`](embodiment.md), [`device`](device.md), [`consent`](../l1-core/consent.md) and
[`moderation`](../l3-expression/moderation.md) — the same set [`rooms`](rooms.md) consumes, which
is why rooms is the proving ground.

The interface that does not yet exist anywhere is **discovery**, and that is the open problem
below.

## Consent surface

**Unknown, and that is the reason for deferral.** Every other module on this platform could state
its consent surface because the parties are identifiable and bounded. An open persistent space with
strangers, embodied in verified real anatomy, has a consent surface nobody here has characterised.

Two things are already known:

- [`consent`](../l1-core/consent.md) resolution must stay cheap enough to run per-interaction in
  real time, because in an embodied space interactions are continuous rather than discrete
  requests.
- [`rooms`](rooms.md)'s independence property — presence, appearance, proximity, device and
  capture as separate grants — becomes harder and more necessary with parties who are not known to
  each other.

## Open questions

- `OQ-052` — What replaces invitation as the access-control primitive in an open space?
- `OQ-053` — Are verified real bodies compatible with open social space at all, or does the
  combination of accurate real anatomy and strangers create a dynamic the platform should not
  build? This is a question about whether to do it, and it is legitimate to answer no.
- `OQ-054` — Does open space run on the platform's own runtime or on an existing social VR
  platform, given that the latter would mean accepting someone else's consent and moderation
  model? See `OQ-046`.
