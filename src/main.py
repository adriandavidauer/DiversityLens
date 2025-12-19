"""
This module is responsible for being the backbone of the project that merges other modules. 
"""
from .dataset_loader import Loader, pathlib
from .demographic_estimator import analyze_image
from .data_writing import write_csv
import argparse
from src.logger import setup_logger

def main():
    """
    This function initiates the process to analyze the face dataset.
    """

    logger = setup_logger()
    logger.info("DiversityLens Started...")

    parser= argparse.ArgumentParser()
    parser.add_argument("--path", default= "tests/data/images", type= str, help= "Path to the dataset directory.")
    parser.add_argument("--output", default= "Demographic_Results.csv", type= str, help= "Path to the output CSV file.")
    args= parser.parse_args()
    path= args.path
    output= args.output


    logger.info(f"Analyzing the folder: {path}")

    first_data = Loader(path)
    found_images = first_data.find_images()

    if isinstance(found_images, str):
        logger.error(f"Image loading error: {found_images}")
        return

    logger.info(f"Total {len(found_images)} images found.")

    all_results= []

    for image_path in found_images:
        try:
            result_list = analyze_image(image_path)
            if result_list:
                all_results.extend(result_list)
                logger.info(f"[Successfull! ] {image_path.name} -> {len(result_list)} Face detected!")
            else:
                # Yüz bulunamadıysa uyarı (warning) seviyesinde log düşelim
                logger.warning(f"[Empty!] {image_path.name} No face found.")
                
        except Exception as e:
            # Beklenmedik bir hata olursa program durmasın, loga yazsın
            logger.error(f"[Error] {image_path.name} In processing the face: {e}")


    ### SAVE THE DATA AS CSV FILE
    if all_results:
        write_csv(output, all_results)
        logger.info(f"{len(all_results)} Results are saved in CSV File.")
    else:
        logger.info("No data to save.")
if __name__ == "__main__":
    main()