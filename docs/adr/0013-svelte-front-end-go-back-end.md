# ADR-0013: SvelteKit front end, Go back end

- **Status:** Proposed
- **Date:** 2026-11-18
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** Would supersede ADR-0001 on acceptance; allocation of the Rust
  parts pending decision embodied-rust-parts-go-20261118

## Context

The owner's direction on 2026-11-18 (paraphrased) is to use Svelte for the front end and Go for the
back end. The remaining question is what happens to the work previously assigned to Rust.

ADR-0001 accepted three languages: a Go control plane in `cmd/` and `internal/`, a Rust compute
kernel in `crates/`, and a SvelteKit / Svelte 5 interface in `ui/`. It assigns everything
quantitative to the Rust kernel and compiles visualizer geometry to WASM. SvelteKit runs
full-stack, with session authority in Go.

At commit `a729a87f0b0c3f2b71b02a85ee2bc0330ed11642`, checked on 2026-11-18, the tracked tree has
65 files, including 58 Markdown files and no source files. There is no Go, Rust or TypeScript
code to remove. This proposal changes the planned allocation; it does not migrate an implementation.

## Decision

Propose the following application stack, with the seven Rust allocations below left open:

| Layer | Language | Scope |
| :--- | :--- | :--- |
| Interface | SvelteKit / Svelte 5 Runes (`ui/`) | Full-stack SSR, routing, form actions, rendering; session authority stays in Go, unchanged from ADR-0001 |
| Back end | Go (`cmd/`, `internal/`) | API, sessions, orchestration, platform modules |

### Parts ADR-0001 gave the Rust kernel

ADR-0001's quantitative-kernel allocation is detailed by the existing concept pages and subsequent
ADRs. The table includes learning and the geometry used by the visualizer, avatar and embodiment.
The Go paths are candidates, not dependency or implementation decisions.

| # | Part | ADR-0001 placement | Go path if Go takes it | Open point |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Vectors | `crates/embodied-vector`; SIMD similarity via `simsimd`, Qdrant store | `github.com/qdrant/go-client` v1.20.1; local numerical implementation pending | Go SIMD is experimental; Qdrant already performs similarity search server-side. Allocation of projection and local distance work remains open. |
| 2 | Graph | `crates/embodied-graph`; Memgraph store | Neo4j Go driver over Bolt, v5.28.6 or v6.4.0 | Allocation of graph logic and driver selection |
| 3 | Statistics | `crates/embodied-stats`, called by Go `internal/statistics` | `gonum.org/v1/gonum` v0.17.0 | Allocation of statistical logic |
| 4 | Simulation | `crates/embodied-sim`; WASM for client and server | Go WASM targets; model implementation pending | Shared client/server WASM model and the 2026-10-10 shared-library direction |
| 5 | Learning | `crates/embodied-learn` | No Go library established by the available evidence | Implementation and dependency allocation |
| 6 | Device control | `crates/embodied-device`, using the Buttplug Rust library | `github.com/diamondburned/go-buttplug` v0.0.3, a community Intiface WebSocket API client | Buttplug client maturity and protocol version; protocol version support is not verified. |
| 7 | Visualizer, avatar and embodiment geometry | Rust geometry in `crates/`, compiled to WASM | Go WASM targets; geometry implementation pending | Shared client/server WASM model and the 2026-10-10 shared-library direction |

The Go paths were checked on 2026-11-18. On a Go 1.27.4 toolchain, `go tool dist list` includes
`js/wasm` and `wasip1/wasm`. Target support alone does not settle how the shared simulation and
geometry model would be implemented.

Go 1.27's `simd/archsimd` is experimental, AMD64-only, requires `GOEXPERIMENT=simd`, and is outside
the Go 1 compatibility promise. It does not resolve the vector allocation by itself.

The Qdrant client is Apache-2.0 licensed and was pushed on 2026-11-18. The Neo4j driver is
Apache-2.0 licensed; Memgraph documents it as the Go client over Bolt. Gonum is BSD-3-Clause
licensed and was pushed on 2026-11-17. The community Go Buttplug client is ISC licensed, with its
last commit on 2025-12-01; its Buttplug protocol version support has not been verified.

The fleet direction dated 2026-10-10 (paraphrased) calls for extracting shared Rust physics,
geometry and rendering into a common library when a second project needs the same component.
That direction must be reconciled with the simulation and geometry allocation.

Allocation of these seven parts is not decided by this record. It waits for decision
`embodied-rust-parts-go-20261118`. Until then this record stays **Proposed** and ADR-0001 stays
**Accepted**.

## Consequences

If Go takes all seven parts, there are two toolchains instead of three, no Go-Rust FFI boundary,
and only the `go-service` and `frontend-svelte` Praetor flavors. The Node runtime stays in
production because SvelteKit remains full-stack.

If some parts stay in Rust, the Go-Rust FFI boundary and the `rust-systems` flavor stay for those
parts. The pending decision must state which parts retain that boundary.

On acceptance, follow-up records must supersede ADR-0010's device-control decision and, if vectors
move, the Rust line of ADR-0009. Documentation updates must cover `README.md:38`,
`docs/MASTER_CONCEPT.md:188` and lines 216 to 239, `docs/concept/README.md:28`, and
`docs/dev/README.md:16` and line 30. The concept-page owner lines also need reconciliation:

- `docs/concept/l2-intelligence/body-vector.md:3`
- `docs/concept/l2-intelligence/knowledge-graph.md:3`
- `docs/concept/l2-intelligence/statistics-engine.md:3`
- `docs/concept/l1-core/statistics.md:3`
- `docs/concept/l2-intelligence/simulation.md:3`
- `docs/concept/l2-intelligence/learning.md:3`
- `docs/concept/l4-presence/device.md:3`
- `docs/concept/l3-expression/visualizer.md:3`
- `docs/concept/l3-expression/avatar.md:3`
- `docs/concept/l4-presence/embodiment.md:3`

These are follow-ups on acceptance; this proposal does not amend those documents or any existing
ADR body.

## Alternatives considered

**Keep ADR-0001 unchanged.** Retains the accepted three-language allocation and its shared Rust
WASM model. It leaves the owner's revised stack direction unresolved.

**Go with Rust kept only for device control and WASM geometry.** Retains the direct Buttplug Rust
dependency and Rust geometry while moving the other kernel responsibilities to Go. Three
toolchains and the FFI boundary remain; simulation and geometry must still share one model.

**Go only, including WASM geometry.** Allocates all seven parts to Go and removes the Go-Rust
boundary. Go's WASM targets provide a candidate path, while the shared model, experimental SIMD,
community device client and shared-library direction still need resolution.

## References

- User direction, 2026-11-18, stack (paraphrased): use Svelte for the front end and Go for the back
  end.
- Fleet direction, 2026-10-10, shared components (paraphrased): extract common Rust physics,
  geometry and rendering into a shared library once a second project needs the same component.
- [ADR-0001](0001-go-rust-svelte-split.md) — accepted language allocation and shared WASM model
- [ADR-0002](0002-relational-vector-graph-persistence.md) — Qdrant and Memgraph persistence
- [ADR-0009](0009-learned-body-vector.md) — learned body-vector
- [ADR-0010](0010-buttplug-device-control.md) — direct Buttplug Rust dependency
- [Memgraph Go client documentation](https://memgraph.com/docs/client-libraries/go)
- [Qdrant Go client](https://github.com/qdrant/go-client)
- [Neo4j Go driver](https://github.com/neo4j/neo4j-go-driver)
- [Gonum](https://github.com/gonum/gonum)
- [Community Go Buttplug client](https://github.com/diamondburned/go-buttplug)
