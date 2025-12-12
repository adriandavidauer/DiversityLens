"""
This module is responsible for being the backbone of the project that merges other modules. 
"""
from dataset_loader import Loader, pathlib
from demographic_estimator import Estimator
from data_writing import Write

def main():
    path = 'data/images'
    
    First_Data = Loader(path)
    found_images = First_Data.image_finder()

    if isinstance(found_images, str):
        print(f"Error: {found_images}")
        return

    print(f"Total {len(found_images)} images found.")

    Person = Estimator()
    all_results= []

    for image_path in found_images:
        try:
            result = Person.analyze_image(image_path) 
            if result:
                all_results.append(result)
            else:
                print("No new face found.")
        except Exception as e:
            print(f"Error {image_path.name} : {e}")
    

    ### SAVE THE DATA AS CSV FILE
    if all_results:
        Writer1= Write()
        Writer1.write(all_results)
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()