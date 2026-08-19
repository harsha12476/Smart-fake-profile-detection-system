# Smart Fake Profile Detection - Browser Extensions

Cross-browser extensions for Google Chrome and Mozilla Firefox that provide real-time fake profile detection on social media platforms.

## Features

- **Real-time Detection**: Analyze profiles as you browse social media
- **Multi-platform Support**: Works with Facebook, Twitter/X, Instagram, and LinkedIn
- **Visual Indicators**: Red/yellow/green badges showing risk levels
- **Customizable Settings**: Adjust detection sensitivity
- **Whitelist**: Mark verified accounts as safe
- **Dashboard Integration**: Connects to your local Fake Profile Detection system

## Installation

### Google Chrome

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right corner
3. Click "Load unpacked" and select the `chrome` directory from this project
4. The extension will appear in your extensions list

### Mozilla Firefox

1. Open Firefox and navigate to `about:debugging`
2. Click "This Firefox"
3. Click "Load Temporary Add-on"
4. Select any file in the `firefox` directory (e.g., `manifest.json`)
5. The extension will be loaded temporarily

## File Structure

```
browser-extension/
├── chrome/          # Chrome extension files
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── content.css
│   ├── popup.html
│   ├── popup.js
│   ├── popup.css
│   └── icons/
├── firefox/         # Firefox extension files
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── content.css
│   ├── popup.html
│   ├── popup.js
│   ├── popup.css
│   └── icons/
├── shared/          # Shared source files
│   ├── api.js
│   ├── background.js
│   ├── content.js
│   ├── content.css
│   ├── popup.html
│   ├── popup.js
│   └── popup.css
├── README.md
├── INSTALLATION.md
└── PRIVACY.md
```

## Usage

1. Make sure your local Fake Profile Detection system is running on `http://localhost:5000`
2. Browse any supported social media platform
3. The extension will automatically analyze profiles and display risk indicators
4. Click the extension icon to access settings and the dashboard

## Configuration

- **Sensitivity**: Low/Medium/High detection thresholds
- **Whitelist**: Add usernames you trust to avoid false positives
- **Toggle**: Enable/disable the extension completely

## Privacy

All processing happens locally in your browser or on your own server. No data is sent to third parties. See [PRIVACY.md](PRIVACY.md) for more details.

## Development

To modify the extension:
1. Edit files in the `shared/` directory
2. Copy changes to both `chrome/` and `firefox/` directories
3. Reload the extension in your browser

## License

MIT License
