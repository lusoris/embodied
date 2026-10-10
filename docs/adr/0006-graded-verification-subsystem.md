# ADR-0006: One verification subsystem with graded assertions

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

Verification appeared twice in the replan, arriving from opposite directions.

The reference-data decision called for published literature now and proven user data later,
which requires a way to establish that a user measurement was taken properly.

The VR embodiment decision called for avatars built from a person's real body — once approved as
real — which requires a way to establish that the measurements behind an avatar are genuinely
that person's.

These look like different problems. One is scientific methodology; the other is trust and safety.
They are the same question asked by two callers: *how much should I trust this measurement?*

Building them separately would produce two concepts, two audit trails, two sets of evidence
handling for the platform's most sensitive artifact class, and no consistent way to describe how
well anything is established.

## Decision

One subsystem producing **graded assertions** about measurements. Each consumer sets its own
threshold.

| Grade | Meaning |
| :--- | :--- |
| `self-reported` | The person entered it. No claim beyond that. |
| `protocol-guided` | Entered while following a defined, versioned protocol. |
| `evidenced` | Supported by artifact evidence assessed against that protocol. |
| `witnessed` | Independently confirmed by a party other than the subject. |

Grades are ordered and monotonic in trust, so consumer policy is a threshold rather than a special
case. Thresholds are data (`grade_policy`), not scattered code.

Verification grades a **measurement, never a person.** There is no verified-person status on this
platform and no feature may imply one.

Evidence is **retention-limited by default** — it supports the assertion and is then discarded,
leaving the graded assertion and an audit record.

## Consequences

Statistics, avatar authenticity, pair simulation and embodiment all read one grade and apply their
own policy. One implementation, one audit trail, no duplicate concepts.

The ordering makes §5's uncertainty commitments expressible: a simulation result can report the
verification grade of its inputs, and a prediction built from two self-reported measurements says
so.

Costs: evidence is the most sensitive artifact the platform holds — it exists to prove a claim
about a specific body and is by nature unambiguous. Retention limiting reduces the exposure and
means re-verification later is impossible without new evidence, which is accepted.

`evidenced` needs an assessor. An automated one is a model that can be fooled and must view
extremely sensitive material; a human one is a person who must view it. Unresolved — `OQ-011`.

`witnessed` may not be reachable at all without an identity system the platform declined to build
under ADR-0004, and may end up reserved for clinically sourced reference data — `OQ-012`.

## Alternatives considered

**Separate subsystems for reference methodology and avatar authenticity.** Keeps each free of the
other's constraints and duplicates evidence handling for the platform's most dangerous data class.

**One subsystem with a binary verified / unverified flag.** Much easier to build and explain.
Rejected because the platform commits to showing uncertainty, and a binary flag cannot express how
strongly something is established — the statistics module needs the gradation to set an overlay
threshold at all.

## References

- User decision, 2026-09-16, verification (paraphrased): a single subsystem with graded levels,
  which was the recommended option.
- User direction, 2026-09-16, reference data (paraphrased): published literature first, proven
  user data afterwards.
- User direction, 2026-09-16, VR avatars (paraphrased): people could move about in their own real
  bodies, on condition that the body is approved as real.
- `docs/concept/l1-core/verification.md` — `OQ-011`, `OQ-012`
