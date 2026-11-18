# ADR-0013: WebAssembly boundary between Go and the Rust kernel

- **Status:** Proposed
- **Date:** 2026-11-18
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** — (extends ADR-0001; does not supersede it)

## Context

The owner's stack direction of 2026-11-18 (paraphrased) is a Svelte front end and a Go back end.
The owner's kernel decision of the same date (paraphrased) retains all seven Rust parts:
vectors, graph, statistics, simulation, learning, device control and WASM geometry. SvelteKit and
Go surround the Rust kernel; the quantitative allocation accepted in ADR-0001 remains in force.

ADR-0001 leaves the form of the Go-to-Rust boundary open and identifies ownership and error
propagation as concerns. It requires an I/O-free quantitative kernel and shared WASM geometry.
The simulation and visualizer concept pages require the same parametric model to render in the
browser and compute on the server.

At commit `a729a87f0b0c3f2b71b02a85ee2bc0330ed11642`, checked on 2026-11-18, the tracked tree has
65 files, including 58 Markdown files and no source files. This record specifies a boundary for
the planned implementation; there is no Go, Rust or TypeScript code to migrate.

The runtime and binding options were checked on 2026-11-18, between 09:45 and 09:57.
A spike at 09:53 used Rust 1.98.1, Go 1.27.4 and wazero v1.12.0 with `CGO_ENABLED=0`.
A Rust `cdylib` targeting `wasm32-unknown-unknown` with `-C target-feature=+simd128`, plain
`extern "C"` allocation, free and dot-product exports, and no wasm-bindgen produced a
23,355-byte module with no imported functions or memories. The dot product of [1,2,3] and
[4,5,6] returned 32. A length mismatch caused a Rust panic, returned to Go as
`wasm error: unreachable` with a WASM stack trace; the Go process survived and a fresh instance
returned 32. An endless export with a 200 ms context deadline returned after 200 ms with
`module closed with context deadline exceeded`. This spike has no tracked path.

## Decision

### 1. Retain the stack and quantitative ownership

| Layer | Language | Scope |
| :--- | :--- | :--- |
| Control plane | Go 1.27+ (`cmd/`, `internal/`) | API, sessions, orchestration, platform modules; assembles kernel calls, owns no numerical logic |
| Compute kernel | Rust 1.85+ (`crates/`) | Vectors, graph, statistics, simulation, learning, device control and geometry |
| Interface | SvelteKit / Svelte 5 Runes (`ui/`) | Full-stack SSR, routing, form actions and rendering; session authority stays in Go |

### 2. Keep all seven kernel parts in Rust

Every server-side kernel call uses a WebAssembly module run in process by the Go back end with
wazero. Qdrant and Memgraph remain the vector and graph stores under ADR-0002; Go handles I/O
around the import-free kernel computations.

| # | Part | Crate | Runs in | Reached from Go by |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Vectors | `embodied-vector` | Server; Qdrant remains the store | Kernel module through wazero |
| 2 | Graph | `embodied-graph` | Server; Memgraph remains the store | Kernel module through wazero |
| 3 | Statistics | `embodied-stats` | Server; called by Go `internal/statistics` | Kernel module through wazero |
| 4 | Simulation | `embodied-sim` | Browser and server, the same module bytes in both | Kernel module through wazero on the server |
| 5 | Learning | `embodied-learn` | Server | Kernel module through wazero |
| 6 | Device control | `embodied-device` | Client only, per ADR-0010 | No Go-to-Rust call; session grants and bounded intent as API data |
| 7 | Visualizer, avatar and embodiment geometry | Rust geometry in `crates/` | Browser and server, the same module bytes in both | Kernel module through wazero on the server |

Device discovery, pairing and connection stay client-side under ADR-0010. The Rust device crate
runs there, with no Go-to-Rust boundary in hardware actuation; `OQ-043`, embedding versus
Intiface Central, remains open.

### 3. Use one WebAssembly boundary

1. Shared and server-side modules target `wasm32-unknown-unknown` with `simd128` and import
   nothing. The Go loader refuses any module with an import, checking ADR-0001's I/O-free
   kernel requirement at load time.
