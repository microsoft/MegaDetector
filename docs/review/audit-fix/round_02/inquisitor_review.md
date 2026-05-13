# Inquisitor review — round 2

## Approval decisions recap
3/3 auditor items APPROVED (ITEM-AUD-201, ITEM-AUD-202, ITEM-AUD-203);
reviewer reported NOTHING-TO-DO and the spot-checks confirmed it.

## Fix verification (per ledger file)

<a name="README-md"></a>
### README.md
**Verdict: VERIFIED with residual concerns.** ITEM-AUD-201 (commit
`b709a155`) applied exactly as approved: 9-row table trimmed to 5 rows at
lines 64–70, "Permissive licenses" highlight bullet at old line 60
deleted, "Best accuracy" bullet at line 75 rewritten to
`MDV6-yolov10-e (82.8% recall, AGPL-3.0)`, "Need MIT license?" bullet
dropped, Python example at line 83 now `version="MDV6-yolov10-e"`. All 5
variants in the new table exactly match `SUPPORTED_DETECT_VERSIONS` in
`cli.py:20–26` and `training_utils.get_model_path`'s whitelist. README
Fine-Tuning section at lines 261–265 already listed exactly the same 5
in round 1, so the file is now internally consistent in its main user
flow.

**Residual concerns (NEW — not in any prior plan, introduced by the
trim cascade, NON-blocking):**

1. **`README.md:54`** — Highlights framing still says "**efficiency**,
   **modern architectures**, and **licensing flexibility**." After the
   trim, all 5 documented V6 variants are AGPL-3.0; the bullet that
   substantiated "licensing flexibility" (Permissive licenses MIT and
   Apache-2.0 alongside AGPL-3.0) was correctly deleted by ITEM-AUD-201
   but the umbrella claim above it survives unchanged. Reader sees the
   framing then scans the table and finds no licensing variety.

2. **`README.md:280`** — Version history table cell for V6.0:
   `2.3M–76M | Multiple variants, MIT/Apache options`. Both halves are
   now stale: max param count in the trimmed table is **58.1M**
   (`MDV6-yolov9-e`), not 76M (that was `MDV6-apa-rtdetr-e`, removed);
   and the "MIT/Apache options" annotation has no referent after the
   trim.

3. **`README.md:340`** — License footer: "Individual model weights are
   released under MIT, Apache-2.0, or AGPL-3.0 — see the [Model
   Variants](#model-variants) table for per-variant licensing." This is
   a direct internal contradiction: the section sends the reader to the
   Model Variants table to verify per-variant licensing, but the table
   now only contains AGPL-3.0 entries. The link target undermines the
   adjacent claim.

None of these cause runtime errors; they are doc-vs-doc inconsistencies
that mislead a reader about license terms and parameter ranges. The
auditor report explicitly carved "editorial consolidation" out of
round 2's scope, so these were arguably implicitly deferred — but they
are genuine NEW findings against the post-round-2 file state and merit
explicit listing here.

<a name="megadetector-md"></a>
### megadetector.md
**Verdict: VERIFIED clean.** Not touched in round 2's commit (`git show`
confirms only 3 files changed: README.md, training_guide.md,
detector.py). Re-read lines 1–62 against the round 1 fix:
- Hint banner + canonical pointer to `README.md` intact (lines 1–7).
- No variant enumeration anywhere in the file (V6 section refers only
  to `MDV6-yolov10-c` as an illustrative compact size — supported
  variant, no risk).
- No license-variety claims that would be stale after the README trim.
- No `plot:` references to cascade-fix.

Syndication target remains accurate and self-contained.

