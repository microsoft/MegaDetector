# MegaDetector Audit Report — round 1

_Date: round 1 of the audit-fix protocol. Auditor scope: documentation /
clarity / package metadata. Reviewer scope (behavioral fixes) is summarized
here and lives in `docs/review/audit-fix/round_01/reviewer_report.md`._


## Executive Summary

**Can a user run inference today?** **Yes** — the Quick Start path
(`pip install PytorchWildlife` → three lines of Python) works end-to-end and
is verified against the installed `pytorchwildlife==1.2.4.2` and
`ultralytics>=8.0.0`. This audit did not touch the inference happy path.

**Can a user run fine-tuning today?** **Not without the reviewer's fixes
landing in the same round.** The `megadetector train|validate|inference` CLI
subcommands ship with at least three blocking bugs that fire on first run from
the shipped example config (details in "Findings: Runtime Bugs" below). Once
those are fixed, fine-tuning is runnable via the documentation now added to
the README and `docs/training_guide.md`.

**Top 3 blockers (all reviewer-owned, fixed in this same round):**
1. `examples/config_training.yaml:25` defines `plot:` (singular) but
   `src/megadetector_ai/training.py:89` reads `cfg.plots` (plural) — so
   `megadetector validate` raises `AttributeError` on first call. (ITEM-REV-001)
2. `examples/config_training.yaml:21` reads `weights: None`, which PyYAML
   parses as the **string** `"None"`, not Python `None`. With `resume: True`
   that becomes `YOLO("None")` and a confusing path-not-found error.
   (ITEM-REV-003)
3. `src/megadetector_ai/training.py:_prepare_data_config` rewrites the user's
   data YAML in place when `path:` is relative — silent, destructive mutation
   of source-controlled config. (ITEM-REV-002)

**What changed in this audit (auditor scope):**
- README gains a Quick-Start bridge sentence, an "Install from source"
  subsection, and a top-level "Fine-Tuning" section that points at the
  training guide.
- `docs/training_guide.md` no longer references a non-existent
  `requirements.txt`, points at `examples/config_training.yaml` by name, and
  links back to the README.
- `pyproject.toml` URLs renamed from the legacy `microsoft/CameraTraps` to
  `microsoft/MegaDetector` (matching the existing `Homepage` and `Repository`
  entries).
- `environment.yaml` env name renamed `PW_Finetuning_Detection` →
  `megadetector-finetuning`, with header comments documenting Linux-only
  pinning.
- `megadetector.md` now declares itself the umbrella-aggregator syndication
  target and points to `README.md` as canonical.
- `src/megadetector_ai/detector.py` V5 docstring now enumerates the three
  V5 classes (animal/person/vehicle). The V6 docstring was NOT changed — see
  "Rejected items" below.


## Repo Layout

| Path | Purpose |
| --- | --- |
| `README.md` | **Canonical** project documentation: Quick Start, installation, model variants, fine-tuning entry point. |
| `megadetector.md` | Syndication target for the `microsoft/Biodiversity` umbrella aggregator. ~70 % overlap with README; explicit pointer added in this round to mark canonical source. |
| `pyproject.toml` | Package metadata for the `megadetector-ai` Python package. Declares the `megadetector` CLI entry point (`megadetector_ai.cli:main`) and the full runtime dependency set. |
| `environment.yaml` | Conda env spec for fine-tuning. Heavily pinned to Linux x86_64 conda-forge builds; macOS/Windows users should `pip install -e .` instead (documented in this round). |
| `docs/training_guide.md` | Long-form fine-tuning reference: data layout, config schema, CLI examples, Python API. Linked from README in this round. |
| `docs/audit_report.md` | This file. |
| `examples/config_training.yaml` | Reference fine-tuning configuration. Reviewer-owned. |
| `src/megadetector_ai/__init__.py` | Package surface: re-exports `MegaDetectorV6` and `MegaDetectorV5`. |
| `src/megadetector_ai/detector.py` | Thin subclass wrappers around `PytorchWildlife.models.detection.MegaDetectorV{5,6}`. |
| `src/megadetector_ai/training.py` | Fine-tuning entry points (`train`, `validate`, `inference`). Reviewer-owned. |
| `src/megadetector_ai/training_utils.py` | Weight download + path resolution. Reviewer-owned. |
| `src/megadetector_ai/cli.py` | argparse-based `megadetector` shell command. Reviewer-owned. |
| `docs/review/` | Audit-fix protocol artifacts (ledger, coverage log, per-round plans/reports). Process metadata, not user-facing. |

