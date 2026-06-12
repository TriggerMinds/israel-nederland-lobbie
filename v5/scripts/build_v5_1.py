#!/usr/bin/env python3
"""
v5.1: epistemic_assessments CSV + copy_overlap filling + validation.
"""

import csv, re, shutil
from pathlib import Path

V5 = Path(r"C:\Users\gewoo\israel nederland lobbie\v5")

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

ALLOWED = {"low", "medium", "high", "unknown"}

# ── 1. epistemic_assessments.csv ──

ASSESSMENT_HEADER = [
    "entity_type", "entity_id",
    "pattern_strength", "transmission_strength", "impact_strength",
    "capture_risk", "independent_verification_level", "institutional_self_interest",
    "assessment_basis", "review_status"
]

assessments = [
    # ── Cases ──
    {
        "entity_type": "case",
        "entity_id": "CASE_NGO_OXFAM_2026",
        "pattern_strength": "high",
        "transmission_strength": "high",
        "impact_strength": "medium",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "high",
        "assessment_basis": "Transmissie: NGO Monitor -> Telegraaf -> VVD+PVV Kamervragen -> kabinet. Patroon: herhaald over meerdere jaren. Impact: officiele non-confirmatie maar geen onafhankelijk onderzoek. Overheid is donor en beleidsverantwoordelijke.",
        "review_status": "draft",
    },
    {
        "entity_type": "case",
        "entity_id": "CASE_ALMEZAN_2020",
        "pattern_strength": "high",
        "transmission_strength": "high",
        "impact_strength": "medium",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "high",
        "assessment_basis": "Transmissie: NGO Monitor -> Joods.nl+Telegraaf -> PVV Kamervragen -> CIDI publicatie. Getrianguleerd via ELSC-rapport. Geen rechterlijke toets. Bevestigingsronde langs betrokken media niet uitgevoerd.",
        "review_status": "needs_source_verification",
    },
    {
        "entity_type": "case",
        "entity_id": "CASE_UAWC_DEFUNDING",
        "pattern_strength": "medium",
        "transmission_strength": "medium",
        "impact_strength": "medium",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "high",
        "assessment_basis": "Transmissie deels gedocumenteerd via TRF/ELSC. Impact op NL-financiering onduidelijk. Overheid is donor en heeft inherent belang bij due-diligence beeld.",
        "review_status": "draft",
    },
    {
        "entity_type": "case",
        "entity_id": "CASE_CESTMOCRO_2023",
        "pattern_strength": "medium",
        "transmission_strength": "high",
        "impact_strength": "medium",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "high",
        "assessment_basis": "Transmissie: CIDI -> NOS + CIDI->kabinet. Geen rechterlijke uitspraak. CIDI is zowel klager als bron. Patroon: losse case, geen herhaling over meerdere instanties.",
        "review_status": "draft",
    },
    {
        "entity_type": "case",
        "entity_id": "CASE_SCHOOLBOOK_2015",
        "pattern_strength": "low",
        "transmission_strength": "low",
        "impact_strength": "low",
        "capture_risk": "low",
        "independent_verification_level": "low",
        "institutional_self_interest": "low",
        "assessment_basis": "Eenmalige campagne Likoed -> ThiemeMeulenhoff. Geen zichtbaar beleidseffect, geen media-amplificatie buiten eigen kanaal, geen politieke opvolging.",
        "review_status": "draft",
    },
    {
        "entity_type": "case",
        "entity_id": "CASE_SCHOOLBOOK_2019",
        "pattern_strength": "low",
        "transmission_strength": "low",
        "impact_strength": "low",
        "capture_risk": "low",
        "independent_verification_level": "low",
        "institutional_self_interest": "low",
        "assessment_basis": "Eenmalige campagne Likoed -> Noordhoff via Jonet. Identiek patroon aan 2015 maar separaat. Geen correctie-effect zichtbaar in dataset.",
        "review_status": "draft",
    },
    {
        "entity_type": "case",
        "entity_id": "CASE_HU_CIDI_2024",
        "pattern_strength": "medium",
        "transmission_strength": "high",
        "impact_strength": "high",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "medium",
        "assessment_basis": "Transmissie: CIDI -> Telegraaf -> GeenStijl -> Yesilgoz+VdPlas+Omtzigt -> HU. Impact: uitstel collegereeks + politieke druk. Rapportage primair via HOP/NOS. CIDI-veiligheidsframe niet onafhankelijk geverifieerd.",
        "review_status": "draft",
    },
    {
        "entity_type": "case",
        "entity_id": "CASE_IAF_CAUCUS_2013",
        "pattern_strength": "medium",
        "transmission_strength": "medium",
        "impact_strength": "high",
        "capture_risk": "low",
        "independent_verification_level": "high",
        "institutional_self_interest": "medium",
        "assessment_basis": "Netwerkvorming IAF/IIACF Nederland caucus. Bron: IAF zelf + Jonet. Impact: structurele parlementaire infrastructuur sinds 2013. Onafhankelijk verifieerbaar via open kamerledenregistraties.",
        "review_status": "draft",
    },
    {
        "entity_type": "case",
        "entity_id": "CASE_CESTMOCRO_BAN_2024",
        "pattern_strength": "low",
        "transmission_strength": "low",
        "impact_strength": "low",
        "capture_risk": "medium",
        "independent_verification_level": "medium",
        "institutional_self_interest": "medium",
        "assessment_basis": "Eenmalige publieke uitspraak Caroline van der Plas. Geen Kamervraag of wetsvoorstel. Villamedia-rapportage bevestigt. Lage transmissie, geen verdere institutionele opvolging.",
        "review_status": "draft",
    },
    {
        "entity_type": "case",
        "entity_id": "CASE_IAF_EU_OFFICE",
        "pattern_strength": "low",
        "transmission_strength": "low",
        "impact_strength": "low",
        "capture_risk": "low",
        "independent_verification_level": "high",
        "institutional_self_interest": "medium",
        "assessment_basis": "IAF Europe opent kantoor in Nederland. Zelfrapportage via IAF-website. Geen directe lobby-edges of parlementaire impact in dataset. Organisatorische voetafdruk, geen transmissiecase.",
        "review_status": "draft",
    },
    # ── Claims ──
    {
        "entity_type": "claim",
        "entity_id": "C1",
        "pattern_strength": "high",
        "transmission_strength": "high",
        "impact_strength": "",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Antisemitismeframing als terugkerend patroon gedocumenteerd door ELSC over 2015-2020. Herkenbaar in meerdere cases (HU, CestMocro, Al Mezan). Geen onafhankelijke rechterlijke toets per incident.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C2",
        "pattern_strength": "high",
        "transmission_strength": "high",
        "impact_strength": "",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Terror-link framing herhaald over meerdere cases (Oxfam, Al Mezan, UAWC). Transmissie via NGO Monitor -> media -> Kamervragen. Geen onafhankelijke bevestiging van inhoudelijke claims.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C3",
        "pattern_strength": "high",
        "transmission_strength": "medium",
        "impact_strength": "",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Karaktermoord-frame gedocumenteerd door TRF over meerdere publicaties. Patroon herkenbaar maar bron is zelf betrokken partij (TRF). Transmissie naar mainstream media beperkt.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C4",
        "pattern_strength": "medium",
        "transmission_strength": "high",
        "impact_strength": "",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Veiligheidsframe door CIDI in HU-case. Transmissie via NOS/HOP. CIDI is zowel klager als framebron. Geen externe verificatie van veiligheidsclaim. Patroonherhaling over meerdere CIDI-interventies.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C5",
        "pattern_strength": "high",
        "transmission_strength": "high",
        "impact_strength": "",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Subsidie- en fondsendruk als terugkerend patroon gedocumenteerd door ELSC. Zichtbaar in UAWC-case. Overheid is donor en doelwit van druk. Herhaald patroon over meerdere jaren en cases.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C6",
        "pattern_strength": "medium",
        "transmission_strength": "medium",
        "impact_strength": "",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Schijn van onafhankelijke expertise rond NGO Monitor. NRC-artikel + NGO Monitor-rebuttal. Beide partijen betwisten elkaars positie. Geen onafhankelijke derde partij die oordeelt.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C7",
        "pattern_strength": "high",
        "transmission_strength": "medium",
        "impact_strength": "",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Chilling effect als impactmechanisme gedocumenteerd door ELSC. Meetbaar via afgezegde events (HU-case). Lastig direct te bewijzen want effect is zelfcensuur, dus per definitie deels onzichtbaar.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C8",
        "pattern_strength": "high",
        "transmission_strength": "high",
        "impact_strength": "",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "NGO Monitor Oxfam/DRA terror-link claim. Volledige transmissieketen: rapport -> Telegraaf -> VVD+PVV Kamervragen -> kabinet. Overheid is donor en reageert met non-confirmatie + due-diligence assertion.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C9",
        "pattern_strength": "high",
        "transmission_strength": "high",
        "impact_strength": "",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Al Mezan terror-link claim. Transmissie via Joods.nl + Telegraaf -> PVV -> CIDI publicatie. Gedocumenteerd door ELSC. Transmissieroute gereconstrueerd maar niet per artikel geverifieerd.",
        "review_status": "needs_source_verification",
    },
    {
        "entity_type": "claim",
        "entity_id": "C10",
        "pattern_strength": "medium",
        "transmission_strength": "medium",
        "impact_strength": "",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "UAWC terror-link claim. Transmissie deels gedocumenteerd via TRF/ELSC. Impact op NL-financiering niet direct aangetoond. Patroon vergelijkbaar met C8/C9 maar minder volledige keten.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C11",
        "pattern_strength": "medium",
        "transmission_strength": "high",
        "impact_strength": "",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "CIDI aangifte CestMocro wegens haatzaaien. Strafrechtelijke aangifte, geen rechterlijke uitspraak. Transmissie via NOS. CIDI is klager en enige bron van de claim.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C12",
        "pattern_strength": "low",
        "transmission_strength": "low",
        "impact_strength": "",
        "capture_risk": "low",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Schoolboek-antisemitism claim door Likoed. Twee campagnes (2015, 2019). Inhalige toets niet onafhankelijk uitgevoerd. Geen bekend correctie-effect. Lage transmissie buiten eigen kanalen.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C13",
        "pattern_strength": "medium",
        "transmission_strength": "high",
        "impact_strength": "",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "CIDI veiligheidsframe in HU-case. Transmissie via Telegraaf -> GeenStijl -> politici. Impact meetbaar (uitstel). Veiligheidsclaim uitsluitend van CIDI, niet extern geverifieerd. Patroon herkenbaar uit eerdere CIDI-interventies.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C14",
        "pattern_strength": "low",
        "transmission_strength": "low",
        "impact_strength": "",
        "capture_risk": "low",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Wierd Duk 'Palestinisering'-frame. Eenmalige opinie-uiting. Geen transmissie naar politiek of beleid. Relevant als indicator van discours maar geen campagnepatroon.",
        "review_status": "draft",
    },
    {
        "entity_type": "claim",
        "entity_id": "C15",
        "pattern_strength": "medium",
        "transmission_strength": "medium",
        "impact_strength": "",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "",
        "assessment_basis": "Antizionisme = antisemitisme frame. Breder discours-frame, niet case-specifiek. Herkenbaar in CIDI-communicatie en Bart Schut-publicaties. Moeilijk te kwantificeren want discours-frame, geen incident.",
        "review_status": "draft",
    },
]

