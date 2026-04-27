"""
This module is responsible for estimating age, gender, and race using DeepFace.
It acts as a wrapper for the deep learning model.
"""

from pathlib import Path

import cv2
from deepface import DeepFace


def _passes_confidence(face, min_confidence):
    """Return True when the detected face confidence meets the threshold."""
    if min_confidence <= 0:
        return True
    return face.get("face_confidence", 0) >= min_confidence


def analyze_image(image_path, detector_backend="retinaface", min_confidence=0.9):
    """
    This function takes an image path and returns a LIST of demographic info for all faces found.
    :param image_path: Path to the image file.
    :return: List of dictionaries with demographic information for each face.
    """
    image_path = Path(image_path)
    processed_faces = []
    img_str = str(image_path)
    results = DeepFace.analyze(
        img_path=img_str,
        actions=["age", "gender", "race"],
        detector_backend=detector_backend,
        enforce_detection=False,
        silent=True,
    )
    if not isinstance(results, list):
        results = [results]
    for face in results:
        # In case no face was detected
        if "dominant_race" not in face:
            continue
        if not _passes_confidence(face, min_confidence):
            continue

        summary = {
            "file": image_path.absolute(),
            "age": face["age"],
            "gender": face["dominant_gender"],
            "race": face["dominant_race"],
            "confidence": face.get("face_confidence", 0),
        }
        processed_faces.append(summary)

    return processed_faces


def analyze_video(
    video_path,
    skip_frames=1,
    detector_backend="retinaface",
    min_confidence=0.9,
):  # Videos are read by OpenCV-then
    """
    This function takes a video path and analyzes frames periodically.
    :param video_path: Path to the video file.
    :param skip_frames: Analyze every n-th frame. Use 1 to analyze all frames.
    :return: List of dictionaries with demographic information for each face found.
    """
    # If it's Path object,convert it into string, if it's string then keep it
    video_path_str = str(video_path)
    frame_step = max(1, int(skip_frames))

    cap = cv2.VideoCapture(video_path_str)

    if not cap.isOpened():
        print(f"Error: {video_path_str} could not be opened.")
        return []

    results_data = []
    frame_count = 0

    while True:
        ret, frame = cap.read()

        # if video ends, break the loop
        if not ret:
            break

        if frame_count % frame_step == 0:
            try:
                # DeepFace expects RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # send array to img_path parameter
                analysis = DeepFace.analyze(
                    img_path=rgb_frame,
                    actions=["age", "gender", "race"],
                    detector_backend=detector_backend,
                    enforce_detection=False,
                    silent=True,
                )

                if not isinstance(analysis, list):
                    analysis = [analysis]

                for face in analysis:
                    if "dominant_race" not in face:
                        continue
                    if not _passes_confidence(face, min_confidence):
                        continue

                    summary = {
                        "file": video_path.absolute(),
                        "age": face["age"],
                        "gender": face["dominant_gender"],
                        "race": face["dominant_race"],
                        "confidence": face.get("face_confidence", 0),
                    }
                    results_data.append(summary)

            except Exception as e:
                print(f"Frame {frame_count} has an error: {e}")

        frame_count += 1

    cap.release()
    return results_data
