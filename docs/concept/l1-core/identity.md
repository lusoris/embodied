# identity

> **Layer:** L1 Core · **Owner:** planned Go `internal/identity`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet) · **ADR:**
> [0004](../../adr/0004-two-tier-identity.md)

## Purpose

Establish who is acting, at the weakest level of identification that the action actually requires.

emBodied runs two tiers because §3 and §11A of the concept pull in opposite directions — one
profile per person, and anonymous education — and both are correct. The resolution is not a
compromise between them but a recognition that they describe different activities.

**Anonymous tier.** No account, no profile, no stored subject. Reads education material, browses
reference statistics, runs the visualizer against reference distributions. Contributes nothing,
and is asked for nothing. A person learning what an ordinary body looks like must never have to
expose their own to find out; a platform that demands a profile first has failed the people who
need it most.

**Profile tier.** A deliberate opt-in. Carries body data, media, texts, preferences and community
presence, always pseudonymously. One person, one profile — enforced as strongly as is possible
without collecting identity documents, which is a liability the platform declines to hold by
default.

One human may use both tiers, and the platform must not attempt to correlate them. That
non-correlation is a design obligation, not an accident of implementation.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `account` | Pseudonym, credentials, creation time. No legal name. |
| `session` | Tier, scope, expiry. Anonymous sessions carry no account reference. |
| `role_assertion` | Self-described sexual, psychological, social and contextual roles. Descriptive only — never used to gate features. |
| `uniqueness_signal` | Weak signals supporting one-profile-per-person. Deliberately not identity documents. |

## Interfaces

- **Provides:** authentication, session resolution, tier assertion, pseudonym resolution.
- **Consumes:** [`consent`](consent.md) for visibility scoping on any identity-bearing read.
- **Consumed by:** effectively everything. Identity is the root of every authorisation decision.

Sessions are owned here and in Go, not in the SvelteKit layer. The UI holds a cookie; it does not
hold authority.

## Consent surface

Tier transition is itself a consent event: moving from anonymous to profile is the moment a person
begins to be knowable, and it is recorded as such. Downgrade, export and deletion are first-class
operations, not support tickets.

The anonymous tier must degrade gracefully rather than nagging. An anonymous user who is
repeatedly asked to sign up is being told the platform does not mean what §11A says.

## Open questions

- `OQ-003` — How is one-profile-per-person enforced without identity documents, and what failure
  rate is acceptable? Related: [`verification`](verification.md) grades a *measurement*, not a
  person.
- `OQ-004` — Does the anonymous tier support any persistence at all (saved comparisons, a local
  visualizer state), and if so where does it live so that it stays uncorrelatable?
