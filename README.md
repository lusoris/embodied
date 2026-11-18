# emBodied

emBodied is the concept for a private, international adult platform for the realistic modelling,
representation, discussion and experience of human bodies, sexuality and intimacy.

**Consent is the only hard boundary.**

The name is the English word *embodied*, pronounced the same way (em-BOD-eed); the capital B
marks the word *body* inside it.

## What this repository holds

Planning documents only: the master concept, one page per module, the architectural decision
records and the open questions. There is no product code, no running service, no dataset and no
media; the only executable files are repository tooling: the file-type gate and its tests, which
`make verify-all` runs, and the secret-scan replay, which the docs workflow runs. Nothing here
collects or stores data about anyone.

## Adult subject matter and safety scope

- The platform described here is for adults only. The documents discuss anatomy, sexuality,
  sexual health and pornography in plain, descriptive language.
- The repository is text only. It contains no images, video, audio or other media, and no
  personal data about any real person.
- Consent is the platform's only hard boundary: every artifact carries the consent terms under
  which it may be seen, and a revoked grant reaches every copy derived from it
  ([ADR-0012](docs/adr/0012-consent-as-only-hard-boundary.md)).
- Age verification, identity checks, jurisdiction and hosting are not decided yet; see
  [OPEN-QUESTIONS.md](docs/design-basis/OPEN-QUESTIONS.md).

## Where to start

| Document | Purpose |
| :--- | :--- |
| [MASTER_CONCEPT.md](docs/MASTER_CONCEPT.md) | Canonical concept. What the platform is and what it refuses to be. |
| [docs/concept/](docs/concept/README.md) | The module architecture — one page per module. |
| [docs/adr/](docs/adr/README.md) | Architectural decision records. |
| [docs/design-basis/OPEN-QUESTIONS.md](docs/design-basis/OPEN-QUESTIONS.md) | What is not decided yet, and what would close it. |

The planned stack — a Go control plane, a Rust compute kernel and a SvelteKit interface over
PostgreSQL, Qdrant and Memgraph — is decided in
[ADR-0001](docs/adr/0001-go-rust-svelte-split.md) and
[ADR-0002](docs/adr/0002-relational-vector-graph-persistence.md).

## Licensing

Split licensing, REUSE compliant
([ADR-0011](docs/adr/0011-split-licensing-reuse.md)):

- **EUPL-1.2** ([LICENSE](LICENSE)) — code, schemas, configuration and scripts
- **CC BY-SA 4.0** — documentation, prose and architectural decision records

`REUSE.toml` maps each path to its licence; the full texts are in `LICENSES/`. Run `reuse lint`
to verify.

## Status

Concept stage. No implementation yet. The roadmap — phasing, jurisdiction, age
verification, payments — is deliberately not decided; see
[OPEN-QUESTIONS.md](docs/design-basis/OPEN-QUESTIONS.md).

<!-- praetor:readme-governance:start -->
[![HISS Adopted][praetor-hiss-badge]][praetor-hiss-agents]

Praetor manages this repository's declared governance policy. This managed
block records adoption state; it is not a verification certificate.

**Verification**: `make verify-all` runs the repository's configured
verification cascade.

**HISS Audit**: `praetorctl audit` enforces policy, generated-surface
integrity, and the debt ratchet.

**Context Sync**: `praetorctl compile-context --verify` verifies every
generated agent context against `AGENTS.md`.

**Debt Baseline**: `.standards-baseline.json` anchors the debt ratchet at
0 recorded infractions; audit forbids growth.

[praetor-hiss-badge]: https://img.shields.io/badge/Standards-HISS%20Adopted-blue
[praetor-hiss-agents]: https://github.com/lusoris/embodied/blob/HEAD/AGENTS.md
<!-- praetor:readme-governance:end -->
