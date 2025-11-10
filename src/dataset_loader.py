"""
This module is responsible for searching and listing all relevant files(images/videos) in a given dataset directory.
In will be used as the first step in order to create a demopgraphic analysis.
"""

import os, glob, pathlib

class Loader:           
    
    """
    This class' functions can be used to manipulate the dataset.
    """
    
    def __init__(self, dataset): 
        self.dataset= dataset

    def load_data(self):
        for i in self.dataset:
            return 