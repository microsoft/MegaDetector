"""
MegaDetector: AI-powered wildlife detection for camera trap images.

This package provides a simplified interface to MegaDetector models
via PyTorch Wildlife. MegaDetector detects animals, people, and vehicles
in camera trap images.

Quick start:
    >>> from megadetector_core import MegaDetectorV6
    >>> model = MegaDetectorV6()
    >>> results = model.single_image_detection("image.jpg")

For more information, visit https://github.com/microsoft/MegaDetector
"""

__version__ = "0.1.0"

from megadetector_core.detector import MegaDetectorV6, MegaDetectorV5

__all__ = ["MegaDetectorV6", "MegaDetectorV5"]
