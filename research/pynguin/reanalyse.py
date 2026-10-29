#!/usr/bin/env python3
"""Execute the original artifact's numeric notebook cells, without rendering plots/TeX."""
import argparse
from bisect import bisect_left
import hashlib
import json
from pathlib import Path
import re
import statistics
from typing import Any

import numpy as np
import pandas as pd
import scipy.stats as ss
from rich.table import Table

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('artifact', type=Path, help='Extracted emse2022-experiments folder from Zenodo 6838658')
args = parser.parse_args()
root_dir = args.artifact.resolve()
notebook = root_dir / 'notebooks/project-analysis.ipynb'
nb = json.loads(notebook.read_text())
cells = [10, 12, 14, 17, 19, 21, 23, 25, 27, 31, 38]
for index in cells:
    source = ''.join(nb['cells'][index]['source'])
    exec(compile(source, f'<author-notebook-cell-{index}>', 'exec'))
    if index == 10:
        # Preserve this module's published reference before the authors remove
        # modules missing repetitions in any other configuration.
        selected = results_df[(results_df['ConfigurationId'] == 'DynaMOSA-TypeHints') &
                              (results_df['TargetModule'] == 'codetiming._timers')].copy()

# Cell 39 is evaluated unchanged. Only serialization below is new.
summary = eval(compile(''.join(nb['cells'][39]['source']), '<author-notebook-cell-39>', 'eval'))
stored = ''.join(nb['cells'][39]['outputs'][0]['data']['text/plain'])
checks = []
for name, row in summary.iterrows():
    lines = [line for line in stored.splitlines() if line.startswith(name + ' ')]
    numbers = [float(n) for line in lines
               for n in re.findall(r'-?\d+\.\d+', line[len(name):])]
    fields = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    # Pandas wraps the stored table into two blocks. Check every column.
    checks.append(len(numbers) == len(fields) and all(
        abs(float(row[field]) - value) < 0.000001
        for field, value in zip(fields, numbers)))
sources = ['notebooks/project-analysis.ipynb', 'data/results.csv.xz',
           'data/results-assertions.csv.xz', 'data/loc_data.csv',
           'data/types.csv', 'data/types_per_project.csv']
result = {
    'scope': 'author-notebook-numeric-cells-on-published-data',
    'new_test_generation': False,
    'artifact_doi': '10.5281/zenodo.6838658',
    'executed_cells': cells + [39],
    'retained_modules': int(results_df['TargetModule'].nunique()),
    'runs_per_configuration_per_module': int(runs),
    'retained_rows': int(len(results_df)),
    'configurations': summary.reset_index().to_dict(orient='records'),
    'matches_author_stored_describe_output': len(checks) == 10 and all(checks),
    'compared_columns': fields,
    'selected_module_reference': {
        'module': 'codetiming._timers', 'configuration': 'DynaMOSA-TypeHints',
        'runs': len(selected), 'median_branch_coverage': float(selected['Coverage'].median()),
        'reference_stage': 'Published data before cross-configuration completeness filter',
        'in_retained_cross_configuration_comparison': 'codetiming._timers' in set(results_df['TargetModule']),
    },
    'input_sha256': {name: hashlib.sha256((root_dir/name).read_bytes()).hexdigest() for name in sources},
    'limitation': 'Re-executes numeric analysis, not 30 fresh runs per module/configuration; plotting and TeX export omitted.'
}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result['matches_author_stored_describe_output'] and len(selected) == 30 else 1)
