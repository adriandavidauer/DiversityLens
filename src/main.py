"""
This module is responsible for being the backbone of the project that merges other modules. 
"""
from .dataset_loader import Loader, pathlib
from .demographic_estimator import analyze_image
from .data_writing import write_csv
import argparse

def main():

    """
    This function initiates the process to analyze the face dataset.
    """

    parser= argparse.ArgumentParser()
    parser.add_argument("--path", default= "tests/data/images", type= str, help= "Path to the dataset directory.")
    parser.add_argument("--output", default= "Demographic_Results.csv", type= str, help= "Path to the output CSV file.")
    args= parser.parse_args()
    path= args.path
    output= args.output

    first_data = Loader(path)
    found_images = first_data.find_images()

#    if isinstance(found_images, str):
#        print(f"Error: {found_images}")
#        return

    print(f"Total {len(found_images)} images found.")
    all_results= []

    for image_path in found_images:
            result_list = analyze_image(image_path) 
            if result_list:
                all_results.extend(result_list)
            else:
                print("No new face found.") 
    
    ### SAVE THE DATA AS CSV FILE
    if all_results:
        write_csv(output, all_results)
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()