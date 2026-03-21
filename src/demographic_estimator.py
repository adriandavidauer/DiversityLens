"""
This module is responsible for estimating demographic attributes
(age, gender, and ethnicity) for detected faces, using predictions
from a pretrained model.
"""

import cv2
from deepface import DeepFace


class Estimator:
    """
    This class provides methods to analyze demographic attributes
    (age, gender, ethnicity) of faces in images using DeepFace.
    """

    def analyze_image(self, path):
        """
        This function will analyze the image in the given path.

        Args:
            path: Path object or string pointing to the image file.

        Returns:
            A list of dicts containing demographic info per detected face,
            or None if analysis fails.
        """
        img_str = path.name if hasattr(path, 'name') else str(path)
        print(f"Analyzing: {img_str} ...")

        try:
            results = DeepFace.analyze(
                img_path=str(path),
                actions=["gender", "race"],
                detector_backend="opencv",
                enforce_detection=False,
                silent=True,
            )

            if not isinstance(results, list):
                results = [results]

            output = []
            for person_info in results:
                output.append({
                    "file": img_str,
                    "gender": person_info.get("dominant_gender"),
                    "race": person_info.get("dominant_race"),
                    "confidence": person_info.get("face_confidence"),
                })
            return output

        except Exception as e:
            print(f"Error: {img_str}: {e}")
            return None