write_csv("epistemic_assessments.csv", assessments)
print(f"epistemic_assessments.csv: {len(assessments)} entries written")

# ── 2. Refactor update_epistemic_model.py to read from CSV ──

# The update_epistemic_model.py should read from this CSV.
# For now, verify all cases and claims are covered
existing_case_ids = {r["case_id"] for r in read_csv("cases.csv")}
existing_claim_ids = {r["claim_id"] for r in read_csv("claims.csv")}

assessed_case_ids = {r["entity_id"] for r in assessments if r["entity_type"] == "case"}
assessed_claim_ids = {r["entity_id"] for r in assessments if r["entity_type"] == "claim"}

missing_cases = existing_case_ids - assessed_case_ids
missing_claims = existing_claim_ids - assessed_claim_ids
extra_cases = assessed_case_ids - existing_case_ids
extra_claims = assessed_claim_ids - existing_claim_ids

if missing_cases:
    print(f"WARNING: cases missing from assessments: {missing_cases}")
if missing_claims:
    print(f"WARNING: claims missing from assessments: {missing_claims}")
if extra_cases:
    print(f"WARNING: assessments for non-existent cases: {extra_cases}")
if extra_claims:
    print(f"WARNING: assessments for non-existent claims: {extra_claims}")
if not (missing_cases or missing_claims or extra_cases or extra_claims):
    print("Coverage: all 10 cases + 15 claims have assessments")

