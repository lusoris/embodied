# telemetry

> **Layer:** Cross-cutting · **Owner:** planned Go `internal/telemetry`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

Know whether the system is working, without building a surveillance apparatus pointed at people's
sex lives.

The default posture is inverted from ordinary product analytics: **measure the system, not the
user.** Latency, error rates, queue depth, resource consumption and model performance are
operational facts. What a specific person looked at, measured, filtered or simulated is not
telemetry — it is the most sensitive data on the platform, and collecting it "for product
insight" would contradict every commitment the concept makes.

## What is collected

| Collected | Not collected |
| :--- | :--- |
| Request latency, error rate, saturation | Which content a person viewed |
| Resource and token accounting | Which filters a person set |
| Model fit statistics, refit outcomes | Which simulations a person ran |
| Consent-resolution performance | Which bodies a person compared against |
| Moderation queue depth and age | Session-level behavioural traces |

Following the `20 Watts` resource principles taken from Epitrop's early design (its current
documents no longer state them), accounting is a first-class concern rather than an
afterthought — compute spent on embedding refits, simulation and assisted tagging is ledgered,
because those are the expensive paths and the ones most likely to grow silently.

## The specific hazard

Operational telemetry on this platform leaks by accident more easily than elsewhere. A URL path
containing a feature type, an error message quoting a measurement, a trace span named after a
space, a log line with a profile identifier next to a content identifier — each is ordinary
practice, and each would produce a record of someone's intimate activity in a system that was
never designed to hold one.

So: no identifiers in logs beyond what an incident genuinely requires; no content or feature names
in span names or metric labels; structured fields with an explicit allow-list rather than
free-text interpolation; and log retention shorter than one would ordinarily choose.

Logs are a data store. They get the same scrutiny as the databases.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `metric` | Aggregate operational measurement. No subject. |
| `trace` | Request-scoped, sanitised, short retention. |
| `resource_ledger` | Compute and token accounting per subsystem. |
| `model_statistic` | Fit quality, refit outcomes, calibration drift. |

## Interfaces

- **Provides:** instrumentation, accounting, health reporting.
- **Consumes:** nothing that carries personal data by design.
- **Consumed by:** [`admin`](admin.md).

## Consent surface

Intended to be none, which is an active requirement rather than a passive state. Any telemetry
that would let an operator reconstruct an individual's activity is out of scope, and that includes
telemetry which becomes identifying only in combination.

## Open questions

- `OQ-066` — Incident investigation needs enough detail to diagnose a specific user's failure. What
  is the minimum, and is it gathered on demand under audit rather than collected continuously?
- `OQ-067` — Model performance monitoring needs per-prediction outcomes, which are exactly the
  sensitive records [`learning`](../l2-intelligence/learning.md) governs. Which of the two owns
  that boundary?