<a name="pyproject-toml"></a>
### pyproject.toml
**Verdict: VERIFIED clean.** Not touched in round 2. Re-read end-to-end:
all imports in the codebase (`PytorchWildlife`, `ultralytics`, `munch`,
`wget`, `yaml`, `torch`) are present in `dependencies` (lines 39–46);
`PyYAML>=6.0` covers `yaml.safe_load`/`yaml.load`/`yaml.safe_dump` calls
in `training.py:18,65,77`; `munch>=2.0.0` covers `from munch import
Munch` in `training.py:10`; project URLs all point to the public
`microsoft/MegaDetector` repo (the round 1 fix); `[project.scripts]`
exposes `megadetector = megadetector_ai.cli:main`, which matches
`cli.py:171–244` exactly. Deferred reviewer item — PW version pin — is
non-blocking polish that the round 2 plan correctly held back.

<a name="environment-yaml"></a>
### environment.yaml
**Verdict: VERIFIED clean.** Not touched in round 2. Conda block remains
Linux-x86_64-only; the platform-portability banner at the top of the
file (round 1 fix) is intact. `name: megadetector-finetuning` (line 10)
matches the round 1 rename. Pip subtree pins `ultralytics==8.2.100`,
`munch==4.0.0`, `wget==3.2`, `pyyaml==6.0.2`, `pytorchwildlife`,
`torch==2.4.1` — superset of pyproject.toml runtime deps. No regression.

<a name="docs-training-guide-md"></a>
### docs/training_guide.md
**Verdict: VERIFIED clean.** ITEM-AUD-203 applied exactly: line 130 now
reads `- \`plots\`: Boolean value indicating whether to plot results.
Default: True`. The cascade is now closed end-to-end across the three
sites (`examples/config_training.yaml:25` `plots: True`, this doc, and
`training.py:120` `plots=cfg.plots`). Verified by:
- `git show b709a155 -- docs/training_guide.md` → single-character
  diff, `plot` → `plots`.
- `grep -n 'plot' docs/training_guide.md` returns only the new `plots:`
  bullet at line 130 — no stale `plot:` survives.
- Cross-checked `training.py` for `cfg.plot` (bare) — zero hits;
  `cfg.plots` — one hit at line 120.

Deferred line-125 `weights: ... Default: None` lag remains — it does
not block use because `training.py:25–30` `_load_model` raises a clear
`ValueError("Got: 'None'")` when a user follows the doc literally.
Non-blocking and explicitly waved off in the round 2 plan.

<a name="src-megadetector-ai-init-py"></a>
### src/megadetector_ai/__init__.py
**Verdict: VERIFIED clean.** Not touched in round 2. Imports
`MegaDetectorV6, MegaDetectorV5` from `.detector`; `__all__` is the
two-element tuple; `__version__ = "0.1.0"` matches `pyproject.toml:7`.
Module-level docstring's class-set wording ("animals, people, and
vehicles") is consistent with the AUD-013/014 rejection verdict (V6
CLASS_NAMES upstream matches V5's). Skipped in round 1 by the auditor's
own judgment (ITEM-AUD-013) and that verdict still holds.

