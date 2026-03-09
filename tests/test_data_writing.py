import csv
from pathlib import Path

from src.data_writing import write_csv


def test_write_csv_creates_file(tmp_path):
    output = tmp_path / "output.csv"
    data = [
        {"file": "img1.png", "age": 25, "gender": "Man", "race": "white", "confidence": 0.9},
        {"file": "img2.png", "age": 30, "gender": "Woman", "race": "asian", "confidence": 0.8},
    ]
    write_csv(output, data)
    assert output.exists()


def test_write_csv_content(tmp_path):
    output = tmp_path / "output.csv"
    data = [
        {"file": "img1.png", "age": 25, "gender": "Man", "race": "white", "confidence": 0.9},
    ]
    write_csv(output, data)

    with open(output, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 1
    assert rows[0]["file"] == "img1.png"
    assert rows[0]["age"] == "25"
    assert rows[0]["gender"] == "Man"


def test_write_csv_empty_data(tmp_path):
    output = tmp_path / "output.csv"
    write_csv(output, [])
    assert not output.exists()


def test_write_csv_creates_parent_directory(tmp_path):
    output = tmp_path / "subdir" / "nested" / "output.csv"
    data = [{"file": "img.png", "age": 20, "gender": "Man", "race": "white", "confidence": 0.5}]
    write_csv(output, data)
    assert output.exists()


def test_write_csv_multiple_rows(tmp_path):
    output = tmp_path / "output.csv"
    data = [
        {"file": f"img{i}.png", "age": 20 + i, "gender": "Man", "race": "white", "confidence": 0.5}
        for i in range(10)
    ]
    write_csv(output, data)

    with open(output, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 10
