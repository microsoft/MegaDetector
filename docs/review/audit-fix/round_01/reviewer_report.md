# Reviewer report — round 1

**Commit:** `badc1c2cdc6b4bb7a761f11d48112ff210b70849`

All 10 reviewer items APPROVED by the inquisitor in round 1. All 10 applied. No items skipped.

Owned files touched:
- `examples/config_training.yaml`
- `src/megadetector_ai/training.py`
- `src/megadetector_ai/training_utils.py`
- `src/megadetector_ai/cli.py`

Sanity checks before commit:
- `python3 -m py_compile` on the three `.py` files: passed.
- `yaml.safe_load(open('examples/config_training.yaml'))` → `weights` parses as Python `None`; `plots` key present (True); `plot` key gone; `optimizer`/`lr0` present.
- AST parse of `cli.py` confirms `SUPPORTED_DETECT_VERSIONS = ('MDV6-yolov9-c', 'MDV6-yolov9-e', 'MDV6-yolov10-c', 'MDV6-yolov10-e', 'MDV6-rtdetr-c')`.

---

## Changes Applied

<a name="ITEM-REV-001"></a>
### ITEM-REV-001 | examples/config_training.yaml:25 | `plot: True` → `plots: True` | unblock `megadetector validate`
Before: `plot: True`
After:  `plots: True`
Why: `training.py:89` reads `cfg.plots`; ultralytics canonical kwarg for `Model.val()` is `plots=`. The YAML key was the wrong side. Without the rename, `megadetector validate` raises `AttributeError` on first access.

---

<a name="ITEM-REV-002"></a>
### ITEM-REV-002 | src/megadetector_ai/training.py:39-49 (now :49-70) and call sites :60,87 | non-destructive `_prepare_data_config` | stop mutating user's source-controlled data YAML
Before:
```python
def _prepare_data_config(cfg: Munch):
    ...
    if not os.path.isabs(data["path"]):
        data["path"] = os.path.abspath(data["path"])
        with open(cfg.data, 'w') as f:
            yaml.dump(data, f)
    return data
```
After:
```python
def _prepare_data_config(cfg: Munch) -> str:
    """Return a path to a data YAML whose `path:` is absolute.

    Never mutates the user's source-controlled data YAML. If the user's YAML
    uses a relative `path:`, it is resolved relative to the directory holding
    that YAML (not CWD) and a sidecar YAML is written under
    ``runs/_resolved_data/`` for the run to consume.
    """
    with open(cfg.data) as f:
        data = yaml.safe_load(f)
    if os.path.isabs(data.get("path", "")):
        return cfg.data
    base = os.path.dirname(os.path.abspath(cfg.data))
    data["path"] = os.path.normpath(os.path.join(base, data["path"]))
    resolved_dir = os.path.join("runs", "_resolved_data")
    os.makedirs(resolved_dir, exist_ok=True)
    out_path = os.path.join(resolved_dir, f"{cfg.exp_name}_data.yaml")
    with open(out_path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)
    return out_path
```
Call-site rewiring:
- `train()`: captures `data_path = _prepare_data_config(cfg)`; passes `data=data_path` to `model.train()` (was `data=cfg.data`).
- `validate()`: same pattern, `data=data_path` to `model.val()` (was `data=cfg.data`).
- `inference()`: calls `_prepare_data_config(cfg)` for the absolute-path side effect on relative YAMLs that the inference pipeline may later need; the return is discarded because `model(cfg.test_data)` consumes `cfg.test_data` directly. (No regression — old code also discarded the return.)

Why: The old function silently rewrote the user's YAML on disk every run, destroying comments and key ordering. Resolving relative to the YAML's own directory (not CWD) matches the mental model in the training guide.

---

<a name="ITEM-REV-003"></a>
### ITEM-REV-003 | src/megadetector_ai/training.py:22-27 + examples/config_training.yaml:21 | guard `cfg.resume=True` with weights validation + YAML default `null` | stop confusing `YOLO("None")` failure
Before (training.py):
```python
if cfg.resume:
    model_path = cfg.weights
else:
    model_path = get_model_path(cfg.model_name)
```
After:
```python
if cfg.resume:
    weights = cfg.get("weights") if hasattr(cfg, "get") else getattr(cfg, "weights", None)
    if weights in (None, "None", "", "null"):
        raise ValueError(
            "cfg.resume=True requires a real `weights:` path in the config "
            "(path to a .pt file). Got: %r" % (weights,)
        )
    model_path = weights
else:
    model_path = get_model_path(cfg.model_name)
```
Before (config YAML line 21): `weights: None # Path to weight to resume training`
After: `weights: null # Path to .pt to resume from when resume=True`
Why: PyYAML's FullLoader parses unquoted `None` as the Python string `'None'`, not Python `None`. `YOLO("None")` then fails as a missing file. YAML 1.1 null sentinel is `null`. The code-level guard also covers users who simply omit `weights:` entirely.

