---
description: "Install MegaDetector via PyTorch-Wildlife for camera-trap wildlife detection. Supports pip, conda, and Docker on Windows, macOS, and Linux with optional CUDA GPU acceleration."
tags:
  - MegaDetector installation
  - pip install PytorchWildlife
  - conda environment
  - wildlife AI setup
  - PyTorch-Wildlife
  - GPU CUDA setup
---

# Installation

MegaDetector is installed as part of the [PyTorch-Wildlife](https://github.com/microsoft/PytorchWildlife) framework.

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


## Verify Installation

```python
from PytorchWildlife.models import detection as pw_detection

model = pw_detection.MegaDetectorV6()
print("MegaDetector loaded successfully.")
```

Weights are downloaded automatically on first use.


## Try Without Installing

- [Hugging Face demo](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife) — upload images in your browser
- [Google Colab notebook](https://colab.research.google.com/drive/1rjqHrTMzEHkMualr4vB55dQWCsCKMNXi?usp=sharing) — free cloud GPU


## Next Steps

- [Model Zoo](model_zoo.md) — choose the right MDV6 variant for your hardware
- [Training Guide](training_guide.md) — fine-tune MegaDetector on your own data
