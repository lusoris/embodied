# Contributing to embodied

Thank you for contributing! This repository adheres strictly to the
**High-Integrity Systems Standard (HISS)** and modernized **NASA JPL
Power-of-10** rules defined in the *Core Directives & Invariants* table of
[AGENTS.md](AGENTS.md).

## Core Directives & Verification

Local prerequisites for running the verification gate (`Makefile`):

- **Praetor engine**: `praetorctl` (or its older name `standardsctl`) on `PATH`,
  installed from the [Praetor repository](https://github.com/cordanaLLM/praetor);
  the `Makefile` resolves whichever name is installed.
- **gitleaks v8.30.1**: Install it with `mise use --global gitleaks@8.30.1` or
  the `gitleaks` v8.30.1 release archive binary — a Go-built `gitleaks` lacks
  the version stamp and shadows the pinned binary when earlier on `PATH` (e.g.
  `~/go/bin`).
- **Git and Python 3**: `git` and `python3` on `PATH` for the file-type gate and
  unit tests.

All changes must pass local verification before submitting:

```bash
make verify-all
```

### Modernized NASA JPL Power-of-10 Rules

Each rule names its row in the canonical HISS table of [AGENTS.md](AGENTS.md):

1. **Simple Control Flow (HISS-01)**: Recursion is strictly banned; call graph
   must be an acyclic DAG; zero `goto`.
2. **Bounded Loops and I/O Deadlines (HISS-02)**: All loops must have a
   statically verifiable scalar upper bound. Every network and disk I/O call
   requires an explicit deadline across all languages; in Go, I/O takes a
   `context.Context` deadline.
3. **Deterministic Memory (HISS-03)**: Zero dynamic heap allocations
   (`malloc` / `free`) in hot simulation or rendering loops.
4. **Function Length Cap (HISS-04)**: No function may exceed
   **60 lines of code** ($\le 60$ LOC).
5. **Data Scope (HISS-05)**: Declare every identifier in the smallest lexical
   scope serving it.
6. **Checked Errors (HISS-07)**: Check return values of all non-void functions;
   zero `.unwrap()` or unchecked errors.
7. **Static Execution (HISS-08)**: Dynamic code evaluation (`eval` / `exec`)
   and banned unsafe libc calls (`gets` / `strcpy` / `sprintf`) are prohibited.
8. **Pointer Safety (HISS-09)**: Pointer arithmetic must be bounded; all
   `unsafe` blocks require `// SAFETY:` justifications.
9. **Zero-Warning Hygiene (HISS-10)**: Zero compiler, linter, or formatting
   warnings tolerated across all builds.

### 3D Testing Discipline (HISS-15)

Every public function requires:

- **Positive tests**: Expected valid operational inputs.
- **Negative tests**: Invalid inputs, expected error returns.
- **Boundary tests**: Zero, one, max limits, off-by-one bounds.

### Commit Messages

We enforce Conventional Commits:

- `feat:` New features
- `fix:` Bug fixes
- `chore:` Maintenance and governance
- `feat!:` / `fix!:` Breaking API changes (must include `Migration:` footer)
