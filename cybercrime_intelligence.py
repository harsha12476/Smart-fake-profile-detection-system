
import random
from datetime import datetime

class CybercrimeIntelligenceEngine:
    def __init__(self):
        self.risk_levels = {
            'safe': {'min': 0, 'max': 20, 'color': '#22c55e', 'label': 'SAFE'},
            'low': {'min': 21, 'max': 40, 'color': '#eab308', 'label': 'LOW'},
            'medium': {'min': 41, 'max': 60, 'color': '#f97316', 'label': 'MEDIUM'},
            'high': {'min': 61, 'max': 80, 'color': '#ef4444', 'label': 'HIGH'},
            'critical': {'min': 81, 'max': 100, 'color': '#dc2626', 'label': 'CRITICAL'}
        }
        
        self.phishing_keywords = [
            'login', 'verify', 'confirm', 'account', 'password', 'update', 
            'secure', 'bank', 'credit', 'verify your', 'confirm your', 
            'update your', 'secure your', 'reset', 'recovery', 'validate'
        ]
        
        self.financial_scam_keywords = [
            'investment', 'profit', 'crypto', 'bitcoin', 'ethereum', 'doubling', 
            'lottery', 'giveaway', 'earn money', 'get rich', 'guaranteed', 
            'free money', 'double your', 'investment opportunity', 'scheme'
        ]
        
        self.impersonation_keywords = [
            'official', 'verified', 'support', 'admin', 'ceo', 'celebrity', 
            'influencer', 'brand', 'real', 'authentic', 'team', 'official account'
        ]
        
        self.malware_keywords = [
            'download', 'install', 'apk', 'exe', 'file', 'software', 
            'tool', 'app', 'free download', 'click here', 'get it now'
        ]
        
        self.social_engineering_keywords = [
            'urgent', 'hurry', 'limited time', 'only today', 'act now', 
            'important', 'critical', 'alert', 'warning', 'don\'t miss', 
            'last chance', 'exclusive', 'secret', 'private'
        ]

    def detect_phishing(self, username, bio, captions, links):
        score = 0
        indicators = []
        
        text_content = (username + ' ' + bio + ' ' + ' '.join(captions)).lower()
        
        for keyword in self.phishing_keywords:
            if keyword in text_content:
                score += 15
                indicators.append(f'Phishing keyword found: \"{keyword}\"')
                
        if links:
            for link in links:
                if any(suspicious in link.lower() for suspicious in ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'verify']):
                    score += 20
                    indicators.append('Suspicious short URL detected')
                if 'login' in link.lower() or 'verify' in link.lower():
                    score += 25
                    indicators.append('Possible fake login/verify link')
                    
        return min(score, 100), indicators
    
    def detect_financial_scam(self, username, bio, captions):
        score = 0
        indicators = []
        
        text_content = (username + ' ' + bio + ' ' + ' '.join(captions)).lower()
        
        for keyword in self.financial_scam_keywords:
            if keyword in text_content:
                score += 15
                indicators.append(f'Financial scam keyword: \"{keyword}\"')
                
        if 'profit' in text_content and ('guaranteed' in text_content or 'double' in text_content):
            score += 25
            indicators.append('Guaranteed profit/doubling scam indicators')
            
        return min(score, 100), indicators
    
    def detect_identity_theft(self, username, bio):
        score = 0
        indicators = []
        
        text_content = (username + ' ' + bio).lower()
        
        for keyword in self.impersonation_keywords:
            if keyword in text_content:
                score += 15
                indicators.append(f'Impersonation keyword: \"{keyword}\"')
                
        if any(mark in username for mark in ['_official', '.official', '-official', 'verified', 'real']):
            score += 20
            indicators.append('Username suggests impersonation attempt')
            
        return min(score, 100), indicators
    
    def detect_malware(self, links, captions):
        score = 0
        indicators = []
        
        text_content = ' '.join(captions).lower()
        
        for keyword in self.malware_keywords:
            if keyword in text_content:
                score += 15
                indicators.append(f'Malware keyword found: \"{keyword}\"')
                
        if links:
            for link in links:
                if any(ext in link.lower() for ext in ['.apk', '.exe', '.zip', '.rar', '.bat']):
                    score += 25
                    indicators.append('Potentially malicious file link detected')
                    
        return min(score, 100), indicators
    
    def detect_social_engineering(self, bio, captions):
        score = 0
        indicators = []
        
        text_content = (bio + ' ' + ' '.join(captions)).lower()
        
        for keyword in self.social_engineering_keywords:
            if keyword in text_content:
                score += 12
                indicators.append(f'Social engineering tactic: \"{keyword}\"')
                
        return min(score, 100), indicators

    def get_risk_level(self, score):
        for level, details in self.risk_levels.items():
            if details['min'] <= score <= details['max']:
                return details['label'], details['color']
        return 'SAFE', '#22c55e'

    def analyze_profile(self, username, bio, captions=None, links=None):
        if captions is None:
            captions = []
        if links is None:
            links = []

        phishing_score, phishing_indicators = self.detect_phishing(username, bio, captions, links)
        financial_score, financial_indicators = self.detect_financial_scam(username, bio, captions)
        identity_score, identity_indicators = self.detect_identity_theft(username, bio)
        malware_score, malware_indicators = self.detect_malware(links, captions)
        se_score, se_indicators = self.detect_social_engineering(bio, captions)
        
        overall_score = (
            phishing_score * 0.25 +
            financial_score * 0.25 +
            identity_score * 0.2 +
            malware_score * 0.15 +
            se_score * 0.15
        )
        overall_score = round(overall_score, 0)
        
        threat_level, risk_color = self.get_risk_level(overall_score)
        
        all_indicators = []
        all_indicators.extend(phishing_indicators)
        all_indicators.extend(financial_indicators)
        all_indicators.extend(identity_indicators)
        all_indicators.extend(malware_indicators)
        all_indicators.extend(se_indicators)
        
        categories = []
        if phishing_score > 30:
            categories.append('Phishing Attack')
        if financial_score > 30:
            categories.append('Financial Scam')
        if identity_score > 30:
            categories.append('Identity Theft')
        if malware_score > 30:
            categories.append('Malware Distribution')
        if se_score > 30:
            categories.append('Social Engineering')
            
        final_result = 'Low-Risk Profile'
        if overall_score > 80:
            final_result = 'High-Risk Cybercrime Profile Detected'
        elif overall_score > 60:
            final_result = 'Medium-Risk Profile - Monitor Activity'
        elif overall_score > 40:
            final_result = 'Low-Medium Risk - Review Profile'
            
        ai_confidence = min(90 + round(random.uniform(-5, 5)), 99)
        
        recommended_action = 'No Action Needed'
        if overall_score > 80:
            recommended_action = 'Immediate Investigation and Account Flagging'
        elif overall_score > 60:
            recommended_action = 'Monitor Account and Report if Necessary'
        elif overall_score > 40:
            recommended_action = 'Review Profile Carefully'
            
        report = {
            'username': username,
            'threat_intelligence_score': int(overall_score),
            'threat_level': threat_level,
            'risk_color': risk_color,
            'phishing_score': phishing_score,
            'financial_scam_score': financial_score,
            'identity_theft_score': identity_score,
            'malware_score': malware_score,
            'social_engineering_score': se_score,
            'detected_threats': all_indicators,
            'threat_categories': categories,
            'ai_confidence_score': ai_confidence,
            'recommended_action': recommended_action,
            'final_result': final_result,
            'created_at': datetime.now()
        }
        
        return report


engine = CybercrimeIntelligenceEngine()
