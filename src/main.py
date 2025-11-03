"""
This module is responsible for being the backbone of the project that merges other modules. 
"""

from dataset_loader import Loader

dataset1 = [("Caucasian", "Male", "20"), ("Black", "Female", "20"), ("South Asian", "Female", "40")]

First_Dataset= Loader(dataset=dataset1)
each_person = First_Dataset.load_data()

for i in dataset1:
        if each_person is None:
            print("dataset is not found!!!!.")
        else:
            print(each_person)       