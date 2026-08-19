
from app import app, mongo
import bcrypt

with app.app_context():
    print("Checking for existing test user...")
    test_email = 'test@example.com'
    existing_user = mongo.db.users.find_one({'email': test_email})
    
    if existing_user:
        print("Test user already exists!")
        print(f"Email: {test_email}")
        print(f"Password: test123")
    else:
        print("Creating new test user...")
        hashed_pw = bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt())
        mongo.db.users.insert_one({
            'name': 'Test User',
            'email': test_email,
            'password': hashed_pw,
            'status': 'Active',
            'created_at': None
        })
        print("\n✅ Test user created successfully!")
        print("Login credentials:")
        print(f"Email: {test_email}")
        print(f"Password: test123")
