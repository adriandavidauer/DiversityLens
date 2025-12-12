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
        Takes an image path (Path object or string) and returns demographic info.
        """
        try:
            # DeepFace requires a string.
            img_str = str(image_path)
            
            print(f"Analyzing: {img_str} ...")
            
            results = DeepFace.analyze(
                img_path=img_str, 
                actions=['age', 'gender', 'race'],
                detector_backend='opencv', 
                enforce_detection=False, # in case no face found.
                silent=True
            )
            # DeepFace might return list or dict. 
            if isinstance(results, list):
                result = results[0]
            else:
                result = results
            summary = {
                "Age": result['age'],
                "Gender": result['dominant_gender'],
                "Race": result['dominant_race'],
                #"confidence": result['face_confidence'] 
            }
            return summary

        except Exception as e:
            print(f"Error analyzing {image_path}: {e}")
            return None