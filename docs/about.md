# About

## DiversityLens

DiversityLens was developed as part of a Master's thesis at Fachhochschule Dortmund in collaboration with the DFKI Robotics Innovation Center in Bremen.

## Purpose

The tool is designed exclusively as a dataset auditing tool for improving transparency and fairness in AI systems. It helps users inspect whether image and video datasets contain demographic imbalances before those datasets are used for model training, evaluation, or human-robot interaction research.

DiversityLens is not intended for individual identification, surveillance, or any form of personal profiling. Its demographic labels are aggregate estimates for dataset-level analysis and should be interpreted as signals for auditing, not as definitive statements about individual identity.

## Application Context

The project is motivated by datasets used in computer vision and social robotics. In these contexts, unbalanced datasets can influence how perception systems detect and respond to different people. Auditing a dataset before training makes it possible to identify representation gaps, improve dataset composition, and document limitations before those limitations become embedded in a downstream system.

## Technology Stack

- **DeepFace** — Face detection and demographic estimation
- **RetinaFace** — Default face detection backend, selected to prioritize audit reliability
- **Bokeh** — Interactive visualization dashboard
- **pandas** — Data processing and age group binning
- **OpenCV** — Video frame extraction

The detector backend is configurable because detection quality affects the audit. Backend selection can improve the reliability of the results, but it remains a technical part of the auditing pipeline rather than the main research objective.

## Author

Veli Ates — Master's student in Embedded Systems Engineering (Computer Science track), Fachhochschule Dortmund.

## Supervisor

Adrian Auer — DFKI Robotics Innovation Center, Bremen.

## License

This project is licensed under the MIT License. See the [License](license.md) page for details.
