# Inquisitor review — round 1

## Approval decisions recap

Round 1 had 28 items planned across two editors. From `inquisitor_approvals.md`:

- **Auditor items (18):** 16 APPROVED, 2 REJECTED (`ITEM-AUD-013`, `ITEM-AUD-014` — both proposed a "V6 is animal-only" docstring rewrite that contradicts installed PW 1.2.4.2 where `MegaDetectorV6.CLASS_NAMES = {0: animal, 1: person, 2: vehicle}` is identical to V5).
- **Reviewer items (10):** 10 APPROVED, 0 REJECTED, 0 MODIFIED.
- **Cross-scope items:** 7 explicit deferrals to round 2 (auditor B3 / B8, reviewer CS-1 / CS-2 / CS-4 / CS-5 / CS-6); 5 cross-cuts resolved within round 1 by the appropriate editor; 1 cross-cut (B7) resolved by inquisitor verdict (cli.py:83 CLASS_NAMES correct as-is).

Auditor commit `e58feca` touched the 7 files the auditor was scoped for + the new `docs/audit_report.md`. Reviewer commit `badc1c2` touched the 4 files the reviewer was scoped for. Diffs were verified for each below.

## Fix verification (per ledger file)

<a name="README-md"></a>
### README.md

**Diff verified against `e58feca`.** Changes match the auditor report (ITEM-AUD-005/006/007/017):

- Line 36: new bridge sentence after Quick Start — `Need the local megadetector CLI or fine-tuning? See [Install from source](#install-from-source-for-fine-tuning-or-cli-use) and [Fine-Tuning](#fine-tuning) below.` Both anchors resolve (verified against the headings at lines 115 `### Install from source (for fine-tuning or CLI use)` and 239 `## Fine-Tuning`).
- Lines 115-128: new `### Install from source (for fine-tuning or CLI use)` subsection with `git clone` + `pip install -e .` + note about the `megadetector` shell entry point.
- Lines 203 (table) + 239-280: new `## Fine-Tuning` section. The training_guide is linked via `**Full reference:** [docs/training_guide.md](docs/training_guide.md)` — **the explicit user request ("link `docs/training_guide.md` from README.md") is satisfied.**
- Line 203 SPARROW-Studio display typo (`[/SPARROW-Studio]` → `[SPARROW-Studio]`) fixed.
- The Fine-Tuning section lists the 5 PW-1.2.4.2-supported variants (yolov9-c/-e, yolov10-c/-e, rtdetr-c) — correct.

**Residual issues (deferred to round 2 per inquisitor_approvals.md "Cross-cutting observation 2"):**

- Lines 65-75 Model Variants table still advertises 9 V6 variants (incl. `MDV6-apa-rtdetr-e`, `MDV6-mit-yolov9-c/-e`, `MDV6-apa-rtdetr-c`) that installed `pytorchwildlife==1.2.4.2` does NOT expose. This is CS-RF-3 / CS-2 in the reviewer report and Recommended Next Step 2 in `docs/audit_report.md`.
- Line 89 code example `pw_detection.MegaDetectorV6(version="MDV6-apa-rtdetr-e")` will crash on first run against installed PW — same root cause as REV-004 (which fixed the analogous example in `cli.py:7`). Captured implicitly by CS-RF-3 (variant cleanup). Worth flagging explicitly for round 2 so the maintainer sees the duplicated antipattern; not a new finding, but a parallel-implementation oversight.

**Verdict:** Claimed fixes applied correctly. README is now internally inconsistent on V6 variant count (5 in Fine-Tuning, 9 in Model Variants) — explicitly documented as round-2 work, but the inconsistency is now visible in a single user-facing file.

<a name="megadetector-md"></a>
### megadetector.md

**Diff verified against `e58feca`.** Changes match ITEM-AUD-016 / AUD-017:

- Lines 1-8: prepended HTML comment + visible `> [!NOTE]` declaring `megadetector.md` the umbrella-aggregator syndication target and `README.md` the canonical project documentation. Wording matches the inquisitor-approved text.
- Line 57: SPARROW-Studio typo fixed (`[/SPARROW-Studio]` → `[SPARROW-Studio]`).

