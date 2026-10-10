# ADR-0001: Go control plane, Rust compute kernel, Svelte 5 interface

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

The recovered concept named React and Go. React was withdrawn during the replan; the remaining
question was how to divide work between languages given emBodied's two very different halves.

One half is an ordinary platform: authentication, profiles, media, chat, moderation, consent
resolution. Expressive networking and fast iteration matter; raw numerical performance does not.

The other half is quantitative and sustained: vector similarity over embeddings, graph traversal,
percentile and uncertainty mathematics, and a geometric-plus-biomechanical simulation model. Memory
control, determinism and predictable latency matter, and the same geometry must also run in the
browser.

`cordanaLLM/Tribunus` had already resolved the identical split for the same ecosystem, and the
Praetor governance harness already ships `go-service`, `rust-systems` and `frontend-svelte`
archetypes, so all three legs are covered by existing tooling rather than requiring new
scaffolding.

## Decision

Three languages, split by role, in one monorepo:

| Layer | Language | Scope |
| :--- | :--- | :--- |
| Control plane | Go 1.27+ (`cmd/`, `internal/`) | API, sessions, orchestration, platform modules |
| Compute kernel | Rust 1.85+ (`crates/`) | Vectors, graph, statistics, simulation, device control |
| Interface | SvelteKit / Svelte 5 Runes (`ui/`) | SSR, routing, form actions, rendering |

The Rust kernel owns everything quantitative. Go owns no numerical logic beyond assembling calls
into the kernel. Visualizer geometry compiles to WASM so client and server share one model.

SvelteKit runs full-stack — SSR, sessions at the edge, form actions — but **session authority
stays in Go**. The UI holds a cookie; it does not hold authority.

## Consequences

The quantitative core is isolated, testable in isolation and free of I/O, which makes HISS-15
three-dimensional testing tractable — boundary cases in statistics are tails and empty cohorts,
and they have defined correct answers.

Shared WASM geometry means what a user is shown and what the platform computed cannot diverge. It
also allows the anonymous tier to render measurements client-side without transmitting them.

Costs: three toolchains, three linter stacks and an FFI boundary between Go and Rust that will need
care around ownership and error propagation. A Node runtime enters production because SvelteKit
runs full-stack.

The polyglot repository needs three Praetor flavors applied to one monorepo, which is an
adoption-time question rather than a design one.

## Alternatives considered

**Go only.** Simpler to operate, but the simulation and vector work would be written in a language
without the memory control for it, and there would be no path to sharing geometry with the browser.

**Rust only.** Attractive for the compute half and slow for the platform half, which is the larger
volume of ordinary code.

**Svelte as a static SPA with no server runtime.** Removes Node from production and loses SSR,
first-paint quality and form actions. Rejected in favour of full-stack SvelteKit.

## References

- User direction, 2026-09-16 (paraphrased): React is no longer wanted; the stack is now Svelte,
  Rust and Go.
- User decision, 2026-09-16, backend split (paraphrased): both languages, split by role.
- User decision, 2026-09-16, frontend (paraphrased): SvelteKit as the full-stack framework.
- User decision, 2026-09-16, kernel scope (paraphrased): vectors, graph, statistics and
  simulation.
- `cordanaLLM/Tribunus` `architecture-v2.md` §2: "The Go Control Plane acts as the state manager
  and workflow executor" / "The Rust Compute Kernel handles memory-intensive and vector-matching
  operations"
- `cordanaLLM/Tribunus` `tribunus-description-v2.md`: "Core Technologies: Go 1.27+ (Control
  Plane), Rust 1.85+ (Graph Compute Kernel), Svelte 5 (UI Layer)"
- `lusoris/praetor` `internal/flavor/definitions.go` — `go-service`, `rust-systems`,
  `frontend-svelte` flavors
