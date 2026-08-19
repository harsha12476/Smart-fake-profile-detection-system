
import re
import random
from datetime import datetime

class CyberAwarenessChatbot:
    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
        self.context = {}

    def _build_knowledge_base(self):
        return {
            'greeting': {
                'patterns': [r'hello', r'hi', r'hey', r'good morning', r'good afternoon', r'good evening'],
                'responses': [
                    "Hello! I'm CyberSafe, your cyber safety assistant. How can I help you today?",
                    "Hi there! Welcome to CyberSafe. What would you like to know about cyber safety?",
                    "Hey! I'm here to help with all your cyber safety questions. What's on your mind?"
                ]
            },
            'fake_profile': {
                'patterns': [r'fake profile', r'fake account', r'fake instagram', r'fake facebook', r'stolen picture', r'stolen photo'],
                'responses': [
                    "Fake profiles are a major threat! Here are signs to watch for:\n• Few or no posts\n• Unusual follower/following ratio\n• Generic bio or no bio\n• No profile picture or stolen photo\n• Recent account creation\n\nWould you like tips on how to spot them?",
                    "Fake social media profiles often use stolen photos and have suspicious activity. Our system can help detect them!"
                ]
            },
            'phishing': {
                'patterns': [r'phishing', r'phish', r'scam email', r'fake link', r'suspicious link'],
                'responses': [
                    "Phishing attacks try to steal your information! Remember:\n• Never click links from unknown senders\n• Check URL carefully for typos\n• Don't share OTP or passwords\n• Verify sender email addresses\n\nAlways hover over links to check the real URL!",
                    "Phishing is one of the most common cyber threats. Never share sensitive information via email or messages!"
                ]
            },
            'otp_fraud': {
                'patterns': [r'otp fraud', r'otp scam', r'share otp', r'otp theft'],
                'responses': [
                    "⚠️ NEVER share your OTP with ANYONE! Banks and legitimate companies NEVER ask for OTP over phone/email!",
                    "OTP fraud is serious! Remember: OTP is for YOUR eyes only. No legitimate service will ever ask you to share it!"
                ]
            },
            'impersonation': {
                'patterns': [r'impersonation', r'pretending to be', r'fake friend', r'fake relative'],
                'responses': [
                    "Impersonation attacks are when someone pretends to be someone you know. Always verify identity through a separate channel!",
                    "If someone claims to be a friend/family asking for money, CALL THEM directly to verify!"
                ]
            },
            'financial_fraud': {
                'patterns': [r'financial fraud', r'money scam', r'investment scam', r'loan scam'],
                'responses': [
                    "Financial fraud comes in many forms: fake investments, loan scams, lottery wins. Remember: If it sounds too good to be true, it probably is!",
                    "Never invest in schemes promising guaranteed high returns. Always verify with official financial institutions!"
                ]
            },
            'password_security': {
                'patterns': [r'password', r'password security', r'strong password', r'password tips'],
                'responses': [
                    "Password security tips:\n• Use 12+ characters\n• Mix uppercase, lowercase, numbers, symbols\n• Don't reuse passwords\n• Use a password manager\n• Enable 2FA everywhere!",
                    "Strong passwords are your first line of defense! Avoid personal info like birthdays or names!"
                ]
            },
            'report_cybercrime': {
                'patterns': [r'report', r'cyber crime', r'file complaint', r'how to report', r'police report'],
                'responses': [
                    "Steps to report cybercrime in India:\n1. Visit https://cyber.gov.in\n2. Call 1930 (National Cybercrime Reporting Portal)\n3. Visit your local police station\n4. Save all evidence (screenshots, messages, emails)\n\nDo NOT delete anything!",
                    "Report immediately! Contact 1930 or visit cyber.gov.in. Preserve all digital evidence!"
                ]
            },
            'helpline': {
                'patterns': [r'helpline', r'help line', r'phone number', r'contact', r'call'],
                'responses': [
                    "Important cybercrime helplines:\n• National Cybercrime Reporting: 1930\n• Women Helpline: 181\n• Child Helpline: 1098\n• For immediate danger: 100 (Police)\n\nIn case of emergency, call 100!",
                    "For cybercrime emergencies, call 1930 immediately. It's available 24/7!"
                ]
            },
            'safety_tips': {
                'patterns': [r'safety tips', r'cyber safety', r'stay safe', r'online safety'],
                'responses': [
                    "Top cyber safety tips:\n✅ Keep software updated\n✅ Use 2FA\n✅ Be careful with public Wi-Fi\n✅ Don't overshare on social media\n✅ Verify before trusting\n✅ Regularly check privacy settings",
                    "Stay safe online! Think before you click, share, or download!"
                ]
            },
            'identity_theft': {
                'patterns': [r'identity theft', r'stolen identity', r'someone using my name'],
                'responses': [
                    "Identity theft is serious! Act fast:\n1. Report to cyber.gov.in\n2. Contact your bank\n3. Change all passwords\n4. Monitor accounts\n5. File police report",
                    "If your identity is stolen, act immediately! Contact authorities and financial institutions!"
                ]
            },
            'thanks': {
                'patterns': [r'thank', r'thanks', r'appreciate', r'grateful'],
                'responses': [
                    "You're welcome! Stay safe online!",
                    "Happy to help! Remember to practice cyber safety!",
                    "Anytime! Your digital safety matters!"
                ]
            },
            'goodbye': {
                'patterns': [r'bye', r'goodbye', r'see you', r'quit', r'exit'],
                'responses': [
                    "Goodbye! Stay safe online!",
                    "Take care! Remember to practice cyber hygiene!",
                    "See you soon! Stay protected!"
                ]
            }
        }

    def get_response(self, user_message, user_id=None):
        user_message = user_message.lower().strip()

        for intent, data in self.knowledge_base.items():
            for pattern in data['patterns']:
                if re.search(pattern, user_message, re.IGNORECASE):
                    return {
                        'response': random.choice(data['responses']),
                        'intent': intent,
                        'timestamp': datetime.now().isoformat()
                    }

        fallback_responses = [
            "I'm here to help with cyber safety! Could you please rephrase your question?",
            "That's an interesting question! Let me know more about what you need help with regarding cyber safety.",
            "I specialize in cyber safety awareness. Ask me about fake profiles, phishing, password security, or how to report cybercrime!"
        ]

        return {
            'response': random.choice(fallback_responses),
            'intent': 'fallback',
            'timestamp': datetime.now().isoformat()
        }

chatbot = CyberAwarenessChatbot()
