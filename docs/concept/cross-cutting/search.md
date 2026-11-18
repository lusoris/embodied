# search

> **Layer:** Cross-cutting · **Owner:** planned Go `internal/search`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

Find things across three stores that answer different kinds of question — records in Postgres,
similarity in Qdrant, relations in Memgraph — and present one coherent result without leaking
across consent boundaries while doing it.

This module exists because the best-of-breed persistence split
([ADR-0002](../../adr/0002-relational-vector-graph-persistence.md)) pushes the federation problem
somewhere, and it is better solved once here than repeatedly in every caller.

## Three kinds of query

| Query | Store | Example |
| :--- | :--- | :--- |
| Exact and filtered | Postgres | Education material on a topic, tagged content in a space |
| Similarity | Qdrant | Bodies that behave alike, comparable experience reports |
| Relational | Memgraph | Provenance of a figure, pairings behind a prediction |

Most real queries touch more than one — "comparable outcomes for a body like mine" is a similarity
search filtered by consent and qualified by graph relations — and federation is the module's actual
work.

## Consent is a query constraint, not a filter

The central rule: **consent scope is applied inside the query, not to its results.**

Retrieving a result set and then removing what the caller may not see has already read it, and any
ranking, count or timing derived from the unfiltered set leaks. On a platform where the existence
of a record is itself disclosive — that a profile has a given feature, that a person posted in a
protected space — post-filtering is not a safe pattern.

This is the same rule stated in [`knowledge-graph`](../l2-intelligence/knowledge-graph.md) for
traversal, generalised to every store.

Result counts, pagination and relevance scores must all be computed within scope. "There are 47
results but you may see 3" discloses 44 things.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `query_plan` | Which stores a query touches, and in what order. |
| `scope` | The consent-derived constraint set, resolved before execution. |
| `result_set` | Federated, ranked, scoped. Not cached across subjects. |

Caching is per-subject or not at all. A shared result cache on this platform is a cross-consent
leak waiting for a cache hit.

## Interfaces

- **Provides:** federated search, scoped retrieval, ranking.
- **Consumes:** [`consent`](../l1-core/consent.md) for scope resolution,
  [`body-vector`](../l2-intelligence/body-vector.md),
  [`knowledge-graph`](../l2-intelligence/knowledge-graph.md),
  [`tagging`](../l3-expression/tagging.md), [`spaces`](../l5-community/spaces.md).
- **Consumed by:** [`education`](../l5-community/education.md),
  [`spaces`](../l5-community/spaces.md), [`media`](../l3-expression/media.md).

Viewer filters from [`tagging`](../l3-expression/tagging.md) compose into scope alongside consent.
A space's filter floor may narrow a query; nothing may widen it.

## Consent surface

Search queries are disclosive — what someone looks for says more than what they find. Queries are
not logged with a subject, are not retained, and are never used for recommendation. This is an
instance of the telemetry rule, and it matters most here.

There is no cross-user search of bodies. Similarity is available as a platform capability serving
[`simulation`](../l2-intelligence/simulation.md); it is not a way to go looking for people with
particular anatomy.

## Open questions

- `OQ-068` — Does the anonymous tier get search, and if so over what? Reference and education
  material only is the safe answer.
- `OQ-069` — What is the cross-store consistency expectation for a federated query, given three
  stores updated by [`learning`](../l2-intelligence/learning.md) under `OQ-021`?
