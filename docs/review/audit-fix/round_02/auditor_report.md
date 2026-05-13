# Auditor report — round 2

All three approved items (`ITEM-AUD-201`, `ITEM-AUD-202`, `ITEM-AUD-203`)
were applied in a single commit. After this commit, every user-discoverable
V6-variant enumeration in the repo — README Model Variants table, README
Fine-Tuning section, README Python example, `detector.py` V6 docstring,
`cli.py` argparse `choices=` whitelist, `cli.py` docstring example, and
`training_utils.get_model_path` whitelist — names the same 5 variants that
`pytorchwildlife==1.2.4.2` actually accepts. The fourth fix closes the
`plot`/`plots` cascade started by REV-001 (config example) and continued
through REV-009 (`training.py:120` reads `cfg.plots`).

Commit: `b709a15502b0e3fcfea5504e6f150f0234261e81`
Files touched (3): `README.md`, `src/megadetector_ai/detector.py`,
`docs/training_guide.md`. Net diff: 3 insertions, 13 deletions.

## Changes Applied

<a name="ITEM-AUD-201"></a>
### ITEM-AUD-201 — README.md: trim V6 variants table, recommendations, and Python example to the 5 PW 1.2.4.2-supported variants

**Before** (lines 60, 65–90):

```
- **Permissive licenses**: MIT and Apache-2.0 options alongside AGPL-3.0
...
| MDV6-apa-rtdetr-e | 76M | 82.9% | 94.1% | Apache-2.0 |
| MDV6-yolov10-e | 29.5M | 82.8% | 92.8% | AGPL-3.0 |
| MDV6-yolov9-e | 58.1M | 82.1% | 88.6% | AGPL-3.0 |
| MDV6-rtdetr-c | 31.9M | 81.6% | 89.9% | AGPL-3.0 |
| MDV6-apa-rtdetr-c | 20M | 81.1% | 91.0% | Apache-2.0 |
| MDV6-yolov9-c | 25.5M | 78.4% | 87.9% | AGPL-3.0 |
| MDV6-yolov10-c | 2.3M | 76.8% | 87.2% | AGPL-3.0 |
| MDV6-mit-yolov9-e | 51M | 76.1% | 71.5% | MIT |
| MDV6-mit-yolov9-c | 9.7M | 74.8% | 87.6% | MIT |
...
**Which should I use?**
- **Best accuracy**: MDV6-apa-rtdetr-e (82.9% recall, Apache-2.0)
- **Best for laptops/edge**: MDV6-yolov10-c (2.3M params, runs on CPU)
- **Best balance**: MDV6-yolov10-e (29.5M params, 82.8% recall)
- **Need MIT license?**: MDV6-mit-yolov9-c

model = pw_detection.MegaDetectorV6(version="MDV6-apa-rtdetr-e")
```

**After** (lines 58–83 in the new file):

```
- **50x smaller**: ...
- **Multiple architectures**: YOLOv9, YOLOv10, RT-DETR — pick the one that fits your hardware
- **Ongoing fine-tuning**: ...

### Model Variants

| Model | Params | Animal Recall | mAP50 | License |
| --- | --- | --- | --- | --- |
| MDV6-yolov10-e | 29.5M | 82.8% | 92.8% | AGPL-3.0 |
| MDV6-yolov9-e | 58.1M | 82.1% | 88.6% | AGPL-3.0 |
| MDV6-rtdetr-c | 31.9M | 81.6% | 89.9% | AGPL-3.0 |
| MDV6-yolov9-c | 25.5M | 78.4% | 87.9% | AGPL-3.0 |
| MDV6-yolov10-c | 2.3M | 76.8% | 87.2% | AGPL-3.0 |

**Which should I use?**
- **Best accuracy**: MDV6-yolov10-e (82.8% recall, AGPL-3.0)
- **Best for laptops/edge**: MDV6-yolov10-c (2.3M params, runs on CPU)
- **Best balance**: MDV6-yolov10-e (29.5M params, 82.8% recall)

model = pw_detection.MegaDetectorV6(version="MDV6-yolov10-e")
```

