# WeeMOD roadmap / checkpoints

## P0 — Public-safety gate (pre-public checks verified; see GitHub Releases for release status)
- [x] Owner declared publication rights for all 15 tracked source and README files.
- [x] Replace `LICENSE` copyright placeholder with `sugomigo` and confirm MIT license choice.
- [x] Run both test suites locally (7/7 Python unittest, 7/7 Node test) and review the local publication checklist.
- [x] Create private GitHub repository (`sugomigo/weemod`), push `master`, and verify GitHub Actions CI passes (7/7 Python, 7/7 Node).

## P1 — Minimal useful OSS (prototype prepared; authoritative release status on GitHub Releases)
- [x] Machine-readable catalog schema (prototype)
- [x] Agent instructions and minimal selector (prototype)
- [x] One self-contained example module and tests (prototype)
- [ ] Release public `v0.1.0` after P0 (verify live on GitHub Releases)
- [ ] Record real release link and commit SHA after publication

## P2 — Useful to an external developer
- [ ] Feedback from at least one independent user, if actually obtained
- [ ] Validate external integration in a separate clean example project
- [ ] Improve metadata / CLI using actual issues rather than speculative features

## P3 — Validate efficiency hypothesis
- [ ] Define comparable tasks and baseline workflows
- [ ] Measure time-to-integration, token inputs/outputs when tooling exposes them, test pass rate, and manual correction effort
- [ ] Publish methodology and results, including any negative results

**Never fabricate stars, downloads, issues, user adoption, token savings or sponsorship qualification.**
