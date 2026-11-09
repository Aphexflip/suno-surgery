# Contributing to Suno Surgery

## Hard rule — never cross this line

- **No Suno API, no login, no session cookies, ever.** No calling
  Suno's internal endpoints, no scraping Suno, no automating
  Replace Section, no storing anyone's Suno credentials.
- This tool writes instructions a human pastes into Suno, and patches
  audio locally from files the user downloaded themselves. That
  boundary is the whole point. A PR that adds a Suno login, a cookie,
  or an API call will be refused.
- No network calls in the extension except the `suno.com` host
  permission (so the content script can run there) and the Suno help
  link in the GUI. No analytics, no server, no account.

## How to contribute

- Small, focused PRs. One fix per PR where you can.
- Keep the prompt wording in sync: `extension/shared/prompt.js`
  and `cli/src/suno_patch_kit/replace.py` say the same thing. If you
  change one, change the other and note it in the PR.
- Tests: `node --test extension/tests/prompt.test.mjs` and
  `cd cli && python3 -m unittest discover -s tests -v` must pass.
- Don't commit audio, `library.json`, browser profile data, or
  anyone's Suno downloads. Examples use fictional songs only.
- Be kind in issues. The target user is a musician fixing one line
  at 1 a.m., not an engineer reading a spec.
