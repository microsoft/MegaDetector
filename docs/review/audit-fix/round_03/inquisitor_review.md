# Inquisitor review — round 3

## Approval decisions recap
Round 3 reviewer plan was NOTHING-TO-DO. Auditor proposed and applied ITEM-AUD-301 (README — 3 NEW-finding sites from round 2) and ITEM-AUD-302 (detector.py — 2 NEW-finding sites from round 2). Both items APPROVED in Phase 1; both applied at commit `a41abfed` (`docs(audit-fix r3): correct V6 variant claims at residual NEW-finding sites`). `git --no-pager show a41abfed --stat` confirms only `README.md` (6 lines) and `src/megadetector_ai/detector.py` (5 lines) touched — exactly the two files cited by the round-2 NEW findings. All 5 sites edited verbatim per the approved plan.

## Fix verification (per ledger file)

<a name="README-md"></a>
### README.md
**Verdict: VERIFIED clean.** ITEM-AUD-301 (commit `a41abfed`) applied exactly as approved at all 3 round-2-cited sites:
- **L54**: now reads `The latest release focuses on **efficiency** and **modern architectures** — **SMALLER, FASTER, BETTER**.` — "licensing flexibility" tagline removed, which had no referent after the round-2 trim (all 5 documented variants are AGPL-3.0).
- **L280** (Version History V6.0 row): now `2.3M–58.1M | YOLOv9/v10 + RT-DETR variants (AGPL-3.0)` — param max matches the canonical Model Variants table at L64–70 (`MDV6-yolov9-e` = 58.1M); old "76M | MIT/Apache options" cell (referring to the removed `MDV6-apa-rtdetr-e`) is gone.
- **L340** (License footer): now reads `Individual model weights documented in this repository are released under AGPL-3.0 — see the [Model Variants](#model-variants) table for details.` — the internal contradiction is resolved (the link target at H3 L62 is now factually consistent — all 5 rows are AGPL-3.0) and the link is reframed as "details" (param counts, recall, mAP50) rather than "per-variant licensing".

Verified by `grep -nE "76M|MIT/Apache|licensing flexibility" README.md` → zero hits. Anchor cross-check: `grep -n "#model-variants" README.md` → exactly one inbound at L340; `grep -nE "^#{1,3} Model Variants" README.md` → resolves to `### Model Variants` at L62. The MegaDetector *code*-MIT clause at the start of L340 is unchanged (`LICENSE` is still MIT).

One pre-existing umbrella claim at **L5** (`available under permissive licenses`) survives — explicitly deferred by the auditor's plan with the reading that it refers to the repo code (MIT) and PyTorch Wildlife framework (MIT), not to model weights. This line existed identically in commits `e58feca` (round 1) and `b709a15` (round 2); it is NOT a regression introduced by round 3 and was NOT raised as a NEW finding by the round-2 inquisitor (which enumerated lines 54/280/340 only). Recording it here for visibility, not as a NEW finding.

<a name="megadetector-md"></a>
### megadetector.md
**Verdict: VERIFIED clean.** Not touched in round 3 (git log shows last edit at `b709a15` — round 2, content from round 1 and earlier). `grep "MDV6-" megadetector.md` returns only one variant reference (L23: `MDV6-yolov10-c`, a supported variant). No license-variety claims to cascade-fix; no `76M`/`MIT/Apache`/`permissive license`/`licensing flexibility` hits. The hint banner + canonical pointer to README.md (rounds 1–2 fix) remain intact. No regression from round 3.

<a name="pyproject-toml"></a>
### pyproject.toml
**Verdict: VERIFIED clean.** Not touched in round 3 or round 2. `grep` for the round-3 target strings returns zero hits. All declared dependencies (`PyYAML>=6.0`, `munch>=2.0.0`, `wget`, `torch`, `ultralytics`, `PytorchWildlife`) still cover every import in the codebase; project URLs all point to `microsoft/MegaDetector` (round 1 fix intact, confirmed by `verification.txt:14-19`); `[project.scripts] megadetector = megadetector_ai.cli:main` still matches `cli.py:171-244`. No regression from round 3.

