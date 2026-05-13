# Round 2 file ownership (same split as round 1)

## Auditor owns
- README.md
- megadetector.md
- pyproject.toml
- environment.yaml
- docs/training_guide.md
- src/megadetector_ai/__init__.py
- src/megadetector_ai/detector.py
- docs/audit_report.md

## Reviewer owns
- src/megadetector_ai/training.py
- src/megadetector_ai/training_utils.py
- src/megadetector_ai/cli.py
- examples/config_training.yaml

## Goal
Round 1 reported `NEW=13` in the inquisitor review. Round 2 must:
1. Read round 1 inquisitor_review.md and identify the NEW issues + their owners
2. Plan fixes for genuine issues, or `STATUS: NOTHING-TO-DO` if the NEW count was inflated by counting fixed items
3. Aim for convergence: zero source changes + zero new findings in this round
