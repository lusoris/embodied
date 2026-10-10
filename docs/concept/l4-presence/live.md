# live

> **Layer:** L4 Presence · **Owner:** Go `internal/live`

## Purpose

Real-time conversation — text chat, camera, group rooms — for people who are not in VR.

This is the conventional half of presence, and it carries most of the actual community. VR
embodiment is the distinctive capability; text and cam are what people use daily, and treating
them as the lesser feature would be a mistake about how the platform is actually inhabited.

## Scope, and its boundary with `rooms`

The two modules overlap and the split is by **medium and persistence**, not by intent:

| | [`live`](live.md) | [`rooms`](rooms.md) |
| :--- | :--- | :--- |
| Medium | Text, audio, video streams | Embodied presence, avatars, devices |
| Membership | Open, persistent or ad-hoc | Closed, invited, ephemeral |
| Identity | Pseudonym, optionally camera | Avatar with authenticity grade |
| Moderation | Needed, at scale | Participants are access control |

Where a group text room and an invited VR session start to look like the same product with
different clients, they should be unified — flagged for the deduplication pass.

## Owned data

| Entity | Notes |
| :--- | :--- |
| `channel` | A text or media conversation: membership, scope, retention. |
| `message` | Retention-limited by channel policy, not kept indefinitely by default. |
| `stream_session` | A live camera session: participants, consent scope, duration. |
| `presence` | Who is available, to whom. Granular and defaults to invisible. |

Message retention defaults to limited. A community about intimacy that keeps everything forever
has built a liability that grows monotonically and serves nobody.

## Interfaces

- **Provides:** channel lifecycle, messaging, stream session, presence.
- **Consumes:** [`identity`](../l1-core/identity.md), [`consent`](../l1-core/consent.md),
  [`media`](../l3-expression/media.md) for any persisted artifact,
  [`moderation`](../l3-expression/moderation.md), [`device`](device.md) where a session includes
  hardware.
- **Consumed by:** [`spaces`](../l5-community/spaces.md),
  [`education`](../l5-community/education.md).

## Consent surface

**Camera is the sharpest case.** A live stream is unreviewable before it is seen, cannot be
retracted once witnessed, and is trivially recordable by any viewer regardless of platform policy.
The platform must be explicit that it cannot prevent recording, rather than implying protection it
does not have.

Consent for a cam session is per-session and scoped to named participants. Opening a camera to a
group is a different decision from opening it to one person, and the interface must not let one
slide into the other.

**Anonymous tier.** Read-only participation in education channels, per §11A. Speaking requires a
profile — not as a gate but because unattributable speech in an intimacy community is a well-
understood harassment vector.

Presence defaults to invisible. Being known to be online is information.

## Open questions

- `OQ-055` — Are live streams recorded at all, even transiently, for moderation? Recording makes
  moderation possible and creates exactly the artifact the platform otherwise avoids holding.
- `OQ-056` — Where does the `live`/`rooms` boundary actually sit once both exist? See the
  deduplication note above.
- `OQ-057` — What retention does a text channel default to, and can participants agree to
  something longer without that becoming pressure on one of them?
