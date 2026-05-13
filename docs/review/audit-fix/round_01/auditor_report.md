# Auditor report — round 1 (Phase 2 APPLY)

Commit: `e58fecaf98d9f071d7ba75a25bec22d4178ab201`
Phase 1 plan: `auditor_plan.md`
Inquisitor verdicts: `inquisitor_approvals.md` (AUD section)

## Changes Applied

<a name="ITEM-AUD-001"></a>
**ITEM-AUD-001** | `docs/training_guide.md:11-15` | Replaced the `### Using pip and \`requirements.txt\`` subsection (which directed users at a non-existent `requirements.txt`) with a `### Using pip (editable install from source)` subsection that uses `pip install -e .` and explains the editable install also exposes the `megadetector` CLI entry point. | No `requirements.txt` exists in the repo; `pyproject.toml` covers every runtime import. Verified anchor text matched before edit.

<a name="ITEM-AUD-002"></a>
**ITEM-AUD-002** | `pyproject.toml:50` | `Documentation = "https://microsoft.github.io/CameraTraps/"` → `"https://microsoft.github.io/MegaDetector/"`. | Matches existing `Homepage` and `Repository` keys (both point at `microsoft/MegaDetector`) and the README's "Full installation guide" link.

<a name="ITEM-AUD-003"></a>
**ITEM-AUD-003** | `pyproject.toml:52` | `"Source Code" = "https://github.com/microsoft/CameraTraps"` → `"https://github.com/microsoft/MegaDetector"`. | Same migration as AUD-002.

<a name="ITEM-AUD-004"></a>
**ITEM-AUD-004** | `pyproject.toml:53` | `"Bug Tracker" = "https://github.com/microsoft/CameraTraps/issues"` → `"https://github.com/microsoft/MegaDetector/issues"`. | Matches `README.md` "Contributing" section pointer.

<a name="ITEM-AUD-005"></a>
**ITEM-AUD-005** | `README.md` — new `## Fine-Tuning` section inserted between `## Performance` and `## Version History` | Added a top-level Fine-Tuning section with: one-paragraph framing (why/when to fine-tune), Quick path code block (git clone + `pip install -e .` + `cp examples/config_training.yaml ./config.yaml` + the three CLI subcommands), bulleted list of the 5 installed PW V6 variants, output-location note, and a link to `docs/training_guide.md`. | Made the orphaned training guide discoverable from the canonical landing page.

<a name="ITEM-AUD-006"></a>
**ITEM-AUD-006** | `README.md` — Installation section | Added `### Install from source (for fine-tuning or CLI use)` subsection documenting `git clone https://github.com/microsoft/MegaDetector && cd MegaDetector && pip install -e .` and noting that this exposes the `megadetector` shell command. | The `[project.scripts] megadetector = ...` entry in `pyproject.toml` was previously undocumented.

<a name="ITEM-AUD-007"></a>
**ITEM-AUD-007** | `README.md:34` (Quick Start) | Inserted one bridge sentence after "That's it. Three lines…" pointing readers to `#install-from-source-for-fine-tuning-or-cli-use` and `#fine-tuning`. | Reconciles the high-level PW API path with the new local-CLI / fine-tuning paths.

<a name="ITEM-AUD-008"></a>
**ITEM-AUD-008** | `environment.yaml:1` | `name: PW_Finetuning_Detection` → `name: megadetector-finetuning`. | Aligns with `pyproject.toml`'s `name = "megadetector-ai"`. Inquisitor cross-check confirmed exactly two sites referenced the old name (this one + `docs/training_guide.md:23`); both updated in this commit.

<a name="ITEM-AUD-009"></a>
**ITEM-AUD-009** | `environment.yaml` (above `name:`) | Prepended a 9-line `#`-comment header documenting that the conda block is pinned to Linux x86_64 conda-forge builds, that macOS/Windows users should prefer `pip install -e .` from a fresh venv, and that only the `pip:` subtree is platform-portable. | Verified the existing pins include Linux-specific markers (`_libgcc_mutex`, `libgcc-ng=14.1.0=h69a702a_1`).

<a name="ITEM-AUD-010"></a>
**ITEM-AUD-010** | `docs/training_guide.md:23` | `conda activate PW_Finetuning_Detection` → `conda activate megadetector-finetuning`. | Cascade from AUD-008.