<a name="src-megadetector-ai-detector-py"></a>
### src/megadetector_ai/detector.py
**Verdict: VERIFIED with residual concerns.** ITEM-AUD-202 (commit
`b709a155`) applied exactly: lines 22–27 now enumerate the 5 supported
variants only (`yolov9-c/-e`, `yolov10-c/-e`, `rtdetr-c`); the four
unsupported bullets (`mit-yolov9-{c,e}`, `apa-rtdetr-{c,e}`, the last
with the "(best accuracy)" lure) are deleted. `help(MegaDetectorV6)`
output and IDE hovers will no longer name crashing arguments. The
class-set wording at line 14 ("Detects animals, people, and vehicles")
is preserved verbatim per the AUD-013/014 rejection — correct call (V6
CLASS_NAMES upstream is identical to V5's).

**Residual concerns (NEW — not in any prior plan, introduced by the
trim cascade, NON-blocking):**

4. **`detector.py:16`** — V6 docstring summary still reads "Multiple
   model variants are available, ranging from **2.3M to 76M
   parameters**." Max param count in the trimmed bullet list is 58.1M
   (`MDV6-yolov9-e`); 76M was `MDV6-apa-rtdetr-e`, removed two lines
   below. Same trim-cascade pattern as README.md:280.

5. **`detector.py:45–46`** — V5 docstring's comparative claim about V6:
   "We recommend V6 for new projects — it is smaller, faster, and
   **offers permissive license options**." After the trim, all 5
   documented V6 variants are AGPL-3.0; the "permissive license
   options" framing has no referent in the trimmed enumeration. Mirrors
   the README.md:54 issue on the V5 class surface.

Same calculus as the README residuals: doc-only, no runtime effect,
implicitly under the "editorial consolidation out-of-scope for round 2"
carve-out from the auditor report. Worth one round-3 pass.

<a name="src-megadetector-ai-training-py"></a>
### src/megadetector_ai/training.py
**Verdict: VERIFIED clean (no regression).** Not touched in round 2.
End-to-end re-trace of `megadetector train --config
examples/config_training.yaml`:
- `cli.train` validates the path then calls `training.train`.
- `load_config` → `Munch(yaml.load(...))` — all 22 YAML keys load.
- `_load_model`: `cfg.resume=False` → `get_model_path("MDV6-yolov9-e")`
  → resolves to Zenodo URL (supported variant). `cfg.model="YOLO"`,
  `model_name="MDV6-yolov9-e"` (no "rtdetr") → consistency guard passes
  → `YOLO(model_path)`.
- `_prepare_data_config`: opens `cfg.data` read-only; if relative
  `path:`, resolves under `runs/_resolved_data/<exp_name>_data.yaml` —
  non-destructive sidecar. Verified `open()` mode at line 64 is read,
  line 76 is write to the sidecar location only.
- `model.train(...)` kwargs map 1:1 to ultralytics-supported names
  (`data, epochs, imgsz, device, save_period, workers, batch,
  optimizer, lr0, val, project, name, patience, resume`).
- `validate`: passes `plots=cfg.plots` (line 120) — matches YAML key
  `plots:` after REV-001 and matches doc after AUD-203. Cascade closed.
- `inference`: per-image `try/except Exception` with `getattr(results[i],
  "path", "<index i>")` fallback (lines 142–149) — REV-009 fix intact.

`grep -nE "cfg\.[A-Za-z_]+" training.py` → 21 distinct fields, all
present in `examples/config_training.yaml`. Only YAML-only-unused key
is `task:` (cosmetic, already deferred). No regressions.

<a name="src-megadetector-ai-training-utils-py"></a>
### src/megadetector_ai/training_utils.py
**Verdict: VERIFIED clean (no regression).** Not touched in round 2.
The whitelist branches (lines 7–22) name exactly the 5 supported
variants and the `else` raises `ValueError('Select a valid model
version: ...')` listing those 5 by name (line 23). REV-010 CWD
writability precheck (lines 27–32) intact: `wget.download` is only
invoked after `os.access(".", os.W_OK)` succeeds, so the silent-failure
mode is closed. Zenodo URLs use record `14567879` consistently (the
deferred "explain 14567879 vs 15398270" item is informational, not
blocking — the URLs that the code uses are stable Zenodo permalinks).

<a name="src-megadetector-ai-cli-py"></a>
### src/megadetector_ai/cli.py
**Verdict: VERIFIED clean (no regression).** Not touched in round 2.
Spot-checks:
- `SUPPORTED_DETECT_VERSIONS` (lines 20–26) = the 5 supported variants;
  used as `choices=` for `--model` (line 191), so argparse rejects
  unsupported variants before any PW call.
- Module docstring `Usage:` example at line 7 uses `MDV6-yolov10-e`
  (post-REV-004) — supported, no copy-paste crash.
- `train/validate/inference` wrappers all catch `(ValueError, KeyError,
  AttributeError, FileNotFoundError)` and print a friendly error +
  exit 1 (REV-008, lines 126, 145, 164).
- `_format_detections` CLASS_NAMES `{0: "animal", 1: "person", 2:
  "vehicle"}` matches the V6 upstream class set (3-class, identical to
  V5) — same root rationale that kept AUD-013/014 rejected.

<a name="examples-config-training-yaml"></a>
### examples/config_training.yaml
**Verdict: VERIFIED clean (no regression).** Not touched in round 2.
22 keys parse cleanly (`yaml.safe_load` confirmed in `verification.txt`).
REV-001 `plots: True` (line 25), REV-003 `weights: null # Path to .pt
to resume from when resume=True` (line 21) both intact. `model_name:
MDV6-yolov9-e` (line 3) is a supported variant per
`SUPPORTED_DETECT_VERSIONS`. Only-unused key is `task:` (line 6) —
cosmetic, deferred.

## Missed issues (NEW this round)

Round 2's two approved trims (ITEM-AUD-201 README variants, ITEM-AUD-202
detector.py docstring variants) closed the **runtime-crash** cascade
across all surfaces (no copy-pasteable variant string in any
user-discoverable surface will now `ValueError` against PW 1.2.4.2).
But the trims left five **factual / consistency** lag points that
weren't in any prior plan and are direct consequences of the now-shorter
variant list:

