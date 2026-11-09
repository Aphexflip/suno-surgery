# Suno Surgery

Fix the last 10–20% of a nearly-finished Suno song **without
regenerating the whole thing** — and without leaving Suno until you
have to.

Suno songs usually come out ~80% perfect: one mumbled line, one weak
bridge, one glitch. The fix shouldn't mean rebuilding the whole song.
Suno's own **Replace Section** (Pro / Premier: More Actions (…) >
Edit > Replace Section) already regenerates just one slice — but it
doesn't help you find the slice, word the fix, track versions, or
hear the join before you commit. That's what this repo is for.

**No Suno API. No login. No account. No server. No credits spent by
this tool.** Suno has no public self-serve API (as of 2026 it opened
an intake form for selected developer partners only). Unofficial
wrappers that scrape Suno's internal endpoints break often and sit in
a grey area with Suno's terms. This project deliberately avoids all
of that: it writes instructions you paste into Suno, and it patches
audio locally from files you downloaded yourself.

## The three parts — one workflow

| Part | What it is | When you use it |
|---|---|---|
| `extension/` | **Suno Surgery** — Chrome/Edge MV3 extension | While the song plays on suno.com: mark start/end, get the Replace Section prompt, save issues locally |
| `gui/` | **Track Surgery Studio 0.1** — single offline HTML app | After downloading: preview a candidate spliced into the original (80 ms crossfade), export a patched WAV |
| `cli/` | **Suno Patch Kit** — Python CLI, stdlib only | Organize a catalog: library, tags, lyrics/prompt history, version tree, local ffmpeg preview splice |

They share one prompt wording and one discipline. The extension is
the in-browser helper, the GUI is the patcher, the CLI is the
organizer. Pick any one — they work standalone — or use all three.

### The workflow (Erik's actual way of working)

1. **Stay in Suno on the website.** Preview and fix there until a
   song is ~80% right. Never download early versions.
2. When it's close, mark the bad slice in the extension while it
   plays (15–20 s is the sweet spot; under 5 s joins sound stitched,
   over 30 s the model loses the melodic thread).
3. In Suno: **More Actions (…) > Edit > Replace Section**, highlight
   the same range, paste the prompt, **Recreate Section**. Suno
   returns two versions — listen to both in the full song before
   committing one.
4. Download the candidate. Bring it into `gui/track-surgery.html`
   to preview the patch in context and export a patched WAV, and/or
   record the version in the CLI (`suno-patch-kit version … --mark-keeper`).
5. Change **one variable at a time** — fix the lyric *or* push the
   style, not both — so you know what moved the result. Keep the
   original; an edit produces a new song, never an overwrite.

## History / credits

- **Track Surgery Studio 0.1** (`gui/`) was built by **ChatGPT**
  with Erik Erling, November 8, 2026, and documented in Notion
  (“Track Surgery Studio — Local GUI Pilot & Repair Workflow”).
  Kept verbatim here, with credit. Smoke-tested on sample WAVs
  only — not yet tested on real catalog tracks.
- **Suno Patch Kit** (`cli/`) was built by **Muse** (Infinity
  Ultron), November 9, 2026. Python CLI, 17/17 tests pass.
  Vendored into this repo at consolidation time; going forward
  this repo is the single source for it.
- **Suno Surgery extension** (`extension/`) was built by **Muse**,
  November 9, 2026, at Erik's request: “make like an extension
  for Chrome or Edge… Suno surgery or something.”

## Install

**Extension** — Chrome/Edge, load unpacked (see
[`extension/README.md`](extension/README.md)):
`chrome://extensions` → Developer mode → Load unpacked → pick
`extension/`.

**GUI** — double-click `gui/track-surgery.html` in Edge/Chrome.
No install.

**CLI** — Python 3.10+, no dependencies (see
[`cli/README.md`](cli/README.md)):
```bash
cd cli && pip install -e .
suno-patch-kit init
```

## Test

```bash
node --test extension/tests/prompt.test.mjs
python3 -c "import json; json.load(open('extension/manifest.json')); print('manifest OK')"
cd cli && pip install -e . && python3 -m unittest discover -s tests -v   # 17 tests
```

Then load the extension unpacked and check: floating button appears
on suno.com, Mark start/end fills times while playing, Generate shows
a prompt naming the range, Copy works, the issue appears in the popup
after Save. GUI: open `gui/track-surgery.html`, import a WAV, drag a
region, save an issue.

## License

MIT — see [LICENSE](LICENSE).
