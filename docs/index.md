---
title: "MegaDetector, Open-Source Camera-Trap AI for Wildlife Detection"
description: "MegaDetector is Microsoft AI for Good Lab's open-source model that detects animals, people, and vehicles in camera-trap images, faster and smaller in V6."
tags:
  - MegaDetector
  - MegaDetectorV6
  - camera trap AI
  - wildlife detection
  - animal detection
  - conservation AI
  - PyTorch-Wildlife
  - Microsoft AI for Good
  - YOLOv10
  - RT-DETR
---

# MegaDetector

**Built by the [Microsoft AI for Good Lab](https://www.microsoft.com/en-us/ai/ai-for-good), MegaDetector is an open-source model that locates animals, people, and vehicles in camera-trap images.** A typical camera deployment produces millions of frames, most of them empty. MegaDetector boxes whatever it finds and scores each box, so researchers can clear the blanks automatically and spend their time on science rather than sorting images.

MegaDetector is an **animal detector**, not a species classifier. For species recognition, pair MegaDetector with a downstream classifier (see [Species classification](#species-classification) below). It is free and open-source under the [MIT License](https://github.com/microsoft/MegaDetector/blob/main/LICENSE), and runs in more than 80 conservation programs worldwide.

> [!TIP]
> MegaDetector is part of the [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) umbrella, the hub for all AI for Good Lab wildlife tools. The full PyTorch-Wildlife framework and model zoo live at [microsoft/Pytorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife).

This page is the practical user guide for the current release, **MegaDetectorV6**. If you want a one-screen reference, jump to [Quick start](#quick-start); if you're evaluating whether MegaDetector fits your project, the [FAQ](faq.md) answers the most common questions.


## Quick start

Install the package and run the model in three lines of Python, V6 weights download automatically the first time:

```bash
pip install PytorchWildlife
```

```python
from PytorchWildlife.models import detection as pw_detection

# Load MegaDetectorV6 (weights download automatically)
model = pw_detection.MegaDetectorV6()

# Detect in a single image
results = model.single_image_detection("path/to/camera_trap_image.jpg")

# Detect across a whole folder
results = model.batch_image_detection("path/to/image_folder/")
```

**Prefer not to install anything?**

- [Hugging Face demo](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife): upload images and run MegaDetector in your browser
- [Google Colab notebook](https://colab.research.google.com/drive/1rjqHrTMzEHkMualr4vB55dQWCsCKMNXi?usp=sharing): a free cloud GPU
- [SPARROW Studio](https://github.com/microsoft/SPARROW): a full desktop application with a graphical interface

Full setup, including conda environments and GPU configuration, is on the [Installation](installation.md) page.

Prefer the command line? The [CLI reference](cli.md) covers `megadetector detect`, and the [Output Format](output_format.md) guide explains the JSON results MegaDetector writes.


## What does MegaDetector detect?

MegaDetector detects objects of interest into three categories: animals, people, and vehicles.

Each detection comes with a confidence score between 0 and 1. You choose a threshold (e.g., **0.15–0.3** for the animal category) and anything above it is flagged. The output is a standard results file you can feed into downstream tasks such as species classification.


## MegaDetectorV6: smaller, faster, better

MegaDetectorV6 is the sixth generation of the model, rebuilt around three goals: **computational efficiency, modern architectures, and licensing flexibility.** Instead of a single network, V6 ships a family of variants trained on **YOLOv9**, **YOLOv10**, and **RT-DETR**, so you can match the model to your hardware.

The headline result: the compact YOLOv10 variant (`MDV6-yolov10-c`) carries just **2.3M parameters, about 2% of MegaDetectorV5's 139.9M**, while holding comparable accuracy on the lab's validation datasets. That makes it light enough to run on a laptop CPU or an edge device like the [SPARROW](https://github.com/microsoft/SPARROW) field unit.

A representative slice of the model family:

| Model | Params | Animal recall | mAP50 | License |
| --- | --- | --- | --- | --- |
| MDV6-apa-rtdetr-e | 76M | 82.9% | 94.1% | Apache-2.0 |
| MDV6-yolov10-e | 29.5M | 82.8% | 92.8% | AGPL-3.0 |
| MDV6-yolov10-c | 2.3M | 76.8% | 87.2% | AGPL-3.0 |
| MDV6-mit-yolov9-c | 9.7M | 74.8% | 87.6% | MIT |

> [!TIP]
> This is a subset. The full nine-variant lineup, with YOLOv9, RT-DETR, and additional MIT/Apache options, is in the [Model Zoo](model_zoo.md). Variant names are standardized as **MDV6-Compact** and **MDV6-Extra** for the two sizes within each architecture.

```python
from PytorchWildlife.models import detection as pw_detection

# Load a specific variant
model = pw_detection.MegaDetectorV6(version="MDV6-apa-rtdetr-e")
```

V6 models are continuously fine-tuned on newly collected public and private data to keep improving how well they generalize to new environments.


## Which model should I use?

- **Best accuracy**, `MDV6-apa-rtdetr-e` (82.9% recall, Apache-2.0)
- **Best for laptops and edge devices**, `MDV6-yolov10-c` (2.3M params, runs on CPU)
- **Best all-round balance**, `MDV6-yolov10-e` (29.5M params, 82.8% recall)
- **Need an MIT-licensed model**, `MDV6-mit-yolov9-c`

When in doubt, start with `MDV6-yolov10-e` and only switch if accuracy or hardware constraints push you toward a different variant.


## Do I need a GPU?

No. MegaDetector runs on a CPU. A CUDA-capable NVIDIA GPU delivers a **10–50× speedup** and is strongly recommended once you're processing tens of thousands of images, but it is not required to get started. The compact V6 variants are built specifically for low-budget and edge hardware, so a modern laptop is enough for many projects.

### How fast is MegaDetector?

Throughput depends on the variant and your hardware:

| Hardware | Model | Approximate speed |
| --- | --- | --- |
| NVIDIA RTX 3090 | MDV6-yolov10-c (2.3M) | ~100–200 images/sec |
| NVIDIA RTX 3090 | MDV6-yolov10-e (29.5M) | ~30–60 images/sec |
| Modern CPU (no GPU) | MDV6-yolov10-c (2.3M) | ~2–5 images/sec |
| Google Colab (free GPU) | Any V6 variant | ~10–50 images/sec |

As a rule of thumb, at **50 images/sec on a GPU, one million images takes about 5.5 hours**; on CPU with the compact model, roughly 3.9 days. Even the heaviest V6 variant runs faster than V5.


## Is there a graphical interface?

Yes, you don't have to write any Python if you'd rather not:

- **[SPARROW Studio](https://github.com/microsoft/SPARROW)**, the AI for Good Lab's unified desktop app, built on PyTorch-Wildlife. Run MegaDetector and species classifiers through a GUI, manage data locally or in the cloud, and annotate and visualize results. A signed Windows installer is available [from Zenodo](https://zenodo.org/records/19687738/files/SPARROW%20Studio%20Installer.msi?download=1); Mac and Linux builds are in progress.
- **[AddaxAI](https://addaxdatascience.com/addaxai/)** (formerly EcoAssist), a popular third-party desktop tool for running MegaDetector with batch processing, annotation, and visualization on Windows, macOS, and Linux.
- **[Hugging Face Space](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife)**, run MegaDetector in your browser with nothing to install.


## Species classification

To identify species, run a two-stage pipeline: 1) MegaDetector detects the animals, and 2) a classifier recognizes them:

```python
import supervision as sv
from PytorchWildlife.models import detection as pw_detection
from PytorchWildlife.models import classification as pw_classification

detector = pw_detection.MegaDetectorV6()
classifier = pw_classification.AI4GAmazonRainforest()

det_results = detector.single_image_detection("image.jpg")

for xyxy in det_results["detections"].xyxy:
    cropped = sv.crop_image(image=det_results["img"], xyxy=xyxy)
    cls_result = classifier.single_image_classification(cropped)
    print(f"Species: {cls_result['prediction']}")
```

PyTorch-Wildlife ships several animal classifiers (AI4G Amazon Rainforest, AI4G Snapshot Serengeti, AI4G Opossum, DeepFaune, DFNE). You can also run Google's [SpeciesNet](https://github.com/google/cameratrapai) through PyTorch-Wildlife; SpeciesNet covers roughly 2,000 species globally and is designed to consume MegaDetector output.


## How accurate is MegaDetector?

Accuracy depends on your data and your confidence threshold, so the honest answer is always **test on your own images before trusting any number.** The compact V6 variants reach accuracy comparable to V5 at 2% of the parameter count on the lab's validation datasets, and the larger variants in the [Model Zoo](model_zoo.md) report animal recall above 82%.

In practice, a threshold of **0.15–0.3** gives high recall (few missed animals) at the cost of some false positives on vegetation and lighting artifacts; raising it trims false positives but risks dropping low-confidence true positives. MegaDetector generalizes well across ecosystems because it was trained on a large, geographically diverse dataset. Performance is strongest on large mammals in open habitat.

### Where MegaDetector struggles

MegaDetector struggles with small animals and reptiles. Unusual camera angles also tend to produce lower confidence scores and can be missed. If your dataset is atypical, label a small sample and measure recall before relying on the model at scale.


## Who uses MegaDetector?

MegaDetector is used by more than 80 organizations worldwide, including government agencies, universities, NGOs, museums, and technology platforms. A selection:

- **Government**, Idaho Fish & Game, Oregon DFW, Michigan DNR, Parks Canada, U.S. Fish & Wildlife Service, National Park Service
- **Conservation NGOs**, The Nature Conservancy, Island Conservation, Australian Wildlife Conservancy, RSPB
- **Universities**, UCLA, University of Washington, UBC, University of Florida, UNSW Sydney, Wildlife Institute of India
- **Museums & zoos**, American Museum of Natural History, Smithsonian, San Diego Zoo Wildlife Alliance, Taronga Conservation Society
- **Platforms**, TrapTagger, WildTrax, Camelot, Animl, Wildlife Observer Network

The [full list](https://microsoft.github.io/Biodiversity/collaborators/) lives on the Biodiversity documentation site.


## MegaDetectorV5 and earlier

For new projects, use V6. If you need V5 weights or earlier versions, they're on the [archive branch](https://github.com/microsoft/Biodiversity/tree/archive) of the Biodiversity repository (formerly `microsoft/CameraTraps`).

MegaDetector V1–V5 were originally developed by **Dan Morris** while at Microsoft. The V5 weights load directly through PyTorch-Wildlife, so existing V5 workflows keep running without changes, while `microsoft/MegaDetector` carries V6 and future development.


## Part of the Biodiversity ecosystem

MegaDetector is one model in a larger open-source ecosystem from the AI for Good Lab, with the [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) umbrella tying it together:

| Repo | Purpose |
| --- | --- |
| [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) | The umbrella repository, documentation hub for the AI for Good Lab's biodiversity work |
| [microsoft/MegaDetector](https://github.com/microsoft/MegaDetector) | This project, animal, person, and vehicle detection in camera-trap imagery |
| [microsoft/Pytorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife) | The collaborative deep learning framework hosting MegaDetector, species classifiers, and demo notebooks |
| [microsoft/SPARROW](https://github.com/microsoft/SPARROW) | Solar-Powered Acoustic and Remote Recording Observation Watch, the AI-enabled edge device that runs MegaDetector in the field |
| [microsoft/MegaDetector-Acoustic](https://github.com/microsoft/MegaDetector-Acoustic) | Bioacoustic models for audio-based wildlife monitoring |
| [microsoft/MegaDetector-Classifier](https://github.com/microsoft/MegaDetector-Classifier) | Camera-trap species classification fine-tuning, adapt classifiers to your own datasets and regions |
| [microsoft/MegaDetector-Overhead](https://github.com/microsoft/MegaDetector-Overhead) | Point-based detection models for overhead and aerial imagery |
| [microsoft/MegaDetector-Sonar](https://github.com/microsoft/MegaDetector-Sonar) | Sonar-based wildlife detection for aquatic monitoring |
| SPARROW Studio | The desktop application that wraps it all in a graphical interface |


## Citing MegaDetector

If MegaDetector contributed to your research, please cite the original model paper and, if you used the framework, PyTorch-Wildlife:

```bibtex
@misc{beery2019efficient,
      title={Efficient Pipeline for Camera Trap Image Review},
      author={Sara Beery and Dan Morris and Siyu Yang},
      year={2019},
      eprint={1907.06772},
      archivePrefix={arXiv},
}
```

Full citation details and the PyTorch-Wildlife BibTeX are on the [Cite Us](cite.md) page, or use GitHub's **"Cite this repository"** button on [microsoft/MegaDetector](https://github.com/microsoft/MegaDetector).


## Get help

- **GitHub Issues**, [microsoft/MegaDetector/issues](https://github.com/microsoft/MegaDetector/issues) for bugs and feature requests
- **Discord**, [join the PyTorch-Wildlife community](https://discord.gg/TeEVxzaYtm)
- **Email**, [zhongqimiao@microsoft.com](mailto:zhongqimiao@microsoft.com)
- **Contributing**, see the [contributing guide](contributing.md); the [repository architecture](architecture.md) page explains the codebase layout

> [!TIP]
> New to MegaDetector? The [FAQ](faq.md) covers installation, accuracy, GPU requirements, V5 vs. V6, and licensing in one place.
