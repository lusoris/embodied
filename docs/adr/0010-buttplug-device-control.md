# ADR-0010: Buttplug Rust library for physical device control

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

VR embodiment in a verified real body, with connected physical hardware, was added during the
replan as a module the recovered concept never contained. It closes the platform's loop: verified
measurements produce an avatar, the avatar produces presence, presence with device integration
produces an experience, and the reported outcome feeds the learning model.

Device support means speaking to a large and fragmented ecosystem of intimate hardware across
Bluetooth, USB and serial, from many vendors with incompatible protocols. Writing that from scratch
is a multi-year effort producing a worse version of something that already exists.

[Buttplug](https://buttplug.io/) is the established open library for exactly this, behind the
Intiface ecosystem. Verified at the time of decision: Buttplug v10 and Intiface Central v3 released
February 2026, **implemented in Rust**, BSD-3-Clause licensed, covering 750+ devices including
Lovense, Kiiroo, The Handy, WeVibe, Satisfyer and OSR-2/SR-6.

Two properties make it an unusually good fit. It is written in Rust, which is already the compute
kernel's language, so it is a dependency rather than a bridge. And BSD-3-Clause is compatible with
EUPL-1.2.

## Decision

Depend on the Buttplug Rust library directly inside `crates/`. Device control becomes a capability
of the compute kernel.

An internal device-capability interface sits in front of it so that callers speak in platform terms
— intent, bounds, consent scope — rather than device protocol, and so a different backend can be
added later without touching callers.

Device discovery, pairing and connection remain **client-side**, where the hardware is. The
platform sends bounded intent; it does not reach into a user's Bluetooth stack.

Safety semantics are defined in the `device` module and are fail-closed throughout: bounded
commands with intensity ceilings and duration limits, dead-man behaviour on connection loss,
**local stop authority that no remote party can override**, no remote control without a live
session grant, and rate and escalation limits.

## Consequences

The entire device ecosystem is inherited rather than built. The integration is same-language, so
there is no FFI or IPC boundary in the path that actuates hardware — which matters because that
path has physical failure modes.

HISS-02's bounded-iteration and explicit-timeout requirements stop being a formality here: an
unbounded loop in this crate is a physical hazard rather than a performance bug.

Costs: a dependency on an external project's release cadence and device coverage. The abstraction
layer mitigates lock-in at the cost of an indirection.

Whether to embed the library in a platform client or interoperate with a user's existing Intiface
Central is unresolved — embedding means shipping and updating a device stack; interoperating means
depending on software the user must install separately. Recorded as `OQ-043`.

Sensor-capable devices report as well as actuate. Whether that telemetry feeds `learning` is a
separate and very serious consent question — `OQ-045`.

## Alternatives considered

**Intiface Central as an external sidecar over its websocket protocol.** Users keep their own
device setup and updates; the platform ships no device stack. Retained as a live option under
`OQ-043` rather than rejected.

**Direct vendor integrations.** Full control, and it means reimplementing hundreds of vendor
protocols to reach a worse version of an existing maintained library.

**Design the module now, build later.** Reasonable sequencing given VR is not yet built. Rejected
because the decision is cheap to make now and the safety semantics need to constrain the modules
being designed around it.

## References

- User decision, 2026-09-16, haptics (paraphrased): the Buttplug crate, placed inside the kernel.
- User direction, 2026-09-16, on VR scope (paraphrased): consider adding VR chat with device
  connection, where people could move about in their own real bodies, on condition that the body
  is approved as real.
- [buttplug.io](https://buttplug.io/) — Buttplug v10 / Intiface Central v3, February 2026; Rust
  implementation; BSD-3-Clause; 750+ supported devices
- [Intiface ecosystem architecture](https://buttplug.io/docs/dev-guide/architecture/intiface/)
- `docs/concept/l4-presence/device.md` — `OQ-043`, `OQ-044`, `OQ-045`
