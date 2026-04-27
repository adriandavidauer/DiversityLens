"""
This module is responsible for searching and listing all relevant files(images/videos)
in a given dataset directory.
In will be used as the first step in order to create a demopgraphic analysis.
"""

import pathlib
import tarfile
import zipfile


def _is_within_directory(base_dir: pathlib.Path, target_path: pathlib.Path) -> bool:
    """Return True when target_path stays inside base_dir."""
    try:
        target_path.resolve().relative_to(base_dir.resolve())
        return True
    except ValueError:
        return False


class Loader:
    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
    VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
    ARCHIVE_EXTENSIONS = (
        ".tar.gz",
        ".tar.bz2",
        ".tar.xz",
        ".tgz",
        ".zip",
        ".tar",
    )
    """
    This class' functions can be used to manipulate the dataset.
    """

    def __init__(self, dataset):
        """
        :param dataset: Path to the dataset directory.
        """
        self.directory = pathlib.Path(dataset)

    @classmethod
    def is_archive(cls, file_path):
        """Return True if file_path matches a supported archive extension."""
        file_name = pathlib.Path(file_path).name.lower()
        return any(file_name.endswith(ext) for ext in cls.ARCHIVE_EXTENSIONS)

    @classmethod
    def _archive_base_name(cls, archive_path):
        """Return archive filename without archive extension."""
        file_name = pathlib.Path(archive_path).name
        lower_name = file_name.lower()
        for ext in sorted(cls.ARCHIVE_EXTENSIONS, key=len, reverse=True):
            if lower_name.endswith(ext):
                return file_name[: -len(ext)]
        return pathlib.Path(file_name).stem

    def _safe_extract_zip(self, archive_path, output_dir):
        """Extract zip archive while preventing path traversal."""
        with zipfile.ZipFile(archive_path, "r") as zip_ref:
            for member in zip_ref.namelist():
                destination = output_dir / member
                if not _is_within_directory(output_dir, destination):
                    raise ValueError(f"Unsafe path in zip archive: {member}")
            zip_ref.extractall(output_dir)

    def _safe_extract_tar(self, archive_path, output_dir):
        """Extract tar archive while preventing path traversal."""
        with tarfile.open(archive_path, "r:*") as tar_ref:
            for member in tar_ref.getmembers():
                destination = output_dir / member.name
                if not _is_within_directory(output_dir, destination):
                    raise ValueError(f"Unsafe path in tar archive: {member.name}")
            try:
                tar_ref.extractall(output_dir, filter="data")
            except TypeError:
                tar_ref.extractall(output_dir)

    def _extract_archive(self, archive_path):
        """Extract a supported archive and return the extraction directory."""
        archive_path = pathlib.Path(archive_path)
        extraction_dir = archive_path.parent / self._archive_base_name(archive_path)
        extraction_dir.mkdir(parents=True, exist_ok=True)

        if any(extraction_dir.iterdir()):
            return extraction_dir

        if archive_path.suffix.lower() == ".zip":
            self._safe_extract_zip(archive_path, extraction_dir)
        else:
            self._safe_extract_tar(archive_path, extraction_dir)
        return extraction_dir

    def _extract_archives_in_tree(self):
        """Discover and extract supported archives inside dataset directory."""
        archive_files = [
            file
            for file in self.directory.rglob("*")
            if file.is_file() and self.is_archive(file)
        ]
        for archive_path in archive_files:
            self._extract_archive(archive_path)

    def find_images(self):
        """
        This function finds the images in a given path.
        :return: List of image file paths.
        """
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory '{self.directory}' does not exist.")
        self._extract_archives_in_tree()
        image_files = [
            file
            for file in self.directory.rglob("*")  # check all the files
            if file.is_file() and file.suffix.lower() in self.IMAGE_EXTENSIONS
        ]
        return image_files

    def find_videos(self):
        """
        This function finds the videos in a given path.
        ::return: List of videos file paths.
        """
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory '{self.directory}' does not exist.")
        self._extract_archives_in_tree()

        video_files = [
            file
            for file in self.directory.rglob("*")
            if file.is_file() and file.suffix.lower() in self.VIDEO_EXTENSIONS
        ]
        return video_files
