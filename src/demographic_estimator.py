"""
This module is responsible for estimating age, gender, and race using DeepFace.
It acts as a wrapper for the deep learning model.
"""

import logging
from pathlib import Path
from typing import Any

import cv2
from deepface import DeepFace

logger = logging.getLogger(__name__)


def analyze_image(image_path: str | Path) -> list[dict[str, Any]]:
    """
    Analyze an image for faces and return demographic info for each face found.

    :param image_path: Path to the image file.
    :return: List of dictionaries with demographic information for each face.
    """
    image_path = Path(image_path)
    if not image_path.is_file():
        logger.error(f"Image file not found: {image_path}")
        return []

    processed_faces = []
    img_str = str(image_path)
    results = DeepFace.analyze(
        img_path=img_str,
        actions=["age", "gender", "race"],
        detector_backend="retinaface",
        enforce_detection=False,
        silent=True,
    )
    if not isinstance(results, list):
        results = [results]
    for face in results:
        if "dominant_race" not in face:
            continue
        if face.get("face_confidence", 0) < 0.9:
            continue

        summary = {
            "file": str(image_path.absolute()),
            "age": face["age"],
            "gender": face["dominant_gender"],
            "race": face["dominant_race"],
            "confidence": face.get("face_confidence", 0),
        }
        processed_faces.append(summary)

    return processed_faces


def analyze_video(
    video_path: str | Path, skip_frames: int = 30
) -> list[dict[str, Any]]:
    """
    Analyze a video by sampling frames periodically for face demographics.

    :param video_path: Path to the video file.
    :param skip_frames: Number of frames to skip between analyses.
    :return: List of dictionaries with demographic information for each face found.
    """
    video_path = Path(video_path)
    if not video_path.is_file():
        logger.error(f"Video file not found: {video_path}")
        return []

    video_path_str = str(video_path)
    cap = cv2.VideoCapture(video_path_str)

    if not cap.isOpened():
        logger.error(f"Could not open video: {video_path_str}")
        return []

    results_data: list[dict[str, Any]] = []
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 30

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % skip_frames == 0:
            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                analysis = DeepFace.analyze(
                    img_path=rgb_frame,
                    actions=["age", "gender", "race"],
                    detector_backend="retinaface",
                    enforce_detection=False,
                    silent=True,
                )

                if not isinstance(analysis, list):
                    analysis = [analysis]

                for face in analysis:
                    if "dominant_race" not in face:
                        continue
                    if face.get("face_confidence", 0) < 0.9:
                        continue

                    summary = {
                        "file": str(video_path.absolute()),
                        "age": face["age"],
                        "gender": face["dominant_gender"],
                        "race": face["dominant_race"],
                        "confidence": face.get("face_confidence", 0),
                    }
                    results_data.append(summary)

            except Exception as e:
                logger.warning(f"Frame {frame_count} error: {e}")

        frame_count += 1

    cap.release()
    return results_data
