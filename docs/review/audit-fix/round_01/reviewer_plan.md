# Reviewer plan — round 1

**Focus:** behavioral correctness of the four user-facing commands (`detect`, `train`, `validate`, `inference`). Doc clarity is auditor scope; cross-scope concerns are listed at the bottom for the auditor.

**Files owned:**
- `src/megadetector_ai/training.py`
- `src/megadetector_ai/training_utils.py`
- `src/megadetector_ai/cli.py`
- `examples/config_training.yaml`

**Method:** Traced every `cfg.<field>` reference in `training.py` against the YAML keys in `examples/config_training.yaml`; cross-checked `training_utils.get_model_path` versions against `PytorchWildlife.models.detection.MegaDetectorV6` (read from installed package at `~/.cache/uv/archive-v0/.../PytorchWildlife/models/detection/ultralytics_based/megadetectorv6.py`); verified YAML parse of the example config to confirm bug shapes.

Evidence supporting each finding is inline.

---

## MUST-FIX — these block the documented commands today

<a name="ITEM-REV-001"></a>
### ITEM-REV-001 | `examples/config_training.yaml:25` ↔ `src/megadetector_ai/training.py:89` | rename YAML key `plot` → `plots` | `megadetector validate` crashes immediately

**Evidence.** `training.py:89` reads `cfg.plots`; YAML defines `plot:` (no `s`). Verified:
```
$ python -c "import yaml; cfg = yaml.load(open('examples/config_training.yaml'), Loader=yaml.FullLoader); print('plot' in cfg, 'plots' in cfg)"
True False
```
Munch raises `AttributeError`/`KeyError` on `cfg.plots`. The ultralytics `Model.val()` canonical parameter is `plots=`, so the code reference is correct — fix is in the YAML.

**Fix.** In `examples/config_training.yaml` change line 25 to `plots: True`. (Do NOT touch the auditor-owned `docs/training_guide.md` which also documents the wrong name — list under Cross-Scope.)

---

<a name="ITEM-REV-002"></a>
### ITEM-REV-002 | `src/megadetector_ai/training.py:39-49` | non-destructive resolution of relative `path:` in data YAML | currently mutates the user's data YAML on disk

**Evidence.** `_prepare_data_config` calls `yaml.dump` back to `cfg.data` whenever `data["path"]` is relative. This silently rewrites the user's dataset config file (loses comments, formatting, ordering). It's also a hidden side effect of running `train`/`validate`/`inference`.

**Fix.** Resolve the relative path in-memory and write a sidecar resolved YAML next to a run-scoped scratch location, then re-point `cfg.data` (in-process only) at the sidecar. Concretely:

```python
def _prepare_data_config(cfg: Munch) -> str:
    """Return a path to a data YAML whose `path:` is absolute. Never mutates the user's file."""
    with open(cfg.data) as f:
        data = yaml.safe_load(f)
    if os.path.isabs(data.get("path", "")):
        return cfg.data
    # Resolve relative to the directory holding the original YAML, not CWD.
    base = os.path.dirname(os.path.abspath(cfg.data))
    data["path"] = os.path.normpath(os.path.join(base, data["path"]))
    resolved_dir = os.path.join("runs", "_resolved_data")
    os.makedirs(resolved_dir, exist_ok=True)
    out_path = os.path.join(resolved_dir, f"{cfg.exp_name}_data.yaml")
    with open(out_path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)
    return out_path
```

Then in `train()`/`validate()`/`inference()`:
```python
data_path = _prepare_data_config(cfg)
# ... pass data=data_path to model.train/val
```
And update the `data=cfg.data` references on lines 61, 87 to `data=data_path`.

**Rationale.** Resolves relative to the YAML's own directory (which matches the typical user mental model from `docs/training_guide.md` — `path: path/to/your_data` is alongside the YAML), keeps the user's file untouched, and the sidecar is regenerated each run.

---

<a name="ITEM-REV-003"></a>
### ITEM-REV-003 | `src/megadetector_ai/training.py:22-27` and `examples/config_training.yaml:21` | guard `cfg.resume=True` when `cfg.weights` is missing or the literal string `"None"` | currently bombs with a confusing path-not-found error

**Evidence.** PyYAML 1.1 (the FullLoader default for unquoted `None`) parses `weights: None` as the *string* `'None'`, not Python `None`. Verified:
```
$ python -c "import yaml; print(repr(yaml.load(open('examples/config_training.yaml'), Loader=yaml.FullLoader)['weights']))"
'None'
```
With `cfg.resume=True`, `model_path = cfg.weights == "None"`, then `YOLO("None")` is called — ultralytics treats this as a filename, fails to find it, and emits a misleading error.