# Validate allowed values
for row in assessments:
    for field in ["pattern_strength", "transmission_strength", "impact_strength",
                  "capture_risk", "independent_verification_level", "institutional_self_interest"]:
        val = row.get(field, "")
        if val and val not in ALLOWED:
            print(f"  INVALID {row['entity_type']}/{row['entity_id']}: {field}={val}")

# ── 3. Apply assessments to cases.csv and claims.csv ──

def apply_assessments(target_file, type_key, id_key):
    rows = read_csv(target_file)
    # Add new cols if missing
    extra_cols = ["pattern_strength", "transmission_strength", "impact_strength",
                  "capture_risk", "independent_verification_level", "institutional_self_interest",
                  "assessment_basis", "review_status"]
    header = list(rows[0].keys())
    for c in extra_cols:
        if c not in header:
            header.append(c)

    assessment_map = {}
    for a in assessments:
        if a["entity_type"] == type_key:
            assessment_map[a["entity_id"]] = a

    for row in rows:
        eid = row[id_key]
        if eid in assessment_map:
            a = assessment_map[eid]
            for c in extra_cols:
                row[c] = a.get(c, "")
        else:
            for c in extra_cols:
                row.setdefault(c, "unknown")

    out = [{k: row.get(k, "") for k in header} for row in rows]
    write_csv(target_file, out)
    n = sum(1 for r in out if r.get("pattern_strength") in ALLOWED - {"unknown"})
    print(f"{target_file}: updated {n} entries with assessment data")

