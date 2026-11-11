# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Set DeepFace detector backend default to `retinaface` (configurable from CLI)
- Added active confidence filtering (`--min-confidence`, default `0.9`) for face detections
- Added `--video-frame-step` documentation for configurable video-frame sampling
- Implemented automatic archive extraction during dataset traversal
- Updated documentation to emphasize dataset-level auditing, social robotics risk prevention, and the supporting role of backend selection
- Expanded automated tests for archive handling and confidence filtering
- Dashboard charts show the share in percent next to every count (#37)
- The dashboard embeds BokehJS (inline resources), so it opens offline without a CDN

### Fixed
- Video frames are passed to DeepFace in BGR order; the BGR-to-RGB conversion in the video path swapped the colour channels
- Dashboard age-group labels now match the bins (`0-6`, `7-13`, ..., `70+`); ages of 100 and above are no longer dropped
- The dashboard is saved next to its CSV as `<csv-name>_dashboard.html` instead of a fixed `dashboard.html`, so runs no longer overwrite each other (#36)

## [0.2.0] - 2026-03-09

### Changed
- Switched face detection backend from OpenCV (Haar Cascade) to RetinaFace for higher accuracy
- Added confidence threshold filter (0.9) to eliminate false positive face detections

### Added
- Version dropdown support for documentation using mike
- CHANGELOG.md for tracking project changes

## [0.1.0] - 2025-12-01

### Added
- Initial release of DiversityLens
- Face detection and demographic estimation (age, gender, race) using DeepFace
- Support for image and video analysis
- CSV export of demographic results
- Interactive dashboard visualization using Bokeh
- MkDocs documentation with Material theme
- Archive auto-extraction during directory traversal
- Automated tests and coverage workflow
- Code quality enforcement with Ruff
