# Auditor plan — round 2

After re-reading round 1's `inquisitor_review.md` and re-verifying each
owned file, three user-blocking inconsistencies remain in auditor scope.
All three are duplicated-antipattern sites that round 1 resolved in
reviewer-owned files (REV-001, REV-004) but did not cascade into the
auditor-owned docs / docstrings. Fixing them brings the four V6-variant
surfaces in the repo into agreement and matches the new README
Fine-Tuning section (5 PW-1.2.4.2-supported variants).

Convergence stance: these three items eliminate copy-paste crashes and
direct doc-vs-code key-name mismatches. Round 1 priorities #4–#10 from
the inquisitor (training_utils inline comment, Zenodo explainer, tests
skeleton, etc.) are deliberately NOT proposed — they are nice-to-haves
that do not block use of the repo and would prolong the audit.

Out-of-scope-for-this-round (deliberately skipped, with rationale):

- `docs/training_guide.md:125` (`weights: ... Default: None`) — round 1
  REV-003's `_load_model` guard now raises a clear `ValueError` naming the
  exact offending value (`Got: 'None'`). Misleading doc, but the user gets
  a clear, actionable error on first run — not blocking.
- `docs/audit_report.md` — round-1 deliverable, framed as a round-1
  snapshot. The "Findings: Runtime Bugs" table accurately reflects that
  REV-001..010 were applied in round 1's reviewer commit `badc1c2`. No
  update needed at PLAN phase.
- `pyproject.toml` PW pin / `tests/` skeleton / Zenodo explainer / inline
  whitelist comment in `training_utils.py` — listed in round 1's
  "Next-round priorities" but all fall under nice-to-have polish, not
  user-blocking. The convergence rule favors stopping here.

## Items

<a name="ITEM-AUD-201"></a>
**ITEM-AUD-201** | `README.md:65-90` (Model Variants table + "Which should I use?" bullets + Python example) | Trim the 9-row V6 Model Variants table to the 5 variants installed `pytorchwildlife==1.2.4.2` actually exposes (drop `MDV6-apa-rtdetr-e`, `MDV6-apa-rtdetr-c`, `MDV6-mit-yolov9-e`, `MDV6-mit-yolov9-c`); replace the `MDV6-apa-rtdetr-e` and `MDV6-mit-yolov9-c` recommendations at lines 80 and 83 with supported variants (`MDV6-yolov10-e` for best accuracy / `MDV6-yolov10-c` for laptops kept; the "MIT license?" bullet is removed because no MIT-licensed variant ships with PW 1.2.4.2); and change the Python example at line 89 from `version="MDV6-apa-rtdetr-e"` to `version="MDV6-yolov10-e"`. Also drop "MIT and" from the "Permissive licenses" highlight at line 60 (the supported 5 are all AGPL-3.0; Apache-2.0 line preserved only if any apa-* variant is kept — for the conservative trim it goes too). | **Rationale (round 1 inquisitor §"Pre-existing residual issues" items 1+2, §"Next-round priorities" #1):** the Python example at line 89 is the EXACT duplicated antipattern that REV-004 fixed in `cli.py:7` — copy-paste produces `ValueError` from PytorchWildlife. Inquisitor noted: _"Line 89 code example `pw_detection.MegaDetectorV6(version="MDV6-apa-rtdetr-e")` will crash on first run against installed PW — same root cause as REV-004"_. The recommendations at lines 80/83 are the same antipattern (user reads "Best accuracy: MDV6-apa-rtdetr-e" → types it → crashes). Verified the 5 PW-1.2.4.2 variants against `cli.py`'s `SUPPORTED_DETECT_VERSIONS` tuple (lines 20-26) and `training_utils.get_model_path`'s whitelist — both match. This brings the README Model Variants table into agreement with the round-1 Fine-Tuning section (lines 265-271) which already lists exactly these 5.

<a name="ITEM-AUD-202"></a>
**ITEM-AUD-202** | `src/megadetector_ai/detector.py:22-31` (V6 docstring `version=` enumeration) | Remove the four trailing bullet lines (`MDV6-mit-yolov9-c`, `MDV6-mit-yolov9-e`, `MDV6-apa-rtdetr-c`, `MDV6-apa-rtdetr-e`), leaving the 5-bullet list that matches installed PW. Class-set wording in the preceding paragraph (lines 14-15: "Detects animals, people, and vehicles…") MUST remain — round 1's AUD-014 rejection verdict stands. This is a docstring trim only, not a class-set rewrite. | **Rationale (round 1 inquisitor §"src-megadetector-ai-detector-py" + §"Next-round priorities" #1; reviewer's CS-RF-4):** users calling `help(MegaDetectorV6)` or hovering in an IDE see the 9-bullet list and may pick `MDV6-apa-rtdetr-e` from it, then hit `ValueError` at instantiation. Same crash, different surface. Inquisitor: _"V6 docstring at lines 12-15 unchanged (AUD-014 rejected — same root reason as AUD-013). Residual issues (deferred): Lines 22-31 V6 docstring `version=` enumeration still lists 9 variants. Only the 5 in `SUPPORTED_DETECT_VERSIONS` actually work with installed PW. Reviewer CS-4 — auditor round-2 work. The class-set wording at line 14 ('animals, people, and vehicles') must stay per the AUD-013/014 verdict; only the variant list needs trimming."_

<a name="ITEM-AUD-203"></a>
**ITEM-AUD-203** | `docs/training_guide.md:130` (Validation Parameters section) | Replace `- \`plot\`: Boolean value indicating whether to plot results. Default: True` with `- \`plots\`: Boolean value indicating whether to plot results. Default: True`. One-character cascade fix. | **Rationale (round 1 reviewer CS-RF-2 / CS-1, round 1 inquisitor §"docs-training-guide-md" + §"Cross-impact analysis"):** reviewer renamed the YAML key `plot:` → `plots:` in `examples/config_training.yaml:25` (REV-001) and `training.py:120` reads `cfg.plots`. The third site — this doc — still documents the old name. A user who follows the doc and adds `plot: True` to a hand-written config (instead of copying `examples/config_training.yaml`) hits `AttributeError` on `cfg.plots` at `megadetector validate` (wrapped by REV-008's friendly handler, but with no hint about the wrong key). The doc currently lies about a key the code reads — direct auditor-scope correctness issue.

## Cross-Scope Findings (deferred / referenced only)

These were re-verified during round 2 spot-checks but are NOT
proposed for round 2 fixing — they remain valid round-3+ candidates or
are explicitly waved off by the convergence rule.

- **Reviewer scope, deferred:** `training.py:134` `inference()` still calls
  `_prepare_data_config(cfg)` and discards the return (writes an unused
  sidecar YAML each run); `inference()` ignores `cfg.device_*`; download
  hardening (atomic rename + checksum); `task:` field unused in
  `config_training.yaml`. All flagged in round 1, none user-blocking.
- **Auditor scope, deferred:** `training_guide.md:125` `Default: None` →
  `null` (clear runtime error covers it, see preamble above); Zenodo
  14567879 vs 15398270 sentence (informational); `pyproject.toml` PW
  version pin (would belong with a maintainer-level decision about the
  9-variant table — out of scope for the conservative trim in
  ITEM-AUD-201); `tests/` skeleton (structural addition, not blocking).

STATUS: PLAN-READY
