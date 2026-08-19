
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatAlertSystem:
    def __init__(self):
        self.alerts: List[Dict] = []
        self.threat_thresholds = {
            "CRITICAL": 90,
            "HIGH": 70,
            "MEDIUM": 50,
            "LOW": 30
        }
        self.threat_types = [
            "Fake Profiles", 
            "Phishing Attacks", 
            "Online Scams", 
            "Fake Giveaways", 
            "Crypto Frauds", 
            "Malware Campaigns", 
            "Bot Networks", 
            "Impersonation Accounts"
        ]

    def generate_threat_alert(
        self,
        username: str,
        risk_score: int,
        threat_type: str,
        detection_reasons: List[str],
        profile_data: Optional[Dict] = None
    ) -> Dict:
        """Generate a comprehensive threat alert"""
        risk_level = self._determine_risk_level(risk_score)
        
        alert = {
            "id": len(self.alerts) + 1,
            "username": username,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "threat_type": threat_type,
            "detection_reasons": detection_reasons,
            "detection_time": datetime.now().isoformat(),
            "status": "PENDING",
            "alert_status": {
                "email_sent": False,
                "sms_sent": False,
                "dashboard_alert": True
            },
            "profile_data": profile_data or {}
        }
        
        self.alerts.append(alert)
        logger.info(f"Threat alert generated for {username}: {risk_level} ({risk_score}%)")
        
        return alert

    def _determine_risk_level(self, risk_score: int) -> str:
        if risk_score >= self.threat_thresholds["CRITICAL"]:
            return "CRITICAL"
        elif risk_score >= self.threat_thresholds["HIGH"]:
            return "HIGH"
        elif risk_score >= self.threat_thresholds["MEDIUM"]:
            return "MEDIUM"
        elif risk_score >= self.threat_thresholds["LOW"]:
            return "LOW"
        else:
            return "SAFE"

    def send_email_alert(self, alert: Dict, admin_email: str = "admin@example.com") -> bool:
        """Simulate sending an email alert"""
        try:
            logger.info(f"[SIMULATION] Sending email alert to {admin_email}")
            logger.info(f"Subject: CRITICAL THREAT ALERT: {alert['username']}")
            logger.info(f"Body:\n{self._format_email_body(alert)}")
            alert["alert_status"]["email_sent"] = True
            return True
        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")
            return False

    def send_sms_alert(self, alert: Dict, admin_phone: str = "+1234567890") -> bool:
        """Simulate sending an SMS alert"""
        try:
            logger.info(f"[SIMULATION] Sending SMS alert to {admin_phone}")
            logger.info(f"Message: {self._format_sms_message(alert)}")
            alert["alert_status"]["sms_sent"] = True
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS alert: {str(e)}")
            return False

    def _format_email_body(self, alert: Dict) -> str:
        reasons_list = "\n".join([f"  • {reason}" for reason in alert["detection_reasons"]])
        
        return f"""
================================================================================
                            THREAT ALERT REPORT
================================================================================

Profile Username: {alert['username']}
Threat Level:     {alert['risk_level']}
Risk Score:       {alert['risk_score']}%
Threat Type:      {alert['threat_type']}
Detection Time:   {alert['detection_time']}

Detection Reasons:
{reasons_list}

Alert Status:
  • Dashboard Alert Generated: {'✅' if alert['alert_status']['dashboard_alert'] else '❌'}
  • Email Sent: {'✅' if alert['alert_status']['email_sent'] else '❌'}
  • SMS Sent: {'✅' if alert['alert_status']['sms_sent'] else '❌'}

RECOMMENDED ACTION: Immediate Investigation Required

================================================================================
        """.strip()

    def _format_sms_message(self, alert: Dict) -> str:
        return f"[FPDS ALERT] CRITICAL: {alert['username']} (Score: {alert['risk_score']}%) - {alert['threat_type']}. Investigate immediately!"

    def get_all_alerts(self) -> List[Dict]:
        return self.alerts

    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        return self.alerts[-limit:]

    def get_critical_alerts(self) -> List[Dict]:
        return [alert for alert in self.alerts if alert["risk_level"] == "CRITICAL"]

    def update_alert_status(self, alert_id: int, new_status: str) -> bool:
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["status"] = new_status
                logger.info(f"Updated alert {alert_id} to status: {new_status}")
                return True
        return False

# Initialize global alert system instance
alert_system = ThreatAlertSystem()
