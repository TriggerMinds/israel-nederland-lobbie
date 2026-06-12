#!/usr/bin/env python3
"""
Build the research intelligence layer (RAW/TRIAGE mode).
Commit 1: Research vault tables
Commit 2: Donor infrastructure
Commit 4: Source dependency
Commit 6: Social / public figures expansion
"""

import csv, re
from pathlib import Path
from collections import defaultdict

V5 = Path(r"C:\Users\gewoo\israel nederland lobbie\v5")

def read_csv(name):
    p = V5 / name
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(name, rows):
    if not rows:
        return
    with open(V5 / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)

def append_csv(name, rows):
    existing = read_csv(name)
    existing += rows
    write_csv(name, existing)

# ═══════════════════════════════════════════════════════════════
# COMMIT 1: Research vault
# ═══════════════════════════════════════════════════════════════

# ── 1a. research_entities.csv ──

ENTITY_HEADER = [
    "entity_id","label","entity_type","sub_type","country","scope",
    "tier_guess","role_guess","public_status",
    "why_relevant","related_cases","related_claims",
    "known_aliases","source_hint","source_ids",
    "current_status","priority","notes"
]

research_entities = [
    # ===== DONORS / FOUNDATIONS =====
    {
        "entity_id": "WECHSLER_FOUNDATION",
        "label": "Wechsler Family Foundation",
        "entity_type": "FOUNDATION",
        "sub_type": "donor_us",
        "country": "US",
        "scope": "US/IL",
        "tier_guess": "T1",
        "role_guess": "funder",
        "public_status": "known_donor",
        "why_relevant": "NGO Monitor donor via foundation filings",
        "related_cases": "CASE_NGO_OXFAM_2026",
        "related_claims": "C6",
        "known_aliases": "Wechsler Family Foundation",
        "source_hint": "NGO Monitor donor disclosure",
        "source_ids": "",
        "current_status": "raw_lead",
        "priority": "P1",
        "notes": "Zoek filing voor directe link met NGO Monitor",
    },
    {
        "entity_id": "REPORT_ORG",
        "label": "REPORT / Religious Exceptionalism Project",
        "entity_type": "FOUNDATION",
        "sub_type": "donor_us",
        "country": "US",
        "scope": "US/IL",
        "tier_guess": "T2",
        "role_guess": "funder",
        "public_status": "known_donor",
        "why_relevant": "NGO Monitor donor",
        "related_cases": "CASE_NGO_OXFAM_2026",
        "related_claims": "",
        "known_aliases": "Religious Exceptionalism Project; REPORT",
        "source_hint": "NGO Monitor filings",
        "source_ids": "",
        "current_status": "raw_lead",
        "priority": "P1",
        "notes": "",
    },
    {
        "entity_id": "FELNET",
        "label": "Friends of ELNET",
        "entity_type": "FOUNDATION",
        "sub_type": "donor_us",
        "country": "US",
        "scope": "US/IL/EU",
        "tier_guess": "T1",
        "role_guess": "funder",
        "public_status": "known_donor",
        "why_relevant": "Funding conduit for ELNET activities",
        "related_cases": "CASE_IAF_CAUCUS_2013",
        "related_claims": "",
        "known_aliases": "Friends of ELNET; FELNET",
        "source_hint": "ELNET impact report",
        "source_ids": "S_ELNET_IMPACT",
        "current_status": "candidate_actor",
        "priority": "P1",
        "notes": "US-based funding arm for ELNET European operations",
    },
    {
        "entity_id": "WILLIAM_DAVIDSON_FOUNDATION",
        "label": "William Davidson Foundation",
        "entity_type": "FOUNDATION",
        "sub_type": "donor_us",
        "country": "US",
        "scope": "US/IL",
        "tier_guess": "T2",
        "role_guess": "funder",
        "public_status": "known_donor",
        "why_relevant": "Historische donor voor pro-Israël advocacy",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "William Davidson Foundation",
        "source_hint": "Foundation filings / NGO Monitor context",
        "source_ids": "",
        "current_status": "raw_lead",
        "priority": "P2",
        "notes": "",
    },
    {
        "entity_id": "BECKER_TRUST",
        "label": "Newton and Rochelle Becker Charitable Trust",
        "entity_type": "FOUNDATION",
        "sub_type": "donor_us",
        "country": "US",
        "scope": "US/IL",
        "tier_guess": "T2",
        "role_guess": "funder",
        "public_status": "known_donor",
        "why_relevant": "NGO Monitor donor",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "Becker Charitable Trust",
        "source_hint": "NGO Monitor donor disclosure",
        "source_ids": "",
        "current_status": "raw_lead",
        "priority": "P2",
        "notes": "",
    },
    {
        "entity_id": "JEWISH_FEDERATIONS",
        "label": "Jewish Federations of North America",
        "entity_type": "FEDERATION",
        "sub_type": "donor_us",
        "country": "US",
        "scope": "US/IL",
        "tier_guess": "T1",
        "role_guess": "funder_network",
        "public_status": "known_actor",
        "why_relevant": "Grootste Joodse federatieve donor-netwerk; financiert pro-Israël groepen",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "JFNA; Jewish Federations",
        "source_hint": "Openbare jaarverslagen",
        "source_ids": "",
        "current_status": "candidate_actor",
        "priority": "P2",
        "notes": "",
    },
    {
        "entity_id": "ELNET_FRANCE",
        "label": "ELNET France",
        "entity_type": "ADVOCACY_ORG",
        "sub_type": "country_affiliate",
        "country": "FR",
        "scope": "FR/EU",
        "tier_guess": "T2",
        "role_guess": "national_affiliate",
        "public_status": "known_actor",
        "why_relevant": "ELNET nationale tak; model voor NL-operatie",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "ELNET France",
        "source_hint": "ELNET website",
        "source_ids": "",
        "current_status": "candidate_actor",
        "priority": "P2",
        "notes": "Vergelijk structuur met ELNET NL",
    },
    {
        "entity_id": "STICHTING_ELNET_NEDERLAND",
        "label": "Stichting ELNET Nederland",
        "entity_type": "STICHTING",
        "sub_type": "nl_legal_entity",
        "country": "NL",
        "scope": "NL",
        "tier_guess": "T1",
        "role_guess": "legal_entity",
        "public_status": "known_actor",
        "why_relevant": "Nederlandse rechtspersoon voor ELNET-activiteiten; reizen en events",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "ELNET Nederland",
        "source_hint": "KvK / jaarrekening",
        "source_ids": "",
        "current_status": "raw_lead",
        "priority": "P1",
        "notes": "KvK-nummer en bestuur opzoeken",
    },
    {
        "entity_id": "ISRAEL_MFA",
        "label": "Israel Ministry of Foreign Affairs",
        "entity_type": "STATE_ACTOR",
        "sub_type": "government",
        "country": "IL",
        "scope": "IL/transnational",
        "tier_guess": "T0",
        "role_guess": "state_actor",
        "public_status": "confirmed_actor",
        "why_relevant": "Overheidsactor in public diplomacy / advocacy; complementeert MSA_ISRAEL",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "Israeli MFA; Israel Ministry of Foreign Affairs",
        "source_hint": "",
        "source_ids": "",
        "current_status": "candidate_actor",
        "priority": "P2",
        "notes": "MSA_ISRAEL is al in actors.csv; MFA apart modelleren of samenvoegen?",
    },
    # ===== CANDIDATE ACTORS =====
    {
        "entity_id": "OCEAN_STATE_JOB_LOT",
        "label": "Ocean State Job Lot Charitable Foundation",
        "entity_type": "FOUNDATION",
        "sub_type": "donor_us",
        "country": "US",
        "scope": "US/IL",
        "tier_guess": "T3",
        "role_guess": "funder",
        "public_status": "known_donor",
        "why_relevant": "NGO Monitor donor (via charitable foundation)",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "Ocean State Job Lot Foundation",
        "source_hint": "NGO Monitor donor disclosure",
        "source_ids": "",
        "current_status": "raw_lead",
        "priority": "P3",
        "notes": "",
    },
    {
        "entity_id": "BREAKING_THE_SILENCE",
        "label": "Breaking the Silence",
        "entity_type": "NGO",
        "sub_type": "israeli_veterans_ngo",
        "country": "IL",
        "scope": "IL",
        "tier_guess": "T3",
        "role_guess": "counter_actor",
        "public_status": "known_actor",
        "why_relevant": "Israëlische veteranen-ngo; doelwit van NGO Monitor; context voor SGP/CU-samenhang",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "Breaking the Silence; Shovrim Shtika",
        "source_hint": "NGO Monitor dossier",
        "source_ids": "",
        "current_status": "candidate_actor",
        "priority": "P2",
        "notes": "Wordt genoemd in TRF/IAF-analyses als tegenhanger",
    },
    # ===== CANDIDATE EDGES TO EXPLORE =====
    {
        "entity_id": "NGO_MONITOR_CIDI_LINK",
        "label": "NGO Monitor <-> CIDI relatie",
        "entity_type": "RELATIONSHIP",
        "sub_type": "coordination_hypothesis",
        "country": "IL/NL",
        "scope": "IL/NL",
        "tier_guess": "T0",
        "role_guess": "dossier_supply",
        "public_status": "candidate",
        "why_relevant": "Beide partijen delen framing; CIDI gebruikt NGO Monitor-materiaal in NL-context",
        "related_cases": "CASE_ALMEZAN_2020",
        "related_claims": "C2;C9",
        "known_aliases": "",
        "source_hint": "ELSC-rapport; CIDI-publicaties die NGO Monitor citeren",
        "source_ids": "S_ELSC_JOODS_TELEGRAAF_ALMEZAN",
        "current_status": "needs_source",
        "priority": "P1",
        "notes": "Onderzoek welke CIDI-publicaties NGO Monitor als bron gebruiken",
    },
    {
        "entity_id": "NGO_MONITOR_LIKOED",
        "label": "NGO Monitor -> Likoed Nederland",
        "entity_type": "RELATIONSHIP",
        "sub_type": "frame_supply_hypothesis",
        "country": "IL/NL",
        "scope": "IL/NL",
        "tier_guess": "T1",
        "role_guess": "dossier_supply",
        "public_status": "candidate",
        "why_relevant": "Likoed-campagnes (schoolboeken) volgen NGO Monitor-patroon",
        "related_cases": "CASE_SCHOOLBOOK_2015",
        "related_claims": "C12",
        "known_aliases": "",
        "source_hint": "Vergelijk Likoed-publicaties met NGO Monitor-rapporten",
        "source_ids": "",
        "current_status": "needs_source",
        "priority": "P2",
        "notes": "",
    },
    {
        "entity_id": "CIDI_VVD",
        "label": "CIDI -> VVD (publieke coördinatie)",
        "entity_type": "RELATIONSHIP",
        "sub_type": "political_coordination_hypothesis",
        "country": "NL",
        "scope": "NL",
        "tier_guess": "T1",
        "role_guess": "political_transmission",
        "public_status": "candidate",
        "why_relevant": "Yesilgöz (VVD) reageerde direct op CIDI-HU-case; CIDI-data gebruikt door VVD-Kamerleden",
        "related_cases": "CASE_HU_CIDI_2024;CASE_NGO_OXFAM_2026",
        "related_claims": "C13;C8",
        "known_aliases": "",
        "source_hint": "HOP-rapportage; NIW/CIDI-data artikel",
        "source_ids": "S_HOP_HU_POLITICI_2024;S_NIW_CIDI_DATA_2025",
        "current_status": "needs_source",
        "priority": "P1",
        "notes": "CIDI levert stemgedrag-data aan NIW; VVD gebruikt CIDI-data in debat",
    },
    {
        "entity_id": "CIDI_BBB",
        "label": "CIDI -> BBB (publieke coördinatie)",
        "entity_type": "RELATIONSHIP",
        "sub_type": "political_coordination_hypothesis",
        "country": "NL",
        "scope": "NL",
        "tier_guess": "T2",
        "role_guess": "political_transmission",
        "public_status": "candidate",
        "why_relevant": "Van der Plas reageerde op HU-case; CestMocro-uitspraak in lijn met CIDI-framing",
        "related_cases": "CASE_HU_CIDI_2024;CASE_CESTMOCRO_BAN_2024",
        "related_claims": "C13;C11",
        "known_aliases": "",
        "source_hint": "Media-rapportage; Villamedia",
        "source_ids": "S_VILLAMEDIA_CESTMOCRO_2024;S_HOP_HU_POLITICI_2024",
        "current_status": "needs_source",
        "priority": "P2",
        "notes": "",
    },
    {
        "entity_id": "CIDI_JA21",
        "label": "CIDI -> JA21",
        "entity_type": "RELATIONSHIP",
        "sub_type": "political_alignment",
        "country": "NL",
        "scope": "NL",
        "tier_guess": "T3",
        "role_guess": "ideological_alignment",
        "public_status": "candidate",
        "why_relevant": "JA21 ideologisch dicht bij CIDI-standpunten",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "",
        "source_hint": "Nog geen direct spoor; op basis van standpunten",
        "source_ids": "",
        "current_status": "raw_lead",
        "priority": "P4",
        "notes": "Eerst spoor vinden voor opname",
    },
    {
        "entity_id": "CIDI_ELNET",
        "label": "CIDI <-> ELNET",
        "entity_type": "RELATIONSHIP",
        "sub_type": "network_overlap",
        "country": "NL",
        "scope": "NL/EU",
        "tier_guess": "T1",
        "role_guess": "network_bridge",
        "public_status": "candidate",
        "why_relevant": "CIDI en ELNET opereren inzelfde pro-Israël-netwerk; mogelijke personele/event-overlap",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "",
        "source_hint": "Events, deelnemers, bestuurlijke overlap",
        "source_ids": "",
        "current_status": "needs_source",
        "priority": "P2",
        "notes": "Check evenementen waar beide aan deelnamen",
    },
    {
        "entity_id": "CIDI_ECI",
        "label": "CIDI -> ECI",
        "entity_type": "RELATIONSHIP",
        "sub_type": "network_overlap",
        "country": "NL/EU",
        "scope": "NL/EU",
        "tier_guess": "T2",
        "role_guess": "eu_advocacy_bridge",
        "public_status": "candidate",
        "why_relevant": "CIDI en ECI delen EU-advocacy-doelen",
        "related_cases": "",
        "related_claims": "C15",
        "known_aliases": "",
        "source_hint": "LobbyFacts; ECI-website",
        "source_ids": "S_ECI_LOBBYFACTS",
        "current_status": "needs_source",
        "priority": "P3",
        "notes": "",
    },
    {
        "entity_id": "IAF_ELNET",
        "label": "IAF <-> ELNET",
        "entity_type": "RELATIONSHIP",
        "sub_type": "network_overlap",
        "country": "EU",
        "scope": "EU/transnational",
        "tier_guess": "T0",
        "role_guess": "strategic_partner",
        "public_status": "candidate",
        "why_relevant": "Beide transnationale hubs; IAF parlementair, ELNET policy/reizen; mogelijke samenwerking",
        "related_cases": "CASE_IAF_CAUCUS_2013",
        "related_claims": "",
        "known_aliases": "",
        "source_hint": "Open bronnen; TRF/ELSC-rapporten",
        "source_ids": "S_RIGHTSFORUM_IAF_2025",
        "current_status": "needs_source",
        "priority": "P2",
        "notes": "TRF-rapport suggereert overlap",
    },
    {
        "entity_id": "IAF_ECI",
        "label": "IAF <-> ECI",
        "entity_type": "RELATIONSHIP",
        "sub_type": "network_overlap",
        "country": "EU",
        "scope": "EU",
        "tier_guess": "T1",
        "role_guess": "strategic_partner",
        "public_status": "candidate",
        "why_relevant": "Beide EU-level advocacy; ECI richt zich op EU-instellingen, IAF op parlementen",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "",
        "source_hint": "Open bronnen; TRF/ELSC-rapporten",
        "source_ids": "",
        "current_status": "needs_source",
        "priority": "P3",
        "notes": "",
    },
    {
        "entity_id": "SGP_CU_BREAKING_SILENCE",
        "label": "SGP/CU verhouding tot Breaking the Silence",
        "entity_type": "RELATIONSHIP",
        "sub_type": "political_position",
        "country": "NL/IL",
        "scope": "NL/IL",
        "tier_guess": "T2",
        "role_guess": "ideological_position",
        "public_status": "candidate",
        "why_relevant": "SGP/CU steunen IAF dat Breaking the Silence als tegenstander ziet",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "",
        "source_hint": "IAF-positionering",
        "source_ids": "S_RIGHTSFORUM_IAF_2025",
        "current_status": "needs_source",
        "priority": "P3",
        "notes": "Context voor positionering SGP/CU in pro-Israël-netwerk",
    },
    {
        "entity_id": "FJN_TRF",
        "label": "FJN <-> TRF",
        "entity_type": "RELATIONSHIP",
        "sub_type": "counter_advocacy",
        "country": "NL",
        "scope": "NL",
        "tier_guess": "T2",
        "role_guess": "counter_balance",
        "public_status": "candidate",
        "why_relevant": "FJN is pro-Israël; TRF is counter-actor; inhoudelijk tegengesteld",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "",
        "source_hint": "ELSC; TRF-publicaties",
        "source_ids": "",
        "current_status": "needs_source",
        "priority": "P3",
        "notes": "",
    },
    {
        "entity_id": "FJN_JAN_TERVOORT",
        "label": "FJN -> Jan Tervoort",
        "entity_type": "RELATIONSHIP",
        "sub_type": "legal_pressure",
        "country": "NL",
        "scope": "NL",
        "tier_guess": "T3",
        "role_guess": "legal_target",
        "public_status": "candidate",
        "why_relevant": "FJN zou betrokken zijn bij juridische druk op Tervoort/TRF",
        "related_cases": "",
        "related_claims": "C3",
        "known_aliases": "",
        "source_hint": "TRF-publicatie; ELSC-rapport",
        "source_ids": "S_TRF_CHARACTER_2019",
        "current_status": "needs_source",
        "priority": "P2",
        "notes": "TRF claimt karaktermoord; bron is TRF zelf",
    },
]

