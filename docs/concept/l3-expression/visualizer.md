# visualizer

> **Layer:** L3 Expression · **Owner:** Rust geometry in `crates/`, compiled to WASM;
> Svelte 5 shell in `ui/`

## Purpose

Show a body — the user's own, a reference distribution, or a simulated pairing — accurately enough
to be useful and well enough to be wanted.

**One geometry model, three render modes**, chosen by the viewer:

| Mode | What it is for |
| :--- | :--- |
| **2D comparison** | Silhouette and scale against percentile bands. The clearest way to answer "where am I in this distribution", and the cheapest to get right. |
| **Anatomical 3D** | Parametric mesh rendered clinically. Accurate form, visibly a model — which is what §1's "simulation is orientation, not a promise" looks like on screen. |
| **Photoreal 3D** | The same mesh with skin, subsurface scattering and real lighting. |

The viewer chooses, because the platform does not decide whether a person is here clinically or
erotically. That refusal is the same one that governs [`tagging`](tagging.md): emBodied describes
and lets people choose, rather than ruling on what their interest is.

Photoreal is included rather than treated as an indulgence. A platform that models bodies honestly
and then renders them like a textbook has decided, implicitly, that arousal is the disreputable
use — which contradicts principle 3. It is also the harder engineering problem, and the one where
"uncanny" is a real failure mode.

## Shared geometry, no drift

The parametric model is **Rust, compiled to WASM**, and is the same code that
[`simulation`](../l2-intelligence/simulation.md) runs server-side. This is a correctness property
rather than an optimisation: if the renderer had its own geometry, what a person sees and what the
platform computed would diverge, silently, and the visualizer would be showing a body the
simulation does not believe in.

It also makes client-side rendering of private measurements possible without sending them anywhere,
which matters for the anonymous tier.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `geometry_model` | Versioned parametric definition per feature type. |
| `render_preference` | Viewer's mode, detail and presentation choices. Local where possible. |
| `comparison_view` | A saved comparison — measurement against distribution or against another. |

## Interfaces

- **Provides:** render, comparison view, geometry parameter resolution.
- **Consumes:** [`measurement`](../l1-core/measurement.md), [`anatomy`](../l1-core/anatomy.md),
  [`statistics`](../l1-core/statistics.md) for bands and intervals,
  [`reference`](../l1-core/reference.md), [`simulation`](../l2-intelligence/simulation.md).
- **Consumed by:** [`avatar`](avatar.md), which takes the same geometry and rigs it.

Anything the visualizer displays from [`statistics`](../l1-core/statistics.md) must satisfy that
module's `presentation_contract` — a percentile rendered without its interval is a contract
violation, enforceable rather than a review comment.

## Consent surface

The anonymous tier uses the visualizer against reference distributions with **no measurement
leaving the browser**. This is the concrete form of §11A: a person can find out where they fall
without telling anyone, including us.

Rendering another person's body requires their consent at feature granularity, resolved through
[`consent`](../l1-core/consent.md) at render time.

## Open questions

- `OQ-030` — Which render mode is the default, given that the default is itself a statement about
  what the platform thinks the user is here for? A viewer-chosen default with no platform
  preference is probably the answer, but it needs stating.
- `OQ-031` — How much geometric fidelity is achievable from the measurement set, and where does
  the mesh become interpolation presented as fact? The coverage-gap principle applies to geometry
  as much as to statistics.
- `OQ-032` — Photoreal rendering of a real person's verified body is materially close to
  synthetic intimate imagery. The distinction — the subject built it from their own measurements,
  under their own consent — needs to be structural, not just intended.
