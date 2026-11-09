// Suno Surgery — background service worker (MV3).
// Minimal: opens the side panel when the toolbar icon is clicked.
// No network calls, no Suno API, no login. All data stays in
// chrome.storage.local on the user's own machine.
chrome.action.onClicked.addListener((tab) => {
  if (tab && tab.id) chrome.sidePanel.open({ tabId: tab.id }).catch((err) => console.error("Suno Surgery side panel failed to open:", err));
});
