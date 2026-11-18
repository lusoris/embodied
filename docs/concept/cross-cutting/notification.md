# notification

> **Layer:** Cross-cutting · **Owner:** planned Go `internal/notification`
> ([ADR-0001](../../adr/0001-go-rust-svelte-split.md); no code exists yet)

## Purpose

Tell people things they need to know, through channels that do not out them.

Notification is a small module with one outsized risk: **a message from emBodied arriving somewhere
another person can see it discloses membership of an adult platform.** A lock-screen preview, a
subject line, a sender name in an inbox — each is a disclosure the platform made on a user's
behalf, in a context it does not control.

Everything here follows from that.

## Rules

1. **Quiet by default.** New accounts receive operational notifications only — security, consent,
   account state. Social and engagement notification is opt-in, never opt-out.
2. **Nothing disclosive leaves the platform.** External messages carry no content, no sender
   pseudonym, no space name, no feature name. At most: something is waiting. The platform is the
   only place the substance exists.
3. **Neutral external identity.** Sender name and any external-facing identifier are neutral by
   default, chosen by the user where possible. A user must be able to receive notifications
   without the word emBodied appearing on their device.
4. **No engagement notification.** Nothing exists to bring someone back — no "people are active",
   no activity digests, no re-engagement prompts. Those mechanics are designed to override a
   person's own judgement about when to open an app, and on this platform that is not an
   acceptable thing to do.
5. **Consent events always reach the person.** A grant, revocation, moderation action or
   verification outcome is delivered regardless of preference, because they concern rights rather
   than engagement.

Rule 4 is a genuine product cost and is accepted deliberately. It is also the rule most likely to
be eroded later by ordinary growth pressure, which is why it is written here rather than left as
an assumption.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `notification` | An event for a subject, with its class and delivery state. |
| `channel_binding` | Where a person may be reached, and how disclosively. |
| `preference` | Per class, per channel. Defaults closed except consent events. |

## Interfaces

- **Provides:** enqueue, deliver, preference resolution.
- **Consumes:** [`identity`](../l1-core/identity.md), [`consent`](../l1-core/consent.md).
- **Consumed by:** [`consent`](../l1-core/consent.md),
  [`moderation`](../l3-expression/moderation.md),
  [`verification`](../l1-core/verification.md), [`rooms`](../l4-presence/rooms.md),
  [`live`](../l4-presence/live.md).

The anonymous tier has no notification channel, which is a property of the tier rather than a
limitation of this module. Nothing to notify, nobody to notify.

## Consent surface

An external channel binding is a consent decision about being contactable in a context the platform
cannot see. It is confirmed explicitly, revocable, and the disclosure risk is stated in plain
terms when it is set up rather than buried in a preference description.

## Open questions

- `OQ-070` — Which external channels are supported at all? Every one is a third party that learns
  a user's address is associated with this platform, regardless of message content.
- `OQ-071` — In-session notification during [`embodiment`](../l4-presence/embodiment.md) or
  [`rooms`](../l4-presence/rooms.md): what may interrupt someone in VR, and what must wait?
