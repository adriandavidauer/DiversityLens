"""
This module is responsible for searching and listing all relevant files(images/videos) in a given dataset directory.
In will be used as the first step in order to create a demopgraphic analysis.
"""

import os, glob, pathlib

from deepface import DeepFace

class Loader:           
    
    """
    This class' functions can be used to manipulate the dataset.
    """
    def __init__(self, dataset): 
        self.directory= pathlib.Path(dataset)
        """
        This function helps to embed the 'dataset path' into the object of the class.
        """

    def find_images(self):
        """
        This function finds the images in a given path.
        """
        if not self.directory.exists():
            return f"Errror: '{FileNotFoundError}"
        valid_extensions = {'.png', '.jpg', '.jpeg'}

        image_files = [
            file for file in self.directory.iterdir() 
            if file.is_file() and file.suffix.lower() in valid_extensions
        ]

        if not image_files:
            return "No images found."
        return image_files