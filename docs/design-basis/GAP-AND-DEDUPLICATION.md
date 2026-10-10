# Gap and Deduplication Pass

Run after all modules were described, per the replan's step 4: find capabilities owned by no
module, merge overlapping ones, and confirm every section of the recovered concept has an owner.

**Date:** 2026-09-16 · **Modules at start:** 29 · **Modules after:** 31

---

## 1. Coverage — recovered concept against the module map

Every section of the recovered `MASTER_CONCEPT.md` (2026-01-15), and what now owns it.

| Recovered § | Title | Owner |
| :--- | :--- | :--- |
| 0 | Kurzdefinition | `MASTER_CONCEPT.md` §0 — permission-framing removed per ADR-0005 |
| 1 | Grundprinzipien | `MASTER_CONCEPT.md` §1 |
| 2 | Plattform-Säulen | `MASTER_CONCEPT.md` §2 |
| 3 | Nutzeridentität & Profile | `identity`, `anatomy`, `consent` |
| 4 | Körperdaten & Vergleich | `anatomy`, `measurement`, `statistics`, `reference` |
| 5 | Simulation & Kompatibilität | `simulation`, `body-vector` |
| 6 | Realität & Rückkopplung | `learning` |
| 7 | Medien-Ökosystem | `media`, `tagging` |
| 8 | Live-Interaktion | `live`, `rooms` |
| 9 | Gamification & Progress | `progress` |
| 10 | Trust, Consent & Sicherheit | `consent`, `moderation`, `verification` |
| 11 | Community-Räume | `spaces` |
| 11A | Bildung, Selbstermächtigung & Schutzräume | `education`, `spaces`, `identity` (anonymous tier) |
| 12 | Erweiterte Nutzung | **was unowned** → `professional`, `extensibility` |
| 13 | Monetarisierung | Deferred — `OQ-001` |
| 14 | Recht & Governance | Deferred — `OQ-001`; operational half in `admin` |
| 15 | Roadmap | Deferred — `OQ-001` |
| 16 | Techstack | ADR-0001, ADR-0002 |
| 17 | Wiki & Dokumentation | `OQ-002`; role views under `docs/` |

## 2. Gap found and closed

**§12 "Erweiterte Nutzung" — Professionals, Creator options, Plugins.** The only section with no
owning module. It had been silently dropped because its three bullets each looked like somebody
else's problem.

Closing it produced two modules and, more usefully, forced two positions that needed taking
anyway:

- [`professional`](../concept/l5-community/professional.md) — professional status confers **no
  additional access to user data**. A professional tier with data access would be the platform's
  most attractive attack surface and the easiest to claim falsely, and verifying a credential
  means holding identity documents that ADR-0004 declined to hold.
- [`extensibility`](../concept/cross-cutting/extensibility.md) — **no third-party code runs inside
  the platform with access to user data.** Reference consumption, client-side device integration
  and user-authorised export are open; server-side plugins are closed. Closing this now is far
  cheaper than closing it after an ecosystem exists.

The creator *role* is in scope under `professional`; creator *earnings* defer with monetisation.

## 3. Gaps checked and found already owned

| Capability | Owner | Note |
| :--- | :--- | :--- |
| Data export, correction, deletion | `admin` | Self-service, not support tickets |
| Onboarding | `anatomy` presets + `identity` tier transition | Not a separate module |
| Age gate mechanism | `tagging` holds the flag; the gate itself defers | `OQ-001` |
| Billing | — | Deferred with monetisation |
| Abuse and harassment | `moderation` + `live` + `rooms` | Distributed deliberately; consent framing |
| Backup and retention | `media`, `admin` | `OQ-036`, `OQ-074` |

## 4. Overlaps resolved

Nine pairs looked duplicative. Six have a clean boundary, stated below. Three remain genuinely
unresolved and are tracked as open questions rather than papered over.

### Resolved

| Pair | Boundary |
| :--- | :--- |
| `statistics` (L1) / `statistics-engine` (L2) | Policy versus mathematics. L1 decides thresholds, cohorts and presentation contracts; L2 computes and has no I/O, no state and no identity. The split exists so the same number is produced by construction wherever it appears. |
| `tagging` / `moderation` | Detection versus enforcement. `tagging` produces integrity signals; `moderation` acts on them. Deliberate mis-tagging is a consent violation and routes to `moderation` as one. |
| `consent` / `moderation` | Recording versus enforcement. Consent binds terms at creation; moderation resolves what was already recorded. If moderation's ambiguous queue is large, the consent model upstream is underspecified. |
| `visualizer` / `avatar` | One shared parametric geometry, two outputs. `visualizer` renders for viewing; `avatar` rigs for inhabiting. Sharing the geometry is a correctness property — the two cannot disagree. |
| `identity` / `verification` | Actors versus measurements. `identity` establishes who is acting; `verification` grades how well a measurement is established. **There is no verified-person status**, and this boundary is what guarantees it. |
| `telemetry` / `admin` | System versus operator. `telemetry` measures the system and carries no subject; `admin` operates and is audited when it touches anything that does. |

### Unresolved — tracked, not merged

| Pair | Problem | Tracked as |
| :--- | :--- | :--- |
| `live` / `rooms` / `social-vr` | Split by medium and persistence: text and streams versus embodied presence, open versus invited, persistent versus ephemeral. Where a group text room and an invited VR session become the same product with different clients, they should unify. | `OQ-056` |
| `spaces` / `live` | Do channels live inside spaces, or does `spaces` subsume them? Both currently claim membership and context. | `OQ-060` |
| `spaces` / `education` | Context versus content — clean in principle. In practice an education space and the education module both claim the anonymous-tier access rule. | `OQ-060` (shares a resolution) |

## 5. Dependency direction check

The stated rule is that L1 never depends upward and L2 never calls out to L3–L5. Verified against
every module page's interfaces section: **no violations.**

Two near-misses worth recording:

- `statistics` (L1) consumes `statistics-engine` (L2). This is downward, not upward — L2 is the
  compute layer beneath L1, not above it. The numbering reads as a hierarchy and is a grouping.
- `learning` (L2) consumes `consent` (L1). Correct direction, and it makes `learning` the module
  that owns the cross-store write path — which is why `OQ-021` lands there.

## 6. Cross-cutting obligations every module answered

Two obligations propagate from L1 to everything holding derived data. Both were checked page by
page:

**Derived-data deletion** ([`consent`](../concept/l1-core/consent.md)). Every module holding
derived data owes a deletion path: `media` enumerates derivatives, `body-vector` evicts cached
neighbourhoods, `knowledge-graph` removes edges while preserving that a withdrawal occurred,
`avatar` revokes exports and states it cannot recall downloads, `search` caches per-subject or not
at all. Completion across three stores plus object storage plus backups remains `OQ-074`.

**Scope inside the query, never applied to results.** Stated in `knowledge-graph` for traversal and
generalised in `search` to every store. Post-filtering has already read what it removes, and
counts, ranking and timing leak. This is the rule most likely to be violated by an otherwise
reasonable implementation.

## 7. Outcome

| | Count |
| :--- | :--- |
| Modules described | 31 |
| Recovered sections with an owner | 16 of 19 (§13, §14, §15 deferred by decision) |
| Gaps found | 1 (§12) |
| Gaps closed | 1 |
| Overlaps resolved | 6 |
| Overlaps tracked as open questions | 3 |
| Open questions raised | 78 |
| Dependency-direction violations | 0 |
