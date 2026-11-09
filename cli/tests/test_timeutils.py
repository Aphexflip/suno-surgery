import unittest

from suno_patch_kit.timeutils import format_time, parse_time, section_warning


class TestTimeutils(unittest.TestCase):
    def test_parse_seconds(self):
        self.assertEqual(parse_time("42"), 42.0)
        self.assertEqual(parse_time("42.5"), 42.5)
        self.assertEqual(parse_time(42), 42.0)

    def test_parse_mmss(self):
        self.assertEqual(parse_time("0:42"), 42.0)
        self.assertEqual(parse_time("1:05"), 65.0)

    def test_parse_bad(self):
        with self.assertRaises(ValueError):
            parse_time("not-a-time")
        with self.assertRaises(ValueError):
            parse_time("-5")

    def test_format(self):
        self.assertEqual(format_time(42), "0:42")
        self.assertEqual(format_time(125), "2:05")

    def test_section_warning_sweet_spot(self):
        self.assertIsNone(section_warning(42, 58))  # 16s

    def test_section_warning_too_short(self):
        self.assertIn("under 5s", section_warning(42, 44))

    def test_section_warning_too_long(self):
        self.assertIn("over 30s", section_warning(0, 45))


if __name__ == "__main__":
    unittest.main()
