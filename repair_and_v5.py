#!/usr/bin/env python3
"""
v4 repair + audit + v5 claim-level provenance expansion
Loopt in 3 fases:
  Phase 1: CSV-repair (quoting, kolomverschuivingen, missing actors)
  Phase 2: Audit (referentiële integriteit, source_ids)
  Phase 3: V5 tables (article_claim_links, parliamentary_claim_links, timeline_events,
            copy_overlap, social_posts, event_participants, organization_people_roles)
"""

import csv
import os
import shutil
import re
from pathlib import Path
from datetime import date
from collections import defaultdict
import textwrap

BASE = Path(r"C:\Users\gewoo\israel nederland lobbie\v4")
OUT = Path(r"C:\Users\gewoo\israel nederland lobbie\v4_repaired")
# We'll output v5 to v4_repaired as well (same directory)

# ── Phase 1: Repair ─────────────────────────────────────────────

def repair_csv(path, fname):
    """Read CSV with repair, return (header, rows, bad_rows_log)."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        bad = []
        for lineno, row in enumerate(reader, 2):
            if len(row) == len(header):
                rows.append(dict(zip(header, row)))
                continue

            bad.append((lineno, len(row), row[0] if row else "EMPTY"))

            # ── claims.csv: unquoted commas in notes field ──
            if fname == "claims.csv" and len(row) > len(header):
                # notes is the last field; join extra cols back
                fixed = row[: len(header) - 1] + [", ".join(row[len(header) - 1 :])]
                rows.append(dict(zip(header, fixed)))
                continue

            # ── cases.csv: extra empty amplifier field ──
            if (
                fname == "cases.csv"
                and row[0] == "CASE_CESTMOCRO_BAN_2024"
                and len(row) == 14
            ):
                fixed = row[:5] + row[6:]
                rows.append(dict(zip(header, fixed)))
                continue

            # ── outcomes.csv: unquoted commas in description + notes ──
            if (
                fname == "outcomes.csv"
                and row[0] == "OUTC_HU_POLITICAL_PRESSURE_2024"
                and len(row) == 13
            ):
                # Columns: outcome_id,case_id,outcome_type,description,date,impact_level,confidence,source_ids,notes
                # Row split: index 0..2 = outcome_id,case_id,outcome_type
                #            3..5 = description split into 3 parts (VVD/BBB/NSC)
                #            6..8 = date,impact_level,confidence
                #            9..12 = source_ids split into parts + notes split
                # Fixed: glue fields 3-5 into description, fields 9-12 into last cols
                fixed = [
                    row[0],  # outcome_id
                    row[1],  # case_id
                    row[2],  # outcome_type
                    ", ".join(row[3:6]),  # description
                    row[6],  # date
                    row[7],  # impact_level
                    row[8],  # confidence
                    ", ".join(row[9:12]),  # source_ids + notes (we'll split afterward)
                ]
                # Actually need to figure out where source_ids ends and notes begins
                # Looking at the data: source_ids = S_HOP_HU_POLITICI_2024, notes = Yesilgöz, Van der Plas, Omtzigt
                # Row[9] = S_HOP_HU_POLITICI_2024, row[10] = Yesilgöz, row[11] = Van der Plas, row[12] = Omtzigt
                # So: source_ids = row[9], notes = ", ".join(row[10:13])
                fixed = [
                    row[0],  # outcome_id
                    row[1],  # case_id
                    row[2],  # outcome_type
                    re.sub(r'\s{2,}', ' ', ", ".join(row[3:6])).strip(),  # description
                    row[6],
                    row[7],
                    row[8],
                    row[9],
                    re.sub(r'\s{2,}', ' ', ", ".join(row[10:13])).strip(),  # notes
                ]
                rows.append(dict(zip(header, fixed)))
                continue

            # ── sources.csv: unquoted comma in reliability_note ──
            if (
                fname == "sources.csv"
                and row[0] == "S_ELSC_2021"
                and len(row) == 7
            ):
                # Columns: source_id,title,url,source_type,evidence_use,reliability_note
                # Row[5] = 'Advocacy/legal monitoring source; use as documented claim'
                # Row[6] = 'not neutral adjudication'
                fixed = row[:5] + [", ".join(row[5:])]
                rows.append(dict(zip(header, fixed)))
                continue

            # ── Generic fallback: more cols than expected ──
            if len(row) > len(header):
                fixed = row[: len(header) - 1] + [re.sub(r'\s{2,}', ' ', ", ".join(row[len(header) - 1 :])).strip()]
                rows.append(dict(zip(header, fixed)))
            else:
                # fewer cols than expected — pad
                fixed = (row + [""] * len(header))[: len(header)]
                rows.append(dict(zip(header, fixed)))

    return header, rows, bad


# ── Read & repair all CSVs ──

tables = {}
bad_rows_log = {}
all_csv = sorted(BASE.glob("*.csv"))

for p in all_csv:
    header, rows, bad = repair_csv(p, p.name)
    tables[p.name] = rows  # list of dicts
    bad_rows_log[p.name] = bad

    print(f"  {p.name}: {len(rows)} rijen, {len(header)} kolommen", end="")
    if bad:
        print(f", {len(bad)} herstelde rijen: {[b[0] for b in bad]}")
    else:
        print()

# ── Add missing abstract / platform actors ──

def get_set(tname, key):
    return {row[key] for row in tables[tname]}

existing_actor_ids = get_set("actors.csv", "actor_id")

missing_actor_rows = [
    {
        "actor_id": "PALESTINIAN_NGOS",
        "label": "Palestijnse / pro-Palestijnse NGO-cluster",
        "actor_type": "NGO",
        "sub_type": "target_cluster",
        "scope": "NL/Palestine",
        "tier": "T1",
        "role": "target_cluster",
        "confidence": "high",
        "source_ids": "S_ELSC_2021",
    },
    {
        "actor_id": "NETHERLANDS_OFFICE",
        "label": "Nederlands kantoor / organisatorische voetafdruk",
        "actor_type": "INFRASTRUCTURE_NODE",
        "sub_type": "organizational_footprint",
        "scope": "NL",
        "tier": "T2",
        "role": "location_or_footprint_node",
        "confidence": "high",
        "source_ids": "S_IAF_EU_NL_OFFICE",
    },
    {
        "actor_id": "EU_POLITICAL_LEADERS",
        "label": "Europarlementariërs en Europese politieke leiders",
        "actor_type": "POLITICAL_CLUSTER",
        "sub_type": "advocacy_target_cluster",
        "scope": "EU",
        "tier": "T2",
        "role": "advocacy_target_cluster",
        "confidence": "medium",
        "source_ids": "S_ECI_LOBBYFACTS",
    },
    {
        "actor_id": "HOP",
        "label": "Hoger Onderwijs Persbureau / HOP",
        "actor_type": "MEDIA_OUTLET",
        "sub_type": "higher_education_press",
        "scope": "NL",
        "tier": "T3",
        "role": "sector_reporting_node",
        "confidence": "high",
        "source_ids": "S_HOP_HU_POLITICI_2024",
    },
    {
        "actor_id": "VILLAMEDIA",
        "label": "Villamedia",
        "actor_type": "MEDIA_OUTLET",
        "sub_type": "journalism_trade_press",
        "scope": "NL",
        "tier": "T3",
        "role": "sector_reporting_node",
        "confidence": "high",
        "source_ids": "S_VILLAMEDIA_CESTMOCRO_2024",
    },
    {
        "actor_id": "CVANDAAG",
        "label": "Cvandaag",
        "actor_type": "MEDIA_OUTLET",
        "sub_type": "christian_media",
        "scope": "NL",
        "tier": "T3",
        "role": "media_reporting_node",
        "confidence": "medium_high",
        "source_ids": "S_CVANDAAG_BARTSCHUT_2017",
    },
    {
        "actor_id": "DUTCH_DONORS",
        "label": "Nederlandse donoren / subsidiegevers",
        "actor_type": "DONOR_CLUSTER",
        "sub_type": "funding_target_cluster",
        "scope": "NL",
        "tier": "T1",
        "role": "financial_leverage_target",
        "confidence": "medium_high",
        "source_ids": "S_ELSC_2021;S_ELSC_PRESS_2021",
    },
]

added_actors = []
for row in missing_actor_rows:
    if row["actor_id"] not in existing_actor_ids:
        tables["actors.csv"].append(row)
        existing_actor_ids.add(row["actor_id"])
        added_actors.append(row["actor_id"])

if added_actors:
    print(f"\n  Toegevoegde referentie-nodes: {', '.join(added_actors)}")

# ── Phase 2: Audit ──────────────────────────────────────────────

def make_set(tname, key):
    return {row[key] for row in tables[tname] if row.get(key)}

actor_ids = make_set("actors.csv", "actor_id")
claim_ids = make_set("claims.csv", "claim_id")
article_ids = make_set("articles.csv", "article_id")
case_ids = make_set("cases.csv", "case_id")
event_ids = make_set("events.csv", "event_id")
parl_ids = make_set("parliamentary_items.csv", "item_id")
outcome_ids = make_set("outcomes.csv", "outcome_id")
source_ids = make_set("sources.csv", "source_id")
travel_ids = make_set("travel.csv", "travel_id")
funding_ids = make_set("funding.csv", "funding_id")
legal_ids = make_set("legal_actions.csv", "action_id")

type_sets = {
    "actor": actor_ids,
    "claim": claim_ids,
    "article": article_ids,
    "case": case_ids,
    "event": event_ids,
    "parliamentary_item": parl_ids,
    "outcome": outcome_ids,
    "source": source_ids,
    "travel": travel_ids,
    "funding": funding_ids,
    "legal_action": legal_ids,
}

missing_refs = []
for row in tables["edges.csv"]:
    for side in ["source", "target"]:
        typ = row.get(f"{side}_type")
        val = row.get(f"{side}_id")
        if typ in type_sets and val and val not in type_sets[typ]:
            missing_refs.append(f"  edges.csv: edge_id={row['edge_id']}, {side}_id={val} (type={typ})")

for fname, cols in [
    ("articles.csv", ["publisher_id", "author_id"]),
    ("cases.csv", ["originator_actor_id"]),
    ("events.csv", ["organizer_id"]),
    ("funding.csv", ["funder_id", "recipient_id"]),
    ("legal_actions.csv", ["plaintiff_id", "defendant_id"]),
    ("parliamentary_items.csv", ["actor_id"]),
    ("travel.csv", ["traveler_id", "organizer_id"]),
    ("claims.csv", ["originator_actor_id"]),
]:
    for col in cols:
        for row in tables[fname]:
            val = row.get(col)
            if val and val not in actor_ids:
                missing_refs.append(f"  {fname}: {col}={val}")

for fname, col in [("cases.csv", "claim_id"), ("parliamentary_items.csv", "related_claim_id")]:
    for row in tables[fname]:
        val = row.get(col)
        if val and val not in claim_ids:
            missing_refs.append(f"  {fname}: {col}={val}")

missing_sources = []
for fname, rows in tables.items():
    for col in ["source_ids", "primary_source_ids"]:
        if col in rows[0] if rows else False:
            for row in rows:
                for sid in [x.strip() for x in str(row.get(col, "")).split(";") if x.strip()]:
                    if sid not in source_ids:
                        missing_sources.append(f"  {fname}: {col}={sid}")

has_col = lambda tname, c: c in (tables[tname][0] if tables[tname] else {})
edges_have_day = lambda: any(len(r.get("date_range", "").split("-")[0].strip().split("-")) == 3 for r in tables["edges.csv"] if r.get("date_range"))

print(f"\n  Missing refs (edges): {len([r for r in missing_refs if 'edges.csv' in r])}")
print(f"  Missing refs (other): {len([r for r in missing_refs if 'edges.csv' not in r])}")
print(f"  Missing source refs: {len(missing_sources)}")

# ── Write Phase 1 repaired CSVs ──

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

for fname, rows in tables.items():
    fpath = OUT / fname
    if not rows:
        continue
    header = list(rows[0].keys())
    with open(fpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)

# Copy markdown files
for md in BASE.glob("*.md"):
    shutil.copy(md, OUT / md.name)

print(f"\n  Repaired CSVs geschreven naar: {OUT}")

# ═══════════════════════════════════════════════════════════════
# Phase 3: V5 — Claim-level provenance expansion
# ═══════════════════════════════════════════════════════════════

# ── Helper: get article metadata ──
article_map = {r["article_id"]: r for r in tables["articles.csv"]}
claim_map = {r["claim_id"]: r for r in tables["claims.csv"]}
case_map = {r["case_id"]: r for r in tables["cases.csv"]}
actor_map = {r["actor_id"]: r for r in tables["actors.csv"]}
parl_map = {r["item_id"]: r for r in tables["parliamentary_items.csv"]}

# ── 3.1 article_claim_links.csv ──
# Build explicit links between articles and claims based on:
#   - edges.csv where source_type=article and target_type=claim (or vice versa)
#   - cases.csv: articles in chain descriptions that relate to claim_id
#   - articles with publisher_id that is originator of a claim

article_claim_links = []
article_claim_links_header = [
    "link_id",
    "article_id",
    "claim_id",
    "source_actor_id",
    "frame_type",
    "citation_type",
    "text_overlap_score",
    "publication_date",
    "confidence",
    "notes",
]

# Strategy A: edges with article source referencing a claim
for row in tables["edges.csv"]:
    if row.get("source_type") == "article" and row.get("target_type") == "claim":
        art = article_map.get(row["source_id"])
        claim = claim_map.get(row["target_id"])
        if art and claim:
            article_claim_links.append({
                "link_id": f"ACL_{row['edge_id']}",
                "article_id": art["article_id"],
                "claim_id": claim["claim_id"],
                "source_actor_id": art.get("publisher_id", ""),
                "frame_type": row.get("edge_type", ""),
                "citation_type": "edge_from_graph",
                "text_overlap_score": "",
                "publication_date": art.get("publication_date", ""),
                "confidence": row.get("confidence", ""),
                "notes": row.get("relation_label", ""),
            })
    if row.get("source_type") == "claim" and row.get("target_type") == "article":
        art = article_map.get(row["target_id"])
        claim = claim_map.get(row["source_id"])
        if art and claim:
            article_claim_links.append({
                "link_id": f"ACL_{row['edge_id']}",
                "article_id": art["article_id"],
                "claim_id": claim["claim_id"],
                "source_actor_id": art.get("publisher_id", ""),
                "frame_type": row.get("edge_type", ""),
                "citation_type": "edge_from_graph",
                "text_overlap_score": "",
                "publication_date": art.get("publication_date", ""),
                "confidence": row.get("confidence", ""),
                "notes": row.get("relation_label", ""),
            })

# Strategy B: cases where chain description names articles and the case has a claim
art_in_chain_pat = re.compile(r"(ART_\w+)")
for case_row in tables["cases.csv"]:
    cid = case_row.get("claim_id", "")
    chain = case_row.get("chain", "")
    if not cid or not chain:
        continue
    matched_articles = art_in_chain_pat.findall(chain)
    for aid in matched_articles:
        if aid in article_map and cid in claim_map:
            # Check if not already added
            if not any(
                l["article_id"] == aid and l["claim_id"] == cid
                for l in article_claim_links
            ):
                article_claim_links.append({
                    "link_id": f"ACL_case_{case_row['case_id']}_{aid[:20]}",
                    "article_id": aid,
                    "claim_id": cid,
                    "source_actor_id": article_map[aid].get("publisher_id", ""),
                    "frame_type": "case_chain_reference",
                    "citation_type": "mentioned_in_case_chain",
                    "text_overlap_score": "",
                    "publication_date": article_map[aid].get("publication_date", ""),
                    "confidence": case_row.get("confidence", ""),
                    "notes": f"Article referenced in case {case_row['case_id']} chain",
                })

# Strategy C: restricted originator links — only when article plausibly transmits the claim
# Uses temporal and content-based heuristics to avoid over-broad linking
claim_by_originator = defaultdict(list)
for r in tables["claims.csv"]:
    oid = r.get("originator_actor_id", "")
    if oid:
        claim_by_originator[oid].append(r)

# Build a set of article IDs referenced in case chains for cross-checking
articles_in_case_chains = set()
for case_row in tables["cases.csv"]:
    chain = case_row.get("chain", "")
    if chain:
        for aid in re.findall(r"ART_\w+", chain):
            articles_in_case_chains.add(aid)

for art_row in tables["articles.csv"]:
    pub = art_row.get("publisher_id", "")
    if pub not in claim_by_originator:
        continue
    art_date = str(art_row.get("publication_date", ""))
    art_title = (art_row.get("title", "") + " " + art_row.get("notes", "")).lower()
    art_id = art_row["article_id"]

    for claim_row in claim_by_originator[pub]:
        cid = claim_row["claim_id"]
        # Skip if already linked via edges or chain
        if any(
            l["article_id"] == art_id and l["claim_id"] == cid
            for l in article_claim_links
        ):
            continue

        # Temporal check: article must be in same year or after claim
        claim_date = claim_row.get("first_publication_date", "")
        if claim_date and art_date:
            try:
                if int(str(art_date)[:4]) < int(claim_date[:4]):
                    continue
            except ValueError:
                pass

        # Plausibility check: article must either appear in a case chain
        # or the claim label/cid must have a keyword match in the article
        in_chain = art_id in articles_in_case_chains
        cid_in_notes = cid in art_row.get("notes", "")
        label_match = any(
            kw in art_title
            for kw in re.findall(r"[A-Za-z]{4,}", claim_row.get("label", "").lower())
        )

        if not (in_chain or cid_in_notes or label_match):
            # Only keep report-type articles as broad originator links
            if art_row.get("type") not in ("ngo_report", "ngo_report_summary", "advocacy_analysis"):
                continue

        article_claim_links.append({
            "link_id": f"ACL_originator_{art_id[:20]}_{cid[:10]}",
            "article_id": art_id,
            "claim_id": cid,
            "source_actor_id": pub,
            "frame_type": "originator_publication",
            "citation_type": "same_actor",
            "text_overlap_score": "",
            "publication_date": art_date,
            "confidence": "high",
            "notes": f"Publisher {pub} is originator of claim {cid}",
        })

# ── 3.2 parliamentary_claim_links.csv ──

parliamentary_claim_links = []
parliamentary_claim_links_header = [
    "link_id",
    "parliamentary_item_id",
    "claim_id",
    "actor_id",
    "link_type",
    "publication_date",
    "confidence",
    "source_ids",
    "notes",
]

# Strategy A: parliamentary_items with explicit related_claim_id
for row in tables["parliamentary_items.csv"]:
    cid = row.get("related_claim_id", "")
    if cid and cid in claim_map:
        parliamentary_claim_links.append({
            "link_id": f"PCL_{row['item_id']}",
            "parliamentary_item_id": row["item_id"],
            "claim_id": cid,
            "actor_id": row.get("actor_id", ""),
            "link_type": "explicit_relation",
            "publication_date": row.get("date", ""),
            "confidence": "high",
            "source_ids": row.get("source_ids", ""),
            "notes": claim_map[cid].get("label", ""),
        })

# Strategy B: edges where parliamentary_item references a claim
for row in tables["edges.csv"]:
    if row.get("source_type") == "parliamentary_item" and row.get("target_type") == "claim":
        cid = row["target_id"]
        pid = row["source_id"]
        if cid in claim_map and pid in parl_map:
            if not any(l["parliamentary_item_id"] == pid and l["claim_id"] == cid for l in parliamentary_claim_links):
                parliamentary_claim_links.append({
                    "link_id": f"PCL_edge_{row['edge_id']}",
                    "parliamentary_item_id": pid,
                    "claim_id": cid,
                    "actor_id": parl_map[pid].get("actor_id", ""),
                    "link_type": row.get("edge_type", "edge_reference"),
                    "publication_date": parl_map[pid].get("date", ""),
                    "confidence": row.get("confidence", ""),
                    "source_ids": f"{row.get('source_ids', '')};{parl_map[pid].get('source_ids', '')}",
                    "notes": row.get("relation_label", ""),
                })

# Strategy C: cases where chain mentions parliamentary items and the case has a claim
parl_in_chain_pat = re.compile(r"(PQ_\w+|GOV_\w+|MOTIE_\w+|TRAVEL_\w+)")
for case_row in tables["cases.csv"]:
    cid = case_row.get("claim_id", "")
    chain = case_row.get("chain", "")
    if not cid or not chain:
        continue
    matched_parl = parl_in_chain_pat.findall(chain)
    for pid in matched_parl:
        if pid in parl_map and cid in claim_map:
            if not any(l["parliamentary_item_id"] == pid and l["claim_id"] == cid for l in parliamentary_claim_links):
                parliamentary_claim_links.append({
                    "link_id": f"PCL_case_{case_row['case_id']}_{pid[:20]}",
                    "parliamentary_item_id": pid,
                    "claim_id": cid,
                    "actor_id": parl_map[pid].get("actor_id", ""),
                    "link_type": "case_chain_reference",
                    "publication_date": parl_map[pid].get("date", ""),
                    "confidence": case_row.get("confidence", ""),
                    "source_ids": parl_map[pid].get("source_ids", ""),
                    "notes": f"Referenced in case {case_row['case_id']} chain",
                })

# ── 3.3 timeline_events.csv ──

timeline_events = []
timeline_events_header = [
    "event_id",
    "case_id",
    "date",
    "event_type",
    "source_type",
    "source_id",
    "source_label",
    "target_type",
    "target_id",
    "target_label",
    "edge_type",
    "claim_id",
    "source_ids",
    "notes",
]

# Collect timeline from edges with date_range
for row in tables["edges.csv"]:
    dr = row.get("date_range", "")
    case_id = row.get("case_id", "")
    if not dr or not case_id:
        continue
    # Use first year or full date
    date_val = dr.split("-")[0].strip() if "-" in dr else dr.strip()
    source_label = actor_map.get(row.get("source_id", ""), {}).get("label", row.get("source_id", ""))
    target_label = actor_map.get(row.get("target_id", ""), {}).get("label", row.get("target_id", ""))
    claim_id = ""
    # Find associated claim
    if row.get("source_type") == "claim":
        claim_id = row["source_id"]
    elif row.get("target_type") == "claim":
        claim_id = row["target_id"]
    elif case_id in case_map:
        claim_id = case_map[case_id].get("claim_id", "")

    timeline_events.append({
        "event_id": f"TL_{row['edge_id']}",
        "case_id": case_id,
        "date": date_val,
        "event_type": row.get("edge_type", ""),
        "source_type": row.get("source_type", ""),
        "source_id": row.get("source_id", ""),
        "source_label": str(source_label) if len(str(source_label)) < 80 else str(source_label)[:77] + "...",
        "target_type": row.get("target_type", ""),
        "target_id": row.get("target_id", ""),
        "target_label": str(target_label) if len(str(target_label)) < 80 else str(target_label)[:77] + "...",
        "edge_type": row.get("edge_type", ""),
        "claim_id": claim_id,
        "source_ids": row.get("source_ids", ""),
        "notes": row.get("relation_label", ""),
    })

# Add timeline entries from articles
for row in tables["articles.csv"]:
    pub_date = row.get("publication_date", "")
    if not pub_date:
        continue
    # Find cases this article is linked to
    linked_cases = set()
    for erow in tables["edges.csv"]:
        if erow.get("source_id") == row["article_id"] or erow.get("target_id") == row["article_id"]:
            if erow.get("case_id"):
                linked_cases.add(erow["case_id"])
    if not linked_cases:
        # Try from article_claim_links
        for acl in article_claim_links:
            if acl["article_id"] == row["article_id"]:
                for cr in tables["cases.csv"]:
                    if cr.get("claim_id") == acl["claim_id"]:
                        linked_cases.add(cr["case_id"])
    for cid in linked_cases or ["UNCategorized"]:
        timeline_events.append({
            "event_id": f"TL_ART_{row['article_id'][:20]}",
            "case_id": cid if cid != "UNCategorized" else "",
            "date": pub_date,
            "event_type": "publication",
            "source_type": "article",
            "source_id": row["article_id"],
            "source_label": str(row.get("title", ""))[:80],
            "target_type": "",
            "target_id": "",
            "target_label": "",
            "edge_type": "",
            "claim_id": next((acl["claim_id"] for acl in article_claim_links if acl["article_id"] == row["article_id"]), ""),
            "source_ids": row.get("source_ids", ""),
            "notes": f"Article: {row.get('title', '')[:100]}",
        })

# Add timeline entries from parliamentary_items
for row in tables["parliamentary_items.csv"]:
    dt = row.get("date", "")
    if not dt:
        continue
    claim_id = row.get("related_claim_id", "")
    timeline_events.append({
        "event_id": f"TL_Parl_{row['item_id']}",
        "case_id": "",
        "date": dt,
        "event_type": row.get("type", "parliamentary_item"),
        "source_type": "parliamentary_item",
        "source_id": row["item_id"],
        "source_label": str(row.get("title", ""))[:80],
        "target_type": "",
        "target_id": "",
        "target_label": "",
        "edge_type": "",
        "claim_id": claim_id,
        "source_ids": row.get("source_ids", ""),
        "notes": "",
    })

# Sort timeline by date
timeline_events.sort(key=lambda x: str(x.get("date", "")))

# ── 3.4 copy_overlap.csv ──
# Prepare structure for text overlap measurement
copy_overlap = []
copy_overlap_header = [
    "overlap_id",
    "source_article_id",
    "target_article_id",
    "source_type",
    "target_type",
    "overlap_score",
    "method",
    "notes",
]

# Seed: identify watchdog/report articles that may be source material for media articles.
# Watchdog actors are those with type WATCHDOG_ORG, COUNTER_ACTOR, or TRANSNATIONAL_HUB.
watchdog_actor_ids = {
    aid for aid, a in actor_map.items()
    if a.get("actor_type") in ("WATCHDOG_ORG", "COUNTER_ACTOR", "TRANSNATIONAL_HUB")
}
report_articles = {r["article_id"]: r for r in tables["articles.csv"]
                   if r.get("publisher_id") in watchdog_actor_ids
                   and r.get("type") in ("ngo_report", "ngo_report_summary", "advocacy_analysis")}

media_articles = {r["article_id"]: r for r in tables["articles.csv"]
                  if r.get("publisher_id") not in watchdog_actor_ids}

# For each watchdog report, find media articles published in the same or next year
# that share a case or claim context
for rid, rart in report_articles.items():
    ryear = str(rart.get("publication_date", ""))[:4]
    if not ryear:
        continue
    rpub = rart.get("publisher_id", "")
    for mid, mart in media_articles.items():
        myear = str(mart.get("publication_date", ""))[:4]
        if not myear:
            continue
        # Only same-year or next-year pairs
        try:
            if int(myear) not in (int(ryear), int(ryear) + 1):
                continue
        except ValueError:
            continue
        # Check for shared case context via edges
        shared_case = False
        for erow in tables["edges.csv"]:
            e_source = erow.get("source_id", "")
            e_target = erow.get("target_id", "")
            if (e_source == rid and e_target == mid) or (e_source == mid and e_target == rid):
                shared_case = True
                break
            # Also check if both connect to the same case
            if erow.get("case_id") and (
                erow.get("source_id") in (rid, mid) or erow.get("target_id") in (rid, mid)
            ):
                for erow2 in tables["edges.csv"]:
                    if erow2.get("case_id") == erow.get("case_id") and erow2.get("edge_id") != erow.get("edge_id"):
                        if erow2.get("source_id") in (rid, mid) or erow2.get("target_id") in (rid, mid):
                            shared_case = True
                            break
        if shared_case:
            overlap_id = f"CO_{rid[:15]}_{mid[:15]}"
            if not any(c["overlap_id"] == overlap_id for c in copy_overlap):
                copy_overlap.append({
                    "overlap_id": overlap_id,
                    "source_article_id": rid,
                    "target_article_id": mid,
                    "source_type": "article",
                    "target_type": "article",
                    "overlap_score": "",
                    "method": "temporal+case — manual verification required",
                    "notes": f"Report {rid} ({ryear}) and media article {mid} ({myear}) share case context",
                })

# Also add pairs from FRAME_SUPPLY or MEDIA_AMPLIFICATION edges that link
# watchdog actors to media outlets, and expand to article level
for row in tables["edges.csv"]:
    if row.get("edge_type") in ("FRAME_SUPPLY", "MEDIA_AMPLIFICATION"):
        src = row.get("source_id", "")
        tgt = row.get("target_id", "")
        # Find articles by source actor and target actor in adjacent years
        src_articles = [r for r in tables["articles.csv"] if r.get("publisher_id") == src]
        tgt_articles = [r for r in tables["articles.csv"] if r.get("publisher_id") == tgt]
        for sa in src_articles:
            syear = str(sa.get("publication_date", ""))[:4]
            for ta in tgt_articles:
                tyear = str(ta.get("publication_date", ""))[:4]
                if syear and tyear:
                    try:
                        if abs(int(tyear) - int(syear)) <= 2:
                            overlap_id = f"CO_edge_{row['edge_id']}_{sa['article_id'][:10]}_{ta['article_id'][:10]}"
                            if not any(c["overlap_id"] == overlap_id for c in copy_overlap):
                                copy_overlap.append({
                                    "overlap_id": overlap_id,
                                    "source_article_id": sa["article_id"],
                                    "target_article_id": ta["article_id"],
                                    "source_type": "article",
                                    "target_type": "article",
                                    "overlap_score": "",
                                    "method": "edge_based — manual verification required",
                                    "notes": f"Via {row['edge_type']}: {row.get('relation_label', '')}",
                                })
                    except ValueError:
                        pass

# ── 3.5 social_posts.csv ──
social_posts = []
social_posts_header = [
    "post_id",
    "platform",
    "author_actor_id",
    "post_date",
    "post_type",
    "content_summary",
    "url",
    "claim_id",
    "case_id",
    "confidence",
    "source_ids",
    "notes",
]

# Extract known social media references from edges and articles
# CestMocro is an Instagram account
social_posts.append({
    "post_id": "SOC_CESTMOCRO_CIDI_COMPLAINT_2023",
    "platform": "Instagram",
    "author_actor_id": "CESTMOCRO",
    "post_date": "2023",
    "post_type": "content_that_triggered_complaint",
    "content_summary": "CestMocro content that CIDI filed complaint about (aanzetten tot haat)",
    "url": "",
    "claim_id": "C11",
    "case_id": "CASE_CESTMOCRO_2023",
    "confidence": "medium",
    "source_ids": "S_CIDI_CESTMOCRO_2023;S_NOS_CESTMOCRO_2023",
    "notes": "Exacte posts niet gearchiveerd in deze dataset; CIDI stelde aangifte op",
})

# Dilan Yesilgöz X statement about HU
social_posts.append({
    "post_id": "SOC_YESILGOZ_HU_X_2024",
    "platform": "X",
    "author_actor_id": "DILAN_YESILGOZ",
    "post_date": "2024",
    "post_type": "public_criticism",
    "content_summary": "Yesilgöz criticized HU postponement as 'gotspe' / disgrace",
    "url": "",
    "claim_id": "C13",
    "case_id": "CASE_HU_CIDI_2024",
    "confidence": "high",
    "source_ids": "S_HOP_HU_POLITICI_2024",
    "notes": "Reported by HOP; exacte post-URL toevoegen uit archief",
})

# Pieter Omtzigt X statement about HU
social_posts.append({
    "post_id": "SOC_OMTZIGT_HU_X_2024",
    "platform": "X",
    "author_actor_id": "PIETER_OMTZIGT",
    "post_date": "2024",
    "post_type": "public_criticism",
    "content_summary": "Omtzigt questioned HU's moral compass over postponement",
    "url": "",
    "claim_id": "C13",
    "case_id": "CASE_HU_CIDI_2024",
    "confidence": "medium_high",
    "source_ids": "S_HOP_HU_POLITICI_2024",
    "notes": "Reported by HOP; exacte post-URL toevoegen uit archief",
})

# Wierd Duk commentary on Nieuws van de Dag (could also be social)
social_posts.append({
    "post_id": "SOC_WIERD_DUK_NVD_2026",
    "platform": "Web",
    "author_actor_id": "WIERD_DUK",
    "post_date": "2026",
    "post_type": "commentary",
    "content_summary": "Wierd Duk over 'Palestiniseren' van media en onderwijs",
    "url": "",
    "claim_id": "C14",
    "case_id": "",
    "confidence": "high",
    "source_ids": "S_NVD_WIERD_DUK_2026",
    "notes": "Nieuws van de Dag platform",
})

# CIDI director statement to NOS
social_posts.append({
    "post_id": "SOC_CIDI_NOS_STATEMENT_2024",
    "platform": "NOS",
    "author_actor_id": "NAOMI_MESTRUM",
    "post_date": "2024",
    "post_type": "media_statement",
    "content_summary": "CIDI director Naomi Mestrum provided statement to NOS about HU postponement",
    "url": "",
    "claim_id": "C13",
    "case_id": "CASE_HU_CIDI_2024",
    "confidence": "high",
    "source_ids": "S_NOS_HU_CIDI_2024",
    "notes": "NOS interview/statement",
})

# ── 3.6 event_participants.csv ──
event_participants = []
event_participants_header = [
    "participant_id",
    "event_id",
    "actor_id",
    "role",
    "confidence",
    "source_ids",
    "notes",
]

# Extract from edges with event source/target
for row in tables["edges.csv"]:
    if row.get("source_type") == "event" and row.get("target_type") == "actor":
        eid = row["source_id"]
        aid = row["target_id"]
        if eid in event_ids and aid in actor_ids:
            event_participants.append({
                "participant_id": f"EP_{row['edge_id']}",
                "event_id": eid,
                "actor_id": aid,
                "role": row.get("edge_type", "participant"),
                "confidence": row.get("confidence", ""),
                "source_ids": row.get("source_ids", ""),
                "notes": row.get("relation_label", ""),
            })
    if row.get("source_type") == "actor" and row.get("target_type") == "event":
        aid = row["source_id"]
        eid = row["target_id"]
        if eid in event_ids and aid in actor_ids:
            event_participants.append({
                "participant_id": f"EP_{row['edge_id']}",
                "event_id": eid,
                "actor_id": aid,
                "role": row.get("edge_type", "participant"),
                "confidence": row.get("confidence", ""),
                "source_ids": row.get("source_ids", ""),
                "notes": row.get("relation_label", ""),
            })

# Add from events.csv organizer_id
for row in tables["events.csv"]:
    org = row.get("organizer_id", "")
    if org and org in actor_ids:
        event_participants.append({
            "participant_id": f"EP_org_{row['event_id']}",
            "event_id": row["event_id"],
            "actor_id": org,
            "role": "organizer",
            "confidence": "high",
            "source_ids": row.get("source_ids", ""),
            "notes": "Event organizer",
        })

# ── 3.7 organization_people_roles.csv ──
org_people_roles = []
org_people_roles_header = [
    "relation_id",
    "person_actor_id",
    "organization_actor_id",
    "role",
    "start_date",
    "end_date",
    "confidence",
    "source_ids",
    "notes",
]

# Extract from edges with FORMER_ROLE, EMPLOYEE_ROLE, FOUNDER_ROLE, EDITORIAL_ROLE, etc.
role_edge_types = {
    "FORMER_ROLE", "EMPLOYEE_ROLE", "FOUNDER_ROLE",
    "EDITORIAL_ROLE", "MEDIA_AFFILIATION",
}
for row in tables["edges.csv"]:
    etype = row.get("edge_type", "")
    if etype in role_edge_types:
        if row.get("source_type") == "actor" and row.get("target_type") == "actor":
            person = row["source_id"]
            org = row["target_id"]
            if person in actor_ids and org in actor_ids:
                org_people_roles.append({
                    "relation_id": f"OR_{row['edge_id']}",
                    "person_actor_id": person,
                    "organization_actor_id": org,
                    "role": etype.lower(),
                    "start_date": "",
                    "end_date": "",
                    "confidence": row.get("confidence", ""),
                    "source_ids": row.get("source_ids", ""),
                    "notes": row.get("relation_label", ""),
                })

# Also extract from articles.csv author->publisher
for row in tables["articles.csv"]:
    author = row.get("author_id", "")
    pub = row.get("publisher_id", "")
    if author and pub and author in actor_ids and pub in actor_ids:
        if not any(
            r["person_actor_id"] == author and r["organization_actor_id"] == pub
            for r in org_people_roles
        ):
            org_people_roles.append({
                "relation_id": f"OR_art_{row['article_id'][:20]}",
                "person_actor_id": author,
                "organization_actor_id": pub,
                "role": "author_or_contributor",
                "start_date": "",
                "end_date": "",
                "confidence": "high",
                "source_ids": row.get("source_ids", ""),
                "notes": f"Author for article {row['article_id']}",
            })

# ── Write v5 CSVs ──

v5_tables = {
    "article_claim_links.csv": (article_claim_links_header, article_claim_links),
    "parliamentary_claim_links.csv": (parliamentary_claim_links_header, parliamentary_claim_links),
    "timeline_events.csv": (timeline_events_header, timeline_events),
    "copy_overlap.csv": (copy_overlap_header, copy_overlap),
    "social_posts.csv": (social_posts_header, social_posts),
    "event_participants.csv": (event_participants_header, event_participants),
    "organization_people_roles.csv": (org_people_roles_header, org_people_roles),
}

for fname, (header, rows) in v5_tables.items():
    fpath = OUT / fname
    with open(fpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  --> {fname}: {len(rows)} rijen, {len(header)} kolommen")

# ── Audit report ──

audit_lines = []
audit_lines.append("# v4 repair + audit + v5 rapport")
audit_lines.append("")
audit_lines.append(f"Generated: {date.today().isoformat()}")
audit_lines.append("")
audit_lines.append("## Phase 1: CSV-repair")
audit_lines.append("")
audit_lines.append("| bestand | probleem | herstel |")
audit_lines.append("|---|---|---|")

repair_map = {
    "claims.csv": "3 rijen (C5, C7, C11) hadden ongequote komma's in notes",
    "cases.csv": "1 rij (CASE_CESTMOCRO_BAN_2024) had extra leeg amplifier-veld → kolomverschuiving",
    "outcomes.csv": "1 rij (OUTC_HU_POLITICAL_PRESSURE_2024) had ongequote komma's in description en notes",
    "sources.csv": "1 rij (S_ELSC_2021) had ongequote komma in reliability_note",
    "actors.csv": f"{len(added_actors)} ontbrekende referentie-nodes toegevoegd",
}
for fname, problem in sorted(repair_map.items()):
    audit_lines.append(f"| {fname} | {problem} | hersteld |")

audit_lines.append("")
audit_lines.append("## Phase 2: Audit")
audit_lines.append("")
audit_lines.append(f"Missing refs in edges.csv: {len([r for r in missing_refs if 'edges.csv' in r])}")
audit_lines.append(f"Missing refs in other tables: {len([r for r in missing_refs if 'edges.csv' not in r])}")
audit_lines.append(f"Missing source refs: {len(missing_sources)}")
audit_lines.append("")
audit_lines.append("### Tabel telling na repair")
audit_lines.append("")
audit_lines.append("| bestand | rijen |")
audit_lines.append("|---|---|")
for fname in sorted(tables):
    audit_lines.append(f"| {fname} | {len(tables[fname])} |")
audit_lines.append("")
audit_lines.append("## Phase 3: V5 - Claim-level provenance expansion")
audit_lines.append("")
audit_lines.append("| tabel | rijen | functie |")
audit_lines.append("|---|---|---|")
v5_desc = {
    "article_claim_links.csv": "Koppelt media-artikelen aan claims via edges, case chains en originator-relaties",
    "parliamentary_claim_links.csv": "Koppelt Kamervragen/moties/reisregistraties aan claims",
    "timeline_events.csv": "Tijdlijn van gebeurtenissen per case, gesorteerd op datum",
    "copy_overlap.csv": "Voorbereiding voor tekstoverlapmeting tussen rapporten en artikelen",
    "social_posts.csv": "Social media / publieke uitingen van actoren (X, Instagram, media-statements)",
    "event_participants.csv": "Deelnemers aan events met rol",
    "organization_people_roles.csv": "Personele relaties (oud-medewerker, founder, editor, etc.)",
}
for fname in sorted(v5_desc):
    n = len(v5_tables[fname][1])
    desc = v5_desc.get(fname, "")
    audit_lines.append(f"| {fname} | {n} | {desc} |")
audit_lines.append("")
audit_lines.append("## Volgende stappen")
audit_lines.append("")
audit_lines.append("1. Per case 5-20 media-items toevoegen aan articles.csv met exacte datums")
audit_lines.append("2. social_posts.csv uitbreiden met systematische X/YouTube/podcast-verzameling")
audit_lines.append("3. copy_overlap.csv vullen via tekstoverlap-analyse (bijv. diff/Python difflib)")
audit_lines.append("4. Datumvelden verbeteren naar ISO-formaat (YYYY-MM-DD) voor temporale sequencing")
audit_lines.append("")

(OUT / "AUDIT_REPORT_V5.md").write_text("\n".join(audit_lines), encoding="utf-8")
print(f"\n  Audit rapport: {OUT / 'AUDIT_REPORT_V5.md'}")
print("\n>> v4 repair + audit + v5 basistabellen gereed")
