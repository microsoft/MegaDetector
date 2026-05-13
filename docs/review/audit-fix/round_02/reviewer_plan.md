# Reviewer plan — round 2

## Summary

After re-tracing all 4 user-facing CLI commands against the current source
state (HEAD = `0e544df`, reviewer round-1 commit `badc1c2` confirmed landed
via `git show --stat`) and re-checking each round 1 fix:

**End-to-end traces — all clean:**

- `megadetector detect …` → `cli.detect` → `MegaDetectorV6` wrapper →
  `PytorchWildlife`. argparse `choices=SUPPORTED_DETECT_VERSIONS` (cli.py:191)
  is the 5-variant whitelist that matches `training_utils.get_model_path`
  exactly; `_format_detections` CLASS_NAMES `{0: animal, 1: person, 2: vehicle}`
  matches installed PW 1.2.4.2 (inquisitor-verified upstream B7).
- `megadetector train --config …` → `cli.train` (validates `--config` path on
  cli.py:119 BEFORE importing ultralytics) → `training.train` →
  `_load_model` (resume/weights guard + framework↔weights guard) →
  `_prepare_data_config` (sidecar at `runs/_resolved_data/`, no destructive
  rewrite — verified by reading current `training.py:56-78`; only `open()` in
  read mode against `cfg.data`, write goes to `out_path`) → `model.train(
  data=data_path, …)`.
- `megadetector validate --config …` → analogous path; uses `plots=cfg.plots`
  and YAML key is `plots: True`.
- `megadetector inference --config …` → analogous path; per-image
  `try/except Exception` wraps `results[i].save(...)` with `getattr(results[i],
  "path", ...)` fallback.

**`cfg.<field>` ↔ YAML cross-check** (`grep -nE "cfg\.[A-Za-z_]+" training.py`
+ `yaml.safe_load examples/config_training.yaml`):

- All 21 distinct `cfg.X` reads in `training.py` resolve to keys present in
  `examples/config_training.yaml`: `resume, weights, model_name, model, data,
  exp_name, epochs, imgsz, device_train, save_period, workers,
  batch_size_train, optimizer, lr0, val, patience, save_json, plots,
  device_val, batch_size_val, test_data`.
- Only YAML-only-unused key: `task` (line 6). Already tracked as reviewer
  CS-5 / Next-Round Priority 10. Cosmetic — does not block any command.

**Inquisitor "Missed issues" review:**

1. `docs/training_guide.md:125` `Default: None` cascade after REV-003 —
   explicitly tagged "auditor-scope in round 2" by the inquisitor. File not
   in reviewer's scope.
2. `src/megadetector_ai/training_utils.py:23` inline comment for variant
   whitelist — also tagged "auditor-scope in round 2" by the inquisitor.
   File IS in reviewer's owned list, but the proposed change is a one-line
   code comment with **zero behavioral impact**. Reviewer scope per ledger is
   BEHAVIORAL only.

**Bar test — "would the user be unable to run inference or fine-tuning
without this fix?"** Applied to each deferred reviewer-scope priority:

| Priority | Item | Bar cleared? |
|----------|------|--------------|
| 5 | `inference()` ignores `cfg.device_*` | NO — ultralytics auto-detects device; inference still runs |
| 6 | `inference()` calls `_prepare_data_config(cfg)` and discards the return (wasteful sidecar each run) | NO — example config has valid `cfg.data`, sidecar is harmless; no regression from round 1 |
| 7 | `wget.download` lacks retry/checksum/atomic-rename hardening | NO — REV-010 CWD-writability precheck is in place; downloads succeed in normal conditions |
| 10 | YAML `task:` field unread by `training.py` | NO — cosmetic |

No reviewer-scope item clears the round-2 convergence bar (user-facing
inference/fine-tuning would be blocked). All four are polish items correctly
deferred per the round 1 inquisitor's next-round priorities; they are NOT
genuine new round-2 bugs requiring fixes.

## Items

(none)

## Cross-Scope Findings (deferred to round 3 if any)

None new. Pre-existing deferrals already enumerated in round 1's
`inquisitor_review.md` "Next-round priorities" remain auditor-scope:

- README.md:65-75 + README.md:89 V6 variant-list cleanup (auditor).
- docs/training_guide.md:130 `plot:` → `plots:` cascade (auditor).
- docs/training_guide.md:125 `Default: None` → `null` cascade (auditor, NEW
  in round 1 inquisitor review).
- `src/megadetector_ai/training_utils.py:23` inline-comment for variant
  whitelist (inquisitor designated auditor-scope; cosmetic, no behavioral
  impact).
- `src/megadetector_ai/detector.py:22-31` V6 docstring variant-list trim
  (auditor — class-set wording must stay 3-class per AUD-013/014 verdict).

STATUS: NOTHING-TO-DO
