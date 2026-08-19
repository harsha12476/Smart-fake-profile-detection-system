from flask_mail import Message
from datetime import datetime

def send_fake_profile_alert(mail, prediction_data, notification_email, threshold):
    if prediction_data['result'] == 'Fake' and prediction_data['confidence'] >= threshold:
        try:
            msg = Message(
                subject=f"⚠️ HIGH RISK: Fake Profile Detected - {prediction_data['username']}",
                recipients=[notification_email],
                html=f"""
                <html>
                    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <div style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; font-size: 24px;">⚠️ Fake Profile Alert</h1>
                        </div>
                        <div style="padding: 20px; border: 1px solid #e9ecef; border-top: none; border-radius: 0 0 8px 8px;">
                            <h2 style="color: #333;">Suspicious Profile Detected</h2>
                            <p>A highly suspicious fake profile has been detected with <strong>{prediction_data['confidence']}%</strong> confidence.</p>
                            
                            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                                <h3 style="color: #495057; margin-top: 0;">Profile Details:</h3>
                                <table style="width: 100%;">
                                    <tr>
                                        <td style="padding: 8px 0;"><strong>Username:</strong></td>
                                        <td style="padding: 8px 0;">{prediction_data['username']}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;"><strong>Followers:</strong></td>
                                        <td style="padding: 8px 0;">{prediction_data['followers']}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;"><strong>Following:</strong></td>
                                        <td style="padding: 8px 0;">{prediction_data['following']}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;"><strong>Posts:</strong></td>
                                        <td style="padding: 8px 0;">{prediction_data['posts']}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;"><strong>Account Age:</strong></td>
                                        <td style="padding: 8px 0;">{prediction_data['account_age_days']} days</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;"><strong>Detected By:</strong></td>
                                        <td style="padding: 8px 0;">{prediction_data['user_name']}</td>
                                    </tr>
                                </table>
                            </div>
                            
                            <p style="text-align: center; color: #6c757d; font-size: 12px; margin-top: 20px;">
                                This is an automated alert from your Fake Profile Detection System.<br>
                                Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                            </p>
                        </div>
                    </body>
                </html>
                """
            )
            mail.send(msg)
            print(f"Alert email sent for profile: {prediction_data['username']}")
            return True
        except Exception as e:
            print(f"Failed to send email alert: {str(e)}")
            return False
    return False
