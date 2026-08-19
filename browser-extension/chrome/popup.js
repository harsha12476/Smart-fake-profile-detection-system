document.addEventListener('DOMContentLoaded', () => {
    const toggleExtension = document.getElementById('toggleExtension');
    const sensitivity = document.getElementById('sensitivity');
    const addWhitelist = document.getElementById('addWhitelist');
    
    chrome.storage.sync.get(['enabled', 'sensitivity', 'whitelist'], (result) => {
        toggleExtension.checked = result.enabled !== false;
        if (result.sensitivity) {
            sensitivity.value = result.sensitivity;
        }
        updateWhitelist(result.whitelist || []);
    });
    
    toggleExtension.addEventListener('change', (e) => {
        chrome.storage.sync.set({ enabled: e.target.checked });
    });
    
    sensitivity.addEventListener('change', (e) => {
        chrome.storage.sync.set({ sensitivity: e.target.value });
    });
    
    addWhitelist.addEventListener('click', () => {
        const username = prompt('Enter username to whitelist:');
        if (username) {
            chrome.storage.sync.get(['whitelist'], (result) => {
                const whitelist = result.whitelist || [];
                if (!whitelist.includes(username)) {
                    whitelist.push(username);
                    chrome.storage.sync.set({ whitelist });
                    updateWhitelist(whitelist);
                }
            });
        }
    });
});

function updateWhitelist(whitelist) {
    const whitelistDiv = document.getElementById('whitelist');
    if (whitelist.length === 0) {
        whitelistDiv.innerHTML = '<p class="text-muted small mb-0">No accounts whitelisted</p>';
    } else {
        whitelistDiv.innerHTML = whitelist.map(username => `
            <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="small">@${username}</span>
                <button class="btn btn-sm btn-outline-danger remove-whitelist" data-username="${username}">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        `).join('');
        
        document.querySelectorAll('.remove-whitelist').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const username = e.target.closest('.remove-whitelist').dataset.username;
                chrome.storage.sync.get(['whitelist'], (result) => {
                    const whitelist = (result.whitelist || []).filter(u => u !== username);
                    chrome.storage.sync.set({ whitelist });
                    updateWhitelist(whitelist);
                });
            });
        });
    }
}
