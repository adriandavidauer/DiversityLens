# DiversityLens

DiversityLens is an automated command-line tool for auditing the demographic composition of large-scale image and video datasets before they are used in downstream AI systems.

## Overview

Modern computer vision and human-robot interaction systems often rely on large datasets of human faces. When these datasets contain hidden demographic imbalances, the resulting models may perform unevenly across groups, reproduce narrow assumptions about who is represented, or fail in ways that are only discovered after deployment. This is especially important for social robotics, where perception systems can influence how a robot detects, interprets, and responds to people in shared environments.

DiversityLens addresses this risk at the dataset stage. Its goal is not to prove that a model is fair after training, but to help researchers and developers inspect a dataset early enough to improve it, document its limitations, or decide that it is not suitable for a given use case. The tool provides an end-to-end auditing pipeline that:

1. **Scans** a dataset directory for all supported image and video files
2. **Estimates** age, gender, and race attributes for detected faces using DeepFace
3. **Exports** structured results to CSV
4. **Visualizes** demographic distributions through an interactive HTML dashboard

## Why Dataset Auditing Matters

Datasets used to train or evaluate social robot perception systems can shape how reliably those systems interact with different people. If a dataset overrepresents some groups and underrepresents others, a robot's perception pipeline may become less reliable for the people who are least visible in the training data. In practical terms, this can affect face detection, estimated demographic analysis, interaction quality, user trust, and the fairness of experimental results.

DiversityLens supports earlier intervention by turning a dataset into inspectable evidence. Instead of discovering representation problems only after training, users can review demographic distributions, identify missing or weakly represented groups, and make informed decisions about collecting additional data, balancing samples, changing dataset scope, or reporting known limitations.

## Backend Role

DiversityLens uses DeepFace for demographic estimation and supports configurable detector backends. The detector backend affects the quality of the audit because missed faces or false detections can distort the resulting distribution. For that reason, the default backend favors detection quality, and users can choose another backend when their dataset or runtime constraints require it.

Backend comparison is therefore a supporting technical concern rather than the main purpose of the project. A stronger backend can make the audit results more reliable, but the central contribution of DiversityLens is the dataset-level auditing workflow: finding, estimating, exporting, and visualizing demographic patterns so potential bias can be addressed before a dataset is used for training or evaluation.

## Quick Start

```bash
pip install diversitylens
diversitylens --path /path/to/dataset --output results.csv
```

## CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--path` | `tests/data` | Path to the dataset directory |
| `--output` | `Demographic_Results.csv` | Path to the output CSV file |
| `--detector-backend` | `retinaface` | DeepFace detector backend (e.g. `retinaface`, `opencv`, `mtcnn`) |
| `--min-confidence` | `0.9` | Minimum face confidence for keeping detections (`0` disables filtering) |
| `--video-frame-step` | `1` | Analyze every n-th video frame (`1` analyzes all frames) |

## Supported Formats

**Images:** `.jpg`, `.jpeg`, `.png`

**Videos:** `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`

**Archives (auto-extracted):** `.zip`, `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tar.xz`
