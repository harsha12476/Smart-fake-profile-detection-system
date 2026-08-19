
import os
from dotenv import load_dotenv
from app import app

def test_admin_routes():
    load_dotenv()
    client = app.test_client()
    
    # Log in as admin
    with client.session_transaction() as sess:
        sess['admin_id'] = 'test-admin-123'
        sess['admin_email'] = 'admin@example.com'
        sess['admin_logged_in'] = True

    routes = [
        ('admin_dashboard', '/admin/dashboard'),
        ('admin_users', '/admin/users'),
        ('admin_predictions', '/admin/predictions'),
        ('admin_feedback', '/admin/feedback'),
        ('admin_behavior', '/admin/behavior'),
        ('admin_admins', '/admin/admins'),
        ('admin_chat_logs', '/admin/chat-logs'),
        ('admin_network_analysis', '/admin/network-analysis'),
        ('admin_behavioral_analytics', '/admin/behavioral-analytics'),
        ('admin_social_graph_analytics', '/admin/social-graph-analytics'),
        ('admin_growth_analytics', '/admin/growth-analytics'),
        ('admin_geolocation_dashboard', '/admin/geolocation-dashboard'),
        ('admin_threat_alerts', '/admin/threat-alerts'),
    ]

    print("Testing all admin routes...")
    print("=" * 60)
    
    all_passed = True
    for route_name, url in routes:
        try:
            response = client.get(url, follow_redirects=False)
            status = response.status_code
            
            if status == 200:
                print(f"OK {url:40} [200 OK]")
            else:
                print(f"ERROR {url:40} [Status: {status}]")
                all_passed = False
        except Exception as e:
            print(f"ERROR {url:40} [Error: {str(e)}]")
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("\nAll admin routes are working perfectly!")
    else:
        print("\nSome admin routes have errors!")

if __name__ == '__main__':
    test_admin_routes()
