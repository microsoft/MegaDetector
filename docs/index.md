---
title: "MegaDetector: Open-Source Camera-Trap AI | Microsoft AI for Good"
description: "MegaDetector: open-source AI model from Microsoft AI for Good Lab that detects animals, people, and vehicles in camera-trap images. Used by 80+ conservation organizations worldwide."
schema: software
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

# MegaDetector: Open-Source AI for Camera-Trap Wildlife Detection

> [!TIP]
> MegaDetector is part of the [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) umbrella — the hub for all AI for Good Lab wildlife tools. The full PyTorch-Wildlife framework and model zoo live at [microsoft/Pytorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife).

**MegaDetector is an open-source AI model from the [Microsoft AI for Good Lab](https://www.microsoft.com/en-us/ai/ai-for-good) that detects animals in camera-trap imagery.** Used by more than 80 conservation organizations worldwide, MegaDetector automates the review of camera-trap images so researchers can skip empty frames and focus on science. It does not identify species — it locates animals so they can be passed to a downstream classifier.

Our mission is to create a global community where conservation scientists can collaborate — sharing datasets and deep learning architectures for wildlife conservation. We're committed to supporting, maintaining, and advancing **MegaDetector** to ensure its continued **relevance, performance, and impact** for biodiversity research worldwide.


## Official Resources

The canonical, up-to-date home for MegaDetector — start here, and link here:

| Resource | Where |
| --- | --- |
| **Official documentation** | This site — [microsoft.github.io/MegaDetector](https://microsoft.github.io/MegaDetector/) |
| **Source code & releases** | [microsoft/MegaDetector on GitHub](https://github.com/microsoft/MegaDetector) |
| **Python framework** | [PyTorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife) — hosts and distributes MegaDetectorV6 |
| **Python package** | [`PytorchWildlife` on PyPI](https://pypi.org/project/PytorchWildlife/) — `pip install PytorchWildlife` |
| **Legacy V5 tooling** | [Dan Morris community fork](https://github.com/agentmorris/MegaDetector) |
| **MegaDetectorV5 weights** | [Biodiversity archive branch](https://github.com/microsoft/Biodiversity/tree/archive) (formerly `microsoft/CameraTraps`) |


## What is MegaDetector?

MegaDetector is a **detector**, not a species classifier: it draws a bounding box around each animal it finds and assigns a confidence score, telling you *something is there* rather than *what species it is*. That single design choice is why one model generalizes across ecosystems — from African savanna to North American forest to tropical insect surveys — far better than a region-specific classifier. For species identification, pair MegaDetector with a downstream classifier such as those in [PyTorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife). For the full breakdown of what MegaDetector locates in each frame, see the [MegaDetector FAQ](faq.md#what-does-megadetector-detect).


## Why use MegaDetector for camera-trap images?

Camera traps generate enormous volumes of imagery, and the majority of frames are empty — triggered by wind, rain, or moving vegetation. MegaDetector solves the triage problem:

- **Filter empty frames** so reviewers only spend time on images that actually contain wildlife.
- **Process large datasets** — run locally on CPU, on a CUDA GPU for a 10–50× speedup, or on low-budget edge hardware.
- **Stay open source** — MIT-licensed, free for research and commercial use.
- **Plug into an ecosystem** — graphical tools, notebooks, and field devices already speak MegaDetector.

See the [camera-trap AI guide](camera-trap-ai.md) for how detection fits into a full review workflow.


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


### Which MegaDetector version should I use?

Use **MegaDetectorV6** for new projects — it is smaller, faster, and ships modern architectures (YOLOv9, YOLOv10, RT-DETR). Use **MegaDetectorV5** if you need the original V5 workflow, legacy scripts, or continuity with previously published results; it remains community-maintained by Dan Morris. See the [full V5-vs-V6 comparison in the FAQ](faq.md#what-is-the-difference-between-megadetectorv5-and-megadetectorv6) and per-variant benchmarks in the [MegaDetector model zoo](model_zoo.md).


## MegaDetectorV5 and Archive Repos

For those interested in accessing the previous MegaDetector repository, which utilizes the same `MegaDetectorV5` model weights and was primarily developed by **Dan Morris** during his time at Microsoft, please visit the [archive branch](https://github.com/microsoft/Biodiversity/tree/archive) of the Biodiversity repository (formerly `microsoft/CameraTraps`), or visit the [forked repository](https://github.com/agentmorris/MegaDetector/tree/main) that Dan Morris is currently actively maintaining.


## Use MegaDetector without code

Prefer a graphical workflow? MegaDetector runs inside several no-code tools:

- **[SPARROW Studio](https://github.com/microsoft/SPARROW)** — the desktop application that wraps the AI for Good Lab biodiversity stack in a graphical interface.
- **[Hugging Face demo](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife)** — upload images in your browser, nothing to install.
- **[Google Colab notebook](https://colab.research.google.com/drive/1rjqHrTMzEHkMualr4vB55dQWCsCKMNXi?usp=sharing)** — free cloud GPU.

See [camera-trap software](camera-trap-software.md) for the full landscape of desktop and web interfaces.


## Who uses MegaDetector?

MegaDetector is used by **more than 80 conservation organizations worldwide** — academic camera-trap labs, conservation NGOs, and government wildlife agencies — to triage biodiversity-monitoring imagery at scale, and it runs in the field on the solar-powered [SPARROW](https://github.com/microsoft/SPARROW) edge device. See the [project repository](https://github.com/microsoft/MegaDetector) for current deployments and collaborators.


## MegaDetector in conservation research

MegaDetector has been used and evaluated in peer-reviewed camera-trap research on automated wildlife detection, blank-frame filtering, and large-scale monitoring workflows. The foundational references are:

- Beery, Morris, Yang (2019). *Efficient Pipeline for Camera Trap Image Review.* arXiv:1907.06772.
- Hernandez et al. (2024). *Pytorch-Wildlife: A Collaborative Deep Learning Framework for Conservation.* arXiv:2405.12930.

See [Cite Us](cite.md) for full citation details and BibTeX.


## MegaDetector licenses and model variants

MegaDetector is released under the [MIT License](https://github.com/microsoft/MegaDetector/blob/main/LICENSE) — free for research and commercial use. Individual V6 weights may carry their own terms depending on the backbone architecture; see the [MegaDetector model zoo](model_zoo.md) for per-variant licensing and the [FAQ](faq.md#what-is-the-license) for details.


## Cite MegaDetector

If MegaDetector supports your work, please cite it. A `CITATION.cff` in the repository powers GitHub's "Cite this repository" button and Zenodo. Full BibTeX for both the MegaDetector model and the PyTorch-Wildlife framework is on the [Cite Us](cite.md) page.


## Frequently asked questions

Common questions, answered in full on the [MegaDetector FAQ](faq.md):

- [What does MegaDetector detect?](faq.md#what-does-megadetector-detect)
- [Do I need a GPU?](faq.md#do-i-need-a-gpu)
- [How accurate is MegaDetector?](faq.md#how-accurate-is-megadetector)
- [What is the difference between MegaDetectorV5 and MegaDetectorV6?](faq.md#what-is-the-difference-between-megadetectorv5-and-megadetectorv6)
- [What is the license?](faq.md#what-is-the-license)


## Part of the Biodiversity Ecosystem

MegaDetector is one project in a larger open-source ecosystem from the AI for Good Lab:

| Repo | Purpose |
| --- | --- |
| [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) | The umbrella repository — documentation hub for the AI for Good Lab's biodiversity work |
| [microsoft/MegaDetector](https://github.com/microsoft/MegaDetector) | This project — animal detection in camera-trap imagery |
| [microsoft/Pytorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife) | The collaborative deep learning framework hosting MegaDetector, species classifiers, and demo notebooks |
| [microsoft/SPARROW](https://github.com/microsoft/SPARROW) | Solar-Powered Acoustic and Remote Recording Observation Watch — the AI-enabled edge device that runs MegaDetector in the field |
| [microsoft/MegaDetector-Acoustic](https://github.com/microsoft/MegaDetector-Acoustic) | Bioacoustic models for audio-based wildlife monitoring |
| [microsoft/MegaDetector-Classifier](https://github.com/microsoft/MegaDetector-Classifier) | Camera-trap species classification fine-tuning — adapt classifiers to your own datasets and geographic regions |
| [microsoft/MegaDetector-Overhead](https://github.com/microsoft/MegaDetector-Overhead) | Point-based detection models for overhead and aerial imagery |
| [microsoft/MegaDetector-Sonar](https://github.com/microsoft/MegaDetector-Sonar) | Sonar-based wildlife detection for aquatic monitoring |
| SPARROW Studio | The desktop application that wraps it all in a graphical interface |

> [!TIP]
> If you have any questions regarding MegaDetector and PyTorch-Wildlife, please [email us](mailto:zhongqimiao@microsoft.com) or join us in our Discord channel: [![](https://img.shields.io/badge/any_text-Join_us!-blue?logo=discord&label=PyTorch-Wildlife)](https://discord.gg/TeEVxzaYtm)
