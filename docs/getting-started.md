---
title: "Getting Started with MegaDetector: First Steps for Camera-Trap AI"
description: "Getting started with MegaDetector: decide whether it fits, pick a no-code or pip path, run your first camera-trap batch, and read the detection output."
slug: getting-started
tags:
  - getting started
  - MegaDetector
  - camera trap AI
  - quickstart
  - run MegaDetector
---

# Getting Started with MegaDetector

New to MegaDetector? This page is the short path from "I have a folder of camera-trap images" to "I have detections I can act on." It walks four steps: decide whether the model fits your project, choose how you want to run it, process a first small batch, and read the results. Each step links to the deeper reference page when you are ready for detail.

If you only want the three-line code snippet, the [Overview](index.md#quick-start) has it. If you are weighing whether to adopt the model at all, the rest of this page is written for you.

## Is MegaDetector right for my project?

MegaDetector finds animals, people, and vehicles in camera-trap photos and draws a scored box around each one. It is a detector, so it tells you that something is present, not which species it is. Pairing it with a classifier adds species identity later (see Step 4). Because a single detector travels across habitats far better than any region-specific species model, the same weights work whether your cameras sit in savanna, boreal forest, or rainforest.

It is a strong fit when:

- A large image backlog where most frames are empty is the thing slowing your research down.
- Your project spans several regions or ecosystems and you want one model for all of them.
- You need a quick, dependable first pass before expert reviewers spend time on the images.
- You are deploying on low-power field hardware such as a [SPARROW](https://github.com/microsoft/SPARROW) unit.

Some inputs need a different tool in the family rather than MegaDetector itself: underwater or sonar imagery, overhead and aerial views, and audio recordings each have a dedicated sibling project linked from the [Camera-Trap AI](camera-trap-ai.md#when-to-use-megadetector) guide. Very small, well-camouflaged, or under-represented species can also score low, so test on a labeled sample before you trust the model at scale. The [FAQ](faq.md#what-species-does-megadetector-support) covers these caveats in one place.

## Step 1: Pick how you want to run it

There is no single "correct" entry point. Choose the one that matches how much code you want to write and what hardware you have.

- **No code, graphical app.** [SPARROW Studio](https://github.com/microsoft/SPARROW), the AI for Good Lab desktop application, and [AddaxAI](https://addaxdatascience.com/addaxai/) (formerly EcoAssist) both run MegaDetector through a point-and-click interface with batch processing and visualization. The [Hugging Face Space](https://huggingface.co/spaces/ai-for-good-lab/pytorch-wildlife) runs it in a browser tab with nothing to install.
- **Python or the command line.** Install the package and call it from a few lines of Python, or use the `megadetector` command. This is the most flexible path and the rest of this page assumes it.
- **Free cloud GPU.** The [Google Colab notebook](https://colab.research.google.com/drive/1rjqHrTMzEHkMualr4vB55dQWCsCKMNXi?usp=sharing) gives you a hosted GPU when your own machine has none.

For a fuller side-by-side of the surrounding tools, see [Camera-Trap Software and Tools](camera-trap-software.md).

## Step 2: Run a first small batch

Start small. Run the model on a handful of images first and check that the results look sane before you scale up. Install the framework:

```bash
pip install PytorchWildlife
```

Then run the current release, MegaDetectorV6, over a folder. The weights download themselves the first time:

```python
from PytorchWildlife.models import detection as pw_detection

model = pw_detection.MegaDetectorV6()
results = model.batch_image_detection("path/to/a_few_images/")
```

A laptop CPU handles roughly two to five images per second with the compact variant, which is plenty for a trial run of a few hundred frames. No GPU is required to begin. If you prefer to stay out of Python entirely, the same job runs from the terminal:

```bash
megadetector detect --input ./a_few_images/ --output results.json --model MDV6-yolov10-e
```

The [Installation](installation.md) page covers conda environments and GPU setup, and the [CLI reference](cli.md) lists every flag.

## Step 3: Read the output

MegaDetector writes one record per image. Each record holds the file path and a list of detections, and every detection carries three things:

- `category`: `animal`, `person`, or `vehicle`.
- `confidence`: a score from 0 to 1.
- `bbox`: the box as `[x1, y1, x2, y2]` pixel coordinates.

You apply a confidence threshold to decide what counts. A value between 0.15 and 0.3 on the animal category suits most datasets: it keeps almost every real animal while letting through a few false hits on swaying vegetation or odd lighting. Anything under your threshold is, in effect, a blank you can set aside, which is what makes the first pass clear so much of the review queue. The [Output Format](output_format.md) reference documents the full schema, and the [Camera-Trap AI](camera-trap-ai.md#filtering-blank-camera-trap-images) guide explains the blank-filtering workflow.

## Step 4: Scale up and add species

Once a trial batch looks right, the same code scales to a full deployment. A GPU changes the economics: at around fifty images per second, a million-image set finishes in roughly five and a half hours, against several days on CPU. Pick a heavier variant for accuracy or a compact one for speed using the guidance in the [Model Zoo](model_zoo.md).

Two common next steps:

- **Identify species.** Feed each MegaDetector box into a downstream classifier. PyTorch-Wildlife ships several, and [MegaDetector-Classifier](https://github.com/microsoft/MegaDetector-Classifier) lets you fine-tune one for your own region. The [Overview](index.md#species-classification) shows the two-stage pipeline in code.
- **Fine-tune the detector.** If your species or habitats are thin in the base model, the [fine-tuning guide](training_guide.md) walks through preparing data and running `megadetector train`.

Downstream review and analysis tools read MegaDetector results directly, including Timelapse, Wildlife Insights, and CamtrapR; the [software guide](camera-trap-software.md) shows where each one fits.

## Get help

- **GitHub Issues:** [microsoft/MegaDetector/issues](https://github.com/microsoft/MegaDetector/issues) for bugs and feature requests.
- **Discord:** [the PyTorch-Wildlife community server](https://discord.gg/TeEVxzaYtm).
- **Email:** [zhongqimiao@microsoft.com](mailto:zhongqimiao@microsoft.com).

Still deciding? The [FAQ](faq.md) answers the most common questions about accuracy, GPU needs, licensing, and the difference between V5 and V6.