# Also add existing actors from actors.csv as confirmed_actor references
existing_actors = read_csv("actors.csv")
existing_entity_ids = {e["entity_id"] for e in research_entities}

for a in existing_actors:
    aid = a["actor_id"]
    if aid in existing_entity_ids:
        continue
    research_entities.append({
        "entity_id": aid,
        "label": a.get("label", aid),
        "entity_type": a.get("actor_type", "ACTOR"),
        "sub_type": a.get("sub_type", ""),
        "country": "NL" if "NL" in a.get("scope", "") else a.get("scope", ""),
        "scope": a.get("scope", ""),
        "tier_guess": a.get("tier", "T5"),
        "role_guess": a.get("role", ""),
        "public_status": a.get("confidence", "known"),
        "why_relevant": "Bestaande actor in evidence graph",
        "related_cases": "",
        "related_claims": "",
        "known_aliases": "",
        "source_hint": "",
        "source_ids": a.get("source_ids", ""),
        "current_status": "confirmed_actor",
        "priority": "P0" if a.get("tier") in ("T0", "T1") else "P1" if a.get("tier") == "T2" else "P2",
        "notes": "Imported from actors.csv",
    })

write_csv("research_entities.csv", research_entities)
print(f"research_entities.csv: {len(research_entities)} entries")

# ── 1b. research_edges.csv ──

EDGE_HEADER = [
    "research_edge_id","source_label","target_label","proposed_edge_type",
    "mechanism_guess","why_relevant","related_case","related_claim",
    "current_trace_level","needed_evidence","priority","status","notes"
]

