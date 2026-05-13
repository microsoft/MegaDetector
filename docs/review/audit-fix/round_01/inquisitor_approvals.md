# Inquisitor approvals — round 1

Anchor evidence used below:
- Installed PyTorch Wildlife `MegaDetectorV6` and `MegaDetectorV5` at
  `~/.cache/uv/archive-v0/NmuqR_Vp-sUYaNsyKewlK/PytorchWildlife/models/detection/ultralytics_based/megadetectorv6.py:8-21,35-51`
  and `.../megadetectorv5.py:10-27` — both classes declare
  `CLASS_NAMES = {0: "animal", 1: "person", 2: "vehicle"}` and both docstrings say "specifically designed for detecting animals, persons, and vehicles."
- Ultralytics `model.val(**kwargs)` reads kwarg `plots` (verified
  `~/.cache/uv/archive-v0/isBvHKRoo5RhL5MnGwDul/ultralytics/cfg/default.yaml:58 → plots: True # (bool) save plots and images during train/val`).
- pyproject.toml deps (PytorchWildlife, ultralytics>=8.0.0, munch>=2.0.0, wget>=3.0, PyYAML>=6.0, torch>=2.0.0) cover every import in `training.py`, `training_utils.py`, `cli.py`, `detector.py`.

---

## Auditor verdicts

ITEM-AUD-001 | APPROVED — `requirements.txt` does not exist in the repo (verified `ls` of repo root). `pyproject.toml:39-46` lists PytorchWildlife / ultralytics>=8.0.0 / munch>=2.0.0 / wget>=3.0 / PyYAML>=6.0 / torch>=2.0.0, which covers every import in `training.py` (`ultralytics`, `munch`, `yaml`), `training_utils.py` (`wget`, `torch`), `cli.py` (`torch`, `megadetector_ai`), and `detector.py` (`PytorchWildlife.models.detection`). `pip install -e .` is the correct replacement.

ITEM-AUD-002 | APPROVED — `pyproject.toml:50` reads `Documentation = "https://microsoft.github.io/CameraTraps/"`; verified the asymmetry against `Homepage` / `Repository` (lines 49, 51) which point at `microsoft/MegaDetector`, and `README.md:113` points at `microsoft.github.io/MegaDetector/`.

ITEM-AUD-003 | APPROVED — `pyproject.toml:52` reads `"Source Code" = "https://github.com/microsoft/CameraTraps"`. Same asymmetry as AUD-002.

ITEM-AUD-004 | APPROVED — `pyproject.toml:53` reads `"Bug Tracker" = "https://github.com/microsoft/CameraTraps/issues"`. `README.md:273` already directs users to `microsoft/MegaDetector/issues`; pyproject lags.

ITEM-AUD-005 | APPROVED — README.md has no Fine-Tuning section today and `docs/training_guide.md` is orphaned from the README. Verified line 218 is the last Performance line ("Every V6 variant is faster than V5…") and line 221 is `## Version History`, so the proposed insertion point is correct. The 5-variant fine-tuning list correctly matches installed PW (see AUD-006 evidence below).

ITEM-AUD-006 | APPROVED — `pyproject.toml:55-56` declares `[project.scripts] megadetector = "megadetector_ai.cli:main"` and the package is shipped at `src/megadetector_ai/`, but `README.md`'s Installation section (lines 91-114) only documents `pip install PytorchWildlife`. Source-install path is genuinely undiscoverable today.

ITEM-AUD-007 | APPROVED — Bridging the Quick Start (which uses the high-level `PytorchWildlife` API) to the new Fine-Tuning / source-install sections is the standard navigation pattern. Line 34 ("That's it. Three lines…") is the correct anchor.

ITEM-AUD-008 | APPROVED — `environment.yaml:1` literally reads `name: PW_Finetuning_Detection`, which is a holdover from the legacy PyTorch Wildlife Fine-tuning Detection repo and inconsistent with the project name `megadetector-ai` in `pyproject.toml:6`. The fix is stylistic but improves discoverability when users juggle multiple AI4G envs; not behavioral.

ITEM-AUD-009 | APPROVED — The conda block in `environment.yaml:4-26` is pinned to Linux x86_64 conda-forge builds (e.g. `_libgcc_mutex=0.1=conda_forge`, `libgcc-ng=14.1.0=h69a702a_1`) that will not solve on macOS or Windows. A documented platform constraint up front is the lowest-cost mitigation.

