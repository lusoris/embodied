# embodiment

> **Layer:** L4 Presence · **Owner:** Go `internal/embodiment`, geometry and device via `crates/`

## Purpose

Let a person inhabit their own real body — see it, move in it, be in it — alone.

Solo first, deliberately. Every hard problem in the chain is present without any of the networking,
moderation or multi-party consent complexity: does the avatar actually look like this person, does
the measurement-to-geometry pipeline hold up at arm's length in VR, does device integration feel
connected to what is being seen. Those answers are prerequisites for shared space, and none of them
need another person present.

It is also valuable on its own terms, and probably the most therapeutically interesting thing the
platform does. Seeing your own body accurately, at scale, from outside, is an experience almost
nobody has had. §11A's self-determination theme lands here more than anywhere.

## What it composes

```text
[`avatar`] ──> verified body, rigged, authenticity-graded
[`visualizer`] ──> shared parametric geometry, photoreal or anatomical
[`device`] ──> bounded physical feedback, local stop authority
[`simulation`] ──> what this body does, with its uncertainty shown
```

This module owns the session that binds them: presence, tracking, rendering target, device
binding, and the safety envelope across all of it.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `session` | An embodiment session: avatar version, device bindings, duration. |
| `presence_state` | Tracking and pose. Transient by default; not retained after session end. |
| `comfort_setting` | Locomotion, scale, boundaries, exit affordances. Per person, persistent. |

Pose and tracking data are not retained. Movement is biometric — gait and posture identify people
— and there is no platform use for it that justifies the risk.

## Interfaces

- **Provides:** session lifecycle, presence, device binding, safety envelope.
- **Consumes:** [`avatar`](../l3-expression/avatar.md), [`device`](device.md),
  [`visualizer`](../l3-expression/visualizer.md),
  [`simulation`](../l2-intelligence/simulation.md), [`consent`](../l1-core/consent.md).
- **Consumed by:** [`rooms`](rooms.md), which adds other people to this foundation.

Solo embodiment must be fully functional with no network path to other users. That is both the
staging discipline and a privacy property: this experience should be available to someone who
never wants to be seen.

## Consent surface

Solo embodiment involves one person, so the consent surface is small — but two things matter.

**Exit is always available and always immediate.** A person in VR in their own body, with a device
connected, must be able to stop all of it in one action they can find without looking. This
inherits [`device`](device.md)'s local stop authority and extends it to the whole session.

**Nothing leaves.** A solo session produces no shareable artifact by default. Recording, capture or
export is a separate, explicit act — never a session setting someone might have left on.

## Open questions

- `OQ-046` — Which runtimes are targeted, and does the platform ship a client or export to
  existing ones? This is the avatar-pipeline-versus-runtime question, deferred rather than
  answered, and it determines the size of this module by an order of magnitude.
- `OQ-047` — Distress and dysphoria are foreseeable outcomes of seeing your own body accurately.
  What does the session owe a person who is not having a good time, without becoming
  paternalistic about an experience they chose?
- `OQ-048` — Does solo embodiment generate [`learning`](../l2-intelligence/learning.md) signal at
  all, or is it entirely outside the model loop? Outside is the safer default.