2. Exports are plain C-ABI functions over module linear memory: allocate, free, pointers and
   lengths, without wasm-bindgen, so browser and Go instantiate the same bytes. The back end
   serves the browser the exact module it runs, named by its SHA-256, and serves no other
   version. Each request for a shared computation names the hash the browser loaded. When a
   deployment has changed the module, the back end refuses that request with a version-mismatch
   status, and the browser reloads the module before computing again, so both sides compute
   with identical bytes.
3. Data crosses by copy: Go writes inputs into module memory and reads results out. Neither
   side retains a pointer into the other's memory.
4. Expected failures return a status code with an error record; a Rust panic aborts, becoming
   a WASM trap that wazero returns as an error. Go discards that instance and creates a fresh one.
5. Every call runs under a context deadline with `WithCloseOnContextDone`, implementing
   HISS-02's explicit timeouts; cancellation closes the module and returns `sys.ExitError`.
   Go discards that closed instance and creates a fresh one, as for a trap.
6. wazero's `Call` is not goroutine-safe, so the back end maintains an instance pool with
   one call per instance at a time.
7. Each module exports an ABI version that the loader checks.
8. The module hash identifies code only. Model data crosses as input: the back end supplies the
   `model_version` and `parameter_set` for each shared computation, the browser computes with
   the values it received, and each result stores both with the module hash. This follows the
   Simulation page, where a result stores the model version that produced it.

The baseline checked here is wazero v1.12.0 (`github.com/tetratelabs/wazero`, Apache-2.0),
whose Go module checksum is `h1:DuWcpNu/FzgEXgGBDp8J1Spc+CWOvvtvVyjKlaZopYU=`.
Its default `CoreFeaturesV2` supports WebAssembly Core 1.0 and 2.0, including 128-bit SIMD.
Threads, tail calls, extended-const and exception handling are experimental; memory64 is absent.
For the Rust target, `rustc --target wasm32-unknown-unknown --print cfg` reports
`panic="abort"`, which accounts for the spike's panic becoming a trap.

### 4. Preserve the shared-library direction

The fleet direction of 2026-10-10 (paraphrased) applies per kernel part: extract common Rust
physics, geometry and rendering into a shared library once a second project needs the same
component. Moving a crate does not change this boundary.

## Consequences

Gains:

- No cgo: wazero is written in Go, so the Go build stays pure Go.
- One binding form covers every server-side kernel call.
- The module hash gives browser and server one code identity; with `model_version` and
  `parameter_set` as inputs, both hosts compute the same model.
- A kernel panic or trap returns an error without crashing the Go back end, as the spike showed.
- Rejecting imports enforces the kernel's freedom from I/O.

Costs:

- SIMD is 128-bit; native AVX and Neon paths are unavailable inside a module.
- Each call copies data across the boundary.
- Linear memory is 32-bit, at most 4 GiB per instance.
- Modules use no threads; parallelism comes from the instance pool.
- SimSIMD 6.5.16 builds for this target with no imports, but its SIMD paths target x86 and Arm,
  so it runs its serial path in a module. The vector crate needs its own `simd128` path or
  another library; measure that choice when the crate exists.

Revisit when a benchmark on representative data shows a kernel part missing its latency budget
under wazero while a native build meets it. That part would receive a native C-ABI binding,
with a cbindgen header, cgo and every export catching panics, through a superseding record.
Also revisit when wazero ships memory64 or threads outside its experimental package.

On acceptance, change the Go-to-kernel arrow at `docs/MASTER_CONCEPT.md:225` from `FFI / IPC`
to `WASM (wazero)`. Concept owner lines stay Rust. The Praetor flavours remain `go-service`,
`rust-systems` and `frontend-svelte`, as in ADR-0001. This record amends no existing ADR body.

## Alternatives considered

**Native C ABI with cbindgen and cgo.** cbindgen 0.29.4 generates C headers from Rust; cgo
would call a native library. Deferred pending the latency trigger: cgo requires pinned Go
memory for pointers passed to C and forbids retaining those pointers after a call unless they
remain pinned with `runtime.Pinner`; `runtime/cgo.Handle` can carry Go values safely.
Rust's non-unwind `extern "C"` ABI aborts on uncaught unwinds, as documented for Rust 1.81.0,
so every native export would need to catch panics to protect the back end.

