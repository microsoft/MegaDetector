---
title: "Install MegaDetector: pip, Conda, and GPU Setup"
description: "Install MegaDetector via PyTorch-Wildlife for camera-trap detection: pip, conda, and Docker on Windows, macOS, and Linux, with optional CUDA GPU support."
tags:
  - MegaDetector installation
  - pip install PytorchWildlife
  - conda environment
  - wildlife AI setup
  - PyTorch-Wildlife
  - GPU CUDA setup
---

# Installation

MegaDetector is installed as part of the [PyTorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife) framework. A single `pip install PytorchWildlife` pulls in the latest MegaDetector V6, and the model weights download automatically the first time you run a detection.

```bash
pip install PytorchWildlife
```

**Requirements:**

- Python 3.8+ (3.10+ recommended)
- Optional: NVIDIA GPU with CUDA for 10–50x speedup


## Conda

```bash
conda create -n megadetector python=3.10 -y
conda activate megadetector
pip install PytorchWildlife
```


## GPU Setup

If PyTorch installed without CUDA support, install the GPU-enabled build manually:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Then reinstall PyTorch-Wildlife:

```bash
pip install PytorchWildlife
```


## Install from Source (CLI and Fine-Tuning)

To use the local `megadetector` command-line tool, or to fine-tune V6 weights on your own dataset, install this repository in editable mode:

```bash
git clone https://github.com/microsoft/MegaDetector
cd MegaDetector
pip install -e .
```

This installs the `megadetector_core` package and registers the `megadetector` command (`detect`, `train`, `validate`, `inference`). The `pyproject.toml` declares the full dependency set, so there is no separate `requirements.txt`.

Prefer conda for a source install? The repository ships an `environment.yaml` you can build from directly:

```bash
conda env create -f environment.yaml
conda activate megadetector
pip install -e .
```

Confirm the CLI is on your path:

```bash
megadetector --help
```

See the [CLI reference](cli.md) for the full command surface, and the [Repository Architecture](architecture.md) for how the `megadetector_core` package is organized.


## Verify Installation

```python
from PytorchWildlife.models import detection as pw_detection

model = pw_detection.MegaDetectorV6()
print("MegaDetector loaded successfully.")
```

Weights are downloaded automatically on first use.


## Try Without Installing

- [Hugging Face demo](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife): upload images in your browser
- [Google Colab notebook](https://colab.research.google.com/drive/1rjqHrTMzEHkMualr4vB55dQWCsCKMNXi?usp=sharing): free cloud GPU


## Next Steps

- [CLI Reference](cli.md): run detection from the command line
- [Model Zoo](model_zoo.md): choose the right MDV6 variant for your hardware
- [Training Guide](training_guide.md): fine-tune MegaDetector on your own data
