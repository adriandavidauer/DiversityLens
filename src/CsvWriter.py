
"""
This module is used to write out the results.
"""

import csv
import os

class Write:

    """
    This class is used to write the face informations in CSV File format.
    """
    def __init__(self):
        """
        Initialization function of the class.
        """

    def write(self, data_dict):

        """
        This function helps to write out the informations of faces in a CSV file.
        """
        self.data_dict= data_dict

        if not self.data_dict:
            print("No data found!")
            return
        
        field_names = self.data_dict[0].keys()
        file_name=  "Demographic_Results.csv"
        try: 
            with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
                writer= csv.DictWriter(csv_file, fieldnames=field_names)
                
                writer.writeheader()
                writer.writerows(self.data_dict)
                print("Successful!")
        except Exception as e:
            print(f"Error :{e}")