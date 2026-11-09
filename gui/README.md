# Track Surgery Studio — GUI patcher (prior prototype)

This is the **ChatGPT-built prototype, version 0.1**, kept verbatim
except for this README. Credit: built by ChatGPT with Erik Erling,
November 8, 2026, documented in Notion as
“Track Surgery Studio — Local GUI Pilot & Repair Workflow”
(page `413964d6-7acf-81eb-bd7f-d8fc01bf87ea`).

Original zip: `~/workspace/user/files/TrackSurgery-Studio-0.1.zip`
(13 KB, SHA-256 `87d5e9acf610d9dca268c9412a7cd7fc75d133bce48090c6e41df547368ae3e6`).
`track-surgery.html` here is byte-identical to the file in that zip
(SHA-256 `4f57e1f17fde24d761c22329c8d574e4bac51911bb1737fa94a33a62d3e930ee`).

## What it is

A single offline HTML app (`track-surgery.html`, 30 KB, no external
scripts). Open it in Edge/Chrome on Windows:

1. Import up to 5 original songs (WAV preferred, MP3 works).
2. Drag across the waveform over the faulty passage, save the region,
   log the defect and desired correction.
3. Copy the focused edit brief. In Suno: open the song >
   Edit > Replace Section, select the same passage, try alternate
   takes, download a candidate.
4. Import the candidate, compare original / candidate / patched-in-
   context preview. Correct candidate offset: same timestamp for a
   full track, 0 for a short extracted clip.
5. Export a **new** WAV with the candidate spliced in, 80 ms
   crossfade. Listen to the whole new song before promoting it.

See `README.txt` (the original) for the full instructions and limits.

## Status / limits (as documented Nov 8, 2026)

- Smoke-tested on sample WAVs only — **not yet tested on real
  catalog tracks**. That test is the next step before publishing.
- No direct Suno authentication, API call, credit usage, or automated
  Replace Section. Copy/paste + manual candidate import.
- 80 ms crossfade cannot guarantee vocal timbre, phase, beat
  alignment, or reverb continuity. Not mastered; WAV export is
  32-bit float at the decoded sample rate.
- Library lives in the browser's IndexedDB — clearing site data can
  erase it. Keep master files backed up separately. Originals are
  never modified.
