#!/usr/bin/env python3
"""
IMD API Agricultural Relevance Analyzer
Fetches full responses from all IMD API endpoints and analyzes them for agricultural relevance
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Base URLs
CITY_BASE_URL = "http://100.100.108.101:18080/city"
MAUSAM_BASE_URL = "http://100.100.108.101:18080/mausam"
TIMEOUT = 30

# Sample IDs for parameterized endpoints
SAMPLE_IDS = {
    "city_id": "42182",
    "district_id": "5",
    "station_name": "Jaipur AP",
    "warning_id": "1"
}

class AgriculturalAnalyzer:
    def __init__(self):
        self.endpoints = []
        self.full_responses = {}
        
    def fetch_endpoint(self, name: str, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Fetch full response from an endpoint"""
        print(f"Fetching: {name}...")
        
        endpoint_data = {
            "name": name,
            "url": url,
            "params": params,
            "fetch_time": datetime.now().isoformat(),
            "status": "UNKNOWN",
            "data": None,
            "fields": [],
            "sample_records": [],
            "record_count": 0,
            "data_type": None
        }
        
        try:
            response = requests.get(url, params=params, timeout=TIMEOUT)
            
            if response.status_code == 200:
                endpoint_data["status"] = "SUCCESS"
                
                # Try to parse JSON
                try:
                    json_data = response.json()
                    endpoint_data["data"] = json_data
                    endpoint_data["data_type"] = type(json_data).__name__
                    
                    # Analyze structure
                    if isinstance(json_data, list):
                        endpoint_data["record_count"] = len(json_data)
                        if len(json_data) > 0:
                            # Get fields from first record
                            if isinstance(json_data[0], dict):
                                endpoint_data["fields"] = list(json_data[0].keys())
                            # Get sample records (first 3)
                            endpoint_data["sample_records"] = json_data[:3]
                    elif isinstance(json_data, dict):
                        endpoint_data["fields"] = list(json_data.keys())
                        endpoint_data["record_count"] = 1
                        endpoint_data["sample_records"] = [json_data]
                        
                except json.JSONDecodeError:
                    endpoint_data["data_type"] = "XML/HTML"
                    endpoint_data["data"] = response.text[:1000]
                    
            else:
                endpoint_data["status"] = f"FAILED: HTTP {response.status_code}"
                
        except Exception as e:
            endpoint_data["status"] = f"ERROR: {str(e)}"
        
        self.endpoints.append(endpoint_data)
        return endpoint_data
    
    def fetch_all_endpoints(self):
        """Fetch data from all IMD API endpoints"""
        
        print("="*80)
        print("FETCHING DATA FROM ALL IMD API ENDPOINTS")
        print("="*80)
        
        # City API Endpoints
        print("\n📍 CITY API ENDPOINTS")
        print("-"*80)
        
        self.fetch_endpoint(
            "City Weather 7-day Forecast (All)",
            f"{CITY_BASE_URL}/api/cityweather.php"
        )
        
        self.fetch_endpoint(
            "City Weather 7-day Forecast (Sample City)",
            f"{CITY_BASE_URL}/api/cityweather.php",
            params={"id": SAMPLE_IDS["city_id"]}
        )
        
        self.fetch_endpoint(
            "City Weather with Lat/Lon (All)",
            f"{CITY_BASE_URL}/api/cityweather_loc.php"
        )
        
        self.fetch_endpoint(
            "City Weather with Lat/Lon (Sample City)",
            f"{CITY_BASE_URL}/api/cityweather_loc.php",
            params={"id": SAMPLE_IDS["city_id"]}
        )
        
        self.fetch_endpoint(
            "AWS/ARG Weather Station Data",
            f"{CITY_BASE_URL}/api/aws_data_api.php"
        )
        
        # Mausam API Endpoints
        print("\n🌤️  MAUSAM API ENDPOINTS")
        print("-"*80)
        
        self.fetch_endpoint(
            "Current Weather API (All)",
            f"{MAUSAM_BASE_URL}/api/current_wx_api.php"
        )
        
        self.fetch_endpoint(
            "Current Weather API (Sample City)",
            f"{MAUSAM_BASE_URL}/api/current_wx_api.php",
            params={"id": SAMPLE_IDS["city_id"]}
        )
        
        self.fetch_endpoint(
            "District Wise Nowcast (All)",
            f"{MAUSAM_BASE_URL}/api/nowcast_district_api.php"
        )
        
        self.fetch_endpoint(
            "District Wise Nowcast (Sample District)",
            f"{MAUSAM_BASE_URL}/api/nowcast_district_api.php",
            params={"id": SAMPLE_IDS["district_id"]}
        )
        
        self.fetch_endpoint(
            "District wise Rainfall",
            f"{MAUSAM_BASE_URL}/api/districtwise_rainfall_api.php"
        )
        
        self.fetch_endpoint(
            "District wise Warning (All)",
            f"{MAUSAM_BASE_URL}/api/warnings_district_api.php"
        )
        
        self.fetch_endpoint(
            "District wise Warning (Sample)",
            f"{MAUSAM_BASE_URL}/api/warnings_district_api.php",
            params={"id": SAMPLE_IDS["warning_id"]}
        )
        
        self.fetch_endpoint(
            "Station Wise Nowcast (All)",
            f"{MAUSAM_BASE_URL}/api/nowcastapi.php"
        )
        
        self.fetch_endpoint(
            "Station Wise Nowcast (Sample Station)",
            f"{MAUSAM_BASE_URL}/api/nowcastapi.php",
            params={"id": SAMPLE_IDS["station_name"]}
        )
        
        self.fetch_endpoint(
            "State wise Rainfall",
            f"{MAUSAM_BASE_URL}/api/statewise_rainfall_api.php"
        )
        
        self.fetch_endpoint(
            "RSS Feeds",
            f"{MAUSAM_BASE_URL}/imd_latest/contents/dist_nowcast_rss.php"
        )
        
        self.fetch_endpoint(
            "River Basin QPF",
            f"{MAUSAM_BASE_URL}/api/basin_qpf_api.php"
        )
        
        self.fetch_endpoint(
            "Port Warning",
            f"{MAUSAM_BASE_URL}/api/port_wx_api.php"
        )
        
        self.fetch_endpoint(
            "Sea Area Bulletin",
            f"{MAUSAM_BASE_URL}/api/seaarea_bulletin_api.php"
        )
        
        self.fetch_endpoint(
            "Coastal Area Bulletin",
            f"{MAUSAM_BASE_URL}/api/coastal_bulletin_api.php"
        )
        
        self.fetch_endpoint(
            "5-day Subdivisional Rainfall",
            f"{MAUSAM_BASE_URL}/api/api_5d_subdivisional_rf.php"
        )
        
        self.fetch_endpoint(
            "5-day Statewise Districts Rainfall Forecast",
            f"{MAUSAM_BASE_URL}/api/api_5d_statewisedistricts_rf_forecast.php"
        )
        
        self.fetch_endpoint(
            "Subdivision wise Warning",
            f"{MAUSAM_BASE_URL}/api/api_subDivisionWiseWarning.php"
        )
        
        self.fetch_endpoint(
            "Subdivision wise Rainfall",
            f"{MAUSAM_BASE_URL}/api/subdivisionwise_rainfall_api.php"
        )
        
        print("\n" + "="*80)
        print(f"✅ Completed fetching {len(self.endpoints)} endpoints")
        print("="*80)
    
    def save_full_responses(self, filename: str = "imd_full_responses.json"):
        """Save all full responses to JSON file"""
        output = {
            "fetch_date": datetime.now().isoformat(),
            "total_endpoints": len(self.endpoints),
            "endpoints": self.endpoints
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✅ Full responses saved to: {filename}")
    
    def save_field_analysis(self, filename: str = "endpoint_field_analysis.json"):
        """Save field analysis for each endpoint"""
        analysis = {
            "analysis_date": datetime.now().isoformat(),
            "endpoints": []
        }
        
        for ep in self.endpoints:
            endpoint_analysis = {
                "name": ep["name"],
                "url": ep["url"],
                "status": ep["status"],
                "record_count": ep["record_count"],
                "data_type": ep["data_type"],
                "fields": ep["fields"],
                "sample_records": ep["sample_records"]
            }
            analysis["endpoints"].append(endpoint_analysis)
        
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"✅ Field analysis saved to: {filename}")
    
    def print_summary(self):
        """Print summary of fetched data"""
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        successful = sum(1 for ep in self.endpoints if ep["status"] == "SUCCESS")
        failed = len(self.endpoints) - successful
        
        print(f"Total Endpoints: {len(self.endpoints)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        
        print("\n" + "-"*80)
        print("ENDPOINT OVERVIEW")
        print("-"*80)
        
        for ep in self.endpoints:
            status_symbol = "✓" if ep["status"] == "SUCCESS" else "✗"
            print(f"{status_symbol} {ep['name'][:50]:<50} | Records: {ep['record_count']:>6} | Fields: {len(ep['fields']):>3}")


def main():
    analyzer = AgriculturalAnalyzer()
    
    # Fetch all data
    analyzer.fetch_all_endpoints()
    
    # Save outputs
    analyzer.save_full_responses("imd_full_responses.json")
    analyzer.save_field_analysis("endpoint_field_analysis.json")
    
    # Print summary
    analyzer.print_summary()
    
    print("\n✅ Analysis complete! Ready for agricultural relevance assessment.")


if __name__ == "__main__":
    main()
