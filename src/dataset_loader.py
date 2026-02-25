"""
This module is responsible for searching and listing all relevant files(images/videos) in a given dataset directory.
In will be used as the first step in order to create a demopgraphic analysis.
"""

import pathlib


class Loader:
    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
    VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
    """
    This class' functions can be used to manipulate the dataset.
    """

    def __init__(self, dataset):
        """
        :param dataset: Path to the dataset directory.
        """
        self.directory = pathlib.Path(dataset)

    def find_images(self):
        """
        This function finds the images in a given path.
        :return: List of image file paths.
        """
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory '{self.directory}' does not exist.")
        image_files = [
            file
            for file in self.directory.rglob("*")  # check all the files
            if file.is_file() and file.suffix.lower() in self.IMAGE_EXTENSIONS
        ]
        return image_files

    def find_videos(self):
        """
        This function finds the videos in a given path.
        ::return: List of videos file paths.
        """
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory '{self.directory}' does not exist.")

        video_files = [
            file
            for file in self.directory.rglob("*")
            if file.is_file() and file.suffix.lower() in self.VIDEO_EXTENSIONS
        ]
        return video_files
