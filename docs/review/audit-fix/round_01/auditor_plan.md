# Auditor plan — round 1

Scope: structural changes only (docs clarity, README content gaps, broken
instructions, URL consistency, naming, dead code, package metadata, doc
alignment for the V5/V6 animal-vs-people-vehicles question). Behavioral
runtime bugs are noted under "Cross-Scope Findings" for the reviewer.

## Items

<a name="ITEM-AUD-001"></a>
ITEM-AUD-001 | docs/training_guide.md:11-15 | Remove the `### Using pip and \`requirements.txt\`` subsection (which says `pip install -r requirements.txt`) and replace it with an editable-install instruction sourced from `pyproject.toml`: `pip install -e .` (run from the repo root). Keep the conda alternative immediately below. | No `requirements.txt` exists anywhere in the repo — the instruction is broken on first run. `pyproject.toml` already lists the full dependency set, so editable install is the correct path.

<a name="ITEM-AUD-002"></a>
ITEM-AUD-002 | pyproject.toml:50 | Change `Documentation = "https://microsoft.github.io/CameraTraps/"` to `Documentation = "https://microsoft.github.io/MegaDetector/"`. | URL inconsistency: `Homepage` and `Repository` already point at `microsoft/MegaDetector`; `README.md:113` also points at the MegaDetector docs site. CameraTraps is the legacy archive name.

<a name="ITEM-AUD-003"></a>
ITEM-AUD-003 | pyproject.toml:52 | Change `"Source Code" = "https://github.com/microsoft/CameraTraps"` to `"https://github.com/microsoft/MegaDetector"`. | Same URL inconsistency as ITEM-AUD-002.

<a name="ITEM-AUD-004"></a>
ITEM-AUD-004 | pyproject.toml:53 | Change `"Bug Tracker" = "https://github.com/microsoft/CameraTraps/issues"` to `"https://github.com/microsoft/MegaDetector/issues"`. | Same URL inconsistency; `README.md:273` already points users at `microsoft/MegaDetector/issues`.

<a name="ITEM-AUD-005"></a>
ITEM-AUD-005 | README.md (new section, inserted between current "Performance" (ends ~line 218) and "Version History" (~line 221)) | Add a top-level `## Fine-Tuning` section. Contents: one-paragraph framing of when to fine-tune; a "Quick path" code block with (a) `git clone` + `pip install -e .`, (b) "copy `examples/config_training.yaml` to `config.yaml` and edit `data:` to point at your dataset", (c) the three CLI subcommands `megadetector train|validate|inference --config ./config.yaml`; a callout listing the 5 supported fine-tuning models (MDV6-yolov9-c/-e, MDV6-yolov10-c/-e, MDV6-rtdetr-c); a "Full guide" link to `docs/training_guide.md`. | README currently has zero fine-tuning content; `docs/training_guide.md` is orphaned. User cannot discover fine-tuning from the README.

<a name="ITEM-AUD-006"></a>
ITEM-AUD-006 | README.md:91-114 (Installation) | Add a subsection "Install from source (for fine-tuning or CLI use)" with: `git clone https://github.com/microsoft/MegaDetector && cd MegaDetector && pip install -e .`. Mention that this also exposes the `megadetector` shell command. | The repo declares `[project.scripts] megadetector = "megadetector_ai.cli:main"` and ships a `megadetector_ai` package, but the README documents neither. Users have no way to discover them today.

<a name="ITEM-AUD-007"></a>
ITEM-AUD-007 | README.md:34 (immediately after the "That's it." line of Quick Start) | Add one sentence: "Need the local `megadetector` CLI or fine-tuning? See [Install from source](#install-from-source-for-fine-tuning-or-cli-use) and [Fine-Tuning](#fine-tuning) below." | Bridges the Quick Start (which uses the high-level `PytorchWildlife` API) to the local CLI and the new Fine-Tuning section. Removes confusion about which package does what.

<a name="ITEM-AUD-008"></a>
ITEM-AUD-008 | environment.yaml:1 | Rename `name: PW_Finetuning_Detection` to `name: megadetector-finetuning`. | The env name is a holdover from the legacy "PyTorch Wildlife Fine-tuning Detection" repo; project is now `megadetector-ai`. Consistent naming reduces friction when users have multiple related envs.