**Canonical-vs-syndicated note:** the two top-level Markdown files
(`README.md` and `megadetector.md`) overlap by roughly 70 %. From this round
forward, **`README.md` is the canonical source**; `megadetector.md` carries
an explicit note declaring itself the aggregator syndication target so future
edits land in the right place and search-engine crawlers can identify the
primary copy.


## Findings: Documentation & Clarity (auditor scope)

All items in this section were applied in this round unless explicitly marked
"deferred" or "rejected". Cross-reference to per-item anchors lives in
`docs/review/audit-fix/round_01/auditor_report.md`.

| ID | File:Line | Issue | Resolution |
| --- | --- | --- | --- |
| AUD-001 | `docs/training_guide.md:11-15` | `pip install -r requirements.txt` instruction — but no `requirements.txt` exists in the repo. | **Applied.** Subsection rewritten to use `pip install -e .` from the repo root; `pyproject.toml` covers all runtime deps. |
| AUD-002 | `pyproject.toml:50` | `Documentation` URL points at the legacy `microsoft.github.io/CameraTraps/`. | **Applied.** Now `microsoft.github.io/MegaDetector/`, matching `Homepage`. |
| AUD-003 | `pyproject.toml:52` | `Source Code` URL points at `microsoft/CameraTraps`. | **Applied.** Now `microsoft/MegaDetector`. |
| AUD-004 | `pyproject.toml:53` | `Bug Tracker` URL points at `microsoft/CameraTraps/issues`. | **Applied.** Now `microsoft/MegaDetector/issues`, matching the README's `Contributing` section. |
| AUD-005 | `README.md` (new section) | No fine-tuning content; `docs/training_guide.md` was orphaned from the README. | **Applied.** New `## Fine-Tuning` section inserted between `## Performance` and `## Version History`; covers when-to-fine-tune, quick path, supported variants, and a link to the full guide. |
| AUD-006 | `README.md` (Installation) | `pip install PytorchWildlife` is the only install path documented, despite `pyproject.toml` declaring a `megadetector` CLI entry point. | **Applied.** New `### Install from source (for fine-tuning or CLI use)` subsection documents `git clone` + `pip install -e .`. |
| AUD-007 | `README.md:34` | Quick Start uses the high-level `PytorchWildlife` API; no bridge to the local CLI or fine-tuning sections. | **Applied.** Single bridge sentence added after "That's it." pointing to `#install-from-source-for-fine-tuning-or-cli-use` and `#fine-tuning`. |
| AUD-008 | `environment.yaml:1` | Env name `PW_Finetuning_Detection` is a holdover from the legacy "PyTorch Wildlife Fine-tuning Detection" repo. | **Applied.** Renamed to `megadetector-finetuning`. |
| AUD-009 | `environment.yaml` (top) | Conda block is Linux x86_64–pinned; macOS/Windows users hit cryptic solver errors with no recovery guidance. | **Applied.** Header comments added documenting the platform constraint and pointing macOS/Windows users at `pip install -e .`. |
| AUD-010 | `docs/training_guide.md:23` | Cascade: `conda activate PW_Finetuning_Detection` had to follow the rename in AUD-008. | **Applied.** Updated to `conda activate megadetector-finetuning`. |
| AUD-011 | `docs/training_guide.md:86-89` | Doc referred only to `config.yaml`, not the shipped reference `examples/config_training.yaml`. | **Applied.** Configuration section now opens with a `cp examples/config_training.yaml ./config.yaml` snippet. |
| AUD-012 | `docs/training_guide.md:1` | No navigation back to the main README from the training guide. | **Applied.** One-line back-link added under the H1. |
| AUD-013 | `src/megadetector_ai/__init__.py:5-6` | Proposed change to claim "V6 focuses on animals only". | **REJECTED.** Installed PyTorch Wildlife 1.2.4.2 ships `MegaDetectorV6.CLASS_NAMES = {0: animal, 1: person, 2: vehicle}` and its docstring reads "designed for detecting animals, persons, and vehicles." The README's "Animal Recall" metric column does NOT imply a class-set restriction. Current text matches installed PW; left alone. |
| AUD-014 | `src/megadetector_ai/detector.py:12-15` | Proposed parallel "V6 is animal-only" rewrite on the MegaDetectorV6 docstring. | **REJECTED.** Same reason as AUD-013. |
| AUD-015 | `src/megadetector_ai/detector.py:42-58` | MegaDetectorV5 docstring did not enumerate its three-class output. | **Applied.** Inserted "MegaDetectorV5 detects three classes: animals (class 0), people (class 1), and vehicles (class 2)." Unaffected by AUD-013/014 because the V5 class set is uncontroversial. |
| AUD-016 | `megadetector.md:1` | `megadetector.md` and `README.md` overlap ~70 % with no canonical pointer. | **Applied.** HTML comment + visible `> [!NOTE]` declaring `megadetector.md` the umbrella syndication target and `README.md` canonical. |
| AUD-017 | `README.md:185`, `megadetector.md:49` | Display text `[/SPARROW-Studio]` (leading slash) in the Biodiversity Ecosystem table. | **Applied.** Fixed in both files. URL was already correct. |
| AUD-018 | `docs/audit_report.md` | User-facing audit deliverable did not exist. | **Applied.** This file. |


