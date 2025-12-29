"""
This module is used to write out the results.
"""
import csv
import os

def write_csv(file_path, data):
    """
    Write data to a CSV file.
    
    :param file_path: Path to the output CSV file.
    :param data: List of dictionaries containing the data to write.
    """
    if not data:
        print("No data to write.")
        return

    field_names = data[0].keys()
    
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)
            print(f"Data successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing CSV: {e}")