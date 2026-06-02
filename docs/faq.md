---
description: "MegaDetector FAQ — frequently asked questions about installation, accuracy, GPU requirements, V5 vs V6, licensing, and how to use MegaDetector for camera-trap wildlife detection."
tags:
  - MegaDetector FAQ
  - MegaDetector how to
  - camera trap AI questions
  - MegaDetector accuracy
  - MegaDetector license
  - V5 vs V6
---

# Frequently Asked Questions

## What is MegaDetector?

MegaDetector is an open-source AI model from the [Microsoft AI for Good Lab](https://www.microsoft.com/en-us/ai/ai-for-good) that detects animals, people, and vehicles in camera-trap images. It draws bounding boxes around detected objects and assigns a confidence score between 0 and 1.

MegaDetector is a **detector**, not a classifier — it tells you *something is there*, not what species it is. This design choice is intentional: a single detector generalizes across ecosystems far better than a species classifier, which is typically region-specific. For species identification, pair MegaDetector with a downstream classifier.


## What does MegaDetector detect?

MegaDetector detects three categories:

| Category | Examples |
|---|---|
| Animal | Mammals, birds, reptiles, insects, fish — any wildlife |
| Person | Researchers, poachers, tourists |
| Vehicle | Cars, trucks, ATVs |

It does not identify species. An image containing a lion and a zebra returns two "animal" detections, not "lion" and "zebra."


## Do I need a GPU?

No — MegaDetector runs on CPU. A GPU with CUDA support gives a 10–50x speedup and is strongly recommended for large datasets (tens of thousands of images or more), but is not required.

The compact MegaDetectorV6 variants (YOLOv10-Compact, YOLOv9-Compact) are specifically designed for low-budget devices and edge hardware like the [SPARROW](https://github.com/microsoft/SPARROW) field unit.


## What is the difference between MegaDetectorV5 and MegaDetectorV6?

| | MegaDetectorV5 | MegaDetectorV6 |
|---|---|---|
| Architecture | YOLOv5 | YOLOv9, YOLOv10, RT-DETR (multiple variants) |
| Parameters (compact) | 139.9M | 2.3M (YOLOv10-Compact — 2% of V5) |
| License | MIT | MIT |
| Status | Maintained by Dan Morris at [agentmorris/MegaDetector](https://github.com/agentmorris/MegaDetector) | Current release — recommended for new projects |
| Weights | Available on [archive branch](https://github.com/microsoft/Biodiversity/tree/archive) | Download automatically via PyTorch-Wildlife |

**Recommendation:** Use MegaDetectorV6 for new projects. MegaDetectorV5 remains available and is actively maintained by the community.

> [!TIP]
> For detailed model variants and benchmark results, see the [Model Zoo](model_zoo.md).


## How accurate is MegaDetector?

Accuracy depends on the dataset and confidence threshold. MegaDetectorV6 compact variants achieve comparable accuracy to V5 at 2% of the parameter count on the AI for Good Lab's validation datasets.

In practice, most deployments use a confidence threshold of 0.15–0.3 for the "animal" category, which provides high recall (few missed animals) at the cost of some false positives on vegetation and lighting artifacts. Setting the threshold higher reduces false positives but risks missing low-confidence true detections.

MegaDetector generalizes well across ecosystems because it was trained on a large and geographically diverse dataset. Performance is typically strongest on large mammals and degrades on very small or camouflaged animals.


## What species does MegaDetector support?

All of them — with caveats. MegaDetector detects the presence of an animal, not the species. It has been deployed on projects involving African savanna megafauna, North American forest species, European ungulates, tropical insects, and marine wildlife.

Performance varies. Large mammals in open habitat are reliably detected. Very small animals, heavily camouflaged species, or unusual angles may have lower confidence scores. If you're working with an atypical dataset, we recommend testing on a labeled sample before full deployment.


## How do I run MegaDetector?

The quickest path is three lines of Python:

```bash
pip install PytorchWildlife
```

```python
from PytorchWildlife.models import detection as pw_detection
model = pw_detection.MegaDetectorV6()
results = model.batch_image_detection("path/to/image_folder/")
```

For a graphical interface, use [SPARROW Studio](https://github.com/microsoft/SPARROW) or the [Hugging Face demo](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife).

See [Installation](installation.md) for full setup instructions.


## What is the license?

MegaDetector is released under the [MIT License](https://github.com/microsoft/MegaDetector/blob/main/LICENSE). You can use it for any purpose, including commercial use, subject to the license terms.

The PyTorch-Wildlife framework that distributes MegaDetector is also MIT-licensed. Individual model weights may carry separate licenses — see the [Model Zoo](model_zoo.md) for per-model licensing information.


## What is Dan Morris's fork?

Dan Morris developed MegaDetector V1–V5 during his time at Microsoft. He continues to actively maintain a community fork at [agentmorris/MegaDetector](https://github.com/agentmorris/MegaDetector), which includes an extensive set of helper scripts, batch processing tools, and documentation accumulated over years of community use. It remains a valuable resource — especially for users of V5 weights or the original `run_detector_batch.py` workflow.

The `microsoft/MegaDetector` repository carries MegaDetectorV6 and future development. Both projects coexist and serve the community.


## Where are the V5 weights?

MegaDetectorV5 weights are available on the [archive branch](https://github.com/microsoft/Biodiversity/tree/archive) of the `microsoft/Biodiversity` repository (formerly `microsoft/CameraTraps`). Dan Morris's fork at [agentmorris/MegaDetector](https://github.com/agentmorris/MegaDetector) also hosts V5 and provides extensive tooling around it.


## How do I cite MegaDetector?

A `CITATION.cff` is maintained in this repository for automated citation tools (Zenodo, GitHub's "Cite this repository" button).

For MegaDetector specifically, cite:

> Beery, Morris, Yang (2019). *Efficient Pipeline for Camera Trap Image Review*. arXiv:1907.06772.

For the PyTorch-Wildlife framework:

> Hernandez et al. (2024). *Pytorch-Wildlife: A Collaborative Deep Learning Framework for Conservation*. arXiv:2405.12930.

See [Cite Us](cite.md) for full citation details and BibTeX.


## Where do I get help?

- **GitHub Issues:** [microsoft/MegaDetector/issues](https://github.com/microsoft/MegaDetector/issues) — bug reports and feature requests
- **Discord:** [Join the PyTorch-Wildlife server](https://discord.gg/TeEVxzaYtm) — community support and discussion
- **Email:** [zhongqimiao@microsoft.com](mailto:zhongqimiao@microsoft.com)
