"""
Fine-tuning module for MegaDetector models.

Provides functions to train, validate, and run inference with detection models
using the ultralytics framework.
"""

from ultralytics import YOLO, RTDETR
from megadetector_core.training_utils import get_model_path
from munch import Munch
import yaml
import os


def load_config(config_path: str = './config.yaml') -> Munch:
    """Load configuration from YAML file."""
    with open(config_path) as f:
        cfg = Munch(yaml.load(f, Loader=yaml.FullLoader))
    return cfg


def _load_model(cfg: Munch):
    """Load the appropriate model based on config."""
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

    if cfg.model == "YOLO":
        model = YOLO(model_path)
    elif cfg.model == "RTDETR":
        model = RTDETR(model_path)
    else:
        raise ValueError("Model not supported")

    return model


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


def train(config_path: str = './config.yaml'):
    """Train a detection model with the specified configuration."""
    cfg = load_config(config_path)
    model = _load_model(cfg)
    data_path = _prepare_data_config(cfg)

    model.info()

    results = model.train(
        data=data_path,
        epochs=cfg.epochs,
        imgsz=cfg.imgsz,
        device=cfg.device_train,
        save_period=cfg.save_period,
        workers=cfg.workers,
        batch=cfg.batch_size_train,
        optimizer=cfg.optimizer,
        lr0=cfg.lr0,
        val=cfg.val,
        project=f"runs/train_{cfg.exp_name}",
        name="exp",
        patience=cfg.patience,
        resume=cfg.resume
    )

    return results


def validate(config_path: str = './config.yaml'):
    """Validate a detection model with the specified configuration."""
    cfg = load_config(config_path)
    model = _load_model(cfg)
    data_path = _prepare_data_config(cfg)

    model.info()

    metrics = model.val(
        data=data_path,
        save_json=cfg.save_json,
        plots=cfg.plots,
        device=cfg.device_val,
        project=f'runs/val_{cfg.exp_name}',
        name="exp",
        batch=cfg.batch_size_val
    )

    return metrics


def inference(config_path: str = './config.yaml'):
    """Run inference on test data with the specified configuration."""
    cfg = load_config(config_path)
    model = _load_model(cfg)
    _prepare_data_config(cfg)

    model.info()

    results = model(cfg.test_data)
    save_path = os.path.join("inference_results", cfg.exp_name)
    os.makedirs(save_path, exist_ok=True)

    for i in range(len(results)):
        try:
            results[i].save(filename=os.path.join(save_path, f"inference_{i}.jpg"))
        except Exception as e:
            src = getattr(results[i], "path", f"<index {i}>")
            print(f"Warning: failed to save inference result for {src}: "
                  f"{type(e).__name__}: {e}")
            continue

    return results
