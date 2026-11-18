# emBodied — Master Concept (Canonical)

> **Status:** Concept · **Language:** English · **Licence:** CC BY-SA 4.0
> **Supersedes:** the recovered German draft of 2026-01-15.
> Module detail lives in [docs/concept/](concept/README.md). This document states what the
> platform *is*; the module pages state how each part works.

---

## 0. Definition

emBodied is a private, international adult platform for the realistic modelling,
representation, discussion and experience of human bodies, sexuality and intimacy.

**Consent is the only hard boundary.**

The platform makes no editorial ruling on whether content is pornographic, medical, educational
or artistic. That boundary does not survive contact with reality: a well-lit anatomical
photograph will be called pornography by someone regardless of intent, and a piece of
pornography may be the most accurate anatomical reference a person has ever seen. emBodied
therefore does not classify. It describes, and it lets people choose what they want to see.

Classification appears in exactly one place — a legal age gate where jurisdiction requires one —
and that flag is explicitly a legal artifact carrying no editorial meaning.

---

## 1. Principles

1. **Bodies are real, not idealised.** The reference is the distribution, not the ideal.
2. **Fantasy is not reality.** Both are legitimate. Neither is mistaken for the other.
3. **Expression is not a special case.** The platform does not grant permission for sexual
   content, because it does not treat sexual content as requiring permission.
4. **Consent outranks morality, which outranks taste.** Only the first is enforced.
5. **Simulation is orientation, not a promise.** Every prediction carries its uncertainty.
6. **There is no default body.** Anatomy is a set of features, never a type with variants.
7. **Uncertainty is shown, never hidden.** A number without a sample size and an interval is a
   claim the platform will not make.

---

## 2. What the platform actually does

| # | Capability | Modules |
| :-- | :--- | :--- |
| I | Records a body accurately, and says how strongly each measurement is established | [`measurement`](concept/l1-core/measurement.md), [`verification`](concept/l1-core/verification.md) |
| II | Places that body in a real distribution, with honest uncertainty | [`statistics`](concept/l1-core/statistics.md), [`reference`](concept/l1-core/reference.md) |
| III | Shows it — 2D comparison, anatomical 3D, photoreal 3D | [`visualizer`](concept/l3-expression/visualizer.md) |
| IV | Predicts compatibility and experience, and learns when it is wrong | [`simulation`](concept/l2-intelligence/simulation.md), [`learning`](concept/l2-intelligence/learning.md) |
| V | Lets people inhabit their real body, alone and with others | [`embodiment`](concept/l4-presence/embodiment.md), [`rooms`](concept/l4-presence/rooms.md) |
| VI | Carries media and conversation under binding consent | [`media`](concept/l3-expression/media.md), [`live`](concept/l4-presence/live.md) |
| VII | Teaches, anonymously, without requiring exposure | [`education`](concept/l5-community/education.md), [`spaces`](concept/l5-community/spaces.md) |

---

## 3. Identity

Two tiers, and one person may hold both.

**Anonymous tier.** No profile, no account required. Reads education content, browses statistics,
uses the visualizer against reference distributions. Contributes nothing and is asked for nothing.
This tier exists so that learning about your own body never requires exposing it.

**Profile tier.** A deliberate, opt-in step. Carries body data, media, texts, preferences and
community presence, always under a pseudonym. Roles — sexual, psychological, social, contextual —
are self-described attributes, not categories the platform assigns.

Visibility is granular and defaults closed. See [`identity`](concept/l1-core/identity.md)
and [`consent`](concept/l1-core/consent.md).

---

## 4. Anatomy and body data

A profile is **a set of anatomical features**, each with its own measurement schema and its own
reference cohort. Gender and identity are separate social attributes that never gate which
features a person may record.

This is the inclusive model and also the correct one: intersex, trans and post-surgical bodies
require no special case because there is no default case. Common configurations are offered as
**presets** so that ordinary signup is not a schema exercise — presets are starting points, freely
editable, never constraints.

Every measurement carries a **verification grade** (see §6) and a plausibility assessment.

See [`anatomy`](concept/l1-core/anatomy.md), [`measurement`](concept/l1-core/measurement.md).

---

## 5. Statistics and population comparison

Reference data is **versioned, citable and physically separated from user data** — it lives in its
own repository with its own release cadence.

The baseline is published literature using measured rather than self-reported protocols. User
measurements form a clearly separate overlay, never silently merged into the reference curve.

**On population differences.** Human populations do differ measurably, and the mechanism is
evolutionary and regional — climate, latitude, UV exposure, founder effects, genetic drift. That
is legitimate, interesting content and the platform keeps it. What the platform does not do is
present those differences as facts about racial categories. Comparisons are framed by study
cohort and region, always with sample size, measurement protocol and confidence interval
attached, and always stating what the data cannot support. Individual variation dwarfs group
means, and the platform says so wherever it shows a group mean.

See [`statistics`](concept/l1-core/statistics.md), [`reference`](concept/l1-core/reference.md),
and [ADR-0008](adr/0008-population-comparison-as-regional-adaptation.md).

---

## 6. Verification

One subsystem, four grades, consumed by everything that needs to know how much to trust a number:

| Grade | Meaning |
| :--- | :--- |
| `self-reported` | The person entered it. |
| `protocol-guided` | Entered following a defined measurement protocol. |
| `evidenced` | Supported by artifact evidence against that protocol. |
| `witnessed` | Independently confirmed. |

Statistics decides its own inclusion threshold. Avatar authenticity decides its own. Pair
simulation decides its own. One implementation, one audit trail.

