"""
This module is responsible for being the backbone of the project that merges other modules.
"""

import argparse
import pathlib

from src.dataset_loader import Loader
from src.demographic_estimator import analyze_image, analyze_video
from src.data_writing import write_csv
from src.logger import setup_logger
from src.visualization import Visualizer


def main() -> None:
    logger = setup_logger()
    logger.info("DiversityLens Started...")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path", default="tests/data", type=str, help="Path to the dataset directory."
    )
    parser.add_argument(
        "--output",
        default="Demographic_Results.csv",
        type=str,
        help="Path to the output CSV file.",
    )

    args = parser.parse_args()
    path = args.path
    output_file = args.output

    logger.info(f"Analyzing the folder: {path}")

    try:
        first_data = Loader(path)
        found_images = first_data.find_images()
        logger.info(f"Total {len(found_images)} images found.")

        found_videos = first_data.find_videos()
        logger.info(f"Total {len(found_videos)} videos found.")
    except FileNotFoundError as e:
        logger.error(str(e))
        return

    all_results: list[dict] = []

    for image_path in found_images:
        try:
            result_list = analyze_image(image_path)
            if result_list:
                all_results.extend(result_list)
                logger.info(
                    f"[OK] {image_path.name} -> {len(result_list)} faces detected."
                )
            else:
                logger.warning(f"[SKIP] No face found in {image_path.name}")
        except Exception as e:
            logger.error(f"Error processing {image_path.name}: {e}")

    if found_videos:
        logger.info(f"Processing {len(found_videos)} videos...")
        for video_path in found_videos:
            try:
                result_list = analyze_video(video_path)
                if result_list:
                    all_results.extend(result_list)
                    logger.info(
                        f"[OK] {video_path.name} -> {len(result_list)} faces detected."
                    )
                else:
                    logger.warning(f"[SKIP] No face found in {video_path.name}")
            except Exception as e:
                logger.error(f"Error processing {video_path.name}: {e}")

    if all_results:
        logger.info(f"Saving {len(all_results)} results to {output_file}...")
        try:
            write_csv(output_file, all_results)
            logger.info("Successfully saved!")
            logger.info("Starting visualization...")
            output_dir = pathlib.Path(output_file).parent
            viz = Visualizer(all_results, output_dir)
            viz.plot_charts()
1        except Exception as e:
            logger.error(f"CSV Error: {e}")
    else:
        logger.warning("No data to save.")


if __name__ == "__main__":
    main()
