
import os
from dotenv import load_dotenv
from app import app

def test_routes():
    load_dotenv()
    client = app.test_client()
    
    print("Testing all public routes...")
    routes = [
        "/",
        "/about",
        "/how-it-works",
        "/contact",
        "/login",
        "/register"
    ]
    
    all_passed = True
    for route in routes:
        try:
            res = client.get(route, follow_redirects=False)
            print(f"  {route:40} [{res.status_code}]")
            if res.status_code not in (200,302):
                all_passed = False
        except Exception as e:
            print(f"  ERROR {route} → {str(e)}")
            all_passed = False
    
    print("\nTesting with logged-in user...")
    with client.session_transaction() as sess:
        sess['user_id'] = "TEST-USER-123"
        sess['user_name'] = "Test User"
        sess['logged_in'] = True
        
    user_routes = [
        "/dashboard",
        "/detect",
        "/history",
        "/behavior-analysis",
        "/network-analysis",
        "/social-graph",
        "/growth-prediction",
        "/growth-history",
        "/threat-heatmap",
        "/geolocation-risk",
        "/identity-verification",
        "/profile/edit",
        "/edit-profile"
    ]
    
    for route in user_routes:
        try:
            res = client.get(route, follow_redirects=False)
            print(f"  {route:40} [{res.status_code}]")
            if res.status_code not in (200,302):
                all_passed = False
        except Exception as e:
            print(f"  ERROR {route} → {str(e)}")
            all_passed = False
    
    print("\nTesting with admin login...")
    with client.session_transaction() as sess:
        sess['admin_id'] = "ADMIN-123"
        sess['admin_email'] = "admin@example.com"
        sess['admin_logged_in'] = True
        
    admin_routes = [
        "/admin/dashboard",
        "/admin/users",
        "/admin/predictions",
        "/admin/feedback",
        "/admin/behavior",
        "/admin/admins",
        "/admin/chat-logs",
        "/admin/network-analysis",
        "/admin/behavioral-analytics",
        "/admin/social-graph-analytics",
        "/admin/growth-analytics",
        "/admin/threat-intelligence",
        "/admin/geolocation-dashboard",
        "/admin/threat-alerts",
        "/admin/identity-dashboard"
    ]
    
    for route in admin_routes:
        try:
            res = client.get(route, follow_redirects=False)
            print(f"  {route:40} [{res.status_code}]")
            if res.status_code not in (200,302):
                all_passed = False
        except Exception as e:
            print(f"  ERROR {route} → {str(e)}")
            all_passed = False
    
    print(f"\nOverall status: {'OK All tests passed' if all_passed else 'ERROR Some tests failed'}")

if __name__ == "__main__":
    test_routes()
