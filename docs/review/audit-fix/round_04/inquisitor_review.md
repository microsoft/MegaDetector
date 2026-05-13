# Inquisitor review — round 4 (convergence candidate)

## Approval decisions recap
Both editor plans NOTHING-TO-DO. Zero source edits this round (no `action="fixed"` entries from round 4). The combined APPROVAL+FINAL_REVIEW phase therefore has nothing to approve and nothing to apply — only re-verification of the round-3 HEAD against every ledger file.

## Fix verification (per ledger file)
<a name="README-md"></a>
### README.md
Verified clean at HEAD `f83929b`. Round-3 fixes (commit `a41abfe`) all intact:
- L54 V6 tagline: `**SMALLER, FASTER, BETTER**` — no `76M` / `MIT/Apache` / `licensing flexibility`.
- L64–70 Model Variants table: exactly 5 rows, all `AGPL-3.0` (MDV6-yolov10-e 29.5M, MDV6-yolov9-e 58.1M, MDV6-rtdetr-c 31.9M, MDV6-yolov9-c 25.5M, MDV6-yolov10-c 2.3M). Matches `cli.py:SUPPORTED_DETECT_VERSIONS`, `training_utils.get_model_path`, and `docs/training_guide.md:87–91`.
- L280 Version-History V6.0 row: `2.3M–58.1M | YOLOv9/v10 + RT-DETR variants (AGPL-3.0)` — min/max matches the variants table.
- L340 License footer: `… AGPL-3.0 — see the [Model Variants](#model-variants) table …`; anchor `#model-variants` resolves to the H3 at L62.

L5 still contains "available under permissive licenses" — this is the pre-existing umbrella tagline whose referents are the MegaDetector code (MIT, footer L340) and the PyTorch Wildlife framework (MIT). Considered and explicitly deferred in rounds 2 and 3 (round-2 NEW=5 list did not include it; round-3 close confirmed it); not a regression, not a NEW finding. No action needed.

<a name="megadetector-md"></a>
### megadetector.md
Verified clean. Last touched at `e58feca` (round 1). Canonical-pointer banner intact (L1–3 HTML comment + L6–7 `[!NOTE]` block pointing to README.md). SPARROW row L54 carries the round-1 typo fix. Only V6 variant string referenced is `MDV6-yolov10-c` at L23, which is a supported variant. No license-variety / parameter-range claims.

<a name="pyproject-toml"></a>
### pyproject.toml
Verified clean. Last touched at `e58feca`. All 5 `[project.urls]` entries (L49–53) point to `github.com/microsoft/MegaDetector` — Homepage, Documentation, Repository, "Source Code", "Bug Tracker". `[project.scripts] megadetector = "megadetector_ai.cli:main"` (L55–56) resolves correctly to `cli.py:main` (L171, `__main__` guard at L243). License `{text = "MIT"}` consistent with README.md:340.

<a name="environment-yaml"></a>
### environment.yaml
Verified clean. Last touched at `e58feca`. Linux-x86_64 caveat banner (L1–8) intact; `name: megadetector-finetuning` at L10 matches `docs/training_guide.md:30` (`conda activate megadetector-finetuning`). pip subtree at L36–170 is platform-portable per the banner.

<a name="docs-training-guide-md"></a>
### docs/training_guide.md
Verified clean. Last touched at `b709a15` (round 2 — AUD-203 `plot` → `plots` cascade). 5-variant whitelist at L85–91 all `AGPL-3.0` matches `cli.py:SUPPORTED_DETECT_VERSIONS`, `training_utils.get_model_path`, README.md table. `plots` key at L130 matches `examples/config_training.yaml:25` and `training.py:120`. Default `model_name: MDV6-yolov9-e` at L106 matches `examples/config_training.yaml:3` and is a supported variant. `weights` description at L125 ("Default: None") is the pre-existing doc-lag re. REV-003 `weights: null`; explicitly deferred in rounds 1–3 as non-blocking (the runtime-correct value is `null`; the doc string `None` is a description not a literal). Not a NEW finding.

<a name="src-megadetector-ai-init-py"></a>
### src/megadetector_ai/__init__.py
Verified clean. Last touched at `e58feca`. Re-exports `MegaDetectorV6` and `MegaDetectorV5` from `.detector`; `__version__ = "0.1.0"` matches `pyproject.toml:7`.

<a name="src-megadetector-ai-detector-py"></a>
### src/megadetector_ai/detector.py
Verified clean at HEAD `f83929b`. Round-3 fix (commit `a41abfe`) intact:
- V6 docstring summary L15–16: `Multiple model variants are available, ranging from 2.3M to 58.1M parameters.` — no `76M`, no license-flexibility claim.
- V6 docstring `version` arg L22–27: enumerates the 5 PW-1.2.4.2-supported variants only; matches README table.
- V5 docstring L44–45: `Still available for backward compatibility. We recommend V6 for new projects — it is smaller and faster.` — "permissive license options" framing removed.

IDE-hover surface is now consistent with README.md Model Variants table.

