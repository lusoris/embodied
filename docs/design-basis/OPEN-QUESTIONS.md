# emBodied — Open Questions

Every question the concept raises and does not answer. Referenced by `OQ-NNN` from module pages
and ADRs.

**Status vocabulary:** `Prep Answer Exists` — a working answer is proposed and can be built on ·
`Partially Answered` — decided in part · `External Decision` — depends on something outside
engineering · `Open` — no answer yet.

Numbering is append-only. Never reuse, never renumber.

---

## Deferred by decision

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-001 | Roadmap: phasing, first-release scope, jurisdiction and hosting, age verification, payments, subscriptions, creator earnings, launch posture. | External Decision | Deliberately not decided in the concept pass. Software architecture first, per owner direction. | A dedicated roadmap pass. |
| OQ-002 | The recovered §17 declares the wiki the canonical source, but Praetor/HISS-16 makes `AGENTS.md` canonical and the house pattern puts prose in `docs/` with MkDocs publishing. | Prep Answer Exists | `docs/` is canonical; the wiki becomes a published surface built from it. Recorded rather than silently overridden. | Owner decision. |

## Identity and consent

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-003 | How is one-profile-per-person enforced without identity documents, and what failure rate is acceptable? | Open | Weak signals only. ADR-0004 declines to hold identity documents. | A stated acceptable duplicate rate. |
| OQ-004 | Does the anonymous tier support any persistence, and if so where does it live so it stays uncorrelatable? | Open | Client-side only, if at all. | A design for anonymous-tier state. |
| OQ-005 | Does revoking an experience report retract its contribution to the trained model, or only its displayable form? | Open | Unresolved. Retraining on withdrawal is expensive; not retraining means withdrawn data still shapes predictions. | A decision on retraining policy, which constrains the `OQ-018` objective. |
| OQ-006 | Pair simulation has one output and two subjects. Whose consent governs it, and what happens when one withdraws? | Open | Both must consent to compute. Withdrawal semantics undefined. | A joint-artifact consent model. |

## Anatomy and measurement

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-007 | What is the initial feature catalogue, and how is it extended? | Open | None drafted. An under-specified catalogue reintroduces a default body. | A drafted catalogue plus an extension process. |
| OQ-008 | How is feature history exposed, given a trajectory can be a transition record? | Partially Answered | Default closed. Granularity undefined. | A history visibility design. |
| OQ-009 | Which measurement protocols ship initially, and are they the same protocols the reference literature used? | Open | Must match, or comparability is lost. | A protocol set derived from the reference catalogue. |
| OQ-010 | How much does the platform assist with capture before assistance becomes pressure? | Open | — | A guided-capture design with a stated limit. |

## Verification

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-011 | What constitutes `evidenced`, and who or what assesses it? | Open | Automated assessors can be fooled and must view sensitive material; human assessors must view it. | An assessment design with a stated exposure model. |
| OQ-012 | Is `witnessed` reachable without an identity system ADR-0004 declined to build? | Partially Answered | May be reserved for clinically sourced reference data only. | A decision on whether user data can ever reach this grade. |

## Reference data and statistics

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-013 | What is the ingestion process for a new source, and who reviews methodology? | Open | An unreviewed citation trail is decorative. | A review process for the reference repository. |
| OQ-014 | Does the reference repository hold derived distributions only, or extracted source data too? | Open | Latter is more useful, raises per-source redistribution questions. | A per-source licence review. |
| OQ-015 | How is a published study's protocol mapped onto a platform protocol version when they do not match exactly? | Open | Related to OQ-009. | A mapping methodology. |
| OQ-016 | What is the minimum cohort size for display, and how is suppression communicated? | Open | Suppress rather than show a wide interval — a narrow enough cohort is a person. | A suppression threshold and its presentation. |
| OQ-017 | Does the user overlay feed anything other than display? If it influences plausibility, self-selection bias becomes self-reinforcing. | Open | Display only, provisionally. | A decision on overlay use. |

