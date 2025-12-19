"""
This module is responsible for searching and listing all relevant files(images/videos) in a given dataset directory.
In will be used as the first step in order to create a demopgraphic analysis.
"""

import os, glob, pathlib


class Loader:           
    IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg'}
    """
    This class' functions can be used to manipulate the dataset.
    """
    def __init__(self, dataset): 
        """
        :param dataset: Path to the dataset directory.
        """
        self.directory= pathlib.Path(dataset)


    def find_images(self):
        """
        This function finds the images in a given path.
        :return: List of image file paths.
        """
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory '{self.directory}' does not exist.")
        
        image_files = [
            file for file in self.directory.iterdir() 
            if file.is_file() and file.suffix.lower() in self.IMAGE_EXTENSIONS
        ]

        return image_files