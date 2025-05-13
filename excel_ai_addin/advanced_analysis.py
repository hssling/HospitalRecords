import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class AdvancedAnalyzer:
    def __init__(self):
        """Initialize the advanced analyzer."""
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        self.isolation_forest = IsolationForest(contamination=0.1)
        self.label_encoder = LabelEncoder()

    def detect_anomalies(self, df):
        """Detect anomalies in the data using Isolation Forest."""
        try:
            # Prepare numerical features
            numerical_features = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numerical_features) > 0:
                X = df[numerical_features].values
                X_scaled = self.scaler.fit_transform(X)
                
                # Detect anomalies
                anomalies = self.isolation_forest.fit_predict(X_scaled)
                
                # Add anomaly column to dataframe
                df['Anomaly'] = anomalies
                
                return df[df['Anomaly'] == -1]  # Return anomalous cases
            return pd.DataFrame()
        except Exception as e:
            print(f"Error detecting anomalies: {str(e)}")
            return pd.DataFrame()

    def cluster_analysis(self, df, n_clusters=3):
        """Perform cluster analysis on the data."""
        try:
            # Prepare numerical features
            numerical_features = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numerical_features) > 0:
                X = df[numerical_features].values
                X_scaled = self.scaler.fit_transform(X)
                
                # Perform PCA
                X_pca = self.pca.fit_transform(X_scaled)
                
                # Perform clustering
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                clusters = kmeans.fit_predict(X_pca)
                
                # Add cluster information to dataframe
                df['Cluster'] = clusters
                
                return df
            return df
        except Exception as e:
            print(f"Error performing cluster analysis: {str(e)}")
            return df

    def analyze_temporal_patterns(self, df):
        """Analyze temporal patterns in the data."""
        try:
            if 'Date' in df.columns:
                # Convert to datetime if not already
                df['Date'] = pd.to_datetime(df['Date'])
                
                # Extract temporal features
                df['Day_of_Week'] = df['Date'].dt.dayofweek
                df['Month'] = df['Date'].dt.month
                df['Year'] = df['Date'].dt.year
                df['Week'] = df['Date'].dt.isocalendar().week
                
                # Calculate daily case counts
                daily_cases = df.groupby(df['Date'].dt.date).size()
                
                # Calculate weekly case counts
                weekly_cases = df.groupby(df['Date'].dt.isocalendar().week).size()
                
                # Calculate monthly case counts
                monthly_cases = df.groupby(df['Date'].dt.month).size()
                
                return {
                    'daily_cases': daily_cases.to_dict(),
                    'weekly_cases': weekly_cases.to_dict(),
                    'monthly_cases': monthly_cases.to_dict()
                }
            return {}
        except Exception as e:
            print(f"Error analyzing temporal patterns: {str(e)}")
            return {}

    def analyze_risk_factors(self, df):
        """Analyze risk factors in the data."""
        try:
            risk_factors = {}
            
            # Age-based risk
            if 'Age' in df.columns:
                risk_factors['age_risk'] = {
                    'high_risk': df[df['Age'] < 5]['Age'].count(),
                    'moderate_risk': df[(df['Age'] >= 5) & (df['Age'] < 18)]['Age'].count(),
                    'low_risk': df[df['Age'] >= 18]['Age'].count()
                }
            
            # Gender-based risk
            if 'Gender' in df.columns:
                risk_factors['gender_risk'] = df['Gender'].value_counts().to_dict()
            
            # District-based risk
            if 'District' in df.columns:
                district_counts = df['District'].value_counts()
                risk_factors['district_risk'] = {
                    'high_risk_districts': district_counts[district_counts > district_counts.mean()].to_dict(),
                    'low_risk_districts': district_counts[district_counts <= district_counts.mean()].to_dict()
                }
            
            # Outcome-based risk
            if 'Outcome' in df.columns:
                risk_factors['outcome_risk'] = df['Outcome'].value_counts().to_dict()
            
            return risk_factors
        except Exception as e:
            print(f"Error analyzing risk factors: {str(e)}")
            return {}

    def predict_outcomes(self, df):
        """Predict outcomes based on available features."""
        try:
            # Prepare features
            categorical_features = df.select_dtypes(include=['object']).columns
            numerical_features = df.select_dtypes(include=['int64', 'float64']).columns
            
            # Encode categorical features
            for feature in categorical_features:
                if feature != 'Outcome':  # Don't encode the target variable
                    df[feature] = self.label_encoder.fit_transform(df[feature])
            
            # Prepare target variable
            if 'Outcome' in df.columns:
                y = self.label_encoder.fit_transform(df['Outcome'])
                
                # Prepare features
                X = df.drop('Outcome', axis=1)
                X = X.select_dtypes(include=['int64', 'float64'])
                
                # Scale features
                X_scaled = self.scaler.fit_transform(X)
                
                # Perform PCA
                X_pca = self.pca.fit_transform(X_scaled)
                
                # Add predictions to dataframe
                df['Predicted_Outcome'] = self.label_encoder.inverse_transform(
                    self.isolation_forest.fit_predict(X_pca)
                )
                
                return df
            return df
        except Exception as e:
            print(f"Error predicting outcomes: {str(e)}")
            return df

    def generate_insights(self, df):
        """Generate comprehensive insights from the data."""
        try:
            insights = {
                'temporal_patterns': self.analyze_temporal_patterns(df),
                'risk_factors': self.analyze_risk_factors(df),
                'anomalies': self.detect_anomalies(df),
                'clusters': self.cluster_analysis(df)
            }
            
            # Add predictions if possible
            if 'Outcome' in df.columns:
                insights['predictions'] = self.predict_outcomes(df)
            
            return insights
        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return {}