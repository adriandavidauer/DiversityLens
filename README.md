# DiversityLens

DiversityLens is a command-line auditing tool for inspecting demographic patterns in face image and video datasets before they are used in AI training, evaluation, or social robotics research.

The tool scans a dataset directory, detects faces, estimates demographic attributes with DeepFace, exports structured results to CSV, and generates an interactive HTML visualization of the observed distributions.

## Motivation

Datasets used in computer vision and social robotics can contain hidden demographic imbalances. If these imbalances are not inspected early, downstream systems may perform unevenly across different groups or reproduce narrow assumptions about who is represented in the data.

DiversityLens supports dataset-level auditing before training or evaluation. Its purpose is not to certify that a model is fair, but to help researchers identify representation patterns, document dataset limitations, and make better decisions about data collection or dataset suitability.

## Features

- Scans directories for supported image and video files
- Estimates age, gender, and race attributes for detected faces
- Supports configurable DeepFace detector backends
- Filters detections by configurable confidence threshold
- Exports demographic analysis results to CSV
- Generates an interactive HTML dashboard
- Includes tests and MkDocs-based project documentation

## Installation

Clone the repository and install the project dependencies:

```bash
git clone https://github.com/adriandavidauer/DiversityLens.git
cd DiversityLens
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Usage

Run DiversityLens on a dataset directory:

```bash
diversitylens --path /path/to/dataset --output results/Demographic_Results.csv
```

The command can also be run directly from the source module:

```bash
python -m src.main --path /path/to/dataset --output results/Demographic_Results.csv
```

Common options:

```bash
diversitylens \
  --path /path/to/dataset \
  --output results/Demographic_Results.csv \
  --detector-backend retinaface \
  --min-confidence 0.9 \
  --video-frame-step 1
```

## Supported Formats

- Images: `.jpg`, `.jpeg`, `.png`
- Videos: `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`
- Archives: `.zip`, `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tar.xz`

## Project Structure

```text
DiversityLens/
|-- src/                  # Core implementation
|-- tests/                # Unit tests and test data
|-- docs/                 # MkDocs documentation
|-- data/                 # Local dataset directory
|-- images/               # Image dataset or extracted frames
|-- results/              # Generated analysis outputs
|-- pyproject.toml        # Project metadata and packaging config
|-- requirements.txt      # Runtime dependencies
|-- requirements_doc.txt  # Documentation dependencies
|-- mkdocs.yml            # Documentation configuration
```

## Documentation

The documentation is built with MkDocs:

```bash
pip install -r requirements_doc.txt
mkdocs serve
```

## Testing

Run the test suite with:

```bash
pytest
```

## Ethical Note

DiversityLens uses automated demographic estimation and should be treated as an auditing aid rather than a source of ground-truth identity labels. The resulting estimates are approximate, model-dependent, and should be interpreted carefully, especially when used in research involving human subjects or socially sensitive categories.

## Authors & Acknowledgments

- **Veli Ates** - Author and lead developer, developed as part of an M.Sc. thesis at DFKI (2025-2026).
- **Adrian Auer** - Thesis supervisor, DFKI Robotics Innovation Center.

This project was developed as part of the author's M.Sc. thesis at the German Research Center for Artificial Intelligence (DFKI).

## License

This project is licensed under the MIT License. See `LICENSE` for details.
