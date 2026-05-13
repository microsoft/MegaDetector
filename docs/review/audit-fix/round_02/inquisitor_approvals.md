# Inquisitor approvals — round 2

## Auditor verdicts

ITEM-AUD-201 | APPROVED — Verified `README.md:65-90` matches plan exactly: 9-row table at lines 67-75, "Best accuracy: MDV6-apa-rtdetr-e" bullet at line 80, "Need MIT license?: MDV6-mit-yolov9-c" bullet at line 83, and the Python example `pw_detection.MegaDetectorV6(version="MDV6-apa-rtdetr-e")` at line 89. The line-89 example is a direct copy-paste-crash: PytorchWildlife 1.2.4.2 raises `ValueError` on the four advertised variants (`apa-rtdetr-*`, `mit-yolov9-*`) because they aren't in the installed package's accepted set. This is the same root cause REV-004 fixed in `cli.py:7` — README is the parallel sibling surface that round 1 didn't cascade into. The recommendation bullets at lines 80/83 push users straight toward the crashing variants. Clears the "would the user be unable to use the repo without this fix" bar: the canonical "Load a specific variant" snippet in the project README crashes verbatim on installed PW. Trim to the 5-variant set already used by `SUPPORTED_DETECT_VERSIONS` (cli.py:20-26), `training_utils.get_model_path`, and the round-1 README Fine-Tuning section — full self-consistency in one file.

ITEM-AUD-202 | APPROVED — Verified `src/megadetector_ai/detector.py:22-31` lists all 9 variants in the V6 docstring `version=` enumeration, with `MDV6-mit-yolov9-c/-e` at lines 28-29 and `MDV6-apa-rtdetr-c/-e` at lines 30-31. Users invoking `help(MegaDetectorV6)` or hovering in an IDE will see these and select one → `ValueError` at instantiation. Same crash class as ITEM-AUD-201, different surface (IDE/REPL vs README copy-paste). The plan correctly preserves the class-set wording at line 14 ("Detects animals, people, and vehicles") — the round-1 AUD-014 rejection verdict stands and was the right call (V6 CLASS_NAMES is identical to V5 in installed PW). This is a docstring-trim only, no class-set rewrite. Clears the bar: an in-tree `help()` output that names crashing arguments is a usability defect, and the fix is a 4-line deletion that brings detector.py into agreement with the other three V6-variant surfaces (cli.py, training_utils.py, README Fine-Tuning section) after ITEM-AUD-201 lands.

ITEM-AUD-203 | APPROVED — Verified `docs/training_guide.md:130` reads `- \`plot\`: Boolean value indicating whether to plot results. Default: True`. Cross-verified that `training.py:120` reads `plots=cfg.plots` and `examples/config_training.yaml:25` is `plots: True` (post-REV-001). The doc is the third site in the `plot:`/`plots:` cascade and currently lies about a key the code reads. A user who hand-writes a config from this doc (rather than `cp`-ing the example) types `plot: True` and hits `AttributeError: 'Namespace' object has no attribute 'plots'` at `megadetector validate` — wrapped by REV-008's friendly handler but with no hint that the key name is wrong. One-character cascade fix (`plot` → `plots`); round 1 inquisitor `Missed issues` and `Cross-impact analysis` both flagged this site as the explicit auditor-round-2 follow-up to REV-001. Clears the bar: doc-vs-code key-name disagreement is correctness, not polish.

## Reviewer verdicts

(reviewer reported STATUS: NOTHING-TO-DO)

Spot-check 1 — `megadetector detect` argparse path:
- `cli.py:20-26` `SUPPORTED_DETECT_VERSIONS = ("MDV6-yolov9-c", "MDV6-yolov9-e", "MDV6-yolov10-c", "MDV6-yolov10-e", "MDV6-rtdetr-c")` — intact, matches the 5-variant whitelist post-REV-005.
- `cli.py:7` docstring example uses `MDV6-yolov10-e` (post-REV-004) — supported variant; no copy-paste crash.

Spot-check 2 — `megadetector validate` config path:
- `training.py:120` reads `plots=cfg.plots` (substantive: confirmed by `grep -n "cfg\.plots\|cfg\.plot\b"` returning exactly one hit, line 120, with `plots`).
- `examples/config_training.yaml:25` is `plots: True` (post-REV-001) and `:21` is `weights: null # Path to .pt to resume from when resume=True` (post-REV-003) — both align with current `training.py`.

No round-1 reviewer fix has regressed. Reviewer's "bar test" table is sound: the four deferred reviewer-scope priorities (inference `cfg.device_*`, sidecar discard, download hardening, unused `task:` field) are all polish — none would prevent a user from running inference or fine-tuning. Reviewer correctly declined to manufacture round-2 work where none clears the convergence bar. Both round-1 fix commits (`e58feca`, `badc1c2`) are present in `git log`; HEAD is `0e544df`. NOTHING-TO-DO accepted.

## Notes

- The three approved auditor items together close the four V6-variant surfaces in the repo (README Fine-Tuning section + README Model Variants + detector.py V6 docstring + cli.py docstring/argparse + training_utils whitelist). After round 2, every user-discoverable enumeration of V6 variants names the same 5 supported by `pytorchwildlife==1.2.4.2`.
- The auditor's deferrals (Zenodo explainer, PW version pin, `tests/` skeleton, `training_utils.py:23` inline comment, `docs/training_guide.md:125` `Default: None` lag, reviewer-scope inference polish) are correctly held back under the round-2 bar. The `weights` doc lag (training_guide.md:125) is mitigated by REV-003's explicit `ValueError("Got: 'None'")` guard, so a user who types the doc-suggested `None` literal gets a clear actionable error on first run — not blocking.
- Stance: this should be the convergence round for the editing phase. If after round-2 fixes land the inquisitor verifies cleanly and no NEW user-blocking item surfaces, the lead should declare CONVERGED. All remaining items in the round-1 "Next-round priorities" list 4-10 are polish or hardening that belong in a follow-on hardening pass, not in audit-fix.
- No new in-scope files discovered this round — ledger remains 11 entries.

STATUS: APPROVALS-DONE
