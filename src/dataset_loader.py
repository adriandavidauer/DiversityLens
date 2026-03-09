"""
This module is responsible for searching and listing all relevant files (images/videos)
in a given dataset directory. It is used as the first step in order to create a demographic analysis.
"""

import logging
import pathlib
import shutil
import tarfile
import zipfile

logger = logging.getLogger(__name__)

ARCHIVE_EXTENSIONS: set[str] = {".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tar.xz"}


def _is_archive(path: pathlib.Path) -> bool:
    """Check if a file is a supported archive format."""
    name = path.name.lower()
    if name.endswith((".tar.gz", ".tar.bz2", ".tar.xz")):
        return True
    return path.suffix.lower() in {".zip", ".tar", ".tgz"}


def extract_archives(directory: pathlib.Path) -> list[pathlib.Path]:
    """
    Find and extract all archive files in the directory tree.
    Each archive is extracted into a subfolder next to it, then the archive is kept as-is.

    :param directory: Root directory to scan for archives.
    :return: List of directories where archives were extracted.
    """
    extracted_dirs: list[pathlib.Path] = []

    archive_files = [f for f in directory.rglob("*") if f.is_file() and _is_archive(f)]

    for archive_path in archive_files:
        extract_dir = archive_path.parent / archive_path.stem
        # For .tar.gz etc., strip double extension
        if archive_path.name.lower().endswith((".tar.gz", ".tar.bz2", ".tar.xz")):
            extract_dir = archive_path.parent / pathlib.Path(archive_path.stem).stem

        if extract_dir.exists():
            logger.info(f"Archive already extracted, skipping: {archive_path.name}")
            continue

        try:
            if zipfile.is_zipfile(archive_path):
                with zipfile.ZipFile(archive_path, "r") as zf:
                    zf.extractall(extract_dir)
                logger.info(f"Extracted zip: {archive_path.name} -> {extract_dir}")
                extracted_dirs.append(extract_dir)

            elif tarfile.is_tarfile(archive_path):
                with tarfile.open(archive_path, "r:*") as tf:
                    tf.extractall(extract_dir, filter="data")
                logger.info(f"Extracted tar: {archive_path.name} -> {extract_dir}")
                extracted_dirs.append(extract_dir)

            else:
                logger.warning(f"Unrecognized archive format: {archive_path.name}")

        except Exception as e:
            logger.error(f"Failed to extract {archive_path.name}: {e}")
            if extract_dir.exists():
                shutil.rmtree(extract_dir)

    return extracted_dirs


class Loader:
    """
    Discovers image and video files within a dataset directory.
    Automatically extracts any archive files found before scanning.
    """

    IMAGE_EXTENSIONS: set[str] = {".png", ".jpg", ".jpeg"}
    VIDEO_EXTENSIONS: set[str] = {".mp4", ".avi", ".mov", ".mkv", ".webm"}

    def __init__(self, dataset: str | pathlib.Path) -> None:
        """
        :param dataset: Path to the dataset directory.
        """
        self.directory = pathlib.Path(dataset)
        self._archives_extracted = False

    def _ensure_archives_extracted(self) -> None:
        """Extract archives once before scanning for media files."""
        if not self._archives_extracted:
            extract_archives(self.directory)
            self._archives_extracted = True

    def find_images(self) -> list[pathlib.Path]:
        """
        Find all image files recursively in the dataset directory.
        Archives are extracted automatically before scanning.

        :return: List of image file paths.
        """
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory '{self.directory}' does not exist.")
        self._ensure_archives_extracted()
        image_files = [
            file
            for file in self.directory.rglob("*")
            if file.is_file() and file.suffix.lower() in self.IMAGE_EXTENSIONS
        ]
        return image_files

    def find_videos(self) -> list[pathlib.Path]:
        """
        Find all video files recursively in the dataset directory.
        Archives are extracted automatically before scanning.

        :return: List of video file paths.
        """
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory '{self.directory}' does not exist.")
        self._ensure_archives_extracted()
        video_files = [
            file
            for file in self.directory.rglob("*")
            if file.is_file() and file.suffix.lower() in self.VIDEO_EXTENSIONS
        ]
        return video_files