**Fix.** In `_load_model`, validate:
```python
if cfg.resume:
    weights = cfg.get("weights") if hasattr(cfg, "get") else cfg.weights
    if weights in (None, "None", "", "null"):
        raise ValueError(
            "cfg.resume=True requires a real `weights:` path in the config (path to a .pt file). "
            "Got: %r" % (weights,)
        )
    model_path = weights
else:
    model_path = get_model_path(cfg.model_name)
```
(Munch supports `.get()` like dict, so the hasattr dance isn't strictly needed — but defensive.)

Also change the example YAML default to a clearer sentinel: leave `weights: null # path to .pt to resume from when resume=True` so YAML 1.1 parses to Python `None` (`null` is the YAML 1.1 token) and the guard reads cleanly.

---

## HIGH — surfaces that advertise features that don't work

<a name="ITEM-REV-004"></a>
### ITEM-REV-004 | `src/megadetector_ai/cli.py:7` (module docstring) | replace example `--model MDV6-apa-rtdetr-e` with a supported variant | example as shipped raises `ValueError` from PyTorch Wildlife

**Evidence.** Read installed `PytorchWildlife.models.detection.MegaDetectorV6.__init__` at `~/.cache/uv/archive-v0/NmuqR_Vp-sUYaNsyKewlK/PytorchWildlife/models/detection/ultralytics_based/megadetectorv6.py:35-51`. The accepted set is exactly `{MDV6-yolov9-c, MDV6-yolov9-e, MDV6-yolov10-c, MDV6-yolov10-e, MDV6-rtdetr-c}`. `MDV6-apa-rtdetr-e` is in the README's "Model Variants" table but the installed `pytorchwildlife==1.2.4.2` does not implement it — calling it raises `ValueError("Select a valid model version: ...")`.

**Fix.** Change the docstring example on line 7 of `cli.py` to `--model MDV6-yolov10-e --threshold 0.2` (or another supported variant). The CLI-level `--model` flag default (`MDV6-yolov9-c`, line 169) is already valid; only the docstring example is wrong.

---

<a name="ITEM-REV-005"></a>
### ITEM-REV-005 | `src/megadetector_ai/cli.py:34-35` (and `src/megadetector_ai/detector.py` docstring — cross-scope flag only) | fail-fast model-version validation in `cli.detect` | currently the bogus version error surfaces from deep inside PyTorch Wildlife after model class instantiation, with a stack trace

**Evidence.** Same as ITEM-REV-004. Today a user typing `megadetector detect --input x --model MDV6-apa-rtdetr-e` gets the PW `ValueError` with a traceback. The 5-variant constraint is enumerated locally already (in `training_utils.get_model_path`), so we can pre-validate.

**Fix.** In `cli.py`, before `MegaDetectorV6(...)`:
```python
SUPPORTED_DETECT_VERSIONS = {
    "MDV6-yolov9-c", "MDV6-yolov9-e",
    "MDV6-yolov10-c", "MDV6-yolov10-e",
    "MDV6-rtdetr-c",
}
if args.model not in SUPPORTED_DETECT_VERSIONS:
    print(
        f"Error: model {args.model!r} is not supported by the installed "
        f"PyTorch Wildlife. Supported: {sorted(SUPPORTED_DETECT_VERSIONS)}",
        file=sys.stderr,
    )
    sys.exit(2)
```
Also restrict argparse `choices=SUPPORTED_DETECT_VERSIONS` on the `--model` argument so help text enumerates the valid set. Argparse will reject unknown values *before* device/torch imports.

---

## MEDIUM — silently-ignored user input

<a name="ITEM-REV-006"></a>
### ITEM-REV-006 | `src/megadetector_ai/training.py:60-73` | pass `cfg.optimizer` and `cfg.lr0` to `model.train(...)` | currently in the example config but silently ignored

**Evidence.** `examples/config_training.yaml` lines 15-16 define `optimizer: auto` and `lr0: 0.01`. `docs/training_guide.md:106-107` documents them as user-tunable. `training.py:60-73` does not forward them. ultralytics `Model.train()` accepts `optimizer=` and `lr0=` directly.

**Fix.** Add to the kwargs of `model.train(...)`:
```python
optimizer=cfg.optimizer,
lr0=cfg.lr0,
```

---

<a name="ITEM-REV-007"></a>
### ITEM-REV-007 | `src/megadetector_ai/training_utils.py:5-31` and `src/megadetector_ai/cli.py` | document/validate framework↔weights consistency | mismatch can produce silent confusion

**Evidence.** `cfg.model` switches between `YOLO` and `RTDETR` (line 29-32 of training.py). `cfg.model_name` selects the URL/weights. Nothing prevents `model: YOLO` + `model_name: MDV6-rtdetr-c` (or vice-versa). Loading rtdetr weights with `YOLO(...)` either fails late in ultralytics or, worse, succeeds with subtly broken behavior depending on the checkpoint metadata.

**Fix.** In `_load_model`, after computing `model_path` but before `YOLO/RTDETR(...)`:
```python
if cfg.model == "YOLO" and "rtdetr" in cfg.model_name.lower():
    raise ValueError(
        f"model='YOLO' is inconsistent with model_name='{cfg.model_name}'. "
        f"Use model='RTDETR' for rtdetr weights."
    )
if cfg.model == "RTDETR" and "rtdetr" not in cfg.model_name.lower():
    raise ValueError(
        f"model='RTDETR' is inconsistent with model_name='{cfg.model_name}'. "
        f"Use model='YOLO' for yolov9/yolov10 weights."
    )
```

---

<a name="ITEM-REV-008"></a>
### ITEM-REV-008 | `src/megadetector_ai/cli.py:105-147` | wrap training-function calls so users get a one-line error, not a raw traceback | currently any AttributeError/ValueError from `training.py` bubbles up as an unfiltered Python traceback

**Evidence.** `cli.train`, `cli.validate`, `cli.inference` call into `training.py` with no `try/except`. For non-developer users running `megadetector validate --config ./config.yaml`, a Python traceback (e.g. `AttributeError: plots` before ITEM-REV-001's fix) is hostile.

**Fix.** Wrap each call:
```python
try:
    results = run_training(config_path)
except (ValueError, KeyError, AttributeError, FileNotFoundError) as e:
    print(f"Error: training failed — {type(e).__name__}: {e}", file=sys.stderr)
    sys.exit(1)
```
Keep tracebacks for unexpected exceptions (catching only the listed types preserves debuggability for actual runtime bugs).

---

## LOW — polish, won't block running but worth noting

<a name="ITEM-REV-009"></a>
### ITEM-REV-009 | `src/megadetector_ai/training.py:99-114` (`inference`) | per-image safety + clearer save path for inference | currently a single corrupt image aborts the whole inference run

**Evidence.** `results = model(cfg.test_data)` returns one `Results` per input. The `for i in range(len(results)):` loop assumes every result is saveable. If a frame is unreadable, ultralytics may emit a placeholder Results that errors on `.save(...)`.

**Fix.** Wrap the per-image save in a per-iteration try/except and continue on failure, logging the failed path. Lower priority than ITEM-REV-001..008.

---

<a name="ITEM-REV-010"></a>
### ITEM-REV-010 | `src/megadetector_ai/training_utils.py:25-29` | `wget.download` writes a temp file into CWD | breaks if CWD isn't writable

**Evidence.** Read `wget==3.2` source at `~/.cache/uv/archive-v0/.../wget.py:506` — `tempfile.mkstemp(".tmp", prefix=prefix, dir=".")`. The download function mkstemps in `.` regardless of the `out=` target. If a user runs `megadetector train` from a read-only directory, the download silently fails. Edge case — note for the user-facing audit but not blocking.

**Fix.** Out of scope to rewrite the download flow this round; flag to user via cross-scope. Minor mitigation: do an explicit `os.makedirs(...)` + `os.access(".", os.W_OK)` precheck in `get_model_path` and emit a clearer error.

---

## Cross-Scope Findings (auditor's report should mention these — DO NOT fix in this round)

- **CS-1.** `docs/training_guide.md:117` documents `plot:` as a validation parameter; after ITEM-REV-001 lands the canonical name is `plots:`. The training guide table needs the same rename.
- **CS-2.** `README.md:65-73` advertises 9 V6 variants but installed `pytorchwildlife==1.2.4.2` exposes only 5. Either downgrade the README claim to match installed PW, or call out in the README that `apa-*` and `mit-*` variants require a newer PW release (and pin a version range in `pyproject.toml`).
- **CS-3.** `docs/training_guide.md:11-15` instructs `pip install -r requirements.txt`, but no `requirements.txt` exists in the repo. `pyproject.toml` covers `ultralytics`, `munch`, `wget`, `PyYAML`, `torch`, `PytorchWildlife` — so `pip install -e .` is the right substitute, and the guide should say so.
- **CS-4.** `src/megadetector_ai/detector.py:22-31` docstring lists all 9 model variants as valid `version=` values for `MegaDetectorV6`, but only the 5 in ITEM-REV-004's evidence work with installed PW. The auditor should trim that docstring to match the supported set (or note it's a forward-looking list).
- **CS-5.** `examples/config_training.yaml` `task:` field is read nowhere in `training.py`. Either remove it or wire it to dispatch between train/validate/inference (which currently is done by the CLI subcommand instead). Recommend documenting that `task:` is informational only — or removing it — for auditor's call.
- **CS-6.** `training_utils.get_model_path` URLs point at Zenodo record `14567879` with filenames like `MDV6b-yolov9c.pt`. PyTorch Wildlife's own V6 fetches from record `15398270` with filenames like `MDV6-yolov9-c.pt`. The fine-tuning weights and the inference weights may differ on purpose, but the README doesn't explain this. Worth a sentence in the training guide.

---

STATUS: PLAN-READY