## Findings: Runtime Bugs (reviewer scope — summarized from reviewer plan)

Source of truth for these items: `docs/review/audit-fix/round_01/reviewer_report.md`.
Listed here for the user-facing report so the maintainer sees the full
picture of round-1 changes in one place.

| ID | File:Line | Issue | Reviewer fix |
| --- | --- | --- | --- |
| REV-001 | `examples/config_training.yaml:25` ↔ `src/megadetector_ai/training.py:89` | YAML key `plot:` (singular) vs code reference `cfg.plots` (plural); ultralytics canonical kwarg is `plots`. `megadetector validate` raises `AttributeError` on first call. | Rename YAML key `plot` → `plots`. |
| REV-002 | `src/megadetector_ai/training.py:39-49` | `_prepare_data_config` silently rewrites the user's data YAML in place when `path:` is relative — loses comments, formatting, ordering. | Resolve `path:` relative to the YAML's own directory in-memory; write a sidecar resolved YAML under `runs/_resolved_data/` and re-point `cfg.data` (in-process only). Callers updated to use the return value. |
| REV-003 | `src/megadetector_ai/training.py:22-27` and `examples/config_training.yaml:21` | PyYAML parses unquoted `weights: None` as the string `"None"` — `YOLO("None")` fails with a confusing path-not-found. | Two-part fix: guard in `_load_model` raises `ValueError` when `resume=True` and `weights` is missing/`None`/`"None"`/`""`; YAML default changed to `null` (the YAML 1.1 null token). |
| REV-004 | `src/megadetector_ai/cli.py:7` (module docstring) | Example uses `--model MDV6-apa-rtdetr-e`, which raises `ValueError` against installed PW 1.2.4.2 (accepted set is exactly the 5 variants listed in the new README Fine-Tuning section). | Docstring example changed to a supported variant (`MDV6-yolov10-e`). |
| REV-005 | `src/megadetector_ai/cli.py:34-35` (`detect` subcommand) | Bogus `--model` values produce a deep PW traceback instead of a clean argparse error. | Added `SUPPORTED_DETECT_VERSIONS` constant, argparse `choices=`, and a pre-import sanity check that exits with code 2 and a one-line error. |
| REV-006 | `src/megadetector_ai/training.py:60-73` | `cfg.optimizer` and `cfg.lr0` are documented and present in the example config but never forwarded to `model.train(...)` — silently ignored. | Both forwarded as kwargs. |
| REV-007 | `src/megadetector_ai/training_utils.py:5-31` and `src/megadetector_ai/cli.py` | `cfg.model` (`YOLO` / `RTDETR`) and `cfg.model_name` are coupled but not cross-validated; a mismatch produces a confusing late ultralytics error. | Pre-emptive `ValueError` raised in `_load_model` for `YOLO`+`rtdetr-*` or `RTDETR`+`yolov*` combinations. |
| REV-008 | `src/megadetector_ai/cli.py:105-147` | `cli.train`/`validate`/`inference` let any exception bubble up as a Python traceback. | Wrap in `try / except (ValueError, KeyError, AttributeError, FileNotFoundError)` — friendly error for config typos, raw traceback preserved for genuine bugs. |
| REV-009 | `src/megadetector_ai/training.py:99-114` (`inference`) | A single corrupt frame can abort the whole inference run. | Per-image try/except in the save loop; continue and log on failure. |
| REV-010 | `src/megadetector_ai/training_utils.py:25-29` | `wget.download` creates its scratch file in CWD via `tempfile.mkstemp(..., dir=".")` regardless of `out=` — silently fails in a read-only working directory. | `os.makedirs(...)` + `os.access(".", os.W_OK)` precheck with a clear error message. (Full atomic-rename / checksum hardening deferred to round 2.) |


