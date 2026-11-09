// Suno Surgery — content script, runs on suno.com only.
// What it does:
//  - Finds the <audio> element Suno is playing and reads its currentTime.
//  - Shows a small floating panel: "Mark start" / "Mark end" while the
//    song plays, plus fields for what's wrong and what should change.
//  - Generates the Replace Section prompt (shared/prompt.js) and copies it.
//  - Saves issues to chrome.storage.local. Nothing leaves the browser.
// What it does NOT do:
//  - No login, no session cookie, no Suno API call, no scraping of
//    credentials, no downloading or uploading audio. Suno's player DOM
//    changes often, so time capture falls back to manual entry if no
//    <audio> element is found — the panel always works by typing times.

(() => {
  if (window.__sunoSurgeryLoaded) return;
  window.__sunoSurgeryLoaded = true;

  const STORE_KEY = "sunoSurgeryIssues";

  function currentAudioTime() {
    const audios = [...document.querySelectorAll("audio")];
    const playing = audios.find((a) => !a.paused && !a.ended);
    const el = playing || audios[0];
    return el ? el.currentTime : null;
  }

  function songTitle() {
    // Best effort only — the user can edit the title in the panel.
    const h = document.querySelector("h1");
    return h ? h.textContent.trim().slice(0, 120) : "Untitled Suno song";
  }

  async function loadIssues() {
    const out = await chrome.storage.local.get(STORE_KEY);
    return out[STORE_KEY] || [];
  }
  async function saveIssues(issues) {
    await chrome.storage.local.set({ [STORE_KEY]: issues });
  }

  function buildPanel() {
    const panel = document.createElement("div");
    panel.id = "suno-surgery-panel";
    panel.innerHTML = `
      <div class="ss-head"><strong>Suno Surgery</strong><span>local only · no login</span><button id="ss-close" title="Hide panel">×</button></div>
      <div class="ss-row"><label>Song</label><input id="ss-title" type="text" placeholder="Song title"></div>
      <div class="ss-row ss-times">
        <label>Start <input id="ss-start" type="text" inputmode="decimal" placeholder="0:42"></label>
        <label>End <input id="ss-end" type="text" inputmode="decimal" placeholder="0:58"></label>
        <button id="ss-mark-start" type="button">Mark start ▶</button>
        <button id="ss-mark-end" type="button">Mark end ▶</button>
      </div>
      <div class="ss-row"><label>What's wrong?</label><input id="ss-problem" type="text" placeholder="e.g. vocal says 'away' not 'awake'"></div>
      <div class="ss-row"><label>What should change?</label><input id="ss-desired" type="text" placeholder="e.g. sing 'awake', same melody"></div>
      <div class="ss-row"><label>Replacement lyrics (this section only)</label><textarea id="ss-lyrics" rows="2" placeholder="optional"></textarea></div>
      <div class="ss-row ss-actions">
        <button id="ss-generate" type="button" class="primary">Generate prompt</button>
        <button id="ss-copy" type="button">Copy editing brief</button>
        <button id="ss-copy-lyrics" type="button">Copy lyrics only</button>
        <button id="ss-save" type="button">Save issue</button>
      </div>
      <pre id="ss-output" class="ss-output">Mark a slice while the song plays, or type the times.</pre>
      <div id="ss-status" class="ss-status"></div>`;
    document.body.appendChild(panel);

    const $ = (id) => panel.querySelector(id);
    const parseTime = (v) => {
      if (v == null || v === "") return null;
      if (/^\d+(\.\d+)?$/.test(v.trim())) return parseFloat(v);
      const m = v.trim().match(/^(\d+):(\d{1,2}(\.\d+)?)$/);
      return m ? parseInt(m[1], 10) * 60 + parseFloat(m[2]) : null;
    };
    const fmt = (s) => (s == null ? "" : formatTime(s));
    const status = (msg) => { $("#ss-status").textContent = msg; };

    $("#ss-title").value = songTitle();
    $("#ss-close").onclick = () => panel.remove();
    $("#ss-mark-start").onclick = () => {
      const t = currentAudioTime();
      if (t == null) return status("No audio element found — type the start time.");
      $("#ss-start").value = fmt(t);
      status(`Start marked at ${fmt(t)}.`);
    };
    $("#ss-mark-end").onclick = () => {
      const t = currentAudioTime();
      if (t == null) return status("No audio element found — type the end time.");
      $("#ss-end").value = fmt(t);
      status(`End marked at ${fmt(t)}.`);
    };

    const collect = () => ({
      title: $("#ss-title").value.trim() || "Untitled Suno song",
      startSeconds: parseTime($("#ss-start").value),
      endSeconds: parseTime($("#ss-end").value),
      problem: $("#ss-problem").value.trim(),
      desired: $("#ss-desired").value.trim(),
      replacementLyrics: $("#ss-lyrics").value.trim(),
    });

    $("#ss-generate").onclick = () => {
      const issue = collect();
      if (issue.startSeconds == null || issue.endSeconds == null) return status("Need a start and an end time first.");
      if (issue.endSeconds <= issue.startSeconds) return status("End must be after start.");
      $("#ss-output").textContent = buildReplacePrompt(issue);
      status("Editing brief ready. Only replacement lyrics belong in Suno’s lyrics field.");
    };
    $("#ss-copy").onclick = async () => {
      const text = $("#ss-output").textContent;
      if (!text || text.startsWith("Mark a slice")) return status("Generate a prompt first.");
      try { await navigator.clipboard.writeText(text); status("Copied."); }
      catch { status("Copy failed — select the text manually."); }
    };
    $("#ss-copy-lyrics").onclick = async () => {
      const lyrics = $("#ss-lyrics").value.trim();
      if (!lyrics) return status("No replacement lyrics entered.");
      try { await navigator.clipboard.writeText(lyrics); status("Copied ONLY replacement lyrics."); }
      catch { status("Copy failed — select the lyrics manually."); }
    };
    $("#ss-save").onclick = async () => {
      const issue = collect();
      if (issue.startSeconds == null || issue.endSeconds == null) return status("Need a start and an end time first.");
      const issues = await loadIssues();
      issues.push({ ...issue, id: Date.now().toString(36), savedAt: new Date().toISOString(), pageUrl: location.href });
      await saveIssues(issues);
      status(`Saved issue #${issues.length} locally.`);
    };
    return panel;
  }

  // Small floating toggle so the panel can be re-opened after closing.
  function buildToggle() {
    const btn = document.createElement("button");
    btn.id = "suno-surgery-toggle";
    btn.textContent = "🎛️ Suno Surgery";
    btn.title = "Open Suno Surgery — mark a slice, get a Replace Section prompt";
    btn.onclick = () => {
      if (!document.getElementById("suno-surgery-panel")) buildPanel();
    };
    document.body.appendChild(btn);
  }

  // Wait for <body> if the script ran early.
  if (document.body) buildToggle();
  else new MutationObserver((_, obs) => { if (document.body) { buildToggle(); obs.disconnect(); } }).observe(document.documentElement, { childList: true });

  // Keep the popup / side panel in sync: answer time queries from them.
  chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
    if (msg && msg.type === "sunoSurgery:now") {
      sendResponse({ currentTime: currentAudioTime(), title: songTitle(), url: location.href });
      return true;
    }
  });
})();
