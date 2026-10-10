# extensibility

> **Layer:** Cross-cutting · **Owner:** Go `internal/extensibility`
> **Added by:** gap pass — closes recovered §12 "Erweiterte Nutzung" (plugins)

## Purpose

Decide how — and whether — third-party code and integrations may exist, before somebody asks for
them under pressure.

The recovered concept listed "Plugins" as a bullet with no elaboration. On most platforms that
would be an unremarkable growth feature. Here it is a direct threat to the platform's only hard
rule: a plugin is third-party code running in an environment that holds body measurements, intimate
media, verification evidence and reported sexual experiences.

The question is therefore not "what plugin API should we build" but "what, if anything, can be
extended without putting consent enforcement in someone else's hands".

## Position

**No third-party code runs inside the platform, with access to user data.** That path is closed,
and closing it deliberately now is cheaper than closing it later after an ecosystem exists.

Three extension surfaces are compatible with the consent model, in increasing order of risk:

| Surface | Risk | Position |
| :--- | :--- | :--- |
| **Reference data consumption** | None — public, citable data with no user content | Open. This is the catalogue export in [`professional`](../l5-community/professional.md). |
| **Client-side device integration** | Low — runs on the user's machine, on their hardware, under their control | Open. This is how [`device`](../l4-presence/device.md) already works. |
| **User-authorised data export** | Moderate — the user's own data, at their request, leaving to a destination they chose | Open, with explicit per-export consent and a clear statement that exported data has left the platform. |
| **Server-side plugins with data access** | Severe | Closed. |

The distinction that makes the first three acceptable is that none of them requires a third party
to enforce consent. Reference data has no consent attached. Client-side integration operates on
data the user already has. Export is a consent decision the user makes explicitly, once, per
export.

## Federation and integrations

Third-party service integrations — a VR runtime, a storage provider, an inference backend — are
not plugins but vendor dependencies, and are governed as such: each is a decision recorded where it
is made, with a stated data exposure. [`device`](../l4-presence/device.md) and the runtime question
in `OQ-046` are the live examples.

An integration that would transmit body data, media or outcome reports to a third party requires an
ADR, not a configuration change.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `export_grant` | A user-authorised export: scope, destination, timestamp. Per-export, never standing. |
| `integration` | A recorded third-party dependency and its data exposure. |

There is no plugin registry, no extension manifest and no sandbox, because there is nothing to
register, manifest or sandbox.

## Interfaces

- **Provides:** authorised export, integration registry.
- **Consumes:** [`consent`](../l1-core/consent.md), [`identity`](../l1-core/identity.md),
  [`admin`](admin.md) for data-subject export.
- **Consumed by:** [`professional`](../l5-community/professional.md) for catalogue export.

## Consent surface

Export is the whole of it, and it is the one place where the platform hands data to something it
does not control. Two obligations:

**Per-export, never standing.** A standing export authorisation is an ongoing data flow that the
user stops thinking about. Each export is its own decision.

**Honest about irreversibility.** Once exported, data has left. The platform can stop future
exports and cannot recall what was taken. This is stated at the point of export, in those terms —
the same honesty [`avatar`](../l3-expression/avatar.md) owes about exported avatars.

## Open questions

- `OQ-077` — Is the closed position on server-side plugins permanent, or is there a sandboxed
  design that could hold? Any such design must enforce consent inside the sandbox, which is the
  hard part and probably the disqualifying one.
- `OQ-078` — Does user-authorised export cover derived data — embeddings, simulation results,
  trajectories — or only source records? Derived data is more disclosive per byte.
