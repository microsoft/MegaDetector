---
description: "MegaDetector model zoo: all MegaDetectorV6 variants with architectures, parameter counts, animal recall, mAP50, and license options for camera-trap wildlife detection."
tags:
  - MegaDetector
  - MegaDetectorV6
  - MegaDetectorV5
  - wildlife detection models
  - camera trap AI
  - model zoo
  - YOLOv9
  - YOLOv10
  - RT-DETR
---

# Model Zoo

All MegaDetector model variants with performance metrics, parameter counts, and licenses.


## MegaDetector V6 (Current)

The latest release focuses on **efficiency**, **modern architectures**, and **licensing flexibility** — **SMALLER, FASTER, BETTER**.

### Highlights

- **50x smaller**: The compact YOLOv10 variant has **2.3M parameters** — 2% of MegaDetectorV5's 139.9M — with comparable accuracy
- **Multiple architectures**: YOLOv9, YOLOv10, RT-DETR — pick the one that fits your hardware
- **Permissive licenses**: MIT and Apache-2.0 options alongside AGPL-3.0
- **Ongoing fine-tuning**: V6 models are continuously fine-tuned on newly collected public and private data

### Model Variants

| Model | Params | Animal Recall | mAP50 | License |
| --- | --- | --- | --- | --- |
| MDV6-apa-rtdetr-e | 76M | 82.9% | 94.1% | Apache-2.0 |
| MDV6-yolov10-e | 29.5M | 82.8% | 92.8% | AGPL-3.0 |
| MDV6-yolov9-e | 58.1M | 82.1% | 88.6% | AGPL-3.0 |
| MDV6-rtdetr-c | 31.9M | 81.6% | 89.9% | AGPL-3.0 |
| MDV6-apa-rtdetr-c | 20M | 81.1% | 91.0% | Apache-2.0 |
| MDV6-yolov9-c | 25.5M | 78.4% | 87.9% | AGPL-3.0 |
| MDV6-yolov10-c | 2.3M | 76.8% | 87.2% | AGPL-3.0 |
| MDV6-mit-yolov9-e | 51M | 76.1% | 71.5% | MIT |
| MDV6-mit-yolov9-c | 9.7M | 74.8% | 87.6% | MIT |

Model names are standardized into **MDV6-Compact** and **MDV6-Extra** for the two model sizes within each architecture.

### Which Model Should I Use?

- **Best accuracy**: MDV6-apa-rtdetr-e (82.9% recall, Apache-2.0)
- **Best for laptops/edge**: MDV6-yolov10-c (2.3M params, runs on CPU)
- **Best balance**: MDV6-yolov10-e (29.5M params, 82.8% recall)
- **Need MIT license?**: MDV6-mit-yolov9-c

```python
from PytorchWildlife.models import detection as pw_detection

# Load a specific variant
model = pw_detection.MegaDetectorV6(version="MDV6-apa-rtdetr-e")
```


## Model Licensing

V6 deliberately offers variants under three licenses so you can match the model to your project's distribution requirements:

| License | Variants | Use when |
| --- | --- | --- |
| **MIT** | `MDV6-mit-yolov9-c`, `MDV6-mit-yolov9-e` | You need a permissive license with no copyleft obligations — e.g. bundling weights into a closed-source product |
| **Apache-2.0** | `MDV6-apa-rtdetr-c`, `MDV6-apa-rtdetr-e` | You want a permissive license with an explicit patent grant; `MDV6-apa-rtdetr-e` is also the top-accuracy variant |
| **AGPL-3.0** | the remaining YOLOv9/YOLOv10/RT-DETR variants | Your use is compatible with strong copyleft (research, internal tools, AGPL-licensed services) |

The repository **code** is MIT-licensed independently of the weights. Always confirm the license of the specific variant you ship.

> [!NOTE]
> The [`megadetector` CLI](cli.md) selects from the AGPL YOLOv9/YOLOv10/RT-DETR variants via `--model`; the MIT and Apache variants are loaded through the PyTorch-Wildlife Python API.


## Performance Benchmarks

| Hardware | Model | Approximate Speed |
| --- | --- | --- |
| NVIDIA RTX 3090 | MDV6-yolov10-c (2.3M) | ~100–200 images/sec |
| NVIDIA RTX 3090 | MDV6-yolov10-e (29.5M) | ~30–60 images/sec |
| Modern CPU (no GPU) | MDV6-yolov10-c (2.3M) | ~2–5 images/sec |
| Google Colab (free GPU) | Any V6 variant | ~10–50 images/sec |

At 50 images/sec on a GPU, **one million images takes about 5.5 hours**. On CPU with the compact model, about 3.9 days. Every V6 variant is faster than V5 (139.9M params).


## Version History

| Version | Year | Architecture | Params | Notes |
| --- | --- | --- | --- | --- |
| **V6.0** (current) | 2024 | YOLOv9/v10, RT-DETR | 2.3M–76M | Multiple variants, MIT/Apache options |
| V5.0 | 2022 | YOLOv5 | 139.9M | Two sub-versions (5a, 5b) |
| V4.1 | 2020 | Faster R-CNN | — | Added vehicle class |
| V3 | 2019 | Faster R-CNN | — | Added human class |
| V2 | 2018 | Faster R-CNN | — | First public release |


## MegaDetector V5 and Earlier

For MegaDetectorV5 model weights and earlier versions, see the [archive branch](https://github.com/microsoft/Biodiversity/tree/archive) of the Biodiversity repository (formerly `microsoft/CameraTraps`).

The original MegaDetector repository was primarily developed by **Dan Morris** during his time at Microsoft. Dan continues to actively maintain a forked version at [agentmorris/MegaDetector](https://github.com/agentmorris/MegaDetector), which remains a valuable resource for the community.
