---
title: "Contributing to MegaDetector & Getting Support"
description: "How to contribute to MegaDetector and get help: filing issues, submitting pull requests, reporting security concerns, and reaching the community."
tags:
  - contribute to megadetector
  - megadetector support
  - report a bug
  - megadetector community
  - security
---

# Contributing & Support

MegaDetector is open source and community-driven. This page explains where to file things, how to contribute changes, and how to get help.

## Where does my issue belong?

The MegaDetector ecosystem spans a few repositories, so routing your report to the right place gets it answered faster:

| Your topic | Repository |
| --- | --- |
| MegaDetector models, the CLI, fine-tuning, these docs | [microsoft/MegaDetector](https://github.com/microsoft/MegaDetector) |
| The PyTorch-Wildlife framework, classifiers, demo notebooks | [microsoft/Pytorch-Wildlife](https://github.com/microsoft/Pytorch-Wildlife) |
| Ecosystem-wide questions and discussion | [microsoft/Biodiversity](https://github.com/microsoft/Biodiversity) |

## Reporting bugs and requesting features

Open an issue on [microsoft/MegaDetector/issues](https://github.com/microsoft/MegaDetector/issues). Helpful reports include the model variant and threshold you used, the command or code that triggered the problem, and a sample of the output. If you are reporting how MegaDetector performed on your data, good or bad, that feedback is genuinely useful for improving the models.

## Submitting changes

1. Fork the repository and create a branch for your change.
2. Make your edits, for code, the [Repository Architecture](architecture.md) page explains the package layout; for docs, the [Developer Guide](build_mkdocs.md) covers building the site locally.
3. Open a pull request describing the change and the motivation.

Documentation improvements are welcome and are often the easiest first contribution.

## Reporting security issues

Please do **not** report security vulnerabilities through public GitHub issues. Follow the process in the repository's [SECURITY.md](https://github.com/microsoft/MegaDetector/blob/main/SECURITY.md), which routes reports to the Microsoft Security Response Center (MSRC).

## Getting help

- **Discord**, [join the PyTorch-Wildlife community](https://discord.gg/TeEVxzaYtm)
- **GitHub Discussions**, [microsoft/Biodiversity/discussions](https://github.com/microsoft/Biodiversity/discussions)
- **Email**, [zhongqimiao@microsoft.com](mailto:zhongqimiao@microsoft.com)

## Next steps

- [Repository Architecture](architecture.md): orient yourself in the codebase
- [Developer Guide](build_mkdocs.md): build and preview the docs
- [FAQ](faq.md): common questions before you file an issue
