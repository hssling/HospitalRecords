import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import os
from matplotlib.dates import DateFormatter
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class SurveillanceVisualizer:
    def __init__(self, output_dir="visualizations"):
        """Initialize the visualizer with output directory."""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set style
        plt.style.use('seaborn')
        sns.set_palette("husl")

    def create_temporal_analysis(self, df, save_path=None):
        """Create temporal analysis visualizations."""
        try:
            # Create figure with subplots
            fig = make_subplots(rows=2, cols=1, 
                              subplot_titles=('Daily Cases', 'Weekly Trend'),
                              vertical_spacing=0.2)

            # Daily cases
            daily_cases = df.groupby(df['Date'].dt.date).size().reset_index(name='count')
            fig.add_trace(
                go.Scatter(x=daily_cases['Date'], y=daily_cases['count'],
                          mode='lines+markers', name='Daily Cases'),
                row=1, col=1
            )

            # Weekly trend
            weekly_cases = df.groupby(df['Date'].dt.isocalendar().week)['Date'].count()
            fig.add_trace(
                go.Bar(x=weekly_cases.index, y=weekly_cases.values,
                      name='Weekly Cases'),
                row=2, col=1
            )

            # Update layout
            fig.update_layout(
                title_text="Temporal Analysis of Cases",
                height=800,
                showlegend=True
            )

            if save_path:
                fig.write_html(os.path.join(self.output_dir, save_path))
            return fig

        except Exception as e:
            print(f"Error creating temporal analysis: {str(e)}")
            return None

    def create_geographic_distribution(self, df, save_path=None):
        """Create geographic distribution visualization."""
        try:
            # District-wise case distribution
            district_cases = df['District'].value_counts().reset_index()
            district_cases.columns = ['District', 'Cases']

            fig = px.bar(district_cases, 
                        x='District', 
                        y='Cases',
                        title='Case Distribution by District',
                        color='Cases',
                        color_continuous_scale='Viridis')

            if save_path:
                fig.write_html(os.path.join(self.output_dir, save_path))
            return fig

        except Exception as e:
            print(f"Error creating geographic distribution: {str(e)}")
            return None

    def create_age_gender_analysis(self, df, save_path=None):
        """Create age and gender analysis visualization."""
        try:
            # Create age groups
            df['Age_Group'] = pd.cut(df['Age'], 
                                   bins=[0, 5, 12, 18, 60, 100],
                                   labels=['0-5', '6-12', '13-18', '19-60', '60+'])

            # Create pivot table
            age_gender = pd.pivot_table(df, 
                                      values='Age',
                                      index='Age_Group',
                                      columns='Gender',
                                      aggfunc='count')

            fig = px.bar(age_gender,
                        title='Age and Gender Distribution',
                        barmode='group',
                        labels={'value': 'Number of Cases',
                               'Age_Group': 'Age Group',
                               'Gender': 'Gender'})

            if save_path:
                fig.write_html(os.path.join(self.output_dir, save_path))
            return fig

        except Exception as e:
            print(f"Error creating age-gender analysis: {str(e)}")
            return None

    def create_diagnosis_analysis(self, df, save_path=None):
        """Create diagnosis analysis visualization."""
        try:
            # Diagnosis distribution
            diagnosis_cases = df['Diagnosis'].value_counts().reset_index()
            diagnosis_cases.columns = ['Diagnosis', 'Cases']

            fig = px.pie(diagnosis_cases,
                        values='Cases',
                        names='Diagnosis',
                        title='Case Distribution by Diagnosis',
                        hole=0.3)

            if save_path:
                fig.write_html(os.path.join(self.output_dir, save_path))
            return fig

        except Exception as e:
            print(f"Error creating diagnosis analysis: {str(e)}")
            return None

    def create_outcome_analysis(self, df, save_path=None):
        """Create outcome analysis visualization."""
        try:
            # Outcome distribution
            outcome_cases = df['Outcome'].value_counts().reset_index()
            outcome_cases.columns = ['Outcome', 'Cases']

            fig = px.bar(outcome_cases,
                        x='Outcome',
                        y='Cases',
                        title='Case Distribution by Outcome',
                        color='Outcome',
                        color_discrete_sequence=px.colors.qualitative.Set3)

            if save_path:
                fig.write_html(os.path.join(self.output_dir, save_path))
            return fig

        except Exception as e:
            print(f"Error creating outcome analysis: {str(e)}")
            return None

    def create_heatmap(self, df, save_path=None):
        """Create a heatmap of case distribution."""
        try:
            # Create pivot table for heatmap
            heatmap_data = pd.pivot_table(df,
                                        values='Age',
                                        index=df['Date'].dt.date,
                                        columns='District',
                                        aggfunc='count')

            fig = px.imshow(heatmap_data,
                          title='Case Distribution Heatmap',
                          labels=dict(x="District", y="Date", color="Cases"),
                          aspect="auto")

            if save_path:
                fig.write_html(os.path.join(self.output_dir, save_path))
            return fig

        except Exception as e:
            print(f"Error creating heatmap: {str(e)}")
            return None

    def create_dashboard(self, df, save_path="dashboard.html"):
        """Create an interactive dashboard with all visualizations."""
        try:
            # Create subplots
            fig = make_subplots(
                rows=3, cols=2,
                subplot_titles=(
                    'Temporal Analysis', 'Geographic Distribution',
                    'Age-Gender Analysis', 'Diagnosis Distribution',
                    'Outcome Analysis', 'Case Distribution Heatmap'
                )
            )

            # Add all visualizations
            temporal = self.create_temporal_analysis(df)
            geographic = self.create_geographic_distribution(df)
            age_gender = self.create_age_gender_analysis(df)
            diagnosis = self.create_diagnosis_analysis(df)
            outcome = self.create_outcome_analysis(df)
            heatmap = self.create_heatmap(df)

            # Combine all plots
            for trace in temporal.data:
                fig.add_trace(trace, row=1, col=1)
            for trace in geographic.data:
                fig.add_trace(trace, row=1, col=2)
            for trace in age_gender.data:
                fig.add_trace(trace, row=2, col=1)
            for trace in diagnosis.data:
                fig.add_trace(trace, row=2, col=2)
            for trace in outcome.data:
                fig.add_trace(trace, row=3, col=1)
            for trace in heatmap.data:
                fig.add_trace(trace, row=3, col=2)

            # Update layout
            fig.update_layout(
                title_text="Disease Surveillance Dashboard",
                height=1200,
                showlegend=True
            )

            if save_path:
                fig.write_html(os.path.join(self.output_dir, save_path))
            return fig

        except Exception as e:
            print(f"Error creating dashboard: {str(e)}")
            return None