---

<a name="ITEM-REV-004"></a>
### ITEM-REV-004 | src/megadetector_ai/cli.py:7 (docstring) | `MDV6-apa-rtdetr-e` → `MDV6-yolov10-e` | stop shipping a docstring example that crashes
Before: `megadetector detect --input ./images/ --model MDV6-apa-rtdetr-e --threshold 0.2`
After:  `megadetector detect --input ./images/ --model MDV6-yolov10-e --threshold 0.2`
Why: Installed `PytorchWildlife==1.2.4.2` `MegaDetectorV6` accepts exactly `{MDV6-yolov9-c, MDV6-yolov9-e, MDV6-yolov10-c, MDV6-yolov10-e, MDV6-rtdetr-c}`. `MDV6-apa-rtdetr-e` raises `ValueError` from PW.

---

<a name="ITEM-REV-005"></a>
### ITEM-REV-005 | src/megadetector_ai/cli.py:14-26 + 170-175 | argparse `choices=` for `--model` | fail-fast on bogus model versions before any heavy import
Added module-level constant:
```python
SUPPORTED_DETECT_VERSIONS = (
    "MDV6-yolov9-c", "MDV6-yolov9-e",
    "MDV6-yolov10-c", "MDV6-yolov10-e",
    "MDV6-rtdetr-c",
)
```
Updated argparse:
```python
detect_parser.add_argument(
    "--model", "-m", default="MDV6-yolov9-c",
    choices=SUPPORTED_DETECT_VERSIONS,
    help="Model variant (default: MDV6-yolov9-c). "
         f"Supported: {', '.join(SUPPORTED_DETECT_VERSIONS)}",
)
```
Why: argparse rejects invalid values before any `torch`/`PytorchWildlife` import, replacing a deep stack trace with a clear one-line error and `--help`-visible enumeration.

---

<a name="ITEM-REV-006"></a>
### ITEM-REV-006 | src/megadetector_ai/training.py:60-73 (now `train()` kwargs) | forward `cfg.optimizer` and `cfg.lr0` | stop silently ignoring documented user knobs
Before: `model.train(...)` did not pass `optimizer=` or `lr0=`.
After: added `optimizer=cfg.optimizer, lr0=cfg.lr0,` to the kwargs.
Why: `examples/config_training.yaml:15-16` defines `optimizer: auto` and `lr0: 0.01`; `docs/training_guide.md:106-107` advertises them as tunable. They were unwired — silent config drop is a correctness issue.

---

<a name="ITEM-REV-007"></a>
### ITEM-REV-007 | src/megadetector_ai/training.py `_load_model` | framework↔weights consistency check | stop allowing YOLO-class + rtdetr-weights mismatches
Added (after `model_path = get_model_path(cfg.model_name)`):
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
Placement note: the check runs *after* `model_name` validation (via `get_model_path`), so users with a bogus `model_name` see the version-list error first — matches the inquisitor's note on ordering.

---

<a name="ITEM-REV-008"></a>
### ITEM-REV-008 | src/megadetector_ai/cli.py train/validate/inference | wrap `run_training/_validation/_inference` calls | one-line user errors instead of raw tracebacks
Before: bare `results = run_training(config_path)`.
After (each of the three subcommands):
```python
try:
    results = run_training(config_path)
except (ValueError, KeyError, AttributeError, FileNotFoundError) as e:
    print(f"Error: training failed — {type(e).__name__}: {e}", file=sys.stderr)
    sys.exit(1)
```
Why: covers Munch `AttributeError`, missing YAML keys, bad paths, ultralytics version validation. Anything outside this set (`RuntimeError`, CUDA OOM, etc.) still raises with a full traceback — debuggability preserved for genuine runtime bugs.

---

<a name="ITEM-REV-009"></a>
### ITEM-REV-009 | src/megadetector_ai/training.py inference save loop | per-image try/except | one bad frame no longer aborts the run
Before:
```python
for i in range(len(results)):
    results[i].save(filename=os.path.join(save_path, f"inference_{i}.jpg"))
```
After:
```python
for i in range(len(results)):
    try:
        results[i].save(filename=os.path.join(save_path, f"inference_{i}.jpg"))
    except Exception as e:
        src = getattr(results[i], "path", f"<index {i}>")
        print(f"Warning: failed to save inference result for {src}: "
              f"{type(e).__name__}: {e}")
        continue
```
Why: an unreadable input image historically aborts the whole batch. Per-iteration isolation plus a warn-and-continue keeps the run alive.

