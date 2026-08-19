
from datetime import datetime, timedelta
import random

class GrowthPredictionEngine:
    def __init__(self):
        pass

    def calculate_growth_metrics(self, profile_data):
        followers = profile_data.get('followers', 0)
        following = profile_data.get('following', 0)
        posts = profile_data.get('posts', 0)
        total_likes = profile_data.get('total_likes', 0)
        total_comments = profile_data.get('total_comments', 0)
        account_age_days = profile_data.get('account_age_days', 30)
        
        avg_followers_per_day = followers / max(account_age_days, 1)
        avg_likes_per_post = total_likes / max(posts, 1)
        avg_comments_per_post = total_comments / max(posts, 1)
        engagement_rate = ((total_likes + total_comments) / max(followers, 1)) * 100
        follower_following_ratio = followers / max(following, 1)
        
        return {
            'avg_followers_per_day': avg_followers_per_day,
            'avg_likes_per_post': avg_likes_per_post,
            'avg_comments_per_post': avg_comments_per_post,
            'engagement_rate': engagement_rate,
            'follower_following_ratio': follower_following_ratio
        }

    def detect_growth_anomalies(self, growth_history):
        if not growth_history or len(growth_history) < 2:
            return {'has_spike': False, 'anomalies': []}
        
        anomalies = []
        has_spike = False
        
        for i in range(1, len(growth_history)):
            prev_day = growth_history[i-1]['followers']
            current_day = growth_history[i]['followers']
            increase = current_day - prev_day
            
            if prev_day > 0:
                percent_increase = (increase / prev_day) * 100
                if percent_increase > 50:
                    has_spike = True
                    anomalies.append({
                        'day': i,
                        'date': growth_history[i]['date'],
                        'increase': increase,
                        'percent_increase': round(percent_increase, 2),
                        'severity': 'High' if percent_increase > 100 else 'Medium'
                    })
        
        return {
            'has_spike': has_spike,
            'anomalies': anomalies,
            'anomaly_count': len(anomalies)
        }

    def calculate_growth_trust_score(self, profile_data, growth_history=None):
        score = 100
        reasons = []
        
        metrics = self.calculate_growth_metrics(profile_data)
        
        if profile_data.get('followers', 0) > 0:
            if metrics['engagement_rate'] < 0.5:
                score -= 30
                reasons.append("Very low engagement rate")
            elif metrics['engagement_rate'] < 2:
                score -= 15
                reasons.append("Low engagement rate")
        
        if metrics['follower_following_ratio'] < 0.2:
            score -= 25
            reasons.append("Extremely low follower/following ratio")
        elif metrics['follower_following_ratio'] < 0.5:
            score -= 10
            reasons.append("Low follower/following ratio")
        
        if metrics['avg_followers_per_day'] > 500 and metrics['engagement_rate'] < 1:
            score -= 30
            reasons.append("Unnatural growth pattern with low engagement")
        elif metrics['avg_followers_per_day'] > 200:
            score -= 15
            reasons.append("High daily follower growth")
        
        if growth_history:
            anomalies = self.detect_growth_anomalies(growth_history)
            if anomalies['has_spike']:
                score -= 30
                reasons.append("Sudden follower spike(s) detected")
        
        return {
            'trust_score': max(0, min(score, 100)),
            'reasons': reasons
        }

    def calculate_growth_risk_score(self, trust_score, profile_data, growth_history=None):
        risk_score = 100 - trust_score
        
        if trust_score < 30:
            risk_level = "Critical Risk"
        elif trust_score < 50:
            risk_level = "High Risk"
        elif trust_score < 70:
            risk_level = "Moderate Risk"
        elif trust_score < 90:
            risk_level = "Low Risk"
        else:
            risk_level = "Safe"
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level
        }

    def predict_future_followers(self, current_followers, avg_daily_growth, days_to_predict):
        if avg_daily_growth <= 0:
            avg_daily_growth = 1
        
        predictions = {}
        
        if days_to_predict >= 7:
            predictions['7_days'] = round(current_followers + (avg_daily_growth * 7))
        if days_to_predict >= 30:
            predictions['30_days'] = round(current_followers + (avg_daily_growth * 30))
        if days_to_predict >= 90:
            predictions['90_days'] = round(current_followers + (avg_daily_growth * 90))
        
        confidence = 75 + random.randint(0, 20)
        
        return {
            'predictions': predictions,
            'confidence': min(confidence, 95)
        }

    def generate_growth_report(self, username, profile_data, growth_history=None):
        metrics = self.calculate_growth_metrics(profile_data)
        trust_result = self.calculate_growth_trust_score(profile_data, growth_history)
        risk_result = self.calculate_growth_risk_score(trust_result['trust_score'], profile_data, growth_history)
        future_growth = self.predict_future_followers(
            profile_data.get('followers', 0),
            metrics['avg_followers_per_day'],
            90
        )
        
        return {
            'username': username,
            'current_followers': profile_data.get('followers', 0),
            'metrics': metrics,
            'growth_trust_score': trust_result['trust_score'],
            'growth_trust_reasons': trust_result['reasons'],
            'growth_risk_score': risk_result['risk_score'],
            'growth_risk_level': risk_result['risk_level'],
            'future_predictions': future_growth,
            'generated_at': datetime.now().isoformat()
        }

    def predict_growth(self, current_followers, account_age_days, avg_posts_per_week=1):
        avg_daily_growth = current_followers / max(account_age_days, 1)
        
        predicted_7_days = round(current_followers + (avg_daily_growth * 7))
        predicted_30_days = round(current_followers + (avg_daily_growth * 30))
        
        growth_trust_score = 80
        if avg_daily_growth > 500:
            growth_trust_score = 40
        elif avg_daily_growth > 200:
            growth_trust_score = 60
        
        growth_manipulation_probability = 100 - growth_trust_score
        
        ai_recommendation = "Account growth appears natural" if growth_trust_score > 70 else "Potential growth manipulation detected"
        
        return {
            'predicted_7_days': predicted_7_days,
            'predicted_30_days': predicted_30_days,
            'growth_rate': round(avg_daily_growth, 2),
            'growth_trust_score': growth_trust_score,
            'growth_manipulation_probability': growth_manipulation_probability,
            'ai_recommendation': ai_recommendation
        }
        
    def generate_sample_growth_history(self, start_followers=1000, days=30):
        history = []
        current_date = datetime.now()
        current_followers = start_followers
        
        for day in range(days):
            date = current_date - timedelta(days=days - day)
            history.append({
                'date': date.isoformat(),
                'followers': current_followers,
                'posts': random.randint(0, 2),
                'likes': random.randint(50, 200) if current_followers > 1000 else random.randint(5, 50)
            })
            
            growth = random.randint(10, 50)
            if random.random() < 0.05:
                growth = random.randint(500, 2000)
            current_followers += growth
        
        return history

growth_engine = GrowthPredictionEngine()