### Cross-cutting clarification — V6 class set

The auditor's initial plan (B7 / AUD-013 / AUD-014) suggested that V6 is
"animal-only", motivated by the README's emphasis on animal detection.
**That framing is wrong.** Verified against installed `pytorchwildlife==1.2.4.2`:

- `MegaDetectorV6.CLASS_NAMES = {0: "animal", 1: "person", 2: "vehicle"}` —
  identical to V5.
- The upstream V6 docstring reads "specifically designed for detecting
  animals, persons, and vehicles."
- The README's "Animal Recall" column reports a single metric per variant
  (animal-class recall), **not** a class-set restriction.

Consequences:
- `src/megadetector_ai/cli.py:83` `CLASS_NAMES = {0: "animal", 1: "person", 2: "vehicle"}`
  is **correct** and should not be "fixed" to `{0: "animal"}`.
- The V6 docstring in `detector.py` is **left as-is**.
- A separate, narrower cleanup item (trim the 9-variant docstring list to the
  5 variants the installed PW actually exposes) is **deferred to round 2**.


## README — Suggested Fine-Tuning Section (paste-ready)

This is the exact Markdown fragment now present in `README.md` between
`## Performance` and `## Version History` (applied as part of AUD-005 in this
round). Reproduced here so the maintainer can review it in isolation and
confirm wording.

```markdown
## Fine-Tuning

MegaDetector V6 ships with a fine-tuning pipeline (built on the
[ultralytics](https://github.com/ultralytics/ultralytics) framework) so you can
adapt a V6 model to your own camera-trap dataset. Fine-tuning is useful when
the off-the-shelf V6 models miss animals that look different from the training
distribution — for example, an under-represented species, a specific
environment (forest canopy, snow, night-vision IR), or a new sensor.

**Quick path:**

```bash
# 1. Clone and install in editable mode (from a fresh venv or conda env).
git clone https://github.com/microsoft/MegaDetector
cd MegaDetector
pip install -e .

# 2. Copy the reference config and edit `data:` to point at your dataset YAML.
cp examples/config_training.yaml ./config.yaml

# 3. Train, validate, and run inference with the same CLI.
megadetector train    --config ./config.yaml
megadetector validate --config ./config.yaml
megadetector inference --config ./config.yaml
```

**Supported fine-tuning model variants:**

- `MDV6-yolov9-c` — compact YOLOv9
- `MDV6-yolov9-e` — extra-large YOLOv9
- `MDV6-yolov10-c` — compact YOLOv10 (2.3M params)
- `MDV6-yolov10-e` — extra-large YOLOv10
- `MDV6-rtdetr-c` — compact RT-DETR

Training outputs (weights, plots, metrics) land under `./runs/` keyed by the
`exp_name` field in your config. Fine-tuned `.pt` weights can be loaded back
into `MegaDetectorV6(weights="path/to/best.pt")` for inference.

**Full reference:** [docs/training_guide.md](docs/training_guide.md) covers
data layout, the full config schema, conda environment setup, and the Python
API equivalents of each CLI subcommand.
```


