from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g
from flask_pymongo import PyMongo
from flask_mail import Mail
from bson.objectid import ObjectId
import bcrypt
import joblib
import numpy as np
from datetime import datetime, timedelta
import os
import logging
from dotenv import load_dotenv
from notifications import send_fake_profile_alert
from behavioral_analysis import analyze_behavior, combine_with_profile_prediction, analyzer as behavioral_analyzer
from chatbot import chatbot
from network_analysis import analyzer

from social_graph_intelligence import social_graph_engine
from growth_prediction_engine import growth_engine
from threat_analytics import engine as threat_engine
from geolocation_risk import engine as geolocation_engine
from threat_alert_system import alert_system
from blockchain_identity import identity_system
from fake_follower_detection import engine as fake_follower_engine
from cybercrime_intelligence import engine as cybercrime_engine

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

TRANSLATIONS = {
    'en': {
        'Home': 'Home',
        'About': 'About',
        'Features': 'Features',
        'How It Works': 'How It Works',
        'Contact': 'Contact',
        'Login': 'Login',
        'Register': 'Register',
        'Dashboard': 'Dashboard',
        'Detect': 'Detect',
        'History': 'History',
        'Behavior Analysis': 'Behavior Analysis',
        'Network Analysis': 'Network Analysis',
        'Chatbot': 'Chatbot',
        'Admin Dashboard': 'Admin Dashboard',
        'Logout': 'Logout',
        'FPDS': 'FPDS',
        'Smart Fake Profile Detection System': 'Smart Fake Profile Detection System',
        'Copyright': '&copy; 2026 Smart Fake Profile Detection System. All rights reserved.',
        'Language': 'Language'
    },
    'kn': {
        'Home': 'ಮುಖಪುಟ',
        'About': 'ಬಗ್ಗೆ',
        'Features': 'ವೈಶಿಷ್ಟ್ಯಗಳು',
        'How It Works': 'ಇದು ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ',
        'Contact': 'ಸಂಪರ್ಕಿಸಿ',
        'Login': 'ಲಾಗಿನ್',
        'Register': 'ನೋಂದಾಯಿಸಿ',
        'Dashboard': 'ಡ್ಯಾಶ್ಬೋರ್ಡ್',
        'Detect': 'ಪತ್ತೆ ಮಾಡಿ',
        'History': 'ಇತಿಹಾಸ',
        'Behavior Analysis': 'ನಡವಿಕೆ ವಿಶ್ಲೇಷಣೆ',
        'Network Analysis': 'ನೆಟ್ವರ್ಕ್ ವಿಶ್ಲೇಷಣೆ',
        'Chatbot': 'ಚಾಟ್ಬಾಟ್',
        'Admin Dashboard': 'ಅಡ್ಮಿನ್ ಡ್ಯಾಶ್ಬೋರ್ಡ್',
        'Logout': 'ಲಾಗ್ಔಟ್',
        'FPDS': 'FPDS',
        'Smart Fake Profile Detection System': 'ಸ್ಮಾರ್ಟ್ ಫೇಕ್ ಪ್ರೊಫೈಲ್ ಪತ್ತೆ ಮಾಡುವ ವ್ಯವಸ್ಥೆ',
        'Copyright': '&copy; 2026 ಸ್ಮಾರ್ಟ್ ಫೇಕ್ ಪ್ರೊಫೈಲ್ ಪತ್ತೆ ಮಾಡುವ ವ್ಯವಸ್ಥೆ. ಎಲ್ಲಾ ಹಕ್ಕುಗಳು ರಕ್ಷಿಸಲ್ಪಟ್ಟಿವೆ.',
        'Language': 'ಭಾಷೆ'
    },
    'hi': {
        'Home': 'होम',
        'About': 'हमारे बारे में',
        'Features': 'विशेषताएँ',
        'How It Works': 'यह कैसे काम करता है',
        'Contact': 'संपर्क करें',
        'Login': 'लॉगिन',
        'Register': 'रजिस्टर करें',
        'Dashboard': 'डैशबोर्ड',
        'Detect': 'पता लगाएँ',
        'History': 'इतिहास',
        'Behavior Analysis': 'व्यवहार विश्लेषण',
        'Network Analysis': 'नेटवर्क विश्लेषण',
        'Chatbot': 'चैटबॉट',
        'Admin Dashboard': 'एडमिन डैಶबोर्ड',
        'Logout': 'लॉगआउट',
        'FPDS': 'FPDS',
        'Smart Fake Profile Detection System': 'स्मार्ट फेक प्रोफाइल डिटेक्शन सिस्टम',
        'Copyright': '&copy; 2026 स्मಾರ्ट फेक ಪ್ರೊಫೈಲ್ ಡಿಟೆಕ್ಷನ್ ಸಿಸ್ಟಮ್. सर್ವಾಧಿಕಾರ ಸುರಕ್ಷಿತ.',
        'Language': 'ಭಾಷೆ'
    },
    'ta': {
        'Home': 'முகப்பு',
        'About': 'பற்றி',
        'Features': 'அம்சங்கள்',
        'How It Works': 'இது எப்படி செயல்படுகிறது',
        'Contact': 'தொடர்பு',
        'Login': 'உள்நுழைக',
        'Register': 'பதிவு செய்யவும்',
        'Dashboard': 'டாஷ்போர்டு',
        'Detect': 'கண்டறியவும்',
        'History': 'வரலாறு',
        'Behavior Analysis': 'நடத்தை பகுப்பாய்வு',
        'Network Analysis': 'வலைய பகுப்பாய்வு',
        'Chatbot': 'அரட்டை போட்',
        'Admin Dashboard': 'நிர்வாகி டாஷ்போர்டு',
        'Logout': 'வெளியேறு',
        'FPDS': 'FPDS',
        'Smart Fake Profile Detection System': 'ஸ்மார்ட் போலி சுயவிவர கண்டறிதல் அமைப்பு',
        'Copyright': '&copy; 2026 ஸ்மார்ட் போலி சுயவிவர கண்டறிதல் அமைப்பு. அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.',
        'Language': 'மொழி'
    },
    'te': {
        'Home': 'హోమ్',
        'About': 'గురించి',
        'Features': 'లక్షణాలు',
        'How It Works': 'ఇది ఎలా పనిచేస్తుంది',
        'Contact': 'సంప్రదించండి',
        'Login': 'లాగిన్',
        'Register': 'నమోదించండి',
        'Dashboard': 'డాష్బోర్డ్',
        'Detect': 'గుర్తించండి',
        'History': 'చరిత్ర',
        'Behavior Analysis': 'ప్రవర్తన విశ్లేషణ',
        'Network Analysis': 'నెట్వర్క్ విశ్లేషణ',
        'Chatbot': 'చాట్బాట్',
        'Admin Dashboard': 'అడ్మిన్ డాష్బోర్డ్',
        'Logout': 'లాగ్ఔట్',
        'FPDS': 'FPDS',
        'Smart Fake Profile Detection System': 'స్మార్ట్ ఫేక్ ప్రొఫైల్ డిటెక్షన్ సిస్టమ్',
        'Copyright': '&copy; 2026 స్మార్ట్ ఫేక్ ప్రొఫైల్ డిటెక్షన్ సిస్టమ్. అన్ని హక్కులు రిజర్వ్ చేయబడ్డాయి.',
        'Language': 'భాష'
    }
}

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'kn': 'ಕನ್ನಡ',
    'hi': 'हिन्दी',
    'ta': 'தமிழ்',
    'te': 'తెలుగు'
}

