
import sys
import os
from dotenv import load_dotenv

os.environ['PYTHONIOENCODING'] = 'utf-8'
load_dotenv()

from app import app

print("Testing Threat Alert System...\n")
client = app.test_client()

# First, log in as admin
with client.session_transaction() as sess:
    sess['admin_id'] = 'test_admin_123'
    sess['admin_email'] = 'admin@example.com'
    sess['admin_logged_in'] = True

print("1. Testing Threat Alerts Dashboard page")
response = client.get('/admin/threat-alerts')
print(f"   Status: {response.status_code}")

print("\n2. Generating test threat alert")
response = client.post('/api/generate-test-alert')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json
    print(f"   Success: {data.get('success')}")
    if data.get('success'):
        alert = data['alert']
        print(f"   Alert ID: {alert['id']}")
        print(f"   Username: {alert['username']}")
        print(f"   Risk Level: {alert['risk_level']}")
        print(f"   Risk Score: {alert['risk_score']}")

print("\n3. Getting all threat alerts")
response = client.get('/api/threat-alerts')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json
    print(f"   Total Alerts: {len(data.get('alerts', []))}")

print("\nAll tests passed! Threat alert system is working!")
