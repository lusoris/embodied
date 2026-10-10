# ADR-0004: Two-tier identity — anonymous tier and pseudonymous profile tier

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

The recovered concept contained a direct contradiction. §3 required one profile per person; §11A
promised anonymous education and protection from exposure. Both are correct requirements and they
cannot both be satisfied by a single account model.

The contradiction dissolves once it is noticed that they describe different activities. Learning
what an ordinary body looks like requires nothing from the user. Contributing body data, media or
community presence requires an account. Treating these as one activity forces either identified
learning or unaccountable contribution.

The population that most needs the educational half — people anxious about their bodies, who have
been told something false by pornography or advertising — is exactly the population least willing
to create a profile on an adult platform in order to ask.

## Decision

Two tiers, and one person may hold both.

**Anonymous tier.** No account, no profile, no stored subject. Reads education material, browses
reference statistics, runs the visualizer against reference distributions with measurements never
leaving the browser. Contributes nothing and is asked for nothing.

**Profile tier.** A deliberate opt-in. Carries body data, media, texts, preferences and community
presence, always under a pseudonym. One person, one profile — enforced as strongly as possible
*without collecting identity documents*, which the platform declines to hold by default.

The platform **must not attempt to correlate the two tiers**. That non-correlation is a design
obligation, not an implementation accident.

## Consequences

§11A becomes structurally true rather than aspirational, and it propagates: the visualizer must
render client-side, statistics must be queryable without a subject, education must be reachable
without an account. Those constraints are consequences of this ADR.

Tier transition becomes a meaningful, recorded consent event — the moment a person begins to be
knowable.

Costs: one-profile-per-person is enforced weakly. Without identity documents, duplicate accounts
are possible, and the acceptable failure rate is unresolved — `OQ-003`. Any future age-verification
obligation will collide with this, since certified verification is exactly the identity collection
this ADR avoids; that collision is deferred with the rest of the roadmap.

The anonymous tier must degrade gracefully rather than prompting for signup. An anonymous user
repeatedly asked to register has been told the platform does not mean this.

## Alternatives considered

**Single pseudonymous account for everything.** Simple, but "anonymous education" then means
"logged in but unidentified", which does not protect the person who will not create an account at
all.

**Verified-unique person, displayed pseudonymously.** Strongest against duplicates and minors, and
requires holding identity documents — the single largest breach liability the platform could take
on, for a benefit that does not serve the educational mission.

**Anonymous-first with accounts only for contribution.** Very close to the chosen model; the
difference is that a defined profile tier makes consent and visibility tractable, which a purely
incidental account does not.

## References

- User decision, 2026-09-16, identity (paraphrased): two tiers.
- `MASTER_CONCEPT.md` §3 (recovered draft): "Ein Profil pro Person"
- `MASTER_CONCEPT.md` §11A (recovered draft): "Anonyme Bildung / Schutz vor Exponierung / Fokus
  auf Selbstbestimmung"
- `docs/concept/l1-core/identity.md` — `OQ-003`, `OQ-004`
