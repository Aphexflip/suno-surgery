"""Audio preview safety tests; no ffmpeg install or media fixtures required."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from suno_patch_kit.audio import preview_splice


class TestPreviewSplice(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p = Path(self.tmp.name)
        self.original = p / "original.wav"
        self.replacement = p / "candidate.wav"
        self.output = p / "preview.wav"
        self.original.write_bytes(b"original")
        self.replacement.write_bytes(b"candidate")

    @patch("suno_patch_kit.audio.subprocess.run")
    @patch("suno_patch_kit.audio.ffmpeg_available", return_value=True)
    def test_full_song_candidate_uses_matching_offset(self, _available, run):
        result = preview_splice(
            self.original, self.replacement,
            start_seconds=42, end_seconds=58, output=self.output,
            replacement_offset_seconds=42,
        )
        self.assertEqual(result, self.output)
        cmd = run.call_args.args[0]
        flt = cmd[cmd.index("-filter_complex") + 1]
        self.assertIn("[1:a]atrim=start=42:duration=16", flt)
        self.assertIn("[0:a]atrim=start=0:end=42", flt)
        self.assertIn("[0:a]atrim=start=58", flt)
        self.assertIn("aresample=44100", flt)
        run.assert_called_once()

    @patch("suno_patch_kit.audio.subprocess.run")
    @patch("suno_patch_kit.audio.ffmpeg_available", return_value=True)
    def test_clip_defaults_to_start_of_replacement(self, _available, run):
        preview_splice(
            self.original, self.replacement,
            start_seconds=42, end_seconds=58, output=self.output,
        )
        flt = run.call_args.args[0][run.call_args.args[0].index("-filter_complex") + 1]
        self.assertIn("[1:a]atrim=start=0.0:duration=16", flt)

    def test_never_overwrites_original(self):
        with self.assertRaisesRegex(ValueError, "must not overwrite"):
            preview_splice(
                self.original, self.replacement,
                start_seconds=1, end_seconds=2, output=self.original,
            )

    def test_rejects_negative_candidate_offset(self):
        with self.assertRaisesRegex(ValueError, "negative"):
            preview_splice(
                self.original, self.replacement,
                start_seconds=1, end_seconds=2, output=self.output,
                replacement_offset_seconds=-1,
            )


if __name__ == "__main__":
    unittest.main()
