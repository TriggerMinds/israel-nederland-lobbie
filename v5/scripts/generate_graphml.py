#!/usr/bin/env python3
"""
Generate israel_advocacy_sna.graphml from v5 CSVs.
Nodes: actors, claims, articles, parliamentary_items, events, funding, travel, legal_actions, outcomes
Edges: edges.csv (all)
"""

import csv
import xml.etree.ElementTree as ET
from pathlib import Path

V5 = Path(r"C:\Users\gewoo\israel nederland lobbie\v5")
OUT = Path(r"C:\Users\gewoo\israel nederland lobbie\v5\israel_advocacy_sna.graphml")

def read_csv(name):
    with open(V5 / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

# ── Build node index ──
nodes = {}  # node_id -> {attr dict}
node_types = {}

for row in read_csv("actors.csv"):
    nid = row["actor_id"]
    nodes[nid] = {
        "label": row.get("label", nid),
        "node_type": "actor",
        "actor_type": row.get("actor_type", ""),
        "sub_type": row.get("sub_type", ""),
        "scope": row.get("scope", ""),
        "tier": row.get("tier", ""),
        "role": row.get("role", ""),
        "confidence": row.get("confidence", ""),
    }
    node_types[nid] = "actor"

for row in read_csv("claims.csv"):
    nid = row["claim_id"]
    nodes[nid] = {
        "label": row.get("label", nid),
        "node_type": "claim",
        "claim_type": row.get("claim_type", ""),
        "status": row.get("status", ""),
        "confidence": row.get("confidence", ""),
    }
    node_types[nid] = "claim"

for row in read_csv("articles.csv"):
    nid = row["article_id"]
    nodes[nid] = {
        "label": row.get("title", nid)[:60],
        "node_type": "article",
        "publisher": row.get("publisher_id", ""),
        "publication_date": row.get("publication_date", ""),
        "type": row.get("type", ""),
    }
    node_types[nid] = "article"

for row in read_csv("parliamentary_items.csv"):
    nid = row["item_id"]
    nodes[nid] = {
        "label": row.get("item_id", nid),
        "node_type": "parliamentary_item",
        "type": row.get("type", ""),
        "actor_id": row.get("actor_id", ""),
        "date": row.get("date", ""),
    }
    node_types[nid] = "parliamentary_item"

for row in read_csv("events.csv"):
    nid = row["event_id"]
    nodes[nid] = {
        "label": row.get("name", nid),
        "node_type": "event",
        "event_type": row.get("event_type", ""),
        "organizer": row.get("organizer_id", ""),
        "date": row.get("date", ""),
    }
    node_types[nid] = "event"

for row in read_csv("funding.csv"):
    nid = row["funding_id"]
    nodes[nid] = {
        "label": nid,
        "node_type": "funding",
        "program": row.get("program", ""),
        "amount_category": row.get("amount_category", ""),
    }
    node_types[nid] = "funding"

for row in read_csv("legal_actions.csv"):
    nid = row["action_id"]
    nodes[nid] = {
        "label": nid,
        "node_type": "legal_action",
        "action_type": row.get("action_type", ""),
        "status": row.get("status", ""),
    }
    node_types[nid] = "legal_action"

for row in read_csv("travel.csv"):
    nid = row["travel_id"]
    nodes[nid] = {
        "label": nid,
        "node_type": "travel",
        "traveler": row.get("traveler_id", ""),
        "destination": row.get("destination", ""),
        "year": row.get("year", ""),
    }
    node_types[nid] = "travel"

for row in read_csv("outcomes.csv"):
    nid = row["outcome_id"]
    nodes[nid] = {
        "label": row.get("outcome_id", nid),
        "node_type": "outcome",
        "outcome_type": row.get("outcome_type", ""),
        "case_id": row.get("case_id", ""),
    }
    node_types[nid] = "outcome"

for row in read_csv("cases.csv"):
    nid = row["case_id"]
    nodes[nid] = {
        "label": row.get("case_name", nid)[:60],
        "node_type": "case",
        "claim_id": row.get("claim_id", ""),
        "confidence": row.get("confidence", ""),
    }
    node_types[nid] = "case"

# ── Build graphml ──

def make_attr(key, value, type="string"):
    a = ET.Element("data", key=key)
    a.text = str(value) if value else ""
    return a

# Keys
ns_graph = "http://graphml.graphdrawing.org/xmlns"
ET.register_namespace("", ns_graph)
g = ET.Element("graphml", xmlns=ns_graph)

key_defs = [
    ("label", "string", "node"),
    ("node_type", "string", "node"),
    ("actor_type", "string", "node"),
    ("sub_type", "string", "node"),
    ("scope", "string", "node"),
    ("tier", "string", "node"),
    ("role", "string", "node"),
    ("claim_type", "string", "node"),
    ("status", "string", "node"),
    ("confidence", "string", "node"),
    ("publisher", "string", "node"),
    ("publication_date", "string", "node"),
    ("type", "string", "node"),
    ("date", "string", "node"),
    ("organizer", "string", "node"),
    ("event_type", "string", "node"),
    ("program", "string", "node"),
    ("amount_category", "string", "node"),
    ("action_type", "string", "node"),
    ("traveler", "string", "node"),
    ("destination", "string", "node"),
    ("year", "string", "node"),
    ("outcome_type", "string", "node"),
    ("case_id", "string", "node"),
    ("claim_id", "string", "node"),
    ("actor_id", "string", "node"),
    ("edge_type", "string", "edge"),
    ("relation_label", "string", "edge"),
    ("evidence_status", "string", "edge"),
    ("date_range", "string", "edge"),
    ("weight", "int", "edge"),
    ("source_type", "string", "edge"),
    ("target_type", "string", "edge"),
    ("confidence_e", "string", "edge"),
]

for kid, ktype, kfor in key_defs:
    k = ET.SubElement(g, "key", id=kid, attr_name=kid, attr_type=ktype)
    k.set("for", kfor)

graph = ET.SubElement(g, "graph", edgedefault="directed")

# Nodes
for nid in sorted(nodes.keys()):
    attrs = nodes[nid]
    n = ET.SubElement(graph, "node", id=nid)
    n.append(make_attr("label", attrs.get("label", "")))
    n.append(make_attr("node_type", attrs.get("node_type", "")))
    for k in ["actor_type","sub_type","scope","tier","role","claim_type","status",
              "confidence","publisher","publication_date","type","date","organizer",
              "event_type","program","amount_category","action_type","traveler",
              "destination","year","outcome_type","case_id","claim_id","actor_id"]:
        if k in attrs:
            n.append(make_attr(k, attrs[k]))

# Edges
edges = read_csv("edges.csv")
missing_nodes = set()
edge_count = 0
for row in edges:
    src = row["source_id"]
    tgt = row["target_id"]
    if src not in nodes:
        missing_nodes.add(src)
        continue
    if tgt not in nodes:
        missing_nodes.add(tgt)
        continue
    e = ET.SubElement(graph, "edge", id=row["edge_id"], source=src, target=tgt)
    e.append(make_attr("edge_type", row.get("edge_type", "")))
    e.append(make_attr("relation_label", row.get("relation_label", "")))
    e.append(make_attr("evidence_status", row.get("evidence_status", "")))
    e.append(make_attr("date_range", row.get("date_range", "")))
    e.append(make_attr("weight", row.get("weight", "1")))
    e.append(make_attr("source_type", row.get("source_type", "")))
    e.append(make_attr("target_type", row.get("target_type", "")))
    e.append(make_attr("confidence_e", row.get("confidence", "")))
    edge_count += 1

tree = ET.ElementTree(g)
tree.write(OUT, encoding="utf-8", xml_declaration=True)

print(f"graphml generated: {OUT}")
print(f"  Nodes: {len(nodes)}")
print(f"  Edges: {edge_count} (from {len(edges)} total; {len(missing_nodes)} skipped for missing node refs)")
if missing_nodes:
    print(f"  Skipped node IDs: {', '.join(sorted(missing_nodes))}")