ITEM-AUD-010 | APPROVED — `docs/training_guide.md:23` reads `conda activate PW_Finetuning_Detection` and must cascade with AUD-008. Confirm both fixes land in the same round.

ITEM-AUD-011 | APPROVED — Verified `docs/training_guide.md:86` (`## Configuration`) onward references only `config.yaml` and does not point at the actual reference `examples/config_training.yaml`. Causes real confusion for first-time users.

ITEM-AUD-012 | APPROVED — Cheap navigation polish; aligns with the new Fine-Tuning link added in AUD-005.

ITEM-AUD-013 | REJECTED: contradicts installed upstream. The proposed text "V6 focuses on animals only" is **factually wrong** against installed PyTorch Wildlife 1.2.4.2. Verified `~/.cache/uv/archive-v0/NmuqR_Vp-sUYaNsyKewlK/PytorchWildlife/models/detection/ultralytics_based/megadetectorv6.py:8-21` — `MegaDetectorV6.CLASS_NAMES = {0: "animal", 1: "person", 2: "vehicle"}` and the upstream docstring reads "specifically designed for detecting animals, persons, and vehicles." Re-reading `README.md`: no line in the README explicitly claims V6 is animal-only — the "Animal Recall" column at line 63 is a single metric reported per variant, not a class-set restriction. The current `__init__.py:5-6` text ("animals, people, and vehicles") matches installed PW and should be **left alone**. If the auditor still wants to add nuance, propose a different, narrower wording in round 2 (e.g. "MegaDetector primarily detects animals; the legacy 3-class output (animal/person/vehicle) is inherited from V5"). Do not commit the proposed text.

ITEM-AUD-014 | REJECTED: same root reason as AUD-013. The proposed text "V6 focuses exclusively on the animal class; for people/vehicle detection use the legacy MegaDetectorV5" is contradicted by installed PW V6 having `CLASS_NAMES = {0: animal, 1: person, 2: vehicle}` identical to V5. The current docstring at `src/megadetector_ai/detector.py:12-15` ("Detects animals, people, and vehicles") is correct and matches both the upstream class definition and the upstream docstring. Leave the V6 docstring as-is.

ITEM-AUD-015 | APPROVED — Reading `src/megadetector_ai/detector.py:42-58`, the V5 docstring never enumerates the 3-class output. Adding "MegaDetectorV5 detects three classes: animals (class 0), people (class 1), and vehicles (class 2)" is consistent with installed PW V5 (`megadetectorv5.py:23-27`). This is genuinely useful at the API surface and unaffected by the AUD-013/014 rejection.

ITEM-AUD-016 | APPROVED — `megadetector.md` and `README.md` overlap heavily; explicit canonical-source pointer at the top of `megadetector.md` prevents drift and helps crawlers. The proposed two-line note is minimal and clear.

ITEM-AUD-017 | APPROVED — Verified `README.md:185` and `megadetector.md:49` both contain the cell `[/SPARROW-Studio](https://github.com/microsoft/Biodiversity/tree/main/SPARROW-Studio)`. The leading slash is a display typo; URL is fine.

