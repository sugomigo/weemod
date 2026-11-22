#!/usr/bin/env python3
"""Read WeeMOD catalog and export a module's explicit allowlist. Python 3.10+."""
import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'catalog' / 'index.json'


def load_catalog():
    data = json.loads(CATALOG.read_text(encoding='utf-8'))
    modules = data['modules']
    ids = [module['id'] for module in modules]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate module IDs in catalog')
    return {module['id']: module for module in modules}


def safe_relative_file(filename):
    relative = Path(filename)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError(f'Unsafe allowlist path: {filename}')
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
        raise ValueError(f'Missing or unsafe file: {filename}')
    return path


def pack(module, output):
    output = output.resolve()
    if output == ROOT.resolve() or ROOT.resolve().is_relative_to(output):
        raise ValueError('Output may not be the repository root or its ancestor')
    file_names = module['files']
    if len(file_names) != len(set(file_names)):
        raise ValueError('Duplicate file names in module allowlist')
    resolved = [(f, safe_relative_file(f)) for f in file_names]
    output.mkdir(parents=True, exist_ok=True)
    for name, src in resolved:
        dest = output / Path(name).name
        if dest.exists():
            raise FileExistsError(f'Refusing to overwrite existing file: {dest}')
        shutil.copyfile(src, dest)
    info = {
        'module_id': module['id'],
        'runtime': module['runtime'],
        'use_when': module['use_when'],
        'avoid_when': module['avoid_when'],
        'license': module['license'],
        'original_files': file_names,
        'note': 'Inspect before use; integrate and retest manually in the destination project.'
    }
    (output / 'WEEMOD_SELECTION.json').write_text(json.dumps(info, indent=2) + '\n', encoding='utf-8')
    print(f"Exported {module['id']} to {output}")


def main():
    parser = argparse.ArgumentParser(description='WeeMOD selective module catalog and pack tool')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list', help='Show available modules')
    inspect_parser = sub.add_parser('inspect', help='Show metadata for one module')
    inspect_parser.add_argument('id')
    pack_parser = sub.add_parser('pack', help='Export allowlisted files for one module')
    pack_parser.add_argument('id')
    pack_parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    try:
        modules = load_catalog()
        if args.command == 'list':
            for module in modules.values():
                print(f"{module['id']} [{module['status']}]: {module['summary']}")
        else:
            if args.id not in modules:
                parser.error(f"Unknown module: {args.id}")
            module = modules[args.id]
            if args.command == 'inspect':
                print(json.dumps(module, indent=2, ensure_ascii=False))
            else:
                pack(module, args.out)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f'WeeMOD error: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
