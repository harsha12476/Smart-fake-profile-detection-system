
import os
from dotenv import load_dotenv
from app import app, mongo, bcrypt

def create_admin():
    db = mongo.db
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    existing_admin = db.admins.find_one({'email': admin_email})
    if not existing_admin:
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        from datetime import datetime
        db.admins.insert_one({
            'email': admin_email,
            'password': hashed_password,
            'created_at': datetime.now()
        })
        print("Admin account created successfully!")
        print(f"  Email: {admin_email}")
        print(f"  Password: {admin_password}")
    else:
        print("Admin account already exists!")
        print(f"  Email: {admin_email}")

if __name__ == '__main__':
    load_dotenv()
    with app.app_context():
        create_admin()
