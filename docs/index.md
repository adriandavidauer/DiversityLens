# DiversityLens

DiversityLens is an automated command-line tool for auditing the demographic composition of large-scale image and video datasets.

## Overview

Modern computer vision models require large datasets for training, but these datasets often contain hidden demographic imbalances that can lead to biased AI systems. DiversityLens addresses this problem by providing an end-to-end pipeline that:

1. **Scans** a dataset directory for all supported image and video files
2. **Analyzes** each detected face for age, gender, and race using DeepFace
3. **Exports** structured results to CSV
4. **Visualizes** demographic distributions through an interactive HTML dashboard

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

## Supported Formats

**Images:** `.jpg`, `.jpeg`, `.png`

**Videos:** `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`

**Archives (auto-extracted):** `.zip`, `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tar.xz`
