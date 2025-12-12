"""
This module is responsible for estimating age, gender, and race using DeepFace.
It acts as a wrapper for the deep learning model.
"""
from deepface import DeepFace

class Estimator:
    def __init__(self):
        pass

    def analyze_image(self, image_path):
        """
        Takes an image path and returns a LIST of demographic info for all faces found.
        """
        processed_faces = []
        
        try:
            img_str = str(image_path)
            # print(f"Analyzing: {img_str} ...") 
            
            # 1. Analizi yap
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
                if 'dominant_race' not in face:
                    continue

                summary = {
                    "file": image_path.name,
                    "age": face['age'],
                    "gender": face['dominant_gender'],
                    "race": face['dominant_race'],
                    "confidence": face.get('face_confidence', 0)
                }
                processed_faces.append(summary)

            return processed_faces

        except Exception as e:
            return []