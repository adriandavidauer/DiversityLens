"""
This module is responsible for being the backbone of the project that merges other modules.
"""

import argparse

from src.data_writing import write_csv
from src.dataset_loader import Loader, pathlib
from src.demographic_estimator import analyze_image, analyze_video
from src.logger import setup_logger
from src.visualization import Visualizer


def main():
    # 1. Logger Creation
    logger = setup_logger()
    logger.info("DiversityLens Started...")

    # 2. CLI Creation
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
    parser.add_argument(
        "--detector-backend",
        default="retinaface",
        type=str,
        help="DeepFace detector backend (e.g. retinaface, opencv, mtcnn, ssd).",
    )
    parser.add_argument(
        "--min-confidence",
        default=0.9,
        type=float,
        help="Minimum face confidence to keep a detection (0 disables filtering).",
    )

    args = parser.parse_args()
    path = args.path
    output_file = args.output
    detector_backend = args.detector_backend
    min_confidence = args.min_confidence

    logger.info(f"Analyzing the folder: {path}")
    logger.info(
        "Detector backend: %s | Min confidence: %.2f",
        detector_backend,
        min_confidence,
    )

    # Find the images
    first_data = Loader(path)
    found_images = first_data.find_images()

    if isinstance(found_images, str):
        logger.error(f"Error finding images: {found_images}")
        return

    logger.info(f"Total {len(found_images)} images found.")

    # Find the videos

    found_videos = first_data.find_videos()
    logger.info(f"Total {len(found_videos)} videos found.")
    if isinstance(found_videos, str):
        logger.error(f"Error finding videos: {found_videos}")
        return

    all_results = []

    # Analyze Images
    for image_path in found_images:
        try:
            result_list = analyze_image(
                image_path,
                detector_backend=detector_backend,
                min_confidence=min_confidence,
            )
            if result_list:
                all_results.extend(result_list)
                logger.info(
                    f"[OK] {image_path.name} -> {len(result_list)} faces detected."
                )
            else:
                logger.warning(f"[SKIP] No face found in {image_path.name}")
        except Exception as e:
            logger.error(f"Error processing {image_path.name}: {e}")

    # Analyze Videos
    if found_videos:
        logger.warning(f"Found {len(found_videos)} videos")
        for video_path in found_videos:
            try:
                result_list = analyze_video(
                    video_path,
                    detector_backend=detector_backend,
                    min_confidence=min_confidence,
                )
                if result_list:
                    all_results.extend(result_list)
                    logger.info(
                        f"[OK] {video_path.name} -> {len(result_list)} faces detected."
                    )
                else:
                    logger.warning(f"[SKIP] No face found in {video_path.name}")
            except Exception as e:
                logger.error(f"Error processing {video_path.name}: {e}")

    # Save results
    if all_results:
        logger.info(f"Saving {len(all_results)} results to {output_file}...")
        try:
            write_csv(output_file, all_results)
            logger.info("Successfully saved!")
            # data_visualizer = Visualizer(output_file)
            logger.info("Starting visualization...")
            output_dir = pathlib.Path(output_file).parent
            viz = Visualizer(all_results, output_dir)
            viz.plot_charts()

        except Exception as e:
            logger.error(f"CSV Error: {e}")
    else:
        logger.warning("No data to save.")


if __name__ == "__main__":
    main()
