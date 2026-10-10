# ADR-0009: Learned body-vector as the primary embedding space

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

The decision to use a dedicated vector store (ADR-0002) raised an obvious objection: a body is
described by a modest number of structured measurements, and an approximate-nearest-neighbour
index over a dozen floats earns nothing that sorting and filtering in Postgres would not.

If the vector store is to be the intelligence core rather than an accessory, something other than
raw measurements must be embedded.

The candidates were: embed text, preferences and media (natively semantic content, but leaving the
body itself outside the vector layer); embed a *learned* body-vector trained against reported
outcomes; or project everything into one shared multimodal space.

The concept's simulation ambition is the deciding factor. §5 compatibility prediction needs a
notion of similarity that means *these bodies behave alike*, which raw measurement distance does
not provide. That notion has to be learned from outcomes.

## Decision

The **learned body-vector is the first embedding space**. Text, preference and media embeddings
come later.

Measurements are projected through a learned model into a space where distance approximates
behavioural similarity. Compatibility becomes neighbourhood search in that space, qualified by the
knowledge graph.

Because no outcomes exist at concept stage, the space uses a **structured bootstrap**: the initial
projection is derived from reference distributions — normalised, decorrelated, weighted by
measurement reliability — so it is a defensible similarity metric on day one, and is progressively
refit as `learning` supplies outcomes.

The space is **versioned**. A refit produces a new space, not a silent redefinition. Anything that
cached a neighbour set stores the space version alongside it.

## Consequences

The distinctive capability of the platform is built first, and the vector store earns its place.
§8's reality feedback becomes the training signal for the core model rather than an adjustment to a
formula somebody tuned.

The bootstrap problem is accepted openly rather than discovered later: a learned space needs
outcomes to learn from, and there are none. The structured bootstrap makes the space reasonable
before it is trained, and the platform must present that state honestly — a model that has learned
nothing must not present itself as though it has. Recorded as `OQ-019`.

Versioning means refits are traceable and reversible, at the cost of invalidating caches and
requiring every stored neighbourhood to carry a version.

Embeddings are derived personal data. Revocation must delete the vector and evict cached
neighbourhoods containing it — and `OQ-005` asks whether it must also retract the vector's
contribution to a trained space, which is the expensive version of the question.

The projection model itself is unspecified — a learned low-dimensional metric needs an objective,
and that objective is exactly what withdrawal would force retraining of. Recorded as `OQ-018`.

## Alternatives considered

**Text, preferences and media first; body-vector later.** The safer build order — embed what is
natively semantic, and derive the body-vector once outcomes exist to fit it against. Avoids
inventing a space with nothing to train it on. Rejected in favour of building the distinctive part
first, accepting the bootstrap cost.

**One shared multimodal space from the start.** Most powerful, most speculative, and hardest to
keep interpretable or to explain a result from — which matters on a platform committed to showing
its uncertainty.

**No learned space; measurements stay relational.** Honest division of labour, and it forecloses
the compatibility prediction that is the point of §5.

## References

- User decision, 2026-09-16, embeddings (paraphrased): the learned body-vector comes first.
- User direction, 2026-09-16, on simulation scope (paraphrased): essentially the full scope, so
  that a good prediction is possible across everything that was listed.
- `cordanaLLM/Tribunus` `tribunus-description-v2.md`: "tasks are dynamically matched to agent skill
  embeddings using SIMD-accelerated vector distance calculations in Rust (`crates/tribunus-graph`)"
- `MASTER_CONCEPT.md` §6 (recovered draft): "Erfahrungsabgleich / Modell-Verbesserung / Lernendes
  System"
- `docs/concept/l2-intelligence/body-vector.md` — `OQ-018`, `OQ-019`, `OQ-020`
