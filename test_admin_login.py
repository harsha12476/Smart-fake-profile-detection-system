
import os
from dotenv import load_dotenv
from app import app, mongo, bcrypt

def test_admin_login():
    load_dotenv()
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    print(f"Testing admin login with:")
    print(f"  Email: {admin_email}")
    print(f"  Password: {admin_password}")
    
    with app.app_context():
        admin = mongo.db.admins.find_one({'email': admin_email})
        if admin:
            print("\nFound admin account in DB")
            print(f"  Email: {admin['email']}")
            
            if bcrypt.checkpw(admin_password.encode('utf-8'), admin['password']):
                print("\nPassword matches! Login works perfectly!")
            else:
                print("\nPassword does NOT match!")
        else:
            print("\nAdmin account NOT found in DB!")

if __name__ == '__main__':
    test_admin_login()
