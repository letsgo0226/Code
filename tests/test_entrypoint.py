"""Exercise the public shell entry point, including filesystem and exit behavior."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EntryPointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / "repo with spaces"
        self.folder.mkdir()
        self.entry = self.folder / "Code.sh"
        shutil.copyfile(ROOT / "Code.sh", self.entry)
        self.core = self.folder / "lfp_atgc_tm_2kb.sh"

    def run_entry(self, *args):
        return subprocess.run(["sh", str(self.entry), *args],
                              cwd=self.temp.name, capture_output=True, text=True,
                              timeout=10)

    def test_real_core_from_another_directory(self):
        shutil.copyfile(ROOT / "lfp_atgc_tm_2kb.sh", self.core)
        direct = subprocess.run(["sh", str(self.core)], check=True,
                                capture_output=True, text=True, timeout=10)
        wrapped = self.run_entry()
        self.assertEqual(wrapped.returncode, 0, wrapped.stderr)
        self.assertEqual(json.loads(wrapped.stdout), json.loads(direct.stdout))
        certificate = json.loads(wrapped.stdout)
        self.assertEqual(certificate["program"], 55067263)
        self.assertTrue(certificate["U2_identity"])

    def test_arguments_preserved_including_run_and_spaces(self):
        self.core.write_text('printf "%s\\n" "$#" "$@"\n')
        result = self.run_entry("--run", "two words", "")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "3\n--run\ntwo words\n\n")

    def test_core_failure_is_not_reported_as_success(self):
        self.core.write_text('echo "core failed" >&2\nexit 23\n')
        result = self.run_entry()
        self.assertEqual(result.returncode, 23)
        self.assertIn("core failed", result.stderr)

    def test_missing_managed_core_fails(self):
        result = self.run_entry()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
