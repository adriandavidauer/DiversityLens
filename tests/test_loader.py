import tarfile
import zipfile
from pathlib import Path

from src.dataset_loader import Loader


def test_loader_initialization():
    dummy_path = "tests/data"
    loader = Loader(dummy_path)
    assert loader.directory == Path(dummy_path)


def test_extensions_exist():
    assert ".jpg" in Loader.IMAGE_EXTENSIONS
    assert ".mp4" in Loader.VIDEO_EXTENSIONS
    assert Loader.is_archive("dataset.zip")
    assert Loader.is_archive("dataset.tar.gz")
    assert not Loader.is_archive("dataset.csv")


def test_find_images_and_videos(tmp_path):
    (tmp_path / "a.jpg").write_bytes(b"jpg")
    (tmp_path / "b.mp4").write_bytes(b"mp4")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.png").write_bytes(b"png")

    loader = Loader(tmp_path)
    images = loader.find_images()
    videos = loader.find_videos()

    image_names = {file.name for file in images}
    video_names = {file.name for file in videos}
    assert {"a.jpg", "c.png"} <= image_names
    assert {"b.mp4"} <= video_names


def test_zip_archive_auto_extraction(tmp_path):
    archive_path = tmp_path / "faces.zip"
    with zipfile.ZipFile(archive_path, "w") as zip_file:
        zip_file.writestr("inside/face.jpg", b"jpg")

    loader = Loader(tmp_path)
    images = loader.find_images()

    image_paths = {file.as_posix() for file in images}
    assert any(path.endswith("faces/inside/face.jpg") for path in image_paths)


def test_tar_gz_archive_auto_extraction(tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    source_file = source_dir / "clip.mov"
    source_file.write_bytes(b"mov")

    archive_path = tmp_path / "videos.tar.gz"
    with tarfile.open(archive_path, "w:gz") as tar_file:
        tar_file.add(source_file, arcname="folder/clip.mov")

    loader = Loader(tmp_path)
    videos = loader.find_videos()

    video_paths = {file.as_posix() for file in videos}
    assert any(path.endswith("videos/folder/clip.mov") for path in video_paths)
