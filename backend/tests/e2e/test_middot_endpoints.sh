#!/bin/bash

# Test script for middot endpoints
# Make sure your backend is running with: docker compose up

# Set UTF-8 locale explicitly
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Load environment variables from .env file
if [ -f "../../../.env" ]; then
    export $(grep -v '^#' ../../../.env | xargs)
else
    echo "❌ .env file not found at ../../../.env"
    echo "Please make sure you're running this from backend/tests/e2e/ and that .env exists in project root"
    exit 1
fi

BASE_URL="http://localhost:8000/api/v1"
ADMIN_EMAIL="${FIRST_SUPERUSER}"
ADMIN_PASSWORD="${FIRST_SUPERUSER_PASSWORD}"

# Validate required environment variables
if [ -z "$ADMIN_EMAIL" ] || [ -z "$ADMIN_PASSWORD" ]; then
    echo "❌ Missing required environment variables:"
    echo "FIRST_SUPERUSER: ${ADMIN_EMAIL:-'NOT SET'}"
    echo "FIRST_SUPERUSER_PASSWORD: ${ADMIN_PASSWORD:+'SET':NOT SET}"
    exit 1
fi

echo "=== Testing Middot Endpoints ==="
echo

# Step 1: Get access token
echo "1. Getting access token..."
TOKEN_RESPONSE=$(curl -s -X POST "${BASE_URL}/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=${ADMIN_EMAIL}&password=${ADMIN_PASSWORD}")

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Failed to get access token. Response:"
  echo "$TOKEN_RESPONSE"
  echo "Make sure your backend is running and credentials are correct."
  exit 1
fi

echo "✅ Got access token: ${TOKEN:0:20}..."
echo

# Step 2: Test GET /middot/ (should be empty initially)
echo "2. Testing GET /middot/ (initial list)..."
curl -s -X GET "${BASE_URL}/middot/" \
  -H "Authorization: Bearer $TOKEN" | jq '.'
echo

# Step 3: Create a test middah using printf to ensure proper UTF-8 encoding
echo "3. Creating test middah (chesed)..."

# Create JSON payload using printf to preserve UTF-8 encoding
JSON_PAYLOAD=$(printf '{
  "name_transliterated": "chesed",
  "name_hebrew": "חסד",
  "name_english": "Kindness"
}')

CREATE_RESPONSE=$(curl -s -X POST "${BASE_URL}/middot/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data-raw "$JSON_PAYLOAD")

echo "$CREATE_RESPONSE" | jq '.'
echo

# Step 3.5: Debug encoding - check what was actually stored
echo "3.5. Debug: Checking what was actually stored..."
STORED_RESPONSE=$(curl -s -X GET "${BASE_URL}/middot/chesed" \
  -H "Authorization: Bearer $TOKEN")

echo "Raw response: $STORED_RESPONSE"
echo "Pretty JSON:"
echo "$STORED_RESPONSE" | jq '.'
echo "Hebrew field: $(echo "$STORED_RESPONSE" | jq -r '.name_hebrew')"
echo

# Step 4: Create another test middah using --data-raw
echo "4. Creating another test middah (gevurah)..."

JSON_PAYLOAD2=$(printf '{
  "name_transliterated": "gevurah",
  "name_hebrew": "גבורה",
  "name_english": "Strength"
}')

curl -s -X POST "${BASE_URL}/middot/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data-raw "$JSON_PAYLOAD2" | jq '.'
echo

# Step 5: Test GET /middot/ (should now have items)
echo "5. Testing GET /middot/ (should show created middot)..."
curl -s -X GET "${BASE_URL}/middot/" \
  -H "Authorization: Bearer $TOKEN" | jq '.'
echo

# Step 6: Test GET /middot/{name} for specific middah
echo "6. Testing GET /middot/chesed (specific middah)..."
curl -s -X GET "${BASE_URL}/middot/chesed" \
  -H "Authorization: Bearer $TOKEN" | jq '.'
echo

# Step 7: Test error case - non-existent middah
echo "7. Testing GET /middot/nonexistent (should return 404)..."
curl -s -X GET "${BASE_URL}/middot/nonexistent" \
  -H "Authorization: Bearer $TOKEN" | jq '.'
echo

# Step 8: Test DELETE endpoint
echo "8. Testing DELETE /middot/gevurah..."
curl -s -X DELETE "${BASE_URL}/middot/gevurah" \
  -H "Authorization: Bearer $TOKEN" -w "HTTP Status: %{http_code}\n"
echo

# Step 9: Verify deletion worked
echo "9. Testing GET /middot/ after deletion..."
curl -s -X GET "${BASE_URL}/middot/" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo
echo "=== Testing Complete ==="