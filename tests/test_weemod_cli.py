import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'tools' / 'weemod.py'


class CliTest(unittest.TestCase):
    def call(self, *args):
        return subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True, text=True, cwd=ROOT)

    def test_list(self):
        p = self.call('list')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('async-retry', p.stdout)

    def test_inspect(self):
        p = self.call('inspect', 'async-retry')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['id'], 'async-retry')

    def test_pack_allowlist(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'bundle'
            p = self.call('pack', 'async-retry', '--out', target)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual({x.name for x in target.iterdir()}, {'retry.mjs', 'retry.test.mjs', 'README.md', 'WEEMOD_SELECTION.json'})
            check = json.loads((target / 'WEEMOD_SELECTION.json').read_text(encoding='utf-8'))
            self.assertEqual(check['module_id'], 'async-retry')
            p2 = self.call('pack', 'async-retry', '--out', target)
            self.assertNotEqual(p2.returncode, 0, 'Pack must not overwrite existing files')

    def test_unknown_module(self):
        self.assertNotEqual(self.call('inspect', 'not-here').returncode, 0)

if __name__ == '__main__':
    unittest.main()
