import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

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

    def test_pack_rejects_preexisting_selection_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'bundle'
            target.mkdir()
            sentinel = '{"existing": true}\n'
            manifest = target / 'WEEMOD_SELECTION.json'
            manifest.write_text(sentinel, encoding='utf-8')
            p = self.call('pack', 'async-retry', '--out', target)
            self.assertNotEqual(p.returncode, 0)
            self.assertEqual({x.name for x in target.iterdir()}, {'WEEMOD_SELECTION.json'})
            self.assertEqual(manifest.read_text(encoding='utf-8'), sentinel)

    def test_pack_late_collision_leaves_no_partial_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'bundle'
            target.mkdir()
            sentinel = 'keep-existing-readme\n'
            readme = target / 'README.md'
            readme.write_text(sentinel, encoding='utf-8')
            p = self.call('pack', 'async-retry', '--out', target)
            self.assertNotEqual(p.returncode, 0)
            self.assertEqual({x.name for x in target.iterdir()}, {'README.md'})
            self.assertEqual(readme.read_text(encoding='utf-8'), sentinel)

    def test_pack_rejects_duplicate_destination_basenames(self):
        spec = importlib.util.spec_from_file_location('weemod_under_test', CLI)
        weemod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(weemod)
        with tempfile.TemporaryDirectory() as tmp:
            src_file = Path(tmp) / 'sample.txt'
            src_file.write_text('ok\n', encoding='utf-8')
            target = Path(tmp) / 'bundle'
            base_module = {
                'id': 'synthetic-mod',
                'runtime': 'python',
                'use_when': 'test',
                'avoid_when': 'test',
                'license': 'MIT',
            }
            with mock.patch.object(weemod, 'safe_relative_file', side_effect=lambda _f: src_file):
                dup_module = {**base_module, 'files': ['a/retry.mjs', 'b/RETRY.MJS']}
                with self.assertRaises(ValueError):
                    weemod.pack(dup_module, target)
                self.assertFalse(target.exists())

                reserved_module = {**base_module, 'files': ['a/weemod_selection.json']}
                with self.assertRaises(ValueError):
                    weemod.pack(reserved_module, target)
                self.assertFalse(target.exists())

if __name__ == '__main__':
    unittest.main()
