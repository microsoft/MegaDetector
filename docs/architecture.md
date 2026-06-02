---
title: "MegaDetector Repository Architecture"
description: "How the MegaDetector repository is organized: the megadetector_core package, the megadetector CLI entry point, model wrappers, and the fine-tuning pipeline."
tags:
  - megadetector repo structure
  - megadetector_core
  - package layout
  - megadetector architecture
  - contributing
---

# Repository Architecture

This page orients contributors and integrators to how the `microsoft/MegaDetector` repository is laid out and how its pieces fit together.

## Package and entry point

MegaDetector installs as **`megadetector-core`**, with its source under `src/megadetector_core/`. Installing the repository registers a single console command:

```
megadetector = "megadetector_core.cli:main"
```

So `megadetector detect …` on the command line maps to `main()` in `megadetector_core/cli.py`. The package metadata, dependencies, and entry point all live in `pyproject.toml`; there is no separate `requirements.txt`.

## Source layout

| Path | Responsibility |
| --- | --- |
| `src/megadetector_core/cli.py` | Argument parsing and the `detect`, `train`, `validate`, and `inference` subcommands |
| `src/megadetector_core/detector.py` | Thin wrappers around PyTorch-Wildlife's `MegaDetectorV6` (and `MegaDetectorV5` for backward compatibility) |
| `src/megadetector_core/training.py` | Config-driven fine-tuning, validation, and inference, delegating to the underlying training framework |
| `src/megadetector_core/training_utils.py` | Resolves and caches model weights, downloading them when they are not already present |
| `examples/config_training.yaml` | Reference fine-tuning config you copy and edit |
| `environment.yaml` | Conda environment definition for setup from source |

## How it relates to PyTorch-Wildlife

MegaDetector models are served through the [PyTorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife) framework. The wrappers in `detector.py` instantiate PyTorch-Wildlife's `MegaDetectorV6`, so the CLI, the Python API, and PyTorch-Wildlife all run the same weights. Model files are downloaded on first use and cached locally, so no weights are committed to this repository.

## The fine-tuning path

`megadetector train|validate|inference` each read a YAML config that points at your dataset and hyperparameters, then call into `training.py`. Outputs (weights, plots, metrics) are written under `./runs/`, and a fine-tuned `.pt` file can be loaded straight back into `MegaDetectorV6(weights="path/to/best.pt")`. The full schema and data layout are documented in the [Training Guide](training_guide.md).

## Documentation

Docs are built with MkDocs Material from the `docs/` directory. To build or preview them locally, see the [Developer Guide](build_mkdocs.md).

## Next steps

- [Contributing & Support](contributing.md): how to file issues and submit changes
- [CLI reference](cli.md): the commands exposed by `megadetector_core`
- [Training Guide](training_guide.md): fine-tune a V6 model on your own data
