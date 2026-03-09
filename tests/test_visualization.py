from pathlib import Path

from src.visualization import Visualizer


def _sample_data(n=10):
    return [
        {
            "file": f"img{i}.png",
            "age": 20 + i * 3,
            "gender": "Man" if i % 2 == 0 else "Woman",
            "race": ["white", "asian", "black", "indian", "latino hispanic"][i % 5],
            "confidence": 0.9,
        }
        for i in range(n)
    ]


def test_visualizer_initialization(tmp_path):
    data = _sample_data()
    viz = Visualizer(data, tmp_path)
    assert len(viz.df) == 10
    assert viz.output_dir == tmp_path


def test_visualizer_empty_data(tmp_path):
    viz = Visualizer([], tmp_path)
    assert viz.df.empty


def test_plot_charts_creates_dashboard(tmp_path):
    data = _sample_data()
    viz = Visualizer(data, tmp_path)
    viz.plot_charts()
    dashboard = tmp_path / "dashboard.html"
    assert dashboard.exists()
    content = dashboard.read_text()
    assert "Race Distribution" in content
    assert "Gender Distribution" in content
    assert "Age Distribution" in content


def test_plot_charts_empty_data_no_crash(tmp_path):
    viz = Visualizer([], tmp_path)
    viz.plot_charts()
    dashboard = tmp_path / "dashboard.html"
    assert not dashboard.exists()


def test_visualizer_creates_output_dir(tmp_path):
    output = tmp_path / "new_subdir"
    data = _sample_data(3)
    viz = Visualizer(data, output)
    assert output.exists()


def test_plot_charts_single_gender(tmp_path):
    data = [
        {"file": "img.png", "age": 25, "gender": "Man", "race": "white", "confidence": 0.9}
    ]
    viz = Visualizer(data, tmp_path)
    viz.plot_charts()
    assert (tmp_path / "dashboard.html").exists()


def test_plot_charts_many_genders(tmp_path):
    genders = ["A", "B", "C", "D", "E"]
    data = [
        {"file": f"img{i}.png", "age": 25, "gender": genders[i], "race": "white", "confidence": 0.9}
        for i in range(5)
    ]
    viz = Visualizer(data, tmp_path)
    viz.plot_charts()
    assert (tmp_path / "dashboard.html").exists()
