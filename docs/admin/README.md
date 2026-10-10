# emBodied for administrators

A **view** into the canonical concept. Where this disagrees with
[admin](../concept/cross-cutting/admin.md), that wins.

## The rule that governs this role

**Operators are not exempt from the consent model.**

This is the module where platforms usually abandon their stated principles quietly — consent is
enforced against users, and then a support tool exists that sees everything, used by whoever holds
the credential, logged nowhere. On a platform holding this material, that would make every other
guarantee conditional on operator discretion.

## What you can see

| Capability | Constraint |
| :--- | :--- |
| Aggregate operational data | Unrestricted — [telemetry](../concept/cross-cutting/telemetry.md) carries no subject |
| Account state, tier | Scoped to the account, on a support request from that account |
| Content inspection | Only via a [moderation](../concept/l3-expression/moderation.md) case, never ad hoc |
| Body data, media, outcome reports | **No routine path exists.** Break-glass only |
| Verification evidence | **No access.** Retention-limited, assessed by its own path |

There is no operator view showing an individual's body data, media or reported experiences as a
matter of routine. If support cannot be delivered without it, support is delivered without it.

## Break-glass

A deliberate, logged, alerting action requiring a stated reason, which **notifies the affected
user** unless a legal obligation prevents it.

It exists because refusing to have any emergency path produces an unrunnable system, and
pretending it does not exist produces an unaudited one. It is not a convenience and technical
bounds — time limits, mandatory notification, second-party alerting — should prevent it becoming
one.

`access_record` is append-only and written outside your control. An audit log an administrator can
edit is a formality.

## What you do not do

**Data subject operations are self-service.** Export, correction and deletion are user-initiated,
not support tickets. Routing them through you means a person exercising a right has to ask a human
for permission, and means that human sees the data.

You verify deletion completed. You do not perform it by hand.

## Operating the platform

Three stateful stores — PostgreSQL, Qdrant, Memgraph
([ADR-0002](../adr/0002-relational-vector-graph-persistence.md)) — each with its own backup,
restore and failover story. Plus object storage for media. Cross-store consistency has no
transaction spanning them (`OQ-021`), and deletion verification across all of them is unresolved
(`OQ-074`).

Logs are a data store and get the same scrutiny as the databases. No identifiers beyond what an
incident requires, no content or feature names in span names or metric labels, retention shorter
than you would ordinarily choose.

## Open questions that affect you

`OQ-072` break-glass holders · `OQ-073` where the tamper-proof audit log lives on a platform you
run · `OQ-074` proving deletion completed · `OQ-036` backup deletion window · `OQ-066` incident
diagnostics.

See [OPEN-QUESTIONS.md](../design-basis/OPEN-QUESTIONS.md).