**Residual issues:** None for this file's round-1 scope. Out-of-scope observation: the rest of `megadetector.md` still duplicates ~70 % of `README.md` content; the canonical-pointer note is a low-cost anti-drift mechanism but doesn't eliminate the duplication. This is the intentional design per the approvals doc — not a fix-needed item.

**Verdict:** Claimed fixes applied correctly.

<a name="pyproject-toml"></a>
### pyproject.toml

**Diff verified against `e58feca`.** Changes match ITEM-AUD-002/003/004:

- Line 50: `Documentation = "https://microsoft.github.io/MegaDetector/"` (was `.../CameraTraps/`).
- Line 52: `"Source Code" = "https://github.com/microsoft/MegaDetector"` (was `.../CameraTraps`).
- Line 53: `"Bug Tracker" = "https://github.com/microsoft/MegaDetector/issues"` (was `.../CameraTraps/issues`).

URLs now consistent with `Homepage` and `Repository` (both unchanged, both already pointed at `microsoft/MegaDetector`) and the README "Contributing" pointer at line ~334.

**Residual issues (deferred):** No version pin on `PytorchWildlife` (currently bare `PytorchWildlife` in `dependencies`). This is the lever for CS-RF-3 / CS-2 (variant whitelist drifting against future PW releases) — documented as Recommended Next Step 4 in `docs/audit_report.md`. Round-2 item, not in this round's scope.

**Verdict:** Claimed fixes applied correctly.

<a name="environment-yaml"></a>
### environment.yaml

**Diff verified against `e58feca`.** Changes match ITEM-AUD-008 / AUD-009:

- Lines 1-8: prepended 9-line header documenting that the conda block is Linux-x86_64–pinned (cites `libgcc-ng=14.1.0=h69a702a_1`) and that macOS/Windows users should `pip install -e .` from a fresh venv.
- Line 10: `name: megadetector-finetuning` (was `PW_Finetuning_Detection`).

Verification script's `yaml.safe_load(open("environment.yaml"))["name"] == "megadetector-finetuning"` confirms the rename took.

Inquisitor cross-checked that exactly two sites referenced the old name (this file + `docs/training_guide.md:23`); both updated in this commit. Verified no third site by running `grep -rn "PW_Finetuning_Detection"` — zero hits.

**Verdict:** Claimed fixes applied correctly. Two-site cascade complete.

<a name="docs-training-guide-md"></a>
### docs/training_guide.md

**Diff verified against `e58feca`.** Changes match ITEM-AUD-001 / AUD-010 / AUD-011 / AUD-012:

- Line 3: new back-link `← Back to [main README](../README.md).` — bidirectional navigation with the README's new Fine-Tuning section.
- Lines 13-23: replaced `### Using pip and \`requirements.txt\`` → `### Using pip (editable install from source)` with `pip install -e .` and three-line explanation that `pyproject.toml` covers all deps. AUD-001 satisfied.
- Line 30: `conda activate megadetector-finetuning` (was `PW_Finetuning_Detection`). Cascade from AUD-008.
- Lines 93-101: rewrote `## Configuration` opener to name `examples/config_training.yaml` explicitly with a `cp examples/config_training.yaml ./config.yaml` snippet.

**Residual issues (NEW — partially captured, partially missed):**

- Line 130 still reads `- \`plot\`: Boolean value indicating whether to plot results. Default: True` — the YAML rename `plot:` → `plots:` (REV-001) did not cascade to this third site. **Already tracked** as reviewer CS-RF-2 / CS-1 → deferred to round 2 (auditor scope). Confirmed.
- Line 125 still reads `- \`weights\`: Path to the weights file to resume training. Default: None` — should now say `Default: null` (or "unset") after REV-003 changed the YAML default to `null` and added the `_load_model` guard that rejects the literal string `"None"`. **NOT tracked** in any plan, report, or approvals doc. **NEW finding** — minor doc-cascade miss from REV-003.
- Line 109 documents `task:` field; reviewer CS-5 flags this is unused (no read in `training.py`). Deferred per approvals.

