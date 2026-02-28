# IMD API Agricultural Relevance Analysis

**Document Version:** 1.0  
**Analysis Date:** 2026-01-30  
**Total Endpoints Analyzed:** 24

---

## Executive Summary

This document provides a comprehensive analysis of all IMD (India Meteorological Department) API endpoints to help the agricultural team identify which data sources are most relevant for agricultural applications. Each endpoint has been evaluated for agricultural relevance and assigned a rating (🌾 High, 🌱 Medium, 🌿 Low).

### Quick Reference Table

| # | Endpoint Name | Records | Agri Relevance | Key Use Cases |
|---|---------------|---------|----------------|---------------|
| 1 | City Weather 7-day Forecast (All) | 683 | 🌾 **HIGH** | Crop planning, irrigation scheduling |
| 2 | City Weather 7-day Forecast (Specific City) | 1 | 🌾 **HIGH** | Single-city detailed forecast |
| 3 | City Weather with Lat/Lon (All) | 678 | 🌾 **HIGH** | Location-based farm advisories |
| 4 | City Weather with Lat/Lon (Specific City) | 1 | 🌾 **HIGH** | GPS-enabled single-city forecast |
| 5 | AWS/ARG Weather Station Data | 1,187 | 🌾 **HIGH** | Real-time micro-climate monitoring |
| 6 | Current Weather API (All) | 392 | 🌾 **HIGH** | Daily farm operations |
| 7 | Current Weather API (Specific City) | 1 | 🌾 **HIGH** | Single-city current conditions |
| 8 | District Wise Nowcast (All) | 751 | 🌾 **HIGH** | Short-term weather alerts |
| 9 | District Wise Nowcast (Specific District) | 1 | 🌾 **HIGH** | Single-district nowcast |
| 10 | District wise Rainfall | 726 | 🌾 **HIGH** | Irrigation & water management |
| 11 | District wise Warning (All) | 750 | 🌾 **HIGH** | Disaster preparedness |
| 12 | District wise Warning (Specific District) | 1 | 🌾 **HIGH** | Single-district warnings |
| 13 | Station Wise Nowcast (All) | 1,209 | 🌾 **HIGH** | Localized weather tracking |
| 14 | Station Wise Nowcast (Specific Station) | 1 | 🌾 **HIGH** | Single-station nowcast |
| 15 | State wise Rainfall | 41 | 🌱 **MEDIUM** | Regional planning |
| 16 | 5-day Subdivisional Rainfall | 36 | 🌾 **HIGH** | Medium-term planning |
| 17 | 5-day Districts Rainfall Forecast | 748 | 🌾 **HIGH** | District-level planning |
| 18 | Subdivision wise Warning | 36 | 🌱 **MEDIUM** | Regional alerts |
| 19 | Subdivision wise Rainfall | 41 | 🌱 **MEDIUM** | Regional rainfall tracking |
| 20 | River Basin QPF | 11 | 🌱 **MEDIUM** | Flood risk assessment |
| 21 | Port Warning | 148 | 🌿 **LOW** | Coastal agriculture only |
| 22 | Sea Area Bulletin | 16 | 🌿 **LOW** | Marine/coastal specific |
| 23 | Coastal Area Bulletin | 16 | 🌿 **LOW** | Coastal agriculture |
| 24 | RSS Feeds | N/A | 🌿 **LOW** | General alerts |

---

## Detailed Endpoint Analysis

### 1. City Weather 7-day Forecast

**Endpoint:** `/city/api/cityweather.php`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 683 cities  
**Data Type:** JSON Array

#### Available Fields (38 total)
- **Temperature Data:** `Today_Max_temp`, `Today_Min_temp`, `Todays_Forecast_Max_Temp`, `Todays_Forecast_Min_temp`, Day 2-7 forecasts
- **Rainfall:** `Past_24_hrs_Rainfall`
- **Humidity:** `Relative_Humidity_at_0830`, `Relative_Humidity_at_1730`
- **Forecast:** 7-day weather forecasts with descriptions
- **Astronomical:** Sunrise, Sunset, Moonrise, Moonset times

