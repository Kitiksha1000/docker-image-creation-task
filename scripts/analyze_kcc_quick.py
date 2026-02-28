#!/usr/bin/env python3
"""
Quick Analysis of KCC Master Dataset
Analyze weather-related queries from Kisan Call Center data
"""

import pandas as pd
import re
from collections import Counter

# Read just first 100k rows to understand structure
print("Reading sample data...")
df_sample = pd.read_csv('kcc_master_dataset.csv', nrows=100000)

print("\n" + "="*80)
print("DATASET OVERVIEW")
print("="*80)
print(f"Sample size: {len(df_sample):,} rows")
print(f"\nColumns: {list(df_sample.columns)}")
print(f"\nData types:\n{df_sample.dtypes}")

print("\n" + "="*80)
print("BASIC STATISTICS")
print("="*80)
print(f"\nUnique States: {df_sample['StateName'].nunique()}")
print(f"Unique Districts: {df_sample['DistrictName'].nunique()}")
print(f"Unique Crops: {df_sample['Crop'].nunique()}")
print(f"Unique Query Types: {df_sample['QueryType'].nunique()}")

print("\n" + "="*80)
print("TOP QUERY TYPES")
print("="*80)
print(df_sample['QueryType'].value_counts().head(15))

print("\n" + "="*80)
print("TOP SECTORS")
print("="*80)
print(df_sample['Sector'].value_counts().head(10))

print("\n" + "="*80)
print("SAMPLE QUERIES")
print("="*80)
print(df_sample[['QueryType', 'QueryText', 'KccAns']].head(10).to_string())

# Weather-related keyword search
print("\n" + "="*80)
print("WEATHER-RELATED QUERY DETECTION")
print("="*80)

weather_keywords = [
    'rain', 'rainfall', 'weather', 'temperature', 'drought', 'water',
    'irrigation', 'frost', 'cold', 'heat', 'monsoon', 'wind', 'storm',
    'flood', 'dry', 'wet', 'humidity', 'fog', 'hail', 'climate'
]

pattern = '|'.join(weather_keywords)
df_sample['is_weather'] = df_sample['QueryText'].fillna('').str.lower().str.contains(pattern, regex=True)

weather_count = df_sample['is_weather'].sum()
weather_pct = (weather_count / len(df_sample)) * 100

print(f"Weather-related queries in sample: {weather_count:,} ({weather_pct:.1f}%)")

# Show weather query examples
print("\nSample Weather-Related Queries:")
weather_queries = df_sample[df_sample['is_weather']][['QueryType', 'QueryText','KccAns']].head(20)
print(weather_queries.to_string())

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nNext: Run full dataset analysis to extract all weather-related queries")
