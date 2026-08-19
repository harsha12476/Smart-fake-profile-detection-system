chrome.runtime.onInstalled.addListener(() => {
  console.log('Fake Profile Detector extension installed');
  chrome.storage.sync.set({
    enabled: true,
    sensitivity: 'medium',
    whitelist: []
  });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'checkProfile') {
    checkProfile(request.data).then(result => {
      sendResponse(result);
    });
    return true;
  }
});

async function checkProfile(profileData) {
  try {
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams(profileData)
    });
    
    if (!response.ok) {
      throw new Error('API request failed');
    }
    
    return { success: true, data: profileData };
  } catch (error) {
    console.error('Error checking profile:', error);
    return { success: false, error: error.message };
  }
}
