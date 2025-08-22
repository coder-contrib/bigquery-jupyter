#!/usr/bin/env python3
"""
BigQuery Weather Analysis - Standalone Script

Complete weather analysis using Coder external auth and BigQuery public datasets.
Can be run directly or used as reference for notebook development.
"""

import sys
import subprocess

# Install required packages
try:
    import pandas as pd
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--break-system-packages', 'pandas', 'matplotlib', 'seaborn', 'google-cloud-bigquery', 'db-dtypes', 'pyarrow'])
import subprocess
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import bigquery
from google.oauth2 import credentials
import warnings
warnings.filterwarnings('ignore')

# Set up plotting
plt.style.use('default')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = (12, 8)

def get_access_token():
    try:
        result = subprocess.run(
            ['coder', 'external-auth', 'access-token', 'gcp'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f'Error: {e}')
        return None

# Get access token and create BigQuery client
access_token = get_access_token()
if access_token:
    print('✅ Access token obtained')
    creds = credentials.Credentials(token=access_token)
    client = bigquery.Client(credentials=creds, project='coder-vertex-demos')
    print('✅ BigQuery client ready')
    
    # Query the GSOD dataset
    query = '''
    SELECT * 
    FROM `bigquery-public-data.samples.gsod` 
    LIMIT 500
    '''
    
    print('🔍 Executing BigQuery query...')
    df = client.query(query).to_dataframe()
    print(f'✅ Retrieved {len(df)} rows')
    print(f'📋 Columns: {list(df.columns)}')
    
    # Display first few rows
    print('\n📊 First 5 rows:')
    print(df.head())
    
    # Dataset info
    print('\n📈 Dataset info:')
    df.info()
    
    # Statistical summary
    print('\n🔢 Statistical summary:')
    print(df.describe())
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Weather Data Analysis - GSOD Dataset', fontsize=16)
    
    # Temperature
    if 'mean_temp' in df.columns:
        temp_clean = df[df['mean_temp'].notna()]['mean_temp']
        axes[0,0].hist(temp_clean, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0,0].set_title('Mean Temperature Distribution')
        axes[0,0].set_xlabel('Temperature (°F)')
        axes[0,0].set_ylabel('Frequency')
    
    # Precipitation
    if 'total_precipitation' in df.columns:
        prcp_clean = df[df['total_precipitation'].notna()]['total_precipitation']
        axes[0,1].hist(prcp_clean, bins=30, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0,1].set_title('Total Precipitation Distribution')
        axes[0,1].set_xlabel('Precipitation (inches)')
        axes[0,1].set_ylabel('Frequency')
    
    # Wind Speed
    if 'mean_wind_speed' in df.columns:
        wind_clean = df[df['mean_wind_speed'].notna()]['mean_wind_speed']
        axes[1,0].hist(wind_clean, bins=30, alpha=0.7, color='coral', edgecolor='black')
        axes[1,0].set_title('Mean Wind Speed Distribution')
        axes[1,0].set_xlabel('Wind Speed (knots)')
        axes[1,0].set_ylabel('Frequency')
    
    # Visibility
    if 'mean_visibility' in df.columns:
        vis_clean = df[df['mean_visibility'].notna()]['mean_visibility']
        axes[1,1].hist(vis_clean, bins=30, alpha=0.7, color='gold', edgecolor='black')
        axes[1,1].set_title('Mean Visibility Distribution')
        axes[1,1].set_xlabel('Visibility (miles)')
        axes[1,1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.show()
    
    # Station analysis
    if 'station_number' in df.columns:
        top_stations = df['station_number'].value_counts().head(10)
        
        plt.figure(figsize=(12, 6))
        top_stations.plot(kind='bar', color='steelblue', alpha=0.8)
        plt.title('Top 10 Weather Stations by Number of Records')
        plt.xlabel('Station ID')
        plt.ylabel('Number of Records')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        print(f'\n📡 Total unique stations: {df["station_number"].nunique()}')
        print('🏆 Top 10 stations:')
        for i, (station, count) in enumerate(top_stations.items(), 1):
            print(f'{i:2d}. Station {station}: {count} records')
    
    print('\n✅ Weather data analysis complete!')
    
else:
    print('❌ Failed to get access token')