**Verdict:** Claimed fixes applied correctly. One new tiny cascade miss (line 125 `Default: None`).

<a name="src-megadetector-ai-init-py"></a>
### src/megadetector_ai/__init__.py

**No commit changes (correctly).** Audit-fix ITEM-AUD-013 was REJECTED by the inquisitor — the proposed "V6 focuses on animals only" rewrite contradicts installed PW 1.2.4.2 (`MegaDetectorV6.CLASS_NAMES = {0: animal, 1: person, 2: vehicle}`, identical to V5). Current file content at lines 4-6 reads `MegaDetector detects animals, people, and vehicles in camera trap images.` — matches installed PW and is left intact.

Auditor report `Skipped` section correctly documents this with the verified evidence path (`~/.cache/uv/archive-v0/NmuqR_Vp-sUYaNsyKewlK/PytorchWildlife/.../megadetectorv6.py:8-21`).

**Verdict:** Correctly NOT modified. Auditor accepted the inquisitor's rejection without dissent.

<a name="src-megadetector-ai-detector-py"></a>
### src/megadetector_ai/detector.py

**Diff verified against `e58feca`.** ITEM-AUD-015 applied; ITEM-AUD-014 rejected (no change).

- Lines 44-46: inserted `MegaDetectorV5 detects three classes: animals (class 0), people (class 1), and vehicles (class 2).` as the second paragraph of the V5 docstring (AUD-015).
- V6 docstring at lines 12-15 unchanged (AUD-014 rejected — same root reason as AUD-013).

**Residual issues (deferred):**

- Lines 22-31 V6 docstring `version=` enumeration still lists 9 variants. Only the 5 in `SUPPORTED_DETECT_VERSIONS` actually work with installed PW. Reviewer CS-4 — auditor round-2 work. The class-set wording at line 14 ("animals, people, and vehicles") must stay per the AUD-013/014 verdict; only the variant list needs trimming.

**Verdict:** Claimed fixes applied correctly. Structural change (V5 class enumeration) does not contradict any behavioral fix; V6 variant list inconsistency is the documented round-2 cascade.

<a name="src-megadetector-ai-training-py"></a>
### src/megadetector_ai/training.py

**Diff verified against `badc1c2`.** All 6 of ITEM-REV-002/003/006/007/009 changes match the reviewer report:

- Lines 24-31 `_load_model` resume-weights guard: rejects `None`, `"None"`, `""`, `"null"` with a clear `ValueError`. REV-003 ✓
- Lines 35-44 `_load_model` framework↔weights consistency check: rejects `model=YOLO` with `rtdetr` in `model_name`, and vice versa. REV-007 ✓
- Lines 56-78 `_prepare_data_config` rewritten: returns the path to a sidecar YAML under `runs/_resolved_data/{exp_name}_data.yaml`, never mutates the user's source YAML. Resolves relative to the YAML's directory (not CWD). REV-002 ✓
- Lines 85, 90, 113, 118 — call sites correctly capture `data_path = _prepare_data_config(cfg)` and pass `data=data_path` to `model.train()` / `model.val()`. REV-002 wiring ✓
- Lines 97-98 — `optimizer=cfg.optimizer, lr0=cfg.lr0` added to `model.train()` kwargs. REV-006 ✓
- Lines 143-149 — per-iteration `try/except Exception` in the inference save loop, with `getattr(results[i], "path", ...)` fallback for the path used in the warning. REV-009 ✓

**Verified the `cfg.plots` ↔ `plot:` fix aligns BOTH files** (substantive check from lead task):
- `training.py:120` reads `plots=cfg.plots` (unchanged from before this round).
- `examples/config_training.yaml:25` now reads `plots: True` (was `plot: True`).
- `grep -nE "cfg\.plot|plot:" src/megadetector_ai/training.py examples/config_training.yaml` returns exactly two lines that match `plots`, zero stale `plot` singulars. ✓ Same name in both files. (Third site `docs/training_guide.md:130` is the deferred cascade — auditor round 2.)