**Why:** The previous canonical "Load a specific variant" snippet at line 89
crashed verbatim on installed PW 1.2.4.2 with `ValueError` — the exact
duplicated antipattern REV-004 fixed in `cli.py:7` for the CLI docstring.
The Best-accuracy bullet at line 80 and the MIT-license bullet at line 83
were the same trap on adjacent surfaces (user reads "Best accuracy:
MDV6-apa-rtdetr-e" → types it → crash). All four unsupported rows
(`apa-rtdetr-{e,c}`, `mit-yolov9-{e,c}`) deleted from the table to match
`SUPPORTED_DETECT_VERSIONS` in `cli.py:20-26` and `training_utils.get_model_path`'s
whitelist. The "Permissive licenses" highlight at line 60 also dropped:
no MIT-licensed variant ships with PW 1.2.4.2 and the conservative trim
removes both Apache-2.0 variants too, so all 5 remaining variants are
AGPL-3.0 — the bullet no longer says anything true. The "Best balance"
bullet now coincides with "Best accuracy" (both `MDV6-yolov10-e`) — a
minor cosmetic redundancy preserved per the plan's literal instructions;
editorial consolidation is out-of-scope for round 2.

<a name="ITEM-AUD-202"></a>
### ITEM-AUD-202 — detector.py: trim V6 docstring `version=` enumeration to the 5 supported variants

**Before** (lines 22–31):

```python
        version: Model variant to load. Options:
            - "MDV6-yolov9-c" (default) — compact YOLOv9
            - "MDV6-yolov9-e" — extra-large YOLOv9
            - "MDV6-yolov10-c" — compact YOLOv10 (2.3M params)
            - "MDV6-yolov10-e" — extra-large YOLOv10
            - "MDV6-rtdetr-c" — compact RT-DETR
            - "MDV6-mit-yolov9-c" — MIT-licensed compact
            - "MDV6-mit-yolov9-e" — MIT-licensed extra
            - "MDV6-apa-rtdetr-c" — Apache-licensed compact
            - "MDV6-apa-rtdetr-e" — Apache-licensed extra (best accuracy)
```

**After** (lines 22–27 in the new file):

```python
        version: Model variant to load. Options:
            - "MDV6-yolov9-c" (default) — compact YOLOv9
            - "MDV6-yolov9-e" — extra-large YOLOv9
            - "MDV6-yolov10-c" — compact YOLOv10 (2.3M params)
            - "MDV6-yolov10-e" — extra-large YOLOv10
            - "MDV6-rtdetr-c" — compact RT-DETR
```

**Why:** Users running `help(MegaDetectorV6)` or hovering on the class in an
IDE saw the four trailing bullets and would pick one (e.g. the
"(best accuracy)" annotation on `apa-rtdetr-e` is an explicit lure), then
hit `ValueError` at instantiation. Same crash class as ITEM-AUD-201,
different surface (REPL / IDE tooltip vs. README copy-paste). 4-line
deletion only; the class-set wording at line 14 ("Detects animals, people,
and vehicles") is preserved verbatim per the round-1 AUD-014 rejection
verdict — V6's `CLASS_NAMES` in installed PW is identical to V5's, so the
"animal/person/vehicle" framing remains correct.

<a name="ITEM-AUD-203"></a>
### ITEM-AUD-203 — training_guide.md: rename `plot` → `plots` in Validation Parameters list

**Before** (line 130):

```
- `plot`: Boolean value indicating whether to plot results. Default: True
```

**After** (line 130):

```
- `plots`: Boolean value indicating whether to plot results. Default: True
```

**Why:** Reviewer renamed the YAML key in REV-001 (`examples/config_training.yaml:25`
became `plots: True`) and `training.py:120` reads `plots=cfg.plots`. This doc
was the third site in the cascade and still documented the obsolete `plot:`
spelling. A user hand-writing a config from this doc (instead of `cp`-ing
the example) would type `plot: True`, then hit `AttributeError: 'Namespace'
object has no attribute 'plots'` at `megadetector validate` — wrapped by
REV-008's friendly handler but with no hint that the key name is wrong.
Doc-vs-code key-name disagreement is a correctness defect, not polish.
One-character fix (`plot` → `plots`).

## Tests Added/Updated

n/a — all three items are documentation/docstring edits in surfaces that
have no test coverage in this repo (no `tests/` directory exists; round 1
inquisitor flagged the missing test skeleton as a deferred priority).
Verification is by direct read of the post-commit files against the
already-passing whitelist sources of truth (`cli.py` `SUPPORTED_DETECT_VERSIONS`
and `training.py:120` `cfg.plots`).

## Cross-Scope Findings

None new this round. The deferrals catalogued in `auditor_plan.md` §"Cross-Scope
Findings (deferred / referenced only)" stand unchanged: reviewer-scope inference
polish (`cfg.device_*`, sidecar discard, download hardening, unused `task:`
field) and auditor-scope polish (`training_guide.md:125` `Default: None`,
Zenodo 14567879 vs 15398270 explainer, `pyproject.toml` PW version pin,
`tests/` skeleton, `training_utils.py:23` inline whitelist comment) all
remain under the round-2 convergence bar — none would prevent a user from
running detection or fine-tuning.

## Skipped

None — all three approved items applied as proposed.

STATUS: DONE COMMIT=b709a15502b0e3fcfea5504e6f150f0234261e81