**UniFFI with uniffi-bindgen-go.** Generated bindings would bridge Go and a compiled Rust
library. The separate pre-1.0 Go generator's v0.7.x targets uniffi-rs 0.31.0, whereas the
checked UniFFI release is 0.32.2; it requires Rust 1.87+ and finds the compiled library via
`LD_LIBRARY_PATH`. This does not provide the selected shared-module boundary.

**Separate Rust kernel service over gRPC with tonic.** tonic 0.14.9 supplies gRPC for Rust.
This would give the I/O-free kernel a network shell and add serialisation and a deployable;
the in-process spike demonstrates a boundary without that service.

**WebAssembly for shared models, cgo for the rest.** This combines the measured WASM path with
native calls for other parts. It creates two binding forms before a benchmark establishes a need.

**Go reimplementation.** Moving quantitative work into Go is ruled out by the owner's
2026-11-18 kernel decision (paraphrased): all seven parts stay Rust.

wasm-bindgen is excluded from shared modules: a measured build with version 0.2.130 imported
four functions from `__wbindgen_placeholder__` and `__wbindgen_externref_xform__`. Its CLI
rewrites the module and generates JavaScript glue; a plain Go host supplies neither.

## References

- Owner direction, 2026-11-18, stack (paraphrased): use Svelte for the front end and Go for the
  back end.
- Owner decision, 2026-11-18, kernel parts (paraphrased): retain the Rust kernel from ADR-0001;
  vectors, graph, statistics, simulation, learning, device control and WASM geometry all stay
  Rust, with SvelteKit and Go around the kernel; the shared-library direction of 2026-10-10
  still applies when a second project needs a kernel part.
- Fleet direction, 2026-10-10, shared components (paraphrased): extract common Rust physics,
  geometry and rendering into a shared library once a second project needs the same component.
- [ADR-0001](0001-go-rust-svelte-split.md) — stack, quantitative ownership and open boundary
- [ADR-0002](0002-relational-vector-graph-persistence.md) — Qdrant and Memgraph stores
- [ADR-0009](0009-learned-body-vector.md) — learned body-vector
- [ADR-0010](0010-buttplug-device-control.md) — client-side device control and `OQ-043`
- [Simulation](../concept/l2-intelligence/simulation.md) — shared parametric model, line 73
- [Visualizer](../concept/l3-expression/visualizer.md) — shared Rust WASM geometry, line 29
- Source checks and spike, 2026-11-18, 09:45–09:57; spike at 09:53, Rust 1.98.1,
  Go 1.27.4, wazero v1.12.0, `CGO_ENABLED=0`; results described in Context, no tracked path.
- [wazero source](https://github.com/tetratelabs/wazero) — v1.12.0, README, LICENSE,
  `api/features.go`, `api/wasm.go:378–380` and `RuntimeConfig.WithCloseOnContextDone`
- [wazero API](https://pkg.go.dev/github.com/tetratelabs/wazero) — runtime configuration
- [WebAssembly specification changes](https://webassembly.github.io/spec/core/appendix/changes.html)
  — Core 1.0 and 2.0 feature context
- [Rust wasm32 intrinsics](https://doc.rust-lang.org/core/arch/wasm32/index.html)
  — direct access to 128-bit SIMD instructions
- [Rust 1.81.0](https://blog.rust-lang.org/2024/09/05/Rust-1.81.0/)
  — non-unwind ABI behaviour
- [cgo](https://pkg.go.dev/cmd/cgo) — Passing pointers
- [cbindgen](https://github.com/mozilla/cbindgen) — v0.29.4, C header generation
- [UniFFI](https://github.com/mozilla/uniffi-rs) — v0.32.2
- [uniffi-bindgen-go](https://github.com/NordSecurity/uniffi-bindgen-go)
  — v0.7.x compatibility and native-library requirements
- [tonic](https://crates.io/crates/tonic) — v0.14.9, gRPC for Rust
- [SimSIMD](https://github.com/ashvardanian/SimSIMD) — v6.5.16, measured serial WASM path
- [wasm-bindgen](https://crates.io/crates/wasm-bindgen) — v0.2.130, measured imports and glue
