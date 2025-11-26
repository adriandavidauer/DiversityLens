"""
This module is responsible for being the backbone of the project that merges other modules. 
"""

from dataset_loader import Loader, pathlib
from demographic_estimator import Estimator


def main():
    path = 'data/images'
    
    First_Data = Loader(path)
    found_images = First_Data.image_finder()

    if isinstance(found_images, str):
        print(f"Error: {found_images}")
        return

    print(f"Total {len(found_images)} images found.")

    Person = Estimator()

    for image_path in found_images:
        print(f"\Processing: {image_path.name}")
        sonuc = Person.analyze_image(image_path)
        print(sonuc)

if __name__ == "__main__":
    main()