<a name="ITEM-AUD-011"></a>
**ITEM-AUD-011** | `docs/training_guide.md:86-89` (start of `## Configuration`) | Rewrote the section opener to name `examples/config_training.yaml` explicitly and document the `cp examples/config_training.yaml ./config.yaml` pattern. | The doc previously referenced only `config.yaml`, leaving readers unsure where the reference example lived.

<a name="ITEM-AUD-012"></a>
**ITEM-AUD-012** | `docs/training_guide.md:1` (just under H1) | Added `← Back to [main README](../README.md).` | Bidirectional navigation, now that the README links into the guide via AUD-005.

<a name="ITEM-AUD-013"></a>
**ITEM-AUD-013** | `src/megadetector_ai/__init__.py:5-6` | **NOT APPLIED — REJECTED by inquisitor.** | The proposed "V6 focuses on animals only" framing is factually wrong against installed PW 1.2.4.2 (`MegaDetectorV6.CLASS_NAMES = {0: animal, 1: person, 2: vehicle}`). Existing text is correct. See "Skipped" below.

<a name="ITEM-AUD-014"></a>
**ITEM-AUD-014** | `src/megadetector_ai/detector.py:12-15` | **NOT APPLIED — REJECTED by inquisitor.** | Same root reason as AUD-013. See "Skipped" below.

<a name="ITEM-AUD-015"></a>
**ITEM-AUD-015** | `src/megadetector_ai/detector.py:42-58` | Inserted "MegaDetectorV5 detects three classes: animals (class 0), people (class 1), and vehicles (class 2)." as the second paragraph of the V5 docstring. | Made the V5 class set explicit at the API surface. Unaffected by the AUD-013/014 rejection because V5's 3-class output is uncontroversial.

<a name="ITEM-AUD-016"></a>
**ITEM-AUD-016** | `megadetector.md:1` (above the H1) | Prepended an HTML comment plus a `> [!NOTE]` callout declaring `megadetector.md` the umbrella-aggregator syndication target and `README.md` the canonical project documentation. | Prevents drift between the two ~70 %-overlapping landing pages.

<a name="ITEM-AUD-017"></a>
**ITEM-AUD-017** | `README.md:185` and `megadetector.md:49` | `[/SPARROW-Studio](...)` → `[SPARROW-Studio](...)` in the Biodiversity Ecosystem tables. | Cosmetic typo. URL was correct in both files; only the display text needed fixing.

<a name="ITEM-AUD-018"></a>
**ITEM-AUD-018** | `docs/audit_report.md` (NEW FILE) | Created the user-facing audit report covering: Executive Summary, Repo Layout, Findings — Documentation & Clarity, Findings — Runtime Bugs (reviewer scope summarized), README — Suggested Fine-Tuning Section (paste-ready), Recommended Next Steps, Appendix: Files Reviewed. | Primary user deliverable. The report explicitly drops the rejected "V6 animal-only" framing and reports the verified ground truth instead (per inquisitor verdict on AUD-013/014/018).


## Tests Added/Updated

**n/a — flagged as Cross-Scope Finding.** This repository ships **no
automated test infrastructure** at round 1: no `tests/` directory, no
`pytest` / `unittest` configuration in `pyproject.toml`, no CI workflow under
`.github/`. Two of the round-1 reviewer fixes (REV-001 `plot` → `plots` and
REV-003 `weights: None` string-vs-null) are exactly the class of bug a single
YAML-parse smoke test would have caught at commit time. This is the highest-
value piece of round-2 follow-up listed in `docs/audit_report.md` §
"Recommended Next Steps" item 3.


## Cross-Scope Findings (behavioral — reviewer territory)

These were noticed during read-once cross-context inspection of reviewer-
owned files and were correctly **not** acted on in auditor scope. They are
reproduced here for the audit trail; the reviewer's plan/report covers the
ones addressed this round and the inquisitor's `inquisitor_approvals.md`
"Cross-cutting observation 2 — deferrals to round 2" specifies which carry
into round 2.

