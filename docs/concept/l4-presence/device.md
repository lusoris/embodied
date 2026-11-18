# device

> **Layer:** L4 Presence · **Owner:** planned Rust `crates/embodied-device`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet) · **ADR:**
> [0010](../../adr/0010-buttplug-device-control.md)

## Purpose

Control physical intimate hardware as a capability of the compute kernel, with consent and safety
semantics that hold when something goes wrong.

Built on [Buttplug](https://buttplug.io/) — the mature open library behind the Intiface ecosystem.
It is **implemented in Rust**, which is the same language as the compute kernel, so it is a
dependency rather than a bridge; it is BSD-3-Clause, which is compatible with EUPL-1.2; and it
covers 750+ devices across Lovense, Kiiroo, The Handy, WeVibe, Satisfyer and OSR-2/SR-6 via
Bluetooth, USB and serial.

Writing a device stack instead would mean reimplementing hundreds of vendor protocols to arrive at
a worse version of something that already exists and is maintained. The build-versus-adopt question
here is not close.

## Safety semantics

Device control is the only part of emBodied that acts on a body rather than describing one. Its
failure modes are physical, so the design is fail-closed throughout:

1. **Bounded commands.** Every command carries an intensity ceiling and a duration bound. There is
   no unbounded actuation primitive in the interface.
2. **Dead-man behaviour.** Loss of connection, session, or heartbeat stops the device. The safe
   state is off, and reaching it must not depend on a message arriving.
3. **Local stop authority.** The person with the device can always stop it, immediately, without
   the network. This cannot be overridden by any remote party, session policy or platform state.
4. **No remote control without a live grant.** Consent to be controlled is per-session, explicitly
   scoped, and revocable mid-session with immediate effect.
5. **Rate and escalation limits.** A remote party cannot ramp intensity faster than defined bounds,
   regardless of what they send.

HISS-02's bounded-iteration and explicit-timeout requirements are not a formality here — an
unbounded loop in this crate is a physical hazard.

## Integration shape

The Buttplug library will be depended on directly inside the planned `crates/` workspace
([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet). An internal
device-capability interface sits in front of it so that callers speak in platform terms — intent,
bounds, consent scope — rather than in device protocol, and so that a future backend can be added
without touching callers.

Device discovery, pairing and connection stay client-side where the hardware is. The platform
sends bounded intent; it does not reach into someone's Bluetooth stack.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `device_session` | An active control relationship: parties, scope, bounds, expiry. |
| `control_grant` | Who may control what, within which limits, for how long. Revocable. |
| `safety_bound` | Ceilings and rate limits. Owner-set, never remotely raisable. |
| `session_log` | What was commanded. Retention-limited, private to the participants. |

Device telemetry is deliberately minimal. What a person's hardware did is not platform analytics.

## Interfaces

- **Provides:** connect, bounded command, session management, immediate stop.
- **Consumes:** [`consent`](../l1-core/consent.md), [`identity`](../l1-core/identity.md).
- **Consumed by:** [`embodiment`](embodiment.md), [`rooms`](rooms.md), [`live`](live.md).

## Consent surface

Consent to be physically controlled is the most consequential grant on the platform, and it is
deliberately the most constrained: per-session, time-bounded, scope-limited, instantly revocable,
and never inheritable from any other consent. Agreeing to share a room is not agreeing to be
touched.

Withdrawal takes effect at the device, not at the next policy check.

## Open questions

- `OQ-043` — Does the platform embed the Buttplug library in its own client, or interoperate with
  a user's existing Intiface Central? Embedding means shipping and updating a device stack;
  interoperating means depending on software the user must install.
- `OQ-044` — What are the default safety bounds, and who may raise them? Owner-set is the answer
  for the ceiling; the floor may need to be platform-set and non-negotiable.
- `OQ-045` — Sensor-capable devices report as well as actuate. Does the platform ingest that as
  [`learning`](../l2-intelligence/learning.md) signal, and if so under what separate consent?
  This would be among the most intimate data conceivable.
