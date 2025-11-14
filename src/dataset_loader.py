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

    def load_data(self):
        for i in self.dataset:
            return 