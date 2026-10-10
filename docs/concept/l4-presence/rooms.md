# rooms

> **Layer:** L4 Presence · **Owner:** Go `internal/rooms`

## Purpose

Limited, invited, multi-person sessions — two people or a small group, in their real bodies, by
explicit invitation.

This is the middle step between [`embodiment`](embodiment.md) and
[`social-vr`](social-vr.md), and it is where most of the actual value of shared presence is,
without most of the cost. A closed invited session removes open-world discovery, drop-in
strangers, persistent-world moderation and unbounded scaling — which together are the large
majority of the engineering and safety burden of social VR — while keeping the part people
actually want.

## Invitation, not discovery

There is no browsing of rooms, no public listing, no joining something you were not invited to.
A room exists because specific people were invited and accepted, and its membership is closed for
its duration.

This is a deliberate constraint rather than a phase-one limitation. Discovery is what makes a
space require moderation at scale; invitation makes the participants themselves the access control.

## Consent composition

A room is where several consent grants must hold simultaneously and independently:

| Grant | Scope |
| :--- | :--- |
| Presence | Being in a shared space with these specific people |
| Appearance | Which avatar, at what authenticity grade, visible to whom |
| Proximity | How close, and what interaction is permitted |
| Device | Whether any participant may control your hardware, within what bounds |
| Capture | Whether anything may be recorded — default no, and unanimous to change |

None of these implies any other. **Agreeing to share a room is not agreeing to be touched**, and
the interface must never present them as a single decision. This is the most likely place for the
platform to accidentally bundle consents, and the separation is stated here so that it is
testable.

Every grant is revocable mid-session with immediate effect, and revocation must never require
confrontation — leaving, becoming invisible, or cutting device control must all be achievable
without announcing it.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `room` | Session: participants, duration, permitted interactions. Ephemeral. |
| `invitation` | Offer, acceptance, and the grants offered alongside it. |
| `participant_grant` | Per-person, per-scope consent within the room. Independently revocable. |
| `incident` | A report arising from a session, routed to [`moderation`](../l3-expression/moderation.md). |

Rooms are ephemeral. Nothing persists after a session but incident records and whatever
participants explicitly and unanimously chose to keep.

## Interfaces

- **Provides:** room lifecycle, invitation, grant management, in-session revocation.
- **Consumes:** [`embodiment`](embodiment.md), [`avatar`](../l3-expression/avatar.md),
  [`device`](device.md), [`consent`](../l1-core/consent.md), [`identity`](../l1-core/identity.md).
- **Consumed by:** [`moderation`](../l3-expression/moderation.md) for incidents,
  [`learning`](../l2-intelligence/learning.md) only where a participant separately reports an
  outcome.

## Consent surface

The composition table above is the surface. Its governing property is **independence**: five
separate grants, none implying any other, each revocable mid-session with immediate effect.

The failure this guards against is bundling — presenting presence, appearance, proximity, device
and capture as one "join room" decision. That would make agreeing to share a space equivalent to
agreeing to be touched, which is the single most consequential consent error this platform could
make.

Revocation must never require confrontation. Leaving, becoming invisible, or cutting device
control must all be achievable without announcing it to the other participants.

## Safety

A closed room is safer than an open world and is not safe by construction. The specific risks are
coercion and pressure between people who know each other, which access control does not address.

Therefore: exit is unconditional and always immediate; leaving cannot be prevented, delayed or made
socially visible as a refusal; device control cuts on exit; and reporting from within a session is
possible without alerting other participants.

## Open questions

- `OQ-049` — Maximum participants before a room becomes a space needing moderation rather than
  invitation? The number matters because it is where this module's assumptions break.
- `OQ-050` — Does authenticity grade get displayed to other participants, and at what granularity?
  Showing it makes the real-bodies claim meaningful; showing it precisely discloses how much
  evidence someone provided.
- `OQ-051` — Capture requiring unanimity is stated; what enforces it technically, given a
  participant can always point a camera at their own headset display?
