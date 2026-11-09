# Suno Surgery — browser extension (Chrome / Edge, MV3)

Mark a broken slice of a Suno song **while it plays on suno.com**, write
the exact Replace Section prompt, and keep it local. No Suno login, no
API, no server, no credits spent by this tool.

## What it does

- Floating panel on suno.com: **Mark start ▶ / Mark end ▶** reads the
  playing audio's current time (falls back to typing `0:42` / `42`).
- Fields for what's wrong, what should change, and replacement lyrics
  for that section only.
- **Generate prompt** builds the Replace Section brief (same wording as
  `cli/src/suno_patch_kit/replace.py`, single shared logic in
  `shared/prompt.js`). **Copy editing brief** for an instruction/prompt field when available, or use it as a checklist. **Copy lyrics only** for Suno’s lyrics field. Never paste the whole brief into the lyrics field.
- Issues save to `chrome.storage.local` only. Side panel lists them; the side
  panel is the full editor. Clicking the toolbar icon opens the side panel. The legacy popup files remain in the repository but are not configured as the toolbar action.

## What it does NOT do

- No Suno authentication, session cookie, API call, or automated edit.
  Suno has no public self-serve API. The regeneration happens in Suno's
  own editor — this tool only writes the instruction.
- No audio upload/download, no scraping of credentials, no network
  calls at all except the `https://suno.com` link in the GUI help text.
  The extension's only host permission is `suno.com`.

## Install (load unpacked)

Chrome or Edge:

1. Open `chrome://extensions` (Edge: `edge://extensions`).
2. Turn on **Developer mode** (top right).
3. **Load unpacked** → pick this `extension/` folder.
4. Open a song on [suno.com](https://suno.com), play it, click the
   floating **🎛️ Suno Surgery** button (bottom right).
5. After changing extension files, click **Reload** on its card in
   `chrome://extensions`, then reload the Suno tab once.

## Use it — Erik's actual workflow

1. Stay in Suno on the website. Preview and fix there until a song is
   ~80% right. Never download early versions.
2. When it's close, mark the bad slice here (15–20s is the sweet spot;
   under 5s joins sound stitched, over 30s the model loses the thread).
3. In Suno: **More Actions (…) > Edit > Replace Section**, highlight
   the same range, paste replacement lyrics ONLY into the lyrics field; use the brief in an instruction field if available, then **Recreate Section**. Suno returns
   two versions — listen to both in the full song before committing one.
4. Download the candidate, bring it into `gui/track-surgery.html`
   (Track Surgery Studio) to preview the patch in context with an
   80ms crossfade and export a patched WAV — or track versions with
   the `cli/` Patch Kit (`suno-patch-kit version … --mark-keeper`).
5. Change one variable at a time: fix the lyric *or* push the style,
   not both, so you know what moved the result.

## Files

| File | What it is |
|---|---|
| `manifest.json` | MV3 manifest: `storage` + `sidePanel`, host `suno.com` only |
| `background.js` | Service worker — opens the side panel on icon click |
| `content.js` / `content.css` | Floating panel injected on suno.com |
| `popup.html` / `popup.js` / `popup.css` | Legacy popup (currently unused; action opens side panel) |
| `sidepanel.html` / `sidepanel.js` | Side panel — full editor |
| `shared/prompt.js` | Prompt builder, shared by all three surfaces |
| `tests/prompt.test.mjs` | Node tests for the prompt builder |

## Test

```bash
node --test extension/tests/prompt.test.mjs
python3 -c "import json; json.load(open('extension/manifest.json')); print('manifest OK')"
```

Then load unpacked (above) and check: floating button appears on
suno.com, Mark start/end fills times while playing, Generate shows a
prompt naming the range, Copy works, and the issue appears in the
side panel after Save.
