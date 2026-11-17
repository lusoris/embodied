# emBodied for developers

A **view** into the canonical concept. Authority lives in
[MASTER_CONCEPT.md](../MASTER_CONCEPT.md), [docs/concept/](../concept/README.md) and
[docs/adr/](../adr/README.md).

## Read first

1. [MASTER_CONCEPT.md](../MASTER_CONCEPT.md) — what the platform is
2. [docs/concept/README.md](../concept/README.md) — the module map and dependency direction
3. [docs/adr/README.md](../adr/README.md) — the decisions and why
4. [OPEN-QUESTIONS.md](../design-basis/OPEN-QUESTIONS.md) — what is not decided

## Stack

A Go control plane, a Rust compute kernel and a SvelteKit interface, over PostgreSQL, Qdrant and
Memgraph. The decisions hold the versions, directories, scope of each layer and store, and the
boundaries between them; this page does not repeat them:

- [ADR-0001](../adr/0001-go-rust-svelte-split.md) — languages, layers, the kernel boundary and
  session authority
- [ADR-0002](../adr/0002-relational-vector-graph-persistence.md) — the three stores and what each
  holds

## Governance

Praetor HISS-16. `AGENTS.md` is canonical; `CLAUDE.md` and the other vendor targets are compiled
from it by `standardsctl compile-context` — **do not edit them directly**.

Scaffolding comes from `standardsctl adopt`, which applies the `go-service`, `rust-systems` and
`frontend-svelte` flavors. Do not hand-write what adoption generates.

Relevant invariants: no recursion (HISS-01), bounded loops and explicit I/O deadlines (HISS-02),
McCabe ≤ 10 and functions ≤ 75 LOC (HISS-04), zero unchecked errors and no `unwrap` in production
(HISS-07), zero warnings (HISS-10), and positive/negative/boundary tests on every public API
(HISS-15).

## Rules that constrain how you write code here

These are not style preferences. Each exists because violating it breaks a stated guarantee.

1. **Consent is bound to artifacts, not checked at the door.** There is no ingest path producing an
   unbound artifact. [ADR-0012](../adr/0012-consent-as-only-hard-boundary.md)
2. **Scope goes inside the query, never applied to results.** Post-filtering has already read what
   it removes; counts, ranking and timing leak.
3. **Enumerate every derivative.** Transcodes, thumbnails, embeddings, graph edges, avatars,
   exports and caches. Revocation needs a complete list.
4. **Cache per subject or not at all.** A shared result cache is a cross-consent leak waiting for
   a hit.
5. **Consent checks must be cheap.** If checking is expensive, some path will skip it — so the
   cost of the check is a safety property.
6. **Logs are a data store.** No identifiers beyond incident need, no content or feature names in
   span names or metric labels.
7. **"We cannot say" is a valid return.** Statistics returns typed insufficiency rather than
   panicking or guessing. A distribution with too little data has a correct answer and it is not a
   number.
8. **Never display a figure without its uncertainty.** `statistics` enforces this as a
   `presentation_contract`, in data, not in review.

## Local gate

```bash
make verify-all        # lint, test, check-hiss16, check-reuse
reuse lint             # split licensing: EUPL-1.2 code, CC BY-SA 4.0 docs
mkdocs build --strict  # docs must build with no broken links
```

Run it before pushing. Do not use `--no-verify`, `LEFTHOOK=0`, or touch `.git/hooks`.

## Conventions

Conventional Commits. Smallest coherent change. Every file you touch leaves lint-clean and
warning-free. One ADR per decision, append-only numbering; Accepted ADRs are frozen — write a
superseding one rather than editing.
