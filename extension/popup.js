// Suno Surgery — popup: list saved issues, show/copy their prompt.
const KEY = "sunoSurgeryIssues";
const $ = (id) => document.getElementById(id);

async function load() {
  const out = await chrome.storage.local.get(KEY);
  return out[KEY] || [];
}

function render(issues) {
  $("count").textContent = issues.length;
  const box = $("issues");
  box.innerHTML = "";
  if (!issues.length) { box.innerHTML = "<p class='muted'>No issues saved yet. Open a Suno tab and use the floating panel.</p>"; return; }
  issues.forEach((it, i) => {
    const b = document.createElement("button");
    b.className = "issue";
    b.textContent = `${i + 1}. ${it.title || "Untitled"} — ${formatTime(it.startSeconds)}–${formatTime(it.endSeconds)} — ${it.problem || "no note"}`;
    b.onclick = () => { $("output").textContent = buildReplacePrompt(it); };
    box.appendChild(b);
  });
}

async function refresh() {
  const issues = await load();
  render(issues);
  if (issues.length) $("output").textContent = buildReplacePrompt(issues[issues.length - 1]);
  // Ask the active Suno tab where playback is, if any.
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.url && tab.url.includes("suno.com")) {
      const res = await chrome.tabs.sendMessage(tab.id, { type: "sunoSurgery:now" });
      if (res && res.currentTime != null) $("now").textContent = `Now playing: ${res.title || ""} — ${formatTime(res.currentTime)}`;
    }
  } catch { /* content script not on this tab — fine */ }
}

$("refresh").onclick = refresh;
$("open-panel").onclick = async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab && tab.id) { await chrome.sidePanel.open({ tabId: tab.id }); window.close(); }
};
$("copy").onclick = async () => { await navigator.clipboard.writeText($("output").textContent); };
$("clear").onclick = async () => {
  if (confirm("Delete all locally saved Suno Surgery issues?")) {
    await chrome.storage.local.remove(KEY); refresh();
  }
};
refresh();
