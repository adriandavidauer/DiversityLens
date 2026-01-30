"""
This module is responsible for visualizing the demographic data using Bokeh.
It generates an interactive HTML dashboard.
"""
from math import pi
import pandas as pd
from pathlib import Path

from bokeh.plotting import figure, save, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column
from bokeh.transform import cumsum, jitter
from bokeh.palettes import Category20c, Spectral6

from src.logger import setup_logger


class Visualizer():
    def __init__(self, csv_path):
        """
        :param csv_path: Path to the dataset directory.
        """
        self.csv_path = Path(csv_path)
        self.logger= setup_logger()
        self.df= None #### Embedding the dataframe into the class' initialization
    def load_data(self):
        """
        Loads the CSV data into a pandas DataFrame.
        :return: True if successful, False otherwise.
        """
        if not self.csv_path.exists():
            self.logger.error(f"The given path doesn't exist!")
            return False
        try: 
            self.df= pd.read_csv(self.csv_path) ### Read the CSV File
            self.logger.info(f"Data loaded successfully. Rows: {len(self.df)}")
            return True
        except Exception as e:
            self.logger.error(f"Error loading CSV: {e}")
            return False
        
    def plot_charts(self):
        """
        This function creates an HTML dashboard.
        """
        if self.df is None or self.df.empty:
            self.logger.info("No data to visualize.")
            return
        
        output_dir= Path("results")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_html= output_dir / "output.html"

        #Bokeh file setting
        output_file(output_html, title="DiversityLens Dashboard")
        self.logger.info("Generating Interactive charts.")
        try:
            ##GRAPH 1: Race Distribution
            race_counts= self.df['race'].value_counts().reset_index()
            race_counts.columns= ['race', 'count']
            source_race= ColumnDataSource(race_counts)
            p_race = figure(x_range=race_counts['race'], height=350, title="Race Distribution",
                            toolbar_location=None, tools="") # Drawing
            
            p_race.vbar(x='race', top='count', width=0.9, source=source_race, 
                        line_color='white', fill_color=Spectral6[0]) # Color Setting
            
            p_race.add_tools(HoverTool(tooltips=[("Race", "@race"), ("Count", "@count")])) #Interactive Information Display

            ##GRAPH 2: Gender Distribution
            gender_counts= self.df['gender'].value_counts().reset_index()
            gender_counts.columns= ['gender', 'count']
            
            gender_counts['angle'] = gender_counts['count'] / gender_counts['count'].sum() * 2*pi  # Angle Graph is used


            if len(gender_counts)==2:
                gender_counts['color']= ['pink', 'blue']
            else:
                gender_counts['color']= Category20c[len(gender_counts)]

            source_gender= ColumnDataSource(gender_counts)

            p_gender = figure(height=350, title="Gender Distribution", toolbar_location=None,
                              tools="hover", tooltips="@gender: @count", x_range=(-0.5, 1.0))
            
            p_gender.wedge(x=0, y=1, radius=0.4,
                           start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                           line_color="white", fill_color='color', legend_field='gender', source=source_gender)
            
            p_gender.axis.visible = False
            p_gender.grid.grid_line_color = None

            
              ##GRAPH 3: Age Distribution

            self.df['age_str'] = self.df['age'].astype(str)
            age_order = sorted(self.df['age_str'].unique(), key=lambda x: int(x) if x.isdigit() else x)
            
            source_full = ColumnDataSource(self.df)
            
            p_age = figure(x_range=age_order, height=450, title="Age Distribution (Point Cloud)",
                           toolbar_location="above", tools="hover,pan,wheel_zoom,reset")

            # jitter on 'age_str' spreads dots horizontally within the age category
            # jitter on 'age' spreads dots vertically for a cloud effect
            p_age.circle(x=jitter('age_str', width=0.7, range=p_age.x_range), 
                         y=jitter('age', width=0.5, distribution='uniform'), 
                         source=source_full, 
                         size=5, 
                         fill_color=Spectral6[0], 
                         line_color=None, 
                         fill_alpha=0.5) # Alpha helps see density

            p_age.add_tools(HoverTool(tooltips=[("Age", "@age"), ("Gender", "@gender"), ("Race", "@race")]))
            
            # Optional: Hide Y axis if it's purely for visual cloud spread
            p_age.yaxis.axis_label = "Age Density"
            
            layout = column(p_race, p_gender, p_age)
            save(layout)
        
            self.logger.info(f"Dashboard saved successfully: {output_html}")


        except Exception as e:
            self.logger.error(f"Error creating charts: {e}")