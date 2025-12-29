"""
This module is responsible for being the backbone of the project that merges other modules. 
"""
import argparse
from src.dataset_loader import Loader, pathlib
from src.demographic_estimator import analyze_image
from src.data_writing import write_csv  # Adrian'ın yeni fonksiyonu
from src.logger import setup_logger     # Senin Logger'ın

def main():
    # 1. Logger Kurulumu
    logger = setup_logger()
    logger.info("DiversityLens Started...")

    # 2. Argümanları Ayarla (Adrian'ın eklediği output argümanı dahil)
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="tests/data/images", type=str, help="Path to the dataset directory.")
    parser.add_argument("--output", default="Demographic_Results.csv", type=str, help="Path to the output CSV file.")
    
    args = parser.parse_args()
    path = args.path
    output_file = args.output

    logger.info(f"Analyzing the folder: {path}")

    # 3. Resimleri Bul
    first_data = Loader(path)
    found_images = first_data.find_images()

    if isinstance(found_images, str):
        logger.error(f"Error finding images: {found_images}")
        return

    logger.info(f"Total {len(found_images)} images found.")

    all_results = []

    # 4. Analiz Döngüsü
    for image_path in found_images:
        try:
            result_list = analyze_image(image_path)
            if result_list:
                all_results.extend(result_list)
                logger.info(f"[OK] {image_path.name} -> {len(result_list)} faces detected.")
            else:
                logger.warning(f"[SKIP] No face found in {image_path.name}")
        except Exception as e:
            logger.error(f"Error processing {image_path.name}: {e}")

    # 5. Kaydetme (Adrian'ın write_csv fonksiyonunu kullanıyoruz)
    if all_results:
        logger.info(f"Saving {len(all_results)} results to {output_file}...")
        try:
            write_csv(output_file, all_results)
            logger.info("Successfully saved!")
        except Exception as e:
            logger.error(f"CSV Error: {e}")
    else:
        logger.warning("No data to save.")

if __name__ == "__main__":
    main()