## Recommended Next Steps

1. **Land the reviewer's round-1 commit alongside this one.** None of the
   fine-tuning documentation added in this round is runnable without
   REV-001 / REV-002 / REV-003 in place. The audit-fix protocol intentionally
   sequences them in the same round.
2. **Plan a round 2 with the deferred items.** Specifically:
   - Trim the README "Model Variants" table (currently 9 rows) and the
     `detector.py` V6 docstring (currently 9 bullets) to the 5 variants the
     installed `pytorchwildlife==1.2.4.2` actually exposes — or document that
     `apa-*` / `mit-*` variants require a newer PW release and pin a version
     range in `pyproject.toml`. (Reviewer's CS-2 and CS-4.)
   - Cascade `plot:` → `plots:` rename into `docs/training_guide.md:117`
     (Reviewer's CS-1).
   - Honor `cfg.device_val` / a new `cfg.device_inference` in
     `training.py:inference()` (Auditor B3, reviewer round 2).
   - Add atomic-rename and checksum verification to the weight downloader
     (Auditor B6, full hardening on top of REV-010).
   - Decide the fate of the unused `task:` field in `config_training.yaml`
     (Reviewer's CS-5).
   - Add a sentence in `docs/training_guide.md` explaining the divergence
     between fine-tuning weights (Zenodo 14567879, filename pattern
     `MDV6b-yolov9c.pt`) and PW inference weights (Zenodo 15398270,
     `MDV6-yolov9-c.pt`). (Reviewer's CS-6.)
3. **Stand up a minimal test suite.** The repo currently ships no automated
   tests. Three high-value additions:
   - A YAML-parse smoke test for `examples/config_training.yaml` that asserts
     every `cfg.<field>` reference in `training.py` resolves.
   - A `--help` smoke test for each `megadetector` subcommand.
   - An offline `_prepare_data_config` test that confirms the user's input
     YAML is never mutated on disk.
4. **Pin `pytorchwildlife` to a version range in `pyproject.toml`.** The
   current unpinned dependency (`PytorchWildlife`) means a future PW release
   that changes the accepted `version=` set will silently break the CLI's
   `SUPPORTED_DETECT_VERSIONS` whitelist.


## Appendix: Files Reviewed

All 11 ledger files plus the new `docs/audit_report.md` (created by this
round). "Status" = round-1 outcome.

| Ledger file | Owner | Round-1 status |
| --- | --- | --- |
| `README.md` | auditor | **Modified** — AUD-005 Fine-Tuning section, AUD-006 Install-from-source, AUD-007 Quick Start bridge, AUD-017 SPARROW typo. |
| `megadetector.md` | auditor | **Modified** — AUD-016 canonical-source note, AUD-017 SPARROW typo. |
| `pyproject.toml` | auditor | **Modified** — AUD-002/003/004 CameraTraps→MegaDetector URLs. |
| `environment.yaml` | auditor | **Modified** — AUD-008 env rename, AUD-009 platform-constraint header. |
| `docs/training_guide.md` | auditor | **Modified** — AUD-001 editable install, AUD-010 env cascade, AUD-011 config_training.yaml, AUD-012 back-link. |
| `src/megadetector_ai/__init__.py` | auditor | **Unchanged** — AUD-013 rejected (V6 animal-only claim contradicts installed PW). |
| `src/megadetector_ai/detector.py` | auditor | **Modified** — AUD-015 V5 class enumeration. AUD-014 rejected (V6 animal-only claim contradicts installed PW). |
| `src/megadetector_ai/training.py` | reviewer | **Modified** — REV-001..003, REV-006, REV-007, REV-009. |
| `src/megadetector_ai/training_utils.py` | reviewer | **Modified** — REV-010. |
| `src/megadetector_ai/cli.py` | reviewer | **Modified** — REV-004, REV-005, REV-008. |
| `examples/config_training.yaml` | reviewer | **Modified** — REV-001 `plot`→`plots`, REV-003 `weights: null`. |
| `docs/audit_report.md` | auditor | **Created** — AUD-018 (this file). |
