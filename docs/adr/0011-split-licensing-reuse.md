# ADR-0011: Split licensing — EUPL-1.2 code, CC BY-SA 4.0 docs, REUSE v3.2

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Repository owner
- **Supersedes / Superseded by:** —

## Context

emBodied needed a licensing posture. The sibling repositories in this collection already use a
consistent model, and there is no reason for this project to diverge from it.

Code and prose have genuinely different needs. A copyleft software licence applied to documentation
produces awkward results around attribution and adaptation; a content licence applied to source
code fails to address patent grants, distribution of binaries and source-availability obligations.

EUPL-1.2 additionally suits a European project: it is an EU-originated licence with official
translations into every EU language, and explicit compatibility provisions with other copyleft
licences.

## Decision

Adopt the `cordanaLLM` split-licensing model, REUSE v3.2 compliant:

- **EUPL-1.2** — all code, schemas, configuration and scripts
- **CC BY-SA 4.0** — all documentation, prose and architecture decision records

Declared via a root `REUSE.toml` with aggregate annotations rather than per-file SPDX headers,
matching the sibling convention. Licence texts live in `LICENSES/`.

`reuse lint` is part of the local gate and of CI.

## Consequences

Both licences suit their material. Contributors and consumers have a machine-readable declaration
of what governs which file, and `reuse lint` makes drift a build failure rather than a discovery.

Consistency with the sibling repositories means tooling, CI steps and habits transfer directly.

BSD-3-Clause dependencies, including the Buttplug library adopted in ADR-0010, are compatible with
EUPL-1.2 — so the device ecosystem is usable without a licensing conflict.

Costs: two licences means contributors must understand which applies where, and the boundary needs
maintaining in `REUSE.toml` as new directories appear. The aggregate-annotation approach keeps this
to one file, which is why it was chosen over per-file headers.

EUPL-1.2's copyleft is genuine. Anyone distributing a modified version must make source available
under a compatible licence — intended, and worth stating plainly rather than discovering later.

## Alternatives considered

**A single licence for everything.** Simpler and applies a licence unsuited to half the repository
in either direction.

**AGPL-3.0 for code.** Comparable copyleft strength with wider recognition. Rejected for
consistency with the sibling repositories and because EUPL-1.2's EU-language status and
compatibility provisions suit this collection.

**Permissive licensing.** Rejected: nothing in the project's purpose calls for allowing
proprietary redistribution.

**Per-file SPDX headers rather than aggregate annotations.** More explicit per file and noisier in
every document. The sibling convention uses aggregate annotations, and it was followed.

## References

- User direction, 2026-09-16 (paraphrased): concentrate on developing the software first, license
  it under EUPL, and bring it into full conformance.
- `cordanaLLM/Tribunus` `tribunus-description-v2.md`: "**EUPL-1.2** (European Union Public Licence
  v1.2) for all Go code, Rust crates, scripts, and schemas. **CC BY-SA 4.0** ... for all
  documentation, prose, and architectural decision records. **REUSE v3.2 Compliance**: Fully
  annotated with SPDX headers and a root `REUSE.toml` mapping file."
- Rename note, 2026-11-18: `cordanaLLM/Tribunus` is now
  [Epitrop](https://github.com/tekmora/epitrop) at `tekmora/epitrop` (renamed 2026-10-11; the old
  address redirects). The wording quoted above is not in that repository's history: on
  2026-11-18, `git log --all -S '<phrase>'` for each quoted phrase found no commit among the 306
  commits on all refs of a clone at `0c759dbd`.
- `cordanaLLM/praetor` `REUSE.toml` — aggregate annotation pattern
- [buttplug.io](https://buttplug.io/) — BSD-3-Clause, compatible with EUPL-1.2