| # | Site | Stale text | Now-correct value |
|---|------|------------|-------------------|
| 1 | `README.md:54` | "**efficiency**, **modern architectures**, and **licensing flexibility**" | After trim, all 5 documented variants are AGPL-3.0; "licensing flexibility" has no referent in the trimmed Highlights / Model Variants block. |
| 2 | `README.md:280` | V6.0 row: `2.3M–76M` and `Multiple variants, MIT/Apache options` | 2.3M–58.1M; "AGPL-3.0 only" (MIT/Apache variants no longer in the canonical table). |
| 3 | `README.md:340` | "Individual model weights are released under MIT, Apache-2.0, or AGPL-3.0 — see the [Model Variants](#model-variants) table for per-variant licensing." | Internal contradiction: the link target now only shows AGPL-3.0 rows. |
| 4 | `detector.py:16` | V6 class docstring summary: "ranging from 2.3M to 76M parameters" | 2.3M to 58.1M after the bullet list trim two lines below. |
| 5 | `detector.py:45–46` | V5 docstring's comparative claim: "We recommend V6 for new projects — it is smaller, faster, and offers permissive license options." | "permissive license options" no longer documented for V6 after the trim. |

These are clustered as **2 NEW issues** for the NEW_FINDINGS count (one
per file): (a) README trim-cascade residuals at lines 54/280/340, (b)
detector.py trim-cascade residuals at lines 16/45-46. Neither blocks
running `megadetector detect/train/validate/inference`; both are
user-visible factual inconsistencies.

Round 1 priorities #4–#10 ("Next-round priorities" from
`round_01/inquisitor_review.md`) are NOT being re-raised here — the
auditor's "would the user be unable to run the repo" bar correctly
deferred them and they remain out of scope.

## Cross-impact analysis

**Auditor docs changes vs current code state** — all three round 2 fixes
align with the source-of-truth modules they were meant to mirror:

- README Model Variants table & Python example (post-AUD-201) match
  `cli.py:20–26` `SUPPORTED_DETECT_VERSIONS` and
  `training_utils.get_model_path` whitelist exactly.
- `detector.py` V6 docstring `version=` bullets (post-AUD-202) name
  the same 5; trimmed summary line 16 is the only intra-file lag.
- `docs/training_guide.md:130` (post-AUD-203) `plots:` matches both
  `examples/config_training.yaml:25` (post-REV-001) and
  `training.py:120` `plots=cfg.plots` (post-REV-009).

**Round 1 fixes vs round 2 changes** — no round 1 fix has been
re-opened or contradicted:

- REV-004 (CLI docstring example): `cli.py:7` still uses
  `MDV6-yolov10-e`, a supported variant. Round 2 README now agrees.
- REV-001/REV-009 (`plots` rename): three-site cascade closed after
  AUD-203.
