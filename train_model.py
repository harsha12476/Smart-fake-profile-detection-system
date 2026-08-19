import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

def create_sample_dataset():
    np.random.seed(42)
    n_samples = 1000
    
    usernames = [f'user_{i}' for i in range(n_samples)]
    followers = np.concatenate([
        np.random.randint(0, 100, size=int(n_samples*0.6)),
        np.random.randint(100, 10000, size=int(n_samples*0.4))
    ])
    following = np.concatenate([
        np.random.randint(500, 2000, size=int(n_samples*0.6)),
        np.random.randint(0, 500, size=int(n_samples*0.4))
    ])
    posts = np.concatenate([
        np.random.randint(0, 50, size=int(n_samples*0.6)),
        np.random.randint(50, 1000, size=int(n_samples*0.4))
    ])
    bio_length = np.concatenate([
        np.random.randint(0, 20, size=int(n_samples*0.6)),
        np.random.randint(20, 200, size=int(n_samples*0.4))
    ])
    has_profile_picture = np.concatenate([
        np.random.choice([0, 1], size=int(n_samples*0.6), p=[0.7, 0.3]),
        np.random.choice([0, 1], size=int(n_samples*0.4), p=[0.1, 0.9])
    ])
    account_age_days = np.concatenate([
        np.random.randint(1, 100, size=int(n_samples*0.6)),
        np.random.randint(100, 1500, size=int(n_samples*0.4))
    ])
    
    fake = np.concatenate([np.ones(int(n_samples*0.6)), np.zeros(int(n_samples*0.4))])
    
    indices = np.random.permutation(n_samples)
    
    data = {
        'username': [usernames[i] for i in indices],
        'followers': followers[indices],
        'following': following[indices],
        'posts': posts[indices],
        'bio_length': bio_length[indices],
        'has_profile_picture': has_profile_picture[indices],
        'account_age_days': account_age_days[indices],
        'fake': fake[indices]
    }
    
    df = pd.DataFrame(data)
    os.makedirs('dataset', exist_ok=True)
    df.to_csv('dataset/social_media_profiles.csv', index=False)
    print("Sample dataset created successfully!")
    return df

def train_model():
    print("Loading dataset...")
    if not os.path.exists('dataset/social_media_profiles.csv'):
        df = create_sample_dataset()
    else:
        df = pd.read_csv('dataset/social_media_profiles.csv')
    
    X = df[['followers', 'following', 'posts', 'bio_length', 'has_profile_picture', 'account_age_days']]
    y = df['fake']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    print("\nModel Performance:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    joblib.dump(model, 'model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    print("\nModel and scaler saved successfully!")

if __name__ == "__main__":
    train_model()
