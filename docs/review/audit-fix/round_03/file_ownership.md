# Round 3 file ownership

Round 3 goal: address the 2 NEW findings raised by round 2's inquisitor review and (if no other concerns remain) converge.

Both editors must read `docs/review/audit-fix/round_02/inquisitor_review.md` first — that file lists 3 applied fixes + 2 NEW findings. The 2 NEW findings determine ownership:
- If a NEW finding is structural (docs/wording/dead code/duplication) → goes to auditor's owned files
- If a NEW finding is behavioral (bug/edge case/error handling) → goes to reviewer's owned files

If both editors find their scope NOTHING-TO-DO, round 3 converges.

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
