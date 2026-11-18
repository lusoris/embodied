# emBodied for AI agents

A **view** into the canonical concept, for agents working in this repository.

## Authority

`AGENTS.md` at the repository root is your operating harness and it is canonical. `CLAUDE.md`,
`.cursor/rules/*.mdc`, `.windsurfrules`, `.gemini/GEMINI.md` and `.github/copilot-instructions.md`
are **compiled from it** by `make compile-context`. Never edit a compiled target — the edit
will be overwritten and will have created a second authority in the meantime.

The recovered concept's §17 described this role as "read and propose". That remains accurate and
is sharpened below.

## Read before substantial work

1. [MASTER_CONCEPT.md](../MASTER_CONCEPT.md) — what the platform is
2. [docs/concept/README.md](../concept/README.md) — module map, dependency direction
3. [docs/adr/README.md](../adr/README.md) — decisions and rationale
4. [OPEN-QUESTIONS.md](../design-basis/OPEN-QUESTIONS.md) — what is undecided
5. [docs/dev/README.md](../dev/README.md) — the eight rules that constrain code here

Do not re-derive the architecture from the source tree. It is written down.

## What you may and may not change

| | |
| :--- | :--- |
| **Propose freely** | Implementation, tests, docs, new ADRs in `Proposed` status |
| **Never without instruction** | An Accepted ADR's body. Write a superseding ADR instead — the solo-repo relaxation in [docs/adr/README.md](../adr/README.md) applies to the owner, not to you |
| **Never** | Compiled vendor harnesses, `.standards.yaml` strictness reductions, `--no-verify`, `LEFTHOOK=0`, `.git/hooks` |

Strictness in `.standards.yaml` can only be increased, never reduced.

## Domain constraints you must not optimise away

This repository's subject matter makes several ordinary engineering reflexes wrong. Each of these
exists because violating it breaks a stated guarantee, and each looks like a reasonable
simplification from inside the code:

- **Do not add a content classifier that decides.** Assisted tagging *proposes*; the uploader
  confirms. The platform makes no editorial porn/medical/artistic judgement
  ([ADR-0005](../adr/0005-no-editorial-classification.md)).
- **Do not filter results after retrieval.** Scope goes inside the query. Post-filtering has
  already read what it removes.
- **Do not introduce a shared cache** across subjects, or a standing export authorisation.
- **Do not add engagement mechanics** — streaks, scores, rankings, activity feeds, re-engagement
  notifications. These are forbidden by [progress](../concept/l5-community/progress.md) and
  [notification](../concept/cross-cutting/notification.md), not merely absent.
- **Do not add a gendered profile type**, or a "default" anatomy, however convenient for a form.
  ([ADR-0003](../adr/0003-anatomy-first-feature-model.md))
- **Do not widen operator access** to make support easier.
- **Do not display a computed figure without its uncertainty.**
- **Do not let a measurement be rejected, clamped or corrected** for implausibility. Flag it and
  keep it — real bodies occupy the tails.
- **Do not merge the reference curve and the user overlay**, or give `reference` a read path into
  user data.

If a task seems to require one of these, that is a signal to raise the conflict, not to proceed.

## Verification before you claim done

```bash
make verify-all
reuse lint
mkdocs build --strict
```

Report failures with their output. Do not describe work as complete that has not passed.
