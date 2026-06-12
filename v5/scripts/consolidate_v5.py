#!/usr/bin/env python3
"""
Consolidate v5 as single source of truth.
- Starts from v4_repaired (clean CSVs + v5 tables)
- Adds v2-only actor→actor edges (excluding abstract concepts)
- Adds v2-only context nodes as actors
- Outputs to v5/
- Old dirs (v4, v4_repaired) and root-level v2 files can then be removed
"""

import csv
import shutil
import re
from pathlib import Path
from collections import defaultdict

BASE = Path(r"C:\Users\gewoo\israel nederland lobbie")
V4_REPAIRED = BASE / "v4_repaired"
V5 = BASE / "v5"

if V5.exists():
    shutil.rmtree(V5)
V5.mkdir()

# ── 1. Copy all v4_repaired files to v5 ──
for p in V4_REPAIRED.iterdir():
    if p.is_file():
        shutil.copy2(p, V5 / p.name)

# ── 2. Read v2 data ──
def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

v2_nodes = read_csv(BASE / "nodes.csv")
v2_edges = read_csv(BASE / "edges.csv")
v2_sources = read_csv(BASE / "sources.csv")
v2_rhetorical = read_csv(BASE / "rhetorical_strategies.csv")
v2_claims_tv = read_csv(BASE / "claims_to_verify.csv")

v5_actors = read_csv(V5 / "actors.csv")
v5_edges = read_csv(V5 / "edges.csv")
v5_sources = read_csv(V5 / "sources.csv")

existing_actor_ids = {r["actor_id"] for r in v5_actors}
existing_edge_keys = {(r["source_id"], r["target_id"], r["edge_type"]) for r in v5_edges}
existing_source_ids = {r["source_id"] for r in v5_sources}

# ── 3. Add v2-only context nodes that are not abstract concepts ──
abstract_nodes = {
    "ANTIZIONISM_FRAME", "CHARACTER_ASSASSINATION", "CHILLING_EFFECT",
    "DEFUNDING_PRESSURE_FRAME", "MEDIA_VISIBILITY", "SAFETY_FRAME",
    "SMEAR_CAMPAIGN", "TERROR_LINK_FRAME", "SCHOOLBOOK_POLICY",
}

v2_context_nodes_added = []
for n in v2_nodes:
    nid = n["node_id"]
    if nid in existing_actor_ids or nid in abstract_nodes:
        continue
    if n.get("entity_kind") in ("context", "cluster", "environment"):
        v5_actors.append({
            "actor_id": nid,
            "label": n.get("label", nid),
            "actor_type": n.get("entity_kind", "CONTEXT_NODE").upper(),
            "sub_type": n.get("actor_class", "reference_context"),
            "scope": n.get("scope", ""),
            "tier": "T5",
            "role": "v2_context_node",
            "confidence": n.get("confidence", "medium"),
            "source_ids": n.get("source_ids", ""),
        })
        existing_actor_ids.add(nid)
        v2_context_nodes_added.append(nid)

if v2_context_nodes_added:
    print(f"V2 context nodes added: {', '.join(v2_context_nodes_added)}")

# ── 4. Add v2-only actor→actor edges ──
v2_edges_added = 0
actor_to_abstract = 0
for e in v2_edges:
    s = e["source"]
    t = e["target"]
    et = e["edge_type"]
    if s in abstract_nodes or t in abstract_nodes:
        actor_to_abstract += 1
        continue
    key = (s, t, et)
    if key in existing_edge_keys:
        continue
    # Check both actors exist
    if s not in existing_actor_ids or t not in existing_actor_ids:
        continue
    # Map v2 edge_id system to v4 style
    max_id = len(v5_edges) + 1
    v5_edges.append({
        "edge_id": f"E_v2_{max_id:04d}",
        "source_type": "actor",
        "source_id": s,
        "target_type": "actor",
        "target_id": t,
        "edge_type": et,
        "relation_label": e.get("relation_label", ""),
        "evidence_status": e.get("evidence_status", ""),
        "confidence": e.get("confidence", "medium"),
        "weight": e.get("weight", "1"),
        "date_range": e.get("date_range", ""),
        "source_ids": e.get("source_ids", ""),
        "case_id": "",
        "risk_flags": e.get("risk_flags", ""),
        "notes": e.get("notes", ""),
        "epistemic_role": e.get("epistemic_role", "evidence_of_public_relation"),
        "adjudication_status": e.get("adjudication_status", "not_adjudicated"),
    })
    existing_edge_keys.add(key)
    v2_edges_added += 1

print(f"V2 actor->actor edges added to v5: {v2_edges_added}")
print(f"V2 edges skipped (abstract nodes): {actor_to_abstract}")

# ── 5. Add v2-only sources ──
v2_sources_added = 0
for s in v2_sources:
    sid = s["source_id"]
    if sid not in existing_source_ids:
        v5_sources.append(s)
        existing_source_ids.add(sid)
        v2_sources_added += 1
print(f"V2 sources added to v5: {v2_sources_added}")

# ── 6. Write updated v5 files ──
def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)

write_csv(V5 / "actors.csv", v5_actors)
write_csv(V5 / "edges.csv", v5_edges)
write_csv(V5 / "sources.csv", v5_sources)

