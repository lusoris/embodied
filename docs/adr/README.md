# Architecture Decision Records (ADRs)

Records the significant decisions for emBodied — their context, the choice, and the consequences.

## Process

- One ADR per decision, numbered sequentially: `NNNN-short-title.md` (use `template.md`).
- Status flow: **Proposed → Accepted → (Superseded by ADR-NNNN | Deprecated)**.
- Numbering is append-only. Never reuse a number, never renumber. Gaps are acceptable.

## Immutable once Accepted

Once an ADR's status is **Accepted**, its body is **frozen**. To change a decision, write a **new**
ADR that supersedes it (and set the old one's status to "Superseded by ADR-NNNN").

**Solo-repo relaxation:** as this is a single-owner repository, the owner may edit ADRs directly.
Agents may not — an agent changing an Accepted decision writes a superseding ADR.

## References sections

The `## References` section is an audit trail. Cite documents, requirements and open questions
exactly. Cite owner statements in paraphrase, marked "(paraphrased)", with date and topic; their
original wording stays in the private `.workingdir/` ledger and is never committed. (Elsewhere,
paraphrase user input to neutral English.)

## Index

- [0000](0000-record-architecture-decisions.md) — Record architecture decisions *(Accepted)*
- [0001](0001-go-rust-svelte-split.md) — Go control plane, Rust compute kernel, Svelte 5 interface
  *(Accepted)*
- [0002](0002-relational-vector-graph-persistence.md) — Best-of-breed persistence: Postgres, Qdrant,
  Memgraph *(Accepted)*
- [0003](0003-anatomy-first-feature-model.md) — Anatomy-first, gender-independent feature model with
  presets *(Accepted)*
- [0004](0004-two-tier-identity.md) — Two-tier identity: anonymous tier and pseudonymous profile
  tier *(Accepted)*
- [0005](0005-no-editorial-classification.md) — No editorial content classification; descriptors
  with integrity watching *(Accepted)*
- [0006](0006-graded-verification-subsystem.md) — One verification subsystem with graded assertions
  *(Accepted)*
- [0007](0007-user-reference-data-separation.md) — Reference data separated from user data at the
  repository boundary *(Accepted)*
- [0008](0008-population-comparison-as-regional-adaptation.md) — Population comparison framed as
  regional adaptation, not racial category *(Accepted)*
- [0009](0009-learned-body-vector.md) — Learned body-vector as the primary embedding space
  *(Accepted)*
- [0010](0010-buttplug-device-control.md) — Buttplug Rust library for physical device control
  *(Accepted)*
- [0011](0011-split-licensing-reuse.md) — Split licensing: EUPL-1.2 code, CC BY-SA 4.0 docs, REUSE
  v3.2 *(Accepted)*
- [0012](0012-consent-as-only-hard-boundary.md) — Consent as the only hard boundary, bound to
  artifacts *(Accepted)*
- [0013](0013-wasm-boundary-go-rust-kernel.md) — WebAssembly boundary between Go and the Rust kernel
  *(Proposed)*