#### Sample Data
```json
{
  "Station_Name": "Faridabad",
  "Today_Min_temp": "8.2",
  "Past_24_hrs_Rainfall": "NIL",
  "Relative_Humidity_at_0830": "NA",
  "Todays_Forecast": "Mainly Clear sky",
  "Day_2_Forecast": "Partly cloudy sky",
  "Day_3_Forecast": "Partly cloudy sky with one or two spells of rain"
}
```

#### Agricultural Use Cases
1. **Crop Planning:** 7-day temperature forecasts help plan sowing/harvesting activities
2. **Irrigation Scheduling:** Rainfall forecasts reduce unnecessary irrigation
3. **Pest Management:** Temperature and humidity data predict pest outbreaks
4. **Frost Protection:** Minimum temperature alerts for sensitive crops
5. **Harvest Timing:** Weather forecasts optimize harvest windows

#### Key Fields for Agriculture
- ✅ `Past_24_hrs_Rainfall` - Critical for soil moisture assessment
- ✅ `Relative_Humidity_at_0830` / `at_1730` - Disease risk prediction
- ✅ `Day_1` through `Day_7` forecasts - Planning operations
- ✅ `Today_Min_temp` / `Today_Max_temp` - Crop stress indicators

---

### 2. City Weather with Lat/Lon

**Endpoint:** `/city/api/cityweather_loc.php`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 678 cities  
**Data Type:** JSON Array

#### Additional Fields (40 total)
All fields from City Weather 7-day Forecast **PLUS**:
- `Latitude`
- `Longitude`

#### Agricultural Use Cases
1. **Precision Agriculture:** GPS coordinates enable field-level mapping
2. **Farm Location Matching:** Match farms to nearest weather stations
3. **Spatial Analysis:** Create weather interpolation maps
4. **Mobile Apps:** Location-based farmer advisories
5. **GIS Integration:** Combine with farm boundary data

#### Key Advantage
The latitude/longitude data makes this endpoint **essential for location-based agricultural services** and precision farming applications.

---

### 3. AWS/ARG Weather Station Data

**Endpoint:** `/city/api/aws_data_api.php`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 1,187 stations  
**Data Type:** JSON Array

#### Available Fields (24 total)
- **Location:** `STATE`, `DISTRICT`, `STATION`, `Latitude`, `Longitude`
- **Temperature:** `CURR_TEMP`, `MIN_TEMP`, `MAX_TEMP`, `DEW_POINT_TEMP`, `Feel Like`
- **Humidity:** `RH` (Relative Humidity)
- **Wind:** `WIND_DIRECTION`, `WIND_SPEED`
- **Pressure:** `MSLP` (Mean Sea Level Pressure)
- **Weather:** `WEATHER_CODE`, `NEBULOSITY`, `WEATHER_MESSAGE`
- **Timestamp:** `DATE`, `TIME`

#### Sample Data
```json
{
  "STATION": "PUROLA",
  "DISTRICT": "UTTARKASHI",
  "STATE": "UTTARAKHAND",
  "CURR_TEMP": "12.5",
  "RH": "65",
  "MIN_TEMP": "4.8",
  "MAX_TEMP": "20.4",
  "WIND_SPEED": 0,
  "Latitude": "30.86",
  "Longitude": "78"
}
```

#### Agricultural Use Cases
1. **Real-time Monitoring:** Current conditions for immediate decisions
2. **Micro-climate Analysis:** District-level granular data
3. **Evapotranspiration Calculation:** Temperature, humidity, wind for ET estimation
4. **Spray Operations:** Wind speed data for pesticide application timing
5. **Frost Alerts:** Real-time minimum temperature monitoring
6. **Heat Stress:** Maximum temperature tracking for livestock/crops

#### Key Fields for Agriculture
- ✅ `CURR_TEMP`, `MIN_TEMP`, `MAX_TEMP` - Thermal stress monitoring
- ✅ `RH` - Disease risk and irrigation needs
- ✅ `WIND_SPEED` - Spray operations and pollination
- ✅ `DEW_POINT_TEMP` - Dew formation for disease prediction
- ✅ `DISTRICT` + `STATE` - Administrative boundary matching

---

### 4. Current Weather API

**Endpoint:** `/mausam/api/current_wx_api.php`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 392 stations  
**Data Type:** JSON Array