- **B1** | `src/megadetector_ai/training.py:89` reads `cfg.plots`; `examples/config_training.yaml:25` defines `plot:`. → Addressed this round by reviewer ITEM-REV-001.
- **B2** | `examples/config_training.yaml:21` `weights: None` parses as Python string `"None"`. → Addressed this round by reviewer ITEM-REV-003.
- **B3** | `src/megadetector_ai/training.py:107` `inference()` ignores `cfg.device_*`. → **Deferred to round 2** (reviewer scope).
- **B4** | `src/megadetector_ai/training.py:39-49` `_prepare_data_config` mutates the user's data YAML in place. → Addressed this round by reviewer ITEM-REV-002.
- **B5** | Callers of `_prepare_data_config(cfg)` discard its return value. → Addressed implicitly by reviewer ITEM-REV-002 (the rewritten function returns a path the callers now use).
- **B6** | `training_utils.py:25-29` `wget.download` has no retry / checksum / atomic-rename. → Partially addressed by reviewer ITEM-REV-010 (CWD-writable precheck); full hardening **deferred to round 2**.
- **B7** | `src/megadetector_ai/cli.py:83` `CLASS_NAMES = {0: animal, 1: person, 2: vehicle}` vs README's "V6 = animals" framing. → **Resolved** by inquisitor cross-check: `cli.py:83` is **correct** and matches the installed PW V6 class set. AUD-013 and AUD-014 (the proposed docstring rewrites built on the wrong assumption) were rejected.
- **B8** | `training_utils.py:13-15` maps `MDV6-yolov10-c` → `MDV6-yolov10n.pt` (yolov10 nano). → **Deferred to round 2** as a one-line code-comment item.

Plus two additional auditor-scope items the reviewer flagged that did not
make round 1 (deferred to round 2 per the inquisitor's "Cross-cutting
observation 2"):
- **Reviewer CS-1** | `docs/training_guide.md:117` documents `plot:` and needs to cascade to `plots:` after REV-001 lands.
- **Reviewer CS-2** | `README.md:65-73` advertises 9 V6 variants but installed `pytorchwildlife==1.2.4.2` exposes only 5 (`MDV6-yolov9-c/-e`, `MDV6-yolov10-c/-e`, `MDV6-rtdetr-c`). Either trim the table or pin a PW version range and document the gap.
- **Reviewer CS-4** | `src/megadetector_ai/detector.py:22-31` V6 docstring lists all 9 variants; trim to the supported 5 (class-set wording must stay "animals, people, and vehicles" per the AUD-013/014 verdict).
- **Reviewer CS-6** | `training_utils.get_model_path` URLs point at Zenodo record 14567879; PW's own V6 fetches from record 15398270. Worth one sentence in `docs/training_guide.md`.


## Skipped

<a name="ITEM-AUD-013"></a>
**ITEM-AUD-013 — REJECTED.** The plan proposed rewriting the package docstring
in `src/megadetector_ai/__init__.py:5-6` from "MegaDetector detects animals,
people, and vehicles in camera trap images." to a V6-animal-only framing.
Inquisitor verified against installed `pytorchwildlife==1.2.4.2` at
`~/.cache/uv/archive-v0/NmuqR_Vp-sUYaNsyKewlK/PytorchWildlife/models/detection/ultralytics_based/megadetectorv6.py:8-21`:
`MegaDetectorV6.CLASS_NAMES = {0: "animal", 1: "person", 2: "vehicle"}` and
upstream docstring reads "specifically designed for detecting animals,
persons, and vehicles." The README's "Animal Recall" metric column is a
per-variant metric reported only for the animal class — NOT a class-set
restriction. Existing text is correct. **No change.**

<a name="ITEM-AUD-014"></a>
**ITEM-AUD-014 — REJECTED.** Same root reason as AUD-013. The proposed V6
docstring rewrite at `src/megadetector_ai/detector.py:12-15` ("V6 focuses
exclusively on the animal class…") contradicts the installed PW V6's actual
3-class output. **No change.** The narrower variant-list cleanup (trim the
9-bullet `version` list in the V6 docstring to the 5 variants the installed
PW actually accepts) is deferred to round 2 as reviewer CS-4 — but the class-
set wording must stay "animals, people, and vehicles".


## Files NOT Owned by Auditor — Verified Untouched

Reviewer-owned files (`src/megadetector_ai/training.py`,
`src/megadetector_ai/training_utils.py`, `src/megadetector_ai/cli.py`,
`examples/config_training.yaml`) were read once for cross-scope findings but
**not** edited in this commit. `git show --stat e58feca` confirms the commit
touched only the 7 owned paths listed in the Changes Applied table above.


STATUS: DONE COMMIT=e58fecaf98d9f071d7ba75a25bec22d4178ab201
