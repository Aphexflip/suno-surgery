# Suno Surgery — consolidated notes (Notion draft)

> Draft text for a Notion page under Erik Life OS / Music Artist OS —
> INDYSKATE / Aphexflip. Not yet written to Notion. Copy the sections
> below into a new page, or paste this file's contents. Source of
> truth for the project until the GitHub repo is public.

## What this is

**Suno Surgery** — fix the last 10–20% of a nearly-finished Suno song
without regenerating the whole song. Three parts, one workflow:

1. **Extension** (`extension/`) — Chrome/Edge MV3. On suno.com,
   mark start/end while the song plays, enter what's wrong, generate
   the exact Replace Section prompt to copy. Local only.
2. **Track Surgery Studio 0.1** (`gui/`) — single offline HTML app.
   Import a downloaded WAV, drag the bad region, load the Suno
   candidate, preview the patch (80 ms crossfade), export a patched
   WAV.
3. **Suno Patch Kit** (`cli/`) — Python CLI. Local library, tags,
   lyrics/prompt history, version tree, ffmpeg preview splice.

## How Erik actually works (this shapes everything)

- He works **entirely in Suno on the website**. He previews and fixes
  there, and **never downloads a song** until it is ~80% right.
- Only then does he download one version to patch.
- Songs come out ~80% perfect with dumb little spots to fix. The
  frustration: Suno will almost always completely remake the song and
  just leave a little bit. He needs a targeted fix, not a re-roll.
- He wants to pump out a lot of songs — some of them will hit — and
  learn to edit specific parts.
- Goal: build public GitHub repos from scratch, done right, as a
  **connector of things** — connect systems together, release the
  pieces so other people can use them. This is the first one.

## The workflow

1. Stay in Suno on the website until a song is ~80% right.
2. Mark the bad slice in the extension while it plays.
   15–20 seconds is the sweet spot. Under 5 s joins sound stitched;
   over 30 s the model loses the melodic thread.
3. In Suno: More Actions (…) > Edit > Replace Section, highlight the
   same range, paste the prompt, Recreate Section. Suno returns two
   versions — listen to both in the full song before committing one.
4. Download the candidate. Bring it into Track Surgery to preview
   the patch in context and export a patched WAV, and/or record the
   version in the Patch Kit CLI (`version … --mark-keeper`).
5. Change one variable at a time — fix the lyric *or* push the style,
   not both. Keep the original; an edit produces a new song.

## What was already built before this repo

- **ChatGPT — Track Surgery Studio 0.1** (Nov 8, 2026). Notion page
  `413964d6-7acf-81eb-bd7f-d8fc01bf87ea` (“Track Surgery Studio —
  Local GUI Pilot & Repair Workflow”). Single-file HTML app + Windows
  ZIP. Zip at `~/workspace/user/files/TrackSurgery-Studio-0.1.zip`
  (13 KB). Smoke-tested on sample WAVs only — **not yet tested on
  real catalog tracks**. No Suno login/API.
- **Muse — Suno Patch Kit CLI** (Nov 9, 2026). Local at
  `~/workspace/suno-patch-kit/`. Python stdlib only, 17/17 tests
  pass. Commands: init / import / list / show / mark /
  replace-prompt / version / preview. Vendored into this repo.
- **Muse — Suno Surgery extension** (Nov 9, 2026). Built in this
  repo at Erik's request: “make like an extension for Chrome or
  Edge… Suno surgery or something.”

## Key facts checked (Nov 9, 2026)

- Suno has **no public self-serve API**. It opened an intake form
  for selected developer partners in July 2026. Everything else is
  unofficial wrappers (session cookie) or paid third-party APIs —
  fragile and grey on Suno's terms. This project uses none of them.
- **Replace Section is Pro/Premier** in Suno's own editor. Erik is
  on Suno Pro ($10/month, Oct 28–Nov 28, 2026), so he has it.
- Suno v6 plain-language section editing also exists, but Replace
  Section is the documented, supported path.
- GitHub account confirmed: **Aphexflip** (Erik Erling, RSYMO, Inc.,
  Indianapolis). Public repos at check time: only `8zoff.com` and
  `indiana-2026-voter-guide` — **no Suno repo exists yet**.
- GitHub + Notion are both connected for Muse. Muse can create the
  repo and push, and write the Notion page — no need for ChatGPT or
  Claude to do it. (Chat handles other GitHub work; Claude is the
  primary developer in the RSYMO system — noted, not needed here.)

## Decisions made

- Build from scratch, clean, public-first, MIT license.
- Local-first, $0: no server, no login, no API key, no Suno account
  in the tool. `chrome.storage.local` / local `library.json` /
  browser IndexedDB only.
- Hard rule (in CONTRIBUTING.md): no Suno API, no login, no session
  cookies, ever.
- Name: **Suno Surgery** for the extension and the consolidated
  repo. Patch Kit stays as the CLI's name inside it.
- Do NOT push to GitHub / create a repo / write to Notion until Erik
  confirms the open questions below. Local only until then.

## Open questions — need Erik's yes

1. **Repo name:** `suno-surgery` (proposed) vs `suno-patch-kit`?
2. **Public vs private** on first push?
3. **GitHub account:** Aphexflip — confirmed as the account, confirm
   it as the repo owner.
4. Who does the push + Notion page — Muse (can do it directly) or
   ChatGPT/Claude? Erik asked “can you handle this or should I get
   ChatGPT on it?” — answer: Muse can handle it; GitHub and Notion
   are both connected and verified.

## Next actions (in order)

- [ ] Erik confirms repo name + public/private.
- [ ] Test Track Surgery with **one real song** (its documented gap:
  sample WAVs only so far). Download an 80% song, mark a real defect,
  get a Replace Section candidate, preview, export.
- [ ] Create public repo `Aphexflip/suno-surgery`, push this folder.
- [ ] Write this page into Notion under Music Artist OS, link the repo.
- [ ] Announce / first use: run one real song end-to-end through all
  three parts and log the result.

## References

- Suno Song Editor: https://help.suno.com/en/articles/6141505
- Suno Replace Section: https://help.suno.com/en/articles/3271873
- Suno Studio 2.0: https://help.suno.com/en/articles/13670529
- Suno MCP beta release notes: https://suno.com/release-notes/suno-mcp-beta
- Notion — Track Surgery Studio: https://app.notion.com/p/413964d67acf81ebbd7fd8fc01bf87ea
- Notion — Suno Free-Generation Music Factory: https://app.notion.com/p/3d8964d67acf81dda4dae7564d750ad8
