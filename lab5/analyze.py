"""Regenerate baseline/final analysis reports using installed lab tools."""

import json
import subprocess
import sys
from pathlib import Path


def main():
    """Run tools on the two versions and preserve output plus exit codes."""
    root = Path(__file__).resolve().parent
    summary = {}
    for phase, folder in [('before', root / 'original'), ('after', root)]:
        output = root / 'reports' / phase
        output.mkdir(parents=True, exist_ok=True)
        summary[phase] = {}
        for tool, options in [
            ('pylint', ['--persistent=n']),
            ('bandit', ['-r', '-f', 'txt']),
            ('flake8', []),
        ]:
            command = [sys.executable, '-m', tool, *options,
                       'bike_share_stations.py']
            result = subprocess.run(command, cwd=folder, capture_output=True,
                                    text=True, encoding='utf-8')
            (output / f'{tool}_report.txt').write_text(
                result.stdout + result.stderr, encoding='utf-8'
            )
            summary[phase][tool] = result.returncode
            print(f'{phase}: {tool} exit code {result.returncode}')
        demo = subprocess.run([sys.executable, 'bike_share_stations.py'],
                              cwd=folder, capture_output=True, text=True)
        (output / 'demo_output.txt').write_text(
            demo.stdout + demo.stderr, encoding='utf-8'
        )
        summary[phase]['demo'] = demo.returncode
    (root / 'reports' / 'analysis_summary.json').write_text(
        json.dumps(summary, indent=2) + '\n', encoding='utf-8'
    )
    return int(any(summary['after'].values()))


if __name__ == '__main__':
    sys.exit(main())
