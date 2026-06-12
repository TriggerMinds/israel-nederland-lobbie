#!/usr/bin/env python3
"""
v5 integrity checker.
- Count per table
- Validate epistemic_assessments.csv values
- Check referential integrity
"""

import os, csv, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

V5 = r'C:\Users\gewoo\israel nederland lobbie\v5'
ALLOWED = {"low", "medium", "high", "unknown"}

print('v5 inventory:')
csv_files = sorted(f for f in os.listdir(V5) if f.endswith('.csv'))
md_files = [f for f in os.listdir(V5) if f.endswith('.md')]
scripts = os.listdir(os.path.join(V5, 'scripts'))
print(f'  CSV tables: {len(csv_files)}')
print(f'  Docs:       {len(md_files)}')
print(f'  Scripts:    {len(scripts)}')
print()

# ── Table counts ──
tables = {}
for fname in csv_files:
    with open(os.path.join(V5, fname), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    tables[fname] = rows
    print(f'  {fname:40s} {len(rows):5d} rows')

# ── Validate epistemic_assessments ──
print()
if "epistemic_assessments.csv" in tables:
    assess_cols = [
        ("pattern_strength", False),
        ("transmission_strength", False),
        ("impact_strength", True),
        ("capture_risk", False),
        ("independent_verification_level", False),
        ("institutional_self_interest", True),
    ]
    errors = []
    for i, row in enumerate(tables["epistemic_assessments.csv"], 2):
        etype = row.get("entity_type", "")
        eid = row.get("entity_id", "")
        if etype not in ("case", "claim"):
            errors.append(f"  Row {i}: invalid entity_type='{etype}'")
        for col, allow_empty in assess_cols:
            val = row.get(col, "")
            if not val and allow_empty:
                continue
            if not val:
                errors.append(f"  Row {i} ({etype}/{eid}): {col} is empty (allowed: {ALLOWED})")
            elif val not in ALLOWED:
                errors.append(f"  Row {i} ({etype}/{eid}): {col}={val} (allowed: {ALLOWED})")
        if not row.get("assessment_basis", ""):
            errors.append(f"  Row {i} ({etype}/{eid}): assessment_basis is empty")
        if not row.get("review_status", ""):
            errors.append(f"  Row {i} ({etype}/{eid}): review_status is empty")

    if errors:
        print(f'  epistemic_assessments.csv validation FAILED: {len(errors)} errors')
        for e in errors[:10]:
            print(e)
    else:
        print(f'  epistemic_assessments.csv: {len(tables["epistemic_assessments.csv"])} entries - all values valid')

# ── Referential integrity ──
print()
source_ids = {r["source_id"] for r in tables.get("sources.csv", []) if r.get("source_id")}
missing_sources = defaultdict(list)

for fname, rows in tables.items():
    if fname in ("sources.csv",):
        continue
    for col in ("source_ids", "primary_source_ids"):
        for row in rows:
            val = row.get(col, "")
            if not val:
                continue
            for sid in (s.strip() for s in val.split(";") if s.strip()):
                if sid not in source_ids:
                    missing_sources[fname].append(sid)

if missing_sources:
    print(f"  Missing source refs:")
    for fname, sids in sorted(missing_sources.items()):
        print(f"    {fname}: {len(sids)} missing - {sids[:5]}")
    total_missing = sum(len(v) for v in missing_sources.values())
    print(f"  Total missing source refs: {total_missing}")
else:
    print(f"  Referential integrity: all source_ids valid (0 missing)")

# ── Non-empty CSVs ──
print()
empty_tables = [fname for fname, rows in tables.items() if len(rows) == 0 and fname != "bak_epistemic"]
if empty_tables:
    print(f"  Empty tables (expected): {', '.join(empty_tables)}")
else:
    print(f"  All tables have data")

print()
print("v5 check complete.")
