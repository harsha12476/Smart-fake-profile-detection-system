
import os
from dotenv import load_dotenv
from app import app, mongo, bcrypt
from datetime import datetime

def test_admin_login_flow():
    load_dotenv()
    client = app.test_client()
    
    print("Testing admin login flow...")
    print("=" * 60)
    
    # First, make sure admin account exists
    admin_email = 'admin@example.com'
    admin_password = 'admin123'
    with app.app_context():
        existing_admin = mongo.db.admins.find_one({'email': admin_email})
        if not existing_admin:
            print("Creating admin account...")
            hashed_pw = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
            mongo.db.admins.insert_one({
                'email': admin_email,
                'password': hashed_pw,
                'created_at': datetime.now()
            })
        print(f"Admin account exists: {existing_admin is not None}")
    
    # Test POST login request
    login_response = client.post('/admin/login', data={
        'email': admin_email,
        'password': admin_password
    }, follow_redirects=False)
    print(f"\nPOST /admin/login status: {login_response.status_code}")
    
    # Check if logged in and get dashboard
    print("\nAccessing /admin/dashboard...")
    dashboard_response = client.get('/admin/dashboard', follow_redirects=False)
    print(f"\nGET /admin/dashboard status: {dashboard_response.status_code}")
    if dashboard_response.status_code != 200:
        print("\nDashboard response data:")
        print(dashboard_response.data.decode('utf-8'))
        
    print("\n" + "=" * 60)
    print("Test complete!")

if __name__ == '__main__':
    test_admin_login_flow()