## Intelligence layer

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-018 | What is the body-vector projection model, concretely? | Open | Structured bootstrap from reference distributions; learned objective undefined. | A model specification. Constrained by OQ-005. |
| OQ-019 | How many outcomes before a refit is defensible, and what is shown in the meantime? | Open | A space that has learned nothing must not present itself as though it has. | A refit threshold and a cold-start presentation. |
| OQ-020 | Does the space include features with no reference distribution to normalise against? | Open | — | A decision tied to OQ-007 coverage. |
| OQ-021 | Cross-store write consistency: what is the transaction boundary when one outcome report writes to Postgres, Qdrant and Memgraph? | Open | `learning` owns the write path. Boundary undefined. | A consistency and reconciliation design. |
| OQ-022 | Does `d_max = 12` suit this domain, or was it inherited from a differently shaped graph? | Open | Inherited from Epitrop, where 12 is a proposed design parameter. | Analysis of real traversal depths. |
| OQ-023 | Is the graph rebuildable from Postgres as a recovery path, and does that argue against a dedicated engine? | Open | — | A recovery design; may reopen ADR-0002. |
| OQ-024 | Which distribution families are supported, and what happens when a source's summary statistics do not fit the assumed family? | Open | Veale et al. simulate from the normal; not every feature will be normal. | A family selection policy. |
| OQ-025 | How are intervals combined when a simulation input is itself an estimate? | Open | Naive propagation yields useless widths; narrowing by assumption is dishonest. | An uncertainty propagation design. |
| OQ-026 | Which biomechanical parameters are literature-derivable and which are pure prior? | Open | The coverage map should extend to model parameters. | A parameter provenance audit. |
| OQ-027 | How is model-composition weighting decided, and is it user-visible or only reported? | Open | Reported at minimum. | A weighting design. |
| OQ-028 | What is the minimum viable structured outcome schema — enough to calibrate, few enough to answer? | Open | — | A drafted schema. |
| OQ-029 | If one party reports and the other does not, is the outcome usable, and does it bias the model toward people willing to report? | Open | — | A bias analysis. |

## Expression

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-030 | Which render mode is default, given the default is itself a statement about what the user is here for? | Partially Answered | Viewer-chosen with no platform preference. | Confirmation. |
| OQ-031 | How much geometric fidelity is achievable from the measurement set, and where does the mesh become interpolation presented as fact? | Open | Coverage-gap principle applies to geometry. | A fidelity analysis. |
| OQ-032 | Photoreal rendering of a verified real body is materially close to synthetic intimate imagery. The distinction — built by the subject, from their own measurements, under their own consent — must be structural. | Open | Consent binding and self-derivation are the distinction. Not yet enforced structurally. | A structural safeguard design. |
| OQ-033 | Which export formats, and does an exported verified-real avatar carry its authenticity assertion? An assertion that travels can be replayed. | Open | — | An export design. |
| OQ-034 | How is the gap between measured features and a complete body filled, and does the person know which parts are theirs? | Open | Inference must be labelled. | An inference disclosure design. |
| OQ-035 | Consent for a depicted person who is not a platform user. | Open | Either refuse such uploads, or build a claim-and-verify path that requires identifying a non-user. | A decision between the two. |
| OQ-036 | How long until deletion is genuinely complete across backups, and is that window acceptable to state publicly? | Open | — | A retention and deletion audit. |
| OQ-037 | Does the anonymous tier see any user media, or only reference and education material? | Open | Reference and education only is the safe answer. | A tier access decision. |
| OQ-038 | Who owns the controlled vocabulary and how does it change? | Open | Uncontrolled makes filters unreliable; over-controlled cannot describe real posts. | A vocabulary governance process. |
| OQ-039 | What does the assisted classifier run on, given it processes the most sensitive material the platform holds? | Partially Answered | On-platform inference. | Confirmation as a hard constraint. |
| OQ-040 | Filter defaults for a new account — restrictive defaults protect and also decide for the user, which is close to the declined editorial judgement. | Open | — | A defaults decision. |
| OQ-041 | Who moderates? Solo review of this material at volume is a wellbeing problem; outsourcing hands the platform's most sensitive assets to a third party. | Open | — | An operational decision. Blocks social-vr. |
| OQ-042 | What is the closed moderation rule set, precisely? | Open | Closure is the guarantee, so it must be written before launch. | A written rule set. |

## Presence and embodiment

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-043 | Embed the Buttplug library in a platform client, or interoperate with the user's existing Intiface Central? | Open | Both viable; ADR-0010 chose the crate, not the deployment shape. | A client architecture decision. |
| OQ-044 | What are default device safety bounds, and who may raise them? | Partially Answered | Owner-set ceiling; the floor may need to be platform-set and non-negotiable. | A bounds specification. |
| OQ-045 | Sensor-capable devices report as well as actuate. Does that feed `learning`, and under what separate consent? | Open | Among the most intimate data conceivable. | A decision, defaulting to no. |
| OQ-046 | Which VR runtimes are targeted, and does the platform ship a client or export to existing ones? | Open | Determines the size of the embodiment module by an order of magnitude. | A runtime decision. |
| OQ-047 | Distress and dysphoria are foreseeable outcomes of seeing your own body accurately. What does a session owe someone having a bad time, without being paternalistic about an experience they chose? | Open | — | A wellbeing design. |
| OQ-048 | Does solo embodiment generate learning signal at all? | Partially Answered | Outside the model loop is the safer default. | Confirmation. |
| OQ-049 | Maximum room participants before a room becomes a space needing moderation rather than invitation? | Open | The number is where the module's assumptions break. | A stated limit. |
| OQ-050 | Is authenticity grade displayed to other participants, and at what granularity? Showing it makes the real-bodies claim meaningful; showing it precisely discloses how much evidence someone provided. | Open | — | A disclosure design. |
| OQ-051 | Capture requires unanimity — what enforces it technically, given a participant can photograph their own headset display? | Open | Cannot be fully enforced; must be stated honestly. | An honest capability statement. |
| OQ-052 | What replaces invitation as the access-control primitive in an open social space? | Open | Rooms are safe largely because there is no discovery. | A discovery design that preserves the safety property. |
| OQ-053 | Are verified real bodies compatible with open social space at all, or does accurate real anatomy plus strangers create a dynamic the platform should not build? | Open | Answering "no" is legitimate. | A decision on whether to build it. |
| OQ-054 | Does open space run on the platform's own runtime or an existing social VR platform, accepting someone else's consent and moderation model? | Open | Related to OQ-046. | A runtime decision. |
| OQ-055 | Are live streams recorded at all, even transiently, for moderation? | Open | Recording enables moderation and creates the artifact the platform otherwise avoids holding. | A decision. |
| OQ-056 | Where does the `live` / `rooms` boundary sit once both exist? | Open | Split by medium and persistence. Overlap flagged in the deduplication pass. | A boundary decision. |
| OQ-057 | What retention does a text channel default to, and can participants agree to longer without that becoming pressure on one of them? | Open | Limited by default. | A retention policy. |

