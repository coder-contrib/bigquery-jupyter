# BigQuery Weather Analysis with Coder Authentication

This guide shows how to query and analyze weather data from Google BigQuery public datasets using Coder's external authentication in Jupyter notebooks.

## 🎯 Overview

We've created a complete workflow to:
- Authenticate with Google Cloud using Coder's external auth
- Query the GSOD (Global Summary of the Day) public dataset from BigQuery
- Analyze and visualize weather patterns with Python

## 📋 Prerequisites

- Coder workspace with GCP external authentication configured
- Jupyter Lab running
- Python 3.12+ environment

## 🚀 Quick Start

### 1. Use the Ready-Made Notebooks

**Basic Analysis:** `basic-weather-analysis.ipynb` - Complete starter weather analysis
**Advanced Analysis:** `regional-temperature-analysis.ipynb` - Regional temperature trends and comparisons

Simply run all cells in order:
1. **Install packages** (db-dtypes, pyarrow)
2. **Import libraries** (pandas, matplotlib, BigQuery client)
3. **Authenticate** with GCP using Coder token
4. **Query** BigQuery public GSOD dataset
5. **Analyze & visualize** weather data

### 2. Authentication Method

The key breakthrough was using Coder's external auth properly:

```python
import subprocess
from google.oauth2 import credentials
from google.cloud import bigquery

def get_access_token():
    result = subprocess.run(
        ['coder', 'external-auth', 'access-token', 'gcp'],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

# Create authenticated BigQuery client
access_token = get_access_token()
creds = credentials.Credentials(token=access_token)
client = bigquery.Client(credentials=creds, project='coder-vertex-demos')
```

## 📊 Sample Queries & Analysis

### Basic Weather Data Query
```sql
SELECT * 
FROM `bigquery-public-data.samples.gsod` 
LIMIT 500
```

### Advanced Weather Patterns
```sql
SELECT 
    station_number,
    year,
    AVG(mean_temp) as avg_temperature,
    SUM(total_precipitation) as total_rain,
    COUNT(*) as observation_days
FROM `bigquery-public-data.samples.gsod`
WHERE year >= 2020 
  AND mean_temp IS NOT NULL
GROUP BY station_number, year
ORDER BY avg_temperature DESC
LIMIT 100
```

### Seasonal Analysis
```sql
SELECT 
    CASE 
        WHEN month IN (12,1,2) THEN 'Winter'
        WHEN month IN (3,4,5) THEN 'Spring' 
        WHEN month IN (6,7,8) THEN 'Summer'
        ELSE 'Fall'
    END as season,
    AVG(mean_temp) as avg_temp,
    AVG(mean_wind_speed) as avg_wind,
    COUNT(*) as records
FROM `bigquery-public-data.samples.gsod`
WHERE mean_temp IS NOT NULL
GROUP BY season
ORDER BY avg_temp DESC
```

## 🎨 Visualization Examples

The notebook includes these visualizations:

1. **Temperature Distribution** - Histogram of mean temperatures
2. **Precipitation Patterns** - Rain/snow distribution 
3. **Wind Speed Analysis** - Wind patterns across stations
4. **Visibility Trends** - Atmospheric visibility data
5. **Station Analysis** - Top weather stations by data volume

## 💡 Helpful Prompts for Claude

**🎯 Pro Tip**: Always request analysis to be done in Jupyter notebooks for interactive visualization!

### Data Exploration (Claude will create notebooks)
- "Show me temperature trends by geographic region in a notebook"
- "Find the wettest weather stations in the dataset with visualizations"
- "Compare seasonal weather patterns across different years in charts"
- "Identify extreme weather events with interactive plots"

### Advanced Analysis (Claude creates complete notebooks)
- "Create a correlation analysis notebook for weather variables"
- "Build a time series forecasting notebook for temperature trends"
- "Make a clustering notebook for weather stations by climate patterns"
- "Create an anomaly detection notebook for unusual weather readings"

### Visualization Requests (Claude builds notebook cells)
- "Create an interactive weather dashboard in a notebook"
- "Make a comprehensive heatmap analysis of weather patterns"
- "Generate statistical plots comparing regions and seasons"
- "Build a multi-chart weather analysis notebook"

## 🔧 Troubleshooting

### Common Issues & Solutions

**Authentication Errors:**
```bash
# Check if coder auth is working
coder external-auth access-token gcp
```

**Missing Packages:**
```python
# Install BigQuery pandas dependencies  
!pip install db-dtypes pyarrow google-cloud-bigquery
```

**Project Permission Issues:**
- Ensure you're using `project='coder-vertex-demos'` 
- Public datasets are accessible with any valid GCP project

**Import Errors:**
```python
# Add subprocess import for authentication
import subprocess
```

## 📁 File Structure

```
/home/coder/
├── basic-weather-analysis.ipynb      # Main working notebook - basic analysis
├── regional-temperature-analysis.ipynb # Advanced regional temperature analysis
├── weather-analysis-script.py        # Standalone Python script (also works)
└── CLAUDE.md                          # This documentation
```

## 🌟 Key Learnings

1. **Authentication**: Use `credentials.Credentials(token=access_token)` with Coder's GCP token
2. **Project ID**: Specify a valid project even for public datasets
3. **Dependencies**: BigQuery requires `db-dtypes` and `pyarrow` for pandas integration
4. **Error Handling**: Always import `subprocess` where it's used

## 🚀 Next Steps

Try these advanced analyses:
- **Machine Learning**: Predict temperature/precipitation using historical data
- **Geospatial Analysis**: Map weather patterns across geographic regions  
- **Real-time Monitoring**: Set up alerts for extreme weather conditions
- **Climate Research**: Analyze long-term climate change trends

## 📚 Resources

- [BigQuery Public Datasets](https://cloud.google.com/bigquery/public-data)
- [GSOD Dataset Documentation](https://cloud.google.com/bigquery/public-data/samples)
- [Coder External Auth Docs](https://coder.com/docs/external-auth)
- [Google Cloud BigQuery Python Client](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries)

---

*Created with ❤️ using Claude Code and Coder workspaces*