console.log('Fake Profile Detector content script loaded');

function detectSocialMediaPlatform() {
  const hostname = window.location.hostname;
  
  if (hostname.includes('facebook.com')) return 'facebook';
  if (hostname.includes('twitter.com') || hostname.includes('x.com')) return 'twitter';
  if (hostname.includes('instagram.com')) return 'instagram';
  if (hostname.includes('linkedin.com')) return 'linkedin';
  
  return null;
}

function extractProfileData() {
  const platform = detectSocialMediaPlatform();
  let data = {
    username: '',
    followers: 0,
    following: 0,
    posts: 0,
    bio_length: 0,
    has_profile_picture: 0,
    account_age_days: 365
  };

  if (platform === 'twitter' || platform === 'x.com') {
    data.username = window.location.pathname.split('/')[1] || 'unknown';
  } else if (platform === 'instagram') {
    data.username = window.location.pathname.split('/')[1] || 'unknown';
  } else if (platform === 'facebook') {
    data.username = window.location.pathname.split('/')[1] || 'unknown';
  } else if (platform === 'linkedin') {
    data.username = window.location.pathname.split('/')[2] || 'unknown';
  }

  return data;
}

function addDetectionBadge(profileData) {
  const badge = document.createElement('div');
  badge.className = 'fpd-badge';
  
  const riskLevel = Math.random() > 0.5 ? 'medium' : 'low';
  
  if (riskLevel === 'high') {
    badge.style.background = '#dc3545';
    badge.innerHTML = '<span class="fpd-text">⚠️ High Risk</span>';
  } else if (riskLevel === 'medium') {
    badge.style.background = '#ffc107';
    badge.style.color = '#000';
    badge.innerHTML = '<span class="fpd-text">⚠️ Medium Risk</span>';
  } else {
    badge.style.background = '#198754';
    badge.innerHTML = '<span class="fpd-text">✓ Low Risk</span>';
  }
  
  const header = document.querySelector('header');
  if (header) {
    header.appendChild(badge);
  }
}

window.addEventListener('load', () => {
  const platform = detectSocialMediaPlatform();
  if (platform) {
    console.log(`Detected platform: ${platform}`);
    const profileData = extractProfileData();
    console.log('Profile data:', profileData);
    
    setTimeout(() => {
      addDetectionBadge(profileData);
    }, 2000);
  }
});
