
# Fake Profile Detector - Mobile Application

## Overview
A cross-platform mobile application (Android &amp; iOS) for the Smart Fake Profile Detection System. Built with Flutter.

## Features

### 1. Instagram Profile Scanning
- Username search
- Profile URL scanning
- QR code scanning
- Automatic fake profile analysis

### 2. Real-Time Alerts
- Fake profile detection alerts
- Scam account warnings
- Phishing threat notifications
- Critical security alerts

### 3. Mobile Dashboard
- Profiles analyzed count
- Fake profiles detected count
- Risk scores display
- Threat trends
- Recent scans history

### 4. Secure Login
- Email/password authentication
- 2FA support
- Biometric authentication (Fingerprint/Face ID)
- Secure session management

## Technologies Used
- Flutter
- Dart
- Python Flask Backend
- MongoDB
- Firebase Cloud Messaging (FCM)
- REST APIs
- Provider for state management

## Getting Started

### Prerequisites
- Flutter SDK 3.0+
- Android Studio or VS Code
- Xcode (for iOS development)
- Python backend running

### Installation
1. Clone the repository
2. Navigate to mobile_app directory:
   ```bash
   cd mobile_app
   ```
3. Install dependencies:
   ```bash
   flutter pub get
   ```
4. Update API base URL in `lib/services/api_service.dart`
5. Run the app:
   ```bash
   flutter run
   ```

## Backend Integration
Ensure your Flask backend is running at the configured URL. The app uses these endpoints:
- `/login` - User authentication
- `/analyze-profile` - Fake profile analysis
- `/api/analyze-fake-followers` - Fake follower detection
- `/api/analyze-cybercrime` - Cybercrime intelligence

## Project Structure
```
mobile_app/
├── lib/
│   ├── main.dart
│   ├── services/
│   │   └── api_service.dart
│   └── screens/
│       ├── login_screen.dart
│       ├── dashboard_screen.dart
│       └── scan_screen.dart
└── pubspec.yaml
```

## Future Enhancements
- Two-factor authentication
- Biometric login integration
- Push notifications
- Offline analysis cache
- Profile comparison
- Bulk scanning
