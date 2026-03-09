import tarfile
import zipfile

import pytest
from pathlib import Path
from src.dataset_loader import Loader, extract_archives


def test_loader_initialization():
    dummy_path = "tests/data"
    loader = Loader(dummy_path)
    assert loader.directory == Path(dummy_path)


def test_loader_initialization_with_path_object():
    dummy_path = Path("tests/data")
    loader = Loader(dummy_path)
    assert loader.directory == dummy_path


def test_extensions_exist():
    assert ".jpg" in Loader.IMAGE_EXTENSIONS
    assert ".png" in Loader.IMAGE_EXTENSIONS
    assert ".jpeg" in Loader.IMAGE_EXTENSIONS
    assert ".mp4" in Loader.VIDEO_EXTENSIONS
    assert ".avi" in Loader.VIDEO_EXTENSIONS
    assert ".mov" in Loader.VIDEO_EXTENSIONS
    assert ".mkv" in Loader.VIDEO_EXTENSIONS
    assert ".webm" in Loader.VIDEO_EXTENSIONS


def test_find_images_returns_list():
    loader = Loader("tests/data")
    images = loader.find_images()
    assert isinstance(images, list)
    for img in images:
        assert isinstance(img, Path)
        assert img.suffix.lower() in Loader.IMAGE_EXTENSIONS


def test_find_images_finds_png_files():
    loader = Loader("tests/data")
    images = loader.find_images()
    assert len(images) > 0
    assert all(img.suffix.lower() == ".png" for img in images)


def test_find_videos_returns_list():
    loader = Loader("tests/data")
    videos = loader.find_videos()
    assert isinstance(videos, list)
    for vid in videos:
        assert isinstance(vid, Path)
        assert vid.suffix.lower() in Loader.VIDEO_EXTENSIONS


def test_find_images_nonexistent_directory():
    loader = Loader("nonexistent/path")
    with pytest.raises(FileNotFoundError):
        loader.find_images()


def test_find_videos_nonexistent_directory():
    loader = Loader("nonexistent/path")
    with pytest.raises(FileNotFoundError):
        loader.find_videos()


def test_find_images_empty_directory(tmp_path):
    loader = Loader(tmp_path)
    images = loader.find_images()
    assert images == []


def test_find_videos_empty_directory(tmp_path):
    loader = Loader(tmp_path)
    videos = loader.find_videos()
    assert videos == []


# --- Archive extraction tests ---


def _create_zip_with_images(zip_path, filenames):
    """Helper to create a zip archive containing dummy image files."""
    with zipfile.ZipFile(zip_path, "w") as zf:
        for name in filenames:
            zf.writestr(name, b"\x89PNG\r\n\x1a\n")


def _create_tar_with_images(tar_path, filenames, mode="w:gz"):
    """Helper to create a tar archive containing dummy image files."""
    import io

    with tarfile.open(tar_path, mode) as tf:
        for name in filenames:
            data = b"\x89PNG\r\n\x1a\n"
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))


def test_extract_zip_archive(tmp_path):
    zip_file = tmp_path / "images.zip"
    _create_zip_with_images(zip_file, ["photo1.png", "photo2.jpg"])

    extracted = extract_archives(tmp_path)
    assert len(extracted) == 1

    extract_dir = tmp_path / "images"
    assert extract_dir.exists()
    assert (extract_dir / "photo1.png").exists()
    assert (extract_dir / "photo2.jpg").exists()


def test_extract_tar_gz_archive(tmp_path):
    tar_file = tmp_path / "images.tar.gz"
    _create_tar_with_images(tar_file, ["pic1.png", "pic2.png"])

    extracted = extract_archives(tmp_path)
    assert len(extracted) == 1

    extract_dir = tmp_path / "images"
    assert extract_dir.exists()
    assert (extract_dir / "pic1.png").exists()


def test_extract_skips_already_extracted(tmp_path):
    zip_file = tmp_path / "data.zip"
    _create_zip_with_images(zip_file, ["img.png"])

    # Pre-create the extract dir to simulate already extracted
    (tmp_path / "data").mkdir()

    extracted = extract_archives(tmp_path)
    assert len(extracted) == 0


def test_loader_finds_images_inside_zip(tmp_path):
    zip_file = tmp_path / "dataset.zip"
    _create_zip_with_images(zip_file, ["face1.png", "face2.jpg", "readme.txt"])

    loader = Loader(tmp_path)
    images = loader.find_images()

    image_names = {img.name for img in images}
    assert "face1.png" in image_names
    assert "face2.jpg" in image_names
    assert "readme.txt" not in image_names


def test_loader_finds_images_inside_tar(tmp_path):
    tar_file = tmp_path / "dataset.tar.gz"
    _create_tar_with_images(tar_file, ["photo.png"])

    loader = Loader(tmp_path)
    images = loader.find_images()

    assert any(img.name == "photo.png" for img in images)


def test_extract_handles_corrupt_archive(tmp_path):
    bad_zip = tmp_path / "corrupt.zip"
    bad_zip.write_bytes(b"this is not a zip file")

    extracted = extract_archives(tmp_path)
    assert len(extracted) == 0


def test_loader_extracts_only_once(tmp_path):
    zip_file = tmp_path / "data.zip"
    _create_zip_with_images(zip_file, ["img.png"])

    loader = Loader(tmp_path)
    loader.find_images()
    assert loader._archives_extracted is True

    # Second call should not re-extract
    loader.find_videos()
    assert loader._archives_extracted is True


def test_multiple_archives(tmp_path):
    zip1 = tmp_path / "set1.zip"
    zip2 = tmp_path / "set2.zip"
    _create_zip_with_images(zip1, ["a.png"])
    _create_zip_with_images(zip2, ["b.jpg"])

    loader = Loader(tmp_path)
    images = loader.find_images()

    image_names = {img.name for img in images}
    assert "a.png" in image_names
    assert "b.jpg" in image_names
