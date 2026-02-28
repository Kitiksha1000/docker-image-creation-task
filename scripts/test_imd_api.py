#!/usr/bin/env python3
"""
Comprehensive IMD API Testing Script
Tests all official API endpoints for city.imd.gov.in and mausam.imd.gov.in
Using base URLs: http://100.100.108.101:18080/city and http://100.100.108.101:18080/mausam
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from tabulate import tabulate
import sys

# Base URLs
CITY_BASE_URL = "http://100.100.108.101:18080/city"
MAUSAM_BASE_URL = "http://100.100.108.101:18080/mausam"

# Test configuration
TIMEOUT = 30  # seconds
SAMPLE_IDS = {
    "city_id": "42182",
    "district_id": "5",
    "station_name": "Jaipur AP",
    "warning_id": "1"
}

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class APITester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def test_endpoint(self, name: str, url: str, method: str = "GET", 
                     params: Optional[Dict] = None, data: Optional[Dict] = None,
                     test_with_params: bool = False) -> Dict[str, Any]:
        """Test a single API endpoint"""
        self.total_tests += 1
        result = {
            "name": name,
            "url": url,
            "method": method,
            "params": params,
            "status": "UNKNOWN",
            "status_code": None,
            "response_time": None,
            "response_size": None,
            "content_type": None,
            "error": None,
            "sample_data": None,
            "data_structure": None,
            "record_count": None
        }
        
        try:
            start_time = time.time()
            
            if method == "GET":
                response = requests.get(url, params=params, timeout=TIMEOUT)
            elif method == "POST":
                response = requests.post(url, data=data, timeout=TIMEOUT)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response_time = time.time() - start_time
            
            result["status_code"] = response.status_code
            result["response_time"] = round(response_time, 3)
            result["response_size"] = len(response.content)
            result["content_type"] = response.headers.get("Content-Type", "Unknown")
            
            # Check if response is successful
            if response.status_code == 200:
                result["status"] = "PASS"
                self.passed_tests += 1
                
                # Try to parse JSON
                try:
                    json_data = response.json()
                    result["sample_data"] = self._get_sample_data(json_data)
                    result["data_structure"] = self._analyze_structure(json_data)
                    result["record_count"] = self._count_records(json_data)
                except json.JSONDecodeError:
                    result["sample_data"] = response.text[:200]
                    result["data_structure"] = "Non-JSON response (likely HTML)"
            else:
                result["status"] = "FAIL"
                result["error"] = f"HTTP {response.status_code}"
                result["sample_data"] = response.text[:200]
                self.failed_tests += 1
                
        except requests.exceptions.Timeout:
            result["status"] = "FAIL"
            result["error"] = "Request timeout"
            self.failed_tests += 1
        except requests.exceptions.ConnectionError:
            result["status"] = "FAIL"
            result["error"] = "Connection error"
            self.failed_tests += 1
        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
            self.failed_tests += 1
        
        self.results.append(result)
        return result
    
    def _count_records(self, data: Any) -> Optional[int]:
        """Count number of records in response"""
        if isinstance(data, list):
            return len(data)
        elif isinstance(data, dict):
            # Look for common array fields
            for key in data.keys():
                if isinstance(data[key], list):
                    return len(data[key])
        return None
    
    def _get_sample_data(self, data: Any, max_items: int = 1) -> Any:
        """Extract sample data from response"""
        if isinstance(data, list):
            return data[:max_items] if len(data) > 0 else []
        elif isinstance(data, dict):
            # Return first few keys
            sample = {}
            for i, (k, v) in enumerate(data.items()):
                if i >= max_items:
                    break
                if isinstance(v, list):
                    sample[k] = f"<array with {len(v)} items>"
                elif isinstance(v, dict):
                    sample[k] = f"<object with {len(v)} keys>"
                else:
                    sample[k] = str(v)[:50]
            return sample
        else:
            return str(data)[:100]
    
    def _analyze_structure(self, data: Any) -> str:
        """Analyze the structure of response data"""
        if isinstance(data, list):
            if len(data) > 0:
                first_item = data[0]
                if isinstance(first_item, dict):
                    keys = list(first_item.keys())[:5]
                    return f"Array of {len(data)} objects with keys: {', '.join(keys)}"
                return f"Array of {len(data)} {type(first_item).__name__} items"
            return "Empty array"
        elif isinstance(data, dict):
            keys = list(data.keys())[:5]
            return f"Object with keys: {', '.join(keys)}"
        else:
            return f"Primitive type: {type(data).__name__}"
    
    def print_progress(self, current: int, total: int, name: str, status: str):
        """Print progress during testing"""
        percentage = (current / total) * 100
        status_symbol = f"{Colors.GREEN}✓{Colors.RESET}" if status == "PASS" else f"{Colors.RED}✗{Colors.RESET}"
        print(f"[{current}/{total}] {status_symbol} {name[:60]}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print(f"{Colors.BOLD}IMD API TEST SUMMARY{Colors.RESET}")
        print("="*80)
        print(f"Total Tests: {Colors.BOLD}{self.total_tests}{Colors.RESET}")
        print(f"Passed: {Colors.GREEN}{self.passed_tests}{Colors.RESET} ({self.passed_tests/self.total_tests*100:.1f}%)")
        print(f"Failed: {Colors.RED}{self.failed_tests}{Colors.RESET} ({self.failed_tests/self.total_tests*100:.1f}%)")
        print("="*80)
    
    def print_results_table(self):
        """Print results in table format"""
        table_data = []
        for r in self.results:
            status_display = f"{Colors.GREEN}PASS{Colors.RESET}" if r["status"] == "PASS" else f"{Colors.RED}FAIL{Colors.RESET}"
            table_data.append([
                r["name"][:35],
                status_display,
                r["status_code"] or "N/A",
                f"{r['response_time']}s" if r["response_time"] else "N/A",
                r["record_count"] if r["record_count"] else "-",
                r["error"] or "OK"
            ])
        
        headers = ["Endpoint", "Status", "HTTP", "Time", "Records", "Note"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def save_json_report(self, filename: str = "imd_api_test_report.json"):
        """Save detailed report as JSON"""
        report = {
            "test_date": datetime.now().isoformat(),
            "base_urls": {
                "city": CITY_BASE_URL,
                "mausam": MAUSAM_BASE_URL
            },
            "summary": {
                "total_tests": self.total_tests,
                "passed": self.passed_tests,
                "failed": self.failed_tests,
                "pass_rate": f"{self.passed_tests/self.total_tests*100:.1f}%"
            },
            "results": self.results
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{Colors.GREEN}✓{Colors.RESET} Detailed JSON report saved to: {Colors.BOLD}{filename}{Colors.RESET}")
    
    def save_html_report(self, filename: str = "imd_api_test_report.html"):
        """Save HTML report"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>IMD API Test Report</title>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 4px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
            font-size: 32px;
        }}
        .meta {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .meta p {{
            margin: 5px 0;
            color: #34495e;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .summary-card.passed {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        .summary-card.failed {{
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        }}
        .summary-card h3 {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 10px;
        }}
        .summary-card .value {{
            font-size: 42px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .summary-card .subtitle {{
            font-size: 16px;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        th {{
            background: #34495e;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
            font-size: 13px;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .status-pass {{
            color: #27ae60;
            font-weight: bold;
        }}
        .status-fail {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .endpoint-name {{
            font-weight: 600;
            color: #2c3e50;
        }}
        .endpoint-url {{
            font-size: 11px;
            color: #7f8c8d;
            font-family: 'Courier New', monospace;
            margin-top: 3px;
        }}
        .section {{
            margin: 40px 0;
        }}
        .section h2 {{
            color: #2c3e50;
            border-left: 5px solid #3498db;
            padding-left: 15px;
            margin-bottom: 20px;
            font-size: 24px;
        }}
        code {{
            background: #ecf0f1;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }}
        .badge-success {{
            background: #d4edda;
            color: #155724;
        }}
        .badge-danger {{
            background: #f8d7da;
            color: #721c24;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌦️ IMD API Comprehensive Test Report</h1>
        
        <div class="meta">
            <p><strong>Test Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>City Base URL:</strong> <code>{CITY_BASE_URL}</code></p>
            <p><strong>Mausam Base URL:</strong> <code>{MAUSAM_BASE_URL}</code></p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total Tests</h3>
                <div class="value">{self.total_tests}</div>
                <div class="subtitle">API Endpoints</div>
            </div>
            <div class="summary-card passed">
                <h3>Passed</h3>
                <div class="value">{self.passed_tests}</div>
                <div class="subtitle">{self.passed_tests/self.total_tests*100:.1f}% Success Rate</div>
            </div>
            <div class="summary-card failed">
                <h3>Failed</h3>
                <div class="value">{self.failed_tests}</div>
                <div class="subtitle">{self.failed_tests/self.total_tests*100:.1f}% Failure Rate</div>
            </div>
        </div>
        
        <div class="section">
            <h2>Detailed Test Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Endpoint</th>
                        <th>Status</th>
                        <th>HTTP Code</th>
                        <th>Response Time</th>
                        <th>Records</th>
                        <th>Data Structure</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for r in self.results:
            status_class = "status-pass" if r["status"] == "PASS" else "status-fail"
            badge_class = "badge-success" if r["status"] == "PASS" else "badge-danger"
            params_str = f"?{r['params']}" if r.get('params') else ""
            
            html += f"""
                    <tr>
                        <td>
                            <div class="endpoint-name">{r['name']}</div>
                            <div class="endpoint-url">{r['url']}{params_str}</div>
                        </td>
                        <td><span class="badge {badge_class}">{r['status']}</span></td>
                        <td>{r['status_code'] or 'N/A'}</td>
                        <td>{r['response_time']}s</td>
                        <td>{r['record_count'] if r['record_count'] else '-'}</td>
                        <td style="font-size: 11px; color: #7f8c8d;">{r['error'] or r['data_structure'] or 'OK'}</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
        
        with open(filename, 'w') as f:
            f.write(html)
        
        print(f"{Colors.GREEN}✓{Colors.RESET} HTML report saved to: {Colors.BOLD}{filename}{Colors.RESET}")


def main():
    print("="*80)
    print(f"{Colors.BOLD}IMD API COMPREHENSIVE TESTING{Colors.RESET}")
    print("="*80)
    print(f"City Base URL: {Colors.BLUE}{CITY_BASE_URL}{Colors.RESET}")
    print(f"Mausam Base URL: {Colors.BLUE}{MAUSAM_BASE_URL}{Colors.RESET}")
    print(f"Timeout: {TIMEOUT}s")
    print("="*80)
    
    tester = APITester()
    test_count = 0
    total_tests = 25  # Approximate total
    
    # ========================================================================
    # PART A: CITY API ENDPOINTS
    # ========================================================================
    print(f"\n{Colors.BOLD}📍 PART A: Testing City API Endpoints{Colors.RESET}")
    print("-" * 80)
    
    # 1. City weather forecast (without ID)
    test_count += 1
    result = tester.test_endpoint(
        "1. City Weather 7-day Forecast (All)",
        f"{CITY_BASE_URL}/api/cityweather.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 2. City weather forecast (with ID)
    test_count += 1
    result = tester.test_endpoint(
        "1. City Weather 7-day Forecast (ID: 42182)",
        f"{CITY_BASE_URL}/api/cityweather.php",
        params={"id": SAMPLE_IDS["city_id"]}
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 3. City weather with location (without ID)
    test_count += 1
    result = tester.test_endpoint(
        "2. City Weather with Lat/Lon (All)",
        f"{CITY_BASE_URL}/api/cityweather_loc.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 4. City weather with location (with ID)
    test_count += 1
    result = tester.test_endpoint(
        "2. City Weather with Lat/Lon (ID: 42182)",
        f"{CITY_BASE_URL}/api/cityweather_loc.php",
        params={"id": SAMPLE_IDS["city_id"]}
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 5. AWS/ARG Data
    test_count += 1
    result = tester.test_endpoint(
        "10. AWS/ARG Data",
        f"{CITY_BASE_URL}/api/aws_data_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # ========================================================================
    # PART B: MAUSAM API ENDPOINTS
    # ========================================================================
    print(f"\n{Colors.BOLD}🌤️  PART B: Testing Mausam API Endpoints{Colors.RESET}")
    print("-" * 80)
    
    # 3. Current Weather (without ID)
    test_count += 1
    result = tester.test_endpoint(
        "3. Current Weather API (All)",
        f"{MAUSAM_BASE_URL}/api/current_wx_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 3. Current Weather (with ID)
    test_count += 1
    result = tester.test_endpoint(
        "3. Current Weather API (ID: 42182)",
        f"{MAUSAM_BASE_URL}/api/current_wx_api.php",
        params={"id": SAMPLE_IDS["city_id"]}
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 4. District Wise Nowcast (without ID)
    test_count += 1
    result = tester.test_endpoint(
        "4. District Wise Nowcast (All)",
        f"{MAUSAM_BASE_URL}/api/nowcast_district_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 4. District Wise Nowcast (with ID)
    test_count += 1
    result = tester.test_endpoint(
        "4. District Wise Nowcast (ID: 5)",
        f"{MAUSAM_BASE_URL}/api/nowcast_district_api.php",
        params={"id": SAMPLE_IDS["district_id"]}
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 5. District wise Rainfall
    test_count += 1
    result = tester.test_endpoint(
        "5. District wise Rainfall",
        f"{MAUSAM_BASE_URL}/api/districtwise_rainfall_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 6. District wise Warning (without ID)
    test_count += 1
    result = tester.test_endpoint(
        "6. District wise Warning (All)",
        f"{MAUSAM_BASE_URL}/api/warnings_district_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 6. District wise Warning (with ID)
    test_count += 1
    result = tester.test_endpoint(
        "6. District wise Warning (ID: 1)",
        f"{MAUSAM_BASE_URL}/api/warnings_district_api.php",
        params={"id": SAMPLE_IDS["warning_id"]}
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 7. Station Wise Nowcast (without ID)
    test_count += 1
    result = tester.test_endpoint(
        "7. Station Wise Nowcast (All)",
        f"{MAUSAM_BASE_URL}/api/nowcastapi.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 7. Station Wise Nowcast (with ID)
    test_count += 1
    result = tester.test_endpoint(
        "7. Station Wise Nowcast (Jaipur AP)",
        f"{MAUSAM_BASE_URL}/api/nowcastapi.php",
        params={"id": SAMPLE_IDS["station_name"]}
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 8. State wise Rainfall
    test_count += 1
    result = tester.test_endpoint(
        "8. State wise Rainfall",
        f"{MAUSAM_BASE_URL}/api/statewise_rainfall_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 9. RSS Feeds
    test_count += 1
    result = tester.test_endpoint(
        "9. RSS Feeds",
        f"{MAUSAM_BASE_URL}/imd_latest/contents/dist_nowcast_rss.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 11. River Basin QPF
    test_count += 1
    result = tester.test_endpoint(
        "11. River Basin QPF",
        f"{MAUSAM_BASE_URL}/api/basin_qpf_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 12. Port Warning
    test_count += 1
    result = tester.test_endpoint(
        "12. Port Warning",
        f"{MAUSAM_BASE_URL}/api/port_wx_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 13. Sea Area Bulletin
    test_count += 1
    result = tester.test_endpoint(
        "13. Sea Area Bulletin",
        f"{MAUSAM_BASE_URL}/api/seaarea_bulletin_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 14. Coastal Area Bulletin
    test_count += 1
    result = tester.test_endpoint(
        "14. Coastal Area Bulletin",
        f"{MAUSAM_BASE_URL}/api/coastal_bulletin_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # 15. Subdivisional APIs
    test_count += 1
    result = tester.test_endpoint(
        "15a. 5-day Subdivisional Rainfall",
        f"{MAUSAM_BASE_URL}/api/api_5d_subdivisional_rf.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    test_count += 1
    result = tester.test_endpoint(
        "15b. 5-day Statewise Districts Rainfall",
        f"{MAUSAM_BASE_URL}/api/api_5d_statewisedistricts_rf_forecast.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    test_count += 1
    result = tester.test_endpoint(
        "15c. Subdivision wise Warning",
        f"{MAUSAM_BASE_URL}/api/api_subDivisionWiseWarning.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    test_count += 1
    result = tester.test_endpoint(
        "15d. Subdivision wise Rainfall",
        f"{MAUSAM_BASE_URL}/api/subdivisionwise_rainfall_api.php"
    )
    tester.print_progress(test_count, total_tests, result["name"], result["status"])
    
    # ========================================================================
    # GENERATE REPORTS
    # ========================================================================
    print("\n" + "="*80)
    print(f"{Colors.BOLD}Generating Reports...{Colors.RESET}")
    print("="*80)
    
    tester.print_summary()
    tester.print_results_table()
    tester.save_json_report("imd_api_test_report.json")
    tester.save_html_report("imd_api_test_report.html")
    
    print(f"\n{Colors.GREEN}✅ Testing complete!{Colors.RESET}")
    
    # Return exit code based on test results
    return 0 if tester.failed_tests == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
