"""
This module is responsible for visualizing the demographic data using Bokeh.
It generates an interactive HTML dashboard directly from memory.
"""

from math import pi
from pathlib import Path

import pandas as pd
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.palettes import Category20c, Spectral6
from bokeh.plotting import figure, save
from bokeh.resources import INLINE
from bokeh.transform import cumsum

from src.logger import setup_logger

# Left-closed age bins: [0, 7) is "0-6", [7, 14) is "7-13", ..., [70, inf) is "70+".
AGE_BINS = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, float("inf")]
AGE_LABELS = [
    "0-6",
    "7-13",
    "14-20",
    "21-27",
    "28-34",
    "35-41",
    "42-48",
    "49-55",
    "56-62",
    "63-69",
    "70+",
]

DEFAULT_DASHBOARD_NAME = "dashboard.html"


def dashboard_name_for(csv_path):
    """
    Return the dashboard file name that belongs to a results CSV.

    The dashboard is saved next to its CSV with the same stem, e.g.
    ``utkface_results.csv`` -> ``utkface_results_dashboard.html``, so runs that
    write different CSV files no longer overwrite each other's dashboard.
    """
    return f"{Path(csv_path).stem}_dashboard.html"


def add_shares(counts):
    """
    Add a ``percent`` column and a ``label`` column ("count (percent%)").

    :param counts: DataFrame with a ``count`` column.
    :return: A copy of the DataFrame with the two new columns.
    """
    counts = counts.copy()
    total = counts["count"].sum()
    if total > 0:
        counts["percent"] = (counts["count"] / total * 100).round(1)
    else:
        counts["percent"] = 0.0
    counts["label"] = [
        f"{count} ({percent:.1f}%)"
        for count, percent in zip(counts["count"], counts["percent"])
    ]
    return counts


def _add_bar_labels(plot, source, x_field):
    """Write "count (percent%)" above every bar and leave room for the text."""
    plot.add_layout(
        LabelSet(
            x=x_field,
            y="count",
            text="label",
            source=source,
            text_align="center",
            y_offset=4,
            text_font_size="8pt",
        )
    )
    plot.x_range.range_padding = 0.05
    plot.y_range.start = 0
    plot.y_range.range_padding = 0.2


class Visualizer:
    def __init__(self, data_list, output_dir, dashboard_name=DEFAULT_DASHBOARD_NAME):
        """
        :param data_list: List of dictionaries containing demographic data.
        :param output_dir: Directory where the dashboard will be saved.
        :param dashboard_name: File name of the dashboard. Use a name that is unique
            per run (see ``dashboard_name_for``) so that runs do not overwrite each other.
        """
        self.logger = setup_logger()
        self.output_dir = Path(output_dir)
        self.dashboard_name = dashboard_name

        if data_list:
            self.df = pd.DataFrame(data_list)
            self.logger.info(f"Visualizer initialized with {len(self.df)} records.")
        else:
            self.df = pd.DataFrame()
            self.logger.warning("Visualizer received empty data!")

    def plot_charts(self):
        """
        This function creates an HTML dashboard.

        BokehJS is embedded in the file (inline resources), so the dashboard also
        opens offline and does not depend on an external CDN.

        :return: Path of the written dashboard, or None if nothing was written.
        """
        if self.df.empty:
            self.logger.info("No data to visualize.")
            return None

        output_html = self.output_dir / self.dashboard_name
        self.logger.info("Generating Interactive charts...")

        try:
            # --- GRAPH 1: Race Distribution ---
            if "race" in self.df.columns:
                race_counts = self.df["race"].value_counts().reset_index()
                race_counts.columns = ["race", "count"]
                race_counts = add_shares(race_counts)
                source_race = ColumnDataSource(race_counts)

                p_race = figure(
                    x_range=list(race_counts["race"]),
                    width=800,
                    height=350,
                    title="Race Distribution",
                    toolbar_location=None,
                    tools="",
                )

                p_race.vbar(
                    x="race",
                    top="count",
                    width=0.9,
                    source=source_race,
                    line_color="white",
                    fill_color=Spectral6[0],
                )
                _add_bar_labels(p_race, source_race, "race")

                p_race.add_tools(
                    HoverTool(
                        tooltips=[
                            ("Race", "@race"),
                            ("Count", "@count"),
                            ("Share", "@percent{0.0}%"),
                        ]
                    )
                )
            else:
                p_race = figure(title="No Race Data Found")

            # --- GRAPH 2: Gender Distribution ---
            if "gender" in self.df.columns:
                gender_counts = self.df["gender"].value_counts().reset_index()
                gender_counts.columns = ["gender", "count"]
                gender_counts = add_shares(gender_counts)
                gender_counts["legend"] = (
                    gender_counts["gender"].astype(str) + ": " + gender_counts["label"]
                )

                gender_counts["angle"] = (
                    gender_counts["count"] / gender_counts["count"].sum() * 2 * pi
                )

                if len(gender_counts) == 2:
                    gender_counts["color"] = ["navy", "orange"]
                else:
                    gender_counts["color"] = (
                        Category20c[len(gender_counts)]
                        if len(gender_counts) > 2
                        else ["gray"]
                    )

                source_gender = ColumnDataSource(gender_counts)

                p_gender = figure(
                    height=350,
                    title="Gender Distribution",
                    toolbar_location=None,
                    tools="hover",
                    tooltips="@gender: @count (@percent{0.0}%)",
                    x_range=(-0.5, 1.0),
                )

                p_gender.wedge(
                    x=0,
                    y=1,
                    radius=0.4,
                    start_angle=cumsum("angle", include_zero=True),
                    end_angle=cumsum("angle"),
                    line_color="white",
                    fill_color="color",
                    legend_field="legend",
                    source=source_gender,
                )

                p_gender.axis.visible = False
                p_gender.grid.grid_line_color = None
            else:
                p_gender = figure(title="No Gender Data Found")

            # --- GRAPH 3: Age Distribution (Histogram) ---
            if "age" in self.df.columns:
                self.df["age_group"] = pd.cut(
                    self.df["age"], bins=AGE_BINS, labels=AGE_LABELS, right=False
                )

                age_data = (
                    self.df["age_group"].value_counts().sort_index().reset_index()
                )
                age_data.columns = ["age_group", "count"]
                age_data["age_group"] = age_data["age_group"].astype(str)
                age_data = add_shares(age_data)

                source_age = ColumnDataSource(age_data)

                p_age = figure(
                    x_range=AGE_LABELS,
                    width=800,
                    height=350,
                    title="Age Distribution",
                    toolbar_location=None,
                    tools="",
                )

                p_age.vbar(
                    x="age_group",
                    top="count",
                    width=0.9,
                    source=source_age,
                    line_color="white",
                    fill_color="#40916c",
                )
                _add_bar_labels(p_age, source_age, "age_group")

                p_age.add_tools(
                    HoverTool(
                        tooltips=[
                            ("Age Group", "@age_group"),
                            ("Count", "@count"),
                            ("Share", "@percent{0.0}%"),
                        ]
                    )
                )
            else:
                p_age = figure(title="No Age Data Found")

            # --- SAVE ---
            layout = column(p_race, p_gender, p_age)
            save(
                layout,
                filename=str(output_html),
                resources=INLINE,
                title="DiversityLens Dashboard",
            )

            self.logger.info(f"Dashboard saved successfully: {output_html}")
            return output_html

        except Exception as e:
            self.logger.error(f"Error creating charts: {e}")
            return None