<a name="ITEM-AUD-009"></a>
ITEM-AUD-009 | environment.yaml (top of file, before `name:`) | Add header comments documenting that (a) the conda block is heavily pinned to Linux x86_64 conda-forge builds and will not solve on macOS or Windows, (b) macOS/Windows users should prefer `pip install -e .` from a fresh venv, (c) only the `pip:` subtree is platform-portable. | Currently a macOS/Windows user hits a cryptic conda solver error with no recovery guidance. Documenting the platform constraint up front is the lowest-cost fix.

<a name="ITEM-AUD-010"></a>
ITEM-AUD-010 | docs/training_guide.md:23 | Update `conda activate PW_Finetuning_Detection` to `conda activate megadetector-finetuning` (cascade from ITEM-AUD-008). | Keeps the doc in sync with the renamed conda env.

<a name="ITEM-AUD-011"></a>
ITEM-AUD-011 | docs/training_guide.md:86-89 (start of "Configuration" section) | Clarify that the shipped reference config is `examples/config_training.yaml` (not `config.yaml`). Recommended phrasing: "Copy `examples/config_training.yaml` to a working location and edit it. The CLI accepts any path via `--config`; the examples below assume you saved it as `./config.yaml`." | The doc currently refers only to `config.yaml`, leaving readers unsure where the example lives or whether the filename matters.

<a name="ITEM-AUD-012"></a>
ITEM-AUD-012 | docs/training_guide.md:1 (immediately after the H1) | Add a one-line link back to the main README: "← Back to [main README](../README.md)." | Bidirectional navigation; today the training guide is reachable only from the README (once ITEM-AUD-005 lands) and has no return path.

<a name="ITEM-AUD-013"></a>
ITEM-AUD-013 | src/megadetector_ai/__init__.py:5-6 | Change the package docstring sentence "MegaDetector detects animals, people, and vehicles in camera trap images." to "MegaDetector detects animals in camera trap images. The legacy V5 model also returns people and vehicles; V6 focuses on animals only — see the README for details." | Aligns the import-time docstring with the README's single source of truth (V6 is animal-only; V3 added human, V4 added vehicle, V6 removes them).

<a name="ITEM-AUD-014"></a>
ITEM-AUD-014 | src/megadetector_ai/detector.py:12-15 | Change the MegaDetectorV6 class docstring opening from "Detects animals, people, and vehicles in camera trap images using modern architectures (YOLOv9, YOLOv10, RT-DETR)." to "Detects animals in camera trap images using modern architectures (YOLOv9, YOLOv10, RT-DETR). V6 focuses exclusively on the animal class; for people/vehicle detection use the legacy MegaDetectorV5." | Same V5/V6 alignment as ITEM-AUD-013, applied to the user-facing class docstring.

<a name="ITEM-AUD-015"></a>
ITEM-AUD-015 | src/megadetector_ai/detector.py:42-58 | Augment the MegaDetectorV5 class docstring to state explicitly what V5 detects: insert at the start of the long-description: "MegaDetectorV5 detects three classes: animals (class 0), people (class 1), and vehicles (class 2)." | Makes the V5-vs-V6 class-coverage difference legible at the API surface.

<a name="ITEM-AUD-016"></a>
ITEM-AUD-016 | megadetector.md:1 (above the H1) | Insert a brief HTML comment + visible note: "This page is the syndication target for the Microsoft Biodiversity umbrella aggregator. The canonical project docs live in [README.md](README.md)." | `megadetector.md` and `README.md` overlap ~70 %; readers (and search-engine crawlers) currently cannot tell which is canonical. Clarifying purpose prevents drift between the two going forward.

<a name="ITEM-AUD-017"></a>
ITEM-AUD-017 | README.md:185 and megadetector.md:49 | Fix the markdown link text `[/SPARROW-Studio]` (leading slash) to `[SPARROW-Studio]` in the Biodiversity Ecosystem table. | Cosmetic typo; the URL is fine but the displayed text reads as a path fragment.

