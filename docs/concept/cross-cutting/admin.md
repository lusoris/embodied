# admin

> **Layer:** Cross-cutting · **Owner:** planned Go `internal/admin`, CLI `cmd/embodiedctl`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

Operate the platform — deploy, diagnose, support, respond to incidents — under the constraint that
**operators are not exempt from the consent model.**

This is the module where a platform's stated principles are usually quietly abandoned. Consent,
visibility and privacy are enforced against users, and then a support tool exists that can see
everything, used by whoever has the credential, logged nowhere. On a platform holding this
material, that would make every other guarantee in this document conditional on operator
discretion.

So the design rule is: operator access is **scoped, justified, audited and bounded**, and the
audit is not written by the person doing the accessing.

## Operator access

| Capability | Constraint |
| :--- | :--- |
| Aggregate operational data | Unrestricted — this is [`telemetry`](telemetry.md), which carries no subject |
| Account state, billing, tier | Scoped to the account, on a support request from that account |
| Content inspection | Only via a [`moderation`](../l3-expression/moderation.md) case, never ad hoc |
| Body data, media, outcome reports | No routine path exists. Break-glass only, and see below |
| Verification evidence | No access. Retention-limited and assessed by its own path |

**Break-glass** is a deliberate, logged, alerting action requiring a stated reason, and it notifies
the affected user unless a legal obligation prevents it. It exists because refusing to have any
emergency path produces an unrunnable system, and pretending it does not exist produces an
unaudited one.

There is no operator view that shows an individual's body data, media or reported experiences as a
matter of routine. If support cannot be delivered without it, support is delivered without it.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `operator` | Identity, role, scope. Scopes are enumerated, not ad hoc. |
| `access_record` | Every privileged read: who, what, when, stated reason. Append-only, external. |
| `support_case` | A user-initiated request, and what was done. |
| `break_glass` | Emergency access: reason, duration, notification state. |

`access_record` being append-only and written outside the operator's control is the property that
makes the rest meaningful. An audit log an administrator can edit is a formality.

## Interfaces

- **Provides:** operations, support, incident response, break-glass.
- **Consumes:** [`telemetry`](telemetry.md), [`moderation`](../l3-expression/moderation.md),
  [`identity`](../l1-core/identity.md), [`consent`](../l1-core/consent.md).
- **Consumed by:** nothing. Nothing in the platform should depend on administrative action to
  function normally.

## Data subject operations

Export, correction and deletion are **user-initiated and self-service**, not support tickets.
Routing them through an operator means a person exercising a right must ask a human for
permission, and means that human sees the data.

Deletion propagates to derived artifacts — embeddings, graph edges, avatars, derivatives, caches —
per the enumeration obligation every module carries from [`consent`](../l1-core/consent.md). This
module verifies completion; it does not perform deletion by hand.

## Consent surface

Operator access is a standing exception to the platform's only hard rule, and is treated as the
serious thing it is: minimised, enumerated, audited externally, and surfaced to affected users.

Users are told, in plain terms and up front, what an operator can and cannot see. A privacy model
users cannot describe is one they cannot rely on.

## Open questions

- `OQ-072` — Who holds break-glass, and what prevents its routine use as a convenience? Technical
  bounds beat policy here — time limits, mandatory notification, alerting to a second party.
- `OQ-073` — Where does the external audit log live such that an operator cannot alter it, on a
  platform the same operator runs?
- `OQ-074` — Deletion verification across three stores plus object storage plus backups: what
  actually proves completion rather than asserting it? See `OQ-036`.
