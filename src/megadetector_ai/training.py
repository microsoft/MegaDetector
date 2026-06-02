"""
Fine-tuning module for MegaDetector models.

Provides functions to train, validate, and run inference with detection models
using the ultralytics framework.
"""

from ultralytics import YOLO, RTDETR
from megadetector_ai.training_utils import get_model_path
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
        model_path = cfg.weights
    else:
        model_path = get_model_path(cfg.model_name)

    if cfg.model == "YOLO":
        model = YOLO(model_path)
    elif cfg.model == "RTDETR":
        model = RTDETR(model_path)
    else:
        raise ValueError("Model not supported")

    return model


def _prepare_data_config(cfg: Munch):
    """Ensure data config paths are absolute."""
    with open(cfg.data) as f:
        data = yaml.safe_load(f)

    if not os.path.isabs(data["path"]):
        data["path"] = os.path.abspath(data["path"])
        with open(cfg.data, 'w') as f:
            yaml.dump(data, f)

    return data


def train(config_path: str = './config.yaml'):
    """Train a detection model with the specified configuration."""
    cfg = load_config(config_path)
    model = _load_model(cfg)
    _prepare_data_config(cfg)

    model.info()

    results = model.train(
        data=cfg.data,
        epochs=cfg.epochs,
        imgsz=cfg.imgsz,
        device=cfg.device_train,
        save_period=cfg.save_period,
        workers=cfg.workers,
        batch=cfg.batch_size_train,
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
    _prepare_data_config(cfg)

    model.info()

    metrics = model.val(
        data=cfg.data,
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
        results[i].save(filename=os.path.join(save_path, f"inference_{i}.jpg"))

    return results
