import json
import unittest
from pathlib import Path

from game_design_skills_github_action.cli import analyze


class GeneratedRepoTests(unittest.TestCase):
    def test_sample_input_is_ready(self):
        payload = json.loads(Path("examples/sample_input.json").read_text(encoding="utf-8"))
        result = analyze(payload)
        self.assertTrue(result["ready"])
        self.assertEqual(result["score"], 100.0)


if __name__ == "__main__":
    unittest.main()