#### Available Fields (21 total)
- **Station:** `Station Id`, `Station`
- **Meteorological:** `Temperature`, `Humidity`, `Mean Sea Level Pressure`
- **Wind:** `Wind Direction`, `Wind Speed KMPH`
- **Rainfall:** `Last 24 hrs Rainfall`
- **Weather:** `Weather Code`, `Nebulosity`, `WEATHER_MESSAGE`
- **Astronomical:** `Sunrise`, `Sunset`, `Moonrise`, `Moonset`
- **Timestamp:** `Date of Observation`, `Time`

#### Agricultural Use Cases
1. **Daily Operations:** Current conditions for field work planning
2. **Rainfall Tracking:** 24-hour rainfall for irrigation decisions
3. **Weather Conditions:** Descriptive weather messages for advisories
4. **Timing Operations:** Sunrise/sunset for work scheduling

#### Key Fields for Agriculture
- ✅ `Last 24 hrs Rainfall` - **Critical** for water management
- ✅ `Temperature` - Crop growth stage monitoring
- ✅ `Humidity` - Disease risk assessment
- ✅ `Wind Speed KMPH` - Spray timing decisions

---

### 5. District Wise Nowcast

**Endpoint:** `/mausam/api/nowcast_district_api.php`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 751 districts  
**Data Type:** JSON Array

#### Available Fields (26 total)
- **Location:** `State_District`
- **Weather Categories:** `cat1` through `cat19` (weather event flags)
- **Timing:** `toi` (Time of Issue), `vupto` (Valid Up To)
- **Alert Level:** `color` (1-4 severity)
- **Message:** `message` (descriptive text)

#### Weather Categories (Decoded)
- `cat1`: No warning
- `cat2`: Thunderstorm
- `cat3`: Dust storm
- `cat4`: Squall
- `cat5`: Hail
- `cat6`: Heavy rainfall
- `cat7`: Very heavy rainfall
- Additional categories for various severe weather events

#### Agricultural Use Cases
1. **Immediate Alerts:** 3-hour advance warnings for severe weather
2. **Field Operations:** Pause/resume decisions for harvesting, spraying
3. **Livestock Protection:** Move animals before storms
4. **Hail Protection:** Deploy protective measures for crops
5. **Heavy Rain Alerts:** Drainage management

#### Key Fields for Agriculture
- ✅ `cat5` (Hail) - **Critical** for crop protection
- ✅ `cat6`, `cat7` (Heavy rainfall) - Flood risk
- ✅ `cat2` (Thunderstorm) - Worker safety
- ✅ `vupto` - Validity period for planning

---

### 6. District wise Rainfall

**Endpoint:** `/mausam/api/districtwise_rainfall_api.php`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 726 districts  
**Data Type:** JSON Array

#### Available Fields (23 total)
- **Location:** `District`, `State`
- **Daily Rainfall:** `Daily Actual`, `Daily Normal`, `Daily Departure Per`, `Daily Category`
- **Weekly Rainfall:** `Weekly Actual`, `Weekly Normal`, `Weekly Departure Per`, `Weekly Category`
- **Cumulative Rainfall:** `Cumulative Actual`, `Cumulative Normal`, `Cumulative Departue Per`, `Cumulative Category`
- **Monthly Rainfall:** `Monthly Acutual`, `Monthly Normal`, `Monthly Departure Per`, `Monthly Category`
- **Date Ranges:** `Week Date`, `Cumulative Date`, `Monthly Date`

#### Rainfall Categories
- **NR:** No Rain
- **D:** Deficient
- **LD:** Large Deficient
- **N:** Normal
- **E:** Excess
- **LE:** Large Excess

#### Sample Data
```json
{
  "District": "ADILABAD",
  "State": "TELANGANA",
  "Daily Actual": "0.00",
  "Daily Normal": "0.20",
  "Daily Departure Per": "-100%",
  "Weekly Actual": "0.00",
  "Cumulative Actual": "0.00",
  "Cumulative Normal": "9.80",
  "Cumulative Category": "NR"
}
```

#### Agricultural Use Cases
1. **Drought Monitoring:** Track cumulative rainfall deficits
2. **Irrigation Planning:** Identify districts needing supplemental water
3. **Crop Insurance:** Rainfall deviation data for claims
4. **Sowing Decisions:** Cumulative rainfall determines sowing viability
5. **Water Resource Management:** District-level water availability

