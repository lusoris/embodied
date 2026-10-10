# ADR-0000: Record architecture decisions

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

emBodied was recovered as a 2.5 KB concept skeleton that named seventeen topics and decided almost
none of them. The specific failure mode was not missing detail but missing *decisions*: sections
like "Simulation & Compatibility" and "Body data & comparison" listed four bullets each and left
every real choice implicit, so nothing could be built from them and nothing could be argued with.

The replan that followed made a large number of binding decisions in a single session. Without a
record of why each was made, the next person to read the concept — including the owner in six
months — would face the same problem the recovered file created: a statement of what, with no
trace of why, and no way to tell a deliberate choice from an accident.

## Decision

Record architecture decisions as ADRs in `docs/adr/`, following the convention already in use
across the sibling repositories in this collection.

- One ADR per decision, `NNNN-short-title.md`, numbered append-only.
- Status flow Proposed → Accepted → (Superseded | Deprecated).
- `## Context` and `## Alternatives considered` are explanation for future readers, paraphrased
  into neutral English.
- `## References` is an audit trail. Documents are cited by their exact wording. Owner statements
  are cited in paraphrase, marked as such, with date and topic; their original wording stays in
  the private `.workingdir2/` ledger and is never committed.
- Accepted ADRs are frozen. Changing a decision means writing a superseding ADR.

## Consequences

Decisions become reviewable and reversible in a traceable way. A future reader can distinguish
"this was considered and rejected" from "this was never thought about", which is the distinction
the recovered concept lost.

The cost is that decisions become slower to change: amending an Accepted ADR requires a new record
rather than an edit. For a single-owner repository this is friction, which is why the solo-repo
relaxation in `README.md` lets the owner edit directly while holding agents to the superseding
rule.

The convention matches the sibling repositories, so tooling and habits transfer.

## Alternatives considered

**Keep decisions in the concept documents.** Rejected: the concept states what the platform is,
and mixing that with why each choice was made makes both harder to read. The recovered file
demonstrated the failure of having only one document.

**No formal record.** Rejected as the status quo that produced the problem.

## References

- `MASTER_CONCEPT.md` §17 (recovered draft, 2026-01-15): "Wiki = kanonische Quelle / Docs =
  Rollen-Views / AI = Read + Vorschläge"
- User direction, 2026-09-16, on the recovered concept (paraphrased): the recovered draft is a
  much reduced version of the concept the owner originally had.
- User direction, 2026-09-16, on scope (paraphrased): standards are to be inherited through
  Praetor, which also supplies the frameworks for each part of the stack.
- `docs/adr/README.md` — process, numbering and immutability rules