**Substantive check: `_prepare_data_config`'s destructive YAML rewrite** — VERIFIED REMOVED. The current function at lines 56-78 has NO `with open(cfg.data, 'w')` call; the only `open` is read-only (`with open(cfg.data) as f:`) and writes go to the sidecar path. The destructive `yaml.dump(data, f)` back to `cfg.data` is gone.

**Residual issues (NEW — minor):**

- Line 134 `inference()` still calls `_prepare_data_config(cfg)` and discards the return. With the new sidecar pattern this means inference creates an unused YAML at `runs/_resolved_data/{exp_name}_data.yaml` every run — wasteful but harmless. Reviewer report acknowledges this ("No regression — old code also discarded the return"), so it is technically known/accepted, not a missed item; flagging here so it lands on a round-2 polish list. The cleaner pattern would be to drop the call in `inference()` entirely (or use the resolved path for `model(cfg.test_data)` if relative-resolution is needed for inference inputs too).
- Auditor B3 (inference ignores `cfg.device_*`) is correctly deferred to round 2.

**Verdict:** Claimed fixes applied correctly and verified by static reading. No regressions in the destructive-rewrite removal. The `cfg.plots` / `plots:` alignment is the same name in both reviewer-owned files.

<a name="src-megadetector-ai-training-utils-py"></a>
### src/megadetector_ai/training_utils.py

**Diff verified against `badc1c2`.** Single change matches ITEM-REV-010:

- Lines 27-32: `os.access(".", os.W_OK)` precheck added before `wget.download(...)`. Raises `PermissionError` with a clear "CWD %r is not writable. Re-run from a writable directory" message.
- Note: the precheck runs AFTER `os.makedirs(os.path.join(torch.hub.get_dir(), "checkpoints"), exist_ok=True)`. That's fine — the makedirs targets the torch hub directory (not CWD), so it doesn't depend on CWD writability. Order is correct.

**Substantive check: did the reviewer add the 4 missing model variants to `get_model_path` OR document why they were excluded?** — Verified that `get_model_path` still supports exactly the same 5 variants it did before this round: `MDV6-yolov9-c/-e`, `MDV6-yolov10-c/-e`, `MDV6-rtdetr-c`. This is the same set as the new `SUPPORTED_DETECT_VERSIONS` in `cli.py` and matches installed PW 1.2.4.2's accepted set. The 4 README-advertised variants (`MDV6-apa-rtdetr-c/-e`, `MDV6-mit-yolov9-c/-e`) are NOT in installed PW, so adding them to `get_model_path` would point at non-existent Zenodo URLs.

The exclusion IS documented — in the reviewer report's `CS-RF-3` / cross-scope notes, in the auditor report's `## Cross-Scope Findings` "Reviewer CS-2", and in `docs/audit_report.md` Recommended Next Step 2 (round-2 cleanup: trim the README to 5 variants OR pin a PW version range that ships the others). But it is **not** documented as an inline code comment in `training_utils.py:23` near the `ValueError("Select a valid model version: ...")` line. **Minor NEW finding:** a one-line code comment near the variant whitelist (e.g. `# 5 variants matching PytorchWildlife==1.2.4.2; README advertises 4 more that require a newer PW release — see docs/audit_report.md`) would help future maintainers.

**Residual issues (deferred):**

- Auditor B6 (no retry / no checksum / no atomic rename) — round-2 hardening. REV-010 only adds the CWD precheck.
- Reviewer CS-RF-8 / Auditor B8 — `MDV6-yolov10-c` → filename `MDV6-yolov10n.pt` (nano) deserves an inline comment for the apparent name mismatch. Deferred.
- Reviewer CS-RF-6 — Zenodo record 14567879 (fine-tuning) vs 15398270 (inference) deserves a docs sentence. Deferred to auditor round 2.

