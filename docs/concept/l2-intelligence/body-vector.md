# body-vector

> **Layer:** L2 Intelligence · **Owner:** planned Rust `crates/embodied-vector`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet) · **Store:** Qdrant
> **ADR:** [0009](../../adr/0009-learned-body-vector.md)

## Purpose

Represent a body as a vector in a space where **distance means behavioural similarity, not
numerical similarity**.

This is the distinctive claim of the platform's intelligence layer. An index over a dozen
measurements would be pointless — exact arithmetic on a dozen floats is what a relational database
is for, and nearest-neighbour search over them tells you nothing that sorting would not. The
body-vector is worth building only if it is *learned*: projected from measurements through a model
trained against reported outcomes, so that two bodies land close together when they behave alike
in the ways the platform is actually asked about.

Under that definition, compatibility becomes neighbourhood search, and §8's reality-feedback loop
becomes the training signal rather than a coefficient somebody tuned.

## The bootstrap problem, stated plainly

A learned space needs outcomes to learn from, and at concept stage there are none. This is the
known weakness of building the body-vector first, and it is accepted deliberately rather than
discovered later.

The mitigation is a **structured bootstrap**: the initial projection is derived from reference
distributions — normalised, decorrelated, weighted by measurement reliability — so that the space
is defensible before it is trained, and behaves as a reasonable similarity metric on day one. It
is then progressively refit as [`learning`](learning.md) supplies outcomes.

The space is **versioned**. A refit produces a new space, not a silent redefinition of what
"similar" meant last week. Anything that stored a neighbour set stores the space version with it.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `projection` | Versioned model mapping a feature set to a vector. |
| `body_vector` | An embedded profile. Pseudonymous, consent-bound, revocable. |
| `space_version` | Model version, training corpus, fit statistics, date. |
| `neighbourhood` | A cached similarity result, tagged with the space version that produced it. |

## Implementation

SIMD similarity follows the Rust vector kernel of
[Epitrop](https://github.com/tekmora/epitrop/blob/main/docs/epitrop-description-v2.md): cosine
and Euclidean distance over f32, f16 and i8 vectors. Two further choices are this project's own
and not taken from Epitrop: the `simsimd` crate as the implementation, and AVX2, AVX-512 and NEON
as the instruction sets it must cover. Qdrant holds the index; the crate owns projection, distance
semantics and versioning.

HISS constraints apply: bounded loops, no recursion, explicit deadlines on every call out to the
index.

## Interfaces

- **Provides:** project, nearest-neighbours, similarity, space version resolution.
- **Consumes:** [`measurement`](../l1-core/measurement.md), [`anatomy`](../l1-core/anatomy.md),
  [`reference`](../l1-core/reference.md) for bootstrap structure,
  [`verification`](../l1-core/verification.md) for input weighting.
- **Consumed by:** [`simulation`](simulation.md), [`learning`](learning.md),
  [`search`](../cross-cutting/search.md).

## Consent surface

An embedding is derived personal data and inherits every obligation of its source. Revocation must
delete the vector and evict cached neighbourhoods that contain it — this is the derived-data
deletion path that [`consent`](../l1-core/consent.md) requires every module to answer.

A body-vector must never be exposed in a form that allows reconstructing the underlying
measurements. Similarity is a platform capability, not a public one.

## Open questions

- `OQ-018` — What is the projection model, concretely? A learned low-dimensional metric needs an
  objective, and the objective is exactly what `OQ-005` says may have to be retrained on
  withdrawal.
- `OQ-019` — How many outcomes before a refit is defensible, and what is shown in the meantime?
  A learned space that has learned nothing must not present itself as though it has.
- `OQ-020` — Does the space include features with no reference distribution, where the bootstrap
  has nothing to normalise against?
