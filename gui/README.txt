APHEXFLIP / INDYSKATE — TRACK SURGERY STUDIO 0.1
================================================

HOW TO RUN ON WINDOWS
1. Extract the ZIP into a folder (or download TrackSurgery.html by itself).
2. Double-click TrackSurgery.html and open it in Microsoft Edge or Google Chrome.
3. Import up to 5 original songs (prefer lossless WAV; MP3 works too).
4. Drag across the waveform over the precise broken spot and click Save region.
5. Describe the defect and the desired replacement, then save/copy the repair brief.
6. In Suno, open the original from your Library > More Actions > Edit > Replace Section.
   Select that same time region and apply your focused request. Generate alternatives.
7. Download a good new version from Suno; attach it in Track Surgery.
8. Play candidate / Patch in context; if it fits, export a new patched WAV.
9. Always compare the complete track to the original before using the new version.

IMPORTANT LIMITATIONS
- The app is local and has NO direct Suno login, upload, credit usage, or API call.
- Suno may regenerate a section differently than instructed. No prompt guarantees exact notes/voice.
- This prototype makes simple 80ms crossfaded audio replacements. Musical and phase continuity is not guaranteed.
- If a candidate is a FULL SUNO SONG, the app initially uses the same timestamp.
  If you downloaded a short replacement clip, set Candidate audio starts at 0 sec.
- WAV output is 32-bit floating-point PCM at the original decoded sample rate, no mastering.
- Source files on disk are never modified. Exported notes JSON does NOT contain audio.
- Song files and candidates are stored in this browser profile via IndexedDB if supported.
  Clearing browser site data may erase the app's library. Keep your master files/backups.
- Maximum 5 original tracks in the prototype.

SOURCE DOCUMENTATION (checked November 8, 2026)
https://help.suno.com/en/articles/6141505 (Song Editor)
https://help.suno.com/en/articles/3271873 (Replace Section)
https://help.suno.com/en/articles/13670529 (Studio 2.0)
https://suno.com/release-notes/suno-mcp-beta (MCP beta)

This is a standalone offline HTML GUI. No installation, subscriptions or API keys required.