**Verdict:** Claimed fix applied correctly. Variant-set is the same 5 as before; whether to extend or document is a round-2 decision.

<a name="src-megadetector-ai-cli-py"></a>
### src/megadetector_ai/cli.py

**Diff verified against `badc1c2`.** Changes match ITEM-REV-004/005/008:

- Line 7 docstring example: `--model MDV6-apa-rtdetr-e` → `--model MDV6-yolov10-e`. REV-004 ✓
- Lines 20-26: new module-level `SUPPORTED_DETECT_VERSIONS = ("MDV6-yolov9-c", "MDV6-yolov9-e", "MDV6-yolov10-c", "MDV6-yolov10-e", "MDV6-rtdetr-c")`. Set matches `training_utils.get_model_path`'s whitelist exactly. REV-005 ✓
- Lines 189-194: argparse `detect_parser.add_argument("--model", ..., choices=SUPPORTED_DETECT_VERSIONS, help="...Supported: ...")`. Argparse pre-import validation; reads `--help` enumerates the 5 supported variants. REV-005 ✓
- Lines 124-128, 143-147, 162-166: `try/except (ValueError, KeyError, AttributeError, FileNotFoundError)` wrapping the three `run_training/_validation/_inference` calls; friendly one-line error → `sys.exit(1)`. REV-008 ✓

**Substantive check: are the CLI `CLASS_NAMES = {0: animal, 1: person, 2: vehicle}` (line 92) consistent with how docstrings + README now describe V6 outputs?** — VERIFIED CONSISTENT. The new README Fine-Tuning section, the (unchanged) `detector.py` V6 docstring "Detects animals, people, and vehicles", the (unchanged) `__init__.py` "MegaDetector detects animals, people, and vehicles", and `cli.py:92` all agree on the 3-class output. The auditor's original AUD-013/014 framing of "V6 is animal-only" was correctly rejected by the inquisitor and the rejection has cascaded cleanly through this round: NO file in the repo now claims V6 is single-class.

**Verified import smoke from verification.txt:** `megadetector --help` runs end-to-end and prints the expected subcommand list `{detect,train,validate,inference}`. The `argparse` `choices=SUPPORTED_DETECT_VERSIONS` doesn't trip help generation.

**Verdict:** Claimed fixes applied correctly. CLI class names are consistent with the new documentation surface.

<a name="examples-config-training-yaml"></a>
### examples/config_training.yaml

**Diff verified against `badc1c2`.** Two-line change matches ITEM-REV-001 / REV-003:

- Line 21: `weights: None # Path to weight to resume training` → `weights: null # Path to .pt to resume from when resume=True`. REV-003 ✓
- Line 25: `plot: True` → `plots: True`. REV-001 ✓

`yaml.safe_load` in verification.txt confirms: `weights` key parses as Python `None` (not the string `"None"`); `plots` key is present with value `True`; `plot` key is absent.

**Residual issues:**

- Reviewer CS-5 `task:` field at line 6 is read nowhere in `training.py`; dispatch is via CLI subcommand. Deferred to round 2 (reviewer scope).

**Verdict:** Claimed fixes applied correctly. The two-character / two-key change is enough to unblock `megadetector validate` and `megadetector train --config ... resume=True`.

## Missed issues

These are findings the auditor and reviewer did NOT enumerate in their plans/reports, surfaced during this round's read-once verification. Both are minor cascades — neither blocks the round.

1. **`docs/training_guide.md:125` — `weights` documentation lag from REV-003.** The line still reads `Default: None`. After this round's REV-003 changed the YAML default to `null` and added a `_load_model` guard that explicitly rejects the literal string `"None"`, the documented default is misleading. Should read `Default: null (or unset)` or similar. Same pattern as reviewer CS-1 / CS-RF-2 (the `plot:`→`plots:` cascade), but specifically for `weights` — and CS-1 only lists the `plot` cascade, so this `weights` cascade is not currently tracked anywhere. **NEW.**

