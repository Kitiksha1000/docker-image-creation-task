# KCC Analysis Project Structure

## Directory Organization

```
kcc_analysis/
├── scripts/           # All Python analysis scripts
├── data/             # Symlinks or references to data files
├── outputs/          # All analysis outputs
│   ├── json/        # JSON results
│   ├── csv/         # CSV exports
│   └── reports/     # Markdown/PDF reports
├── logs/            # Processing logs
└── config/          # Configuration files
```

## Main Dataset
- **Location:** `/home/ubuntu/Kshitij/Testing IMD API/kcc_master_dataset.csv`
- **Size:** ~8 GB (~80-90 million records)
- **Period:** 2006-2025

## Scripts Overview

1. **1_explore_dataset.py** - Full dataset statistics (GPU/CPU optimized)
2. **2_language_analysis.py** - Multilingual language detection
3. **3_weather_query_extraction.py** - Extract weather queries (15+ languages)
4. **4_parameter_analysis.py** - Weather parameter frequency analysis
5. **5_temporal_trends.py** - 19-year evolution analysis
6. **6_regional_analysis.py** - State-wise patterns
7. **7_imd_mapping.py** - Map to IMD API endpoints
8. **8_generate_reports.py** - Final deliverables generation

## Outputs

### JSON Files
- `exploration_results_full.json` - Complete dataset statistics
- `language_distribution.json` - Language breakdown
- `weather_queries.json` - Filtered weather queries
- `parameter_frequency.json` - Weather parameter counts
- `temporal_trends.json` - Yearly evolution
- `regional_patterns.json` - State-wise analysis

### CSV Files
- `weather_queries_full.csv` - All weather-related queries
- `top_queries.csv` - Top 100 most frequent queries
- `imd_api_mapping.csv` - Query-to-API mapping

### Reports
- `exploration_report.md` - Dataset overview
- `weather_analysis_report.md` - Weather query insights
- `temporal_evolution_report.md` - 19-year trends
- `priority_recommendations.md` - Final recommendations

## Processing Strategy

- **NO SAMPLING** - Process entire 8GB dataset
- **Parallel Processing:** Multiprocessing, Dask, GPU (if applicable)
- **Memory Management:** Chunked reading with optimized chunk sizes
- **Progress Tracking:** Real-time progress bars and logging
