import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from excel_ai_addin import ExcelAIAnalyzer
from advanced_analysis import AdvancedAnalyzer
from visualization import SurveillanceVisualizer

class TestExcelAIAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data."""
        # Create sample data
        cls.test_data = pd.DataFrame({
            'Date': pd.date_range(start='2024-01-01', periods=10),
            'District': ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Delhi',
                        'Mumbai', 'Bangalore', 'Chennai', 'Delhi', 'Mumbai'],
            'Age': [5, 3, 7, 4, 6, 5, 4, 3, 7, 6],
            'Gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
            'Symptoms': ['Fever', 'Fever', 'Fever', 'Fever', 'Fever',
                        'Fever', 'Fever', 'Fever', 'Fever', 'Fever'],
            'Diagnosis': ['Rash', 'Rash', 'Rash', 'Rash', 'Rash',
                         'Rash', 'Rash', 'Rash', 'Rash', 'Rash'],
            'Lab_Result': ['Positive', 'Positive', 'Positive', 'Negative',
                          'Positive', 'Positive', 'Positive', 'Negative',
                          'Positive', 'Positive'],
            'Outcome': ['Recovered', 'Recovered', 'Under Treatment', 'Recovered',
                       'Under Treatment', 'Recovered', 'Under Treatment',
                       'Recovered', 'Under Treatment', 'Recovered']
        })
        
        # Initialize analyzers
        cls.analyzer = ExcelAIAnalyzer()
        cls.advanced_analyzer = AdvancedAnalyzer()
        cls.visualizer = SurveillanceVisualizer(output_dir='test_visualizations')

    def test_read_excel_data(self):
        """Test reading Excel data."""
        # Save test data to Excel
        test_file = 'test_data.xlsx'
        self.test_data.to_excel(test_file, index=False)
        
        # Test reading
        df = self.analyzer.read_excel_data(test_file)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), len(self.test_data))
        
        # Clean up
        os.remove(test_file)

    def test_analyze_data(self):
        """Test data analysis."""
        insights = self.analyzer.analyze_data(self.test_data)
        self.assertIsInstance(insights, dict)
        self.assertIn('summary', insights)
        self.assertIn('statistics', insights)
        self.assertIn('trends', insights)

    def test_advanced_analysis(self):
        """Test advanced analysis features."""
        # Test anomaly detection
        anomalies = self.advanced_analyzer.detect_anomalies(self.test_data)
        self.assertIsInstance(anomalies, pd.DataFrame)
        
        # Test cluster analysis
        clustered_data = self.advanced_analyzer.cluster_analysis(self.test_data)
        self.assertIn('Cluster', clustered_data.columns)
        
        # Test risk factor analysis
        risk_factors = self.advanced_analyzer.analyze_risk_factors(self.test_data)
        self.assertIsInstance(risk_factors, dict)
        self.assertIn('age_risk', risk_factors)

    def test_visualization(self):
        """Test visualization features."""
        # Test temporal analysis
        temporal_fig = self.visualizer.create_temporal_analysis(self.test_data)
        self.assertIsNotNone(temporal_fig)
        
        # Test geographic distribution
        geo_fig = self.visualizer.create_geographic_distribution(self.test_data)
        self.assertIsNotNone(geo_fig)
        
        # Test dashboard creation
        dashboard = self.visualizer.create_dashboard(self.test_data)
        self.assertIsNotNone(dashboard)

    def test_report_generation(self):
        """Test report generation."""
        insights = self.analyzer.analyze_data(self.test_data)
        output_path = 'test_report.docx'
        
        # Test report generation
        self.analyzer.generate_report(insights, output_path)
        self.assertTrue(os.path.exists(output_path))
        
        # Clean up
        os.remove(output_path)

    @classmethod
    def tearDownClass(cls):
        """Clean up test files."""
        if os.path.exists('test_visualizations'):
            for file in os.listdir('test_visualizations'):
                os.remove(os.path.join('test_visualizations', file))
            os.rmdir('test_visualizations')

if __name__ == '__main__':
    unittest.main() 