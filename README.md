# WeeMOD

**Reusable, agent-discoverable modules for software builders.**

WeeMOD is a small public library of reusable software building blocks. Each module has an explicit scope, dependency list, limitations, and runnable tests. Human developers and coding agents can discover a module from a short catalog, inspect it, and export only the files needed for the task.

> Status: **v0.1 starter / early prototype**. Token savings and integration benefits are goals to measure, not established results.

## What problem does it solve?

Developers repeatedly build basic infrastructure (retry handling, safe file operations, data validation, etc.). WeeMOD aims to make vetted, generic components easier to **find, understand, reuse, and verify**, without pulling a whole product codebase into an AI agent's context.

## Quick start

Requirements: Python 3.10+ for the optional module selector, Node.js 18+ for the example JavaScript module/tests.

```bash
python tools/weemod.py list
python tools/weemod.py inspect async-retry
python tools/weemod.py pack async-retry --out ./out/async-retry
node --test modules/async-retry/retry.test.mjs
```

The `pack` command exports only the files allowlisted for the selected module; review them before copying into another project. The output is **source code, not an automatically integrated dependency**.

## Agent workflow

1. Read `AGENTS.md` and `catalog/index.json` first.
2. Select by task, runtime and listed `avoid_when` constraints.
3. Inspect the module README and source; do not load unrelated modules.
4. Run module tests, then adapt integration inside the target project.
5. Record any changes made during integration; do not silently claim compatibility.

Example instruction to your coding agent:

> Inspect WeeMOD's catalog for reusable modules related to retrying idempotent API requests. Read only the relevant module and its tests. Explain applicability, license, dependencies and limitations before copying code. Do not import other modules or modify unrelated files.

## Structure

```text
WeeMOD/
  AGENTS.md                 # Instructions for coding agents
  catalog/index.json        # Single source of module metadata
  modules/async-retry/       # One working reference module
  tools/weemod.py            # List / inspect / selective pack CLI
  docs/MODULE_STANDARD.md    # Admission and quality contract
  docs/SECURITY.md           # Public contribution security rules
  docs/ROADMAP.md            # Milestones and evidence principles
  .github/workflows/ci.yml   # Automated tests on GitHub push/PR
  PUBLICATION_CHECKLIST.md   # Required checks before going public
  LICENSE                   # MIT draft; fill owner before release
```

## Current module

| ID | Runtime | Use | Avoid |
|---|---|---|---|
| `async-retry` | Node.js 18+ ESM | Retry transient failures in **idempotent** async operations | Non-idempotent operations without a deduplication strategy |

## Open source and provenance

Only code with verified publication rights may enter WeeMOD. Do not copy company/customer code, proprietary assets, credentials, private architecture or incompatible third-party code. External contributions need proper attribution and license review.

The proposed license is MIT, **subject to completing `LICENSE` ownership information and the publication checklist**.

See [MODULE_STANDARD](docs/MODULE_STANDARD.md), [SECURITY](docs/SECURITY.md), and [ROADMAP](docs/ROADMAP.md).
