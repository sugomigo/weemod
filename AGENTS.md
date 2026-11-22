# WeeMOD — agent instructions

Purpose: reuse verified small infrastructure modules with minimal context, not to execute or rewrite unrelated files.

## Discovery and selection

1. Read `catalog/index.json` only; identify module IDs relevant to the user's requested task.
2. Check `runtime`, `use_when`, `avoid_when`, `dependencies` and `status`.
3. Read only the selected `README.md`, allowlisted source files and tests.
4. Never load an entire directory tree as context unless specifically requested.
5. When uncertain, tell the user which constraint is unknown and do not apply the module blindly.

## Integration boundaries

- `python tools/weemod.py pack <id> --out <directory>` exports reviewed allowlisted files only.
- Treat exported code as a **proposal**. Ask for approval before replacing existing implementations.
- Do not alter target project architecture, canonical data models, or license notices without authorization.
- Respect the destination project's instructions and tests.
- Do not execute downloaded scripts blindly; audit dependencies first.

## Security

- Never write, copy, print or commit API keys, tokens, passwords, customer records or internal product code.
- Do not add telemetry/network callbacks to library modules without explicit user request.
- Before contribution, follow `docs/SECURITY.md` and `PUBLICATION_CHECKLIST.md`.

## Local validation

```bash
python -m unittest discover -s tests -v
node --test modules/async-retry/retry.test.mjs
```

## Evidence

Report only test results actually executed. Never invent adoption, savings, stars, downloads or maintenance history.
