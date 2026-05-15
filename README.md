# MegaDetector

**MegaDetector is an open-source AI model from the [Microsoft AI for Good Lab](https://www.microsoft.com/en-us/ai/ai-for-good) that detects animals in camera-trap imagery.** Used by more than 80 conservation organizations worldwide, MegaDetector automates the review of camera-trap images so researchers can skip empty frames and focus on science. It does not identify species — it locates animals so they can be passed to a downstream classifier.

MegaDetector is one project in the [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) ecosystem and is invoked through the [PyTorch-Wildlife](https://github.com/microsoft/PytorchWildlife) framework. It is free, open-source, and available under permissive licenses.

[![PyPI](https://img.shields.io/pypi/v/PytorchWildlife?color=limegreen)](https://pypi.org/project/PytorchWildlife)
[![Downloads](https://static.pepy.tech/badge/pytorchwildlife)](https://pypi.org/project/PytorchWildlife)
[![Python](https://img.shields.io/pypi/pyversions/PytorchWildlife)](https://pypi.org/project/PytorchWildlife)
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Demo-blue)](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife)
[![License](https://img.shields.io/pypi/l/PytorchWildlife)](https://github.com/microsoft/MegaDetector/blob/main/LICENSE)
[![Discord](https://img.shields.io/badge/any_text-Join_us!-blue?logo=discord&label=Discord)](https://discord.gg/TeEVxzaYtm)


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

That's it. Three lines to detect animals in your camera-trap images.

Need the local `megadetector` CLI or fine-tuning? See [Install from source](#install-from-source-for-fine-tuning-or-cli-use) and [Fine-Tuning](#fine-tuning) below.

**Try it without installing anything:**
- [Hugging Face demo](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife) — upload images in your browser
- [Google Colab notebook](https://colab.research.google.com/drive/1rjqHrTMzEHkMualr4vB55dQWCsCKMNXi?usp=sharing) — free cloud GPU


## What Does MegaDetector Do?

Camera traps generate millions of images, and the vast majority are empty frames triggered by wind or vegetation. Manually reviewing them is one of the biggest bottlenecks in wildlife research.

MegaDetector solves this. It scans your images and draws bounding boxes around any animal — mammals, birds, reptiles, insects, and more. Each detection has a confidence score between 0 and 1. You set a threshold (typically 0.15–0.3), and anything above it is flagged. The output lets you sort images, filter blanks, or feed detected animals into a species classifier.

MegaDetector is intentionally a **detector**, not a classifier. "Animal vs. background" generalizes across ecosystems far better than species identification. For species classification, pair MegaDetector with a downstream classifier — see [Species Classification](#species-classification) below.


## MegaDetector V6

The latest release focuses on **efficiency** and **modern architectures** — **SMALLER, FASTER, BETTER**.

### Highlights

- **50x smaller**: The compact YOLOv10 variant has **2.3M parameters** — 2% of MegaDetector V5's 139.9M — with comparable accuracy
- **Multiple architectures**: YOLOv9, YOLOv10, RT-DETR — pick the one that fits your hardware
- **Ongoing fine-tuning**: V6 models are continuously fine-tuned on newly collected public and private data to further improve generalization

### Model Variants

| Model | Params | Animal Recall | mAP50 | License |
| --- | --- | --- | --- | --- |
| MDV6-yolov10-e | 29.5M | 82.8% | 92.8% | AGPL-3.0 |
| MDV6-yolov9-e | 58.1M | 82.1% | 88.6% | AGPL-3.0 |
| MDV6-rtdetr-c | 31.9M | 81.6% | 89.9% | AGPL-3.0 |
| MDV6-yolov9-c | 25.5M | 78.4% | 87.9% | AGPL-3.0 |
| MDV6-yolov10-c | 2.3M | 76.8% | 87.2% | AGPL-3.0 |

Model names are standardized into **MDV6-Compact** and **MDV6-Extra** for the two model sizes within each architecture, reducing confusion across variants.

**Which should I use?**
- **Best accuracy**: MDV6-yolov10-e (82.8% recall, AGPL-3.0)
- **Best for laptops/edge**: MDV6-yolov10-c (2.3M params, runs on CPU)
- **Best balance**: MDV6-yolov10-e (29.5M params, 82.8% recall)

```python
# Load a specific variant
from PytorchWildlife.models import detection as pw_detection

model = pw_detection.MegaDetectorV6(version="MDV6-yolov10-e")
```


## Installation

```bash
pip install PytorchWildlife
```

**Requirements:**
- Python 3.8+ (3.10+ recommended)
- Optional: NVIDIA GPU with CUDA for 10–50x speedup

**Conda users:**
```bash
conda create -n megadetector python=3.10 -y
conda activate megadetector
pip install PytorchWildlife
```

**GPU setup (if PyTorch didn't install with CUDA):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Install from source (for fine-tuning or CLI use)

For the local `megadetector` command-line tool and to fine-tune V6 weights on
your own dataset, install this repository in editable mode:

```bash
git clone https://github.com/microsoft/MegaDetector
cd MegaDetector
pip install -e .
```

This installs the `megadetector_core` Python package and exposes the
`megadetector` shell command (`megadetector detect|train|validate|inference`).
The `pyproject.toml` covers the full dependency set — no separate
`requirements.txt` is needed.

Full installation guide: [microsoft.github.io/MegaDetector/installation/](https://microsoft.github.io/MegaDetector/installation/)


## Species Classification

MegaDetector finds animals — it doesn't identify species. For species ID, run a two-stage pipeline:

1. **MegaDetector** detects and localizes animals
2. **A species classifier** identifies the species in each crop

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

**Available classifiers in PyTorch-Wildlife:**

| Classifier | Region | Classes | License |
| --- | --- | --- | --- |
| AI4G Amazon Rainforest | Amazon basin | 36 | MIT |
| AI4G Snapshot Serengeti | East Africa | 10 | MIT |
| AI4G Opossum | Galapagos | 2 | MIT |
| DeepFaune Classifier | Europe | 34 | CC BY-SA 4.0 |
| DFNE | Northeastern U.S. | 23 | CC0 1.0 |

Google's [SpeciesNet](https://github.com/google/cameratrapai) is also designed to work with MegaDetector output and covers ~2,000 species globally.


## Desktop and Web Interfaces

### AddaxAI (formerly EcoAssist)

[AddaxAI](https://addaxdatascience.com/addaxai/) is a third-party desktop tool for running MegaDetector with batch processing, annotation, and results visualization. Windows, macOS, and Linux.

### Hugging Face Space

[Upload images and run MegaDetector in your browser](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife) — no installation required.


## Part of the Biodiversity Ecosystem

MegaDetector is one model in a larger open-source ecosystem from the AI for Good Lab. Each project lives in its own repository, with the [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) umbrella tying them together.

| Repo | Purpose |
| --- | --- |
| [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) | The umbrella repository — documentation hub for the AI for Good Lab's biodiversity work |
| [microsoft/PytorchWildlife](https://github.com/microsoft/PytorchWildlife) | The collaborative deep learning framework that hosts MegaDetector, species classifiers (AI4G Amazon Rainforest, AI4G Snapshot Serengeti, DeepFaune), HerdNet, PW-Engine (a Rust-based inference core), and demo notebooks |
| [microsoft/SPARROW](https://github.com/microsoft/SPARROW) | Solar-Powered Acoustic and Remote Recording Observation Watch — the AI-enabled edge device that runs MegaDetector in remote field locations |
| [microsoft/MegaDetector-Acoustic](https://github.com/microsoft/MegaDetector-Acoustic) | Bioacoustic models for audio-based wildlife monitoring |
| [microsoft/MegaDetector-Classifier](https://github.com/microsoft/MegaDetector-Classifier) | Camera-trap species classification fine-tuning — adapt classifiers to your own datasets and geographic regions |
| [microsoft/MegaDetector-Overhead](https://github.com/microsoft/MegaDetector-Overhead) | Point-based detection models for overhead and aerial imagery |
| [microsoft/MegaDetector-Sonar](https://github.com/microsoft/MegaDetector-Sonar) | Sonar-based wildlife detection for aquatic monitoring |
MegaDetector is the entry point for most users. SPARROW is the field-hardened edge device.


## Organizations Using MegaDetector

MegaDetector is used by 80+ organizations across government agencies, universities, NGOs, and technology companies worldwide. A selection:

**Government**: Arizona DEQ, Idaho Fish & Game, Oregon DFW, Michigan DNR, Parks Canada (Banff), U.S. Fish & Wildlife Service (multiple refuges), National Park Service, Canadian Wildlife Service

**Conservation NGOs**: The Nature Conservancy, Island Conservation, Wildlife Protection Solutions, Australian Wildlife Conservancy, RSPB, CPAWS, SPEA, Felidae Conservation Fund

**Universities**: UCLA, University of Washington, UBC, University of Florida, University of Idaho, UNSW Sydney, Macquarie University, University of Saskatchewan, Washington State University, Bangor University, Tel Aviv University, TU Berlin, Wildlife Institute of India

**Museums & Zoos**: American Museum of Natural History, Smithsonian, Woodland Park Zoo, San Diego Zoo Wildlife Alliance, Taronga Conservation Society

**Platforms**: TrapTagger, WildTrax, Camelot, Animl, Wildlife Observer Network, OCAPI, WildePod

See the [full list](https://github.com/microsoft/PytorchWildlife#who-uses-megadetector) in the PyTorch-Wildlife repository.


## Performance

| Hardware | Model | Approximate Speed |
| --- | --- | --- |
| NVIDIA RTX 3090 | MDV6-yolov10-c (2.3M) | ~100–200 images/sec |
| NVIDIA RTX 3090 | MDV6-yolov10-e (29.5M) | ~30–60 images/sec |
| Modern CPU (no GPU) | MDV6-yolov10-c (2.3M) | ~2–5 images/sec |
| Google Colab (free GPU) | Any V6 variant | ~10–50 images/sec |

At 50 images/sec on a GPU, **one million images takes about 5.5 hours**. On CPU with the compact model, about 3.9 days.

Every V6 variant is faster than V5 (139.9M params). The compact V6 is 2% the size.


## Fine-Tuning

MegaDetector V6 ships with a fine-tuning pipeline (built on the
[ultralytics](https://github.com/ultralytics/ultralytics) framework) so you can
adapt a V6 model to your own camera-trap dataset. Fine-tuning is useful when
the off-the-shelf V6 models miss animals that look different from the training
distribution — for example, an under-represented species, a specific
environment (forest canopy, snow, night-vision IR), or a new sensor.

**Quick path:**

```bash
# 1. Clone and install in editable mode (from a fresh venv or conda env).
git clone https://github.com/microsoft/MegaDetector
cd MegaDetector
pip install -e .

# 2. Copy the reference config and edit `data:` to point at your dataset YAML.
cp examples/config_training.yaml ./config.yaml

# 3. Train, validate, and run inference with the same CLI.
megadetector train    --config ./config.yaml
megadetector validate --config ./config.yaml
megadetector inference --config ./config.yaml
```

**Supported fine-tuning model variants:**

- `MDV6-yolov9-c` — compact YOLOv9
- `MDV6-yolov9-e` — extra-large YOLOv9
- `MDV6-yolov10-c` — compact YOLOv10 (2.3M params)
- `MDV6-yolov10-e` — extra-large YOLOv10
- `MDV6-rtdetr-c` — compact RT-DETR

Training outputs (weights, plots, metrics) land under `./runs/` keyed by the
`exp_name` field in your config. Fine-tuned `.pt` weights can be loaded back
into `MegaDetectorV6(weights="path/to/best.pt")` for inference.

**Full reference:** [docs/training_guide.md](docs/training_guide.md) covers
data layout, the full config schema, conda environment setup, and the Python
API equivalents of each CLI subcommand.


## Version History

| Version | Year | Architecture | Params | Notes |
| --- | --- | --- | --- | --- |
| **V6.0** (current) | 2024 | YOLOv9/v10, RT-DETR | 2.3M–58.1M | YOLOv9/v10 + RT-DETR variants (AGPL-3.0) |
| V5.0 | 2022 | YOLOv5 | 139.9M | Two sub-versions (5a, 5b) |
| V4.1 | 2020 | Faster R-CNN | — | Added vehicle class |
| V3 | 2019 | Faster R-CNN | — | Added human class |
| V2 | 2018 | Faster R-CNN | — | First public release |


## MegaDetector V5 and Earlier

For MegaDetectorV5 model weights and earlier versions, see the [archive branch](https://github.com/microsoft/Biodiversity/tree/archive) of the Biodiversity repository (formerly `microsoft/CameraTraps`).

The original MegaDetector repository was primarily developed by **Dan Morris** during his time at Microsoft. Dan continues to actively maintain a forked version at [agentmorris/MegaDetector](https://github.com/agentmorris/MegaDetector), which remains a valuable resource for the community.


## Our Commitment

At the core of our mission is the desire to create a harmonious space where conservation scientists from all over the globe can unite — to share, grow, and use datasets and deep learning architectures for wildlife conservation. We've been inspired by the potential and capabilities of MegaDetector, and we deeply value its contributions to the community. We remain committed to supporting, maintaining, and developing MegaDetector — ensuring its continued relevance, expansion, and utility.


## Citing MegaDetector

**PyTorch-Wildlife (the framework):**
```bibtex
@misc{hernandez2024pytorchwildlife,
      title={Pytorch-Wildlife: A Collaborative Deep Learning Framework for Conservation},
      author={Andres Hernandez and Zhongqi Miao and Luisa Vargas and Sara Beery and Rahul Dodhia and Juan Lavista},
      year={2024},
      eprint={2405.12930},
      archivePrefix={arXiv},
}
```

**MegaDetector (the original model):**
```bibtex
@misc{beery2019efficient,
      title={Efficient Pipeline for Camera Trap Image Review},
      author={Sara Beery and Dan Morris and Siyu Yang},
      year={2019},
      eprint={1907.06772},
      archivePrefix={arXiv},
}
```

You can also use GitHub's "Cite this repository" button in the sidebar.


## Contributing

MegaDetector's source code lives in this repository. To contribute code, file issues, or submit pull requests, head to [microsoft/MegaDetector/issues](https://github.com/microsoft/MegaDetector/issues).

For framework-level changes (PyTorch-Wildlife API, classifiers, demo notebooks), see [microsoft/PytorchWildlife](https://github.com/microsoft/PytorchWildlife). For ecosystem-wide questions, see the [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) umbrella.

For questions, feature requests, or to report how MegaDetector worked on your data:
- **Email**: [zhongqimiao@microsoft.com](mailto:zhongqimiao@microsoft.com)
- **Discord**: [![Discord](https://img.shields.io/badge/any_text-Join_us!-blue?logo=discord&label=Discord)](https://discord.gg/TeEVxzaYtm)
- **GitHub Discussions**: [microsoft/Biodiversity/discussions](https://github.com/microsoft/Biodiversity/discussions)


## License

The MegaDetector code is released under the [MIT License](LICENSE). Individual model weights documented in this repository are released under AGPL-3.0 — see the [Model Variants](#model-variants) table for details.
