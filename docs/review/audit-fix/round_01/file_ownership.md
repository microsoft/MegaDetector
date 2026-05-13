# Round 1 file ownership

## Auditor owns (structural — docs clarity, README fine-tuning section, naming, dead code, URL consistency)
- README.md
- megadetector.md
- pyproject.toml
- environment.yaml
- docs/training_guide.md
- src/megadetector_ai/__init__.py
- src/megadetector_ai/detector.py

## Auditor also creates this deliverable file
- docs/audit_report.md  (user-facing audit report — NEW FILE)

## Reviewer owns (behavioral — runtime bugs, config-key mismatches, error handling, missing variants)
- src/megadetector_ai/training.py
- src/megadetector_ai/training_utils.py
- src/megadetector_ai/cli.py
- examples/config_training.yaml
