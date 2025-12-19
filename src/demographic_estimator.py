"""
This module is responsible for estimating age, gender, and race using DeepFace.
It acts as a wrapper for the deep learning model.
"""
from deepface import DeepFace
from pathlib import Path

def analyze_image(image_path):
    """
    This function takes an image path and returns a LIST of demographic info for all faces found.
    :param image_path: Path to the image file.
    :return: List of dictionaries with demographic information for each face.
    """
    image_path = Path(image_path)
    processed_faces = []
    

    img_str = str(image_path)
    # print(f"Analyzing: {img_str} ...") 
    
    results = DeepFace.analyze(
        img_path=img_str, 
        actions=['age', 'gender', 'race'],
        detector_backend='opencv', 
        enforce_detection=False, 
        silent=True
    )
    
    if not isinstance(results, list):
        results = [results]
    for face in results:
        # for the case no face was detected
        if 'dominant_race' not in face:
            continue

        summary = {
            "file": image_path.absolute(),
            "age": face['age'],
            "gender": face['dominant_gender'],
            "race": face['dominant_race'],
            "confidence": face.get('face_confidence', 0)
        }
        processed_faces.append(summary)

    return processed_faces