ITEM-AUD-018 | APPROVED — Required user-facing deliverable. Note: when authoring `docs/audit_report.md`, the auditor should **drop** any "V6 is animal-only" framing in the Findings section (consistent with AUD-013/014 rejection) and instead state the verified ground truth: V6 inherits V5's 3-class output, the README emphasizes animal detection in metric reporting only, and `cli.py:83`'s `CLASS_NAMES = {0: animal, 1: person, 2: vehicle}` is **correct** (not a bug, contrary to the auditor's own B7 framing).

---

## Reviewer verdicts

ITEM-REV-001 | APPROVED — Verified `examples/config_training.yaml:25` reads `plot: True` and `training.py:89` reads `cfg.plots`. Ultralytics canonical kwarg is `plots` (verified `ultralytics/cfg/default.yaml:58 → plots: True # (bool) save plots and images during train/val`), so the YAML key is the wrong side; renaming `plot` → `plots` in the config is the correct fix. `megadetector validate` is broken at import-of-config time today. Cascade: the auditor's CS-1 / training_guide.md:117 still says `plot:` — defer that rename to round 2 (in auditor scope).

ITEM-REV-002 | APPROVED — Verified `_prepare_data_config` at `training.py:39-49` writes back to `cfg.data` (the user's source-controlled YAML) whenever `data["path"]` is relative. This loses comments / formatting / ordering and is a hidden side effect of train/validate/inference. The proposed sidecar-resolve pattern (resolve relative to the YAML's directory, not CWD) matches the mental model in `docs/training_guide.md:52-64`. One implementation note for the editor: when wiring the return value into `train()` / `validate()` / `inference()`, replace `data=cfg.data` at lines 61 and 87 with `data=data_path` and add the same wiring to `inference()` line 107 (which currently doesn't even use `cfg.data` — the reviewer's draft already covers this).

ITEM-REV-003 | APPROVED — Verified `yaml.load(open('examples/config_training.yaml'), Loader=yaml.FullLoader)['weights']` parses unquoted `None` as the Python string `'None'` (PyYAML 1.1 spec; the YAML 1.1 null sentinel is `null`/`~`/empty). `training.py:22-27` then assigns `model_path = "None"` and `YOLO("None")` raises a confusing file-not-found. Both fixes (guard in `_load_model` + change YAML default to `null`) should land together — the YAML-only fix masks the underlying code bug if `cfg.weights` is missing entirely.

ITEM-REV-004 | APPROVED — Verified the installed `MegaDetectorV6.__init__` at `megadetectorv6.py:35-51` accepts exactly `{MDV6-yolov9-c, MDV6-yolov9-e, MDV6-yolov10-c, MDV6-yolov10-e, MDV6-rtdetr-c}`; `MDV6-apa-rtdetr-e` is **not** in the accepted set despite being advertised in `README.md:65` Model Variants. The docstring example at `cli.py:7` ships a value that will raise `ValueError` on first run. Replacement value `MDV6-yolov10-e` is in the accepted set.

ITEM-REV-005 | APPROVED — Logical complement to REV-004. argparse-level `choices=` is the right surface to reject unknown values before any torch / PW imports, and the proposed `SUPPORTED_DETECT_VERSIONS` set matches the installed PW reality. Cross-link: this also implicitly addresses the cosmetic mismatch between `cli.py:169` default (`MDV6-yolov9-c`, valid) and the docstring example (invalid).

ITEM-REV-006 | APPROVED — Verified `examples/config_training.yaml:15-16` define `optimizer: auto` and `lr0: 0.01`; `docs/training_guide.md:106-107` documents them as user-tunable; `training.py:60-73` does not forward either. ultralytics `Model.train(**kwargs)` accepts both. Silently-ignored user config is a real correctness issue, not polish.

ITEM-REV-007 | APPROVED — The `cfg.model` ∈ {YOLO, RTDETR} flag and the `cfg.model_name` set in `training_utils.get_model_path` are coupled but not validated. Pre-emptive consistency check is cheap and avoids a long ultralytics traceback. Minor implementation note: the check should run **after** `model_name` validation (so the user gets the version-list error first if they passed a bogus model_name) — the reviewer's draft already places it after `model_path = get_model_path(...)`, so this is fine.

ITEM-REV-008 | APPROVED — Catching `(ValueError, KeyError, AttributeError, FileNotFoundError)` and falling through on `Exception` preserves debuggability for genuine bugs while giving non-developer users a one-line error for config typos. The set is well-chosen (covers Munch `AttributeError`, missing YAML keys, bad paths, ultralytics version validation).

ITEM-REV-009 | APPROVED — Inference robustness: a per-iteration try/except in the save loop at `training.py:111-112` is a small, defensive change with no downside. Lower priority than 001-008 but worth landing in the same round.

ITEM-REV-010 | APPROVED — Verified the `wget==3.2` source at `wget.py` (per reviewer): `tempfile.mkstemp(..., dir=".")` writes its scratch file into CWD regardless of `out=`. The proposed precheck (`os.makedirs(...)` + `os.access(".", os.W_OK)` with a clear error) is small, defensive, and explicitly scoped to clearer-error rather than a full rewrite of the download flow. Approved as-is.

---

## Notes

### Cross-cutting observation 1 — V6 class set (cross-check (a))
The reviewer's cross-scope **B7** (auditor plan, line 75) and **CS-2** (reviewer plan, line 209) both correctly note the inconsistency between the README's "V6" emphasis and `cli.py:83`'s 3-class `CLASS_NAMES`. Ground truth verified from installed PyTorch Wildlife 1.2.4.2: V6 (and V5) both ship `CLASS_NAMES = {0: animal, 1: person, 2: vehicle}` and both upstream docstrings say "designed for detecting animals, persons, and vehicles." Conclusion:
- `cli.py:83`'s mapping is **correct** — leave it alone (this rejects the implicit "fix to `{0: animal}`" alternative buried in auditor B7).
- The auditor's ITEM-AUD-013/014 (rewriting docstrings to "V6 is animal-only") are **rejected**; the current docstrings match installed PW.
- The reviewer's CS-2 (about the 9 variants advertised vs 5 supported in installed PW) is a legitimate auditor item for **round 2**: either trim the README Model Variants table to the 5 installed variants, or add a note that `apa-*`/`mit-*` variants require a newer PW release and pin a version range in `pyproject.toml`.
- The reviewer's CS-4 (detector.py V6 docstring lists 9 variants, only 5 are supported) is also a legitimate **round 2** auditor item — but **only** the variant list needs trimming; the class-set wording must stay "animals, people, and vehicles."

### Cross-cutting observation 2 — deferrals to round 2
Cross-scope items each editor flagged for the other are correctly listed and out of round-1 scope. Specifically:
- Auditor's B1 (`cfg.plots` vs `plot:`) → addressed by reviewer ITEM-REV-001 this round ✓
- Auditor's B2 (`weights: None`) → addressed by reviewer ITEM-REV-003 this round ✓
- Auditor's B3 (`inference()` ignores `cfg.device_*`) → DEFER to round 2 — out of scope for the proposing editor (auditor), not addressed by reviewer this round either; reviewer should pick this up in round 2.
- Auditor's B4 (`_prepare_data_config` mutates the user file) → addressed by reviewer ITEM-REV-002 this round ✓
- Auditor's B5 (`_prepare_data_config` return value discarded) → addressed implicitly by reviewer ITEM-REV-002 (the rewritten function returns a path that the callers now use) ✓
- Auditor's B6 (`wget.download` no retry/checksum) → partially addressed by reviewer ITEM-REV-010; full atomic-rename + checksum is a round-2 hardening item.
- Auditor's B7 (`cli.py:83` CLASS_NAMES vs README narrative) → resolved by this inquisitor's cross-check (a): `cli.py:83` is correct, no fix needed; auditor docstring rewrites rejected.
- Auditor's B8 (`MDV6-yolov10-c` → `MDV6-yolov10n.pt` filename clarification) → DEFER to round 2 — out of scope for the proposing editor; reviewer's CS-6 raises a related point about Zenodo records.
- Reviewer's CS-1 (training_guide.md plot→plots cascade) → DEFER to round 2 — auditor scope, not in round-1 auditor plan; should be added in round 2 as a cascade from REV-001.
- Reviewer's CS-2 (README 9 variants vs 5 supported by installed PW) → DEFER to round 2 — auditor scope.
- Reviewer's CS-3 (training_guide.md requirements.txt) → addressed by auditor ITEM-AUD-001 this round ✓
- Reviewer's CS-4 (detector.py V6 docstring lists 9 variants) → DEFER to round 2 — auditor scope; trim variant list only, leave class-set wording alone.
- Reviewer's CS-5 (`task:` field in YAML unused) → DEFER to round 2 — reviewer scope (config_training.yaml is reviewer-owned), but only flagged not planned.
- Reviewer's CS-6 (Zenodo record divergence) → DEFER to round 2 — auditor scope (docs explanation).

### Cross-cutting observation 3 — naming sanity
The auditor renames the conda env `PW_Finetuning_Detection` → `megadetector-finetuning` (AUD-008) and cascades to `docs/training_guide.md` (AUD-010). I note for the editor that there is **no third site** referencing the old env name — verified `grep -rn "PW_Finetuning_Detection"` in the repo returns only `environment.yaml:1` and `docs/training_guide.md:23`. Two-site rename is complete.

### Cross-cutting observation 4 — round-1 scope completeness
The SCOPE_LEDGER lists 11 files; the auditor and reviewer plans together cover all 11. `docs/audit_report.md` is correctly tracked as a NEW FILE created by the auditor (file_ownership.md:13). The COVERAGE_LOG.jsonl already records audited items per file. No ledger-narrowing concerns this round.

STATUS: APPROVALS-DONE
