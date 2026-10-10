# emBodied

A private, international adult platform for the realistic modelling, representation,
discussion and experience of human bodies, sexuality and intimacy.

**Consent is the only hard boundary.**

## Where to start

| Document | Purpose |
| :--- | :--- |
| [MASTER_CONCEPT.md](docs/MASTER_CONCEPT.md) | Canonical concept. What the platform is and what it refuses to be. |
| [docs/concept/](docs/concept/README.md) | The module architecture — one page per module. |
| [docs/adr/](docs/adr/README.md) | Architectural decision records. |
| [docs/design-basis/OPEN-QUESTIONS.md](docs/design-basis/OPEN-QUESTIONS.md) | What is not decided yet, and what would close it. |

## Stack

| Layer | Technology |
| :--- | :--- |
| Control plane | Go 1.27+ (`cmd/`, `internal/`) |
| Compute kernel | Rust 1.85+ (`crates/`) |
| Interface | SvelteKit / Svelte 5 Runes (`ui/`) |
| Records | PostgreSQL |
| Vectors | Qdrant |
| Graph | Memgraph |

Governance follows [Praetor](https://github.com/lusoris/praetor) HISS-16. `AGENTS.md` is the
canonical agent harness; `CLAUDE.md` and the other vendor targets are compiled from it.

## Licensing

Split-licensed under the `cordanaLLM` model, REUSE v3.2 compliant:

- **EUPL-1.2** — all code, schemas, configuration and scripts
- **CC BY-SA 4.0** — all documentation, prose and architectural decision records

Run `reuse lint` to verify.

## Status

Concept stage. No implementation yet. The roadmap — phasing, jurisdiction, age
verification, payments — is deliberately not decided; see
[OPEN-QUESTIONS.md](docs/design-basis/OPEN-QUESTIONS.md).
