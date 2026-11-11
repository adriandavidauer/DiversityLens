import pandas as pd

from src.visualization import AGE_LABELS, Visualizer, add_shares, dashboard_name_for


def _records(ages=(30,), races=("white",), genders=("Man",)):
    return [
        {"age": age, "race": race, "gender": gender}
        for age, race, gender in zip(ages, races, genders)
    ]


def test_age_labels_match_left_closed_bins(tmp_path):
    ages = [0, 6.9, 7, 13, 14, 20.5, 69, 70, 105]
    records = _records(ages, ["white"] * len(ages), ["Man"] * len(ages))
    viz = Visualizer(records, tmp_path)

    assert viz.plot_charts() is not None
    assert list(viz.df["age_group"].astype(str)) == [
        "0-6",
        "0-6",
        "7-13",
        "7-13",
        "14-20",
        "14-20",
        "63-69",
        "70+",
        "70+",
    ]
    assert AGE_LABELS[0] == "0-6" and AGE_LABELS[-1] == "70+"


def test_dashboard_name_follows_csv_name():
    assert dashboard_name_for("out/utkface_results.csv") == "utkface_results_dashboard.html"


def test_runs_with_different_csv_do_not_overwrite_each_other(tmp_path):
    records = _records()
    first = Visualizer(records, tmp_path, dashboard_name=dashboard_name_for("a.csv")).plot_charts()
    second = Visualizer(records, tmp_path, dashboard_name=dashboard_name_for("b.csv")).plot_charts()

    assert first != second
    assert first.exists() and second.exists()


def test_dashboard_is_self_contained_and_shows_percentages(tmp_path):
    records = _records(
        ages=(20, 30, 40, 50),
        races=("white", "white", "white", "asian"),
        genders=("Man", "Man", "Woman", "Woman"),
    )
    html_path = Visualizer(records, tmp_path).plot_charts()
    html = html_path.read_text(encoding="utf-8")

    assert "cdn.bokeh.org" not in html
    assert "3 (75.0%)" in html


def test_add_shares_adds_percent_and_label():
    counts = pd.DataFrame({"race": ["white", "asian"], "count": [3, 1]})
    shared = add_shares(counts)

    assert list(shared["percent"]) == [75.0, 25.0]
    assert list(shared["label"]) == ["3 (75.0%)", "1 (25.0%)"]
