---
title: "MegaDetector Fine-Tuning Guide: Train Custom V6 Models"
description: "MegaDetector fine-tuning guide: train custom MegaDetectorV6 detection models (YOLOv9, YOLOv10, RT-DETR) on your own camera-trap wildlife data."
tags:
  - MegaDetector fine-tuning
  - MegaDetectorV6
  - custom wildlife detection
  - ultralytics training
  - camera trap model training
  - YOLOv9
  - YOLOv10
---

# MegaDetector Model Fine-tuning Guide

← Back to [main README](https://github.com/microsoft/MegaDetector/blob/main/README.md).
> [!TIP]
> This guide covers fine-tuning MegaDetectorV6 models on your own data. For general inference usage, see the [Overview](index.md) and [Model Zoo](model_zoo.md); for the `train`/`validate`/`inference` command surface used below, see the [CLI reference](cli.md), and for how the training code is organized, the [Repository Architecture](architecture.md).

This guide covers training and fine-tuning detection models for MegaDetector using the ultralytics framework. This module is designed to help both programmers and biologists train a detection model for animal identification. The output weights of this training process can be easily integrated with MegaDetector inference.

## Installation

Before you start, ensure you have Python installed on your machine. This project is developed using Python 3.10. If you're not sure how to install Python, you can find detailed instructions on the [official Python website](https://www.python.org/).

To install the required libraries and dependencies, follow these steps:

### Using pip (editable install from source)

```bash
pip install -e .
```

Run this from the repository root. The project's `pyproject.toml` lists all
required runtime dependencies (PyTorch-Wildlife, ultralytics, munch, wget,
PyYAML, torch), so no separate `requirements.txt` is needed. The editable
install also exposes the `megadetector` command-line entry point used below.

### Using conda and `environment.yaml`

Create and activate a Conda environment with Python 3.10:

```bash
conda env create -f environment.yaml
conda activate megadetector-finetuning
```

## Data Preparation: Custom Camera-Trap Datasets

### Data Structure

The codebase is optimized for ease of use by non-technical users. For the code to function correctly, data should be organized as follows. Inside `data/`, create a subfolder `your_data/` including two subfolders: `images/` and `labels/`. The `images/` folder should have three subfolders named `test/`, `train/`, and `val/` for storing test, training, and validation images respectively. Similarly, the `labels/` folder should have subfolders `test/`, `train/`, and `val/` for the corresponding annotation files in txt format. Place a configuration file named `your_data.yaml` within the `data/` folder, alongside the `your_data/` folder.

Example directory structure:

```plaintext
project_root/
│
└── data/
   ├── your_data/
   |    ├── images/
   |    |    ├── test/
   |    │    ├── train/
   |    │    └── val/
   |    └── labels/ 
   |         ├── test/
   |         ├── train/
   |         └── val/
   └── your_data.yaml
```

### Data Configuration File Structure

To ensure the code works correctly, `your_data.yaml` file should be structured as follows. The `path` field should contain the relative path to your `your_data/` folder. The `train`, `val`, and `test` fields should point to the subdirectories within the `images/` folder where the training, validation, and test images are stored, respectively. For the classes, the `names` field should be a list where each class is assigned to a unique identifier number.

Example `data.yaml`:

```yaml
path: path/to/your_data
train: images/train
val: images/val
test: images/test

nc: 2  # number of classes
names: ['class_0', 'class_1']
```

### Annotations Structure

The `.txt` files inside each folder of `./data/labels/` must be structured containing each object on a separate line, following the format: `class x_center y_center width height`. The coordinates for the bounding box should be normalized in the xywh format, with values ranging from 0 to 1.

### Demo Data

You can download some example [demo data](https://zenodo.org/records/15376499/files/demo_data_det.zip?download=1) to test the codebase. Before using the data, make sure to decompress the zip file following the [data directory structure](#data-structure), and check if the `data` and `test_data` entries in the [config file](https://github.com/microsoft/MegaDetector/blob/main/examples/config_training.yaml) are pointing to the data directory. The testing demo data also has an annotation example showing how the preferred annotation format looks like.

## Detection Models Available for Fine-tuning

Below you find the models that you can use for fine-tuning, along with their respective names to use in the configuration file.

| Model | Name | License |
|---|---|---|
| MegaDetectorV6-Ultralytics-YoloV9-Compact | MDV6-yolov9-c | AGPL-3.0 |
| MegaDetectorV6-Ultralytics-YoloV9-Extra | MDV6-yolov9-e | AGPL-3.0 |
| MegaDetectorV6-Ultralytics-YoloV10-Compact | MDV6-yolov10-c | AGPL-3.0 |
| MegaDetectorV6-Ultralytics-YoloV10-Extra | MDV6-yolov10-e | AGPL-3.0 |
| MegaDetectorV6-Ultralytics-RtDetr-Compact | MDV6-rtdetr-c | AGPL-3.0 |

## Configuration

The shipped reference configuration is [`examples/config_training.yaml`](https://github.com/microsoft/MegaDetector/blob/main/examples/config_training.yaml). Copy it to a working location and edit it to match your dataset and training preferences:

```bash
cp examples/config_training.yaml ./config.yaml
```

The CLI accepts any path via `--config`; the examples below assume you saved your copy as `./config.yaml`. Below is a brief explanation of the parameters to help both technical and non-technical users understand their purposes:

### General Parameters

- `model`: The type of model used (YOLO or RTDETR). Default: YOLO
- `model_name`: The name of the model (see available names [here](#detection-models-available-for-fine-tuning)). Default: MDV6-yolov9-e
- `data`: Path to the dataset configuration file. Default: ./data/data_example.yaml
- `test_data`: Path to the test data directory. Default: ./data/data_example/images/test
- `task`: The task to perform (train, validation or inference). Default: train
- `exp_name`: The name of the experiment. Default: MDV6-yolov9e

### Training Parameters

- `epochs`: The total number of training epochs. Default: 20
- `batch_size_train`: The batch size for training. Default: 16
- `imgsz`: The image size. Default: 640
- `device_train`: The device ID for training. Default: 0
- `workers`: The number of workers. Default: 8
- `optimizer`: The optimizer to use. Default: auto
- `lr0`: The initial learning rate. Default: 0.01
- `patience`: The number of epochs to wait before stopping without improvement. Default: 5
- `save_period`: The period for saving the model. Default: 1
- `val`: Boolean value indicating whether to perform validation while training. Default: True
- `resume`: Boolean value indicating whether to resume training from weights. Default: False
- `weights`: Path to the weights file to resume training. Default: None

### Validation Parameters

- `save_json`: Boolean value indicating whether to save results as JSON. Default: True
- `plots`: Boolean value indicating whether to plot results. Default: True
- `device_val`: The device ID for validation. Default: 0
- `batch_size_val`: The batch size for validation. Default: 12

## Usage

After configuring your `config.yaml` file, you can start training your model by running:

### Training

```bash
megadetector train --config ./config.yaml
```

Or using the Python API:

```python
from megadetector_core.training import train
train(config_path='./config.yaml')
```

### Validation

```bash
megadetector validate --config ./config.yaml
```

Or using the Python API:

```python
from megadetector_core.training import validate
validate(config_path='./config.yaml')
```

### Inference

```bash
megadetector inference --config ./config.yaml
```

Or using the Python API:

```python
from megadetector_core.training import inference
inference(config_path='./config.yaml')
```

This command will initiate the training process based on the parameters specified in `config.yaml`. Make sure to monitor the output for any errors or important information regarding the training progress.

## Output

Once training is complete, the output weights will be saved in the `./runs/` directory according to the task and experiment name you configured in the `config.yaml`. These weights can be used for inference with MegaDetector.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue at [microsoft/MegaDetector/issues](https://github.com/microsoft/MegaDetector/issues) or join the community on [Discord](https://discord.gg/TeEVxzaYtm). For ecosystem-wide questions, see [microsoft/Biodiversity/discussions](https://github.com/microsoft/Biodiversity/discussions).