- REV-005 (`SUPPORTED_DETECT_VERSIONS` whitelist): intact at
  `cli.py:20–26`, agrees with README, `detector.py`,
  `training_utils.py`.
- AUD-005/AUD-016/AUD-017 (round 1 docs framing): undisturbed by the
  variant trim — the Highlights / Version-History / License sections
  that acquired residual staleness (above) were touched only by their
  first bullet's removal in round 2; the surrounding claims were
  already there.
- AUD-013/AUD-014 (class-set wording rejection): preserved correctly —
  AUD-202 docstring trim explicitly kept line 14 ("Detects animals,
  people, and vehicles") untouched.

**Reviewer end-to-end re-trace** — both inquisitor spot-checks plus my
own re-trace confirm that `megadetector train --config
examples/config_training.yaml` would resolve cleanly to ultralytics
`model.train(...)` given the current state of the four reviewer-owned
files. Deferred `task:`/sidecar-discard/`cfg.device_*`/download-
hardening items are non-blocking polish. NOTHING-TO-DO accepted.

## Verification results

`round_02/verification.txt` — all clean, no regressions:

- `py_compile` over all Python files: OK.
- `ruff` over the project: "All checks passed!".
- `yaml.safe_load examples/config_training.yaml`: 22 keys, includes
  `plots` (post-REV-001) and `weights` (post-REV-003).
- `environment.yaml` env name: `megadetector-finetuning` (round 1
  fix intact).
- `pyproject.toml`: project URLs all point to public
  `microsoft/MegaDetector` (round 1 fix intact).
- `training_utils.get_model_path` whitelist: the 5 supported variants.
- `megadetector --help` returns the documented subcommand list with
  no import errors.
- README links `docs/training_guide.md` (1 occurrence) and contains
  the Fine-Tuning section (round 1 fix intact).

No expected failures, no regressions, all categories clean.

## Coverage analysis

- Ledger files: 11
- Verified this round: 11
- Cumulative covered (scope_check.sh): 11/11
- Uncovered: []
- action="fixed" entries this round: 3
- NEW issues this round: 2 (two clusters: README cascade
  residuals at lines 54/280/340; detector.py cascade residuals at lines
  16/45-46)

## Next-round priorities (if NEEDS-MORE)

Round 2 produced `action=fixed` entries, so editing-mode convergence
mandates one more round. The new clusters above are the candidate work
for round 3 — strictly cosmetic / factual-consistency, no runtime
impact. Two paths are both protocol-valid:

1. **Conservative close (recommended).** Round 3's auditor judges the
   five residual sites as **deferred editorial consolidation** (the
   exact carve-out used in `round_02/auditor_report.md`'s ITEM-AUD-201
   Why section: "editorial consolidation is out-of-scope") and returns
   `NOTHING-TO-DO`; reviewer also returns `NOTHING-TO-DO`; round 3
   converges.
2. **Tight close.** Round 3's auditor applies a 5-line cascade-cleanup
   PR (lines 54, 280, 340 in README.md; lines 16, 45–46 in
   detector.py — drop "76M", "MIT/Apache options", "permissive license
   options", and reword the "licensing flexibility" framing); reviewer
   returns `NOTHING-TO-DO`; round 4 then converges.

Either is acceptable per the "user-blocking-only" bar that this
audit-fix run has applied throughout. The conservative close is the
lower-cost path to CONVERGED; the tight close removes the last factual
lag points. The round 2 auditor's stated stance ("this should be the
convergence round") and the round 2 inquisitor approvals doc ("If after
round-2 fixes land the inquisitor verifies cleanly and no NEW
user-blocking item surfaces, the lead should declare CONVERGED") both
point at path (1). The two new clusters above are NOT user-blocking —
no command fails, no crash — so path (1) is consistent with that bar.

STATUS: NEEDS-MORE SCOPE_CHECK=PASS COVERED=11/11 UNCOVERED=[] NEW=5
