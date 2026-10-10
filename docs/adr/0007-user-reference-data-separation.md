# ADR-0007: Reference data separated from user data at the repository boundary

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

The recovered concept required reference data to be versioned and separated from user data, and
named physically separate databases in its tech stack. The replan needed to decide how strong that
separation is.

The two kinds of data have incompatible properties:

| | Reference data | User data |
| :--- | :--- | :--- |
| Visibility | Public, citable | Private |
| Mutability | Immutable once released | Mutable and revocable |
| Cadence | Slow, reviewed | Continuous |
| Provenance | Published literature | Individuals |

A boundary that exists only as a schema convention or a table prefix will eventually be crossed by
a convenient join — and the specific join to fear is the one that merges user measurements into the
reference curve, which would silently destroy the citability of every figure derived from it.

Separately, the statistics module requires that the two curves never merge: reference data from
measured-protocol literature, and a user overlay that is self-selected by definition.

## Decision

Reference data lives in its **own repository** — `lusoris/embodied-reference-data` — with its own
release cadence, review process and version history. The platform monorepo consumes pinned
releases.

The `reference` module has **no read path into the user database**. The dependency is one-way by
construction, not by convention.

The user overlay described in `statistics` is a separate dataset with its own consent basis, shown
alongside the reference curve and always labelled. The two are never combined into a single curve.

Consumers pin a release. A reference update produces a new release; it never silently changes what
a user was shown yesterday.

## Consequences

The separation is structural at three levels — repository, database, and dependency direction —
which makes accidental merging require deliberate effort rather than a careless query.

Reference releases become citable artifacts with their own history, which is what makes the
citation trail in `education` and `statistics` meaningful rather than decorative.

Costs: two repositories to maintain, and cross-repository version coordination. A reference update
requires a deliberate bump in the platform repo rather than taking effect automatically — which is
the point, but it is friction.

The coverage map becomes a first-class output: where no defensible reference exists, that absence
is itself released data rather than a gap discovered at query time.

Open: whether the reference repository holds derived distributions only or extracted source data as
well, which raises per-source redistribution questions — `OQ-014`. And how a published study's
protocol maps onto a platform protocol version when they do not match exactly — `OQ-015`.

## Alternatives considered

**Separate schemas in one database.** Operationally simpler, and the boundary is a convention that
a single join defeats. Rejected as too weak for the specific failure it must prevent.

**Separate databases in one repository.** Stronger, and still leaves reference data on the
platform's release cadence, with no independent citable version history.

**Reference data as a versioned package dependency rather than a repository.** Effectively the
chosen model at consumption time; the repository is where the review and citation trail live.

## References

- User decision, 2026-09-16, repository shape (paraphrased): a monorepo plus a separate
  reference-data repository.
- User direction, 2026-09-16, reference data (paraphrased): published literature first, proven
  user data afterwards.
- `MASTER_CONCEPT.md` §4 (recovered draft): "Referenzdaten sind versioniert und von Userdaten
  getrennt."
- `MASTER_CONCEPT.md` §16 (recovered draft): "DB: User DB + Reference DB (physisch getrennt)"
- `docs/concept/l1-core/reference.md` — `OQ-013`, `OQ-014`, `OQ-015`
