# Wiki

**Status:** unresolved — see `OQ-002`.

The recovered concept's §17 declared the wiki the canonical source, with `docs/` as role views and
AI in a read-and-propose role.

That conflicts with the governance this project adopted. Praetor HISS-16 makes `AGENTS.md` the
canonical agent harness, and the house pattern across the sibling repositories puts prose in
`docs/` with MkDocs publishing. Two canonical sources is one too many — it is the exact drift
problem the compiled-harness model exists to prevent.

## Proposed resolution

`docs/` is canonical. The wiki becomes a **published surface built from it** rather than a separate
authority — the same relationship `CLAUDE.md` has to `AGENTS.md`.

This is recorded as `OQ-002` rather than silently overridden, because §17 was an explicit decision
in the recovered concept and reversing it is the owner's call.

## Until that is decided

Nothing canonical lives here. Write concept material in
[docs/concept/](../docs/concept/README.md), decisions in [docs/adr/](../docs/adr/README.md), and
role-specific views under `docs/<role>/`.

See [OPEN-QUESTIONS.md](../docs/design-basis/OPEN-QUESTIONS.md).
