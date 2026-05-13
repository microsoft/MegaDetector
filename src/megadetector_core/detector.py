"""
Convenience wrappers around PyTorch Wildlife's MegaDetector models.

These classes provide a simplified import path and sensible defaults
for common MegaDetector workflows.
"""

from PytorchWildlife.models import detection as pw_detection


class MegaDetectorV6(pw_detection.MegaDetectorV6):
    """MegaDetector V6 — the latest generation of MegaDetector.

    Detects animals, people, and vehicles in camera trap images using
    modern architectures (YOLOv9, YOLOv10, RT-DETR). Multiple model
    variants are available, ranging from 2.3M to 58.1M parameters.

    Args:
        device: Device to run on. "cuda:0" for GPU, "cpu" for CPU,
            "mps" for Apple Silicon. Defaults to CUDA if available.
        pretrained: Whether to download pretrained weights. Default True.
        version: Model variant to load. Options:
            - "MDV6-yolov9-c" (default) — compact YOLOv9
            - "MDV6-yolov9-e" — extra-large YOLOv9
            - "MDV6-yolov10-c" — compact YOLOv10 (2.3M params)
            - "MDV6-yolov10-e" — extra-large YOLOv10
            - "MDV6-rtdetr-c" — compact RT-DETR

    Example:
        >>> from megadetector_core import MegaDetectorV6
        >>> model = MegaDetectorV6()
        >>> results = model.single_image_detection("photo.jpg")
        >>> print(results["detections"])
    """
    pass


class MegaDetectorV5(pw_detection.MegaDetectorV5):
    """MegaDetector V5 — the previous generation, based on YOLOv5.

    MegaDetectorV5 detects three classes: animals (class 0), people
    (class 1), and vehicles (class 2).

    Still available for backward compatibility. We recommend V6 for
    new projects — it is smaller and faster.

    Args:
        device: Device to run on. Default: CUDA if available.
        pretrained: Whether to download pretrained weights. Default True.
        version: "a" (default, recommended) or "b".

    Example:
        >>> from megadetector_core import MegaDetectorV5
        >>> model = MegaDetectorV5(version="a")
        >>> results = model.single_image_detection("photo.jpg")
    """
    pass
