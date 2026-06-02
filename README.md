# MegaDetector

**MegaDetector is an open-source AI model from the [Microsoft AI for Good Lab](https://www.microsoft.com/en-us/ai/ai-for-good) that detects animals, people, and vehicles in camera-trap images.** Used by more than 80 conservation organizations worldwide, MegaDetector automates camera-trap image review so researchers can skip empty frames and focus on science. It is an animal detector, not a species classifier. It finds and boxes objects, then hands them to a downstream classifier for species identification.

MegaDetector is one project in the [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) ecosystem and is invoked through the [PyTorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife) framework. It is free, open-source, and available under permissive licenses.

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
- [Hugging Face demo](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife): upload images in your browser
- [Google Colab notebook](https://colab.research.google.com/drive/1rjqHrTMzEHkMualr4vB55dQWCsCKMNXi?usp=sharing): free cloud GPU


## What Does MegaDetector Do?

Camera traps generate millions of images, and in typical deployments **70–95% are empty**, frames triggered by wind, rain, or moving vegetation. Sorting those by hand is one of the biggest bottlenecks in wildlife research, and it scales badly: more cameras mean exponentially more images to clear before any science can begin.

MegaDetector solves this. It scans your images and draws bounding boxes around every **animal** (mammals, birds, reptiles, insects, and more), **person**, and **vehicle** it finds. Each detection has a confidence score between 0 and 1. You set a threshold (typically 0.15–0.3), and anything above it is flagged. The output lets you sort images, filter blanks, separate human and vehicle traffic, or feed detected animals into a species classifier.

MegaDetector is intentionally a **detector**, not a classifier. "Animal vs. background" generalizes across ecosystems far better than species identification. For species classification, pair MegaDetector with a downstream classifier, see [Species Classification](#species-classification) below.


## MegaDetector V6

The latest release focuses on **efficiency** and **modern architectures**, **SMALLER, FASTER, BETTER**.

### Highlights

- **50x smaller**: The compact YOLOv10 variant has **2.3M parameters**, 2% of MegaDetector V5's 139.9M, with comparable accuracy
- **Multiple architectures**: YOLOv9, YOLOv10, and RT-DETR, so you can match the model to your hardware
- **Ongoing fine-tuning**: we keep retraining V6 on freshly collected public and private data to push generalization further

### Model Variants

| Model | Params | Animal Recall | mAP50 | License |
| --- | --- | --- | --- | --- |
| MDV6-apa-rtdetr-e | 76M | 82.9% | 94.1% | Apache-2.0 |
| MDV6-yolov10-e | 29.5M | 82.8% | 92.8% | AGPL-3.0 |
| MDV6-yolov10-c | 2.3M | 76.8% | 87.2% | AGPL-3.0 |
| MDV6-mit-yolov9-c | 9.7M | 74.8% | 87.6% | MIT |

This is a representative selection. The full nine-variant lineup (YOLOv9, YOLOv10, and RT-DETR, with MIT, Apache-2.0, and AGPL-3.0 options) and all metrics live in the [Model Zoo](https://microsoft.github.io/MegaDetector/model_zoo/). Variant names are standardized as **MDV6-Compact** and **MDV6-Extra** for the two sizes within each architecture.

**Which should I use?**
- **Best accuracy**: `MDV6-apa-rtdetr-e` (82.9% recall, Apache-2.0)
- **Best for laptops/edge**: `MDV6-yolov10-c` (2.3M params, runs on CPU)
- **Permissive MIT license**: `MDV6-mit-yolov9-c`
- **Best via the `megadetector` CLI**: `MDV6-yolov10-e`. The CLI's `--model` flag supports `MDV6-yolov9-c/e`, `MDV6-yolov10-c/e`, and `MDV6-rtdetr-c`; the MIT and Apache variants load through PyTorch-Wildlife.

```python
# Load a specific variant
from PytorchWildlife.models import detection as pw_detection

model = pw_detection.MegaDetectorV6(version="MDV6-yolov10-e")
```


## Which MegaDetector Repo Should I Use?

Use **this repository (`microsoft/MegaDetector`)** for MegaDetector V6: the current models, the [Model Zoo](https://microsoft.github.io/MegaDetector/model_zoo/), the fine-tuning pipeline, and the [documentation site](https://microsoft.github.io/MegaDetector/). It is the official home maintained by the Microsoft AI for Good Lab.

If you are maintaining a legacy V5 workflow, the original models remain available: V5 weights live on the [Biodiversity archive branch](https://github.com/microsoft/Biodiversity/tree/archive) and load directly through PyTorch-Wildlife. For new projects, start with V6 here.


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
The `pyproject.toml` covers the full dependency set, so no separate
`requirements.txt` is needed.

Full installation guide: [microsoft.github.io/MegaDetector/installation/](https://microsoft.github.io/MegaDetector/installation/)


## How Do I Run MegaDetector? (Python, CLI, or No-Code)

There are three ways to run MegaDetector. Choose whichever suits your workflow:

| You are… | Use | How |
| --- | --- | --- |
| A Python developer | the `PytorchWildlife` API | `MegaDetectorV6().batch_image_detection("images/")`, see [Quick Start](#quick-start) |
| Comfortable in a terminal | the `megadetector` CLI | `megadetector detect --input ./images/ --output results.json` |
| Not a coder | a graphical app | [SPARROW Studio](#desktop-and-web-interfaces) or [AddaxAI](#desktop-and-web-interfaces) |

The CLI ships with the package and wraps the same models:

```bash
# Detect on a folder, write JSON, choose a model and threshold
megadetector detect --input ./images/ --output results.json --model MDV6-yolov10-e --threshold 0.2
```

The `--input` path can be a single image or a folder; folders are scanned recursively for `.jpg`, `.jpeg`, `.png`, `.bmp`, and `.tif`/`.tiff` files. `--model` accepts `MDV6-yolov9-c/e`, `MDV6-yolov10-c/e`, and `MDV6-rtdetr-c` (default `MDV6-yolov9-c`); `--device` takes `cuda:0`, `cpu`, or `mps` (auto-detected if omitted). The same CLI exposes `train`, `validate`, and `inference` for fine-tuning. Full reference: [CLI guide](https://microsoft.github.io/MegaDetector/cli/).


## What Does MegaDetector Output Look Like?

MegaDetector returns one record per image: the file path plus a list of detections, each carrying a category (`animal`, `person`, or `vehicle`), a confidence score from 0 to 1, and a bounding box as `[x1, y1, x2, y2]` pixel coordinates.

```json
[
  {
    "file": "images/IMG_0001.jpg",
    "detections": [
      { "category": "animal", "confidence": 0.93, "bbox": [102.4, 88.1, 540.7, 470.2] }
    ]
  }
]
```

Only detections at or above your threshold are kept. When run from the CLI, MegaDetector also prints a short summary, images processed, total detections, and how many images contain at least one animal, so you can sanity-check a batch at a glance. This JSON feeds directly into review tools such as Timelapse or into a downstream species classifier. Full schema: [Output Format guide](https://microsoft.github.io/MegaDetector/output_format/).


## How Accurate Is MegaDetector?

Accuracy depends on your data and threshold, so the honest answer is always: **test it on your own images before trusting any number.** On the AI for Good Lab's validation sets, the larger V6 variants report animal recall above 82%, and the compact `MDV6-yolov10-c` reaches comparable accuracy at 2% of V5's parameter count. MegaDetector generalizes well across ecosystems because it was trained on a large, geographically diverse dataset, and it performs best on large mammals in open habitat. See the [Model Zoo](https://microsoft.github.io/MegaDetector/model_zoo/) for per-variant recall and mAP50.


## What Confidence Threshold Should I Use?

Start at **0.2**, the CLI default, and tune from there. Most projects use a threshold between **0.15 and 0.3** for the animal category. Lower values catch more true animals (higher recall) at the cost of more false positives on vegetation and lighting artifacts; higher values trim false positives but risk dropping low-confidence real detections. Because calibration varies by ecosystem, label a small sample and pick the threshold that balances missed animals against review effort for *your* data.


## What Are MegaDetector's Limitations?

MegaDetector is accurate across many terrestrial ecosystems, but it is not perfect. Very small or distant animals, heavily camouflaged species, and unusual camera angles tend to produce lower confidence and can be missed. Aquatic, overhead/aerial, and acoustic monitoring fall outside its scope. Those are handled by sibling models ([MegaDetector-Sonar](https://github.com/microsoft/MegaDetector-Sonar), [MegaDetector-Overhead](https://github.com/microsoft/MegaDetector-Overhead), and [MegaDetector-Acoustic](https://github.com/microsoft/MegaDetector-Acoustic)). If your dataset is atypical, measure recall on a labeled sample before relying on it at scale.


## Can MegaDetector Identify Species?

MegaDetector finds animals but doesn't identify their species. For species ID, run a two-stage pipeline:

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

### SPARROW Studio

SPARROW Studio is a unified desktop application by the AI for Good Lab built on PyTorch-Wildlife:

- Run MegaDetector and species classifiers through a graphical interface
- Manage camera-trap data locally or in the cloud
- Annotate, analyze, and visualize detection results
- Supports bioacoustics and overhead wildlife imagery

Windows installer: [Download from Zenodo](https://zenodo.org/records/19687738/files/SPARROW%20Studio%20Installer.msi?download=1) (signed). Mac and Linux builds in progress.

### AddaxAI (formerly EcoAssist)

[AddaxAI](https://addaxdatascience.com/addaxai/) is a third-party desktop tool for running MegaDetector with batch processing, annotation, and results visualization. Windows, macOS, and Linux.

### Hugging Face Space

[Upload images and run MegaDetector in your browser](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife), no installation required.


## How Does MegaDetector Fit Into Camera-Trap Software?

Camera-trap analysis has three layers: **detection** (filtering blanks and finding animals, MegaDetector's job), **review** (human verification and annotation), and **analysis** (occupancy, activity, and density modeling). MegaDetector sits in the detection layer and hands its output to the others.

| Tool | Layer | Runs MegaDetector | Code required |
| --- | --- | --- | --- |
| MegaDetector | Detection |, | Python or CLI |
| AddaxAI / SPARROW Studio | Detection (GUI) | Yes | No |
| Timelapse | Review | Imports MD output | No |
| Wildlife Insights | Cloud detect + review | Cloud pipeline | No |
| CamtrapR | Analysis (R) | No | R |

For how these tools fit together, see [Camera-Trap Software and Tools](https://microsoft.github.io/MegaDetector/camera-trap-software/); for the wider picture on AI in camera-trap workflows, see [Camera-Trap AI](https://microsoft.github.io/MegaDetector/camera-trap-ai/).


## Part of the Biodiversity Ecosystem

MegaDetector is one model in a larger open-source ecosystem from the AI for Good Lab. Each project lives in its own repository, with the [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) umbrella tying them together.

| Repo | Purpose |
| --- | --- |
| [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) | The umbrella repository, documentation hub for the AI for Good Lab's biodiversity work |
| [microsoft/Pytorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife) | The collaborative deep learning framework that hosts MegaDetector, species classifiers (AI4G Amazon Rainforest, AI4G Snapshot Serengeti, DeepFaune), HerdNet, PW-Engine (a Rust-based inference core), and demo notebooks |
| [microsoft/SPARROW](https://github.com/microsoft/SPARROW) | Solar-Powered Acoustic and Remote Recording Observation Watch, the AI-enabled edge device that runs MegaDetector in remote field locations |
| [microsoft/MegaDetector-Acoustic](https://github.com/microsoft/MegaDetector-Acoustic) | Bioacoustic models for audio-based wildlife monitoring |
| [microsoft/MegaDetector-Classifier](https://github.com/microsoft/MegaDetector-Classifier) | Camera-trap species classification fine-tuning, adapt classifiers to your own datasets and geographic regions |
| [microsoft/MegaDetector-Overhead](https://github.com/microsoft/MegaDetector-Overhead) | Point-based detection models for overhead and aerial imagery |
| [microsoft/MegaDetector-Sonar](https://github.com/microsoft/MegaDetector-Sonar) | Sonar-based wildlife detection for aquatic monitoring |
| SPARROW Studio | The desktop application that wraps it all in a graphical interface |

MegaDetector is the entry point for most users. SPARROW Studio is the full platform. SPARROW is the field-hardened edge device.


## Organizations Using MegaDetector

MegaDetector is used by more than 80 organizations worldwide, including government agencies, universities, NGOs, museums, and technology platforms. A selection of adopters named in the [Biodiversity collaborators list](https://microsoft.github.io/Biodiversity/collaborators/):

<!-- ATTESTED IN THIS REPO -->
**Government**: Arizona DEQ, Idaho Fish & Game, Oregon DFW, Michigan DNR, Parks Canada (Banff), U.S. Fish & Wildlife Service (multiple refuges), National Park Service, Canadian Wildlife Service

**Conservation NGOs**: The Nature Conservancy, Island Conservation, Wildlife Protection Solutions, Australian Wildlife Conservancy, RSPB, CPAWS, SPEA, Felidae Conservation Fund

**Universities**: UCLA, University of Washington, UBC, University of Florida, University of Idaho, UNSW Sydney, Macquarie University, University of Saskatchewan, Washington State University, Bangor University, Tel Aviv University, TU Berlin, Wildlife Institute of India

**Museums & Zoos**: American Museum of Natural History, Smithsonian, Woodland Park Zoo, San Diego Zoo Wildlife Alliance, Taronga Conservation Society

**Platforms**: TrapTagger, WildTrax, Camelot, Animl, Wildlife Observer Network, OCAPI, WildePod

See the [full list](https://microsoft.github.io/Biodiversity/collaborators/) on the Biodiversity documentation site.
<!-- /ATTESTED -->
<!-- APPROVED-EXTERNAL: append reviewed organizations below this line -->


## Do I Need a GPU?

No, MegaDetector runs on a CPU. A CUDA-capable NVIDIA GPU delivers a **10–50× speedup** and is strongly recommended once you are processing tens of thousands of images, but it is not required to get started. The compact V6 variants (`MDV6-yolov10-c`, `MDV6-yolov9-c`) are designed specifically for low-budget and edge hardware, including the solar-powered [SPARROW](https://github.com/microsoft/SPARROW) field unit, so a modern laptop is enough for many projects. If a GPU is present, the CLI and the Python API detect and use it automatically; pass `--device cpu` to force CPU.


## How Fast Is MegaDetector?

| Hardware | Model | Approximate Speed |
| --- | --- | --- |
| NVIDIA RTX 3090 | MDV6-yolov10-c (2.3M) | ~100–200 images/sec |
| NVIDIA RTX 3090 | MDV6-yolov10-e (29.5M) | ~30–60 images/sec |
| Modern CPU (no GPU) | MDV6-yolov10-c (2.3M) | ~2–5 images/sec |
| Google Colab (free GPU) | Any V6 variant | ~10–50 images/sec |

At 50 images/sec on a GPU, **one million images takes about 5.5 hours**; on CPU with the compact model, about 3.9 days. Even the largest V6 variant outruns the 139.9M-parameter V5, and the compact build is roughly 2% its size.


## Fine-Tuning

MegaDetector V6 ships with a fine-tuning pipeline (built on the
[ultralytics](https://github.com/ultralytics/ultralytics) framework) so you can
adapt a V6 model to your own camera-trap dataset. Fine-tuning is useful when
the off-the-shelf V6 models miss animals that look different from the training
distribution, for example, an under-represented species, a specific
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

- `MDV6-yolov9-c`, compact YOLOv9
- `MDV6-yolov9-e`, extra-large YOLOv9
- `MDV6-yolov10-c`, compact YOLOv10 (2.3M params)
- `MDV6-yolov10-e`, extra-large YOLOv10
- `MDV6-rtdetr-c`, compact RT-DETR

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
| V4.1 | 2020 | Faster R-CNN |, | Added vehicle class |
| V3 | 2019 | Faster R-CNN |, | Added human class |
| V2 | 2018 | Faster R-CNN |, | First public release |


## MegaDetector V5 and Earlier

For MegaDetectorV5 model weights and earlier versions, see the [archive branch](https://github.com/microsoft/Biodiversity/tree/archive) of the Biodiversity repository (formerly `microsoft/CameraTraps`).

MegaDetector V1–V5 were originally developed by **Dan Morris** at Microsoft. The V5 weights load directly through PyTorch-Wildlife, so existing V5 workflows keep running.


## Our Commitment

At the core of our mission is the desire to create a harmonious space where conservation scientists from all over the globe can unite, to share, grow, and use datasets and deep learning architectures for wildlife conservation. We've been inspired by the potential and capabilities of MegaDetector, and we deeply value its contributions to the community. We remain committed to supporting, maintaining, and developing MegaDetector, ensuring its continued relevance, expansion, and utility.


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

For framework-level changes (PyTorch-Wildlife API, classifiers, demo notebooks), see [microsoft/Pytorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife). For ecosystem-wide questions, see the [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) umbrella.

For questions, feature requests, or to report how MegaDetector worked on your data:
- **Email**: [zhongqimiao@microsoft.com](mailto:zhongqimiao@microsoft.com)
- **Discord**: [![Discord](https://img.shields.io/badge/any_text-Join_us!-blue?logo=discord&label=Discord)](https://discord.gg/TeEVxzaYtm)
- **GitHub Discussions**: [microsoft/Biodiversity/discussions](https://github.com/microsoft/Biodiversity/discussions)


## License

The MegaDetector **code** in this repository is released under the [MIT License](LICENSE). The **model weights** carry per-variant licenses, MIT, Apache-2.0, or AGPL-3.0 depending on the variant, so check the license of the specific model you deploy. See the [Model Zoo](https://microsoft.github.io/MegaDetector/model_zoo/) for each variant's license.
