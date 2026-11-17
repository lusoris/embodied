# verification

> **Layer:** L1 Core · **Owner:** Go `internal/verification` · **ADR:** [0006](../../adr/0006-graded-verification-subsystem.md)

## Purpose

Say how strongly a fact is established — once, in one place, for every consumer.

Verification arose twice independently in the concept: the reference pipeline needs proven data
beyond published literature, and VR avatars need to represent a body that is actually the user's.
Those look like different problems — one scientific, one trust-and-safety — but they are the same
question asked by two callers: *how much should I trust this measurement?*

So there is one subsystem producing **graded assertions**, and each consumer sets its own
threshold. The four grades — `self-reported`, `protocol-guided`, `evidenced` and `witnessed` — and
their meanings are defined in [ADR-0006](../../adr/0006-graded-verification-subsystem.md#decision).

The grades are ordered and monotonic in trust, which is what lets consumers express policy as a
threshold rather than a special case. Statistics may require `protocol-guided` for its user
overlay; avatar authenticity may require `evidenced` before a body is presented as real in a
shared space; pair simulation may accept `self-reported` while labelling its output accordingly.

A binary verified/unverified flag was considered and rejected: §5 commits the platform to showing
uncertainty, and a binary flag cannot express how well something is established.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `assertion` | Subject measurement, grade, method, assessor, timestamp. Append-only. |
| `evidence` | Artifact supporting an assertion. Consent-bound, retention-limited, never public. |
| `challenge` | A dispute against an assertion, and its resolution. |
| `grade_policy` | Per-consumer thresholds, so policy is data rather than scattered code. |

## Interfaces

- **Provides:** assert, grade lookup, threshold evaluation, challenge handling.
- **Consumes:** [`measurement`](measurement.md), [`consent`](consent.md), [`identity`](identity.md).
- **Consumed by:** [`statistics`](statistics.md), [`avatar`](../l3-expression/avatar.md),
  [`simulation`](../l2-intelligence/simulation.md), [`embodiment`](../l4-presence/embodiment.md),
  [`reference`](reference.md).

## Consent surface

Evidence is the most sensitive artifact class the platform holds — more so than published media,
because it exists to prove a claim about a specific body and is by nature unambiguous.

Evidence is therefore retention-limited by default: it supports the assertion and is then
discarded, leaving the graded assertion and an audit record behind. Holding evidence indefinitely
in order to re-verify later is a convenience that is not worth the liability.

Verification grades a **measurement**, never a person. There is no verified-person status on this
platform, and no feature may imply one.

## Open questions

- `OQ-011` — What constitutes `evidenced` in practice, and who or what assesses it? An automated
  assessor is a model that can be fooled and that must see extremely sensitive material; a human
  assessor is a person who must view it.
- `OQ-012` — Is `witnessed` reachable at all without building an identity system the platform has
  declined to build? It may be reserved for clinically sourced reference data only.