<a name="src-megadetector-ai-training-py"></a>
### src/megadetector_ai/training.py
Verified clean. Last touched at `badc1c2` (round 1 — REV-002/003/006/007/009). `_prepare_data_config` (L56–78) writes a sidecar under `runs/_resolved_data/`, never mutates the user's YAML (REV-002). `_load_model` resume guard (L24–30) explicitly raises on string `"None"` / empty / null `weights` (REV-003). YOLO vs RTDETR consistency checks (L35–44) intact. `inference()` per-image `try/except` (L142–149) intact with descriptive warning (REV-009). `plots=cfg.plots` at L120 matches the YAML key.

<a name="src-megadetector-ai-training-utils-py"></a>
### src/megadetector_ai/training_utils.py
Verified clean. Last touched at `badc1c2` (round 1 — REV-010). 5-branch `model` whitelist (L7–21) exactly matches `cli.py:SUPPORTED_DETECT_VERSIONS` and the README/training-guide tables. `else: raise ValueError(...)` (L22–23) lists the 5 supported names. CWD-writability precheck (L27–32) intact, raises a descriptive `PermissionError` before `wget.download()` tries to scribble into a read-only CWD.

<a name="src-megadetector-ai-cli-py"></a>
### src/megadetector_ai/cli.py
Verified clean. Last touched at `badc1c2` (round 1 — REV-004/005/008). `SUPPORTED_DETECT_VERSIONS` (L20–26) matches the 5-variant whitelist. `argparse` `--model` `choices=SUPPORTED_DETECT_VERSIONS` (L191) prevents unsupported variants at parse time; default `MDV6-yolov9-c` (L190) is supported. `train` / `validate` / `inference` wrappers (L114–168) each catch `(ValueError, KeyError, AttributeError, FileNotFoundError)` with descriptive stderr output (REV-008). `__main__` guard at L243.

<a name="examples-config-training-yaml"></a>
### examples/config_training.yaml
Verified clean. Last touched at `badc1c2` (round 1 — REV-001/003). `plots: True` (L25) matches `training.py:120` `cfg.plots`. `weights: null` (L21) is real Python `None`, not the string `"None"` — REV-003 fix intact. `model_name: MDV6-yolov9-e` (L3) is a supported variant.


## Missed issues (NEW this round)
None — round 4 is a clean no-change convergence round. All prior fixes (round 1 reviewer 10-item sweep, round 2 auditor 3-item sweep, round 3 auditor 2-item sweep of round-2's NEW findings) are verified in place at HEAD `f83929b`. The remaining "permissive licenses" wording at `README.md:5` and the "Default: None" doc-string at `docs/training_guide.md:125` are pre-existing, were never raised as NEW findings in any round, are non-blocking (no command fails, no crash), and were explicitly deferred in rounds 1–3 reports. Re-opening them now would be drift, not convergence.

## Cross-impact analysis
Zero source edits this round → no cross-impact to assess. The cross-surface 5-variant invariant (README Model Variants ↔ detector.py V6 docstring ↔ cli.py SUPPORTED_DETECT_VERSIONS ↔ training_utils.get_model_path branches ↔ docs/training_guide.md whitelist ↔ examples/config_training.yaml default model_name) was checked end-to-end during per-file verification and holds across all 6 surfaces.

## Verification results
`docs/review/audit-fix/round_04/verification.txt` summary: ruff clean; py_compile clean; `examples/config_training.yaml` parses with `plots` key present; `environment.yaml` parses with env name `megadetector-finetuning`; `pyproject.toml` parses with all 5 URLs at `github.com/microsoft/MegaDetector`; README markers (`### Install from source (for fine-tuning or CLI use)` at L109, `## Fine-Tuning` at L233) present; residual-claims grep for the round-3 targets (`76M`, `MIT/Apache`, `permissive license options`, `licensing flexibility`) returns zero hits. The one match for the generic `permissive license` pattern is the pre-existing umbrella tagline at README.md:5 — not in the round-3 target set, explicitly waived in rounds 2–3.

## Run history (convergence pattern)
- **Round 1**: large fixes — auditor 9 items (README Fine-Tuning section, Install-from-source, Quick Start bridge, SPARROW typo, megadetector.md canonical-source note, pyproject CameraTraps→MegaDetector URLs, environment.yaml rename + platform banner, training_guide editable install + env cascade + config_training.yaml link + back-link, detector.py V5 class enumeration); reviewer 10 items (REV-001..010). Commits `e58feca` (auditor) + `badc1c2` (reviewer).
- **Round 2**: 3 auditor fixes (README V6 variant trim, detector.py V6 docstring trim, training_guide.md `plot`→`plots` cascade); reviewer NOTHING-TO-DO. Commit `b709a15`.
- **Round 3**: 2 auditor fixes resolving round-2's NEW findings (README `76M` / `MIT/Apache` / `licensing flexibility` removal at L54+L280+L340; detector.py docstring same cascade); reviewer NOTHING-TO-DO. Commit `a41abfe`.
- **Round 4**: zero fixes — both editors NOTHING-TO-DO; this is the clean no-change round. **Canonical convergence pattern: each round closes the previous round's NEW findings until a round produces none, followed by a clean verification round.**

## Coverage analysis
- Ledger files: 11
- Verified this round: 11
- Cumulative covered: 11/11
- Uncovered: []
- `action="fixed"` this round: 0
- NEW issues this round: 0

STATUS: CONVERGED SCOPE_CHECK=PASS COVERED=11/11 UNCOVERED=[]
