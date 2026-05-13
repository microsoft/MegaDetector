# Round 4 file ownership

Round 4 goal: confirm no remaining issues; both editors should report NOTHING-TO-DO so the inquisitor can converge.

Both editors MUST read `docs/review/audit-fix/round_03/inquisitor_review.md` first. Round 3 verdict: NEEDS-MORE NEW=2 — where NEW=2 was the 2 round-3 applied fixes (NEW_FINDINGS=0). No genuinely new issues remain.

## Auditor owns (structural)
- README.md
- megadetector.md
- pyproject.toml
- environment.yaml
- docs/training_guide.md
- src/megadetector_ai/detector.py
- docs/audit_report.md

## Reviewer owns (behavioral)
- src/megadetector_ai/training.py
- src/megadetector_ai/training_utils.py
- src/megadetector_ai/cli.py
- examples/config_training.yaml
