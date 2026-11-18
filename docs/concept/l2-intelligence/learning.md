# learning

> **Layer:** L2 Intelligence · **Owner:** planned Rust `crates/embodied-learn`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

Close the loop between what the platform predicted and what actually happened, so that §8's
"learning system" is a mechanism rather than an aspiration.

The design principle is that **reported experience writes edges, it does not tune a coefficient**.
An outcome becomes a node in the [`knowledge-graph`](knowledge-graph.md) connected to the pairing,
the measurements, the protocol and the model version that produced the prediction. The model
improves because the graph grows and the [`body-vector`](body-vector.md) space is refit against
it — not because somebody adjusted a constant.

That distinction matters for auditability. Any prediction can be traced to the outcomes that
shaped it, and any withdrawn outcome can be traced to the predictions it influenced.

## Collection

Structured calibration, opt-in, at the point where a prediction can be compared to reality: did it
match, where was it off, on a defined scale. Structured because free text cannot be compared to a
model output without an interpretation layer that would itself need validating.

Free-text reports are valuable for [`education`](../l5-community/education.md) and
[`spaces`](../l5-community/spaces.md), but they enter through those modules, not this one. This
crate consumes comparable, structured signal only.

**This is the most sensitive data class on the platform.** It is a person reporting on a specific
sexual experience, linked to a specific pairing, linked to identifiable body data. Every
constraint below follows from that.

## Constraints

1. **Consent at collection, separately from profile consent.** Agreeing to record your body is not
   agreeing to report your sex life.
2. **Separable from the profile.** An outcome must be storable in a form that contributes to the
   model without remaining linked to the person who reported it, once linkage is no longer needed.
3. **Both parties.** An outcome describing a pairing describes two people. Either may report;
   neither may report on the other's behalf; and what is disclosed to the other party is an
   explicit setting, not a default.
4. **Withdrawal reaches the model.** `OQ-005` — this is the unresolved question. Retraining on
   every withdrawal is expensive; not retraining means a withdrawn report still shapes
   predictions. The concept commits to answering it before implementation, not after.
5. **Aggregate-only fallback.** Where per-profile linkage cannot be justified, the outcome
   contributes in aggregate. A model that learns only population-level corrections is worth more
   than a breach.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `outcome_report` | Structured comparison of prediction to experience. Consent-bound, revocable. |
| `calibration` | Derived correction signal, tagged with model and space version. |
| `refit` | A training run: corpus, space version produced, fit statistics, date. |
| `retraction` | A withdrawn report and the refits that carried it. |

## Interfaces

- **Provides:** report intake, calibration derivation, refit orchestration, retraction handling.
- **Consumes:** [`consent`](../l1-core/consent.md), [`simulation`](simulation.md) for the
  prediction under test, [`knowledge-graph`](knowledge-graph.md),
  [`body-vector`](body-vector.md).
- **Consumed by:** [`body-vector`](body-vector.md) (refit), [`simulation`](simulation.md)
  (calibration).

This module owns the write path that touches Postgres, Qdrant and Memgraph together, which makes
it the place where `OQ-021`'s cross-store consistency question has to be answered.

## Consent surface

The largest on the platform, and the constraints above are its substance. Restated as obligations
this module owes:

- **Separate consent at collection.** Agreeing to record your body is not agreeing to report your
  sex life. This grant is never inherited from profile or measurement consent.
- **Both parties, independently.** An outcome describes a pairing and therefore two people. Either
  may report; neither may report on the other's behalf; disclosure to the other party is an
  explicit setting, not a default.
- **Separability.** An outcome must be storable in a form that contributes to the model without
  remaining linked to the reporter once linkage is no longer needed.
- **Aggregate fallback.** Where per-profile linkage cannot be justified, the outcome contributes in
  aggregate. A model that learns only population-level corrections is worth more than a breach.
- **Withdrawal reaches the model** — or is honestly documented as not doing so. This is `OQ-005`
  and it is unresolved; the concept commits to answering it before implementation rather than
  after.

## The cold-start honesty problem

Until enough outcomes exist, this module produces nothing, and
[`simulation`](simulation.md) runs on geometry and priors alone. The platform must present that
state accurately rather than implying a learning system that has not yet learned anything. A
model's composition disclosure (simulation, rule 3) is what makes this visible.

## Open questions

- `OQ-005` — Does withdrawal retract a report's contribution to the trained model, or only its
  displayable form?
- `OQ-028` — What is the minimum viable structured schema — enough dimensions to calibrate
  against, few enough to be answerable without an interrogation?
- `OQ-029` — Reporting asymmetry: if one party reports and the other does not, is the outcome
  usable, and does it bias the model toward the experiences of people willing to report?
