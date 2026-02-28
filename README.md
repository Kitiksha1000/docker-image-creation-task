# IMD API Testing & Agricultural Analysis Project

**Project Overview:** Comprehensive analysis of India Meteorological Department (IMD) API endpoints for agricultural applications, combined with Kisan Call Center (KCC) dataset analysis to understand farmer weather information needs.

**Last Updated:** February 27, 2026

---

## 📁 Project Structure

```
Testing IMD API/
├── scripts/                    # Python scripts for testing and analysis
│   ├── test_imd_api.py        # Main IMD API testing script (24 endpoints)
│   ├── analyze_imd_for_agriculture.py  # Agricultural relevance analyzer
│   ├── analyze_kcc_quick.py   # Quick KCC dataset analysis
│   └── convert_to_html.py     # Markdown to HTML converter
│
├── docs/                       # Documentation and reports
│   ├── agricultural_relevance_analysis.md     # Complete endpoint analysis (793 lines)
│   ├── agricultural_relevance_analysis.html   # HTML version
│   ├── agricultural_relevance_analysis.pdf    # PDF version
│   ├── endpoint_coverage_verification.md      # Endpoint coverage checklist
│   └── imd_api_test_report.html              # API test results report
│
├── outputs/                    # JSON results and data files
│   ├── imd_api_test_report.json          # API test results
│   ├── imd_full_responses.json           # Complete API responses
│   └── endpoint_field_analysis.json      # Field-level analysis
│
├── kcc_analysis/              # KCC Dataset Analysis (8GB, 43.5M records)
│   ├── config/                # Configuration files
│   │   └── config.py
│   ├── data/                  # Data files (symlinks/references)
│   ├── logs/                  # Processing logs
│   ├── outputs/               # Analysis results
│   │   ├── csv/              # CSV exports
│   │   ├── json/             # JSON results
│   │   │   └── exploration_full.json  # Full dataset statistics
│   │   └── reports/          # Analysis reports
│   ├── scripts/               # Analysis scripts
│   │   ├── 1_explore_dataset.py          # GPU-accelerated full analysis
│   │   └── explore_kcc_dataset.py        # Multilingual explorer
│   └── README.md             # KCC analysis documentation
│
├── requirements.txt           # Python dependencies
├── discover_endpoints.sh      # Bash script to discover API endpoints
└── README.md                  # This file
```

---

## 🎯 Project Goals

1. ✅ **Document all IMD API endpoints** - Comprehensive testing of 24 endpoints
2. ✅ **Evaluate agricultural relevance** - Rate each endpoint for farming use cases
3. ✅ **Analyze farmer needs** - Extract insights from 43.5M KCC queries
4. ✅ **Map queries to APIs** - Connect farmer questions to appropriate data sources
5. ✅ **Provide recommendations** - Guide agricultural application developers

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test IMD APIs
```bash
python scripts/test_imd_api.py
```
- Tests all 24 IMD endpoints
- Generates JSON and HTML reports
- Shows performance metrics and data samples

### 3. Analyze Agricultural Relevance
```bash
python scripts/analyze_imd_for_agriculture.py
```
- Fetches complete responses from all endpoints
- Analyzes agricultural relevance
- Generates detailed field-level analysis

### 4. Analyze KCC Dataset
```bash
cd kcc_analysis/scripts
python 1_explore_dataset.py
```
- Processes entire 8GB dataset (43.5M records)
- GPU-accelerated analysis
- Generates comprehensive statistics

---

## 📊 Key Findings

### IMD API Endpoints (24 Total)

**High Priority for Agriculture (18 endpoints):**
- 🌾 City Weather 7-day Forecast (683 cities)
- 🌾 AWS/ARG Weather Station Data (1,187 stations)
- 🌾 District-wise Rainfall & Warnings (750 districts)
- 🌾 Real-time Nowcasts (3-hour advance warnings)
- 🌾 5-day Rainfall Forecasts

**Medium Priority (4 endpoints):**
- 🌱 State/Subdivision level data
- 🌱 River Basin QPF

**Low Priority (2 endpoints):**
- 🌿 Marine/Coastal specific data

### KCC Dataset Insights

**From 43,477,170 total queries:**
- **Weather Queries:** 15,103,606 (34.7%) - **#1 category!**
- **Plant Protection:** 9,750,747 (22.4%)
- **Government Schemes:** 4,672,958 (10.7%)
- **Period:** 2006-2025 (19 years)
- **Languages:** Multilingual support

**Key Insight:** Weather is the top concern for farmers calling KCC.

---

## 📖 Documentation

### Main Documents

1. **[Agricultural Relevance Analysis](docs/agricultural_relevance_analysis.md)**
   - Complete guide to all 24 endpoints
   - Agricultural use cases for each API
   - Priority recommendations
   - Field mapping for agricultural applications
   - 793 lines of comprehensive analysis

2. **[Endpoint Coverage Verification](docs/endpoint_coverage_verification.md)**
   - Verification that all endpoints are documented
   - Quick reference checklist

3. **[KCC Analysis README](kcc_analysis/README.md)**
   - KCC dataset structure and analysis plan
   - Processing strategy for 8GB dataset

### Generated Reports

- **HTML Reports:** User-friendly styled reports in `docs/`
- **JSON Results:** Machine-readable results in `outputs/`
- **KCC Statistics:** Full dataset analysis in `kcc_analysis/outputs/json/`

---

## 🔧 Scripts Overview

