#!/usr/bin/env python3
import os, csv, sys

sys.stdout.reconfigure(encoding='utf-8')

v5 = r'C:\Users\gewoo\israel nederland lobbie\v5'
print('v5 inventory:')
csv_files = sorted(f for f in os.listdir(v5) if f.endswith('.csv'))
md_files = [f for f in os.listdir(v5) if f.endswith('.md')]
scripts = os.listdir(os.path.join(v5, 'scripts'))
print(f'  CSV tables: {len(csv_files)}')
print(f'  Docs:       {len(md_files)}')
print(f'  Scripts:    {len(scripts)}')
print()
print(f'  {"Bestand":40s} Rijen')
print(f'  {"-"*40} {"-"*5}')
for fname in csv_files:
    with open(os.path.join(v5, fname), newline='', encoding='utf-8') as f:
        n = sum(1 for _ in csv.DictReader(f))
    print(f'  {fname:40s} {n:5d}')
