# Installation Guide

## Prerequisites

1. The main Fake Profile Detection web application must be running locally on `http://localhost:5000`
2. Google Chrome or Mozilla Firefox browser installed

## Step-by-Step Installation

### Google Chrome

1. **Download the extension files**
   - Clone or download this repository to your computer
   - Navigate to the `browser-extension/chrome/` directory

2. **Open Chrome extensions page**
   - Launch Google Chrome
   - In the address bar, type: `chrome://extensions/`
   - Press Enter

3. **Enable Developer mode**
   - Look for the "Developer mode" toggle switch in the top-right corner
   - Click to enable it (the switch will turn blue)

4. **Load the extension**
   - Click the "Load unpacked" button that appears
   - Navigate to and select the `browser-extension/chrome/` folder
   - Click "Select Folder" (Windows) or "Open" (Mac/Linux)

5. **Verify installation**
   - The extension should now appear in your extensions list
   - You'll see the Fake Profile Detector icon in your browser toolbar

### Mozilla Firefox

1. **Download the extension files**
   - Clone or download this repository to your computer
   - Navigate to the `browser-extension/firefox/` directory

2. **Open Firefox debugging page**
   - Launch Mozilla Firefox
   - In the address bar, type: `about:debugging`
   - Press Enter

3. **Load temporary add-on**
   - Click "This Firefox" in the left sidebar
   - Click the "Load Temporary Add-on" button
   - Navigate to the `browser-extension/firefox/` folder
   - Select any file (e.g., `manifest.json`) and click "Open"

4. **Verify installation**
   - The extension should now appear in the "Temporary Extensions" section
   - You'll see the Fake Profile Detector icon in your browser toolbar

## Post-Installation Setup

1. **Pin the extension** (optional but recommended)
   - Click the puzzle piece icon in your browser toolbar
   - Find "Fake Profile Detector" and click the pin icon

2. **Configure settings**
   - Click the extension icon to open the popup
   - Adjust sensitivity level as needed
   - Add any trusted accounts to the whitelist

3. **Test the extension**
   - Make sure the main Fake Profile Detection app is running on `http://localhost:5000`
   - Visit a social media profile page
   - The extension should display a risk badge

## Troubleshooting

### Extension not loading

**Chrome**:
- Make sure Developer mode is enabled
- Check that you selected the `chrome/` directory, not a parent folder
- Look for error messages on the extensions page

**Firefox**:
- Make sure you selected a file inside the `firefox/` directory
- Temporary add-ons are removed when Firefox closes - you'll need to reload it

### No badge appearing on profiles

- Verify the main app is running on `http://localhost:5000`
- Check that you're on a supported social media platform
- Refresh the page and try again
- Open the browser's developer tools (F12) and check the Console tab for errors

### API connection errors

- Ensure the main Fake Profile Detection app is running
- Check that the app is using port 5000
- Verify there are no firewall restrictions blocking localhost connections

## Updating the Extension

### Chrome

1. Make changes to the extension files
2. Go to `chrome://extensions/`
3. Find the Fake Profile Detector extension
4. Click the refresh icon

### Firefox

1. Make changes to the extension files
2. Go to `about:debugging` → "This Firefox"
3. Find the Fake Profile Detector extension
4. Click "Reload"

## Uninstalling

### Chrome

1. Go to `chrome://extensions/`
2. Find Fake Profile Detector
3. Click "Remove"
4. Confirm removal

### Firefox

1. Go to `about:addons`
2. Find Fake Profile Detector
3. Click the three-dot menu
4. Select "Remove"
5. Confirm removal

## Getting Help

If you encounter issues:
1. Check the browser's console for error messages
2. Verify all prerequisites are met
3. Ensure you're using the latest version of the extension
