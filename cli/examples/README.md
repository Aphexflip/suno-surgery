# Examples

`sample-library.json` is a complete example library — metadata only.

It contains one song, "Neon Highway" (fictional), with:

- one version (`v1 original`)
- one open issue: `0:42–0:58`, mumbled second-chorus line
- one Replace Section attempt logged

No real audio is included in this repo. Point the `audio_path` fields
at your own downloaded Suno files, or copy this file to `library.json`
and try the read-only commands against it:

```bash
cp examples/sample-library.json library.json
suno-patch-kit --library library.json list
suno-patch-kit --library library.json show a1b2c3d4
suno-patch-kit --library library.json replace-prompt a1b2c3d4 --issue e5f6a7
```
