// Suno Surgery — shared prompt builder.
// Single source of truth for the Replace Section brief, shared by the
// content script, popup and side panel. This is a port of the logic in
// cli/src/suno_patch_kit/replace.py — same wording, same discipline.
// It generates TEXT. It never calls Suno, logs in, or spends credits.
// The actual regeneration happens in Suno's own editor:
//   More Actions (...) > Edit > Replace Section (Pro / Premier).

// Format seconds as m:ss, e.g. 42 -> "0:42", 125.5 -> "2:06".
function formatTime(seconds) {
  const s = Math.max(0, Math.round(Number(seconds) || 0));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

// 15-20 seconds is the sweet spot for Replace Section. Under 5s the
// joins sound stitched; over 30s the model loses the melodic thread.
function sectionWarning(startSeconds, endSeconds) {
  const len = endSeconds - startSeconds;
  if (len <= 0) return "End must be after start.";
  if (len < 5) return "Very short section (<5s) — joins often sound stitched. Widen to 10-20s if you can.";
  if (len > 30) return "Long section (>30s) — the model may lose the melodic thread. Narrow to 15-20s if you can.";
  if (len >= 15 && len <= 20) return "";
  return "Usable, but 15-20s is the sweet spot.";
}

// issue: { title, startSeconds, endSeconds, problem, desired,
//          replacementLyrics, stylePrompt, genre, mood }
// Returns a ready-to-paste Replace Section brief.
function buildReplacePrompt(issue) {
  const start = formatTime(issue.startSeconds);
  const end = formatTime(issue.endSeconds);
  const length = Math.round((issue.endSeconds - issue.startSeconds) * 10) / 10;
  const warning = sectionWarning(issue.startSeconds, issue.endSeconds);
  const title = issue.title || "Untitled Suno song";

  const lines = [
    `REPLACE SECTION — EDITING BRIEF (NOT LYRICS) — ${title}  (${start}–${end}, ${length}s)`,
    "",
    "Keep everything outside this range exactly as it is. Regenerate ONLY this section.",
    "",
    `Problem: ${issue.problem || "(describe what's wrong in this slice)"}`,
  ];
  if (issue.desired) lines.push("", `Change to: ${issue.desired}`);
  if (issue.stylePrompt) lines.push("", `Style to keep: ${issue.stylePrompt}`);
  if (issue.genre || issue.mood) {
    lines.push(`Genre/mood: ${[issue.genre, issue.mood].filter(Boolean).join(" / ")}`);
  }
  if (issue.replacementLyrics) {
    lines.push(
      "",
      "Replacement lyrics for this section only:",
      issue.replacementLyrics,
      "",
      "Keep the syllable count and line shape close to the original so the new audio fits the surrounding bars. Same length, same tempo, same key."
    );
  } else {
    lines.push(
      "",
      "No new lyrics supplied — keep the original lyrics for this section, fix only the performance / pronunciation / mix."
    );
  }
  lines.push(
    "",
    `In Suno: open the song > More Actions (…) > Edit > Replace Section > highlight ${start}–${end}. Put ONLY the replacement lyrics in the lyrics field (if provided), never this editing brief. Use the brief for guidance or an instruction field if Suno offers one. Click Recreate Section; audition both versions before committing.`
  );
  if (warning) lines.push("", `Note: ${warning}`);
  return lines.join("\n");
}

// Works in both the extension pages and Node (for tests).
if (typeof module !== "undefined" && module.exports) {
  module.exports = { formatTime, sectionWarning, buildReplacePrompt };
}
