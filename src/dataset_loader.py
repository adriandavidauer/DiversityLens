"""
This module is responsible for searching and listing all relevant files(images/videos) in a given dataset directory.
In will be used as the first step in order to create a demopgraphic analysis.
"""

import os, glob, pathlib, dlib

class Loader:           
    
    """
    This class' functions can be used to manipulate the dataset.
    """
    
    face_detector= dlib.cnn_face_detection_model_v1('dlib_models/mmod_human_face_detector.dat')


    def __init__(self, dataset): 
        self.dataset= dataset

    def image_finder(self):
        # Klasör var mı diye kontrol et, yoksa patlamasın.
        if not self.directory.exists():
            return f"Errror: '{self.directory}"
        valid_extensions = {'.png', '.jpg', '.jpeg'}

        image_files = [
            file for file in self.directory.iterdir() 
            if file.is_file() and file.suffix.lower() in valid_extensions
        ]

        if not image_files:
            return "No images found."
        
        return image_files