#### Key Fields for Agriculture
- ✅ `Cumulative Actual` vs `Cumulative Normal` - **Most critical** for season planning
- ✅ `Daily Actual` - Immediate irrigation decisions
- ✅ `Weekly Actual` - Short-term water management
- ✅ `Cumulative Category` - Quick drought/excess assessment

---

### 7. District wise Warning

**Endpoint:** `/mausam/api/warnings_district_api.php`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 750 districts  
**Data Type:** JSON Array

#### Available Fields (14 total)
- **Location:** `District`
- **5-Day Warnings:** `Day_1` through `Day_5` (warning types)
- **Severity Colors:** `Day1_Color` through `Day5_Color`
- **Metadata:** `Date`, `updated_at`

#### Color Codes (Severity Levels)
- **1 (Green):** No warning
- **2 (Yellow):** Be aware
- **3 (Orange):** Be prepared
- **4 (Red):** Take action

#### Agricultural Use Cases
1. **5-Day Planning:** Advance warning for farm operations
2. **Disaster Preparedness:** Prepare for severe weather
3. **Harvest Scheduling:** Avoid warning periods
4. **Resource Allocation:** Deploy resources to high-risk districts

#### Key Fields for Agriculture
- ✅ `Day_1` through `Day_5` - Planning horizon
- ✅ Color codes - Severity assessment
- ✅ `District` - Administrative alignment

---

### 8. Station Wise Nowcast

**Endpoint:** `/mausam/api/nowcastapi.php`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 1,209 stations  
**Data Type:** JSON Array

#### Available Fields (25 total)
Similar to District Wise Nowcast but at **station level** (more granular)
- **Location:** `Station`
- **Weather Categories:** `cat1` through `cat19`
- **Timing:** `toi`, `vupto`
- **Alert:** `color`, `message`

#### Agricultural Use Cases
1. **Hyper-local Alerts:** Station-specific warnings
2. **Farm-level Decisions:** Match farms to nearest stations
3. **Precision Alerts:** More accurate than district-level

#### Advantage Over District Nowcast
**1,209 stations** vs **751 districts** = **Better spatial resolution**

---

### 9. State wise Rainfall

**Endpoint:** `/mausam/api/statewise_rainfall_api.php`  
**Agricultural Relevance:** 🌱 **MEDIUM**  
**Records Available:** 41 states/UTs  
**Data Type:** JSON Array

#### Available Fields (21 total)
Same structure as District wise Rainfall but aggregated at **state level**

#### Agricultural Use Cases
1. **Regional Planning:** State-level agricultural policy
2. **Resource Allocation:** Inter-state water sharing
3. **Macro Analysis:** National agricultural trends

#### Limitation
**Too coarse for farm-level decisions** - Use district-level data instead

---

### 10. 5-day Subdivisional Rainfall

**Endpoint:** `/mausam/api/api_5d_subdivisional_rf.php`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 36 subdivisions  
**Data Type:** JSON Array

#### Available Fields (23 total)
- **Location:** `Subdivision`, `State`
- **5-Day Forecast:** Daily rainfall predictions
- **Cumulative:** Total expected rainfall
- **Categories:** Rainfall intensity classifications

#### Agricultural Use Cases
1. **Medium-term Planning:** 5-day advance planning
2. **Sowing Windows:** Identify rainfall periods for sowing
3. **Irrigation Scheduling:** Plan around forecasted rainfall

---

### 11. 5-day Statewise Districts Rainfall Forecast

**Endpoint:** `/mausam/api/api_5d_statewisedistricts_rf_forecast.php`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 748 districts  
**Data Type:** JSON Array

#### Available Fields (19 total)
- **Location:** `District`, `State`
- **5-Day Forecast:** Day-wise rainfall predictions
- **Categories:** Rainfall intensity for each day

#### Agricultural Use Cases
1. **District-level Forecasting:** More granular than subdivision
2. **Crop Advisory:** District-specific recommendations
3. **Water Management:** Plan reservoir releases

#### Advantage
**District-level granularity** makes this more actionable than subdivision data

---

### 12. Subdivision wise Warning