app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/fake_profile_detection')
mongo = PyMongo(app)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
mail = Mail(app)

model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

def create_admin():
    db = mongo.db
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    existing_admin = db.admins.find_one({'email': admin_email})
    if not existing_admin:
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        db.admins.insert_one({
            'email': admin_email,
            'password': hashed_password,
            'created_at': datetime.now()
        })
        print(f"Admin account created: {admin_email}")

with app.app_context():
    create_admin()

def get_locale():
    if 'lang' in session:
        if session['lang'] in SUPPORTED_LANGUAGES:
            return session['lang']
    return request.accept_languages.best_match(SUPPORTED_LANGUAGES.keys()) or 'en'

def t(key):
    lang = get_locale()
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    if key in TRANSLATIONS['en']:
        return TRANSLATIONS['en'][key]
    return key

def get_last_scan(user_id):
    if not user_id:
        return None
    return mongo.db.profile_scans.find_one({'user_id': user_id}, sort=[('created_at', -1)])

@app.before_request
def before_request():
    g.supported_languages = SUPPORTED_LANGUAGES
    g.current_lang = get_locale()
    g.t = t

@app.route('/set-language/<lang>')
def set_language(lang):
    if lang in SUPPORTED_LANGUAGES:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

# ==================== FRONTEND ROUTES ====================

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        existing_user = users.find_one({
            '$or': [{'email': email}, {'name': username}]
        })
        
        if existing_user:
            flash('User already exists!', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password,
            'status': 'Active',
            'created_at': datetime.now()
        })
        flash('Registration successful! Please log in to continue.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        user = users.find_one({'email': request.form['email']})
        
        if user and bcrypt.checkpw(request.form['password'].encode('utf-8'), user['password']):
            if user.get('status') == 'Blocked':
                flash('Your account has been blocked!', 'danger')
                return redirect(url_for('login'))
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email/password combination!', 'danger')
    
    return render_template('login.html')

@app.route('/edit_profile')
def edit_profile_old():
    return redirect(url_for('edit_profile'))

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    try:
        user_id = ObjectId(session['user_id'])
    except Exception as e:
        flash('Invalid session, please login again!', 'danger')
        return redirect(url_for('login'))
    
    user = mongo.db.users.find_one({'_id': user_id})
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        update_data = {'name': request.form['name']}
        
        if request.form['password']:
            update_data['password'] = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        
        mongo.db.users.update_one({'_id': user_id}, {'$set': update_data})
        
        session['user_name'] = request.form['name']
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('user/profile.html', user=user)

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    predictions = mongo.db.predictions.find({'user_id': user_id}).sort('created_at', -1).limit(5)
    total_predictions = mongo.db.predictions.count_documents({'user_id': user_id})
    fake_predictions = mongo.db.predictions.count_documents({'user_id': user_id, 'result': 'Fake'})
    real_predictions = mongo.db.predictions.count_documents({'user_id': user_id, 'result': 'Real'})
    last_scan = get_last_scan(user_id)
    
    return render_template('user/dashboard.html', 
                         predictions=predictions, 
                         total=total_predictions,
                         fake=fake_predictions,
                         real=real_predictions,
                         scan=last_scan)

@app.route('/detect')
def detect():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    return render_template('user/detect.html')


@app.route('/scan-profile', methods=['POST'])
def scan_profile():
    if 'logged_in' not in session:
        return jsonify({'success': False, 'error': 'Please login first'}), 401
    
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        username = data.get('username', '')
        followers = int(data.get('followers', 0))
        following = int(data.get('following', 0))
        posts = int(data.get('posts', 0))
        bio_length = int(data.get('bio_length', len(data.get('bio', ''))))
        has_profile_picture = 1 if data.get('has_profile_picture') else 0
        account_age_days = int(data.get('account_age_days', 1))
        avg_likes = int(data.get('avg_likes', 0))
        avg_comments = int(data.get('avg_comments', 0))
        
        features = np.array([[followers, following, posts, bio_length, has_profile_picture, account_age_days]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)
        probability = model.predict_proba(features_scaled)
        pred_class = int(prediction[0])
        profile_result = 'Fake' if pred_class == 1 else 'Real'
        profile_confidence = round(probability[0][pred_class] * 100, 2)
        
        reasons = []
        if followers < 100:
            reasons.append("Low follower count")
        if following > 2000:
            reasons.append("High following count")
        if posts < 5:
            reasons.append("Low post count")
        if bio_length < 20:
            reasons.append("Short bio")
        if account_age_days < 30:
            reasons.append("New account")
        if not has_profile_picture:
            reasons.append("No profile picture")
        
        if profile_result == 'Real':
            risk_level = 'Low'
        elif profile_confidence >= 70:
            risk_level = 'High'
        else:
            risk_level = 'Medium'
        
        growth_result = growth_engine.predict_growth(
            current_followers=followers,
            account_age_days=account_age_days,
            avg_posts_per_week=posts / (account_age_days / 7) if account_age_days > 0 else 0
        )
        
        threat_result = threat_engine.analyze_profile(
            username=username,
            bio='',
            captions=[],
            links=[]
        )
        
        geolocation_result = geolocation_engine.analyze_locations(
            current_location='',
            previous_locations=[]
        )
        
        fake_follower_result = fake_follower_engine.analyze_profile(
            username=username,
            followers=followers,
            following=following,
            avg_likes=avg_likes,
            avg_comments=avg_comments,
            account_age_days=account_age_days
        )
        
        cybercrime_result = cybercrime_engine.analyze_profile(
            username=username,
            bio='',
            captions=[],
            links=[]
        )
        
        verification_result = identity_system.verify_identity(
            username=username,
            bio='',
            has_profile_picture=has_profile_picture
        )
        
        engagement_rate = 0.0
        if followers > 0:
            engagement_rate = round(((avg_likes + avg_comments) / followers) * 100, 2)
        
        follower_ratio = 0.0
        if following > 0:
            follower_ratio = round(followers / following, 2)
        
        scan_data = {
            'user_id': session.get('user_id'),
            'user_name': session.get('user_name'),
            'username': username,
            'profile_data': {
                'followers': followers,
                'following': following,
                'posts': posts,
                'bio_length': bio_length,
                'account_age_days': account_age_days,
                'avg_likes': avg_likes,
                'avg_comments': avg_comments,
                'has_profile_picture': has_profile_picture
            },
            'profile_prediction': {
                'result': profile_result,
                'confidence': profile_confidence,
                'risk_level': risk_level,
                'reasons': reasons
            },
            'growth_prediction': growth_result,
            'threat_analysis': threat_result,
            'geolocation_risk': geolocation_result,
            'fake_follower': fake_follower_result,
            'cybercrime_intel': cybercrime_result,
            'blockchain_verification': verification_result,
            'created_at': datetime.now()
        }
        
        scan_id = mongo.db.profile_scans.insert_one(scan_data).inserted_id
        
        # Save to prediction_history
        prediction_history_data = {
            'user_id': session.get('user_id'),
            'user_name': session.get('user_name'),
            'scan_id': str(scan_id),
            'username': username,
            'profile_url': f"https://instagram.com/{username}",
            'followers': followers,
            'following': following,
            'posts': posts,
            'prediction': profile_result,
            'confidence_score': profile_confidence,
            'risk_score': profile_confidence,
            'threat_level': risk_level,
            'scan_date': datetime.now(),
            'engagement_rate': engagement_rate,
            'follower_ratio': follower_ratio,
            'growth_prediction': growth_result,
            'cybercrime_score': cybercrime_result.get('threat_intelligence_score', 0),
            'fake_follower_score': fake_follower_result.get('purchased_follower_probability', 0),
            'geolocation_risk_score': geolocation_result.get('location_risk_score', 0),
            'blockchain_verification_status': verification_result.get('verification_status', 'Unverified'),
            'full_data': scan_data
        }
        
        mongo.db.prediction_history.insert_one(prediction_history_data)
        
        # Store scan_id in session for easy access
        session['last_scan_id'] = str(scan_id)
        
        flash('Profile analyzed successfully! All modules have been updated.', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        logging.exception(f"Error scanning profile: {str(e)}")
        flash(f'Error scanning profile: {str(e)}', 'danger')
        return redirect(url_for('detect'))

@app.route('/analyze-profile', methods=['POST'])
def analyze_profile():
    if 'logged_in' not in session:
        return jsonify({'success': False, 'error': 'Please login first'}), 401
    
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        username = data.get('username')
        followers = int(data.get('followers', 0))
        following = int(data.get('following', 0))
        posts = int(data.get('posts', 0))
        bio_length = int(data.get('bio_length', 0))
        has_profile_picture = int(data.get('has_profile_picture', 0))
        account_age_days = int(data.get('account_age_days', 1))
        
        features = np.array([[followers, following, posts, bio_length, has_profile_picture, account_age_days]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)
        probability = model.predict_proba(features_scaled)
        
        pred_class = int(prediction[0])
        result = 'Fake' if pred_class == 1 else 'Real'
        confidence = round(probability[0][pred_class] * 100, 2)
        
        # Generate detection reasons
        reasons = []
        if followers < 100:
            reasons.append("Low follower count")
        if following > 2000:
            reasons.append("High following count")
        if posts < 5:
            reasons.append("Low post count")
        if bio_length < 20:
            reasons.append("Short bio")
        if account_age_days < 30:
            reasons.append("New account")
        if not has_profile_picture:
            reasons.append("No profile picture")
        
        if result == 'Real':
            risk_level = 'Low'
        elif confidence >= 70:
            risk_level = 'High'
        else:
            risk_level = 'Medium'
        
        prediction_data = {
            'user_id': session['user_id'],
            'user_name': session['user_name'],
            'username': username,
            'followers': followers,
            'following': following,
            'posts': posts,
            'bio_length': bio_length,
            'has_profile_picture': has_profile_picture,
            'account_age_days': account_age_days,
            'result': result,
            'confidence': confidence,
            'reasons': reasons,
            'risk_level': risk_level,
            'created_at': datetime.now()
        }
        
        mongo.db.predictions.insert_one(prediction_data)
        
        notification_email = os.getenv('NOTIFICATION_EMAIL', 'admin@example.com')
        notification_threshold = int(os.getenv('NOTIFICATION_THRESHOLD', 90))
        send_fake_profile_alert(mail, prediction_data, notification_email, notification_threshold)
        
        # Generate threat alert if high risk
        if result == 'Fake' and confidence >= 70:
            threat_type = "Fake Profiles"
            if confidence >= 90:
                threat_type = "Phishing & Scam Activity"
            
            alert = alert_system.generate_threat_alert(
                username=username,
                risk_score=int(confidence),
                threat_type=threat_type,
                detection_reasons=reasons,
                profile_data=prediction_data
            )
            
            # Send email and SMS (simulated)
            alert_system.send_email_alert(alert, notification_email)
            alert_system.send_sms_alert(alert)
        
        return jsonify({
            'success': True,
            'prediction': {
                'result': result,
                'confidence': confidence,
                'risk_level': risk_level,
                'reasons': reasons
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form['username']
        followers = int(request.form['followers'])
        following = int(request.form['following'])
        posts = int(request.form['posts'])
        bio_length = int(request.form['bio_length'])
        has_profile_picture = int(request.form.get('has_profile_picture', 0))
        account_age_days = int(request.form['account_age_days'])
        
        features = np.array([[followers, following, posts, bio_length, has_profile_picture, account_age_days]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)
        probability = model.predict_proba(features_scaled)
        
        pred_class = int(prediction[0])
        result = 'Fake' if pred_class == 1 else 'Real'
        confidence = round(probability[0][pred_class] * 100, 2)
        
        prediction_data = {
            'user_id': session['user_id'],
            'user_name': session['user_name'],
            'username': username,
            'followers': followers,
            'following': following,
            'posts': posts,
            'bio_length': bio_length,
            'has_profile_picture': has_profile_picture,
            'account_age_days': account_age_days,
            'result': result,
            'confidence': confidence,
            'created_at': datetime.now()
        }
        
        mongo.db.predictions.insert_one(prediction_data)
        
        notification_email = os.getenv('NOTIFICATION_EMAIL', 'admin@example.com')
        notification_threshold = int(os.getenv('NOTIFICATION_THRESHOLD', 90))
        send_fake_profile_alert(mail, prediction_data, notification_email, notification_threshold)
        
        return render_template('result.html', 
                             username=username,
                             result=result,
                             confidence=confidence,
                             data=prediction_data)

@app.route('/history')
def history():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Get query parameters for filtering/sorting
    search = request.args.get('search', '')
    threat_level = request.args.get('threat_level', '')
    prediction_filter = request.args.get('prediction', '')
    sort_order = request.args.get('sort', 'desc')  # 'desc' (newest) or 'asc' (oldest)
    
    # Build query
    query = {'user_id': user_id}
    
    if search:
        query['username'] = {'$regex': search, '$options': 'i'}
    
    if threat_level:
        query['threat_level'] = threat_level
    
    if prediction_filter:
        query['prediction'] = prediction_filter
    
    # Sort
    sort_param = [('scan_date', -1)] if sort_order == 'desc' else [('scan_date', 1)]
    
    predictions = mongo.db.prediction_history.find(query).sort(sort_param)
    
    return render_template('user/history.html', 
                           predictions=predictions, 
                           search=search, 
                           threat_level=threat_level,
                           prediction_filter=prediction_filter,
                           sort_order=sort_order)

@app.route('/prediction-history/view/<id>')
def view_prediction_history(id):
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    prediction_id = ObjectId(id)
    prediction = mongo.db.prediction_history.find_one({'_id': prediction_id, 'user_id': session['user_id']})
    
    if not prediction:
        flash('Prediction not found!', 'danger')
        return redirect(url_for('history'))
    
    return render_template('user/view_report.html', prediction=prediction)

@app.route('/prediction-history/download/<id>')
def download_prediction_history(id):
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    prediction_id = ObjectId(id)
    prediction = mongo.db.prediction_history.find_one({'_id': prediction_id, 'user_id': session['user_id']})
    
    if not prediction:
        flash('Prediction not found!', 'danger')
        return redirect(url_for('history'))
    
    from flask import make_response
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write report data
    writer.writerow(['Scan ID', str(prediction['_id'])])
    writer.writerow(['Username', prediction['username']])
    writer.writerow(['Profile URL', prediction['profile_url']])
    writer.writerow(['Followers', prediction['followers']])
    writer.writerow(['Following', prediction['following']])
    writer.writerow(['Posts', prediction['posts']])
    writer.writerow(['Prediction', prediction['prediction']])
    writer.writerow(['Confidence Score', prediction['confidence_score']])
    writer.writerow(['Risk Score', prediction['risk_score']])
    writer.writerow(['Threat Level', prediction['threat_level']])
    writer.writerow(['Scan Date', prediction['scan_date'].strftime('%Y-%m-%d %H:%M:%S') if prediction.get('scan_date') else 'N/A'])
    writer.writerow(['Engagement Rate', prediction.get('engagement_rate', 'N/A')])
    writer.writerow(['Follower Ratio', prediction.get('follower_ratio', 'N/A')])
    writer.writerow(['Cybercrime Score', prediction.get('cybercrime_score', 'N/A')])
    writer.writerow(['Fake Follower Score', prediction.get('fake_follower_score', 'N/A')])
    writer.writerow(['Geolocation Risk Score', prediction.get('geolocation_risk_score', 'N/A')])
    writer.writerow(['Blockchain Verification', prediction.get('blockchain_verification_status', 'N/A')])
    
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=report_{prediction["username"]}_{prediction["scan_date"].strftime("%Y%m%d_%H%M%S") if prediction.get("scan_date") else "unknown"}.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

@app.route('/prediction-history/delete/<id>', methods=['POST'])
def delete_prediction_history(id):
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    prediction_id = ObjectId(id)
    result = mongo.db.prediction_history.delete_one({'_id': prediction_id, 'user_id': session['user_id']})
    
    if result.deleted_count > 0:
        flash('Record deleted successfully!', 'success')
    else:
        flash('Record not found!', 'danger')
    
    return redirect(url_for('history'))

@app.route('/prediction/edit/<id>', methods=['GET', 'POST'])
def edit_prediction(id):
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    prediction_id = ObjectId(id)
    prediction = mongo.db.predictions.find_one({'_id': prediction_id, 'user_id': session['user_id']})
    
    if not prediction:
        flash('Prediction not found!', 'danger')
        return redirect(url_for('history'))
    
    if request.method == 'POST':
        mongo.db.predictions.update_one(
            {'_id': prediction_id},
            {'$set': {
                'username': request.form['username'],
                'followers': int(request.form['followers']),
                'following': int(request.form['following']),
                'posts': int(request.form['posts']),
                'bio_length': int(request.form['bio_length']),
                'has_profile_picture': int(request.form.get('has_profile_picture', 0)),
                'account_age_days': int(request.form['account_age_days'])
            }}
        )
        flash('Prediction updated successfully!', 'success')
        return redirect(url_for('history'))
    
    return render_template('edit_prediction.html', prediction=prediction)

@app.route('/prediction/delete/<id>', methods=['POST'])
def delete_prediction(id):
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    prediction_id = ObjectId(id)
    result = mongo.db.predictions.delete_one({'_id': prediction_id, 'user_id': session['user_id']})
    
    if result.deleted_count > 0:
        flash('Prediction deleted successfully!', 'success')
    else:
        flash('Prediction not found!', 'danger')
    
    return redirect(url_for('history'))

@app.route('/behavior-analysis', methods=['GET', 'POST'])
def behavior_analysis():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    behavior_result = None
    combined_result = None
    
    if request.method == 'POST':
        behavior_data = {
            'login_count': int(request.form.get('login_count', 0)),
            'posts_count': int(request.form.get('posts_count', 0)),
            'follow_requests_sent': int(request.form.get('follow_requests_sent', 0)),
            'likes_count': int(request.form.get('likes_count', 0)),
            'comments_count': int(request.form.get('comments_count', 0)),
            'shares_count': int(request.form.get('shares_count', 0)),
            'messages_count': int(request.form.get('messages_count', 0)),
            'avg_session_duration': int(request.form.get('avg_session_duration', 0)),
            'avg_actions_per_hour': int(request.form.get('avg_actions_per_hour', 0)),
            'continuous_activity_hours': int(request.form.get('continuous_activity_hours', 0)),
            'low_engagement_ratio': request.form.get('low_engagement_ratio') == 'on',
            'fixed_interval_actions': request.form.get('fixed_interval_actions') == 'on',
            'unusual_login_times': request.form.get('unusual_login_times') == 'on'
        }
        
        behavior_log = {
            'user_id': session['user_id'],
            'user_name': session['user_name'],
            **behavior_data,
            'created_at': datetime.now()
        }
        mongo.db.behavior_logs.insert_one(behavior_log)
        
        behavior_result = analyze_behavior(behavior_data)
        
        username = request.form.get('username', 'test_user')
        followers = int(request.form.get('followers', 100))
        following = int(request.form.get('following', 200))
        posts = int(request.form.get('profile_posts', 50))
        bio_length = int(request.form.get('bio_length', 100))
        has_profile_picture = 1 if request.form.get('has_profile_picture') == 'on' else 0
        account_age_days = int(request.form.get('account_age_days', 365))
        
        features = np.array([[followers, following, posts, bio_length, has_profile_picture, account_age_days]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)
        probability = model.predict_proba(features_scaled)
        pred_class = int(prediction[0])
        result = 'Fake' if pred_class == 1 else 'Real'
        confidence = round(probability[0][pred_class] * 100, 2)
        
        profile_result = {'result': result, 'confidence': confidence}
        combined_result = combine_with_profile_prediction(behavior_result, profile_result)
    
    return render_template('user/behavior_analysis.html', 
                         behavior_result=behavior_result,
                         combined_result=combined_result)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('index'))

# ==================== ADMIN ROUTES ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admins = mongo.db.admins
        admin = admins.find_one({'email': request.form['email']})
        
        if admin and bcrypt.checkpw(request.form['password'].encode('utf-8'), admin['password']):
            session['admin_id'] = str(admin['_id'])
            session['admin_email'] = admin['email']
            session['admin_logged_in'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials!', 'danger')
    
    return render_template('admin/admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    try:
        total_users = mongo.db.users.count_documents({})
    except:
        total_users = 0
    try:
        total_predictions = mongo.db.predictions.count_documents({})
    except:
        total_predictions = 0
    try:
        total_fake = mongo.db.predictions.count_documents({'result': 'Fake'})
    except:
        total_fake = 0
    try:
        total_real = mongo.db.predictions.count_documents({'result': 'Real'})
    except:
        total_real = 0
    try:
        total_feedback = mongo.db.feedback.count_documents({})
    except:
        total_feedback = 0
    try:
        total_behavior = mongo.db.behavior_logs.count_documents({})
    except:
        total_behavior = 0
    
    suspicious_count = 0
    try:
        suspicious_logs = list(mongo.db.behavior_logs.find())
        for log in suspicious_logs:
            avg_actions = log.get('avg_actions_per_hour', 0)
            continuous_hours = log.get('continuous_activity_hours', 0)
            if avg_actions > 100 or continuous_hours > 12:
                suspicious_count += 1
    except:
        suspicious_count = 0
    
    # Clean up recent users
    recent_users = []
    try:
        users_cursor = mongo.db.users.find().sort('created_at', -1).limit(5)
        for user in users_cursor:
            user['name'] = user.get('name', 'Unknown')
            user['email'] = user.get('email', 'N/A')
            recent_users.append(user)
    except:
        pass
    
    # Clean up recent predictions
    recent_predictions = []
    try:
        preds_cursor = mongo.db.predictions.find().sort('created_at', -1).limit(5)
        for pred in preds_cursor:
            pred['user_name'] = pred.get('user_name', 'Unknown')
            pred['username'] = pred.get('username', 'N/A')
            pred['result'] = pred.get('result', 'Unknown')
            pred['confidence'] = pred.get('confidence', 0)
            recent_predictions.append(pred)
    except:
        pass
    
    # Clean up recent behavior logs
    recent_behavior_logs = []
    try:
        recent_behavior_logs = list(mongo.db.behavior_logs.find().sort('created_at', -1).limit(5))
    except:
        pass
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_predictions=total_predictions,
                         total_fake=total_fake,
                         total_real=total_real,
                         total_feedback=total_feedback,
                         total_behavior=total_behavior,
                         suspicious_count=suspicious_count,
                         recent_users=recent_users,
                         recent_predictions=recent_predictions,
                         recent_behavior_logs=recent_behavior_logs)

@app.route('/admin/users')
def admin_users():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    users = mongo.db.users.find().sort('created_at', -1)
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
def admin_add_user():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})
        
        if existing_user is None:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({
                'name': request.form['name'],
                'email': request.form['email'],
                'password': hashed_password,
                'status': request.form.get('status', 'Active'),
                'created_at': datetime.now()
            })
            flash('User created successfully!', 'success')
            return redirect(url_for('admin_users'))
        else:
            flash('That email already exists!', 'danger')
    
    return render_template('admin_add_user.html')

@app.route('/admin/users/edit/<id>', methods=['GET', 'POST'])
def admin_edit_user(id):
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    user_id = ObjectId(id)
    user = mongo.db.users.find_one({'_id': user_id})
    
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('admin_users'))
    
    if request.method == 'POST':
        update_data = {
            'name': request.form['name'],
            'status': request.form['status']
        }
        
        if request.form['password']:
            update_data['password'] = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        
        mongo.db.users.update_one({'_id': user_id}, {'$set': update_data})
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin_edit_user.html', user=user)

@app.route('/admin/users/delete/<id>', methods=['POST'])
def admin_delete_user(id):
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    user_id = ObjectId(id)
    mongo.db.predictions.delete_many({'user_id': str(user_id)})
    mongo.db.users.delete_one({'_id': user_id})
    flash('User and associated predictions deleted successfully!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/predictions')
def admin_predictions():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    predictions = mongo.db.predictions.find().sort('created_at', -1)
    return render_template('admin/predictions.html', predictions=predictions)

@app.route('/admin/predictions/delete/<id>', methods=['POST'])
def admin_delete_prediction(id):
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    prediction_id = ObjectId(id)
    mongo.db.predictions.delete_one({'_id': prediction_id})
    flash('Prediction deleted successfully!', 'success')
    return redirect(url_for('admin_predictions'))

@app.route('/admin/feedback')
def admin_feedback():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    feedbacks = mongo.db.feedback.find().sort('created_at', -1)
    return render_template('admin/feedback.html', feedbacks=feedbacks)

@app.route('/admin/feedback/delete/<id>', methods=['POST'])
def admin_delete_feedback(id):
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    feedback_id = ObjectId(id)
    mongo.db.feedback.delete_one({'_id': feedback_id})
    flash('Feedback deleted successfully!', 'success')
    return redirect(url_for('admin_feedback'))

@app.route('/admin/behavior')
def admin_behavior_logs():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    logs = mongo.db.behavior_logs.find().sort('created_at', -1).limit(50)
    return render_template('admin/behavior_logs.html', logs=logs)

@app.route('/admin/admins')
def admin_admins():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    admins = mongo.db.admins.find().sort('created_at', -1)
    return render_template('admin/admins.html', admins=admins)

@app.route('/admin/admins/add', methods=['GET', 'POST'])
def admin_add_admin():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        admins = mongo.db.admins
        existing_admin = admins.find_one({'email': request.form['email']})
        
        if existing_admin is None:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            admins.insert_one({
                'email': request.form['email'],
                'password': hashed_password,
                'created_at': datetime.now()
            })
            flash('Admin created successfully!', 'success')
            return redirect(url_for('admin_admins'))
        else:
            flash('That email already exists!', 'danger')
    
    return render_template('admin_add_admin.html')

@app.route('/admin/admins/edit/<id>', methods=['GET', 'POST'])
def admin_edit_admin(id):
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    admin_id = ObjectId(id)
    admin = mongo.db.admins.find_one({'_id': admin_id})
    
    if not admin:
        flash('Admin not found!', 'danger')
        return redirect(url_for('admin_admins'))
    
    if request.method == 'POST':
        update_data = {'email': request.form['email']}
        
        if request.form['password']:
            update_data['password'] = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        
        mongo.db.admins.update_one({'_id': admin_id}, {'$set': update_data})
        flash('Admin updated successfully!', 'success')
        return redirect(url_for('admin_admins'))
    
    return render_template('admin_edit_admin.html', admin=admin)

@app.route('/admin/admins/delete/<id>', methods=['POST'])
def admin_delete_admin(id):
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    if str(id) == session.get('admin_id'):
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin_admins'))
    
    admin_id = ObjectId(id)
    mongo.db.admins.delete_one({'_id': admin_id})
    flash('Admin deleted successfully!', 'success')
    return redirect(url_for('admin_admins'))

@app.route('/admin/chat-logs')
def admin_chat_logs():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    chat_logs = mongo.db.chat_logs.find().sort('timestamp', -1).limit(100)
    return render_template('admin/chat_logs.html', chat_logs=chat_logs)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('admin_login'))

# ==================== CHATBOT ROUTES ====================

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    user_id = session.get('user_id')
    
    response_data = chatbot.get_response(user_message, user_id)
    
    if user_id:
        chat_log = {
            'user_id': user_id,
            'user_name': session.get('user_name'),
            'user_message': user_message,
            'bot_response': response_data['response'],
            'intent': response_data['intent'],
            'timestamp': datetime.now()
        }
        mongo.db.chat_logs.insert_one(chat_log)
    
    return jsonify(response_data)

# ==================== NETWORK ANALYSIS ROUTES ====================

@app.route('/network-analysis')
def network_analysis_page():
    if 'logged_in' not in session and 'admin_logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    return render_template('network_analysis.html')

@app.route('/api/network-analysis/generate', methods=['POST'])
def generate_network():
    try:
        num_nodes = request.form.get('num_nodes', 50)
        
        network_data = analyzer.generate_sample_network(num_nodes)
        
        analysis_record = {
            'user_id': session.get('user_id', session.get('admin_id')),
            'user_name': session.get('user_name', 'Admin'),
            'network_data': network_data,
            'success': network_data.get('success', False),
            'timestamp': datetime.now()
        }
        mongo.db.network_analyses.insert_one(analysis_record)
        
        return jsonify(network_data)
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(f"API Error generating network: {str(e)}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': [str(e)]
        }), 500

@app.route('/admin/network-analysis')
def admin_network_analysis():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    return render_template('admin/network_analysis.html')

# ==================== ENHANCED BEHAVIORAL ANALYSIS ROUTES ====================

@app.route('/admin/behavioral-analytics')
def admin_behavioral_analytics():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    return render_template('admin/behavioral_analytics.html')

@app.route('/api/behavioral-dashboard')
def api_behavioral_dashboard():
    if 'admin_logged_in' not in session and 'logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        dashboard_data = behavioral_analyzer.generate_dashboard_data()
        return jsonify(dashboard_data)
    except Exception as e:
        logging.exception(f"Error generating dashboard data: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/behavior-trends')
def behavior_trends():
    """API endpoint for behavioral analytics trends data"""
    data = {
        "login": {
            "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "values": [5, 12, 20, 4, 7, 8, 15]
        },
        "activity": {
            "labels": ["Posts", "Likes", "Comments", "Shares", "Messages"],
            "values": [25, 40, 15, 5, 15]
        },
        "suspicion": {
            "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "values": [15, 35, 68, 10, 22, 30, 45]
        }
    }
    return jsonify(data)

@app.route('/api/detect-coordinated-activity', methods=['POST'])
def detect_coordinated_activity():
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    
    try:
        users_data = request.get_json().get('users_data', [])
        result = behavioral_analyzer.detect_coordinated_activity(users_data)
        return jsonify(result)
    except Exception as e:
        logging.exception(f"Error detecting coordinated activity: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-alerts', methods=['POST'])
def generate_alerts():
    if 'logged_in' not in session and 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        analysis_result = request.get_json()
        alerts = behavioral_analyzer.generate_alerts(analysis_result)
        return jsonify({'alerts': alerts})
    except Exception as e:
        logging.exception(f"Error generating alerts: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analyze-advanced-behavior', methods=['POST'])
def api_analyze_advanced_behavior():
    if 'logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        behavior_data = request.get_json()
        result = behavioral_analyzer.analyze_behavior(behavior_data)
        
        log_data = {
            'user_id': session.get('user_id'),
            'user_name': session.get('user_name'),
            'behavior_data': behavior_data,
            'analysis_result': result,
            'created_at': datetime.now()
        }
        mongo.db.advanced_behavior_logs.insert_one(log_data)
        
        return jsonify(result)
    except Exception as e:
        logging.exception(f"Error analyzing behavior: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== NEW COMPREHENSIVE BEHAVIORAL ANALYSIS ROUTES ====================

@app.route('/api/login-frequency-trend')
def login_frequency_trend():
    """Get login frequency trend data for configurable periods"""
    period = request.args.get('period', 'daily')
    data = behavioral_analyzer.get_login_frequency_trend(period)
    return jsonify(data)

@app.route('/api/activity-distribution')
def activity_distribution_api():
    """Get activity distribution data"""
    data = behavioral_analyzer.get_activity_distribution()
    return jsonify(data)

@app.route('/api/suspicion-score-trend')
def suspicion_score_trend():
    """Get suspicion score trend data"""
    period = request.args.get('period', 'daily')
    data = behavioral_analyzer.get_suspicion_score_trend(period)
    return jsonify(data)

@app.route('/api/detect-deviations', methods=['POST'])
def detect_deviations_api():
    """Detect statistically significant deviations"""
    try:
        data = request.get_json()
        values = data.get('values', [])
        threshold = data.get('threshold', 2.0)
        result = behavioral_analyzer.detect_deviations(values, threshold)
        return jsonify(result)
    except Exception as e:
        logging.exception(f"Error detecting deviations: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export-csv', methods=['POST'])
def export_csv():
    """Export data to CSV format"""
    try:
        data = request.get_json()
        csv_content = behavioral_analyzer.export_data_csv(data)
        return jsonify({'success': True, 'csv_content': csv_content})
    except Exception as e:
        logging.exception(f"Error exporting CSV: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export-json', methods=['POST'])
def export_json():
    """Export data to JSON format"""
    try:
        data = request.get_json()
        json_content = behavioral_analyzer.export_data_json(data)
        return jsonify({'success': True, 'json_content': json_content})
    except Exception as e:
        logging.exception(f"Error exporting JSON: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500





# ==================== SOCIAL GRAPH INTELLIGENCE ROUTES ====================

@app.route('/social-graph')
def social_graph_page():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    return render_template('user/social_graph.html')

@app.route('/api/social-graph/data')
def get_social_graph_data():
    if 'logged_in' not in session and 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    try:
        graph_data = social_graph_engine.get_graph_json()
        return jsonify({'success': True, 'graph': graph_data})
    except Exception as e:
        logging.exception(f"Error getting social graph data: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/social-graph/analyze/<username>')
def analyze_profile_network(username):
    if 'logged_in' not in session and 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    try:
        report = social_graph_engine.generate_report(username)
        return jsonify({'success': True, 'report': report})
    except Exception as e:
        logging.exception(f"Error analyzing profile network: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/social-graph/bot-clusters')
def get_bot_clusters():
    if 'logged_in' not in session and 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    try:
        clusters = social_graph_engine.detect_bot_clusters()
        return jsonify({'success': True, 'clusters': clusters})
    except Exception as e:
        logging.exception(f"Error getting bot clusters: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/social-graph-analytics')
def admin_social_graph_analytics():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    graph_data = social_graph_engine.get_graph_json()
    clusters = social_graph_engine.detect_bot_clusters()
    total_profiles = len(graph_data['nodes'])
    total_clusters = len(clusters)
    high_risk = sum(1 for node in graph_data['nodes'] if node['risk'] >= 70)
    
    return render_template('admin/social_graph_analytics.html',
                          total_profiles=total_profiles,
                          total_clusters=total_clusters,
                          high_risk=high_risk,
                          clusters=clusters)


# ==================== GROWTH PREDICTION ROUTES ====================

@app.route('/growth-prediction')
def growth_prediction_page():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    last_scan = get_last_scan(session.get('user_id'))
    return render_template('user/growth_prediction.html', scan=last_scan)

@app.route('/api/calculate-growth-report', methods=['POST'])
def calculate_growth_report():
    if 'logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        print("Growth prediction request received!")
        username = request.form.get('username', '')
        profile_data = {
            'followers': int(request.form.get('followers', 0)),
            'following': int(request.form.get('following', 0)),
            'posts': int(request.form.get('posts', 0)),
            'total_likes': int(request.form.get('total_likes', 0)),
            'total_comments': int(request.form.get('total_comments', 0)),
            'account_age_days': int(request.form.get('account_age_days', 30))
        }
        
        use_sample_history = request.form.get('use_sample_history', 'on') == 'on'
        growth_history = None
        if use_sample_history:
            growth_history = growth_engine.generate_sample_growth_history(
                profile_data.get('followers', 1000), 30
            )
        
        report = growth_engine.generate_growth_report(username, profile_data, growth_history)
        
        # Store in MongoDB - use datetime object for generated_at
        report_for_mongo = report.copy()
        report_for_mongo['generated_at'] = datetime.now()
        mongo.db.growth_reports.insert_one({
            'user_id': session['user_id'],
            'user_name': session['user_name'],
            **report_for_mongo
        })
        
        return jsonify({'success': True, 'report': report, 'history': growth_history})
    except Exception as e:
        logging.exception(f"Error calculating growth report: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-growth-history', methods=['GET'])
def get_growth_history():
    if 'logged_in' not in session and 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    
    try:
        start_followers = int(request.args.get('start_followers', 1000))
        days = int(request.args.get('days', 30))
        history = growth_engine.generate_sample_growth_history(start_followers, days)
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        logging.exception(f"Error getting growth history: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/growth-history')
@app.route('/growth-prediction/history')
def growth_history():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    history = mongo.db.growth_reports.find({'user_id': session['user_id']}).sort('generated_at', -1)
    return render_template('user/growth_history.html', history=history)

@app.route('/admin/growth-analytics')
def admin_growth_analytics():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    total_reports = mongo.db.growth_reports.count_documents({})
    high_risk_reports = mongo.db.growth_reports.count_documents({'growth_risk_score': {'$gte': 70}})
    avg_trust_score = 0
    if total_reports > 0:
        pipeline = [{'$group': {'_id': None, 'avg': {'$avg': '$growth_trust_score'}}}]
        avg_result = list(mongo.db.growth_reports.aggregate(pipeline))
        avg_trust_score = round(avg_result[0]['avg'], 2) if avg_result else 0
    
    recent_reports = list(mongo.db.growth_reports.find().sort('generated_at', -1).limit(10))
    return render_template('admin/growth_analytics.html',
                          total_reports=total_reports,
                          avg_trust_score=avg_trust_score,
                          high_risk_reports=high_risk_reports,
                          recent_reports=recent_reports)


# ================================================== 
 
# GEOLOCATION RISK ANALYSIS ROUTES 
# ==================================================

@app.route('/geolocation-risk')
def geolocation_risk_page():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    last_scan = get_last_scan(session.get('user_id'))
    return render_template('user/geolocation_risk.html', scan=last_scan)

@app.route('/api/geolocation-analysis', methods=['GET', 'POST'])
def geolocation_analysis():
    if 'logged_in' not in session and 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    
    try:
        # Generate sample login history
        login_history = geolocation_engine.generate_login_history(10)
        
        # Analyze logins
        analysis_result = geolocation_engine.analyze_logins(login_history)
        
        # Create report
        report = geolocation_engine.create_report(analysis_result)
        
        # Convert datetime objects to strings for JSON
        for login in login_history:
            login['timestamp'] = login['timestamp'].isoformat()
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'report': report,
            'login_history': login_history
        })
    except Exception as e:
        logging.exception(f"Error in geolocation analysis: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/geolocation-dashboard')
def admin_geolocation_dashboard():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    return render_template('admin/geolocation_dashboard.html')

# ================================================== 
# THREAT ALERT SYSTEM ROUTES 
# ==================================================

@app.route('/admin/threat-alerts')
def admin_threat_alerts():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    return render_template('admin/threat_alerts.html')

@app.route('/api/threat-alerts')
def api_threat_alerts():
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    try:
        return jsonify({
            'success': True,
            'alerts': alert_system.get_all_alerts(),
            'recent_alerts': alert_system.get_recent_alerts(10),
            'critical_alerts': alert_system.get_critical_alerts()
        })
    except Exception as e:
        logging.exception(f"Error getting threat alerts: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-test-alert', methods=['POST'])
def api_generate_test_alert():
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    try:
        import random
        username = request.form.get('username', f'test_profile_{random.randint(1000,9999)}')
        risk_score = int(request.form.get('risk_score', random.randint(70, 100)))
        threat_type = random.choice(alert_system.threat_types)
        reasons = [
            'Suspicious phishing links detected', 
            'High scam keyword density', 
            'Fake promotional content', 
            'Duplicate profile image'
        ]
        detection_reasons = random.sample(reasons, k=random.randint(2,4))
        
        alert = alert_system.generate_threat_alert(
            username=username,
            risk_score=risk_score,
            threat_type=threat_type,
            detection_reasons=detection_reasons
        )
        
        # Send email and SMS (simulated)
        alert_system.send_email_alert(alert)
        alert_system.send_sms_alert(alert)
        
        return jsonify({'success': True, 'alert': alert})
    except Exception as e:
        logging.exception(f"Error generating test alert: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/update-alert-status/<int:alert_id>', methods=['POST'])
def api_update_alert_status(alert_id):
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    try:
        new_status = request.form.get('status', 'RESOLVED')
        alert_system.update_alert_status(alert_id, new_status)
        return jsonify({'success': True, 'alert_id': alert_id, 'new_status': new_status})
    except Exception as e:
        logging.exception(f"Error updating alert status: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500



# ================================================== 
# BLOCKCHAIN IDENTITY VERIFICATION ROUTES 
# ==================================================

@app.route('/identity-verification')
def identity_verification_page():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    last_scan = get_last_scan(session.get('user_id'))
    return render_template('user/identity_verification.html', scan=last_scan)

@app.route('/api/verify-identity', methods=['POST'])
def api_verify_identity():
    if 'logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    
    try:
        data = request.form
        identity_data = {
            "name": data.get("name", session.get('user_name', 'User')),
            "country": data.get("country", "Unknown"),
            "document_id": data.get("document_id", "")
        }
        user_id = session.get('user_id', 'USR' + str(hash(session.get('user_name')))[:6])
        
        verification_result = identity_system.create_verification_record(
            user_id=user_id,
            user_name=session.get('user_name', 'User'),
            identity_data=identity_data
        )
        
        return jsonify({'success': True, 'verification': verification_result})
    except Exception as e:
        logging.exception(f"Error verifying identity: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/identity-dashboard')
def admin_identity_dashboard():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    history = identity_system.get_verification_history()
    return render_template('admin/identity_dashboard.html', history=history)

@app.route('/api/admin-identity-history')
def api_admin_identity_history():
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    try:
        history = identity_system.get_verification_history()
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        logging.exception(f"Error getting identity history: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== FAKE FOLLOWER MARKETPLACE DETECTION ROUTES ====================

@app.route('/fake-follower-detection')
def fake_follower_detection_page():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    last_scan = get_last_scan(session.get('user_id'))
    return render_template('user/fake_follower_detection.html', scan=last_scan)


@app.route('/api/analyze-fake-followers', methods=['POST'])
def api_analyze_fake_followers():
    if 'logged_in' not in session and 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        username = data.get('username', '')
        followers = int(data.get('followers', 0))
        following = int(data.get('following', 0))
        avg_likes = int(data.get('avg_likes', 0))
        avg_comments = int(data.get('avg_comments', 0))
        account_age_days = int(data.get('account_age_days', 0))

        report = fake_follower_engine.analyze_profile(
            username, followers, following, avg_likes, avg_comments, account_age_days
        )

        # Save to MongoDB
        mongo.db.fake_follower_reports.insert_one({
            'user_id': session.get('user_id', session.get('admin_id')),
            'user_name': session.get('user_name', 'Admin'),
            **report
        })

        return jsonify({'success': True, 'report': report})

    except Exception as e:
        logging.exception(f"Error analyzing fake followers: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/admin/fake-follower-detection')
def admin_fake_follower_detection():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    return render_template('admin/fake_follower_detection.html')


@app.route('/admin/fake-follower-reports')
def admin_fake_follower_reports():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    reports = list(mongo.db.fake_follower_reports.find().sort('created_at', -1).limit(50))
    return render_template('admin/fake_follower_reports.html', reports=reports)


# ==================== CYBERCRIME INTELLIGENCE INTEGRATION ROUTES ====================

@app.route('/cybercrime-intelligence')
def cybercrime_intelligence_page():
    if 'logged_in' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    last_scan = get_last_scan(session.get('user_id'))
    return render_template('user/cybercrime_intelligence.html', scan=last_scan)


@app.route('/api/analyze-cybercrime', methods=['POST'])
def api_analyze_cybercrime():
    if 'logged_in' not in session and 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        username = data.get('username', '')
        bio = data.get('bio', '')
        captions = [c.strip() for c in data.get('captions', '').split('\n') if c.strip()]
        links = [l.strip() for l in data.get('links', '').split('\n') if l.strip()]
        
        report = cybercrime_engine.analyze_profile(username, bio, captions, links)
        
        # Save to MongoDB
        mongo.db.cybercrime_reports.insert_one({
            'user_id': session.get('user_id', session.get('admin_id')),
            'user_name': session.get('user_name', 'Admin'),
            **report
        })
        
        return jsonify({'success': True, 'report': report})
        
    except Exception as e:
        logging.exception(f"Error analyzing cybercrime: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/admin/cybercrime-intelligence')
def admin_cybercrime_intelligence():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    return render_template('admin/cybercrime_intelligence.html')


@app.route('/admin/cybercrime-reports')
def admin_cybercrime_reports():
    if 'admin_logged_in' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    reports = list(mongo.db.cybercrime_reports.find().sort('created_at', -1).limit(50))
    return render_template('admin/cybercrime_reports.html', reports=reports)


if __name__ == '__main__':

    print("Starting Flask server...")
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)
    print("Server stopped.")
