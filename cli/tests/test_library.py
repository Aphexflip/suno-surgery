import json
import tempfile
import unittest
from pathlib import Path

from suno_patch_kit.library import (
    add_issue,
    add_song,
    add_version,
    find_song,
    load_library,
    new_library,
    save_library,
)


class TestLibrary(unittest.TestCase):
    def test_add_song_and_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "library.json"
            data = new_library()
            song = add_song(data, title="Neon Highway",
                            audio_path="./neon-highway.wav",
                            genre="synthwave", status="draft")
            self.assertEqual(song["status"], "draft")
            self.assertEqual(len(song["versions"]), 1)
            self.assertEqual(song["versions"][0]["label"], "v1 original")
            save_library(path, data)
            loaded = load_library(path)
            self.assertEqual(loaded["songs"][0]["title"], "Neon Highway")

    def test_bad_status_rejected(self):
        with self.assertRaises(ValueError):
            add_song(new_library(), title="X", audio_path="./x.wav",
                     status="nope")

    def test_mark_issue_flips_status(self):
        data = new_library()
        song = add_song(data, title="X", audio_path="./x.wav")
        issue = add_issue(song, start_seconds=42, end_seconds=58,
                          note="mumbled line")
        self.assertEqual(song["status"], "fix-needed")
        self.assertEqual(issue["status"], "open")
        self.assertEqual(issue["start_seconds"], 42)

    def test_issue_end_before_start_rejected(self):
        data = new_library()
        song = add_song(data, title="X", audio_path="./x.wav")
        with self.assertRaises(ValueError):
            add_issue(song, start_seconds=58, end_seconds=42, note="bad")

    def test_add_version_increments(self):
        data = new_library()
        song = add_song(data, title="X", audio_path="./x.wav")
        v = add_version(song, label="v2 chorus fix",
                        audio_path="./x-v2.wav", note="attempt 1")
        self.assertEqual(v["version"], 2)
        self.assertEqual(len(song["versions"]), 2)

    def test_find_song_by_prefix(self):
        data = new_library()
        song = add_song(data, title="X", audio_path="./x.wav")
        self.assertEqual(find_song(data, song["id"][:4])["id"], song["id"])
        with self.assertRaises(KeyError):
            find_song(data, "zzzzzzzz")

    def test_sample_library_loads(self):
        sample = Path(__file__).parent.parent / "examples" / "sample-library.json"
        data = json.loads(sample.read_text(encoding="utf-8"))
        self.assertEqual(data["songs"][0]["title"], "Neon Highway")
        self.assertEqual(data["songs"][0]["issues"][0]["start_seconds"], 42)


if __name__ == "__main__":
    unittest.main()
