---
description: "MegaDetector: open-source AI model from Microsoft AI for Good Lab that detects animals, people, and vehicles in camera-trap images. Used by 80+ conservation organizations worldwide."
tags:
  - MegaDetector
  - MegaDetectorV6
  - camera trap AI
  - wildlife detection
  - animal detection
  - conservation AI
  - PyTorch-Wildlife
  - Microsoft AI for Good
---

# MegaDetector

> [!TIP]
> MegaDetector is part of the [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) umbrella — the hub for all AI for Good Lab wildlife tools. The full PyTorch-Wildlife framework and model zoo live at [microsoft/PytorchWildlife](https://github.com/microsoft/PytorchWildlife).

**MegaDetector is an open-source AI model from the [Microsoft AI for Good Lab](https://www.microsoft.com/en-us/ai/ai-for-good) that detects animals in camera-trap imagery.** Used by more than 80 conservation organizations worldwide, MegaDetector automates the review of camera-trap images so researchers can skip empty frames and focus on science. It does not identify species — it locates animals so they can be passed to a downstream classifier.

Our mission is to create a global community where conservation scientists can collaborate — sharing datasets and deep learning architectures for wildlife conservation. We're committed to supporting, maintaining, and advancing **MegaDetector** to ensure its continued **relevance, performance, and impact** for biodiversity research worldwide.


## Quick Start

```bash
pip install PytorchWildlife
```

```python
from PytorchWildlife.models import detection as pw_detection

# Load MegaDetector V6 (weights download automatically)
model = pw_detection.MegaDetectorV6()

# Run on a single image
results = model.single_image_detection("path/to/camera_trap_image.jpg")

# Run on a folder of images
results = model.batch_image_detection("path/to/image_folder/")
```

**Try it without installing anything:**

- [Hugging Face demo](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife) — upload images in your browser
- [Google Colab notebook](https://colab.research.google.com/drive/1rjqHrTMzEHkMualr4vB55dQWCsCKMNXi?usp=sharing) — free cloud GPU


## MegaDetectorV6: SMALLER, FASTER, BETTER

We have officially released our 6th version of MegaDetector, **MegaDetectorV6**. In the next generation of MegaDetector, we focused on computational efficiency, performance, modernizing of model architectures, and licensing. We have trained multiple new models using different model architectures that are optimized for performance and low-budget devices, including **YOLOv9**, **YOLOv10**, and **RT-DETR** for maximum user flexibility.

For example, the **MegaDetectorV6-Ultralytics-YoloV10-Compact** (`MDV6-yolov10-c`) model has only ***2% of the parameters*** of the previous MegaDetectorV5 (2.3M vs. 139.9M) and still exhibits comparable performance on our validation datasets.

To test the newest version of MegaDetector with all the existing functionalities, you can use our [Hugging Face interface](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife) or load the model with **PyTorch-Wildlife** — weights download automatically:

```python
from PytorchWildlife.models import detection as pw_detection
detection_model = pw_detection.MegaDetectorV6()
```

> [!TIP]
> All versions of MegaDetector and corresponding performance can be found in the [Model Zoo](model_zoo.md).

We will continuously fine-tune our V6 models on newly collected public and private data to further improve generalization performance.


## MegaDetectorV5 and Archive Repos

For those interested in accessing the previous MegaDetector repository, which utilizes the same `MegaDetectorV5` model weights and was primarily developed by **Dan Morris** during his time at Microsoft, please visit the [archive branch](https://github.com/microsoft/Biodiversity/tree/archive) of the Biodiversity repository (formerly `microsoft/CameraTraps`), or visit the [forked repository](https://github.com/agentmorris/MegaDetector/tree/main) that Dan Morris is currently actively maintaining.


## Part of the Biodiversity Ecosystem

MegaDetector is one project in a larger open-source ecosystem from the AI for Good Lab:

| Repo | Purpose |
| --- | --- |
| [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) | The umbrella repository — documentation hub for the AI for Good Lab's biodiversity work |
| [microsoft/MegaDetector](https://github.com/microsoft/MegaDetector) | This project — animal detection in camera-trap imagery |
| [microsoft/PytorchWildlife](https://github.com/microsoft/PytorchWildlife) | The collaborative deep learning framework hosting MegaDetector, species classifiers, and demo notebooks |
| [microsoft/SPARROW](https://github.com/microsoft/SPARROW) | Solar-Powered Acoustic and Remote Recording Observation Watch — the AI-enabled edge device that runs MegaDetector in the field |
| [microsoft/MegaDetector-Acoustic](https://github.com/microsoft/MegaDetector-Acoustic) | Bioacoustic models for audio-based wildlife monitoring |
| [microsoft/MegaDetector-Overhead](https://github.com/microsoft/MegaDetector-Overhead) | Point-based detection models for overhead and aerial imagery |
| [SPARROW Studio](https://github.com/microsoft/Biodiversity/tree/main/SPARROW-Studio) | The desktop application that wraps it all in a graphical interface |

> [!TIP]
> If you have any questions regarding MegaDetector and PyTorch-Wildlife, please [email us](mailto:zhongqimiao@microsoft.com) or join us in our Discord channel: [![](https://img.shields.io/badge/any_text-Join_us!-blue?logo=discord&label=PyTorch-Wildlife)](https://discord.gg/TeEVxzaYtm)