### `scripts/test_imd_api.py`
**Purpose:** Comprehensive testing of all IMD API endpoints

**Features:**
- Tests 24 endpoints (City API + Mausam API)
- Performance metrics (response time, data size)
- Data structure analysis
- Colored terminal output
- Generates JSON and HTML reports

**Output:**
- `outputs/imd_api_test_report.json`
- `docs/imd_api_test_report.html`

### `scripts/analyze_imd_for_agriculture.py`
**Purpose:** Fetch full responses and analyze agricultural relevance

**Features:**
- Fetches complete data from all endpoints
- Analyzes field structure
- Extracts sample records
- Counts total records per endpoint

**Output:**
- `outputs/imd_full_responses.json`
- `outputs/endpoint_field_analysis.json`

### `scripts/analyze_kcc_quick.py`
**Purpose:** Quick analysis of KCC dataset (100k sample)

**Features:**
- Quick overview of dataset structure
- Weather-related query detection
- Top query types and sectors
- Sample queries examination

### `kcc_analysis/scripts/1_explore_dataset.py`
**Purpose:** Full dataset analysis with GPU acceleration

**Features:**
- Processes entire 8GB dataset (NO sampling)
- GPU-accelerated (NVIDIA H200 support)
- Multi-core CPU parallelization
- Language detection
- Comprehensive statistics

**Output:**
- `kcc_analysis/outputs/json/exploration_full.json`

---

## 🌐 IMD API Base URLs

```
City API:   http://100.100.108.101:18080/city
Mausam API: http://100.100.108.101:18080/mausam
```

### Sample Endpoints

```bash
# Get all city weather forecasts (683 cities)
curl "http://100.100.108.101:18080/city/api/cityweather.php"

# Get specific city forecast
curl "http://100.100.108.101:18080/city/api/cityweather.php?id=42182"

# Get all weather stations (1,187 stations)
curl "http://100.100.108.101:18080/city/api/aws_data_api.php"

# Get district-wise rainfall (726 districts)
curl "http://100.100.108.101:18080/mausam/api/districtwise_rainfall_api.php"

# Get district nowcasts (751 districts)
curl "http://100.100.108.101:18080/mausam/api/nowcast_district_api.php"
```

---

## 📦 Dependencies

From `requirements.txt`:
```
requests   - HTTP library for API calls
tabulate   - Pretty table formatting
```

Optional for KCC analysis:
```
pandas     - Data manipulation
cudf       - GPU-accelerated dataframes (RAPIDS)
cupy       - GPU-accelerated NumPy
langdetect - Language identification
```

---

## 🎯 Priority Recommendations

### For Agricultural Applications

**Tier 1: Essential (Must Integrate)**
1. District-wise Rainfall - Water management
2. City Weather with Lat/Lon - Location-based advisories
3. AWS/ARG Weather Stations - Real-time monitoring
4. District Nowcast - Immediate alerts
5. 5-day Rainfall Forecast - Medium-term planning

**Tier 2: Highly Valuable**
6. Current Weather API - Daily operations
7. District Warnings - Disaster preparedness
8. Station Nowcast - Hyper-local alerts

**Tier 3: Supplementary**
9. State/Subdivision data - Regional context
10. River Basin QPF - Flood risk

---

## 💡 Use Cases

### For Farmers
- 7-day weather forecasts for crop planning
- Rainfall alerts for irrigation scheduling
- Hail warnings for crop protection
- Temperature forecasts for frost protection
- Wind speed data for spray timing

### For Agri-Tech Companies
- Location-based weather advisories
- Crop insurance risk assessment
- Precision agriculture applications
- Farm management systems
- Automated irrigation systems

### For Government Agencies
- Disaster preparedness planning
- Agricultural policy decisions
- Resource allocation
- State/district-level monitoring

---

## 📈 Data Coverage

- **Cities:** 683 with 7-day forecasts
- **Weather Stations:** 1,187 real-time AWS/ARG stations
- **Districts:** 750+ with warnings and rainfall data
- **States:** 41 states/UTs
- **Subdivisions:** 36 meteorological subdivisions

---

## 🔍 Technical Details

### API Testing
- **Timeout:** 30 seconds per request
- **Method:** GET requests
- **Response Format:** JSON (primary), XML/RSS (some endpoints)
- **Data Freshness:** Hourly to daily updates

### Performance
- **GPU Support:** NVIDIA H200 (143GB VRAM)
- **CPU Cores:** 24 cores utilized
- **Chunk Size:** 2M rows per chunk
- **Processing:** Full dataset, no sampling

---

## 📝 Next Steps

1. **Review Documentation:** Start with `docs/agricultural_relevance_analysis.md`
2. **Test APIs:** Run `scripts/test_imd_api.py` to verify access
3. **Identify Use Cases:** Map your needs to appropriate endpoints
4. **Prototype Integration:** Start with Tier 1 endpoints
5. **Scale Gradually:** Add more endpoints as needed

---

## 🤝 Contributing

This is a comprehensive reference project. To extend or improve:

1. Test additional endpoints not yet covered
2. Add more agricultural use case examples
3. Improve KCC analysis scripts
4. Create visualization tools for data
5. Develop sample integration code

---

## 📄 License

Internal project for agricultural technology development.

---

## 📧 Contact

For questions or feedback, contact the agricultural API analysis team.

**Project Maintained By:** Agricultural Technology Team  
**Last Updated:** February 27, 2026
