# Suno Patch Kit

A local-first organizer and surgical patch helper for Suno songs.

Suno songs usually come out ~80% perfect — one mumbled line, one weak
bridge, one glitch — and the fix shouldn't mean rebuilding the whole
song. Suno Patch Kit keeps your tracks, lyrics, prompts, and versions
in one plain local file, marks exactly what's wrong and where, and
writes the precise brief you paste into Suno's own editor to fix just
that slice.

**No Suno API. No login. No account. No credits spent by this tool.**

## What it is

- A small Python CLI (standard library only) that manages a local
  `library.json` next to your downloaded audio.
- Import a Suno WAV/MP3, tag it (title, genre, mood, status), store its
  lyrics and style prompt.
- Mark a bad time range — e.g. `0:42–0:58`, "second chorus line is
  mumbled" — with replacement lyrics.
- Generate the exact **Replace Section** prompt to paste into Suno.
- Track versions in a tree: v1 original → fix attempt → keeper.
- Optional local preview splice with `ffmpeg`, so you can hear the
  joins before spending Suno credits.

## What it is NOT

- Not a Suno client, plugin, or API wrapper.
- It does not generate music, call Suno, log in to Suno, or use a
  session cookie. Suno has no public self-serve API (as of 2026 it
  opened an intake form for selected developer partners only), and
  unofficial wrappers that scrape Suno's internal endpoints break
  often and sit in a grey area with Suno's terms. This project
  deliberately avoids all of that.
- It does not edit audio in Suno. The actual regeneration happens
  in Suno's own Replace Section editor, which is the supported path.

## How Replace Section works in Suno

This is Suno's own feature (Pro / Premier plans):

1. Open the song in Suno → **More Actions (…) → Edit → Replace Section**.
2. Highlight the part to change on the waveform.
3. Optionally edit the lyrics for just that range.
4. Click **Recreate Section** — Suno returns two new versions.
5. Listen to both in the full song, then commit the one that fits.

Tips that matter:

- **15–20 seconds is the sweet spot.** Under 5s the joins sound
  stitched; over 30s the model loses the melodic thread.
- Change **one variable at a time** — fix the lyric *or* push the
  style, not both — so you know what moved the result.
- Keep the replacement lyrics' syllable count and line shape close
  to the original, and keep the same length, tempo, and key.
- Expect 2–5 attempts for a seamless join. A generated option is an
  audition, not an automatic improvement.
- The original is never modified — an edit produces a new song, so
  you always keep the previous version. That's why this kit tracks
  versions.

## Install

Python 3.10+ only. No dependencies.

```bash
git clone https://github.com/Aphexflip/suno-surgery.git
cd suno-surgery/cli
pip install -e .
```

`ffmpeg` is optional, only for the `preview` command. The preview requires `.wav` output and never overwrites either source file:

```bash
# macOS
brew install ffmpeg
# Debian / Ubuntu
sudo apt install ffmpeg
```

## Quickstart

```bash
# 1. Create a library (a plain library.json in this folder)
suno-patch-kit init

# 2. Import a song you downloaded from Suno
suno-patch-kit import ./neon-highway.wav \
  --title "Neon Highway" \
  --genre "synthwave" --mood "driving, night" \
  --status draft \
  --prompt "driving synthwave, punchy drums, male vocals" \
  --lyrics-file ./neon-highway-lyrics.txt

# 3. Mark the bad bit — 0:42 to 0:58, mumbled line
suno-patch-kit mark <song-id> \
  --start 0:42 --end 0:58 \
  --note "Second chorus line is mumbled, word 'burning' is unclear" \
  --lyrics "We keep burning down the neon highway"

# 4. Get the exact brief to paste into Suno's Replace Section
suno-patch-kit replace-prompt <song-id> --issue <issue-id>

# 5. When Suno gives you a fixed version, record it
suno-patch-kit version <song-id> \
  --label "v2 chorus fix" \
  --audio ./neon-highway-v2.wav \
  --note "Replace Section attempt 1, version B" \
  --mark-keeper

# 6. See where everything stands
suno-patch-kit list
suno-patch-kit show <song-id>
```

Statuses: `draft` → `fix-needed` → `keeper` / `done`.
`mark` automatically flips a song to `fix-needed`.

## Optional: local preview splice

If you already have a replacement audio file for the bad section
(from Suno, a DAW, or anywhere), hear the join locally first:

```bash
suno-patch-kit preview <song-id> --issue <issue-id> \
  --replacement ./chorus-fix.wav \
  --out ./preview-neon-highway.wav
```

This splices `original[0:start] + replacement[offset:offset+length] + original[end:]`
with `ffmpeg`. For a *short replacement clip*, omit the offset (default 0).
For a *complete candidate song*, include `--replacement-offset 0:42` (the
matching timestamp) as in:

```bash
suno-patch-kit preview <song-id> --issue <issue-id> --replacement ./new-whole-song.wav --replacement-offset 0:42 --out ./preview.wav
```

The CLI does **not** automatically align the beats or detect a full-song
candidate. It re-encodes preview audio to 44.1 kHz stereo PCM WAV.
This is a preview, not a release master. If `ffmpeg` isn't installed, this command tells you so
and everything else still works.

## The library file

`library.json` is plain JSON, human-readable, yours to keep:

```json
{
  "schema_version": 1,
  "songs": [
    {
      "id": "a1b2c3d4",
      "title": "Neon Highway",
      "audio_path": "./neon-highway.wav",
      "genre": "synthwave",
      "mood": "driving, night",
      "status": "fix-needed",
      "lyrics": "...",
      "style_prompt": "...",
      "versions": [{ "version": 1, "label": "v1 original", "...": "..." }],
      "issues": [{
        "id": "e5f6a7",
        "start_seconds": 42, "end_seconds": 58,
        "note": "Second chorus line is mumbled",
        "replacement_lyrics": "...",
        "status": "open", "attempts": []
      }],
      "history": []
    }
  ]
}
```

See `examples/sample-library.json` for a complete example (metadata
only — no real audio is included in this repo). Audio files are
ignored by `.gitignore` by default; your library is not committed
unless you choose to.

## Commands

| Command | What it does |
|---|---|
| `init` | Create an empty `library.json` |
| `import <audio> --title ...` | Add a downloaded Suno track |
| `list` | List songs, statuses, open issues |
| `show <song>` | Song detail: versions, issues, lyrics |
| `mark <song> --start --end --note` | Mark a bad time range |
| `replace-prompt <song> --issue` | Print the Replace Section brief |
| `version <song> --label --audio` | Record a new version (optionally `--mark-keeper`) |
| `preview <song> --issue --replacement` | Local ffmpeg splice preview |

Use `--library <path>` before the subcommand to use a different
library file. Times accept seconds (`42`) or `M:SS` (`0:42`).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The hard rule: no Suno API,
no login, no session cookies — ever.

## License

MIT — see [LICENSE](LICENSE).
