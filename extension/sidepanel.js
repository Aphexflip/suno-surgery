// Suno Surgery — side panel: full editor, same prompt builder as the
// content script and popup. Saves to chrome.storage.local only.
const KEY = "sunoSurgeryIssues";
const $ = (id) => document.getElementById(id);
const status = (m) => { $("status").textContent = m; };

function parseTime(v) {
  if (v == null || v === "") return null;
  if (/^\d+(\.\d+)?$/.test(v.trim())) return parseFloat(v);
  const m = v.trim().match(/^(\d+):(\d{1,2}(\.\d+)?)$/);
  return m ? parseInt(m[1], 10) * 60 + parseFloat(m[2]) : null;
}
async function load() { const o = await chrome.storage.local.get(KEY); return o[KEY] || []; }
async function saveAll(list) { await chrome.storage.local.set({ [KEY]: list }); }

function collect() {
  return {
    title: $("title").value.trim() || "Untitled Suno song",
    startSeconds: parseTime($("start").value),
    endSeconds: parseTime($("end").value),
    problem: $("problem").value.trim(),
    desired: $("desired").value.trim(),
    replacementLyrics: $("lyrics").value.trim(),
  };
}

async function refreshList() {
  const issues = await load();
  $("count").textContent = issues.length;
  const box = $("issues"); box.innerHTML = "";
  issues.forEach((it, i) => {
    const b = document.createElement("button");
    b.className = "issue";
    b.textContent = `${i + 1}. ${it.title} — ${formatTime(it.startSeconds)}–${formatTime(it.endSeconds)} — ${it.problem || "no note"}`;
    b.onclick = () => { $("output").textContent = buildReplacePrompt(it); };
    box.appendChild(b);
  });
}

async function askNow() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url || !tab.url.includes("suno.com")) { status("Open a suno.com tab first."); return null; }
  try { return await chrome.tabs.sendMessage(tab.id, { type: "sunoSurgery:now" }); }
  catch { status("Reload the Suno tab once after installing, then try again."); return null; }
}

$("now").onclick = async () => {
  const res = await askNow();
  if (res && res.currentTime != null) {
    if (res.title) $("title").value = res.title;
    status(`Playback is at ${formatTime(res.currentTime)}.`);
  }
};
$("mark-start").onclick = async () => {
  const res = await askNow();
  if (res && res.currentTime != null) { $("start").value = formatTime(res.currentTime); status(`Start marked at ${formatTime(res.currentTime)}.`); }
};
$("mark-end").onclick = async () => {
  const res = await askNow();
  if (res && res.currentTime != null) { $("end").value = formatTime(res.currentTime); status(`End marked at ${formatTime(res.currentTime)}.`); }
};
$("generate").onclick = () => {
  const it = collect();
  if (it.startSeconds == null || it.endSeconds == null) return status("Need a start and an end time first.");
  if (it.endSeconds <= it.startSeconds) return status("End must be after start.");
  $("output").textContent = buildReplacePrompt(it);
  status("Prompt ready.");
};
$("save").onclick = async () => {
  const it = collect();
  if (it.startSeconds == null || it.endSeconds == null) return status("Need a start and an end time first.");
  const list = await load();
  list.push({ ...it, id: Date.now().toString(36), savedAt: new Date().toISOString() });
  await saveAll(list); refreshList(); status(`Saved issue #${list.length} locally.`);
};
$("copy").onclick = async () => {
  const brief = $("output").textContent;
  if (!brief || brief.startsWith("Mark a slice")) return status("Generate a brief first.");
  try { await navigator.clipboard.writeText(brief); status("Copied editing brief (NOT lyrics)."); }
  catch { status("Copy failed; select the brief manually."); }
};
$("copy-lyrics").onclick = async () => {
  const lyrics = $("lyrics").value.trim();
  if (!lyrics) return status("No replacement lyrics entered.");
  try { await navigator.clipboard.writeText(lyrics); status("Copied ONLY replacement lyrics."); }
  catch { status("Copy failed; select the lyrics manually."); }
};
refreshList();