See [`verification`](concept/l1-core/verification.md), [ADR-0006](adr/0006-graded-verification-subsystem.md).

---

## 7. Intelligence — vector and graph

The quantitative core is a **learned body-vector** plus a **knowledge graph**, not a hand-authored
formula.

Measurements are projected into a learned vector space trained against reported outcomes, so
similarity means *bodies that behave alike*, not *bodies with similar numbers*. Compatibility
becomes neighbourhood search in that space, qualified by the graph.

Reported experience does not adjust a coefficient — it writes edges. The model improves because
the graph grows, which is what §8 means by a learning system.

See [`body-vector`](concept/l2-intelligence/body-vector.md),
[`knowledge-graph`](concept/l2-intelligence/knowledge-graph.md),
[ADR-0009](adr/0009-learned-body-vector.md).

---

## 8. Simulation and reality feedback

Simulation is geometric, biomechanical and statistical together — dimensional fit, tissue
response and accommodation, and outcome distributions from comparable pairings.

Every result is reported with its uncertainty and with the evidence grade of the inputs that
produced it. A prediction built from two self-reported measurements says so.

The feedback loop is opt-in, structured, and the most sensitive data class on the platform. It is
consent-bound at the point of collection and separable from the profile that produced it.

See [`simulation`](concept/l2-intelligence/simulation.md), [`learning`](concept/l2-intelligence/learning.md).

---

## 9. Expression and media

Media is carried, not curated. Upload, transcode, storage and delivery, with **consent bound to
every asset** as a first-class property rather than a moderation afterthought.

Because the platform refuses to classify content, **descriptive tags are the only control
surface** — which means tag integrity is a safety system, not metadata hygiene. Uploaders describe
what is depicted in neutral anatomical and situational terms; a classifier proposes descriptors
for confirmation; and mis-tagging is actively watched for rather than assumed away. Viewers
compose their own filters from those descriptors.

See [`media`](concept/l3-expression/media.md), [`tagging`](concept/l3-expression/tagging.md),
[`moderation`](concept/l3-expression/moderation.md), [ADR-0005](adr/0005-no-editorial-classification.md).

---

## 10. Presence and embodiment

The visualizer renders one geometry model three ways — 2D comparison against percentile bands,
anatomical 3D, and photoreal 3D — chosen by the viewer, because the platform does not decide
whether someone is here clinically or erotically.

From that same geometry comes the **avatar**: a person's verified real body, rigged and
inhabitable. Solo embodiment first, then limited invited rooms, with open social space as the
long-term goal.

Physical device control is a kernel capability, built on the Buttplug Rust library — same language
as the compute kernel, and an existing ecosystem of 750+ devices rather than a driver stack of our
own.

See [`visualizer`](concept/l3-expression/visualizer.md), [`avatar`](concept/l3-expression/avatar.md),
[`embodiment`](concept/l4-presence/embodiment.md), [`device`](concept/l4-presence/device.md).

---

## 11. Community, education and protected space

Content lives in **spaces** — education, experience, expression — and the space sets the
expectation, alongside per-item descriptors.

Education is reachable from the anonymous tier by design. The people who most need to learn what a
normal body looks like are the least willing to expose their own, and a platform that demands a
profile before it will answer that question has failed them.

Progress is personal and non-competitive. No rankings, no leaderboards, no comparison of persons —
on a platform built around measurement, this is a constraint that has to be actively defended.

See [`spaces`](concept/l5-community/spaces.md), [`education`](concept/l5-community/education.md),
[`progress`](concept/l5-community/progress.md).

---

## 12. Architecture

Planned stack ([ADR-0001](adr/0001-go-rust-svelte-split.md); no code exists in this repository yet):
Go control plane, Rust compute kernel, Svelte 5 interface — following the `cordanaLLM/Tribunus`
pattern.

```text
[ SvelteKit / Svelte 5 UI ] <--- SSE / REST ---> [ Go Control Plane ]
                                                   internal/{identity,consent,anatomy,
                                                             measurement,verification,
                                                             reference,statistics}
                                                              |
                                                          FFI / IPC
                                                              v
                                                   [ Rust Compute Kernel ]
                                                     crates/{vector,graph,stats,sim,
                                                             learn,device}
                                                              |
                                         +--------------------+--------------------+
                                         v                    v                    v
                                   PostgreSQL              Qdrant              Memgraph
                                   (records)              (vectors)             (graph)
```

The Rust kernel owns everything quantitative: embeddings, similarity, graph traversal,
statistics, the simulation model, and device control. Go is control plane and API. Visualizer
geometry compiles to WASM so client and server share one model and cannot drift.

Reference data lives in a separate repository — the physical separation of user data from
reference data is a repository boundary, not only a schema one.

See [docs/concept/README.md](concept/README.md), [ADR-0001](adr/0001-go-rust-svelte-split.md),
[ADR-0002](adr/0002-relational-vector-graph-persistence.md), [ADR-0007](adr/0007-user-reference-data-separation.md).

---

## 13. Governance and licensing

HISS-16 via Praetor. `AGENTS.md` canonical, vendor harnesses compiled from it. EUPL-1.2 for code,
CC BY-SA 4.0 for documentation, REUSE v3.2 throughout.

See [ADR-0011](adr/0011-split-licensing-reuse.md).

---

## 14. Not decided here

Phasing and first-release scope · jurisdiction and hosting · age verification · payments,
subscriptions and creator earnings · launch posture.

These are deliberately deferred. They are tracked in
[OPEN-QUESTIONS.md](design-basis/OPEN-QUESTIONS.md), not forgotten.