2. **`src/megadetector_ai/training_utils.py:23` — inline comment for the variant whitelist.** The 5-variant set in `get_model_path` matches installed PW 1.2.4.2 exactly, but the four README-advertised variants that are intentionally excluded (`MDV6-apa-rtdetr-c/-e`, `MDV6-mit-yolov9-c/-e`) are documented only in the cross-scope notes (reviewer CS-RF-3 and the audit_report). A one-line code comment next to the `ValueError("Select a valid model version: ...")` line would make the intentional exclusion visible to future maintainers without forcing them to read the cross-scope appendices. **NEW (minor).**

Both are auditor-scope in round 2.

### Pre-existing residual issues NOT new but worth re-noting

- `README.md:65-75` Model Variants table advertises 9 variants; new Fine-Tuning section (this round) lists 5. The internal inconsistency is now visible in a single user-facing file. Tracked as reviewer CS-RF-3 / CS-2; round-2 cascade.
- `README.md:89` example `pw_detection.MegaDetectorV6(version="MDV6-apa-rtdetr-e")` will crash on first run — analogous to the `cli.py:7` example REV-004 fixed. The auditor's plan and report do NOT call out line 89 specifically; it sits under the umbrella of CS-RF-3 but the line-level discoverability is worth bumping in the round-2 priorities below.
- `src/megadetector_ai/training.py:134` — `inference()` calls `_prepare_data_config(cfg)` and discards the return; with the new sidecar pattern this writes an unused YAML each inference run. Reviewer acknowledged in their report; not a regression, just a polish item.
- `src/megadetector_ai/detector.py:22-31` V6 docstring still enumerates 9 variants. Reviewer CS-RF-4 / auditor round 2.

## Cross-impact analysis

**Auditor structural changes affecting reviewer scope:** none observed. The auditor changed only auditor-owned files and the new `docs/audit_report.md`. `git show --stat e58feca` shows 7 source files + 1 new doc, none of which overlap the reviewer's 4 files.

**Reviewer behavioral changes affecting auditor scope:** two cascades land in auditor-owned docs but were correctly NOT applied this round (they would have been out-of-scope edits for the reviewer):

- REV-001 (`plot:` → `plots:` YAML rename) needs `docs/training_guide.md:130` updated. Listed as CS-RF-2.
- REV-003 (`weights:` YAML default changed from `None` → `null`) needs `docs/training_guide.md:125` updated. **NOT listed anywhere — new finding from this verification pass.**

**Contradictions between docs and code introduced this round:** none. The two REJECTED auditor items (AUD-013 / AUD-014) were rejected precisely because applying them would have contradicted the unchanged code (cli.py:92 CLASS_NAMES, the upstream PW V6 class set). The rejection prevented an introduced contradiction. The new `docs/audit_report.md` explicitly states the verified ground truth and avoids the rejected "V6 animal-only" framing.

**Pre-existing contradictions NOT resolved this round (correctly deferred):** README.md vs PW variant set (9 advertised, 5 supported). The new Fine-Tuning section uses the correct 5 — but the existing Model Variants table at lines 65-75 is now in tension with both the new section and installed PW. This is the most user-visible cross-impact and should top round-2 priorities.

**Silent-drop check:** No approved item was silently dropped. AUD-013 / AUD-014 are correctly recorded as `action:"skipped"` in the COVERAGE_LOG. All 16 APPROVED auditor items + all 10 APPROVED reviewer items + AUD-018 (audit_report deliverable) landed in commits e58feca and badc1c2.

## Verification results

From `verification.txt`:

- `python3 -m py_compile` on all changed Python files: **OK**.
- `ruff` lint on `src/` + `examples/`: **All checks passed**.
- YAML syntax on `examples/config_training.yaml`: keys parse cleanly; `weights` is `None` (real Python None, not the string), `plots` is `True`, `plot` is absent.
- YAML syntax on `environment.yaml`: `name == "megadetector-finetuning"`. Rename verified.
- `pyproject.toml` parses; project name `megadetector-ai 0.1.0`; deps list intact.
- `megadetector --help` smoke: prints the expected subcommand list `{detect,train,validate,inference}`.

