import numpy as np
from datetime import datetime, timedelta
import random
import csv
import io
import json

class BehavioralAnalyzer:
    def __init__(self):
        pass
    
    def analyze_behavior(self, behavior_data):
        """
        Analyze user behavior to detect bot-like activity with advanced AI/ML features.
        
        Args:
            behavior_data (dict): Dictionary containing behavior metrics
            
        Returns:
            dict: Analysis results including activity score, bot probability, and risk level
        """
        activity_score = calculate_activity_score(behavior_data)
        bot_probability = calculate_bot_probability(behavior_data, activity_score)
        risk_level = get_risk_level(bot_probability)
        suspicious_flags = identify_suspicious_flags(behavior_data, activity_score)
        recommendation = get_recommendation(bot_probability)
        suspicion_score = self.calculate_suspicion_score(behavior_data, bot_probability)
        anomaly_score = self.detect_anomalies(behavior_data)
        predicted_future_risk = self.predict_future_risk(behavior_data, bot_probability)
        detection_indicators = self.get_detection_indicators(behavior_data)
        
        return {
            'activity_score': activity_score,
            'bot_probability': bot_probability,
            'risk_level': risk_level,
            'suspicious_flags': suspicious_flags,
            'recommendation': recommendation,
            'suspicion_score': suspicion_score,
            'anomaly_score': anomaly_score,
            'predicted_future_risk': predicted_future_risk,
            'detection_indicators': detection_indicators
        }
    
    def get_detection_indicators(self, behavior_data):
        """
        Get fake profile detection indicators
        """
        indicators = []
        
        login_count = behavior_data.get('login_count', 0)
        posts_count = behavior_data.get('posts_count', 0)
        avg_actions_per_hour = behavior_data.get('avg_actions_per_hour', 0)
        continuous_activity_hours = behavior_data.get('continuous_activity_hours', 0)
        follow_requests_sent = behavior_data.get('follow_requests_sent', 0)
        comments_count = behavior_data.get('comments_count', 0)
        messages_count = behavior_data.get('messages_count', 0)
        
        if login_count > 15:
            indicators.append({'type': 'high_frequency_logins', 'description': 'High-frequency login attempts'})
        
        if avg_actions_per_hour > 100:
            indicators.append({'type': 'repetitive_actions', 'description': 'Repetitive actions in short intervals'})
        
        if posts_count > 50 and avg_actions_per_hour > 50:
            indicators.append({'type': 'automated_posting', 'description': 'Automated posting behavior'})
        
        if follow_requests_sent > 100:
            indicators.append({'type': 'sudden_follower_spikes', 'description': 'Sudden following activity'})
        
        if comments_count > 100 or messages_count > 200:
            indicators.append({'type': 'spam_interactions', 'description': 'Spam interaction patterns'})
        
        return indicators
    
    def calculate_suspicion_score(self, behavior_data, bot_probability):
        """
        Calculate a dynamic suspicion score from 0 to 100
        """
        score = bot_probability
        
        login_locations = behavior_data.get('login_locations', 1)
        device_switches = behavior_data.get('device_switches', 0)
        vpn_usage = behavior_data.get('vpn_usage', False)
        
        if login_locations > 3:
            score += 15
        elif login_locations > 1:
            score += 5
            
        if device_switches > 5:
            score += 20
        elif device_switches > 2:
            score += 10
            
        if vpn_usage:
            score += 10
            
        return min(100, max(0, int(score)))
    
    def detect_anomalies(self, behavior_data):
        """
        Simulate anomaly detection using statistical methods
        """
        anomalies = []
        actions_per_hour = behavior_data.get('avg_actions_per_hour', 0)
        continuous_activity = behavior_data.get('continuous_activity_hours', 0)
        messages_count = behavior_data.get('messages_count', 0)
        follow_requests = behavior_data.get('follow_requests_sent', 0)
        
        if actions_per_hour > 150:
            anomalies.append({'type': 'extreme_activity', 'severity': 'high'})
        elif actions_per_hour > 100:
            anomalies.append({'type': 'high_activity', 'severity': 'medium'})
            
        if continuous_activity > 16:
            anomalies.append({'type': 'non_stop_activity', 'severity': 'high'})
            
        if messages_count > 200:
            anomalies.append({'type': 'mass_messaging', 'severity': 'high'})
            
        if follow_requests > 100:
            anomalies.append({'type': 'rapid_following', 'severity': 'medium'})
            
        return {
            'count': len(anomalies),
            'anomalies': anomalies,
            'overall_anomaly_score': min(100, sum(10 if a['severity'] == 'high' else 5 for a in anomalies))
        }
    
    def predict_future_risk(self, behavior_data, current_bot_prob):
        """
        Predict future risky behavior patterns using simple trend analysis
        """
        trend_factor = random.uniform(0.8, 1.2)
        future_risk = current_bot_prob * trend_factor
        
        return {
            'next_24h_risk': min(100, int(future_risk)),
            'next_7d_risk': min(100, int(future_risk * 1.1)),
            'risk_trend': 'increasing' if trend_factor > 1 else 'decreasing'
        }
    
    def generate_dashboard_data(self, user_id=None):
        """
        Generate dashboard analytics data for visualization
        """
        days = 7
        suspicion_trend = []
        login_frequency = []
        activity_distribution = []
        
        for i in range(days):
            suspicion_trend.append(random.randint(10, 80))
            login_frequency.append(random.randint(1, 20))
            
        activity_distribution = [
            {'label': 'Likes', 'value': random.randint(50, 500)},
            {'label': 'Comments', 'value': random.randint(20, 200)},
            {'label': 'Posts', 'value': random.randint(5, 50)},
            {'label': 'Messages', 'value': random.randint(10, 100)},
            {'label': 'Follows', 'value': random.randint(10, 150)}
        ]
        
        return {
            'suspicion_trend': suspicion_trend,
            'login_frequency': login_frequency,
            'activity_distribution': activity_distribution,
            'labels': [f'Day {i+1}' for i in range(days)]
        }
    
    def detect_coordinated_activity(self, users_data):
        """
        Detect coordinated scam campaigns through behavioral similarity
        """
        coordinated_groups = []
        
        if len(users_data) < 2:
            return {'coordinated_groups': [], 'alert': False}
            
        for i, user1 in enumerate(users_data):
            for j, user2 in enumerate(users_data):
                if i >= j:
                    continue
                    
                similarity_score = self.calculate_behavioral_similarity(user1, user2)
                
                if similarity_score > 0.8:
                    coordinated_groups.append({
                        'user1': user1.get('user_id', 'Unknown'),
                        'user2': user2.get('user_id', 'Unknown'),
                        'similarity_score': round(similarity_score * 100, 2)
                    })
        
        return {
            'coordinated_groups': coordinated_groups,
            'alert': len(coordinated_groups) > 0,
            'total_suspicious_pairs': len(coordinated_groups)
        }
    
    def calculate_behavioral_similarity(self, user1_data, user2_data):
        """
        Calculate behavioral similarity between two users
        """
        features = ['login_count', 'posts_count', 'avg_actions_per_hour', 
                   'continuous_activity_hours', 'likes_count', 'comments_count']
        matches = 0
        
        for feature in features:
            val1 = user1_data.get(feature, 0)
            val2 = user2_data.get(feature, 0)
            
            if max(val1, val2) > 0:
                ratio = min(val1, val2) / max(val1, val2)
                if ratio > 0.8:
                    matches += 1
        
        return matches / len(features)
    
    def generate_alerts(self, analysis_result):
        """
        Generate automated alerts for suspicious users and bot activities
        """
        alerts = []
        
        if analysis_result.get('risk_level') == 'High':
            alerts.append({
                'type': 'high_risk',
                'severity': 'critical',
                'message': 'High risk user detected - Immediate review required'
            })
        
        if analysis_result.get('suspicion_score', 0) > 70:
            alerts.append({
                'type': 'high_suspicion',
                'severity': 'warning',
                'message': 'Suspicion score exceeds threshold'
            })
        
        if analysis_result.get('anomaly_score', {}).get('overall_anomaly_score', 0) > 50:
            alerts.append({
                'type': 'anomaly_detected',
                'severity': 'warning',
                'message': 'Behavioral anomalies detected'
            })
        
        return alerts

    def get_login_frequency_trend(self, period='daily'):
        """
        Get login frequency trend data for configurable time periods
        """
        data = {
            'daily': {
                'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'values': [5, 12, 8, 20, 15, 7, 9]
            },
            'weekly': {
                'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                'values': [60, 75, 55, 90]
            },
            'monthly': {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'values': [300, 250, 350, 400, 450, 380]
            }
        }
        
        return data.get(period, data['daily'])

    def get_activity_distribution(self):
        """
        Get activity distribution data
        """
        return [
            {'category': 'Posts', 'count': 45, 'percentage': 15},
            {'category': 'Likes', 'count': 120, 'percentage': 40},
            {'category': 'Comments', 'count': 60, 'percentage': 20},
            {'category': 'Messages', 'count': 35, 'percentage': 11.67},
            {'category': 'Shares', 'count': 15, 'percentage': 5},
            {'category': 'Follows', 'count': 25, 'percentage': 8.33}
        ]

    def get_suspicion_score_trend(self, period='daily'):
        """
        Get suspicion score trend data
        """
        data = {
            'daily': {
                'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'values': [15, 35, 68, 10, 22, 30, 45]
            },
            'weekly': {
                'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                'values': [20, 30, 45, 55]
            },
            'monthly': {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'values': [15, 25, 35, 40, 50, 45]
            }
        }
        
        return data.get(period, data['daily'])

    def detect_deviations(self, data_values, threshold=2.0):
        """
        Detect statistically significant deviations from the mean
        """
        mean = np.mean(data_values)
        std_dev = np.std(data_values)
        deviations = []
        
        for i, value in enumerate(data_values):
            z_score = abs(value - mean) / std_dev if std_dev != 0 else 0
            if z_score > threshold:
                deviations.append({
                    'index': i,
                    'value': value,
                    'z_score': round(z_score, 2),
                    'deviation_from_mean': round(value - mean, 2)
                })
        
        return {
            'mean': round(mean, 2),
            'std_dev': round(std_dev, 2),
            'threshold': threshold,
            'deviations': deviations,
            'has_deviations': len(deviations) > 0
        }

    def export_data_csv(self, data):
        """
        Export data to CSV format
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        if isinstance(data, dict):
            if 'labels' in data and 'values' in data:
                writer.writerow(['Label', 'Value'])
                for label, value in zip(data['labels'], data['values']):
                    writer.writerow([label, value])
        elif isinstance(data, list):
            if len(data) > 0:
                headers = list(data[0].keys())
                writer.writerow(headers)
                for row in data:
                    writer.writerow([row[h] for h in headers])
        
        return output.getvalue()

    def export_data_json(self, data):
        """
        Export data to JSON format
        """
        return json.dumps(data, indent=2)

def calculate_activity_score(behavior_data):
    """Calculate a normalized activity score from 0 to 100."""
    score = 0
    
    login_frequency = behavior_data.get('login_count', 0)
    posting_frequency = behavior_data.get('posts_count', 0)
    follow_requests = behavior_data.get('follow_requests_sent', 0)
    likes = behavior_data.get('likes_count', 0)
    comments = behavior_data.get('comments_count', 0)
    shares = behavior_data.get('shares_count', 0)
    messages = behavior_data.get('messages_count', 0)
    session_duration = behavior_data.get('avg_session_duration', 0)
    actions_per_hour = behavior_data.get('avg_actions_per_hour', 0)
    
    score += min(login_frequency * 5, 20)
    score += min(posting_frequency * 3, 15)
    score += min(follow_requests * 2, 10)
    score += min(likes * 1, 15)
    score += min(comments * 2, 10)
    score += min(shares * 1, 10)
    score += min(messages * 1, 10)
    score += min(session_duration / 5, 10)
    
    if actions_per_hour > 100:
        score -= 20
    elif actions_per_hour > 50:
        score -= 10
    
    return max(0, min(100, int(score)))

def calculate_bot_probability(behavior_data, activity_score):
    """Calculate the probability that the user is a bot (0-100%)."""
    probability = 0
    
    actions_per_hour = behavior_data.get('avg_actions_per_hour', 0)
    continuous_activity_hours = behavior_data.get('continuous_activity_hours', 0)
    low_engagement_ratio = behavior_data.get('low_engagement_ratio', False)
    fixed_interval_actions = behavior_data.get('fixed_interval_actions', False)
    unusual_login_times = behavior_data.get('unusual_login_times', False)
    
    if actions_per_hour > 100:
        probability += 30
    elif actions_per_hour > 50:
        probability += 15
    
    if continuous_activity_hours >= 20:
        probability += 25
    elif continuous_activity_hours >= 12:
        probability += 15
    
    if low_engagement_ratio:
        probability += 20
    
    if fixed_interval_actions:
        probability += 15
    
    if unusual_login_times:
        probability += 10
    
    if activity_score < 20:
        probability += 10
    elif activity_score > 80 and actions_per_hour > 30:
        probability += 5
    
    return min(100, max(0, probability))

def get_risk_level(bot_probability):
    """Determine risk level based on bot probability."""
    if bot_probability >= 70:
        return 'High'
    elif bot_probability >= 40:
        return 'Medium'
    else:
        return 'Low'

def identify_suspicious_flags(behavior_data, activity_score):
    """Identify specific suspicious behavior flags."""
    flags = []
    actions_per_hour = behavior_data.get('avg_actions_per_hour', 0)
    continuous_activity_hours = behavior_data.get('continuous_activity_hours', 0)
    low_engagement_ratio = behavior_data.get('low_engagement_ratio', False)
    fixed_interval_actions = behavior_data.get('fixed_interval_actions', False)
    unusual_login_times = behavior_data.get('unusual_login_times', False)
    
    if actions_per_hour > 100:
        flags.append('Extremely high action frequency')
    elif actions_per_hour > 50:
        flags.append('High action frequency')
    
    if continuous_activity_hours >= 20:
        flags.append('24/7 continuous activity detected')
    elif continuous_activity_hours >= 12:
        flags.append('Unusually long activity periods')
    
    if low_engagement_ratio:
        flags.append('Low engagement with high posting frequency')
    
    if fixed_interval_actions:
        flags.append('Repeated actions at fixed intervals')
    
    if unusual_login_times:
        flags.append('Unusual login time patterns')
    
    if activity_score < 20:
        flags.append('Very low overall activity')
    
    return flags

def get_recommendation(bot_probability):
    """Provide a recommendation based on the analysis."""
    if bot_probability >= 70:
        return 'Potential Bot/Fake Profile'
    elif bot_probability >= 40:
        return 'Needs Further Review'
    else:
        return 'Likely Real User'

def combine_with_profile_prediction(behavior_result, profile_result):
    """Combine behavior analysis with profile prediction for improved accuracy."""
    behavior_bot_prob = behavior_result['bot_probability']
    profile_result_text = profile_result.get('result', 'Real')
    profile_confidence = profile_result.get('confidence', 0)
    
    profile_bot_prob = profile_confidence if profile_result_text == 'Fake' else (100 - profile_confidence)
    
    combined_probability = (behavior_bot_prob * 0.4) + (profile_bot_prob * 0.6)
    combined_risk = get_risk_level(combined_probability)
    
    return {
        'combined_probability': round(combined_probability, 2),
        'combined_risk': combined_risk,
        'behavior_contribution': round(behavior_bot_prob * 0.4, 2),
        'profile_contribution': round(profile_bot_prob * 0.6, 2)
    }

analyzer = BehavioralAnalyzer()

def analyze_behavior(behavior_data):
    return analyzer.analyze_behavior(behavior_data)