research_edges = [
    {
        "research_edge_id": "RE_NGO_CIDI",
        "source_label": "NGO_MONITOR",
        "target_label": "CIDI",
        "proposed_edge_type": "FRAME_SUPPLY",
        "mechanism_guess": "NGO Monitor levert dossiers/frames die CIDI gebruikt in NL-context",
        "why_relevant": "CIDI gebruikt NGO Monitor-materiaal in publieke communicatie",
        "related_case": "CASE_ALMEZAN_2020",
        "related_claim": "C9",
        "current_trace_level": "name_overlap",
        "needed_evidence": "CIDI-artikel of -statement dat NGO Monitor citeert",
        "priority": "P1",
        "status": "needs_source",
        "notes": "ELSC-rapport documenteert route voor Al Mezan",
    },
    {
        "research_edge_id": "RE_NGO_LIKOED",
        "source_label": "NGO_MONITOR",
        "target_label": "LIKOED_NL",
        "proposed_edge_type": "FRAME_SUPPLY",
        "mechanism_guess": "Likoed gebruikt NGO Monitor-rapportage voor schoolboekcampagnes",
        "why_relevant": "Beide actoren richten zich op antisemitismebestrijding in onderwijs",
        "related_case": "CASE_SCHOOLBOOK_2015",
        "related_claim": "C12",
        "current_trace_level": "name_overlap",
        "needed_evidence": "Likoed-publicatie die NGO Monitor noemt",
        "priority": "P2",
        "status": "needs_source",
        "notes": "",
    },
    {
        "research_edge_id": "RE_CIDI_VVD",
        "source_label": "CIDI",
        "target_label": "VVD",
        "proposed_edge_type": "POLITICAL_TRANSMISSION",
        "mechanism_guess": "CIDI-data en -framing worden gebruikt door VVD-Kamerleden",
        "why_relevant": "Zichtbaar in HU-case en NGO Monitor-Kamervragen",
        "related_case": "CASE_HU_CIDI_2024;CASE_NGO_OXFAM_2026",
        "related_claim": "C13;C8",
        "current_trace_level": "public_statement",
        "needed_evidence": "CIDI-communicatie voorafgaand aan VVD-actie",
        "priority": "P1",
        "status": "needs_source",
        "notes": "Yesilgöz reageerde direct. Rajkowski stelde vragen obv Telegraaf/NGO Monitor",
    },
    {
        "research_edge_id": "RE_CIDI_BBB",
        "source_label": "CIDI",
        "target_label": "BBB",
        "proposed_edge_type": "POLITICAL_TRANSMISSION",
        "mechanism_guess": "CIDI-framing wordt overgenomen door BBB in publieke uitspraken",
        "why_relevant": "Van der Plas reageerde op HU-case en CestMocro in lijn met CIDI",
        "related_case": "CASE_HU_CIDI_2024;CASE_CESTMOCRO_BAN_2024",
        "related_claim": "C13;C11",
        "current_trace_level": "public_statement",
        "needed_evidence": "CIDI-communicatie voorafgaand aan BBB-reactie",
        "priority": "P2",
        "status": "needs_source",
        "notes": "",
    },
    {
        "research_edge_id": "RE_CIDI_NIW",
        "source_label": "CIDI",
        "target_label": "NIW",
        "proposed_edge_type": "DATA_USE",
        "mechanism_guess": "CIDI levert stemgedrag-data aan NIW voor publicatie",
        "why_relevant": "NIW-artikel expliciet in samenwerking met CIDI-employee",
        "related_case": "",
        "related_claim": "",
        "current_trace_level": "official_record",
        "needed_evidence": "NIW-artikel met CIDI-bronvermelding (aanwezig)",
        "priority": "P0",
        "status": "trace_found",
        "notes": "ART_NIW_CIDI_DATA_2025; Bart van Dijk is CIDI-employee",
    },
    {
        "research_edge_id": "RE_CIDI_NOS",
        "source_label": "CIDI",
        "target_label": "NOS",
        "proposed_edge_type": "MEDIA_STATEMENT",
        "mechanism_guess": "CIDI-directeur geeft statement aan NOS over lopende zaken",
        "why_relevant": "CIDI gebruikt NOS als platform voor publieke positionering",
        "related_case": "CASE_CESTMOCRO_2023;CASE_HU_CIDI_2024",
        "related_claim": "C11;C13",
        "current_trace_level": "official_record",
        "needed_evidence": "Bevestigd via NOS-artikelen",
        "priority": "P2",
        "status": "needs_source",
        "notes": "Al als edge in v5 via E083, E084, E050",
    },
    {
        "research_edge_id": "RE_CIDI_MEDIA_GENERAL",
        "source_label": "CIDI",
        "target_label": "MEDIA_CLUSTER_NL",
        "proposed_edge_type": "MEDIA_PRESENCE",
        "mechanism_guess": "CIDI heeft structurele media-aanwezigheid (172 dagen in 2024 volgens eigen rapport)",
        "why_relevant": "CIDI meet eigen media-impact; structurele amplificatie",
        "related_case": "",
        "related_claim": "C1;C4",
        "current_trace_level": "official_record",
        "needed_evidence": "CIDI-activiteitenoverzicht 2024 (aanwezig als S_CIDI_ACTIVITY_2024)",
        "priority": "P1",
        "status": "trace_found",
        "notes": "CIDI self-report: 172 media-dagen in 2024",
    },
    {
        "research_edge_id": "RE_TELEGRAAF_VVD",
        "source_label": "TELEGRAAF",
        "target_label": "VVD",
        "proposed_edge_type": "MEDIA_TO_PARLIAMENT",
        "mechanism_guess": "Telegraaf-artikel over NGO Monitor/Oxfam leidt tot VVD-Kamervragen",
        "why_relevant": "Rajkowski (VVD) verwees naar Telegraaf in Kamervragen",
        "related_case": "CASE_NGO_OXFAM_2026",
        "related_claim": "C8",
        "current_trace_level": "official_record",
        "needed_evidence": "Kamerstuk met Telegraaf-referentie (aanwezig)",
        "priority": "P0",
        "status": "trace_found",
        "notes": "Al als edge in v5: E031, E032, E033. Tekstoverlap nog meten.",
    },
    {
        "research_edge_id": "RE_TELEGRAAF_PVV",
        "source_label": "TELEGRAAF",
        "target_label": "PVV",
        "proposed_edge_type": "MEDIA_TO_PARLIAMENT",
        "mechanism_guess": "Telegraaf-artikel leidt tot PVV-Kamervragen over NGO Monitor/Oxfam",
        "why_relevant": "Markuszower + Lammers stelden vragen obv Telegraaf",
        "related_case": "CASE_NGO_OXFAM_2026",
        "related_claim": "C8",
        "current_trace_level": "official_record",
        "needed_evidence": "Kamerstuk (aanwezig)",
        "priority": "P0",
        "status": "trace_found",
        "notes": "Al als edge in v5: E031, E034, E035",
    },
    {
        "research_edge_id": "RE_NGO_TELEGRAAF",
        "source_label": "NGO_MONITOR",
        "target_label": "TELEGRAAF",
        "proposed_edge_type": "FRAME_SUPPLY",
        "mechanism_guess": "NGO Monitor-rapporten worden gebruikt als bron voor Telegraaf-artikelen",
        "why_relevant": "Telegraaf bericht over NGO Monitor-aantijgingen",
        "related_case": "CASE_NGO_OXFAM_2026",
        "related_claim": "C8",
        "current_trace_level": "media_sequence",
        "needed_evidence": "Telegraaf-artikel dat NGO Monitor noemt (verwezen in Kamerstuk)",
        "priority": "P0",
        "status": "trace_found",
        "notes": "Al als edge in v5: E040, E031. Tekstoverlap nog meten.",
    },
    {
        "research_edge_id": "RE_NGO_JOODS",
        "source_label": "NGO_MONITOR",
        "target_label": "JOODS_NL",
        "proposed_edge_type": "FRAME_SUPPLY",
        "mechanism_guess": "ELSC stelt dat Joods.nl NGO Monitor-claims over Al Mezan repliceerde",
        "why_relevant": "Transmissieroute Al Mezan via Joods.nl",
        "related_case": "CASE_ALMEZAN_2020",
        "related_claim": "C9",
        "current_trace_level": "media_sequence",
        "needed_evidence": "Joods.nl-artikel dat NGO Monitor citeert (ELSC-claim, nog niet geverifieerd)",
        "priority": "P1",
        "status": "needs_source",
        "notes": "Al als edge in v5: E072. Bron is ELSC-claim. Per artikel verifiëren.",
    },
    {
        "research_edge_id": "RE_LIKOED_JONET",
        "source_label": "LIKOED_NL",
        "target_label": "JONET",
        "proposed_edge_type": "MEDIA_AMPLIFICATION",
        "mechanism_guess": "Jonet bericht over Likoed-campagnes",
        "why_relevant": "Jonet is community-medium dat Likoed-activiteiten versterkt",
        "related_case": "CASE_SCHOOLBOOK_2019",
        "related_claim": "C12",
        "current_trace_level": "official_record",
        "needed_evidence": "Jonet-artikel over Likoed (aanwezig)",
        "priority": "P2",
        "status": "trace_found",
        "notes": "Al als edge in v5: E064",
    },
    {
        "research_edge_id": "RE_IAF_SGP",
        "source_label": "IAF",
        "target_label": "SGP",
        "proposed_edge_type": "PARLIAMENTARY_ACCESS",
        "mechanism_guess": "IAF heeft SGP-Kamerleden in parlementaire caucus",
        "why_relevant": "Structurele parlementaire toegang via SGP",
        "related_case": "CASE_IAF_CAUCUS_2013",
        "related_claim": "",
        "current_trace_level": "official_record",
        "needed_evidence": "IAF-netwerkpagina + Jonet (aanwezig)",
        "priority": "P0",
        "status": "trace_found",
        "notes": "Al als edge in v5: E017, E015, E016. Stoffer is caucus-voorzitter.",
    },
    {
        "research_edge_id": "RE_CVI_STOFFER",
        "source_label": "CVI",
        "target_label": "CHRIS_STOFFER",
        "proposed_edge_type": "SPONSORED_TRAVEL",
        "mechanism_guess": "CVI sponsort Israël-reis voor Stoffer",
        "why_relevant": "Directe reisondersteuning aan parlementariër",
        "related_case": "CASE_IAF_CAUCUS_2013",
        "related_claim": "",
        "current_trace_level": "official_record",
        "needed_evidence": "Reisregistratie TK (aanwezig)",
        "priority": "P0",
        "status": "trace_found",
        "notes": "Al als edge in v5: E028, E099, E102, E104",
    },
    {
        "research_edge_id": "RE_ELNET_STOFFER",
        "source_label": "ELNET",
        "target_label": "CHRIS_STOFFER",
        "proposed_edge_type": "SPONSORED_TRAVEL",
        "mechanism_guess": "ELNET sponsort Israël-solidariteitsbezoek",
        "why_relevant": "ELNET financiert reis voor parlementariër",
        "related_case": "CASE_IAF_CAUCUS_2013",
        "related_claim": "",
        "current_trace_level": "official_record",
        "needed_evidence": "Reisregistratie TK (aanwezig)",
        "priority": "P0",
        "status": "trace_found",
        "notes": "Al als edge in v5: E027, E098, E101, E103",
    },
    {
        "research_edge_id": "RE_CVI_MEDIA_WIERDDUK",
        "source_label": "CVI_MEDIA",
        "target_label": "WIERD_DUK",
        "proposed_edge_type": "PLATFORMING",
        "mechanism_guess": "CVI geeft podium aan Telegraaf-commentator",
        "why_relevant": "Religieuze organisatie amplificeert journalist met specifiek frame",
        "related_case": "",
        "related_claim": "C14",
        "current_trace_level": "official_record",
        "needed_evidence": "Podcast (aanwezig)",
        "priority": "P1",
        "status": "trace_found",
        "notes": "Al als edge in v5: E051, E100",
    },
    {
        "research_edge_id": "RE_NGO_MSA",
        "source_label": "NGO_MONITOR",
        "target_label": "MSA_ISRAEL",
        "proposed_edge_type": "STATE_COORDINATION",
        "mechanism_guess": "NGO Monitor ontvangt mogelijk aansturing of financiering van Israëlische staatsactoren",
        "why_relevant": "NGO Monitor-directeur heeft MSA-achtergrond; inhoudelijke overlap met MSA-doelen",
        "related_case": "",
        "related_claim": "C6",
        "current_trace_level": "name_overlap",
        "needed_evidence": "Directe link: NGO Monitor funding van MSA, of personele overlap",
        "priority": "P1",
        "status": "needs_source",
        "notes": "MSA_ISRAEL is in actors.csv; NGO Monitor-directeur profiel checken",
    },
    {
        "research_edge_id": "RE_IAF_ELNET_HUB",
        "source_label": "IAF",
        "target_label": "ELNET",
        "proposed_edge_type": "STRATEGIC_PARTNERSHIP",
        "mechanism_guess": "IAF (parlementair netwerk) en ELNET (policy/reizen) vullen elkaar aan",
        "why_relevant": "Beide opereren inzelfde transnationale pro-Israël-ruimte",
        "related_case": "",
        "related_claim": "",
        "current_trace_level": "name_overlap",
        "needed_evidence": "Gedeelde events, deelnemers, bestuurders",
        "priority": "P2",
        "status": "needs_source",
        "notes": "TRF-rapport suggereert overlap; check IAF/ELNET evenementen",
    },
    {
        "research_edge_id": "RE_TELEGRAAF_ALMEZAN",
        "source_label": "TELEGRAAF",
        "target_label": "AL_MEZAN",
        "proposed_edge_type": "MEDIA_AMPLIFICATION",
        "mechanism_guess": "Telegraaf publiceert NGO Monitor-aantijgingen over Al Mezan",
        "why_relevant": "Media-amplificatie van terror-link claim",
        "related_case": "CASE_ALMEZAN_2020",
        "related_claim": "C9",
        "current_trace_level": "media_sequence",
        "needed_evidence": "Telegraaf-artikel over Al Mezan (ELSC-claim)",
        "priority": "P1",
        "status": "needs_source",
        "notes": "Al als edge in v5: E073, E075. ELSC-claim; per artikel verifiëren.",
    },
]

