---
title: "MegaDetector CLI, detect, train, validate, inference"
description: "MegaDetector CLI reference: run detection on camera-trap images with the megadetector detect command, plus train, validate, and inference subcommands."
tags:
  - megadetector cli
  - megadetector detect
  - command line
  - batch detection
  - camera trap AI
---

# MegaDetector CLI

The `megadetector` command-line tool runs MegaDetector on a single image or a whole folder without writing any Python. It ships with the editable install of this repository and wraps the same V6 models exposed by the Python API.

## Install the CLI

Installing the repository from source registers the CLI:

```bash
git clone https://github.com/microsoft/MegaDetector
cd MegaDetector
pip install -e .
```

This installs the `megadetector_core` package and the `megadetector` command. Verify it:

```bash
megadetector --help
```

## Detect

`megadetector detect` is the command you will use most. It accepts either a single image or a directory (scanned recursively for `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tif`, and `.tiff` files).

```bash
# Single image, print results to the terminal
megadetector detect --input photo.jpg

# A folder, write results to JSON, pick a model and threshold
megadetector detect --input ./images/ --output results.json --model MDV6-yolov10-e --threshold 0.2

# Force CPU
megadetector detect --input ./images/ --device cpu
```

### Options

| Flag | Default | Description |
| --- | --- | --- |
| `--input`, `-i` | *(required)* | Path to an image file or a directory of images |
| `--output`, `-o` | *(stdout)* | Path to write JSON results; prints to the terminal if omitted |
| `--model`, `-m` | `MDV6-yolov9-c` | Model variant (see supported list below) |
| `--threshold`, `-t` | `0.2` | Minimum confidence to keep a detection |
| `--device`, `-d` | *(auto)* | `cuda:0`, `cpu`, or `mps`; auto-detects a GPU if omitted |

### Supported models

Five V6 variants are available to `--model`:

`MDV6-yolov9-c`, `MDV6-yolov9-e`, `MDV6-yolov10-c`, `MDV6-yolov10-e`, and `MDV6-rtdetr-c`.

The MIT and Apache-2.0 variants documented in the [Model Zoo](model_zoo.md) (for example `MDV6-apa-rtdetr-e`) are loaded through the PyTorch-Wildlife Python API rather than the CLI's `--model` flag.

### What you get back

Each run writes a JSON list with one entry per image, holding a `file` path and a list of `detections`. When it finishes, the command prints a one-line summary: how many images were processed, the total number of detections, and how many images contain at least one animal. See the [Output Format](output_format.md) reference for the full schema.

## Fine-tuning subcommands

The same CLI drives the fine-tuning workflow, each subcommand reading a YAML config:

```bash
megadetector train    --config ./config.yaml
megadetector validate --config ./config.yaml
megadetector inference --config ./config.yaml
```

`--config` defaults to `./config.yaml`. For the data layout, the full config schema, and the Python API equivalents, see the [Training Guide](training_guide.md).

## Next steps

- [Output Format](output_format.md): interpret the JSON MegaDetector produces
- [Model Zoo](model_zoo.md): every variant, with recall, mAP50, and license
- [Installation](installation.md): environment setup and GPU configuration
