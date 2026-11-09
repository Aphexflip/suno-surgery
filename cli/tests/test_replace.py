import unittest

from suno_patch_kit.library import add_issue, add_song, new_library
from suno_patch_kit.replace import build_replace_prompt


class TestReplacePrompt(unittest.TestCase):
    def _song_with_issue(self):
        data = new_library()
        song = add_song(
            data, title="Neon Highway", audio_path="./x.wav",
            genre="synthwave", mood="driving",
            style_prompt="driving synthwave, male vocals")
        issue = add_issue(
            song, start_seconds=42, end_seconds=58,
            note="Second chorus line is mumbled",
            replacement_lyrics="We keep burning down the neon highway")
        return song, issue

    def test_prompt_contains_range_note_and_lyrics(self):
        song, issue = self._song_with_issue()
        prompt = build_replace_prompt(song, issue)
        self.assertIn("0:42–0:58", prompt)
        self.assertIn("mumbled", prompt)
        self.assertIn("We keep burning down the neon highway", prompt)
        self.assertIn("Replace Section", prompt)
        self.assertIn("Keep everything outside this range", prompt)

    def test_prompt_without_replacement_lyrics(self):
        data = new_library()
        song = add_song(data, title="X", audio_path="./x.wav")
        issue = add_issue(song, start_seconds=10, end_seconds=26,
                          note="weak bridge")
        prompt = build_replace_prompt(song, issue)
        self.assertIn("No new lyrics supplied", prompt)

    def test_short_section_warns(self):
        data = new_library()
        song = add_song(data, title="X", audio_path="./x.wav")
        issue = add_issue(song, start_seconds=42, end_seconds=44,
                          note="glitch")
        prompt = build_replace_prompt(song, issue)
        self.assertIn("under 5s", prompt)


if __name__ == "__main__":
    unittest.main()