apply_assessments("cases.csv", "case", "case_id")
apply_assessments("claims.csv", "claim", "claim_id")

# ── 4. Fill copy_overlap.csv ──

articles = read_csv("articles.csv")
edges = read_csv("edges.csv")
article_links = read_csv("article_claim_links.csv")

def year(date_str):
    try:
        return int(str(date_str)[:4])
    except (ValueError, TypeError):
        return None

pairs_added = set()
copy_overlap = []

# Strategy A: articles by the same publisher sharing a claim
# (e.g., multiple TRF articles all linked to C3)
claim_articles = {}  # claim_id -> list of article_ids
for link in article_links:
    claim_articles.setdefault(link["claim_id"], set()).add(link["article_id"])

for cid, aids in claim_articles.items():
    aids = list(aids)
    for i in range(len(aids)):
        for j in range(i + 1, len(aids)):
            a1, a2 = aids[i], aids[j]
            art1 = next((a for a in articles if a["article_id"] == a1), None)
            art2 = next((a for a in articles if a["article_id"] == a2), None)
            if not art1 or not art2:
                continue
            y1, y2 = year(art1.get("publication_date", "")), year(art2.get("publication_date", ""))
            if not y1 or not y2:
                continue
            pair_key = tuple(sorted([a1, a2]))
            if pair_key in pairs_added:
                continue
            pairs_added.add(pair_key)
            copy_overlap.append({
                "overlap_id": f"CO_claim_{cid}_{i}_{j}",
                "source_article_id": a1,
                "target_article_id": a2,
                "source_type": "article",
                "target_type": "article",
                "overlap_score": "",
                "method": "shared_claim",
                "notes": f"Both linked to claim {cid}; publisher {art1.get('publisher_id','')} ({y1}) -> {art2.get('publisher_id','')} ({y2})",
            })

# Strategy B: articles whose source_ids overlap
# (e.g., two articles both citing S_ELSC_2021)
article_source_map = {}
for a in articles:
    sids = set(s.strip() for s in a.get("source_ids", "").split(";") if s.strip())
    if sids:
        article_source_map[a["article_id"]] = sids

