
import random
from datetime import datetime
from collections import defaultdict


class FakeFollowerDetectionEngine:
    def __init__(self):
        self.risk_levels = {
            'safe': {'min': 0, 'max': 20, 'color': '#22c55e'},
            'low': {'min': 21, 'max': 40, 'color': '#eab308'},
            'medium': {'min': 41, 'max': 60, 'color': '#f97316'},
            'high': {'min': 61, 'max': 80, 'color': '#ef4444'},
            'critical': {'min': 81, 'max': 100, 'color': '#dc2626'}
        }

    def calculate_purchased_follower_probability(self, followers, following, avg_likes, avg_comments, account_age_days):
        score = 0
        reasons = []

        # Sudden follower spike indicator
        engagement_rate = (avg_likes / followers) * 100 if followers > 0 else 0

        if followers > 10000 and avg_likes < 200:
            score += 25
            reasons.append("Large follower count with very low average likes")

        if engagement_rate < 0.5:
            score += 30
            reasons.append("Extremely low engagement rate")

        if followers > 5000 and following > 2000:
            score += 15
            reasons.append("Unusual follower/following ratio")

        if avg_comments < 10 and followers > 10000:
            score += 20
            reasons.append("Very low comment volume relative to follower count")

        if account_age_days < 365 and followers > 20000:
            score += 10
            reasons.append("Rapid follower growth for a new account")

        return min(score, 100), reasons

    def calculate_engagement_fraud_score(self, avg_likes, avg_comments, followers):
        score = 0
        reasons = []

        engagement_rate = (avg_likes / followers) * 100 if followers > 0 else 0
        comment_ratio = avg_comments / avg_likes if avg_likes > 0 else 0

        if engagement_rate > 0 and engagement_rate < 0.3:
            score += 25
            reasons.append("Abnormally low engagement rate")

        if avg_comments < 5 and followers > 5000:
            score += 20
            reasons.append("Minimal comment activity")

        if comment_ratio < 0.02:
            score += 15
            reasons.append("Unusually low comment-to-like ratio")

        if avg_likes > 100 and avg_likes % 10 == 0:
            score += 10
            reasons.append("Round number likes (indicates bot activity)")

        return min(score, 100), reasons

    def calculate_growth_manipulation_score(self, followers, account_age_days, avg_likes):
        score = 0
        reasons = []

        avg_daily_growth = followers / account_age_days if account_age_days > 0 else 0

        if avg_daily_growth > 100:
            score += 30
            reasons.append("Unnatural daily follower growth rate")

        if followers > 50000 and account_age_days < 365:
            score += 25
            reasons.append("Extremely rapid growth over short period")

        if avg_likes < 100 and followers > 10000:
            score += 20
            reasons.append("No corresponding engagement growth with follower growth")

        return min(score, 100), reasons

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

    def get_risk_color(self, score):
        for level, details in self.risk_levels.items():
            if details['min'] <= score <= details['max']:
                return details['color']
        return '#22c55e'

    def analyze_profile(self, username, followers, following, avg_likes, avg_comments, account_age_days):
        purchased_probability, purchased_reasons = self.calculate_purchased_follower_probability(
            followers, following, avg_likes, avg_comments, account_age_days
        )
        engagement_fraud, engagement_reasons = self.calculate_engagement_fraud_score(
            avg_likes, avg_comments, followers
        )
        growth_manipulation, growth_reasons = self.calculate_growth_manipulation_score(
            followers, account_age_days, avg_likes
        )

        overall_risk = (purchased_probability + engagement_fraud + growth_manipulation) / 3

        all_reasons = purchased_reasons + engagement_reasons + growth_reasons

        engagement_rate = (avg_likes / followers) * 100 if followers > 0 else 0

        final_result = "No Fake Follower Marketplace Activity Detected"
        if overall_risk > 80:
            final_result = "Potential Fake Follower Marketplace Activity Detected"
        elif overall_risk > 60:
            final_result = "Suspicious Activity Indicated"
        elif overall_risk > 40:
            final_result = "Some Unusual Patterns Detected"

        report = {
            'username': username,
            'followers': followers,
            'following': following,
            'avg_likes': avg_likes,
            'avg_comments': avg_comments,
            'engagement_rate': round(engagement_rate, 2),
            'account_age_days': account_age_days,
            'purchased_follower_probability': purchased_probability,
            'engagement_fraud_score': engagement_fraud,
            'growth_manipulation_score': growth_manipulation,
            'overall_risk_score': round(overall_risk, 1),
            'risk_level': self.get_risk_level(overall_risk),
            'risk_color': self.get_risk_color(overall_risk),
            'all_reasons': all_reasons,
            'final_result': final_result,
            'created_at': datetime.now()
        }

        return report


engine = FakeFollowerDetectionEngine()

