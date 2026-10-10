# Module Architecture

One page per module. Every page states the same five things: **purpose**, **owned data**,
**interfaces**, **consent surface**, **open questions**.

A module page that leaves a section as a bare heading has failed — that is precisely the failure
of the recovered draft this architecture replaces.

---

## L0 — Governance

Not modules but binding constraints on all of them: Praetor HISS-16 adoption, split licensing
under REUSE v3.2, and the `AGENTS.md` canonical harness. See [docs/adr/](../adr/README.md).

## L1 — Core platform · Go `internal/`

| Module | Owns |
| :--- | :--- |
| [identity](l1-core/identity.md) | Two-tier accounts, sessions, the anonymous tier |
| [consent](l1-core/consent.md) | Consent levels, visibility, binding on every artifact |
| [anatomy](l1-core/anatomy.md) | Gender-independent feature schema and presets |
| [measurement](l1-core/measurement.md) | Capture protocols, units, plausibility |
| [verification](l1-core/verification.md) | Graded assertions about how well a fact is established |
| [reference](l1-core/reference.md) | Literature ingestion, versioning, citation trail |
| [statistics](l1-core/statistics.md) | Percentiles, cohorts, comparison with uncertainty |

## L2 — Intelligence · Rust `crates/`

| Crate | Owns |
| :--- | :--- |
| [body-vector](l2-intelligence/body-vector.md) | The learned embedding of a body; SIMD similarity |
| [knowledge-graph](l2-intelligence/knowledge-graph.md) | Entities, edges, traversal, invariants |
| [statistics-engine](l2-intelligence/statistics-engine.md) | Percentile and plausibility mathematics |
| [simulation](l2-intelligence/simulation.md) | Geometric, biomechanical and statistical prediction |
| [learning](l2-intelligence/learning.md) | Outcome reports to graph edges to model correction |

## L3 — Expression

| Module | Owns |
| :--- | :--- |
| [visualizer](l3-expression/visualizer.md) | Parametric geometry, three render modes, WASM |
| [avatar](l3-expression/avatar.md) | Verified body to rigged, inhabitable avatar |
| [media](l3-expression/media.md) | Upload, transcode, storage, delivery, consent binding |
| [tagging](l3-expression/tagging.md) | Descriptors, assisted tagging, integrity watching |
| [moderation](l3-expression/moderation.md) | Consent enforcement, queues, appeals |

## L4 — Presence and embodiment

| Module | Owns |
| :--- | :--- |
| [device](l4-presence/device.md) | Physical device control via Buttplug; safety semantics |
| [embodiment](l4-presence/embodiment.md) | Solo presence in your own verified body |
| [rooms](l4-presence/rooms.md) | Limited, invited multi-person sessions |
| [social-vr](l4-presence/social-vr.md) | Open persistent social space — long-term goal |
| [live](l4-presence/live.md) | Text chat, cam, group conversation |

## L5 — Community

| Module | Owns |
| :--- | :--- |
| [spaces](l5-community/spaces.md) | Education, experience and expression contexts |
| [education](l5-community/education.md) | Anonymous-tier reachable learning material |
| [progress](l5-community/progress.md) | Personal, non-competitive development |
| [professional](l5-community/professional.md) | Professional and creator roles — conferring no data access |

## Cross-cutting

| Module | Owns |
| :--- | :--- |
| [telemetry](cross-cutting/telemetry.md) | Accounting, observability, resource ledger |
| [search](cross-cutting/search.md) | Retrieval across records, vectors and graph |
| [notification](cross-cutting/notification.md) | Delivery, preference, quiet by default |
| [admin](cross-cutting/admin.md) | Operations, support, incident handling |
| [extensibility](cross-cutting/extensibility.md) | What may integrate, and what may not |

---

## Dependency direction

```text
L5 Community  ──────┐
L4 Presence   ──────┤
L3 Expression ──────┼──> L1 Core ──> L2 Intelligence
                    │       │              │
Cross-cutting ──────┘       └──────────────┴──> Postgres · Qdrant · Memgraph
```

L1 never depends upward. L2 never calls out to L3–L5. Anything that appears to need an upward
call is a missing L1 concept, not a licence to invert the arrow.