all_aids = list(article_source_map.keys())
for i in range(len(all_aids)):
    for j in range(i + 1, len(all_aids)):
        a1, a2 = all_aids[i], all_aids[j]
        shared_sources = article_source_map[a1] & article_source_map[a2]
        if len(shared_sources) < 2:  # need at least 2 shared sources
            continue
        art1 = next((a for a in articles if a["article_id"] == a1), None)
        art2 = next((a for a in articles if a["article_id"] == a2), None)
        if not art1 or not art2:
            continue
        pair_key = tuple(sorted([a1, a2]))
        if pair_key in pairs_added:
            continue
        pairs_added.add(pair_key)
        y1, y2 = year(art1.get("publication_date", "")), year(art2.get("publication_date", ""))
        copy_overlap.append({
            "overlap_id": f"CO_source_{a1[:10]}_{a2[:10]}",
            "source_article_id": a1,
            "target_article_id": a2,
            "source_type": "article",
            "target_type": "article",
            "overlap_score": "",
            "method": "shared_sources",
            "notes": f"Shared sources: {', '.join(shared_sources)}. {art1.get('publisher_id','')} ({y1}) <-> {art2.get('publisher_id','')} ({y2})",
        })

# Strategy C: watchdog publisher -> media publisher via edges (FRAME_SUPPLY/MEDIA_AMPLIFICATION)
watchdog_publishers = {"NGO_MONITOR", "ELSC", "TRF"}
media_publishers = {
    "TELEGRAAF", "JOODS_NL", "NOS", "NIW", "JONET", "GEENSTIJL",
    "VILLAMEDIA", "CVANDAAG", "NIEUWS_VD_DAG", "CVI_MEDIA",
    "NPO_RADIO1", "EW", "HOP", "NRC",
}

for e in edges:
    etype = e.get("edge_type", "")
    if etype not in ("FRAME_SUPPLY", "MEDIA_AMPLIFICATION", "COUNTER_DOCUMENTATION"):
        continue
    src = e.get("source_id", "")
    tgt = e.get("target_id", "")
    if src not in watchdog_publishers and src not in media_publishers:
        continue
    if tgt not in watchdog_publishers and tgt not in media_publishers:
        continue
    # Find articles by these publishers within 2 years
    src_arts = [a for a in articles if a.get("publisher_id") == src]
    tgt_arts = [a for a in articles if a.get("publisher_id") == tgt]
    for sa in src_arts:
        sy = year(sa.get("publication_date", ""))
        if not sy:
            continue
        for ta in tgt_arts:
            ty = year(ta.get("publication_date", ""))
            if not ty:
                continue
            if abs(ty - sy) > 2:
                continue
            pair_key = tuple(sorted([sa["article_id"], ta["article_id"]]))
            if pair_key in pairs_added:
                continue
            pairs_added.add(pair_key)
            copy_overlap.append({
                "overlap_id": f"CO_{e['edge_id']}_{sa['article_id'][:10]}_{ta['article_id'][:10]}",
                "source_article_id": sa["article_id"],
                "target_article_id": ta["article_id"],
                "source_type": "article",
                "target_type": "article",
                "overlap_score": "",
                "method": f"edge_{etype.lower()}",
                "notes": f"Via {etype}: {src} ({sy}) -> {tgt} ({ty}). {e.get('relation_label','')}",
            })

write_csv("copy_overlap.csv", copy_overlap)
print(f"copy_overlap.csv: {len(copy_overlap)} pairs written")

# ── 5. Write refactored update_script ──

# The update_epistemic_model.py should be rewritten to read from the CSV
update_script = """#!/usr/bin/env python3
\"\"\"Apply epistemic assessments from epistemic_assessments.csv to cases.csv and claims.csv.\"\"\"

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
"""

with open(V5 / "scripts" / "update_epistemic_model.py", "w", encoding="utf-8") as f:
    f.write(update_script)
print("scripts/update_epistemic_model.py: refactored to read from epistemic_assessments.csv")

print("\nv5.1 complete.")