<a name="ITEM-AUD-018"></a>
ITEM-AUD-018 | docs/audit_report.md (NEW FILE) | Create the user-facing audit deliverable with sections: (1) Summary — single paragraph answering "can the repo run inference + fine-tuning today?"; (2) Findings — Documentation & Clarity (this round's structural fixes, by file); (3) Findings — Runtime Bugs (cross-scope items B1–B8 below, summarized, with pointers to the reviewer's report); (4) README — Suggested Fine-Tuning Section (the full markdown the user can paste in, mirroring ITEM-AUD-005); (5) Recommended Next Steps (ordered). Author this file in Step 2 after the inquisitor's approval verdicts. | Primary deliverable for this task; required by the user instructions.

## Cross-Scope Findings (behavioral — for reviewer in round 2)

These were noticed during read-once cross-context inspection of reviewer-owned
files. They are NOT in auditor scope and have NOT been planned for fix here.

- **B1 — `src/megadetector_ai/training.py:89`** reads `cfg.plots` (plural) but `examples/config_training.yaml:25` defines the key as `plot:` (singular). With `Munch` attribute access this raises `AttributeError: plots`, so `megadetector validate` is broken out of the box. Either the code key or the config key must change (the config is more user-visible; renaming the code to `cfg.plot` is the safer fix).
- **B2 — `examples/config_training.yaml:21`** has `weights: None # Path to weight to resume training`. PyYAML parses unquoted `None` as the Python **string** `"None"`, not `None`. Verified: `yaml.safe_load("weights: None") == {"weights": "None"}`. If a user sets `resume: True`, `training.py:25` assigns `model_path = "None"` and `YOLO("None")` will fail with a misleading file-not-found error. Use `null`, `~`, or leave the value empty.
- **B3 — `src/megadetector_ai/training.py:107`** in `inference()` calls `model(cfg.test_data)` with no `device=` argument. Neither `cfg.device_val` nor a dedicated `cfg.device_inference` is honored. Inference will silently run on the ultralytics default (GPU 0 if available, else CPU), ignoring the user's config.
- **B4 — `src/megadetector_ai/training.py:39-49`** `_prepare_data_config` rewrites the user's `data.yaml` **in place** every run when the `path:` field is relative. This is a surprising destructive side effect — the user's source-controlled config gets mutated. Safer: normalize in-memory and pass the resolved dict (or a tempfile) to ultralytics; or only rewrite when the value differs.
- **B5 — `src/megadetector_ai/training.py:103, 56, 82`** all call `_prepare_data_config(cfg)` and discard the return value, then pass the file path `cfg.data` to ultralytics anyway. The function name implies it returns a usable dict; either rename to `_normalize_data_config_in_place` or use the return value.
- **B6 — `src/megadetector_ai/training_utils.py:25-29`** has no retry / partial-download / checksum handling. A `wget.download` interrupted by SIGINT or a network hiccup leaves a partial `.pt` in `torch.hub`'s checkpoints dir; the next run's `os.path.exists` check returns True and loads the corrupt file. Suggest atomic-rename pattern (download to `.pt.tmp` then `os.replace`) and/or size/hash verification.
- **B7 — `src/megadetector_ai/cli.py:83`** `CLASS_NAMES = {0: "animal", 1: "person", 2: "vehicle"}` contradicts the README's "V6 is animal-only" narrative (and the docstring fixes in ITEM-AUD-013/014). The CLI only loads V6 (line 35) yet emits "person" / "vehicle" labels for any non-zero class id. Either V6 still emits the legacy classes (in which case the README is too aggressive) or the mapping should be `{0: "animal"}` with `"unknown"` fallback. Reviewer should confirm against actual V6 checkpoints and reconcile.
- **B8 — `src/megadetector_ai/training_utils.py:13-15`** maps `MDV6-yolov10-c` → filename `MDV6-yolov10n.pt` (yolov10 **nano**, ~2.3 M params). The README's "Compact" label is internally consistent with the published model card (2.3 M params), so this is likely intentional, but it deserves a one-line code comment so a future reader doesn't "fix" the apparent mismatch.

STATUS: PLAN-READY
