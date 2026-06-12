#!/usr/bin/env python3
"""Apply epistemic assessments from epistemic_assessments.csv to cases.csv and claims.csv."""

import csv
from pathlib import Path

V5 = Path(__file__).resolve().parent.parent

def read_csv(name):
    with open(V5 / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(name, rows):
    if not rows:
        return
    with open(V5 / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)

assessments = read_csv("epistemic_assessments.csv")
assessment_cols = [
    "pattern_strength", "transmission_strength", "impact_strength",
    "capture_risk", "independent_verification_level", "institutional_self_interest",
    "assessment_basis", "review_status",
]
allowed = {"low", "medium", "high", "unknown"}

# Validate
for a in assessments:
    for col in assessment_cols:
        val = a.get(col, "")
        if col != "assessment_basis" and col != "review_status" and val and val not in allowed:
            print(f"WARNING: invalid {a['entity_type']}/{a['entity_id']}: {col}={val}")

# For each entity type, read target file and apply
for etype, id_col, target_file in [
    ("case", "case_id", "cases.csv"),
    ("claim", "claim_id", "claims.csv"),
]:
    rows = read_csv(target_file)
    header = list(rows[0].keys())
    for c in assessment_cols:
        if c not in header:
            header.append(c)

    idx = {a["entity_id"]: a for a in assessments if a["entity_type"] == etype}

    for row in rows:
        eid = row[id_col]
        if eid in idx:
            for c in assessment_cols:
                row[c] = idx[eid].get(c, "")
        else:
            for c in assessment_cols:
                row.setdefault(c, "unknown")

    write_csv(target_file, [{k: row.get(k, "") for k in header} for row in rows])
    n = sum(1 for r in rows if r.get("pattern_strength") in allowed - {"unknown"})
    print(f"{target_file}: {n} entries updated from epistemic_assessments.csv")

print("Done.")