**Endpoint:** `/mausam/api/api_subDivisionWiseWarning.php`  
**Agricultural Relevance:** 🌱 **MEDIUM**  
**Records Available:** 36 subdivisions  
**Data Type:** JSON Array

#### Available Fields (17 total)
- **Location:** `Subdivision`
- **5-Day Warnings:** Warning types and severity
- **Color Codes:** Severity levels

#### Agricultural Use Cases
1. **Regional Alerts:** Subdivision-level warnings
2. **Multi-district Planning:** Broader than district warnings

#### Limitation
**Less granular than district warnings** - Use district-level for better precision

---

### 13. Subdivision wise Rainfall

**Endpoint:** `/mausam/api/subdivisionwise_rainfall_api.php`  
**Agricultural Relevance:** 🌱 **MEDIUM**  
**Records Available:** 41 subdivisions  
**Data Type:** JSON Array

#### Available Fields (21 total)
Same structure as district rainfall but at **subdivision level**

#### Agricultural Use Cases
1. **Regional Monitoring:** Broader rainfall patterns
2. **Agro-climatic Zone Analysis:** Subdivision often aligns with zones

#### Limitation
**Use district-level data for more precise decisions**

---

### 14. River Basin QPF (Quantitative Precipitation Forecast)

**Endpoint:** `/mausam/api/basin_qpf_api.php`  
**Agricultural Relevance:** 🌱 **MEDIUM**  
**Records Available:** 11 basins  
**Data Type:** JSON Array

#### Available Fields (12 total)
- **Location:** `Basin`, `SubBasin`, `FMO` (Forecasting Office)
- **Area:** `Area (Sq. Km.)`
- **5-Day Forecast:** `Day1` through `Day5` (rainfall categories)
- **Antecedent:** `AAP` (Antecedent Precipitation)

#### Rainfall Categories (1-5)
1. No rain / Very light rain
2. Light rain
3. Moderate rain
4. Heavy rain
5. Very heavy rain

#### Agricultural Use Cases
1. **Flood Risk Assessment:** Basin-level flood predictions
2. **Watershed Management:** Catchment area rainfall
3. **Reservoir Planning:** Inflow predictions

#### Limitation
**Only 11 basins** - Limited coverage, more relevant for water resource management than direct farming

---

### 15. Port Warning

**Endpoint:** `/mausam/api/port_wx_api.php`  
**Agricultural Relevance:** 🌿 **LOW**  
**Records Available:** 148 ports  
**Data Type:** JSON Array

#### Available Fields (10 total)
- **Location:** `Port Name`, `Latitude`, `Longitude`
- **Warning:** `Warning`, `Signal`
- **Metadata:** `Issued By`, `Date of Issue`, `Time of Issue`

#### Agricultural Use Cases
1. **Coastal Agriculture:** Limited to coastal farms
2. **Fisheries:** More relevant for fishing than farming
3. **Export Logistics:** Port conditions for agricultural exports

#### Limitation
**Highly specialized** - Only relevant for coastal/marine agriculture

---

### 16. Sea Area Bulletin

**Endpoint:** `/mausam/api/seaarea_bulletin_api.php`  
**Agricultural Relevance:** 🌿 **LOW**  
**Records Available:** 16 sea areas  
**Data Type:** JSON Array

#### Agricultural Use Cases
**Minimal** - Primarily for marine operations, not land-based agriculture

---

### 17. Coastal Area Bulletin

**Endpoint:** `/mausam/api/coastal_bulletin_api.php`  
**Agricultural Relevance:** 🌿 **LOW**  
**Records Available:** 16 coastal areas  
**Data Type:** JSON Array

#### Agricultural Use Cases
1. **Coastal Farming:** Limited to coastal regions
2. **Salt Pan Operations:** Coastal salt production
3. **Aquaculture:** Coastal fish/shrimp farming

---

---

### 1a. City Weather 7-day Forecast (Specific City)

**Endpoint:** `/city/api/cityweather.php?id={city_id}`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 1 city (filtered)  
**Data Type:** JSON Array  
**Parameter:** `id` - Station Code (e.g., `42182` for New Delhi-Safdarjung)

#### Available Fields (38 total)
Same as endpoint #1

