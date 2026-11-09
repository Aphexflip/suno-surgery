# Contributing to Suno Patch Kit

Thanks for helping. This project is intentionally small and local-first.

## Principles

1. **No Suno API, no login, no session cookies.** Suno has no public
   self-serve API. Do not add unofficial wrappers, reverse-engineered
   endpoints, or anything that impersonates a Suno account.
2. **Local first, $0.** The CLI uses only the Python standard library.
   `ffmpeg` is optional, for the local preview splice only.
3. **Don't break the library format.** `library.json` is the user's data.
   Any schema change needs a migration path and a test.
4. **Keep it releasable.** No real audio, no credentials, no personal
   data in examples or tests.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

No extra dependencies are required.

## Tests

```bash
python3 -m unittest discover -s tests -v
# or, if pytest is installed:
pytest
```

Add a test for any new library, prompt-generation, or time-parsing
behaviour.

## Pull requests

- One focused change per PR.
- Update `README.md` if a command or the library format changes.
- Describe what you tested, including whether `ffmpeg` was present.