## Community

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-058 | Are the three space kinds fixed, or may users create spaces with new expectations? | Open | User-created spaces make the expectation contract unenforceable. | A decision. |
| OQ-059 | How does a person move between spaces without the transition disclosing something? | Open | — | A presence design. |
| OQ-060 | Does `spaces` subsume `live` channels, or do channels live inside spaces? | Open | Overlap flagged in the deduplication pass. | A boundary decision. Related to OQ-056. |
| OQ-061 | Who writes education material, and what review does a claim get? This is medical-adjacent content people will act on. | Open | — | An editorial process. |
| OQ-062 | Where is the boundary with medical advice? | Open | The platform describes distributions and must not diagnose. The line is thin. | A stated boundary, reviewed. |
| OQ-063 | Anonymous questions are an abuse vector as well as a safety feature. What limits exist that do not require identifying the asker? | Open | — | A rate and abuse design. |
| OQ-064 | Is any progress sharing supported? Any sharing creates the comparison the module exists to prevent; total prohibition denies a legitimate wish to be seen. | Open | — | A decision. |
| OQ-065 | How is "no detectable change" presented over long periods without reading as failure? | Open | — | A presentation design. |

## Cross-cutting

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-066 | Incident investigation needs per-user detail. What is the minimum, and is it gathered on demand under audit rather than collected continuously? | Partially Answered | On demand under audit. | A diagnostic access design. |
| OQ-067 | Model performance monitoring needs per-prediction outcomes — exactly the records `learning` governs. Which module owns that boundary? | Open | — | A boundary decision. |
| OQ-068 | Does the anonymous tier get search, and over what? | Partially Answered | Reference and education material only. | Confirmation. |
| OQ-069 | What is the cross-store consistency expectation for a federated query? | Open | Depends on OQ-021. | A consistency model. |
| OQ-070 | Which external notification channels are supported? Every one is a third party learning that an address is associated with this platform. | Open | — | A channel decision. |
| OQ-071 | What may interrupt someone in VR, and what must wait? | Open | — | An interruption policy. |
| OQ-072 | Who holds break-glass access, and what prevents routine use as a convenience? | Open | Technical bounds beat policy — time limits, mandatory notification, second-party alerting. | A break-glass design. |
| OQ-073 | Where does the external audit log live such that an operator cannot alter it, on a platform the same operator runs? | Open | — | An audit architecture. |
| OQ-074 | Deletion verification across three stores plus object storage plus backups — what proves completion rather than asserting it? | Open | Related to OQ-036. | A verification design. |

## Extended use — added by the gap pass

| ID | Question | Status | Current Prep Answer | What Closes It |
| :--- | :--- | :--- | :--- | :--- |
| OQ-075 | Is a professional role displayed at all, given the platform cannot verify it and an unverified credential invites misuse as a trust signal? | Open | Self-described, display only, confers no access. Whether to display at all is undecided. | A display decision. |
| OQ-076 | Does the citable reference export need attribution or usage terms beyond CC BY-SA 4.0? | Open | — | A licensing review of the reference repository. |
| OQ-077 | Is the closed position on server-side plugins permanent, or could a sandboxed design hold? | Open | Closed. Any sandbox must enforce consent inside itself, which is the hard and probably disqualifying part. | A sandbox design that enforces consent, or confirmation that the position is permanent. |
| OQ-078 | Does user-authorised export cover derived data — embeddings, simulation results, trajectories — or only source records? | Open | Derived data is more disclosive per byte. | An export scope decision. |
