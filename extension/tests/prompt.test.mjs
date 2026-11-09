// Suno Surgery — prompt builder tests. Run: node --test extension/tests/prompt.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { formatTime, sectionWarning, buildReplacePrompt } = require("../shared/prompt.js");

const base = {
  title: "Neon Highway",
  startSeconds: 42,
  endSeconds: 58,
  problem: "second chorus line is mumbled",
  desired: "sing it clearly, same melody",
  replacementLyrics: "driving down the neon highway",
  stylePrompt: "synthwave, driving, night",
  genre: "synthwave",
  mood: "driving, night",
};

test("formatTime", () => {
  assert.equal(formatTime(42), "0:42");
  assert.equal(formatTime(125), "2:05");
  assert.equal(formatTime(0), "0:00");
});

test("sectionWarning: 15-20s is the sweet spot, <5s and >30s warn", () => {
  assert.equal(sectionWarning(42, 58), "");
  assert.match(sectionWarning(42, 45), /stitched/);
  assert.match(sectionWarning(0, 45), /melodic thread/);
});

test("buildReplacePrompt names the range, problem, lyrics, and Suno steps", () => {
  const p = buildReplacePrompt(base);
  assert.match(p, /Neon Highway/);
  assert.match(p, /0:42–0:58/);
  assert.match(p, /mumbled/);
  assert.match(p, /driving down the neon highway/);
  assert.match(p, /Replace Section/);
  assert.match(p, /Recreate Section/);
  assert.match(p, /Keep everything outside this range exactly as it is/);
});

test("buildReplacePrompt without lyrics says keep original lyrics", () => {
  const p = buildReplacePrompt({ ...base, replacementLyrics: "" });
  assert.match(p, /keep the original lyrics for this section/);
});

test("brief warns not to paste editing directions into the lyrics field", () => {
  const p = buildReplacePrompt(base);
  assert.match(p, /EDITING BRIEF \(NOT LYRICS\)/);
  assert.match(p, /Put ONLY the replacement lyrics in the lyrics field/);
  assert.doesNotMatch(p, /paste the lyrics above/);
});
