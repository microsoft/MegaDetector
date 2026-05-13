# Reviewer plan — round 3

## Scope recap
Behavioral findings (bugs, edge cases, error handling, correctness,
validation) confined to the four reviewer-owned files:

- `src/megadetector_ai/training.py`
- `src/megadetector_ai/training_utils.py`
- `src/megadetector_ai/cli.py`
- `examples/config_training.yaml`

## Inputs read
- `~/.copilot/skills/_shared/iterative-anti-drift.md` — protocol.
- `docs/review/audit-fix/SCOPE_LEDGER.json` — 11 ledger files,
  4 reviewer-owned (above).
- `docs/review/audit-fix/COVERAGE_LOG.jsonl` — round 1 reviewer fixed
  ITEM-REV-001/002/003/004/005/006/007/008/009/010 in commit
  `badc1c2`; round 2 reviewer = NOTHING-TO-DO; inquisitor verified all
  4 reviewer-owned files clean in both rounds.
- `docs/review/audit-fix/round_02/inquisitor_review.md` —
  `STATUS: NEEDS-MORE NEW=5`. The 5 NEW findings are doc-consistency
  residuals of round 2's variant-trim cascade, all located in
  **auditor-owned files**:
  - README.md lines 54, 280, 340 (3 sites)
  - src/megadetector_ai/detector.py lines 16, 45–46 (2 sites)

  None of the 5 NEW findings touch a reviewer-owned file. None are
  behavioral — they are factual / editorial doc lag points (stale
  "76M parameters", "MIT/Apache options", "permissive license
  options", "licensing flexibility" framings after round 2 trimmed
  the variant list to 5 AGPL-3.0 entries). The inquisitor's own
  classification: "strictly cosmetic / factual-consistency, no
  runtime impact."

## Re-audit of owned files (round-3 sweep)

Each file re-read top-to-bottom against its round 2 inquisitor verdict
and against the candidate failure modes from rounds 1–2 (variant-
whitelist drift, plots/plot key drift, resume/weights handling, CWD
writability, ultralytics kwarg mismatches, per-image inference error
isolation, argparse `choices=` enforcement). Results:

### training.py
- Variant gating: `_load_model` reads `cfg.resume`, `cfg.weights`,
  `cfg.model`, `cfg.model_name`; cross-validates `YOLO` vs `rtdetr`
  (lines 35–44). Round 1 REV-002/003/006/007 fixes intact.
- `_prepare_data_config` (lines 56–78) opens `cfg.data` read-only,
  writes a sidecar under `runs/_resolved_data/` — never mutates the
  user's YAML. No regression.
- `model.train(...)` kwargs (lines 89–104) map 1:1 to ultralytics
  supported names; `plots=cfg.plots` at line 120 (REV-009) matches
  YAML key `plots:` after REV-001 and doc after AUD-203.
- `inference` per-image try/except with `getattr(results[i], "path",
  ...)` fallback (lines 142–149) — REV-009 fix intact.
- `grep -nE "cfg\.[A-Za-z_]+" training.py` → 21 distinct fields, all
  present in `examples/config_training.yaml`. NOTHING-TO-DO.

### training_utils.py
- 5-branch whitelist for the 5 supported variants (lines 7–22); else
  branch raises `ValueError` naming the same 5 (line 23). Matches
  `cli.py:20–26` `SUPPORTED_DETECT_VERSIONS`. REV-010 CWD-writability
  precheck (lines 27–32) intact: `wget.download` only runs after
  `os.access(".", os.W_OK)` succeeds. NOTHING-TO-DO.

### cli.py
- `SUPPORTED_DETECT_VERSIONS` (lines 20–26) = 5 supported variants;
  used as `choices=` for `--model` (line 191), so argparse rejects
  unsupported variants before any PW call.
- Module docstring example at line 7 uses `MDV6-yolov10-e` —
  supported (REV-004 intact).
- `detect` validates `input_path.exists()` and `is_file()/is_dir()`
  (lines 34–70) — REV-005 intact.
- `train`/`validate`/`inference` wrappers each validate config path,
  then wrap the call in `try/except (ValueError, KeyError,
  AttributeError, FileNotFoundError)` with friendly stderr + exit 1
  (REV-008, lines 119–168). NOTHING-TO-DO.

### examples/config_training.yaml
- 22 keys parse via `yaml.safe_load`; covers every `cfg.<field>` read
  in `training.py`. `plots: True` (line 25, REV-001), `weights: null`
  with explanatory comment (line 21, REV-003), `model_name:
  MDV6-yolov9-e` (supported variant). NOTHING-TO-DO.

## NEW behavioral findings in owned files
None. All 4 owned files remain at their round 2 verified-clean state;
no edits have landed since `badc1c2`. The round 2 inquisitor's 5 NEW
findings are auditor-owned and non-behavioral.

## Cross-Scope Findings (routed to auditor — DO NOT FIX)
Same 5 sites already enumerated by the round 2 inquisitor. Logging
here only for cross-scope visibility:

| # | File              | Line(s) | Stale text                                                  | Why now-stale                                                          |
|---|-------------------|---------|-------------------------------------------------------------|------------------------------------------------------------------------|
| 1 | README.md         | 54      | "**efficiency**, **modern architectures**, and **licensing flexibility**" | All 5 documented variants are AGPL-3.0 post-AUD-201.                   |
| 2 | README.md         | 280     | V6.0 row `2.3M–76M` and `Multiple variants, MIT/Apache options` | Trimmed table max is 58.1M (`MDV6-yolov9-e`); no MIT/Apache rows.      |
| 3 | README.md         | 340     | License footer references `[Model Variants](#model-variants)` for MIT/Apache/AGPL-3.0 | Target section now shows AGPL-3.0 only.                               |
| 4 | detector.py       | 16      | "ranging from 2.3M to 76M parameters" in V6 docstring summary | Trimmed bullet list maxes at 58.1M.                                   |
| 5 | detector.py       | 45-46   | V5 docstring's "V6 ... offers permissive license options"    | No permissive variants in the trimmed enumeration.                    |

All 5 are doc-vs-doc factual consistency lag; none break
`megadetector detect/train/validate/inference`. Disposition decision
(consolidate now in round 3 vs accept the deferred-editorial carve-
out) belongs to the auditor.

## Verification
Owned files unchanged since `badc1c2`; round 2 verification
(`docs/review/audit-fix/round_02/verification.txt`) already passed
end-to-end: `py_compile`, `ruff`, `yaml.safe_load`, `megadetector
--help`, whitelist sync. Nothing for the reviewer to re-verify in
round 3.

STATUS: NOTHING-TO-DO
