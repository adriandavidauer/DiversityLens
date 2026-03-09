"""
This module is responsible for visualizing the demographic data using Bokeh.
It generates an interactive HTML dashboard directly from memory.
"""

from math import pi
import pandas as pd
from pathlib import Path

from bokeh.plotting import figure, save, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column
from bokeh.transform import cumsum
from bokeh.palettes import Category20c, Spectral6

from src.logger import setup_logger


class Visualizer:
    def __init__(self, data_list, output_dir):
        """
        :param data_list: List of dictionaries containing demographic data.
        :param output_dir: Directory where the dashboard.html will be saved.
        """
        self.logger = setup_logger()
        self.output_dir = Path(output_dir)

        if data_list:
            self.df = pd.DataFrame(data_list)
            self.logger.info(f"Visualizer initialized with {len(self.df)} records.")
        else:
            self.df = pd.DataFrame()
            self.logger.warning("Visualizer received empty data!")

    def plot_charts(self):
        """
        This function creates an HTML dashboard.
        """
        if self.df.empty:
            self.logger.info("No data to visualize.")
            return

        output_html = self.output_dir / "dashboard.html"

        output_file(output_html, title="DiversityLens Dashboard")
        self.logger.info("Generating Interactive charts...")

        try:
            # --- GRAPH 1: Race Distribution ---
            if "race" in self.df.columns:
                race_counts = self.df["race"].value_counts().reset_index()
                race_counts.columns = ["race", "count"]
                source_race = ColumnDataSource(race_counts)

                p_race = figure(
                    x_range=race_counts["race"],
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

                p_race.add_tools(
                    HoverTool(tooltips=[("Race", "@race"), ("Count", "@count")])
                )
            else:
                p_race = figure(title="No Race Data Found")

            # --- GRAPH 2: Gender Distribution ---
            if "gender" in self.df.columns:
                gender_counts = self.df["gender"].value_counts().reset_index()
                gender_counts.columns = ["gender", "count"]

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
                    tooltips="@gender: @count",
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
                    legend_field="gender",
                    source=source_gender,
                )

                p_gender.axis.visible = False
                p_gender.grid.grid_line_color = None
            else:
                p_gender = figure(title="No Gender Data Found")

            # --- GRAPH 3: Age Distribution (Histogram) ---
            if "age" in self.df.columns:
                bins = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 100]
                labels = [
                    "0-7",
                    "8-14",
                    "15-21",
                    "22-28",
                    "29-35",
                    "36-42",
                    "43-49",
                    "50-56",
                    "57-63",
                    "64-70",
                    "70+",
                ]

                self.df["age_group"] = pd.cut(
                    self.df["age"], bins=bins, labels=labels, right=False
                )

                age_data = (
                    self.df["age_group"].value_counts().sort_index().reset_index()
                )
                age_data.columns = ["age_group", "count"]

                source_age = ColumnDataSource(age_data)

                p_age = figure(
                    x_range=labels,
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

                p_age.add_tools(
                    HoverTool(
                        tooltips=[("Age Group", "@age_group"), ("Count", "@count")]
                    )
                )
            else:
                p_age = figure(title="No Age Data Found")

            # --- SAVE ---
            layout = column(p_race, p_gender, p_age)
            save(layout)

            self.logger.info(f"Dashboard saved successfully: {output_html}")

        except Exception as e:
            self.logger.error(f"Error creating charts: {e}")
