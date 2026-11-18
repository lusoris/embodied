# ADR-0002: Best-of-breed persistence — Postgres, Qdrant, Memgraph

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

Tribunus holds its vector-tree and state-graph in memory, hydrated from declarative repository
files. That works because its source of truth is a handful of GitOps documents.

emBodied cannot do this. Its state is user data — measurements, media, outcome reports, consent
records — which grows monotonically, must survive restarts without a rebuild window, and is
revocable. Files are not an option, and neither is a purely in-memory graph.

Three distinct access patterns exist, and one engine serving all three would serve at least two of
them badly:

- **Relational**: consent records, accounts, measurements, media metadata. Needs transactions,
  constraints and exact arithmetic.
- **Similarity**: nearest-neighbour over learned body-vectors and, later, text and media
  embeddings. Needs a real ANN index.
- **Relational-in-the-graph-sense**: provenance and traceability — a percentile to a distribution
  to a source to a protocol; a prediction to the outcomes that trained it. Needs traversal and a
  query language suited to paths.

## Decision

Three stores, each chosen for its access pattern:

| Store | Holds |
| :--- | :--- |
| **PostgreSQL** | Authoritative records — accounts, consent, measurements, media metadata |
| **Qdrant** | Vector indices — body-vectors, later text and media embeddings |
| **Memgraph** | The knowledge graph — entities, edges, provenance, traversal |

Postgres is the source of truth for entities. The graph holds relations with minimal node payloads
and is never a second authority for facts Postgres owns.

Cross-store writes are owned by a single module — `learning` — rather than being distributed
across callers.

## Consequences

Each store is well suited to its job, scales independently, and brings real tooling: openCypher for
provenance queries, a proper ANN index for similarity, and full relational integrity where consent
and measurement records live.

The cost is honest and substantial: **three stateful systems**, each with its own backup, restore,
failover and upgrade story. Cross-store consistency has no transaction spanning them, so a single
outcome report writing to all three needs a defined boundary and a reconciliation path — recorded
as `OQ-021`.

Federated queries need a module of their own, which is why `search` exists as a cross-cutting
concern rather than a helper.

Deletion becomes harder to prove complete, since a revocation must reach all three plus object
storage plus backups — `OQ-074`.

## Alternatives considered

**Postgres with pgvector and Apache AGE.** One engine for all three patterns: single backup, single
failover, trivial to operate on the existing cluster. Rejected in favour of dedicated engines,
though it remains the obvious fallback if operating three stores proves disproportionate — the
ceiling is almost certainly above what this platform needs.

**Postgres for durability with the graph held in memory in the Rust kernel.** Closest to Tribunus
and the fastest to traverse, but requires the graph to fit in RAM and reintroduces a rehydration
window that grows with the data.

**Postgres only, with the Rust kernel implementing both vector search and graph traversal.** The
fewest dependencies and the most interesting engineering; also the most code to own and maintain
in the area where mature implementations already exist.

## References

- User decision, 2026-09-16, persistence (paraphrased): a best-of-breed split across specialised
  stores.
- User direction, 2026-09-16, on the intelligence layer (paraphrased): use the control concepts of
  the owner's Tribunus concept repository as the model, and build on vector- and graph-based
  systems.
- `cordanaLLM/Tribunus` `tribunus-description-v2.md`: "backed by a **dynamic Vector-Tree and
  State-Graph as its primary Source of Truth (SoT)**"
- `cordanaLLM/Tribunus` ADR-001: "Tribunus adopts an in-memory Graph and SIMD Vector-Tree as its
  primary SoT, hydrated directly from GitOps files"
- Rename note, 2026-11-18: `cordanaLLM/Tribunus` is now
  [Epitrop](https://github.com/tekmora/epitrop) at `tekmora/epitrop` (renamed 2026-10-11; the old
  address redirects). The wording quoted above is not in that repository's history (306 commits,
  checked 2026-11-18).
- `docs/concept/l2-intelligence/knowledge-graph.md` — `OQ-021`, `OQ-023`
