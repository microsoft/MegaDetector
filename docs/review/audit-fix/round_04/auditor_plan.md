# Auditor plan — round 4

## Anti-drift orientation

Per the shared protocol (`~/.copilot/skills/_shared/iterative-anti-drift.md`):
- **Skill mode:** `editing` (per `SCOPE_LEDGER.json:convergence_mode`)
- **My owned files (per `round_04/file_ownership.md`):** README.md, megadetector.md, pyproject.toml, environment.yaml, docs/training_guide.md, src/megadetector_ai/detector.py, docs/audit_report.md.
- **HEAD:** `f83929b` (round-3 review artifacts) on top of fix commit `a41abfe`.
- **Round-3 inquisitor STATUS line** (`round_03/inquisitor_review.md:113`): `NEEDS-MORE SCOPE_CHECK=PASS COVERED=11/11 UNCOVERED=[] NEW=2`. The `NEW=2` is the 2 applied fixes themselves under the strict editing-mode rule ("any `fixed` entry this round → NEEDS-MORE"); the review body explicitly states `NEW issues this round: 0` (line 101) and `NEW_FINDINGS=0` (line 107).

## Verification of round-3 fixes (spot-check, this round)

All 5 sites flagged by the round-2 inquisitor and fixed at `a41abfe` are intact:

- **README.md L54** — `The latest release focuses on **efficiency** and **modern architectures** — **SMALLER, FASTER, BETTER**.` (license tagline removed).
- **README.md L64–70** — Model Variants table: exactly 5 rows, all AGPL-3.0 (`MDV6-yolov10-e` 29.5M, `MDV6-yolov9-e` 58.1M, `MDV6-rtdetr-c` 31.9M, `MDV6-yolov9-c` 25.5M, `MDV6-yolov10-c` 2.3M).
- **README.md L280** (Version History V6.0 row) — `2.3M–58.1M | YOLOv9/v10 + RT-DETR variants (AGPL-3.0)`.
- **README.md L340** (License footer) — `Individual model weights documented in this repository are released under AGPL-3.0 — see the [Model Variants](#model-variants) table for details.` Anchor `#model-variants` resolves to `### Model Variants` H3 at L62.
- **src/megadetector_ai/detector.py L16** (V6 docstring summary) — `Multiple model variants are available, ranging from 2.3M to 58.1M parameters.`
- **src/megadetector_ai/detector.py L44–45** (V5 docstring comparative claim) — `Still available for backward compatibility. We recommend V6 for new projects — it is smaller and faster.` "permissive license options" framing removed.

Other owned files unchanged since rounds 1–2 (`git --no-pager log -- README.md megadetector.md pyproject.toml environment.yaml docs/training_guide.md src/megadetector_ai/detector.py docs/audit_report.md` shows last touch at `a41abfe` for README+detector, `b709a15` for training_guide, `e58feca` for the rest):
- **megadetector.md** — canonical-pointer banner + README link at L7 intact; `grep "MDV6-"` returns only `MDV6-yolov10-c` at L23 (a supported variant); no license-variety claims.
- **pyproject.toml** — 5 project URLs (L49–53) all `microsoft/MegaDetector`; `[project.scripts] megadetector = "megadetector_ai.cli:main"` matches `cli.py:main` entrypoint.
- **environment.yaml** — `name: megadetector-finetuning` at L10; Linux-x86_64 caveat banner at L1–8 intact.
- **docs/training_guide.md** — 5-variant whitelist (L87–91) all AGPL-3.0 and matches `cli.py` `SUPPORTED_DETECT_VERSIONS`; round-2 AUD-203 `plot` → `plots` fix at L130 intact; `model_name: MDV6-yolov9-e` default at L106 matches `cli.py:20-26` whitelist.
- **docs/audit_report.md** — round-1 deliverable; executive summary, findings, README paste-in section, next steps all present (256 lines); never re-opened.

## Cross-cutting stale-string scan

Repo-wide grep across all 7 owned files for the round-2/round-3 target patterns:

```
grep -nE "76M|MIT/Apache|licensing flexibility|permissive license options" \
  README.md src/megadetector_ai/detector.py docs/training_guide.md \
  megadetector.md pyproject.toml environment.yaml docs/audit_report.md
```

Result: **zero hits**. The one surviving "permissive license" wording at `README.md:5` ("available under permissive licenses") was explicitly considered and deferred in round 3 — its referents are the MegaDetector code (MIT) and the PyTorch Wildlife framework (MIT), consistent with the unchanged `The MegaDetector code is released under the [MIT License](LICENSE)` clause at L340. Not a new issue; pre-dates round 1; not a regression.

## Cross-surface consistency (post-round-3)

The 5-variant set is now consistent across all 5 surfaces:

| Surface | Location | Set |
|---|---|---|
| README Model Variants table | L64–70 | 5 rows, AGPL-3.0 |
| detector.py V6 docstring bullets | L22–27 | same 5 variants |
| cli.py `SUPPORTED_DETECT_VERSIONS` | L20–26 (reviewer-owned) | same 5 |
| training_utils.get_model_path | 5 branches (reviewer-owned) | same 5 |
| docs/training_guide.md whitelist | L87–91 | same 5, AGPL-3.0 |

`examples/config_training.yaml model_name: MDV6-yolov9-e` (reviewer-owned) is one of the 5. README L280 `2.3M–58.1M` matches min/max (`MDV6-yolov10-c` 2.3M / `MDV6-yolov9-e` 58.1M).

## Findings this round

**None.** Round 3 closed both the round-2 cascade (runtime-crash variant references) and the doc-vs-doc factual cascade (license-flexibility claims with no surviving referent). All previously deferred items (`README.md:5` umbrella tagline, `docs/training_guide.md:125` weights doc-lag) were considered and remain explicitly deferred — they are pre-existing, were never raised as NEW findings in any round, and have non-blocking failure modes (the training-time `ValueError("Got: 'None'")` per REV-003 is the user-facing surface, not a doc claim).

## Plan
No edits proposed in round 4. Round 3 swept the residual NEW findings; rounds 1–3 collectively swept all in-scope structural issues across my 7 owned files. The 2 round-3 fixes have been independently spot-checked at HEAD and remain intact.

STATUS: NOTHING-TO-DO
