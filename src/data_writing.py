
"""
This module is used to write out the results.
"""

import csv
import os

class Write:
    def __init__(self):
        pass

    def write(self, data_dict):
        self.data_dict= data_dict

        if not self.data_dict:
            print("No data founds!")
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