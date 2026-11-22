# Module contribution contract

A module is eligible for publication only when it is genuinely reusable and the contributor has confirmed rights to publish it.

## Required metadata (catalog/index.json)
- Unique ID, name, purpose, category, tags and status.
- Runtime/language and dependency list.
- `use_when` and `avoid_when` (explicit negative scope).
- Documentation file and explicit exported file allowlist.
- License and test command in module README.

## Required quality gates
- Works independently of any private Wee project and does not import private files.
- Does not contain secrets, confidential employer/customer information, copied external code without permission, or telemetry by default.
- Has basic usage example, edge-case tests and limitations.
- Has an explicit owner and version/release note (via Git history and GitHub Releases).
- Agent may list/inspect/export without automatically modifying the destination project.

## Proposed next candidates (NOT shipped)
- Event emitter helper
- Lightweight schema validation
- Retry with richer HTTP semantics
- Idempotency utilities
- Logging interface adapters

Assess real need, redundancy, license and tests before adding any new module.
