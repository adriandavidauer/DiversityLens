from pathlib import Path

from src.dataset_loader import Loader


#This test checks if Loader_Class works properly
def test_loader_initialization():

    # Send a dummy path
    dummy_path = "tests/data"
    loader = Loader(dummy_path)

    #It checks if Loader directory is set correct
    assert loader.directory == Path(dummy_path)

def test_extensions_exist():
    #It checks if Loader_class has the correct formats
    assert '.jpg' in Loader.IMAGE_EXTENSIONS
    assert '.mp4' in Loader.VIDEO_EXTENSIONS