#### Sample Data
```json
{
  "Station_Code": "42182",
  "Station_Name": "New Delhi-Safdarjung",
  "Todays_Forecast": "Partly cloudy sky",
  "Day_2_Forecast": "Thunderstorm with rain"
}
```

#### Agricultural Use Cases
1. **Farm-Specific Forecasts:** Weather data for a specific farm's nearest city
2. **API Efficiency:** Reduced bandwidth and faster response
3. **Mobile Applications:** Ideal for location-based apps

#### When to Use
- ✅ Use when you know the exact station code
- ✅ Use for single-location queries in mobile apps
- ✅ Use to reduce data transfer

---

### 2a. City Weather with Lat/Lon (Specific City)

**Endpoint:** `/city/api/cityweather_loc.php?id={city_id}`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 1 city (filtered)  
**Data Type:** JSON Array  
**Parameter:** `id` - Station Code

#### Available Fields (40 total)
Same as endpoint #2 (includes Latitude, Longitude)

#### Agricultural Use Cases
1. **GPS-based Farm Matching:** Match farm coordinates to nearest station
2. **Precision Agriculture:** Combine weather with exact location data
3. **GIS Integration:** Direct integration with mapping systems

---

### 4a. Current Weather API (Specific City)

**Endpoint:** `/mausam/api/current_wx_api.php?id={city_id}`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 1 station (filtered)  
**Data Type:** JSON Array  
**Parameter:** `id` - Station ID

#### Available Fields (21 total)
Same as endpoint #4

#### Sample Data
```json
{
  "Station": "New Delhi-Safdarjung",
  "Temperature": "10.2",
  "Humidity": "100",
  "Last 24 hrs Rainfall": "0",
  "Wind Speed KMPH": 0
}
```

#### Agricultural Use Cases
1. **Real-time Farm Monitoring:** Current conditions for specific location
2. **Immediate Decisions:** Quick access to current weather
3. **IoT Integration:** Feed data to automated farm systems

---

### 5a. District Wise Nowcast (Specific District)

**Endpoint:** `/mausam/api/nowcast_district_api.php?id={district_id}`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 1 district (filtered)  
**Data Type:** JSON Array  
**Parameter:** `id` - District Object ID

#### Available Fields (26 total)
Same as endpoint #5

#### Sample Data
```json
{
  "State_District": "WEST GARO HILLS",
  "cat1": "1",
  "cat5": "0",
  "color": "1",
  "vupto": "1900"
}
```

#### Agricultural Use Cases
1. **District-Specific Alerts:** Targeted warnings for one district
2. **Administrative Alignment:** Match government district boundaries
3. **Focused Monitoring:** Track specific agricultural zones

---

### 7a. District wise Warning (Specific District)

**Endpoint:** `/mausam/api/warnings_district_api.php?id={warning_id}`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 1 district (filtered)  
**Data Type:** JSON Array  
**Parameter:** `id` - Warning Object ID

#### Available Fields (14 total)
Same as endpoint #7

#### Agricultural Use Cases
1. **5-Day District Alerts:** Advance warnings for specific district
2. **Targeted Advisories:** District-specific agricultural advisories
3. **Resource Planning:** Allocate resources to specific districts

---

### 8a. Station Wise Nowcast (Specific Station)

**Endpoint:** `/mausam/api/nowcastapi.php?id={station_name}`  
**Agricultural Relevance:** 🌾 **HIGH**  
**Records Available:** 1 station (filtered)  
**Data Type:** JSON Array  
**Parameter:** `id` - Station Name (e.g., "Jaipur AP")

#### Available Fields (25 total)
Same as endpoint #8

#### Sample Data
```json
{
  "Station": "Jaipur AP",
  "cat2": "0",
  "cat5": "0",
  "toi": "1800",
  "vupto": "2130"
}
```

#### Agricultural Use Cases
1. **Hyper-local Nowcasts:** Station-specific 3-hour forecasts
2. **Farm-Station Matching:** Match farms to nearest weather station
3. **Precision Alerts:** Most granular nowcast available

---

### 18. RSS Feeds

**Endpoint:** `/mausam/imd_latest/contents/dist_nowcast_rss.php`  
**Agricultural Relevance:** 🌿 **LOW**  
**Data Type:** XML/RSS

#### Agricultural Use Cases
**General alerts** - Better to use structured JSON endpoints