<a name="environment-yaml"></a>
### environment.yaml
**Verdict: VERIFIED clean.** Not touched in round 3 or round 2. `name: megadetector-finetuning` (round 1 fix intact, confirmed by `verification.txt:11`). Conda block remains Linux-x86_64-only behind the platform-portability banner; pip subtree pins are a superset of pyproject runtime deps. No regression from round 3.

<a name="docs-training-guide-md"></a>
### docs/training_guide.md
**Verdict: VERIFIED clean.** Not touched in round 3 (round 2's AUD-203 `plot`→`plots` cascade fix at L130 is intact). `grep "MDV6-"` returns the same 5-variant whitelist at L87-91, all marked AGPL-3.0 — internally consistent with README's trimmed Model Variants table. `model_name: MDV6-yolov9-e` default at L106 matches `cli.py:20-26` `SUPPORTED_DETECT_VERSIONS`. No license-variety claims to cascade-fix. The deferred `weights: ... Default: None` lag at L125 remains non-blocking (training raises a clear `ValueError("Got: 'None'")` per round-1 reviewer fix). No regression from round 3.

<a name="src-megadetector-ai-init-py"></a>
### src/megadetector_ai/__init__.py
**Verdict: VERIFIED clean.** Not touched in round 3 or round 2. Re-read end-to-end: module docstring's class-set wording (`animals, people, and vehicles`) consistent with the AUD-013/014 rejection verdict (V6 CLASS_NAMES upstream matches V5); `__version__ = "0.1.0"` matches `pyproject.toml:7`; imports and `__all__` exact match `detector.py`'s public surface. No regression from round 3.

<a name="src-megadetector-ai-detector-py"></a>
### src/megadetector_ai/detector.py
**Verdict: VERIFIED clean.** ITEM-AUD-302 (commit `a41abfed`) applied exactly as approved at both round-2-cited sites:
- **L16** (V6 docstring summary): now reads `Multiple model variants are available, ranging from 2.3M to 58.1M parameters.` — the intra-docstring contradiction with the bullet list at L22-27 (max-param variant in that list is `MDV6-yolov9-e` at 58.1M per README L67) is resolved.
- **L44-46** (V5 docstring comparative claim): now reads `Still available for backward compatibility. We recommend V6 for new projects — it is smaller and faster.` — the "permissive license options" framing (which had zero referent on the class's constructable surface after the round-2 variant trim) is dropped. Genuine comparative claims ("smaller, faster") preserved.

Verified by `grep -nE "76M|MIT/Apache|permissive license|licensing flexibility" src/megadetector_ai/detector.py` → zero hits; AST-rendered `MegaDetectorV6.__doc__` shows `2.3M to 58.1M parameters` followed by the bullet list (V9-c, V9-e, V10-c, V10-e, RT-DETR-c) — no intra-docstring contradiction. The class-set wording at L14 ("Detects animals, people, and vehicles") preserved per AUD-013/014 rejection. `ast.parse` clean; `ruff check src/megadetector_ai/` reports `All checks passed!`. No signature, hierarchy, example block, or `pass` body touched.

<a name="src-megadetector-ai-training-py"></a>
### src/megadetector_ai/training.py
**Verdict: VERIFIED clean (no regression).** Not touched in round 3 (last edit at `badc1c2`, round 1 reviewer fixes). Re-spot-checked against the round-2 trace: `cfg.plots` consumed at L120 → matches YAML `plots:` (post-REV-001) and doc (post-AUD-203); `_load_model` cross-validates `cfg.model` vs `cfg.model_name` and routes through `get_model_path` whitelist (5 supported variants); `_prepare_data_config` writes a sidecar (never mutates user YAML); per-image `try/except` in `inference` with `getattr(results[i], "path", "<index i>")` fallback intact. `py_compile` clean. No regression from round 3.

<a name="src-megadetector-ai-training-utils-py"></a>
### src/megadetector_ai/training_utils.py
**Verdict: VERIFIED clean (no regression).** Not touched in round 3. 5-branch whitelist (L7-22) names the 5 supported variants and `else` raises `ValueError` (L23) listing the same 5. REV-010 CWD-writability precheck (L27-32) intact: `wget.download` only invoked after `os.access(".", os.W_OK)`. Zenodo URLs use record `14567879` consistently. `py_compile` clean. No regression from round 3.

<a name="src-megadetector-ai-cli-py"></a>
### src/megadetector_ai/cli.py
**Verdict: VERIFIED clean (no regression).** Not touched in round 3. `SUPPORTED_DETECT_VERSIONS` (L20-26) = the 5 supported variants, used as argparse `choices=` for `--model` (L191). Module docstring example at L7 uses `MDV6-yolov10-e` (supported). `train/validate/inference` wrappers each catch `(ValueError, KeyError, AttributeError, FileNotFoundError)` and print friendly stderr + exit 1 (REV-008). `_format_detections` CLASS_NAMES matches V6 upstream. `py_compile` clean; `megadetector --help` works per verification.txt. No regression from round 3.

<a name="examples-config-training-yaml"></a>
### examples/config_training.yaml
**Verdict: VERIFIED clean (no regression).** Not touched in round 3. `yaml.safe_load` parses cleanly with 22 keys (`['batch_size_train', ..., 'workers']`); critical fields confirmed: `plots: True` (REV-001), `weights: None` (REV-003), `model_name: MDV6-yolov9-e` (supported variant per `SUPPORTED_DETECT_VERSIONS`). The only-unused YAML key is `task:` — cosmetic, explicitly deferred in rounds 1–2 and not re-raised here. No regression from round 3.

## Missed issues (NEW this round)

**None.** Round 3 was a clean-up of round 2's 5 NEW-finding sites (clustered as 2 NEW findings, one per file). All 5 sites resolved verbatim per the approved plan; no new internal contradictions or orphaned references were introduced by the docstring/README trim. Repo-wide `grep` for the four targeted stale-claim strings (`76M`, `MIT/Apache`, `licensing flexibility`, `permissive license options`) returns zero hits in source files (only audit-fix docs from prior rounds match, which is expected). The anchor reframe at `README.md:340` resolves cleanly: `#model-variants` → `### Model Variants` H3 at L62 (verified by `grep`).

The one pre-existing site that surfaces in `grep "permissive license"` is `README.md:5` (`available under permissive licenses`). This wording (a) existed identically in round-1 commit `e58feca` and round-2 commit `b709a155`, (b) was NOT raised as a NEW finding by the round-2 inquisitor (which enumerated lines 54/280/340 only), and (c) was explicitly considered and deferred by the round-3 auditor plan with the reading that it refers to the repo code (MIT) and PyTorch Wildlife framework (MIT), not to model weights — a reading consistent with the unchanged `The MegaDetector code is released under the [MIT License](LICENSE)` clause at L340. Not a regression introduced by round 3 and not a genuinely new issue. Not counted in NEW_FINDINGS.

## Cross-impact analysis

Round 3 auditor edits affected only docstring/Markdown text in 2 auditor-owned files (`README.md`, `src/megadetector_ai/detector.py`). No behavioral surface touched: no signatures, no class hierarchy, no example code, no `pass` bodies, no anchors, no link restructuring.

- **Auditor changes vs reviewer scope:** Reviewer-owned files (`training.py`, `training_utils.py`, `cli.py`, `examples/config_training.yaml`) untouched since `badc1c2` (round 1). `git --no-pager log --oneline` confirms no commits to those paths in rounds 2 or 3. End-to-end `megadetector train --config examples/config_training.yaml` trace remains valid: YAML 22 keys parse, `plots:`/`weights:`/`model_name:` consumed at the right call sites, whitelist routes via supported variants.
- **Cross-file consistency post-fix:** README Model Variants table (L64-70, 5 AGPL-3.0 rows) ↔ `detector.py` V6 docstring bullet list (L22-27, same 5 variants) ↔ `cli.py` `SUPPORTED_DETECT_VERSIONS` (L20-26, same 5) ↔ `training_utils.get_model_path` whitelist (5 branches) ↔ `docs/training_guide.md` whitelist (L87-91, same 5 with AGPL-3.0) ↔ `examples/config_training.yaml` `model_name: MDV6-yolov9-e` — all five surfaces agree on the same 5-variant set and license. README L280 Version History `2.3M-58.1M` matches the max-min of the canonical table (`MDV6-yolov10-c` 2.3M, `MDV6-yolov9-e` 58.1M). README L340 license footer agrees with the trimmed Model Variants table (all AGPL-3.0).
- **No round-1 or round-2 fix has been re-opened or contradicted:** REV-001/REV-009 plots cascade closed; AUD-203 plot→plots intact at training_guide.md L130; AUD-013/AUD-014 class-set wording rejection preserved verbatim at detector.py L14 ("Detects animals, people, and vehicles"); AUD-201 trim of the variant table preserved at L64-70; AUD-202 trim of the V6 docstring bullets preserved at L22-27.

## Verification results

`round_03/verification.txt` re-inspected end-to-end and independently re-run during this review:

- `ruff check src/megadetector_ai/` → `All checks passed!`
- `python -m py_compile src/megadetector_ai/*.py` → clean
- `python -c "import yaml; ..."` on `examples/config_training.yaml` → 22 keys, includes `plots: True`, `weights: None`, `model_name: MDV6-yolov9-e`
- env name: `megadetector-finetuning` (round 1 fix intact)
- pyproject project URLs all point to `microsoft/MegaDetector` (round 1 fix intact)
- README variant references: only the 5 supported variants surface (verification.txt L22-40); detector.py docstring section: "(none — clean)"
- `grep -nE "76M|MIT/Apache|licensing flexibility" README.md src/megadetector_ai/detector.py` → zero hits
- `grep -nE "permissive license" README.md src/megadetector_ai/detector.py` → 1 hit at `README.md:5` (pre-existing, explicitly deferred — see Missed issues section)
- AST-rendered `MegaDetectorV6.__doc__` → summary line says `2.3M to 58.1M parameters`, bullet list shows the same 5 variants — no intra-docstring contradiction
- `grep -n "#model-variants" README.md` → 1 inbound at L340; anchor target H3 `### Model Variants` at L62 — link resolves cleanly

No expected failures, no regressions, all categories clean.

## Coverage analysis

- Ledger files: 11
- Verified this round: 11
- Cumulative covered (`scope_check.sh`): 11/11
- Uncovered: []
- `action="fixed"` this round: 2 (ITEM-AUD-301 README, ITEM-AUD-302 detector.py — both in commit `a41abfed`)
- NEW issues this round: 0

`ITEMS_THIS_ROUND = FIXED + NEW = 2 + 0 = 2`. Per the strict editing-mode rule ("ANY fixed entry this round → NEEDS-MORE"), the 2 applied fixes alone drive NEEDS-MORE. Round 3 introduced no genuinely-new issues; the `NEW=2` in the STATUS line reflects the 2 applied fixes that require a verification round, not 2 newly-discovered problems.

## Next-round priorities (if NEEDS-MORE)

NEW_FINDINGS=0. The only thing keeping round 3 from CONVERGED is the strict editing-mode rule that any `fixed` entry mandates a follow-up verification round. Round 4 expected to converge cleanly:

1. **Reviewer** — owned files unchanged since round 1 `badc1c2`, round-2-verified clean, round-3 did not touch them. Expected: `NOTHING-TO-DO`.
2. **Auditor** — both runtime-crash cascade (round 2) and doc-vs-doc factual cascade (round 3) now closed. The auditor's report explicitly states "Round 4 expected to be a no-op verification round." The two remaining deferred items (`README.md:5` umbrella tagline, `docs/training_guide.md:125` weights doc-lag) are non-blocking, pre-existing, and explicitly waived in rounds 1–3 reports. Expected: `NOTHING-TO-DO`.
3. **Inquisitor** — re-verify all 11 ledger files against round-3 HEAD (`a41abfed`), confirm no new `fixed` entries, declare `CONVERGED`.

STATUS: NEEDS-MORE SCOPE_CHECK=PASS COVERED=11/11 UNCOVERED=[] NEW=2