write_csv("research_edges.csv", research_edges)
print(f"research_edges.csv: {len(research_edges)} entries")

# ── 1c. research_aliases.csv ──

ALIAS_HEADER = ["alias_id","primary_entity_id","alias","alias_type","language","confidence","source_ids","notes"]

research_aliases = [
    {"alias_id": "ALIAS_CIDI_FULL", "primary_entity_id": "CIDI", "alias": "Centrum Informatie en Documentatie Israël", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_CIDI_EN", "primary_entity_id": "CIDI", "alias": "Center for Information and Documentation Israel", "alias_type": "full_name_en", "language": "EN", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_IAF_EN", "primary_entity_id": "IAF", "alias": "Israel Allies Foundation", "alias_type": "full_name", "language": "EN", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_IAF_IIACF", "primary_entity_id": "IAF", "alias": "International Israel Allies Caucus Foundation", "alias_type": "former_name", "language": "EN", "confidence": "high", "source_ids": "S_JONET_IIACF_2013", "notes": "Oude naam voor IAF"},
    {"alias_id": "ALIAS_ELNET_FULL", "primary_entity_id": "ELNET", "alias": "European Leadership Network", "alias_type": "full_name", "language": "EN", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_NGO_MONITOR_FULL", "primary_entity_id": "NGO_MONITOR", "alias": "NGO Monitor", "alias_type": "full_name", "language": "EN", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_NGO_MONITOR_HEB", "primary_entity_id": "NGO_MONITOR", "alias": "המרכז לחקר ארגונים לא-ממשלתיים", "alias_type": "name_hebrew", "language": "HE", "confidence": "high", "source_ids": "", "notes": "Hebrew: NGO Monitor"},
    {"alias_id": "ALIAS_TRF_FULL", "primary_entity_id": "TRF", "alias": "The Rights Forum", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_TRF_EN", "primary_entity_id": "TRF", "alias": "The Rights Forum", "alias_type": "full_name_en", "language": "EN", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_ELSC_FULL", "primary_entity_id": "ELSC", "alias": "European Legal Support Center", "alias_type": "full_name", "language": "EN", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_CVI_FULL", "primary_entity_id": "CVI", "alias": "Christenen voor Israël", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_CVI_EN", "primary_entity_id": "CVI", "alias": "Christians for Israel", "alias_type": "full_name_en", "language": "EN", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_YESILGOZ_FULL", "primary_entity_id": "DILAN_YESILGOZ", "alias": "Dilan Yesilgöz-Zegerius", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_VDP_FULL", "primary_entity_id": "CAROLINE_VDP", "alias": "Caroline van der Plas", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_OMTZIGT_FULL", "primary_entity_id": "PIETER_OMTZIGT", "alias": "Pieter Omtzigt", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_MARKUSZOWER_FULL", "primary_entity_id": "GIDI_MARKUSZOWER", "alias": "Gidi Markuszower", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_RAJKOWSKI_FULL", "primary_entity_id": "QUEENY_RAJKOWSKI", "alias": "Queeny Rajkowski", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_ELNET_IMPACT", "primary_entity_id": "ELNET", "alias": "ELNET Mobilizes Impact", "alias_type": "program_name", "language": "EN", "confidence": "high", "source_ids": "S_ELNET_IMPACT", "notes": "ELNET impact report title"},
    {"alias_id": "ALIAS_CASTRO_FULL", "primary_entity_id": "CASTRO", "alias": "Castro Communicatie en Lobby", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "S_CASTRO_SITE", "notes": ""},
    {"alias_id": "ALIAS_HU_FULL", "primary_entity_id": "HU", "alias": "Hogeschool Utrecht", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_THIEME_FULL", "primary_entity_id": "THIEMEMEULENHOFF", "alias": "ThiemeMeulenhoff", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_EW_FULL", "primary_entity_id": "EW", "alias": "Elsevier Weekblad", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_NIW_FULL", "primary_entity_id": "NIW", "alias": "Nieuw Israëlietisch Weekblad", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_MSA_FULL", "primary_entity_id": "MSA_ISRAEL", "alias": "Israeli Ministry of Strategic Affairs", "alias_type": "full_name", "language": "EN", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_MSA_HEB", "primary_entity_id": "MSA_ISRAEL", "alias": "המשרד לעניינים אסטרטגיים", "alias_type": "name_hebrew", "language": "HE", "confidence": "high", "source_ids": "", "notes": "Israeli Ministry of Strategic Affairs and Public Diplomacy"},
    {"alias_id": "ALIAS_ECI_FULL", "primary_entity_id": "ECI", "alias": "European Coalition for Israel", "alias_type": "full_name", "language": "EN", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_FJN_FULL", "primary_entity_id": "FJN", "alias": "Federatief Joods Nederland", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_NP_KOMITEE", "primary_entity_id": "NPK", "alias": "Nederlands Palestina Komitee", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_DDS_FULL", "primary_entity_id": "DDS", "alias": "De Dagelijkse Standaard", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_STOFFER_FULL", "primary_entity_id": "CHRIS_STOFFER", "alias": "Chris Stoffer", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": ""},
    {"alias_id": "ALIAS_VOET_FULL", "primary_entity_id": "ESTHER_VOET", "alias": "Esther Voet", "alias_type": "full_name", "language": "NL", "confidence": "high", "source_ids": "", "notes": "NIW-hoofdredacteur; oud-CIDI-directeur"},
]

write_csv("research_aliases.csv", research_aliases)
print(f"research_aliases.csv: {len(research_aliases)} entries")

# ── 1d. research_tasks.csv ──

TASK_HEADER = [
    "task_id","entity_id","edge_id","task_type","question",
    "priority","status","next_action","source_hint","notes"
]

research_tasks = [
    {"task_id": "TASK_001", "entity_id": "WECHSLER_FOUNDATION", "edge_id": "", "task_type": "find_funding", "question": "Zoek filing/spoor voor relatie met NGO Monitor", "priority": "P1", "status": "open", "next_action": "check foundation filings / NGO Monitor donor disclosures", "source_hint": "NGO Monitor annual report", "notes": ""},
    {"task_id": "TASK_002", "entity_id": "REPORT_ORG", "edge_id": "", "task_type": "find_funding", "question": "Wat is REPORT/Religious Exceptionalism Project?", "priority": "P1", "status": "open", "next_action": "zoek NGO Monitor filings naar REPORT", "source_hint": "NGO Monitor donor disclosure", "notes": ""},
    {"task_id": "TASK_003", "entity_id": "FELNET", "edge_id": "", "task_type": "find_funding", "question": "Vind Friends of ELNET filings en bestuur", "priority": "P1", "status": "open", "next_action": "zoek US foundation filings", "source_hint": "ELNET impact report", "notes": ""},
    {"task_id": "TASK_004", "entity_id": "STICHTING_ELNET_NEDERLAND", "edge_id": "", "task_type": "find_source", "question": "Vind KvK-inschrijving en bestuur Stichting ELNET Nederland", "priority": "P1", "status": "open", "next_action": "KvK online", "source_hint": "KvK-handelsregister", "notes": "Ook jaarrekening opvragen"},
    {"task_id": "TASK_005", "entity_id": "", "edge_id": "RE_CIDI_NIW", "task_type": "find_source", "question": "Documenteer CIDI->NIW data-levering: welke data, hoe vaak, wie is contact", "priority": "P1", "status": "open", "next_action": "NIW-artikel + CIDI-bron", "source_hint": "NIW-artikel", "notes": ""},
    {"task_id": "TASK_006", "entity_id": "", "edge_id": "RE_NGO_CIDI", "task_type": "find_source", "question": "Vind CIDI-publicatie die NGO Monitor citeert", "priority": "P1", "status": "open", "next_action": "Doorzoek CIDI-publicaties", "source_hint": "CIDI-website", "notes": ""},
    {"task_id": "TASK_007", "entity_id": "", "edge_id": "RE_NGO_JOODS", "task_type": "find_text_overlap", "question": "Vind Joods.nl-artikel dat NGO Monitor Al Mezan-claim repliceert", "priority": "P1", "status": "open", "next_action": "Tekstvergelijking NGO Monitor rapport vs Joods.nl artikel", "source_hint": "ELSC-rapport", "notes": ""},
    {"task_id": "TASK_008", "entity_id": "", "edge_id": "RE_TELEGRAAF_ALMEZAN", "task_type": "find_text_overlap", "question": "Vind Telegraaf-artikel over Al Mezan en vergelijk met NGO Monitor", "priority": "P1", "status": "open", "next_action": "Archief Telegraaf 2020", "source_hint": "ELSC-rapport", "notes": ""},
    {"task_id": "TASK_009", "entity_id": "BREAKING_THE_SILENCE", "edge_id": "", "task_type": "find_source", "question": "Documenteer SGP/CU-positie tav Breaking the Silence", "priority": "P2", "status": "open", "next_action": "zoek Kamervragen/moties", "source_hint": "TRF-rapport; IAF-positionering", "notes": ""},
    {"task_id": "TASK_010", "entity_id": "", "edge_id": "RE_NGO_MSA", "task_type": "find_source", "question": "Onderzoek NGO Monitor-directeur profiel voor MSA-link", "priority": "P1", "status": "open", "next_action": "LinkedIn / NGO Monitor website / publicaties", "source_hint": "", "notes": ""},
    {"task_id": "TASK_011", "entity_id": "ISRAEL_MFA", "edge_id": "", "task_type": "find_source", "question": "Beslis of Israel MFA aparte actor wordt of samenvalt met MSA_ISRAEL", "priority": "P2", "status": "open", "next_action": "Vergelijk MFA vs MSA rol in NL-context", "source_hint": "", "notes": ""},
    {"task_id": "TASK_012", "entity_id": "NGO_MONITOR_CIDI_LINK", "edge_id": "RE_NGO_CIDI", "task_type": "find_source", "question": "Verzamel alle CIDI-publicaties die NGO Monitor noemen", "priority": "P1", "status": "open", "next_action": "CIDI-website doorzoeken op NGO Monitor", "source_hint": "", "notes": ""},
    {"task_id": "TASK_013", "entity_id": "OCEAN_STATE_JOB_LOT", "edge_id": "", "task_type": "find_funding", "question": "Zoek Ocean State Job Lot Foundation filing voor NGO Monitor", "priority": "P3", "status": "open", "next_action": "Foundation directory", "source_hint": "", "notes": ""},
    {"task_id": "TASK_014", "entity_id": "JEWISH_FEDERATIONS", "edge_id": "", "task_type": "find_funding", "question": "Onderzoek JFNA-filings voor Nederlandse pro-Israël organisaties", "priority": "P2", "status": "open", "next_action": "JFNA annual report", "source_hint": "", "notes": ""},
    {"task_id": "TASK_015", "entity_id": "DUTCH_DONORS", "edge_id": "", "task_type": "find_source", "question": "Breng Nederlandse donorclusters (BuZa, RVO, NGO-fondsen) in kaart", "priority": "P1", "status": "open", "next_action": "RVO-subsidieregister; BuZa-begroting", "source_hint": "ELSC-rapport", "notes": "Al als actor in actors.csv"},
    {"task_id": "TASK_016", "entity_id": "", "edge_id": "RE_CIDI_MEDIA_GENERAL", "task_type": "find_source", "question": "Verzamel CIDI-mediaoptredens 2024 obv eigen activiteitenoverzicht", "priority": "P2", "status": "open", "next_action": "CIDI Activiteitenoverzicht 2024 PDF", "source_hint": "S_CIDI_ACTIVITY_2024", "notes": ""},
    {"task_id": "TASK_017", "entity_id": "", "edge_id": "RE_TELEGRAAF_VVD", "task_type": "find_text_overlap", "question": "Meet tekstoverlap tussen Telegraaf NGO-artikel en VVD-Kamervragen", "priority": "P1", "status": "open", "next_action": "Tekstvergelijking", "source_hint": "Kamerstuk 2026D08316", "notes": ""},
    {"task_id": "TASK_018", "entity_id": "", "edge_id": "RE_TELEGRAAF_PVV", "task_type": "find_text_overlap", "question": "Meet tekstoverlap tussen Telegraaf NGO-artikel en PVV-Kamervragen", "priority": "P1", "status": "open", "next_action": "Tekstvergelijking", "source_hint": "Kamerstuk 2026D08317", "notes": ""},
]

write_csv("research_tasks.csv", research_tasks)
print(f"research_tasks.csv: {len(research_tasks)} entries")

# ═══════════════════════════════════════════════════════════════
# COMMIT 2: Donor infrastructure
# ═══════════════════════════════════════════════════════════════

# ── 2a. donors.csv ──

DONOR_HEADER = [
    "donor_id","label","donor_type","country",
    "linked_orgs","known_roles",
    "source_hint","source_ids",
    "status","priority","notes"
]

donors = [
    {"donor_id": "DUTCH_GOV", "label": "Nederlandse overheid (BuZa)", "donor_type": "GOVERNMENT", "country": "NL", "linked_orgs": "OXFAM_NOVIB;DRA;UAWC;PALESTINIAN_NGOS", "known_roles": "humanitarian_aid;development;ngo_subsidies", "source_hint": "Rijksbegroting; Kamerstukken", "source_ids": "S_TK_NGOMONITOR_2026_VVD", "status": "confirmed_actor", "priority": "P0", "notes": "Al in actors.csv als DUTCH_GOV. Grootste donor voor Palestijnse NGO's."},
    {"donor_id": "WECHSLER_FOUNDATION", "label": "Wechsler Family Foundation", "donor_type": "PRIVATE_FOUNDATION", "country": "US", "linked_orgs": "NGO_MONITOR", "known_roles": "ngo_monitor_funder", "source_hint": "NGO Monitor filings / foundation directory", "source_ids": "", "status": "raw_lead", "priority": "P1", "notes": "US-based; zoek 990 filings"},
    {"donor_id": "FELNET", "label": "Friends of ELNET", "donor_type": "FRIENDS_ORG", "country": "US", "linked_orgs": "ELNET;ELNET_FRANCE;STICHTING_ELNET_NEDERLAND", "known_roles": "funding_conduit", "source_hint": "ELNET impact report", "source_ids": "S_ELNET_IMPACT", "status": "candidate_actor", "priority": "P1", "notes": "US funding conduit voor ELNET Europees netwerk"},
    {"donor_id": "ELNET", "label": "European Leadership Network / ELNET", "donor_type": "TRANSNATIONAL_HUB", "country": "EU", "linked_orgs": "CHRIS_STOFFER;ELNET_FRANCE;STICHTING_ELNET_NEDERLAND", "known_roles": "travel_sponsor;policy_network", "source_hint": "Reisregistraties TK", "source_ids": "S_TK_STOFFER_REIZEN;S_ELNET_IMPACT", "status": "confirmed_actor", "priority": "P0", "notes": "Al in actors.csv. Sponsor van parlementaire reizen."},
    {"donor_id": "CVI", "label": "Christenen voor Israël", "donor_type": "RELIGIOUS_NETWORK", "country": "NL", "linked_orgs": "CHRIS_STOFFER;CVI_MEDIA", "known_roles": "travel_sponsor;media_platform", "source_hint": "Reisregistraties TK", "source_ids": "S_TK_STOFFER_REIZEN", "status": "confirmed_actor", "priority": "P0", "notes": "Al in actors.csv"},
    {"donor_id": "SGP", "label": "SGP (fractie/stichting)", "donor_type": "POLITICAL_FOUNDATION", "country": "NL", "linked_orgs": "CHRIS_STOFFER;IAF;IAF_EU", "known_roles": "travel_sponsor;parliamentary_network", "source_hint": "Reisregistraties TK", "source_ids": "S_TK_STOFFER_REIZEN;S_SGP_IAF_2025", "status": "confirmed_actor", "priority": "P0", "notes": "Al in actors.csv. Sponsor via fractie/stichting."},
    {"donor_id": "DUTCH_DONORS", "label": "Nederlandse donoren / subsidiegevers (cluster)", "donor_type": "DONOR_CLUSTER", "country": "NL", "linked_orgs": "UAWC;PALESTINIAN_NGOS", "known_roles": "development_aid", "source_hint": "ELSC-rapport", "source_ids": "S_ELSC_2021;S_ELSC_PRESS_2021", "status": "confirmed_actor", "priority": "P1", "notes": "Al in actors.csv. Abstracte cluster."},
    {"donor_id": "WILLIAM_DAVIDSON_FOUNDATION", "label": "William Davidson Foundation", "donor_type": "PRIVATE_FOUNDATION", "country": "US", "linked_orgs": "", "known_roles": "historical_donor", "source_hint": "Foundation filings", "source_ids": "", "status": "raw_lead", "priority": "P2", "notes": ""},
    {"donor_id": "JEWISH_FEDERATIONS", "label": "Jewish Federations of North America", "donor_type": "FEDERATION", "country": "US", "linked_orgs": "", "known_roles": "funder_network", "source_hint": "JFNA jaarverslagen", "source_ids": "", "status": "candidate_actor", "priority": "P2", "notes": ""},
    {"donor_id": "BECKER_TRUST", "label": "Newton and Rochelle Becker Charitable Trust", "donor_type": "TRUST", "country": "US", "linked_orgs": "NGO_MONITOR", "known_roles": "ngo_monitor_funder", "source_hint": "NGO Monitor filings", "source_ids": "", "status": "raw_lead", "priority": "P2", "notes": ""},
    {"donor_id": "ISRAEL_MFA", "label": "Israel Ministry of Foreign Affairs", "donor_type": "GOVERNMENT", "country": "IL", "linked_orgs": "MSA_ISRAEL", "known_roles": "state_funder;public_diplomacy", "source_hint": "", "source_ids": "", "status": "candidate_actor", "priority": "P2", "notes": "Complementeert MSA_ISRAEL in state-funded advocacy"},
]

write_csv("donors.csv", donors)
print(f"donors.csv: {len(donors)} entries")

# ── 2b. funding_flows.csv ──

FLOW_HEADER = [
    "flow_id","funder_id","recipient_id","intermediary_id","amount","currency","year",
    "flow_type","direct_or_indirect","source_url","source_ids","confidence","capture_risk","notes"
]

funding_flows = [
    {"flow_id": "FLOW_DUTCH_PALESTINIAN_NGOS", "funder_id": "DUTCH_DONORS", "recipient_id": "PALESTINIAN_NGOS", "intermediary_id": "", "amount": "", "currency": "", "year": "", "flow_type": "development_aid", "direct_or_indirect": "direct", "source_url": "", "source_ids": "S_ELSC_2021;S_ELSC_PRESS_2021", "confidence": "medium_high", "capture_risk": "high", "notes": "Abstract; specifieke bedragen/besluiten toevoegen"},
    {"flow_id": "FLOW_DUTCH_OXFAM", "funder_id": "DUTCH_GOV", "recipient_id": "OXFAM_NOVIB", "intermediary_id": "", "amount": "", "currency": "", "year": "2026", "flow_type": "humanitarian_aid", "direct_or_indirect": "direct", "source_url": "", "source_ids": "S_TK_NGOMONITOR_2026_VVD", "confidence": "high", "capture_risk": "high", "notes": "Al in funding.csv. Overheid is donor en beleidsverantwoordelijke."},
    {"flow_id": "FLOW_DUTCH_DRA", "funder_id": "DUTCH_GOV", "recipient_id": "DRA", "intermediary_id": "", "amount": "", "currency": "", "year": "2026", "flow_type": "humanitarian_aid", "direct_or_indirect": "direct", "source_url": "", "source_ids": "S_TK_NGOMONITOR_2026_VVD", "confidence": "high", "capture_risk": "high", "notes": "Al in funding.csv."},
    {"flow_id": "FLOW_ELNET_STOFFER_2024", "funder_id": "ELNET", "recipient_id": "CHRIS_STOFFER", "intermediary_id": "", "amount": "", "currency": "", "year": "2024", "flow_type": "travel_sponsorship", "direct_or_indirect": "direct", "source_url": "", "source_ids": "S_TK_STOFFER_REIZEN", "confidence": "high", "capture_risk": "medium", "notes": "Al in funding.csv."},
    {"flow_id": "FLOW_CVI_STOFFER_2022", "funder_id": "CVI", "recipient_id": "CHRIS_STOFFER", "intermediary_id": "", "amount": "", "currency": "", "year": "2022", "flow_type": "travel_sponsorship", "direct_or_indirect": "direct", "source_url": "", "source_ids": "S_TK_STOFFER_REIZEN", "confidence": "high", "capture_risk": "medium", "notes": "Al in funding.csv."},
    {"flow_id": "FLOW_SGP_STOFFER_2022", "funder_id": "SGP", "recipient_id": "CHRIS_STOFFER", "intermediary_id": "", "amount": "", "currency": "", "year": "2022", "flow_type": "travel_sponsorship", "direct_or_indirect": "direct", "source_url": "", "source_ids": "S_TK_STOFFER_REIZEN", "confidence": "high", "capture_risk": "medium", "notes": "Al in funding.csv."},
    {"flow_id": "FLOW_NGO_MONITOR_WECHSLER", "funder_id": "WECHSLER_FOUNDATION", "recipient_id": "NGO_MONITOR", "intermediary_id": "", "amount": "", "currency": "USD", "year": "", "flow_type": "foundation_grant", "direct_or_indirect": "direct", "source_url": "", "source_ids": "", "confidence": "low", "capture_risk": "medium", "notes": "Lead: zoek foundation filing voor bedrag en jaar"},
    {"flow_id": "FLOW_NGO_MONITOR_BECKER", "funder_id": "BECKER_TRUST", "recipient_id": "NGO_MONITOR", "intermediary_id": "", "amount": "", "currency": "USD", "year": "", "flow_type": "foundation_grant", "direct_or_indirect": "direct", "source_url": "", "source_ids": "", "confidence": "low", "capture_risk": "medium", "notes": "Lead: zoek trust filing"},
    {"flow_id": "FLOW_FELNET_ELNET", "funder_id": "FELNET", "recipient_id": "ELNET", "intermediary_id": "", "amount": "", "currency": "USD", "year": "", "flow_type": "funding_conduit", "direct_or_indirect": "direct", "source_url": "", "source_ids": "S_ELNET_IMPACT", "confidence": "medium", "capture_risk": "medium", "notes": "Friends of ELNET is US-funding conduit voor ELNET Europe"},
    {"flow_id": "FLOW_ELNET_ELNET_FR", "funder_id": "ELNET", "recipient_id": "ELNET_FRANCE", "intermediary_id": "", "amount": "", "currency": "", "year": "", "flow_type": "internal_funding", "direct_or_indirect": "direct", "source_url": "", "source_ids": "", "confidence": "low", "capture_risk": "low", "notes": "Lead: ELNET interne structuur onduidelijk"},
    {"flow_id": "FLOW_ELNET_ELNET_NL", "funder_id": "ELNET", "recipient_id": "STICHTING_ELNET_NEDERLAND", "intermediary_id": "", "amount": "", "currency": "", "year": "", "flow_type": "internal_funding", "direct_or_indirect": "direct", "source_url": "", "source_ids": "", "confidence": "low", "capture_risk": "low", "notes": "Lead: Stichting ELNET Nederland jaarrekening nodig"},
    {"flow_id": "FLOW_UAWC_NL", "funder_id": "DUTCH_DONORS", "recipient_id": "UAWC", "intermediary_id": "", "amount": "", "currency": "", "year": "2022", "flow_type": "development_aid_ceased", "direct_or_indirect": "direct", "source_url": "", "source_ids": "S_RIGHTSFORUM_FREESPEECH_2021;S_ELSC_2021", "confidence": "medium_high", "capture_risk": "high", "notes": "Al in funding.csv. Defunding context."},
]

write_csv("funding_flows.csv", funding_flows)
print(f"funding_flows.csv: {len(funding_flows)} entries")

# ── 2c. foundation_filings.csv ──

FILING_HEADER = ["filing_id","foundation_name","funder_id","recipient_org","year","amount","currency","purpose","source_url","notes"]

foundation_filings = []

write_csv("foundation_filings.csv", foundation_filings)
print(f"foundation_filings.csv: {len(foundation_filings)} entries (to be populated)")

# ── 2d. foreign_state_funding.csv ──

STATE_FUNDING_HEADER = [
    "funding_id","source_state","recipient_org","intermediary_org","program","amount","currency","year",
    "mechanism","source_ids","confidence","notes"
]

foreign_state_funding = [
    {"funding_id": "STATE_ISRAEL_MSA_CAMPAIGN", "source_state": "IL", "recipient_org": "MSA_ISRAEL", "intermediary_org": "", "program": "Public Diplomacy / Strategic Affairs", "amount": "", "currency": "", "year": "", "mechanism": "government_budget", "source_ids": "S_PCHR_MSA_2020", "confidence": "medium", "notes": "Israëlische staatsfinanciering voor public diplomacy; EU/NL-doelen via MSA"},
    {"funding_id": "STATE_ISRAEL_MFA_PUBLIC_DIPLOMACY", "source_state": "IL", "recipient_org": "ISRAEL_MFA", "intermediary_org": "", "program": "Public Diplomacy", "amount": "", "currency": "", "year": "", "mechanism": "government_budget", "source_ids": "", "confidence": "low", "notes": "Lead: MFA-budget voor hasbara/public diplomacy in Europa"},
    {"funding_id": "STATE_NL_PALESTINIAN_AID", "source_state": "NL", "recipient_org": "PALESTINIAN_NGOS", "intermediary_org": "", "program": "Humanitaire hulp / Ontwikkelingssamenwerking", "amount": "", "currency": "EUR", "year": "", "mechanism": "government_budget", "source_ids": "S_ELSC_2021;S_TK_NGOMONITOR_2026_VVD", "confidence": "high", "notes": "NL-overheid financiert Palestijnse NGO's via BuZa/RVO; exacte bedragen toevoegen"},
]

write_csv("foreign_state_funding.csv", foreign_state_funding)
print(f"foreign_state_funding.csv: {len(foreign_state_funding)} entries")

# ═══════════════════════════════════════════════════════════════
# COMMIT 4: Source dependency
# ═══════════════════════════════════════════════════════════════

DEP_HEADER = [
    "dependency_id","source_actor_id","dependent_actor_id","material_type",
    "case_id","claim_id","article_id","parliamentary_item_id",
    "dependency_type","confidence","source_ids","notes"
]

source_dependencies = [
    # NGO Monitor -> media
    {"dependency_id": "DEP_NGO_TELEGRAAF_OXFAM", "source_actor_id": "NGO_MONITOR", "dependent_actor_id": "TELEGRAAF", "material_type": "article", "case_id": "CASE_NGO_OXFAM_2026", "claim_id": "C8", "article_id": "", "parliamentary_item_id": "", "dependency_type": "REPORT_USED_AS_SOURCE", "confidence": "high", "source_ids": "S_TK_NGOMONITOR_2026_VVD", "notes": "Telegraaf-artikel gebruikt NGO Monitor-rapport; bevestigd via Kamerstuk"},
    {"dependency_id": "DEP_NGO_TELEGRAAF_ALMEZAN", "source_actor_id": "NGO_MONITOR", "dependent_actor_id": "TELEGRAAF", "material_type": "article", "case_id": "CASE_ALMEZAN_2020", "claim_id": "C9", "article_id": "", "parliamentary_item_id": "", "dependency_type": "REPORT_USED_AS_SOURCE", "confidence": "medium_high", "source_ids": "S_ELSC_JOODS_TELEGRAAF_ALMEZAN", "notes": "ELSC stelt dat Telegraaf NGO Monitor-claims repliceert; per artikel verifiëren"},
    {"dependency_id": "DEP_NGO_JOODS_ALMEZAN", "source_actor_id": "NGO_MONITOR", "dependent_actor_id": "JOODS_NL", "material_type": "article", "case_id": "CASE_ALMEZAN_2020", "claim_id": "C9", "article_id": "", "parliamentary_item_id": "", "dependency_type": "REPORT_USED_AS_SOURCE", "confidence": "medium_high", "source_ids": "S_ELSC_JOODS_TELEGRAAF_ALMEZAN", "notes": "ELSC stelt dat Joods.nl NGO Monitor repliceert; per artikel verifiëren"},
    # Media -> parlement
    {"dependency_id": "DEP_TELEGRAAF_VVD_KV", "source_actor_id": "TELEGRAAF", "dependent_actor_id": "VVD", "material_type": "parliamentary_question", "case_id": "CASE_NGO_OXFAM_2026", "claim_id": "C8", "article_id": "", "parliamentary_item_id": "PQ_RAJKOWSKI_NGO_2026", "dependency_type": "MEDIA_TO_PARLIAMENT", "confidence": "high", "source_ids": "S_TK_NGOMONITOR_2026_VVD", "notes": "Rajkowski (VVD) baseert Kamervragen op Telegraaf-artikel + NGO Monitor"},
    {"dependency_id": "DEP_TELEGRAAF_PVV_KV", "source_actor_id": "TELEGRAAF", "dependent_actor_id": "PVV", "material_type": "parliamentary_question", "case_id": "CASE_NGO_OXFAM_2026", "claim_id": "C8", "article_id": "", "parliamentary_item_id": "PQ_MARKUSZOWER_NGO_2026", "dependency_type": "MEDIA_TO_PARLIAMENT", "confidence": "high", "source_ids": "S_TK_NGOMONITOR_2026_MARKUSZOWER", "notes": "Markuszower/Lammers (PVV) baseert Kamervragen op Telegraaf + NGO Monitor"},
    # Lobby -> media
    {"dependency_id": "DEP_NGO_DIRECT_VVD_KV", "source_actor_id": "NGO_MONITOR", "dependent_actor_id": "VVD", "material_type": "parliamentary_question", "case_id": "CASE_NGO_OXFAM_2026", "claim_id": "C8", "article_id": "", "parliamentary_item_id": "PQ_RAJKOWSKI_NGO_2026", "dependency_type": "LOBBY_TO_PARLIAMENT", "confidence": "high", "source_ids": "S_TK_NGOMONITOR_2026_VVD", "notes": "NGO Monitor-rapport direct als bron voor Kamervragen"},
    {"dependency_id": "DEP_NGO_DIRECT_PVV_KV", "source_actor_id": "NGO_MONITOR", "dependent_actor_id": "PVV", "material_type": "parliamentary_question", "case_id": "CASE_NGO_OXFAM_2026", "claim_id": "C8", "article_id": "", "parliamentary_item_id": "PQ_MARKUSZOWER_NGO_2026", "dependency_type": "LOBBY_TO_PARLIAMENT", "confidence": "high", "source_ids": "S_TK_NGOMONITOR_2026_MARKUSZOWER", "notes": "NGO Monitor-rapport als bron voor PVV-Kamervragen"},
    # NGO Monitor -> CIDI
    {"dependency_id": "DEP_NGO_CIDI_FRAME", "source_actor_id": "NGO_MONITOR", "dependent_actor_id": "CIDI", "material_type": "public_statement", "case_id": "CASE_ALMEZAN_2020", "claim_id": "C9", "article_id": "", "parliamentary_item_id": "", "dependency_type": "FRAME_REPLICATION", "confidence": "medium", "source_ids": "S_ELSC_JOODS_TELEGRAAF_ALMEZAN", "notes": "CIDI publiceert over PVV-Kamervragen die NGO Monitor claims gebruiken. Indirecte replicatie."},
    # Likoed -> Jonet
    {"dependency_id": "DEP_LIKOED_JONET", "source_actor_id": "LIKOED_NL", "dependent_actor_id": "JONET", "material_type": "article", "case_id": "CASE_SCHOOLBOOK_2019", "claim_id": "C12", "article_id": "ART_JONET_NOORDHOFF_2019", "parliamentary_item_id": "", "dependency_type": "UNCITED_REPLICATION", "confidence": "high", "source_ids": "S_JONET_NOORDHOFF_2019", "notes": "Jonet bericht over Likoed-campagne zonder Likoed als directe bron te vermelden"},
    # CIDI -> NIW
    {"dependency_id": "DEP_CIDI_NIW_DATA", "source_actor_id": "CIDI", "dependent_actor_id": "NIW", "material_type": "article", "case_id": "", "claim_id": "", "article_id": "ART_NIW_CIDI_DATA_2025", "parliamentary_item_id": "", "dependency_type": "DIRECT_CITATION", "confidence": "high", "source_ids": "S_NIW_CIDI_DATA_2025", "notes": "NIW-artikel gebruikt CIDI-data; CIDI-employee is auteur/bron"},
    # CIDI -> media (general safety frame)
    {"dependency_id": "DEP_CIDI_NOS_SAFETY", "source_actor_id": "CIDI", "dependent_actor_id": "NOS", "material_type": "article", "case_id": "CASE_HU_CIDI_2024", "claim_id": "C13", "article_id": "ART_NOS_HU_CIDI_2024", "parliamentary_item_id": "", "dependency_type": "FRAME_REPLICATION", "confidence": "high", "source_ids": "S_NOS_HU_CIDI_2024", "notes": "CIDI-veiligheidsframe gerepliceerd in NOS-rapportage"},
    # CVI -> media platforming
    {"dependency_id": "DEP_CVI_WIERDDUK", "source_actor_id": "CVI_MEDIA", "dependent_actor_id": "WIERD_DUK", "material_type": "podcast", "case_id": "", "claim_id": "C14", "article_id": "ART_CVI_WIERD_DUK_2024", "parliamentary_item_id": "", "dependency_type": "FRAME_REPLICATION", "confidence": "high", "source_ids": "S_CVI_WIERD_DUK_2024", "notes": "CVI geeft podium aan Wierd Duk 'Palestinisering'-frame"},
    # Watchdog -> media (counter-documentation)
    {"dependency_id": "DEP_TRF_TELEGRAAF", "source_actor_id": "TRF", "dependent_actor_id": "TELEGRAAF", "material_type": "report", "case_id": "CASE_NGO_OXFAM_2026", "claim_id": "C3", "article_id": "ART_RIGHTSFORUM_TELEGRAAF_2020", "parliamentary_item_id": "", "dependency_type": "COUNTER_DOCUMENTATION", "confidence": "high", "source_ids": "S_RIGHTSFORUM_TELEGRAAF_2020", "notes": "TRF documenteert Telegraaf als doorgeefluik van NGO Monitor"},
    {"dependency_id": "DEP_ELSC_ALMEZAN_CHAIN", "source_actor_id": "ELSC", "dependent_actor_id": "JOODS_NL", "material_type": "report", "case_id": "CASE_ALMEZAN_2020", "claim_id": "C9", "article_id": "ART_ELSC_2021", "parliamentary_item_id": "", "dependency_type": "WATCHDOG_TO_MEDIA", "confidence": "medium_high", "source_ids": "S_ELSC_JOODS_TELEGRAAF_ALMEZAN", "notes": "ELSC documenteert transmissieroute NGO Monitor -> Joods.nl -> PVV -> CIDI"},
]

write_csv("source_dependency.csv", source_dependencies)
print(f"source_dependency.csv: {len(source_dependencies)} entries")

# ═══════════════════════════════════════════════════════════════
# COMMIT 6: Social / public figures expansion
# ═══════════════════════════════════════════════════════════════

# ── 6a. public_figures.csv ──

FIGURE_HEADER = [
    "person_id","label","person_type","public_role","platforms",
    "known_affiliations","related_claims","related_cases",
    "role_guess","status","priority","source_ids","notes"
]

public_figures = [
    {"person_id": "NAOMI_MESTRUM", "label": "Naomi Mestrum", "person_type": "DIRECTOR", "public_role": "CIDI-directeur; publieke woordvoerder", "platforms": "media;NOS;events", "known_affiliations": "CIDI", "related_claims": "C13;C4", "related_cases": "CASE_HU_CIDI_2024", "role_guess": "primary_spokesperson", "status": "confirmed_actor", "priority": "P1", "source_ids": "S_NOS_HU_CIDI_2024", "notes": "Al in actors.csv als PUBLIC_FIGURE"},
    {"person_id": "ESTHER_VOET", "label": "Esther Voet", "person_type": "EDITOR", "public_role": "NIW-hoofdredacteur; oud-CIDI-directeur", "platforms": "NIW;media", "known_affiliations": "NIW;CIDI", "related_claims": "", "related_cases": "", "role_guess": "media_bridge", "status": "confirmed_actor", "priority": "P1", "source_ids": "S_NIW_REDACTIE;S_NIW_CIDI_DATA_2025", "notes": "Al in actors.csv. Cruciale brug tussen CIDI en NIW."},
    {"person_id": "BART_VAN_DIJK", "label": "Bart van Dijk", "person_type": "EMPLOYEE", "public_role": "CIDI-medewerker; levert data aan NIW", "platforms": "NIW", "known_affiliations": "CIDI", "related_claims": "", "related_cases": "", "role_guess": "data_bridge", "status": "confirmed_actor", "priority": "P2", "source_ids": "S_NIW_CIDI_DATA_2025", "notes": "Al in actors.csv"},
    {"person_id": "WIERD_DUK", "label": "Wierd Duk", "person_type": "JOURNALIST", "public_role": "Telegraaf-columnist; commentaar op media/Israël", "platforms": "Telegraaf;NVD;CVI_podcast", "known_affiliations": "TELEGRAAF;CVI_MEDIA", "related_claims": "C14", "related_cases": "", "role_guess": "opinion_amplifier", "status": "confirmed_actor", "priority": "P2", "source_ids": "S_CVI_WIERD_DUK_2024;S_NVD_WIERD_DUK_2026", "notes": "Al in actors.csv"},
    {"person_id": "LEON_DE_WINTER", "label": "Leon de Winter", "person_type": "JOURNALIST", "public_role": "Schrijver; columnist; opinieplatform", "platforms": "EW;NPO Radio 1;media", "known_affiliations": "EW", "related_claims": "", "related_cases": "", "role_guess": "opinion_amplifier", "status": "confirmed_actor", "priority": "P2", "source_ids": "S_EW_LEON;S_NPORADIO1_LEON_2023", "notes": "Al in actors.csv"},
    {"person_id": "BART_SCHUT", "label": "Bart Schut", "person_type": "OPINION_MAKER", "public_role": "Opiniemaker; publicist over antisemitisme", "platforms": "Cvandaag;NIW", "known_affiliations": "NIW;CIDI_context", "related_claims": "C15", "related_cases": "", "role_guess": "discourse_amplifier", "status": "confirmed_actor", "priority": "P2", "source_ids": "S_CVANDAAG_BARTSCHUT_2017;S_NIW_CIDI_DATA_2025", "notes": "Al in actors.csv"},
    {"person_id": "FRITS_HUFFNAGEL", "label": "Frits Huffnagel", "person_type": "LOBBYIST", "public_role": "Castro-medeoprichter; VVD-connectie", "platforms": "Castro;politiek_netwerk", "known_affiliations": "CASTRO;VVD_context", "related_claims": "", "related_cases": "", "role_guess": "lobby_network_node", "status": "confirmed_actor", "priority": "P1", "source_ids": "S_CASTRO_OVER;S_CASTRO_SITE", "notes": "Al in actors.csv"},
    {"person_id": "RONNY_NAFTANIEL", "label": "Ronny Naftaniel", "person_type": "FORMER_DIRECTOR", "public_role": "Oud-CIDI-directeur; historische rol", "platforms": "media;CIDI_historisch", "known_affiliations": "CIDI", "related_claims": "", "related_cases": "", "role_guess": "historical_bridge", "status": "confirmed_actor", "priority": "P3", "source_ids": "", "notes": "Al in actors.csv"},
    {"person_id": "CHRIS_STOFFER", "label": "Chris Stoffer", "person_type": "POLITICIAN", "public_role": "SGP-Kamerlid; IAF-caucus voorzitter", "platforms": "Tweede Kamer;IAF;ELNET;CVI", "known_affiliations": "SGP;IAF;ELNET;CVI", "related_claims": "", "related_cases": "CASE_IAF_CAUCUS_2013", "role_guess": "parliamentary_network_hub", "status": "confirmed_actor", "priority": "P0", "source_ids": "S_IAF_MEMBERS;S_TK_STOFFER_REIZEN", "notes": "Al in actors.csv. Centrale knoop in IAF/ELNET/CVI-reisnetwerk."},
    {"person_id": "QUEENY_RAJKOWSKI", "label": "Queeny Rajkowski", "person_type": "POLITICIAN", "public_role": "VVD-Kamerlid; stelde vragen over NGO Monitor/Oxfam", "platforms": "Tweede Kamer", "known_affiliations": "VVD", "related_claims": "C8", "related_cases": "CASE_NGO_OXFAM_2026", "role_guess": "question_actor", "status": "confirmed_actor", "priority": "P1", "source_ids": "S_TK_NGOMONITOR_2026_VVD;S_TK_RAJKOWSKI_DETAIL_2026", "notes": "Al in actors.csv"},
    {"person_id": "GIDI_MARKUSZOWER", "label": "Gidi Markuszower", "person_type": "POLITICIAN", "public_role": "PVV-Kamerlid; stelde vragen over NGO Monitor/Oxfam", "platforms": "Tweede Kamer", "known_affiliations": "PVV", "related_claims": "C8;C9", "related_cases": "CASE_NGO_OXFAM_2026;CASE_ALMEZAN_2020", "role_guess": "question_actor", "status": "confirmed_actor", "priority": "P1", "source_ids": "S_TK_NGOMONITOR_2026_MARKUSZOWER", "notes": "Al in actors.csv"},
    {"person_id": "CAROLINE_VDP", "label": "Caroline van der Plas", "person_type": "POLITICIAN", "public_role": "BBB-leider; CestMocro-uitspraak; HU-kritiek", "platforms": "Tweede Kamer;media;X", "known_affiliations": "BBB", "related_claims": "C13;C11", "related_cases": "CASE_HU_CIDI_2024;CASE_CESTMOCRO_BAN_2024", "role_guess": "public_pressure_actor", "status": "confirmed_actor", "priority": "P1", "source_ids": "S_VILLAMEDIA_CESTMOCRO_2024;S_HOP_HU_POLITICI_2024", "notes": "Al in actors.csv"},
    {"person_id": "DILAN_YESILGOZ", "label": "Dilan Yesilgöz", "person_type": "POLITICIAN", "public_role": "VVD-leider; reageerde op HU-case", "platforms": "Tweede Kamer;media;X", "known_affiliations": "VVD", "related_claims": "C13", "related_cases": "CASE_HU_CIDI_2024", "role_guess": "public_pressure_actor", "status": "confirmed_actor", "priority": "P1", "source_ids": "S_HOP_HU_POLITICI_2024", "notes": "Al in actors.csv"},
    {"person_id": "PIETER_OMTZIGT", "label": "Pieter Omtzigt", "person_type": "POLITICIAN", "public_role": "NSC-leider; reageerde op HU-case", "platforms": "Tweede Kamer;media;X", "known_affiliations": "NSC", "related_claims": "C13", "related_cases": "CASE_HU_CIDI_2024", "role_guess": "public_pressure_actor", "status": "confirmed_actor", "priority": "P2", "source_ids": "S_HOP_HU_POLITICI_2024", "notes": "Al in actors.csv"},
]

# Add more public figures leads (not yet in actors.csv)
public_figures += [
    {"person_id": "QUEEN_MAXIMA", "label": "Koningin Máxima", "person_type": "ROYAL", "public_role": "Koninklijk; genoemd in NGO Monitor-context", "platforms": "publiek", "known_affiliations": "", "related_claims": "", "related_cases": "CASE_NGO_OXFAM_2026", "role_guess": "passive_reference", "status": "confirmed_actor", "priority": "P4", "source_ids": "S_TK_NGOMONITOR_2026_VVD", "notes": "Al in actors.csv. Alleen genoemd in Kamervragen, geen actieve rol."},
    {"person_id": "ANNELOTTE_LAMMERS", "label": "Annelotte Lammers", "person_type": "POLITICIAN", "public_role": "PVV-Kamerlid; mede-indiener NGO Monitor-Kamervragen", "platforms": "Tweede Kamer", "known_affiliations": "PVV", "related_claims": "C8", "related_cases": "CASE_NGO_OXFAM_2026", "role_guess": "question_actor", "status": "confirmed_actor", "priority": "P2", "source_ids": "S_TK_NGOMONITOR_2026_MARKUSZOWER", "notes": "Al in actors.csv"},
    {"person_id": "THIERRY_BAUDET", "label": "Thierry Baudet", "person_type": "POLITICIAN", "public_role": "FVD-leider; pro-Israël standpunten", "platforms": "Tweede Kamer;social_media", "known_affiliations": "FVD", "related_claims": "", "related_cases": "", "role_guess": "ideological_aligner", "status": "raw_lead", "priority": "P3", "source_ids": "", "notes": "Niet in actors.csv. FVD mogelijk relevante partij."},
    {"person_id": "GIDEON_VAN_MEIJEREN", "label": "Gideon van Meijeren", "person_type": "POLITICIAN", "public_role": "FVD-Kamerlid", "platforms": "Tweede Kamer", "known_affiliations": "FVD", "related_claims": "", "related_cases": "", "role_guess": "ideological_aligner", "status": "raw_lead", "priority": "P4", "source_ids": "", "notes": ""},
    {"person_id": "ARJAN_VLIEGENTHART", "label": "Arjan Vliegenthart", "person_type": "DIRECTOR", "public_role": "Oud-directeur; NGO/TWijn", "platforms": "media", "known_affiliations": "", "related_claims": "", "related_cases": "", "role_guess": "context_knower", "status": "raw_lead", "priority": "P4", "source_ids": "", "notes": "Lead: rol in NGO-wereld"},
]

write_csv("public_figures.csv", public_figures)
print(f"public_figures.csv: {len(public_figures)} entries")

# ── 6b. social_accounts.csv (expand from existing actors) ──

ACCOUNT_HEADER = [
    "account_id","actor_id","platform","handle","url",
    "account_type","confidence","source_ids","notes"
]

social_accounts = [
    {"account_id": "SOC_X_YESILGOZ", "actor_id": "DILAN_YESILGOZ", "platform": "X", "handle": "@DilanYesilgoz", "url": "https://x.com/DilanYesilgoz", "account_type": "official", "confidence": "high", "source_ids": "S_HOP_HU_POLITICI_2024", "notes": "X-post over HU-case in 2024"},
    {"account_id": "SOC_X_OMTZIGT", "actor_id": "PIETER_OMTZIGT", "platform": "X", "handle": "@PieterOmtzigt", "url": "https://x.com/PieterOmtzigt", "account_type": "official", "confidence": "high", "source_ids": "S_HOP_HU_POLITICI_2024", "notes": "X-post over HU-case in 2024"},
    {"account_id": "SOC_X_VDP", "actor_id": "CAROLINE_VDP", "platform": "X", "handle": "@CarolineVdPlas", "url": "https://x.com/CarolineVdPlas", "account_type": "official", "confidence": "high", "source_ids": "S_HOP_HU_POLITICI_2024", "notes": ""},
    {"account_id": "SOC_INSTA_CESTMOCRO", "actor_id": "CESTMOCRO", "platform": "Instagram", "handle": "@cestmocro", "url": "", "account_type": "content_account", "confidence": "high", "source_ids": "S_CIDI_CESTMOCRO_2023;S_NOS_CESTMOCRO_2023", "notes": "Account waar CIDI aangifte tegen deed"},
    {"account_id": "SOC_X_WIERDDUK", "actor_id": "WIERD_DUK", "platform": "X", "handle": "@WierdDuk", "url": "https://x.com/WierdDuk", "account_type": "official", "confidence": "high", "source_ids": "", "notes": ""},
    {"account_id": "SOC_X_LEONWINTER", "actor_id": "LEON_DE_WINTER", "platform": "X", "handle": "@LeondeWinter", "url": "https://x.com/LeondeWinter", "account_type": "official", "confidence": "medium_high", "source_ids": "", "notes": ""},
    {"account_id": "SOC_CIDI_WEBSITE", "actor_id": "CIDI", "platform": "web", "handle": "cidi.nl", "url": "https://www.cidi.nl", "account_type": "official_website", "confidence": "high", "source_ids": "", "notes": ""},
    {"account_id": "SOC_CIDI_X", "actor_id": "CIDI", "platform": "X", "handle": "@CIDI_Israel", "url": "https://x.com/CIDI_Israel", "account_type": "official", "confidence": "high", "source_ids": "", "notes": ""},
    {"account_id": "SOC_NGO_MONITOR_WEB", "actor_id": "NGO_MONITOR", "platform": "web", "handle": "ngo-monitor.org", "url": "https://www.ngo-monitor.org", "account_type": "official_website", "confidence": "high", "source_ids": "", "notes": ""},
    {"account_id": "SOC_IAF_WEB", "actor_id": "IAF", "platform": "web", "handle": "israelallies.org", "url": "https://israelallies.org", "account_type": "official_website", "confidence": "high", "source_ids": "", "notes": ""},
    {"account_id": "SOC_NIW_WEB", "actor_id": "NIW", "platform": "web", "handle": "niw.nl", "url": "https://niw.nl", "account_type": "news_website", "confidence": "high", "source_ids": "", "notes": ""},
    {"account_id": "SOC_JONET_WEB", "actor_id": "JONET", "platform": "web", "handle": "jonet.nl", "url": "https://jonet.nl", "account_type": "news_website", "confidence": "high", "source_ids": "", "notes": ""},
    {"account_id": "SOC_TELEGRAAF_WEB", "actor_id": "TELEGRAAF", "platform": "web", "handle": "telegraaf.nl", "url": "https://www.telegraaf.nl", "account_type": "news_website", "confidence": "high", "source_ids": "", "notes": ""},
    {"account_id": "SOC_CVI_WEB", "actor_id": "CVI", "platform": "web", "handle": "christenenvoorisrael.nl", "url": "https://www.christenenvoorisrael.nl", "account_type": "advocacy_website", "confidence": "high", "source_ids": "", "notes": ""},
]

write_csv("social_accounts.csv", social_accounts)
print(f"social_accounts.csv: {len(social_accounts)} entries")

# ── 6c. Expand social_posts.csv (add new posts, keep existing) ──

POST_HEADER = [
    "post_id","platform","actor_id","account_handle","date","url",
    "case_id","claim_id","post_type","quoted_source_id","amplified_actor_id",
    "engagement_metric","confidence","notes"
]

existing_posts = read_csv("social_posts.csv")

new_posts = [
    {"post_id": "SOC_YESILGOZ_HU_2024_X", "platform": "X", "actor_id": "DILAN_YESILGOZ", "account_handle": "@DilanYesilgoz", "date": "2024", "url": "", "case_id": "CASE_HU_CIDI_2024", "claim_id": "C13", "post_type": "public_criticism", "quoted_source_id": "", "amplified_actor_id": "CIDI", "engagement_metric": "", "confidence": "high", "notes": "Yesilgöz: HU postponement a 'gotspe' / disgrace. Source: HOP."},
    {"post_id": "SOC_OMTZIGT_HU_2024_X", "platform": "X", "actor_id": "PIETER_OMTZIGT", "account_handle": "@PieterOmtzigt", "date": "2024", "url": "", "case_id": "CASE_HU_CIDI_2024", "claim_id": "C13", "post_type": "public_criticism", "quoted_source_id": "", "amplified_actor_id": "CIDI", "engagement_metric": "", "confidence": "medium_high", "notes": "Omtzigt: questioned HU moral compass. Source: HOP."},
    {"post_id": "SOC_VDP_CESTMOCRO_2024", "platform": "media", "actor_id": "CAROLINE_VDP", "account_handle": "", "date": "2024", "url": "", "case_id": "CASE_CESTMOCRO_BAN_2024", "claim_id": "C11", "post_type": "public_statement", "quoted_source_id": "", "amplified_actor_id": "CIDI", "engagement_metric": "", "confidence": "high", "notes": "Van der Plas suggests CestMocro ban. Source: Villamedia."},
    {"post_id": "SOC_YESILGOZ_GENOCIDE_2024", "platform": "media", "actor_id": "DILAN_YESILGOZ", "account_handle": "", "date": "2024", "url": "", "case_id": "", "claim_id": "C15", "post_type": "public_statement", "quoted_source_id": "", "amplified_actor_id": "", "engagement_metric": "", "confidence": "medium", "notes": "Yesilgóz: 'ik vind dat je het woord genocide niet in de mond moet nemen' - positie in lijn met CIDI/Israël framing. Lead: exact citaat vinden."},
]

# Merge: keep existing posts, add new ones (avoid duplicates)
existing_post_ids = {p["post_id"] for p in existing_posts}
for np in new_posts:
    if np["post_id"] not in existing_post_ids:
        existing_posts.append(np)

# Ensure header order
ordered_posts = []
for p in existing_posts:
    ordered = {k: p.get(k, "") for k in POST_HEADER}
    ordered_posts.append(ordered)

write_csv("social_posts.csv", ordered_posts)
print(f"social_posts.csv: {len(ordered_posts)} entries (merged)")

print("\nv5 research layer build complete.")
print(f"New files: research_entities, research_edges, research_aliases, research_tasks")
print(f"New files: donors, funding_flows, foundation_filings, foreign_state_funding")
print(f"New files: source_dependency")
print(f"New files: public_figures, social_accounts")
print(f"Updated: social_posts")
