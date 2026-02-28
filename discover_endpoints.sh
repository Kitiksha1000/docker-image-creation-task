#!/bin/bash

# Script to discover available API endpoints

echo "=== Discovering City API Endpoints ==="
echo ""

CITY_BASE="http://100.100.108.101:18080/city"
MAUSAM_BASE="http://100.100.108.101:18080/mausam"

# Known endpoints from JavaScript analysis
echo "Testing known City endpoints from JavaScript:"
for endpoint in \
    "/api/fetchCity_static.php" \
    "/api/fetchMapImage.php" \
    "/api/search.php" \
    "/api/cityweather.php" \
    "/api/cityweather_loc.php" \
    "/api/aws_data_api.php"
do
    echo -n "  $endpoint ... "
    status=$(curl -s -o /dev/null -w "%{http_code}" "${CITY_BASE}${endpoint}")
    if [ "$status" = "200" ]; then
        echo "✓ FOUND (200)"
    elif [ "$status" = "404" ]; then
        echo "✗ NOT FOUND (404)"
    else
        echo "? STATUS: $status"
    fi
done

echo ""
echo "=== Discovering Mausam API Endpoints ==="
echo ""

# Test common API endpoints
echo "Testing common Mausam endpoints:"
for endpoint in \
    "/api/current_wx_api.php" \
    "/api/nowcast_district_api.php" \
    "/api/nowcastapi.php" \
    "/api/districtwise_rainfall_api.php" \
    "/api/statewise_rainfall_api.php" \
    "/api/warnings_district_api.php" \
    "/api/basin_qpf_api.php" \
    "/api/port_wx_api.php" \
    "/api/seaarea_bulletin_api.php" \
    "/api/coastal_bulletin_api.php" \
    "/api/aws_arg_data_api.php" \
    "/api_5d_subdivisional_rf.php" \
    "/api_subDivisionWiseWarning.php" \
    "/responsive/curWxMap/fetchWxMapGIS.php" \
    "/responsive/coldwave_guidance.php"
do
    echo -n "  $endpoint ... "
    status=$(curl -s -o /dev/null -w "%{http_code}" "${MAUSAM_BASE}${endpoint}")
    if [ "$status" = "200" ]; then
        echo "✓ FOUND (200)"
    elif [ "$status" = "404" ]; then
        echo "✗ NOT FOUND (404)"
    else
        echo "? STATUS: $status"
    fi
done

echo ""
echo "Done!"