---

<a name="ITEM-REV-010"></a>
### ITEM-REV-010 | src/megadetector_ai/training_utils.py:25-27 | CWD-writability precheck before `wget.download` | clearer error when run from read-only dir
Added before `wget.download(...)`:
```python
if not os.access(".", os.W_OK):
    raise PermissionError(
        "wget.download() requires a writable current working directory "
        "(it creates a temp file in CWD). CWD %r is not writable. "
        "Re-run from a writable directory." % os.getcwd()
    )
```
Why: `wget==3.2` `tempfile.mkstemp(..., dir=".")` writes its scratch file into CWD regardless of `out=`. A user running `megadetector train` from a read-only directory used to fail deep inside `wget.download` with an opaque tempfile error.

---

## Tests Added/Updated
n/a — this repo has no test infrastructure (no `tests/` directory, no `pytest`/`unittest` invocations in `pyproject.toml`, no CI workflow that runs tests). Flagging this as a **Cross-Scope Finding** for the auditor in round 2 (see below).

## Cross-Scope Findings (for auditor in round 2)

- **CS-RF-1 (test infra missing).** No test framework, no `tests/` dir, no CI. Round-1 fixes are validated only by `python3 -m py_compile` and YAML parse. The auditor should consider creating a minimal `tests/` skeleton with at least: (a) a parse-and-resolve unit test for `_prepare_data_config` covering both abs and relative `path:`, (b) an argparse smoke test for `cli.detect` covering valid+invalid `--model` values, (c) a YAML round-trip test confirming `examples/config_training.yaml` parses with `weights is None` and `plots is True`. This is an auditor-scope addition (new files, structural). All three tests are deterministic and don't require GPU or downloaded weights.
- **CS-RF-2 (docs cascade — `plot` → `plots`).** `docs/training_guide.md:117` still documents `plot:` after this round's YAML rename. Auditor round 2.
- **CS-RF-3 (docs cascade — model variants).** `README.md:65-73` advertises 9 V6 variants but installed `pytorchwildlife==1.2.4.2` exposes only the 5 enumerated in `SUPPORTED_DETECT_VERSIONS`. Either trim the README to the 5 supported variants, or note the others require a newer PW release and pin a version range in `pyproject.toml`. Auditor round 2.
- **CS-RF-4 (docs cascade — detector.py V6 docstring).** `src/megadetector_ai/detector.py` V6 docstring lists 9 variants in its `version=` enumeration; only 5 work with installed PW. Trim the variant list only — class-set wording ("animals, people, and vehicles") must remain per inquisitor cross-check (a). Auditor round 2.
- **CS-RF-5 (`task:` field unused).** `examples/config_training.yaml` `task:` is read nowhere in `training.py`; dispatch is via the CLI subcommand. Either remove the key from the example config or document it as informational. Reviewer-owned for round 2; flagging here so the auditor can call it out in the audit_report.md if user-facing.
- **CS-RF-6 (Zenodo record divergence).** `training_utils.get_model_path` URLs point at Zenodo record `14567879` (filenames like `MDV6b-yolov9c.pt`); PyTorch Wildlife's own V6 fetches from record `15398270` (filenames like `MDV6-yolov9-c.pt`). The fine-tuning weights may legitimately differ from inference weights — but this should be documented somewhere in `docs/training_guide.md`. Auditor round 2.
- **CS-RF-7 (auditor B3 — `inference()` ignores `cfg.device_*`).** Deferred from round 1 per inquisitor note. `training.py:inference()` does not pass `device=cfg.device_val` (or similar) to `model(cfg.test_data)`. Reviewer should pick this up in round 2 — flagging now so it's not lost.
- **CS-RF-8 (auditor B8 — `MDV6-yolov10-c` URL filename mismatch).** Deferred from round 1. `training_utils.py:14` maps `MDV6-yolov10-c` → `MDV6-yolov10n.pt` (nano), but the variant name says "compact". Either rename the variant key or clarify in the URL/filename. Reviewer round 2.
- **CS-RF-9 (atomic-rename + checksum for download).** ITEM-REV-010 only added a precheck. Full hardening — atomic rename of partial downloads, SHA256 checksum verification — is a round-2 item. Reviewer-owned but worth coordinating with the auditor since checksums need to be sourced/documented.

## Skipped
None. All 10 reviewer items APPROVED by the inquisitor; all 10 applied.

---

STATUS: DONE COMMIT=badc1c2cdc6b4bb7a761f11d48112ff210b70849
