
class ThreatAnalyticsEngine:
    def __init__(self):
        self.risk_levels = {
            'safe': {'min': 0, 'max': 20, 'color': '#22c55e'},
            'low': {'min': 21, 'max': 40, 'color': '#eab308'},
            'medium': {'min': 41, 'max': 60, 'color': '#f97316'},
            'high': {'min': 61, 'max': 80, 'color': '#ef4444'},
            'critical': {'min': 81, 'max': 100, 'color': '#dc2626'}
        }

    def get_risk_level(self, score):
        if score <= 20:
            return 'Safe'
        elif score <= 40:
            return 'Low Risk'
        elif score <= 60:
            return 'Medium Risk'
        elif score <= 80:
            return 'High Risk'
        else:
            return 'Critical Risk'
        
    def analyze_profile(self, username, bio, captions, links):
        threat_score = 10
        threat_categories = []
        scam_risk = 5
        phishing_risk = 5
        
        bio_lower = bio.lower()
        captions_str = ' '.join(captions).lower()
        
        scam_keywords = ['free money', 'crypto scam', 'double your money', 'giveaway', 'investment opportunity', 'verify your account']
        phishing_keywords = ['verify now', 'login', 'secure your account', 'suspicious activity', 'reset password']
        
        for keyword in scam_keywords:
            if keyword in bio_lower or keyword in captions_str:
                scam_risk += 15
                threat_score += 15
                if 'Scams' not in threat_categories:
                    threat_categories.append('Scams')
        
        for keyword in phishing_keywords:
            if keyword in bio_lower or keyword in captions_str or len(links) > 2:
                phishing_risk += 15
                threat_score += 15
                if 'Phishing' not in threat_categories:
                    threat_categories.append('Phishing')
        
        threat_score = min(100, threat_score)
        risk_level = self.get_risk_level(threat_score)
        
        return {
            'threat_score': threat_score,
            'risk_level': risk_level,
            'scam_risk': scam_risk,
            'phishing_risk': phishing_risk,
            'threat_categories': threat_categories,
            'regional_threat_distribution': [
                {'region': 'India', 'count': 5},
                {'region': 'USA', 'count': 3},
                {'region': 'UK', 'count': 1}
            ]
        }

engine = ThreatAnalyticsEngine()