**Expected failures (environment-only, not regressions):**

- Import smoke fails on `import wget` (`ModuleNotFoundError`) and `from PytorchWildlife.models import detection` (`ModuleNotFoundError`). These are runtime deps listed in `pyproject.toml`. The verification environment does not have them installed via `pip install -e .`; this is an env-prep gap in `verification.txt`, not a regression of this round's edits. Both modules were absent **before** this round's commits as well — the round's diffs do not add or remove any imports of `wget` or `PytorchWildlife` (verified by `grep "import wget\|PytorchWildlife"` against `HEAD~2`).

**No regressions detected.** Every check that succeeded pre-round still succeeds; every check that failed pre-round (the import smokes) fails for the same environment-setup reason.

## Coverage analysis

- Ledger files: 11
- Verified this round: 11
- Cumulative covered (scope_check.sh): 11/11
- Uncovered: []
- action="fixed" entries this round: 11
- NEW issues found this round: 2

Every ledger file has at least one inquisitor `action:"verified"` entry pointing at a resolvable anchor in this file. `scope_check.sh` exits 0.

## Next-round priorities (if NEEDS-MORE)

In order of user impact:

1. **`README.md:65-75` + `README.md:89` + `src/megadetector_ai/detector.py:22-31` — V6 variant cleanup (auditor scope).** Either trim all three sites to the 5 PW-1.2.4.2-supported variants OR pin a `pytorchwildlife` version range in `pyproject.toml` that ships the other 4 (currently the dep is bare `PytorchWildlife`). The code example at README.md:89 is a user-visible crash on copy-paste — highest priority of the deferred items. Tracks CS-RF-3 / CS-2 / CS-4 from reviewer.
2. **`docs/training_guide.md:130` cascade — `plot:` → `plots:` (auditor scope).** Reviewer CS-RF-2 / CS-1. One-line edit.
3. **`docs/training_guide.md:125` cascade — `Default: None` → `Default: null (or unset)` (auditor scope, NEW finding this round).** Mirrors item 2 but for `weights:` after REV-003.
4. **`src/megadetector_ai/training_utils.py` inline comment near the variant whitelist (reviewer or auditor scope, NEW finding this round).** Make the intentional exclusion of `apa-*` / `mit-*` variants legible at the file where future maintainers will be tempted to "fix" the perceived gap.
5. **`src/megadetector_ai/training.py:inference()` — honor `cfg.device_*` (reviewer scope).** Auditor B3 deferral.
6. **`src/megadetector_ai/training.py:inference()` — drop or wire the unused `_prepare_data_config(cfg)` call (reviewer scope).** Acknowledged in reviewer report; round-2 polish.
7. **`src/megadetector_ai/training_utils.py` — full download hardening (atomic rename, SHA256 checksum, retry) (reviewer scope).** Auditor B6; REV-010 was only the CWD precheck.
8. **Set up a minimal `tests/` skeleton (auditor scope, structural).** Three highest-value tests: (a) YAML-parse smoke that asserts every `cfg.<field>` reference in `training.py` resolves against `examples/config_training.yaml`; (b) argparse `--help` smoke for each `megadetector` subcommand; (c) `_prepare_data_config` round-trip test asserting the user's input YAML is not mutated. All three are deterministic, no GPU / no weights download. Tracked in reviewer CS-RF-1 and audit_report Recommended Next Step 3.
9. **`docs/training_guide.md` — sentence explaining Zenodo 14567879 (fine-tuning) vs 15398270 (PW inference) (auditor scope).** Reviewer CS-RF-6.
10. **`examples/config_training.yaml` — decide fate of unused `task:` field (reviewer scope).** Reviewer CS-RF-5 / CS-5.

STATUS: NEEDS-MORE SCOPE_CHECK=PASS COVERED=11/11 UNCOVERED=[] NEW=13
