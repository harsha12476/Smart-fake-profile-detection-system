
from app import app, mongo

with app.test_client() as client:
    print("=== Testing Login ===")
    # Test login page GET
    res = client.get('/login')
    print(f"GET /login: {res.status_code}")
    
    # Test logging in with test credentials
    res = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'test123'
    }, follow_redirects=True)
    
    print(f"POST /login response: {res.status_code}")
    if b'Dashboard' in res.data:
        print("SUCCESS: Logged in, redirected to dashboard!")
    else:
        print("FAILED: Dashboard not reached!")

print("\n=== Done ===")
