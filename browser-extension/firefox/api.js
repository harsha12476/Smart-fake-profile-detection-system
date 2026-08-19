const API_BASE_URL = 'http://localhost:5000';

async function detectProfile(profileData) {
  try {
    const response = await fetch(`${API_BASE_URL}/detect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(profileData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error detecting profile:', error);
    return null;
  }
}

function getRiskLevel(confidence, result) {
  if (result === 'Fake') {
    if (confidence >= 90) return 'high';
    if (confidence >= 70) return 'medium';
    return 'low';
  }
  return 'safe';
}
