# knowledge-graph

> **Layer:** L2 Intelligence · **Owner:** planned Rust `crates/embodied-graph`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet) · **Store:** Memgraph
> **ADR:** [0002](../../adr/0002-relational-vector-graph-persistence.md)

## Purpose

Hold the relations that are not measurements: which bodies were paired, what was reported, which
protocol produced which datum, which source supports which distribution, what a person prefers and
how that changed.

The vector space answers *what is similar*. The graph answers *what is connected, and on what
evidence*. Compatibility prediction needs both: a neighbourhood from
[`body-vector`](body-vector.md), qualified by what the graph knows about the pairings inside it.

The graph is also where the platform's audit trail lives as first-class structure rather than log
lines. A percentile traces to a distribution, to a source, to a protocol. A prediction traces to
the outcomes that trained it. That traceability is what §5's uncertainty commitments require in
order to be more than a disclaimer.

## Shape

| Node kinds | Edge kinds |
| :--- | :--- |
| profile, feature, measurement, protocol | measured-with, graded-as, derived-from |
| source, distribution, cohort | supports, contradicts, supersedes |
| pairing, outcome-report, experience | reported, paired-with, contributed-to |
| space version, model | trained-on, produced-by |

Traversal is **depth-bounded** (following Tribunus, `d_max = 12`) and acyclicity is verified before
commit. HISS-01 forbids recursion and HISS-02 requires bounded iteration, which for a graph engine
means Kahn's-algorithm cycle checking on mutation rather than hoping traversals terminate.

## Why a dedicated engine

Memgraph rather than the graph living inside the Rust kernel in memory, or inside Postgres via an
extension. The reasoning is in [ADR-0002](../../adr/0002-relational-vector-graph-persistence.md);
the short form is that this graph is not hydrated from a handful of GitOps files as Tribunus's is —
it grows monotonically with user activity, it must survive restarts without a rebuild window, and
openCypher is a considerably better tool for the traceability queries above than hand-written
traversal.

The cost is honest and stated: **three stateful systems** — Postgres, Qdrant, Memgraph — each with
its own backup, failover and consistency story. Cross-store consistency is the price of
best-of-breed, and it is paid in [`learning`](learning.md), which owns the write path that touches
all three.

## Owned data

The graph owns **relations**; it does not own the entities. A profile's authoritative record is in
Postgres; the graph holds its node and its edges. Node payloads are kept minimal — identifiers and
what traversal needs — so that the graph never becomes a second source of truth for facts that
Postgres owns.

## Interfaces

- **Provides:** traverse, path query, edge write, invariant check, provenance resolution.
- **Consumes:** [`consent`](../l1-core/consent.md) for scope on any traversal crossing profiles.
- **Consumed by:** [`simulation`](simulation.md), [`learning`](learning.md),
  [`statistics`](../l1-core/statistics.md) for provenance,
  [`search`](../cross-cutting/search.md).

## Consent surface

An edge between two profiles is jointly held data — a pairing is a fact about two people, and
either may withdraw. Withdrawal removes the edge from traversal while preserving the record that
something was withdrawn, since the alternative makes revocation undetectable and therefore
unauditable.

Traversal scope is bounded by consent at query time, not filtered afterwards. A traversal that
walks through a profile the caller may not see has already leaked, regardless of what is returned.

## Open questions

- `OQ-021` — Cross-store write consistency: what is the transaction boundary when a single outcome
  report writes to Postgres, Qdrant and Memgraph?
- `OQ-022` — Does `d_max = 12` suit this domain, or was it inherited from a task-decomposition
  graph with different shape?
- `OQ-023` — Is the graph rebuildable from Postgres as a recovery path, and if so, is that a
  reason to reconsider the dedicated engine?
