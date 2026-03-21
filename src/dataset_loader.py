"""
This module is responsible for searching and listing all relevant files(images/videos) in a given dataset directory.
In will be used as the first step in order to create a demographic analysis.
"""

import pathlib


class Loader:
    """
    This class' functions can be used to manipulate the dataset.
    """

    def __init__(self, dataset):
        self.dataset = pathlib.Path(dataset)
        if not self.dataset.exists():
            raise FileNotFoundError(f"Error: '{dataset}' couldn't be found.")

    def image_finder(self):
        """
        Searches the dataset directory and returns all image files.

        Returns:
            A list of Path objects for each image found (.jpg, .png, .jpeg).
        """
        valid_extensions = {'.jpg', '.png', '.jpeg'}
        image_files = [
            file for file in self.dataset.iterdir()
            if file.is_file() and file.suffix.lower() in valid_extensions
        ]
        if not image_files:
            print("No image found!")
        return image_files

    def load_data(self):
        """
        Loads and returns all image paths from the dataset directory.

        Returns:
            A list of Path objects for each image found.
        """
        return self.image_finder()