---

## Priority Recommendations for Agriculture

### Tier 1: Essential Endpoints (Must Integrate)
1. ✅ **District wise Rainfall** - Critical for water management
2. ✅ **City Weather with Lat/Lon** - Location-based advisories
3. ✅ **AWS/ARG Weather Station Data** - Real-time monitoring
4. ✅ **District Wise Nowcast** - Immediate weather alerts
5. ✅ **5-day Districts Rainfall Forecast** - Medium-term planning

### Tier 2: Highly Valuable (Recommended)
6. ✅ **Current Weather API** - Daily operations
7. ✅ **District wise Warning** - Disaster preparedness
8. ✅ **Station Wise Nowcast** - Hyper-local alerts
9. ✅ **City Weather 7-day Forecast** - Weekly planning

### Tier 3: Supplementary (Optional)
10. ✅ **State wise Rainfall** - Regional context
11. ✅ **5-day Subdivisional Rainfall** - Medium-term regional
12. ✅ **River Basin QPF** - Flood risk

### Tier 4: Specialized (Use Case Specific)
13. ⚠️ **Port/Sea/Coastal Bulletins** - Only for coastal agriculture

---

## Data Integration Strategies

### Strategy 1: Multi-Source Validation
Combine multiple endpoints for robust advisories:
- **Rainfall:** District wise Rainfall + 5-day Forecast + Nowcast
- **Temperature:** City Weather + AWS/ARG + Current Weather
- **Warnings:** District Warning + Nowcast

### Strategy 2: Spatial Hierarchy
Use appropriate granularity:
- **Farm-level:** AWS/ARG stations (1,187 points)
- **Village-level:** City Weather with Lat/Lon (678 points)
- **District-level:** District Rainfall/Warnings (750 districts)
- **Regional-level:** State/Subdivision data

### Strategy 3: Temporal Integration
Combine different time horizons:
- **Now:** Current Weather + Nowcast (0-3 hours)
- **Today:** City Weather (today's forecast)
- **Week:** 7-day Forecast
- **Season:** Cumulative Rainfall

---

## Field Mapping for Agricultural Applications

### Critical Fields Across Endpoints

| Agricultural Need | Endpoint | Key Field |
|-------------------|----------|-----------|
| **Irrigation Decision** | District Rainfall | `Cumulative Actual` vs `Normal` |
| **Spray Timing** | AWS/ARG | `WIND_SPEED`, `RH` |
| **Frost Protection** | City Weather | `Today_Min_temp` |
| **Disease Risk** | Current Weather | `Humidity`, `Temperature` |
| **Flood Alert** | District Nowcast | `cat6`, `cat7` (heavy rain) |
| **Hail Protection** | District Nowcast | `cat5` |
| **Sowing Window** | 5-day Rainfall Forecast | Daily predictions |
| **Harvest Timing** | District Warning | 5-day warnings |

---

## Next Steps for Agri Team

1. **Review Priority Endpoints:** Focus on Tier 1 endpoints first
2. **Identify Use Cases:** Map your specific agricultural advisories to endpoints
3. **Test Integration:** Start with 2-3 high-priority endpoints
4. **Validate Data Quality:** Check data freshness and accuracy
5. **Build Prototypes:** Create sample advisories using the data
6. **Scale Gradually:** Add more endpoints as needed

---

## Technical Notes

### Data Freshness
- **Real-time:** AWS/ARG, Current Weather (updated hourly)
- **Daily:** Rainfall data (updated daily)
- **Nowcast:** Updated every 3 hours
- **Forecasts:** Updated twice daily (morning/evening)

### Data Quality Considerations
- Some fields may have `null` or `"NA"` values
- Rainfall categories use specific codes (NR, D, LD, N, E, LE)
- Color codes for warnings are standardized (1-4)
- Weather categories in nowcast use numeric flags (0/1)

### API Usage Tips
- Use `id` parameter to filter specific locations
- Without `id`, endpoints return all available data
- Combine location filters with data needs
- Cache forecast data to reduce API calls

---

## Contact & Feedback

For questions or feedback on this analysis, please contact the technical team.

**Document Prepared By:** Agricultural API Analysis Team  
**Last Updated:** 2026-01-30