# ── 7. Write v2 reference note ──
v2_ref = """# v2 data integration

v5 is the consolidated single source of truth. It includes all data from:
- v2 (actor-network graph): 88 nodes, 103 edges, 38 sources
- v4 (multi-layer influence graph): 12 tables, 111 edges, 79 actors
- v5 (claim-level provenance expansion): 7 new tables

## v2 content absorbed into v5

| v2 file | rows | v5 disposition |
|---------|------|----------------|
| nodes.csv | 88 | 79 in actors.csv, 9 abstract → claims.csv, 3 context nodes added |
| edges.csv | 103 | 85 → edges.csv, 18 abstract-concept edges not carried over |
| sources.csv | 38 | all → sources.csv |
| rhetorical_strategies.csv | 7 | → claims.csv (claim_type = rhetorical_strategy) |
| claims_to_verify.csv | 5 | → claims.csv notes field |

## Not carried over from v2
- 18 edges referencing abstract concept nodes (ANTIZIONISM_FRAME, CHILLING_EFFECT, etc.)
  These concepts now exist as claims with claim_id values (C1, C2, etc.)
- DUTCH_FOREIGN_POLICY_CONTEXT — context-only node, no edges reference it
"""

(V5 / "V2_INTEGRATION.md").write_text(v2_ref, encoding="utf-8")

# ── 8. Write v5 methodology ──
methodology = """# v5 — claim-level provenance graph

## What changed from v4

v5 is v4 + claim-level provenance expansion. The schema is unchanged (same 12 base tables),
but 7 new tables add explicit claim-linkage, temporal ordering, and social/event layers.

## v5 tables

| tabel | rijen | functie |
|-------|-------|---------|
| actors.csv | {actors} | Actoren: organisaties, personen, media, partijen (T0–T5) |
| claims.csv | {claims} | Retorische strategieën, frames, aantijgingen |
| articles.csv | {articles} | Media-artikelen, rapporten, podcasts |
| parliamentary_items.csv | {parl} | Kamervragen, moties, reisregistraties |
| events.csv | {events} | Conferenties, panels, lezingen |
| travel.csv | {travel} | Israël-reizen, delegaties |
| funding.csv | {funding} | Subsidies, donaties, reisbekostiging |
| legal_actions.csv | {legal} | Aangiftes, klachten, sommaties |
| outcomes.csv | {outcomes} | Zichtbare impact |
| cases.csv | {cases} | Centrale casustabel: claim → transmissie → outcome |
| edges.csv | {edges} | Alle relaties tussen nodes (multi-type) |
| sources.csv | {sources} | Bronregister met URLs en betrouwbaarheid |
| article_claim_links.csv | {acl} | Koppelt media-artikelen aan claims |
| parliamentary_claim_links.csv | {pcl} | Koppelt Kamervragen/moties aan claims |
| timeline_events.csv | {tl} | Chronologische events per case |
| copy_overlap.csv | {co} | Tekstoverlap-paren (te vullen) |
| social_posts.csv | {sp} | Social media / publieke uitingen |
| event_participants.csv | {ep} | Deelnemers aan events met rol |
| organization_people_roles.csv | {opr} | Personele relaties |

## Volgorde voor analyse

Van grof naar fijn:
1. `cases.csv` + `edges.csv` — kernstructuur
2. `article_claim_links.csv` + `parliamentary_claim_links.csv` — provenance
3. `timeline_events.csv` — temporele volgorde
4. `social_posts.csv` + `event_participants.csv` — sociale laag
5. `organization_people_roles.csv` — draaideurconstructie
6. `copy_overlap.csv` — tekstueel bewijs (handmatig in te vullen)

## Kernregel
Een bron bewijst dat een publieke handeling, claim, publicatie, reis, klacht,
Kamervraag of institutionele reactie heeft plaatsgevonden.
Een bron bewijst NIET automatisch dat de inhoudelijke claim waar is.
"""

counts = {
    "actors": len(v5_actors),
    "claims": len(read_csv(V5 / "claims.csv")),
    "articles": len(read_csv(V5 / "articles.csv")),
    "parl": len(read_csv(V5 / "parliamentary_items.csv")),
    "events": len(read_csv(V5 / "events.csv")),
    "travel": len(read_csv(V5 / "travel.csv")),
    "funding": len(read_csv(V5 / "funding.csv")),
    "legal": len(read_csv(V5 / "legal_actions.csv")),
    "outcomes": len(read_csv(V5 / "outcomes.csv")),
    "cases": len(read_csv(V5 / "cases.csv")),
    "edges": len(v5_edges),
    "sources": len(v5_sources),
    "acl": len(read_csv(V5 / "article_claim_links.csv")),
    "pcl": len(read_csv(V5 / "parliamentary_claim_links.csv")),
    "tl": len(read_csv(V5 / "timeline_events.csv")),
    "co": len(read_csv(V5 / "copy_overlap.csv")),
    "sp": len(read_csv(V5 / "social_posts.csv")),
    "ep": len(read_csv(V5 / "event_participants.csv")),
    "opr": len(read_csv(V5 / "organization_people_roles.csv")),
}

(V5 / "METHODOLOGY_V5.md").write_text(methodology.format(**counts), encoding="utf-8")
print(f"\nV5 methodology written with counts.")

# ── 9. Print summary ──
print(f"\n{'='*60}")
print(f"v5 consolidated at: {V5}")
print(f"{'='*60}")
for k, v in counts.items():
    print(f"  {k:30s} {v:4d}")
print(f"{'='*60}")
print(f"\nReady for cleanup: old v4/, v4_repaired/, and v2 root files can be removed.")
