
import sys
import os
from dotenv import load_dotenv

os.environ['PYTHONIOENCODING'] = 'utf-8'
load_dotenv()

from app import app

print("Testing Geolocation Risk Analysis...\n")

client = app.test_client()

# Test user page
with client.session_transaction() as sess:
    sess['user_id'] = 'test_user_123'
    sess['user_name'] = 'Test User'
    sess['logged_in'] = True

print("1. Testing /geolocation-risk page")
response = client.get('/geolocation-risk')
print(f"   Status: {response.status_code}")

print("\n2. Testing /api/geolocation-analysis")
response = client.get('/api/geolocation-analysis')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json
    print(f"   Success: {data.get('success')}")
    print(f"   Risk score: {data.get('analysis', {}).get('risk_score')}")

print("\n3. Testing admin geolocation dashboard")
with client.session_transaction() as sess:
    sess['admin_id'] = 'test_admin_123'
    sess['admin_email'] = 'admin@example.com'
    sess['admin_logged_in'] = True

response = client.get('/admin/geolocation-dashboard')
print(f"   Status: {response.status_code}")

print("\nAll tests complete!")
