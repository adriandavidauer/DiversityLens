"""
This module is used to write out the results.
"""

import csv
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def write_csv(file_path: str | Path, data: list[dict[str, Any]]) -> None:
    """
    Write data to a CSV file.

    :param file_path: Path to the output CSV file.
    :param data: List of dictionaries containing the data to write.
    """
    if not data:
        logger.warning("No data to write.")
        return

    file_path = Path(file_path)
    output_dir = file_path.parent
    if output_dir != Path(".") and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created output directory: {output_dir}")

    field_names = data[0].keys()

    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)
            logger.info(f"Data successfully written to {file_path}")
    except Exception as e:
        logger.error(f"Error writing CSV: {e}")
