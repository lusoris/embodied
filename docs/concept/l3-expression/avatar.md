# avatar

> **Layer:** L3 Expression · **Owner:** planned Rust geometry in `crates/`, pipeline in Go
> `internal/avatar` ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

Turn a verified body into something inhabitable — a rigged, animatable avatar that is recognisably
*this person's actual body* rather than a configured approximation of one.

This is what makes [`embodiment`](../l4-presence/embodiment.md) meaningful. Existing social VR
lets people be anything; emBodied's proposition is the opposite and much rarer: **be yourself, at
your real dimensions, and see what that is actually like.** The value depends entirely on the
avatar being true, which is why it is gated on [`verification`](../l1-core/verification.md) grade
rather than on self-report.

## Authenticity gating

An avatar may be presented as *real* only when the measurements behind it meet the threshold
[`verification`](../l1-core/verification.md) sets for this consumer — expected to be `evidenced`
or above. Below that threshold an avatar is still usable; it is simply not presented as verified,
and other participants in a shared space can tell the difference.

This is the concept's approved-as-real condition made concrete. Without it, a space advertised as
people in their real bodies becomes a space where some people are and nobody knows which — which
is worse than not making the claim at all.

The claim is about the **measurements**, never about the person. There is no verified-person
status on this platform; see [`verification`](../l1-core/verification.md).

## Pipeline

```text
measurements ──> geometry (shared with visualizer) ──> mesh ──> rig ──> avatar
     │                                                                    │
verification grade ──────────────────────────────────────────> authenticity assertion
```

Same parametric geometry as [`visualizer`](visualizer.md), so an avatar and a rendered comparison
of the same body cannot disagree.

Export to standard formats is a first-class output, not an afterthought — it keeps the avatar
useful if the platform's own runtime is not where a person wants to be, and it keeps the pipeline
honest by forcing it to produce something that stands alone.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `avatar` | Versioned, bound to a measurement set and its verification grade. |
| `authenticity_assertion` | Whether this avatar may be presented as real, and on what basis. |
| `rig` | Skeleton and deformation parameters. |
| `export` | A generated standard-format artifact, consent-bound and revocable. |

## Interfaces

- **Provides:** build, authenticity assertion, export, avatar resolution for a session.
- **Consumes:** [`measurement`](../l1-core/measurement.md),
  [`verification`](../l1-core/verification.md), [`anatomy`](../l1-core/anatomy.md),
  [`consent`](../l1-core/consent.md), the shared geometry crate.
- **Consumed by:** [`embodiment`](../l4-presence/embodiment.md),
  [`rooms`](../l4-presence/rooms.md), [`social-vr`](../l4-presence/social-vr.md).

## Consent surface

An avatar is the most complete representation of a person the platform can produce, and it is
derived data — so every obligation from [`consent`](../l1-core/consent.md) applies, including the
propagation of revocation to exports that have already been generated.

Exports are the hard case: an exported avatar has left the system. The platform can revoke its
own copies and refuse to reissue, and it must be explicit with users that it cannot recall what
was downloaded. Saying this clearly at export time is the honest design; implying recall would not
be.

Appearing in a shared space as a verified real body is a distinct consent decision from building
the avatar. Building is private by default.

## Open questions

- `OQ-033` — Which export formats, and does exporting a verified-real avatar carry its
  authenticity assertion with it? An assertion that travels can be replayed by someone else.
- `OQ-034` — How is the gap between measured features and a complete body filled? An avatar needs
  a whole body; the measurement set will cover part of it. The rest is inference, and the person
  should know which parts are theirs and which are inferred.
- `OQ-032` — The synthetic-intimate-imagery boundary, shared with [`visualizer`](visualizer.md).
