#!/usr/bin/env python3
"""
Commit 3: Import full raw lead list into research entities/edges.
Commit 7: Case saturation - expand article-level provenance.
"""

import csv
from pathlib import Path

V5 = Path(r"C:\Users\gewoo\israel nederland lobbie\v5")

def read_csv(name):
    p = V5 / name
    if not p.exists(): return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(name, rows, header=None):
    if not rows: return
    h = header or list(rows[0].keys())
    with open(V5 / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=h, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)

# ═══════════════════════════════════════════════════════════════
# COMMIT 3: Expand research_entities with full lead list
# ═══════════════════════════════════════════════════════════════

existing = read_csv("research_entities.csv")
existing_ids = {r["entity_id"] for r in existing}

def add_entities(new_entries):
    for e in new_entries:
        if e["entity_id"] not in existing_ids:
            existing.append(e)
            existing_ids.add(e["entity_id"])

# ── 3a. More politicians ──
add_entities([
    {"entity_id":"HARRY_V_DM", "label":"Harry van der Molen", "entity_type":"POLITICIAN","sub_type":"MP_CDA","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"question_actor","public_status":"known","why_relevant":"CDA-Kamerlid; betrokken bij Israël/Palestina-dossiers","related_cases":"","related_claims":"","known_aliases":"Harry van der Molen","source_hint":"TK-dossier","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":"Check Kamervragen over Israël/Palestina"},
    {"entity_id":"KATHY_HOOGENBOOM", "label":"Kathy Hoogeboom", "entity_type":"POLITICIAN","sub_type":"MP_D66","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"question_actor","public_status":"known","why_relevant":"D66-Kamerlid; buitenland/Israël","related_cases":"","related_claims":"","known_aliases":"","source_hint":"TK-dossier","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
    {"entity_id":"JAN_PATERNICHEL", "label":"Jan Paternotte", "entity_type":"POLITICIAN","sub_type":"MP_D66","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"question_actor","public_status":"known","why_relevant":"D66-Kamerlid; buitenland/defensie; mogelijk betrokken bij Israël/Palestina-dossiers","related_cases":"","related_claims":"","known_aliases":"","source_hint":"TK-dossier","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
    {"entity_id":"KATI_PIRI", "label":"Kati Piri", "entity_type":"POLITICIAN","sub_type":"MEP_PvdA","country":"NL","scope":"NL/EU","tier_guess":"T3","role_guess":"eu_foreign_policy","public_status":"known","why_relevant":"PvdA-Europarlementariër; buitenlandbeleid inclusief Israël/Palestina","related_cases":"","related_claims":"","known_aliases":"","source_hint":"EP-dossier","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
    {"entity_id":"THIJS_REUTEN", "label":"Thijs Reuten", "entity_type":"POLITICIAN","sub_type":"MEP_PvdA","country":"NL","scope":"NL/EU","tier_guess":"T3","role_guess":"eu_foreign_policy","public_status":"known","why_relevant":"PvdA-Europarlementariër; mensenrechten/buitenland; Israël/Palestina-dossiers","related_cases":"","related_claims":"","known_aliases":"","source_hint":"EP-dossier","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
    {"entity_id":"TOM_V_D_LEE", "label":"Tom van der Lee", "entity_type":"POLITICIAN","sub_type":"MP_GroenLinks","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"question_actor","public_status":"known","why_relevant":"GL-Kamerlid; buitenland/ontwikkelingssamenwerking; betrokken bij NGO/Palestina-dossiers","related_cases":"","related_claims":"","known_aliases":"","source_hint":"TK-dossier","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
    {"entity_id":"STEPHAN_V_BAAK", "label":"Stephan van Baarle", "entity_type":"POLITICIAN","sub_type":"MP_DENK","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"counter_voice","public_status":"known","why_relevant":"DENK-Kamerlid; Palestina-positie; tegenhanger van pro-Israël-framing","related_cases":"","related_claims":"","known_aliases":"","source_hint":"TK-dossier","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
])

# ── 3b. More journalists & media personalities ──
add_entities([
    {"entity_id":"SJOERD_GROESKAMP", "label":"Sjoerd Groeskamp", "entity_type":"JOURNALIST","sub_type":"independent","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"investigative_journalist","public_status":"known","why_relevant":"Onafhankelijk onderzoeksjournalist; publiceert over lobby, financiering, invloed","related_cases":"","related_claims":"","known_aliases":"","source_hint":"Publicaties; sociale media","source_ids":"","current_status":"candidate_actor","priority":"P2","notes":"Lead: mogelijk relevant voor lobby/invloed-dossiers"},
    {"entity_id":"CHRIS_AALBERTS", "label":"Chris Aalberts", "entity_type":"JOURNALIST","sub_type":"independent","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"investigative_journalist","public_status":"known","why_relevant":"Onderzoeksjournalist politiek; publiceert over lobby, partijen, invloed","related_cases":"","related_claims":"","known_aliases":"","source_hint":"Publicaties","source_ids":"","current_status":"candidate_actor","priority":"P2","notes":"Lead: check publicaties over pro-Israël lobby in NL"},
    {"entity_id":"PETER_MALCONTENT", "label":"Peter Malcontent", "entity_type":"ACADEMIC","sub_type":"historian","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"academic_source","public_status":"known","why_relevant":"Historicus UU; publiceerde over Nederlands-Israëlisch buitenlandbeleid (bron S_MALCONTENT_2022)","related_cases":"","related_claims":"","known_aliases":"","source_hint":"UU-publicatie","source_ids":"S_MALCONTENT_2022","current_status":"candidate_actor","priority":"P2","notes":"Al als bron in sources.csv. Academiche context voor NL-IL beleid."},
    {"entity_id":"REEK_V_D_MEEREN", "label":"Reek van de Meeren", "entity_type":"JOURNALIST","sub_type":"follow_the_money","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"investigative_journalist","public_status":"known","why_relevant":"Follow the Money; onderzoekt lobby en financieringsstromen","related_cases":"","related_claims":"","known_aliases":"","source_hint":"FTM-publicaties","source_ids":"","current_status":"candidate_actor","priority":"P2","notes":"Lead: check of FMT over pro-Israël lobby in NL heeft gepubliceerd"},
    {"entity_id":"DENISE_HILLE", "label":"Denise Hille", "entity_type":"JOURNALIST","sub_type":"follow_the_money","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"investigative_journalist","public_status":"known","why_relevant":"Follow the Money; onderzoekt lobby en invloed","related_cases":"","related_claims":"","known_aliases":"","source_hint":"FTM-publicaties","source_ids":"","current_status":"candidate_actor","priority":"P2","notes":""},
    {"entity_id":"JESSIE_KALLE", "label":"Jessie Kalle", "entity_type":"JOURNALIST","sub_type":"joop_vara","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"opinion_journalist","public_status":"known","why_relevant":"Joop (VARA) columnist; publiceert over Israël/Palestina","related_cases":"","related_claims":"","known_aliases":"","source_hint":"Joop-publicaties","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
    {"entity_id":"ANNE_V_D_WEERD", "label":"Anne van der Weerd", "entity_type":"JOURNALIST","sub_type":"nrc","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"investigative_journalist","public_status":"known","why_relevant":"NRC-journalist; schreef over NGO Monitor/Israël-lobby","related_cases":"CASE_NGO_OXFAM_2026","related_claims":"C6","known_aliases":"","source_hint":"NRC artikel over NGO Monitor","source_ids":"S_NGOMONITOR_RESPONSE_NRC_2026","current_status":"candidate_actor","priority":"P1","notes":"NRC-artikel over NGO Monitor was aanleiding voor NGO Monitor-rebuttal. Zeer relevant."},
    {"entity_id":"DERK_STOKMANS", "label":"Derk Stokmans", "entity_type":"JOURNALIST","sub_type":"nrc","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"investigative_journalist","public_status":"known","why_relevant":"NRC-journalist; co-auteur NGO Monitor-artikel","related_cases":"CASE_NGO_OXFAM_2026","related_claims":"C6","known_aliases":"","source_hint":"NRC artikel","source_ids":"S_NGOMONITOR_RESPONSE_NRC_2026","current_status":"candidate_actor","priority":"P1","notes":"Co-auteur met Anne van der Weerd"},
    {"entity_id":"JAN_KRIJGER", "label":"Jan Krijger", "entity_type":"JOURNALIST","sub_type":"nrc","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"editor","public_status":"known","why_relevant":"NRC-redacteur; mogelijk betrokken bij NGO Monitor-artikel","related_cases":"","related_claims":"","known_aliases":"","source_hint":"NRC","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":"Lead: NRC-redactie buitenland"},
    {"entity_id":"JESSICA_V_LITH", "label":"Jessica van Lith", "entity_type":"JOURNALIST","sub_type":"trouw","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"journalist","public_status":"known","why_relevant":"Trouw; buitenlandredactie; mogelijk over Israël/Palestina","related_cases":"","related_claims":"","known_aliases":"","source_hint":"Trouw","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
    {"entity_id":"MARLOES_VAN_H", "label":"Marloes van H.", "entity_type":"JOURNALIST","sub_type":"trouw","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"journalist","public_status":"known","why_relevant":"Trouw-journalist; schrijft over mensenrechten/buitenland","related_cases":"","related_claims":"","known_aliases":"","source_hint":"Trouw","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
])

# ── 3c. More PR/lobby firms ──
add_entities([
    {"entity_id":"PUBLIC_ONE", "label":"Public One", "entity_type":"PR_FIRM","sub_type":"communications","country":"NL","scope":"NL","tier_guess":"T2","role_guess":"political_communications","public_status":"known","why_relevant":"Political communications bureau; werkt met politici en advocacy","related_cases":"","related_claims":"","known_aliases":"Public One","source_hint":"Website; opdrachtgevers","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":"Lead: check of betrokken bij pro-Israël campagnes"},
    {"entity_id":"BKB", "label":"Bureau Buitenlandse Betrekkingen / BKB", "entity_type":"PR_FIRM","sub_type":"campaign_bureau","country":"NL","scope":"NL","tier_guess":"T2","role_guess":"campaign_consultant","public_status":"known","why_relevant":"Campagnebureau; werkt met NGO's en advocacy","related_cases":"","related_claims":"","known_aliases":"BKB","source_hint":"Website","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
    {"entity_id":"DE_PRAKTIJK", "label":"De Praktijk", "entity_type":"PR_FIRM","sub_type":"communications","country":"NL","scope":"NL","tier_guess":"T2","role_guess":"communications_advice","public_status":"known","why_relevant":"Communicatiebureau; werkt met politiek en beleid","related_cases":"","related_claims":"","known_aliases":"","source_hint":"Website","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
    {"entity_id":"DRIFT", "label":"Drift", "entity_type":"PR_FIRM","sub_type":"strategy","country":"NL","scope":"NL","tier_guess":"T2","role_guess":"strategy_consultant","public_status":"known","why_relevant":"Strategiebureau; lobby en advies","related_cases":"","related_claims":"","known_aliases":"Drift","source_hint":"Website","source_ids":"","current_status":"candidate_actor","priority":"P3","notes":""},
])

# ── 3d. More foundations & donors ──
add_entities([
    {"entity_id":"RVO", "label":"Rijksdienst voor Ondernemend Nederland (RVO)", "entity_type":"GOVERNMENT_AGENCY","sub_type":"subsidy_executor","country":"NL","scope":"NL","tier_guess":"T1","role_guess":"subsidy_gatekeeper","public_status":"known","why_relevant":"Uitvoerder van Nederlandse subsidies; relevant voor NGO-financiering","related_cases":"","related_claims":"","known_aliases":"Rijksdienst voor Ondernemend Nederland; RVO","source_hint":"RVO-subsidieregister","source_ids":"","current_status":"candidate_actor","priority":"P2","notes":"Gatekeeper voor ontwikkelingssamenwerkingssubsidies"},
    {"entity_id":"BUZA", "label":"Ministerie van Buitenlandse Zaken", "entity_type":"GOVERNMENT_AGENCY","sub_type":"ministry","country":"NL","scope":"NL","tier_guess":"T0","role_guess":"policy_funder","public_status":"confirmed_actor","why_relevant":"Verantwoordelijk voor buitenlandbeleid, subsidies, Mensenrechtenfonds","related_cases":"CASE_NGO_OXFAM_2026","related_claims":"","known_aliases":"BuZa; Buitenlandse Zaken","source_hint":"Rijksbegroting","source_ids":"S_TK_NGOMONITOR_2026_VVD","current_status":"candidate_actor","priority":"P1","notes":"DUTCH_GOV in actors.csv is breder; BuZa specifiek voor buitenlandbeleid"},
    {"entity_id":"MENSENRECHTENFONDS", "label":"Mensenrechtenfonds (BuZa)", "entity_type":"GOVERNMENT_PROGRAM","sub_type":"funding_program","country":"NL","scope":"NL","tier_guess":"T2","role_guess":"subsidy_program","public_status":"known","why_relevant":"BuZa-fonds voor mensenrechten; financiert ook Palestijnse NGO's","related_cases":"","related_claims":"","known_aliases":"Human Rights Fund","source_hint":"BuZa-begroting","source_ids":"","current_status":"candidate_actor","priority":"P2","notes":""},
    {"entity_id":"IJH", "label":"Internationaal Jongeren Hulp Fonds", "entity_type":"FOUNDATION","sub_type":"dutch_funding","country":"NL","scope":"NL","tier_guess":"T3","role_guess":"subsidy_channel","public_status":"known","why_relevant":"Nederlands fonds voor jongeren/ontwikkeling; mogelijk relevant voor NGO-financiering","related_cases":"","related_claims":"","known_aliases":"","source_hint":"","source_ids":"","current_status":"raw_lead","priority":"P4","notes":""},
    {"entity_id":"OXFAM_NOVIB_FUND", "label":"Oxfam Novib (eigen fondsenwerving)", "entity_type":"FOUNDATION","sub_type":"ngo_fundraising","country":"NL","scope":"NL","tier_guess":"T2","role_guess":"fundraiser","public_status":"known","why_relevant":"Oxfam Novib werft eigen middelen naast overheidssubsidies","related_cases":"CASE_NGO_OXFAM_2026","related_claims":"","known_aliases":"","source_hint":"Oxfam Novib jaarverslag","source_ids":"","current_status":"candidate_actor","priority":"P2","notes":"Scheiding publieke vs private financiering van Oxfam Novib"},
    {"entity_id":"ADELPHI_FUND", "label":"Adelphi Foundation", "entity_type":"FOUNDATION","sub_type":"donor_us","country":"US","scope":"US","tier_guess":"T3","role_guess":"funder","public_status":"known","why_relevant":"NGO Monitor donor","related_cases":"","related_claims":"","known_aliases":"","source_hint":"NGO Monitor filings","source_ids":"","current_status":"raw_lead","priority":"P3","notes":"Zoek filing voor bevestiging"},
    {"entity_id":"HILTON_FOUNDATION", "label":"Conrad N. Hilton Foundation", "entity_type":"FOUNDATION","sub_type":"donor_us","country":"US","scope":"US","tier_guess":"T2","role_guess":"funder","public_status":"known","why_relevant":"Grote US foundation; mogelijke donor voor pro-Israël of Palestijnse NGO's","related_cases":"","related_claims":"","known_aliases":"Hilton Foundation","source_hint":"Foundation filings","source_ids":"","current_status":"raw_lead","priority":"P3","notes":""},
])

# ── 3e. More candidate edges ──
existing_edges = read_csv("research_edges.csv")
existing_edge_keys = {(r["source_label"], r["target_label"], r["proposed_edge_type"]) for r in existing_edges}

def add_edges(new_edges):
    for e in new_edges:
        key = (e["source_label"], e["target_label"], e["proposed_edge_type"])
        if key not in existing_edge_keys:
            existing_edges.append(e)
            existing_edge_keys.add(key)

add_edges([
    {"research_edge_id":"RE_NRC_NGOMONITOR", "source_label":"NRC", "target_label":"NGO_MONITOR", "proposed_edge_type":"COUNTER_DOCUMENTATION", "mechanism_guess":"NRC publiceert kritisch artikel over NGO Monitor", "why_relevant":"NRC-artikel leidt tot NGO Monitor-rebuttal; inhoudelijke betwisting", "related_case":"CASE_NGO_OXFAM_2026", "related_claim":"C6", "current_trace_level":"official_record", "needed_evidence":"NRC-artikel (aanwezig via S_NGOMONITOR_RESPONSE_NRC_2026)", "priority":"P1", "status":"trace_found", "notes":"NGO Monitor publiceerde rebuttal op NRC-artikel"},
    {"research_edge_id":"RE_ELSC_OXFAM", "source_label":"ELSC", "target_label":"OXFAM_NOVIB", "proposed_edge_type":"COUNTER_DOCUMENTATION", "mechanism_guess":"ELSC documenteert NGO Monitor-druk op Oxfam", "why_relevant":"ELSC-rapport is backbone voor Oxfam-case", "related_case":"CASE_NGO_OXFAM_2026", "related_claim":"C8", "current_trace_level":"official_record", "needed_evidence":"ELSC-rapport (aanwezig)", "priority":"P1", "status":"trace_found", "notes":""},
    {"research_edge_id":"RE_VVD_HU_PRESSURE", "source_label":"VVD", "target_label":"HU", "proposed_edge_type":"PUBLIC_PRESSURE", "mechanism_guess":"VVD-leider Yesilgöz oefent publieke druk uit op HU na CIDI-klacht", "why_relevant":"Directe politieke druk op onderwijsinstelling", "related_case":"CASE_HU_CIDI_2024", "related_claim":"C13", "current_trace_level":"official_record", "needed_evidence":"Al als edge in v5: E047, E068", "priority":"P1", "status":"trace_found", "notes":""},
    {"research_edge_id":"RE_PVV_HU", "source_label":"PVV", "target_label":"HU", "proposed_edge_type":"PUBLIC_PRESSURE", "mechanism_guess":"PVV-leider Wilders / fractie reageert op HU-case", "why_relevant":"PVV mogelijk betrokken bij politieke druk op HU", "related_case":"CASE_HU_CIDI_2024", "related_claim":"C13", "current_trace_level":"name_overlap", "needed_evidence":"Check of PVV-Kamerlid reageerde op HU-case", "priority":"P2", "status":"needs_source", "notes":"Markuszower/Lammers zijn actief in NGO Monitor-dossier; check of ze ook HU-case oppakten"},
    {"research_edge_id":"RE_CIDI_WILDERS", "source_label":"CIDI", "target_label":"PVV", "proposed_edge_type":"POLITICAL_ALIGNMENT", "mechanism_guess":"CIDI-framing sluit aan bij PVV-standpunten over Israël", "why_relevant":"PVV gebruikt CIDI-achtige framing in Kamervragen", "related_case":"CASE_ALMEZAN_2020;CASE_NGO_OXFAM_2026", "related_claim":"C8;C9", "current_trace_level":"media_sequence", "needed_evidence":"Check CIDI-communicatie voorafgaand aan PVV-Kamervragen", "priority":"P2", "status":"needs_source", "notes":"PVV-Kamerleden Markuszower en Lammers actief in NGO Monitor-dossier"},
    {"research_edge_id":"RE_IAF_CU", "source_label":"IAF", "target_label":"CU", "proposed_edge_type":"PARLIAMENTARY_ACCESS", "mechanism_guess":"CU-Kamerleden (Voordewind, Ceder) betrokken bij IAF-caucus", "why_relevant":"CU historisch betrokken bij IAF/IIACF", "related_case":"CASE_IAF_CAUCUS_2013", "related_claim":"", "current_trace_level":"official_record", "needed_evidence":"Al als edge in v5: E018", "priority":"P2", "status":"trace_found", "notes":"Voordewind was mede-oprichter; Ceder genoemd in TRF-rapport"},
    {"research_edge_id":"RE_VVD_CIDI_DATA", "source_label":"VVD", "target_label":"CIDI", "proposed_edge_type":"DATA_USE", "mechanism_guess":"VVD gebruikt CIDI-data over stemgedrag in debatten", "why_relevant":"CIDI levert Tweede Kamer-stemdata via NIW; VVD gebruikt dit", "related_case":"", "related_claim":"", "current_trace_level":"media_sequence", "needed_evidence":"NIW-artikel met CIDI-data (aanwezig). Check VVD-gebruik in debatten.", "priority":"P2", "status":"needs_source", "notes":"CIDI-data gepubliceerd in NIW, mogelijk gebruikt door VVD in Kamer"},
    {"research_edge_id":"RE_TRF_ELSC", "source_label":"TRF", "target_label":"ELSC", "proposed_edge_type":"COUNTER_ADVOCACY_COALITION", "mechanism_guess":"TRF en ELSC delen counter-documentatie-doelen", "why_relevant":"Beide actoren documenteren pro-Israël lobby in NL", "related_case":"", "related_claim":"", "current_trace_level":"shared_source", "needed_evidence":"Check of TRF ELSC citeert of vice versa", "priority":"P2", "status":"needs_source", "notes":"Beide counter-actors; mogelijk coördinatie of shared framing"},
    {"research_edge_id":"RE_NGO_MONITOR_RIGHTSFORUM", "source_label":"NGO_MONITOR", "target_label":"TRF", "proposed_edge_type":"DOSSIER_TARGETING", "mechanism_guess":"NGO Monitor heeft dossier over TRF", "why_relevant":"NGO Monitor profileert TRF als target", "related_case":"", "related_claim":"C3", "current_trace_level":"official_record", "needed_evidence":"NGO Monitor website TRF-pagina (aanwezig via edge E067)", "priority":"P1", "status":"trace_found", "notes":"Al als edge in v5: E067"},
    {"research_edge_id":"RE_TELEGRAAF_WILDERS", "source_label":"TELEGRAAF", "target_label":"PVV", "proposed_edge_type":"FRAME_ALIGNMENT", "mechanism_guess":"Telegraaf en PVV delen frame over NGO Monitor/Oxfam", "why_relevant":"PVV baseert Kamervragen op Telegraaf-artikel", "related_case":"CASE_NGO_OXFAM_2026;CASE_ALMEZAN_2020", "related_claim":"C8;C9", "current_trace_level":"official_record", "needed_evidence":"Al als edge in v5: E076. PVV Kamervragen verwijzen naar Telegraaf.", "priority":"P1", "status":"trace_found", "notes":"PVV Kamervragen Al Mezan obv Telegraaf/Joods.nl (ELSC) + Oxfam obv Telegraaf/NGO Monitor (Kamerstuk)"},
    {"research_edge_id":"RE_CIDI_NETWORK_GENERAL", "source_label":"CIDI", "target_label":"MEDIA_CLUSTER_NL", "proposed_edge_type":"FRAME_AMPLIFICATION", "mechanism_guess":"CIDI heeft structurele mediatoegang via NIW, Jonet, Telegraaf, NOS", "why_relevant":"CIDI meet 172 media-dagen in 2024; structurele media-aanwezigheid", "related_case":"", "related_claim":"C1;C4", "current_trace_level":"official_record", "needed_evidence":"CIDI Activiteitenoverzicht (S_CIDI_ACTIVITY_2024)", "priority":"P1", "status":"trace_found", "notes":"CIDI self-report. Structurele media-amplificatie."},
])

write_csv("research_entities.csv", existing)
write_csv("research_edges.csv", existing_edges)
print(f"research_entities.csv: {len(existing)} entries (after Commit 3 expansion)")
print(f"research_edges.csv: {len(existing_edges)} entries")

# ═══════════════════════════════════════════════════════════════
# COMMIT 7: Case saturation - expand articles and provenance
# ═══════════════════════════════════════════════════════════════

# We can't add new articles without URLs and dates (research task),
# but we CAN update article_claim_links and parliamentary_claim_links
# with more accurate links based on what we now know.

articles = read_csv("articles.csv")
article_links = read_csv("article_claim_links.csv")
parl_links = read_csv("parliamentary_claim_links.csv")

existing_acl = {(r["article_id"], r["claim_id"]) for r in article_links}
existing_pcl = {(r["parliamentary_item_id"], r["claim_id"]) for r in parl_links}

# Add missing link: NOS CestMocro article -> C11 (legal claim)
if ("ART_NOS_CESTMOCRO_2023", "C11") not in existing_acl:
    article_links.append({
        "link_id": "ACL_NOS_CESTMOCRO_2023_C11",
        "article_id": "ART_NOS_CESTMOCRO_2023",
        "claim_id": "C11",
        "source_actor_id": "NOS",
        "frame_type": "REPORTING",
        "citation_type": "edge_from_graph",
        "text_overlap_score": "",
        "publication_date": "2023",
        "confidence": "high",
        "notes": "NOS reports CIDI legal complaint against CestMocro",
    })
    existing_acl.add(("ART_NOS_CESTMOCRO_2023", "C11"))
    print("Added ACL: NOS CestMocro -> C11")

# Add missing link: NOS HU article -> C13 (safety frame)
if ("ART_NOS_HU_CIDI_2024", "C13") not in existing_acl:
    article_links.append({
        "link_id": "ACL_NOS_HU_CIDI_2024_C13",
        "article_id": "ART_NOS_HU_CIDI_2024",
        "claim_id": "C13",
        "source_actor_id": "NOS",
        "frame_type": "REPORTING",
        "citation_type": "edge_from_graph",
        "publication_date": "2024",
        "text_overlap_score": "",
        "confidence": "high",
        "notes": "NOS reports HU postponement and CIDI safety frame",
    })
    existing_acl.add(("ART_NOS_HU_CIDI_2024", "C13"))
    print("Added ACL: NOS HU -> C13")

# HOP article -> C13
if ("ART_HOP_HU_POLITICI_2024", "C13") not in existing_acl:
    article_links.append({
        "link_id": "ACL_HOP_HU_2024_C13",
        "article_id": "ART_HOP_HU_POLITICI_2024",
        "claim_id": "C13",
        "source_actor_id": "HOP",
        "frame_type": "REPORTING",
        "citation_type": "edge_from_graph",
        "publication_date": "2024",
        "text_overlap_score": "",
        "confidence": "high",
        "notes": "HOP reports political reactions to HU postponement",
    })
    existing_acl.add(("ART_HOP_HU_POLITICI_2024", "C13"))
    print("Added ACL: HOP HU -> C13")

# CIDI press release -> C4 (safety frame) — specifically about safety
if ("ART_CIDI_CESTMOCRO_2023", "C4") not in existing_acl:
    article_links.append({
        "link_id": "ACL_CIDI_PR_C4",
        "article_id": "ART_CIDI_CESTMOCRO_2023",
        "claim_id": "C4",
        "source_actor_id": "CIDI",
        "frame_type": "FRAMING",
        "citation_type": "same_actor",
        "publication_date": "2023",
        "text_overlap_score": "",
        "confidence": "medium",
        "notes": "CIDI press release uses safety/incitement frame; links to C4 safety frame claim",
    })
    existing_acl.add(("ART_CIDI_CESTMOCRO_2023", "C4"))
    print("Added ACL: CIDI press release -> C4")

# Additional ACL: TRF IAF article -> C3 (confirmed)
# TRF IAF article -> also C2 (terror-link as context for IAF)
if ("ART_RIGHTSFORUM_IAF_2025", "C2") not in existing_acl:
    article_links.append({
        "link_id": "ACL_TRF_IAF_2025_C2",
        "article_id": "ART_RIGHTSFORUM_IAF_2025",
        "claim_id": "C2",
        "source_actor_id": "TRF",
        "frame_type": "COUNTER_DOCUMENTATION",
        "citation_type": "same_actor",
        "publication_date": "2025",
        "text_overlap_score": "",
        "confidence": "medium",
        "notes": "TRF links IAF to broader terror-link/delegitimation campaign narrative",
    })
    existing_acl.add(("ART_RIGHTSFORUM_IAF_2025", "C2"))
    print("Added ACL: TRF IAF -> C2")

# Add parliamentary claim link: GOV_NGOMONITOR_UITSTEL_2025 -> C8
if ("GOV_NGOMONITOR_UITSTEL_2025", "C8") not in existing_pcl:
    parl_links.append({
        "link_id": "PCL_UITSTEL_C8",
        "parliamentary_item_id": "GOV_NGOMONITOR_UITSTEL_2025",
        "claim_id": "C8",
        "actor_id": "DUTCH_GOV",
        "link_type": "explicit_relation",
        "publication_date": "2025-02-03",
        "confidence": "high",
        "source_ids": "S_RIJK_NGOMONITOR_2025",
        "notes": "NGO Monitor report enters Dutch parliamentary workflow; triggers case",
    })
    existing_pcl.add(("GOV_NGOMONITOR_UITSTEL_2025", "C8"))
    print("Added PCL: GOV_NGOMONITOR_UITSTEL -> C8")

# Add parliamentary claim link: GOV_DUEDILIGENCE_DRA_2026 -> C8
if ("GOV_DUEDILIGENCE_DRA_2026", "C8") not in existing_pcl:
    parl_links.append({
        "link_id": "PCL_DUEDILIGENCE_C8",
        "parliamentary_item_id": "GOV_DUEDILIGENCE_DRA_2026",
        "claim_id": "C8",
        "actor_id": "DUTCH_GOV",
        "link_type": "explicit_relation",
        "publication_date": "2026",
        "confidence": "high",
        "source_ids": "S_TK_NGOMONITOR_2026_VVD",
        "notes": "Cabinet due-diligence assertion follows from NGO Monitor allegations",
    })
    existing_pcl.add(("GOV_DUEDILIGENCE_DRA_2026", "C8"))
    print("Added PCL: GOV_DUEDILIGENCE -> C8")

# Also add parliamentary claim links for travel registrations to CASE_IAF_CAUCUS_2013
for pid in ["TRAVEL_STOFFER_ELNET_2024", "TRAVEL_STOFFER_CVI_2022"]:
    key = (pid, "CASE_IAF_CAUCUS_2013")
    if (pid, "") not in existing_pcl:
        existing_parl = {r["parliamentary_item_id"] for r in parl_links}
        if pid not in existing_parl:
            parl_row = next((r for r in read_csv("parliamentary_items.csv") if r["item_id"] == pid), None)
            if parl_row:
                parl_links.append({
                    "link_id": f"PCL_travel_{pid}",
                    "parliamentary_item_id": pid,
                    "claim_id": "",
                    "actor_id": parl_row.get("actor_id", ""),
                    "link_type": "case_context",
                    "publication_date": parl_row.get("date", ""),
                    "confidence": "high",
                    "source_ids": parl_row.get("source_ids", ""),
                    "notes": f"Travel registration linked to IAF/ELNET/CVI network context",
                })
                print(f"Added PCL: {pid} -> case context")

write_csv("article_claim_links.csv", article_links)
write_csv("parliamentary_claim_links.csv", parl_links)
print(f"\narticle_claim_links.csv: {len(article_links)} entries (after case saturation)")
print(f"parliamentary_claim_links.csv: {len(parl_links)} entries")

# ── Update edges with claim_id for better provenance ──
# Some edges in v5 don't have claim_ids that they should have
edges = read_csv("edges.csv")
claim_by_case = {}
for c in read_csv("cases.csv"):
    cid = c.get("claim_id", "")
    if cid:
        claim_by_case[c["case_id"]] = cid

added_claims = 0
for e in edges:
    ecid = e.get("case_id", "")
    eclaim = e.get("claim_id", "")
    if ecid in claim_by_case and not eclaim:
        # Find the right claim from the edge context
        if e.get("source_type") == "claim":
            e["claim_id"] = e["source_id"]
            added_claims += 1
        elif e.get("target_type") == "claim":
            e["claim_id"] = e["target_id"]
            added_claims += 1
        elif e.get("edge_type") in ("PARLIAMENTARY_QUESTION", "OFFICIAL_NONCONFIRMATION",
                                     "MEDIA_AMPLIFICATION", "FRAME_SUPPLY"):
            e["claim_id"] = claim_by_case.get(ecid, "")
            added_claims += 1

# Ensure claim_id column exists in edges
header = list(edges[0].keys()) if edges else []
if "claim_id" not in header:
    header.insert(12, "claim_id")
for e in edges:
    e.setdefault("claim_id", "")
# Write to temp file first, then rename
import os, tempfile
tmp = V5 / "edges.csv.tmp"
with open(tmp, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=header, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    w.writerows(edges)
os.replace(str(tmp), str(V5 / "edges.csv"))
print(f"edges.csv: {added_claims} edges updated with claim_id ({len(edges)} rows)")

print("\nCommit 3 + Commit 7 complete.")
