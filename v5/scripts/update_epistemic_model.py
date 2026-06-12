#!/usr/bin/env python3
"""
Apply capture-aware epistemic model to v5.
- Adds pattern/transmission/impact/capture fields to cases.csv and claims.csv
- Rewrites METHODOLOGY_V5.md with the new framework
"""

import csv, shutil, re
from pathlib import Path

V5 = Path(r"C:\Users\gewoo\israel nederland lobbie\v5")
BAK = V5 / "bak_epistemic"
BAK.mkdir(exist_ok=True)

def read_csv(name):
    with open(V5 / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(name, rows):
    if not rows:
        return
    # backup original
    src = V5 / name
    if src.exists():
        shutil.copy2(src, BAK / name)
    with open(src, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)

# ── 1. Add assessment cols to cases.csv ──

cases = read_csv("cases.csv")
cases_header = list(cases[0].keys())

# Define new cols
new_case_cols = [
    "pattern_strength", "transmission_strength", "impact_strength",
    "capture_risk", "independent_verification_level", "institutional_self_interest"
]
for c in new_case_cols:
    if c not in cases_header:
        cases_header.append(c)

# Assessment data per case
case_assessment = {
    "CASE_NGO_OXFAM_2026": {
        "pattern_strength": "high",
        "transmission_strength": "high",
        "impact_strength": "medium",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "high",
    },
    "CASE_ALMEZAN_2020": {
        "pattern_strength": "high",
        "transmission_strength": "high",
        "impact_strength": "medium",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "high",
    },
    "CASE_UAWC_DEFUNDING": {
        "pattern_strength": "medium",
        "transmission_strength": "medium",
        "impact_strength": "medium",
        "capture_risk": "high",
        "independent_verification_level": "low",
        "institutional_self_interest": "high",
    },
    "CASE_CESTMOCRO_2023": {
        "pattern_strength": "medium",
        "transmission_strength": "high",
        "impact_strength": "medium",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "high",
    },
    "CASE_SCHOOLBOOK_2015": {
        "pattern_strength": "low",
        "transmission_strength": "low",
        "impact_strength": "low",
        "capture_risk": "low",
        "independent_verification_level": "low",
        "institutional_self_interest": "low",
    },
    "CASE_SCHOOLBOOK_2019": {
        "pattern_strength": "low",
        "transmission_strength": "low",
        "impact_strength": "low",
        "capture_risk": "low",
        "independent_verification_level": "low",
        "institutional_self_interest": "low",
    },
    "CASE_HU_CIDI_2024": {
        "pattern_strength": "medium",
        "transmission_strength": "high",
        "impact_strength": "high",
        "capture_risk": "medium",
        "independent_verification_level": "low",
        "institutional_self_interest": "medium",
    },
    "CASE_IAF_CAUCUS_2013": {
        "pattern_strength": "medium",
        "transmission_strength": "medium",
        "impact_strength": "high",
        "capture_risk": "low",
        "independent_verification_level": "high",
        "institutional_self_interest": "medium",
    },
    "CASE_CESTMOCRO_BAN_2024": {
        "pattern_strength": "low",
        "transmission_strength": "low",
        "impact_strength": "low",
        "capture_risk": "medium",
        "independent_verification_level": "medium",
        "institutional_self_interest": "medium",
    },
    "CASE_IAF_EU_OFFICE": {
        "pattern_strength": "low",
        "transmission_strength": "low",
        "impact_strength": "low",
        "capture_risk": "low",
        "independent_verification_level": "high",
        "institutional_self_interest": "medium",
    },
}

cases_out = []
for row in cases:
    cid = row["case_id"]
    if cid in case_assessment:
        row.update(case_assessment[cid])
    else:
        for c in new_case_cols:
            row.setdefault(c, "unknown")
    # Keep header order
    ordered = {k: row.get(k, "") for k in cases_header}
    cases_out.append(ordered)

write_csv("cases.csv", cases_out)
print(f"cases.csv: updated {len(case_assessment)} cases with assessment fields")

# ── 2. Add assessment cols to claims.csv ──

claims = read_csv("claims.csv")
claims_header = list(claims[0].keys())

new_claim_cols = [
    "pattern_strength", "transmission_strength",
    "capture_risk", "independent_verification_level"
]
for c in new_claim_cols:
    if c not in claims_header:
        claims_header.append(c)

claim_assessment = {
    "C1": {"pattern_strength": "high", "transmission_strength": "high",
           "capture_risk": "medium", "independent_verification_level": "low"},
    "C2": {"pattern_strength": "high", "transmission_strength": "high",
           "capture_risk": "high", "independent_verification_level": "low"},
    "C3": {"pattern_strength": "high", "transmission_strength": "medium",
           "capture_risk": "medium", "independent_verification_level": "low"},
    "C4": {"pattern_strength": "medium", "transmission_strength": "high",
           "capture_risk": "medium", "independent_verification_level": "low"},
    "C5": {"pattern_strength": "high", "transmission_strength": "high",
           "capture_risk": "high", "independent_verification_level": "low"},
    "C6": {"pattern_strength": "medium", "transmission_strength": "medium",
           "capture_risk": "high", "independent_verification_level": "low"},
    "C7": {"pattern_strength": "high", "transmission_strength": "medium",
           "capture_risk": "medium", "independent_verification_level": "low"},
    "C8": {"pattern_strength": "high", "transmission_strength": "high",
           "capture_risk": "high", "independent_verification_level": "low"},
    "C9": {"pattern_strength": "high", "transmission_strength": "high",
           "capture_risk": "high", "independent_verification_level": "low"},
    "C10": {"pattern_strength": "medium", "transmission_strength": "medium",
            "capture_risk": "high", "independent_verification_level": "low"},
    "C11": {"pattern_strength": "medium", "transmission_strength": "high",
            "capture_risk": "medium", "independent_verification_level": "low"},
    "C12": {"pattern_strength": "low", "transmission_strength": "low",
            "capture_risk": "low", "independent_verification_level": "low"},
    "C13": {"pattern_strength": "medium", "transmission_strength": "high",
            "capture_risk": "medium", "independent_verification_level": "low"},
    "C14": {"pattern_strength": "low", "transmission_strength": "low",
            "capture_risk": "low", "independent_verification_level": "low"},
    "C15": {"pattern_strength": "medium", "transmission_strength": "medium",
            "capture_risk": "medium", "independent_verification_level": "low"},
}

claims_out = []
for row in claims:
    cid = row["claim_id"]
    if cid in claim_assessment:
        row.update(claim_assessment[cid])
    else:
        for c in new_claim_cols:
            row.setdefault(c, "unknown")
    ordered = {k: row.get(k, "") for k in claims_header}
    claims_out.append(ordered)

write_csv("claims.csv", claims_out)
print(f"claims.csv: updated {len(claim_assessment)} claims with assessment fields")

# ── 3. Rewrite METHODOLOGY_V5.md ──

methodology = r"""# v5 — capture-aware influence provenance graph

## Epistemische basis

Deze dataset gebruikt geen institutionele bevestiging als primaire waarheidsstandaard.
Bewijswaarde wordt opgebouwd uit observeerbare sporen, temporele volgorde, tekstuele
overeenkomst, netwerkpositie, herhaling over cases en onafhankelijke triangulatie.
Ontkenningen of non-confirmations door betrokken actoren worden gemodelleerd als
institutionele posities met mogelijk eigenbelang, niet als sluitende weerlegging.

## Bewijsniveaus

| niveau | betekenis | voorbeeld |
|--------|-----------|-----------|
| OBSERVED_TRACE | Publieke handeling bestaat aantoonbaar | Artikel, Kamervraag, reisregistratie, event |
| SOURCE_CLAIM | Actor beweert iets | NGO Monitor-rapport, CIDI-persbericht |
| REPLICATED_FRAME | Frame komt herkenbaar terug bij andere actor | Zelfde framing in media en politiek |
| TEMPORAL_CHAIN | Publicatie A gaat aantoonbaar vooraf aan actie B | Artikel → Kamervraag → ministeriële reactie |
| TEXTUAL_OVERLAP | Formuleringen overlappen meetbaar | Tussen bronrapport en media-artikel |
| NETWORK_PROXIMITY | Actorrelaties, events, reizen, functies, platforms | Gedeeld podium, zelfde reis, personele overlap |
| CONVERGENT_PATTERN | Meerdere onafhankelijke sporen wijzen dezelfde kant op | Herhaalde transmissie over verschillende cases |
| INSTITUTIONAL_DENIAL | Betrokken instelling ontkent of bevestigt niet | Kabinet zegt "geen informatie" |
| ADJUDICATED_FACT | Rechter, audit of onafhankelijk onderzoek stelt iets vast | Gerechtelijke uitspraak |
| UNRESOLVED_BUT_STRUCTURED | Sterk patroon, geen definitieve adjudicatie | Meerdere cases, zelfde mechanisme, geen uitspraak |

**INSTITUTIONAL_DENIAL is niet sterker dan CONVERGENT_PATTERN.**
Het is een datapunt met eigenbelang, geen waarheidsvinding.

## Drie te scheiden lagen

| laag | vraag | bewijsstandaard |
|------|-------|----------------|
| Trace | Bestaat het spoor? | Publiek observeerbaar (artikel, KV, reis, post) |
| Transmission | Reist dezelfde claim door meerdere lagen? | Timing + herhaling + bronketen |
| Intent/coördinatie | Is er bewuste aansturing? | Hogere drempel: communicatie, gedeeld event, personele link, timingpatroon |

Voor transmissie heb je geen bekentenis nodig.
Voor coördinatie heb je zwaardere indicatoren nodig.
Voor impact kijk je naar gevolgen, niet naar wat betrokkenen zeggen dat hun intentie was.

## Capture-aware analyse

invloed ≠ bewezen intentie
invloed = herhaalbare transmissie + toegang + versterking + institutioneel gevolg

Intentie is een dimensie. Niet de enige. Een actor kan invloed uitoefenen zonder
dat je een e-mail, bekentenis of formeel contract hebt. Als dezelfde claim via
dezelfde bronketen telkens leidt tot media-aandacht, Kamervragen, subsidievragen
of reputatieschade, dan is dat een relevant machtsmechanisme.

## Assessment-velden per case

Elke case in cases.csv heeft deze capture-aware beoordeling:

| veld | waarden | betekenis |
|------|---------|-----------|
| pattern_strength | low/medium/high | Mate van patroonherhaling over cases |
| transmission_strength | low/medium/high | Hoeveel schakels in de transmissieketen zijn gedocumenteerd |
| impact_strength | low/medium/high | Zichtbare gevolgen (Kamervragen, annulering, beleidseffect) |
| capture_risk | low/medium/high | Mate waarin instituties eigenbelang hebben bij uitkomst |
| independent_verification_level | low/medium/high | Onafhankelijke verificatie (rechter, audit, reproduceerbaar dossier) |
| institutional_self_interest | low/medium/high | Belangen van betrokken overheids-/institutionele actoren |

Vergelijkbaar voor claims in claims.csv: pattern_strength, transmission_strength,
capture_risk, independent_verification_level.

## Wat wél en niet bewezen wordt

| claimtype | nodig bewijs |
|-----------|--------------|
| "X publiceerde Y" | Publicatie |
| "X citeerde Y" | Tekst / bronverwijzing |
| "X nam frame over" | Inhoudelijke overeenkomst |
| "X bracht claim politiek binnen" | Kamervraag / motie / debat |
| "X veroorzaakte outcome" | Timing + plausibel mechanisme + outcome |
| "X coördineerde met Y" | Zwaarder: communicatie, gedeeld event, campagne, personele link |
| "X controleert Y" | Zeer zwaar: redactionele aansturing, financiering, instructies |

Frame-amplificatie, institutionele transmissie en drukmechanismen hebben lage,
observeerbare drempels. Controle blijft een hoge drempel.

## 19 tabellen

| Tabel | Rijen | Inhoud |
|-------|-------|--------|
| actors.csv | 81 | Actoren met type, tier, rol |
| claims.csv | 15 | Claims met assessment-velden |
| articles.csv | 23 | Media-artikelen, rapporten, podcasts |
| parliamentary_items.csv | 11 | Kamervragen, moties, reisregistraties |
| events.csv | 7 | Panels, lezingen, conferenties |
| travel.csv | 2 | Israel-reizen met reiziger en organizer |
| funding.csv | 7 | Subsidies, donaties, reisbekostiging |
| legal_actions.csv | 2 | Aangiftes, klachten, sommaties |
| outcomes.csv | 8 | Outcome events |
| cases.csv | 10 | Cases met capture-aware assessment |
| edges.csv | 118 | Alle relaties tussen nodes |
| sources.csv | 38 | Bronregister |
| article_claim_links.csv | 14 | Artikelen aan claims gekoppeld |
| parliamentary_claim_links.csv | 8 | Kamervragen aan claims gekoppeld |
| timeline_events.csv | 97 | Chronologische gebeurtenissen |
| copy_overlap.csv | — | Tekstoverlap (te vullen) |
| social_posts.csv | 5 | Publieke uitingen |
| event_participants.csv | 12 | Wie deed mee aan welk event |
| organization_people_roles.csv | 10 | Personele verbanden |

## 6 analysevragen

1. Wie produceert de claim? → claims.originator_actor_id
2. Wie versterkt de claim? → article_claim_links + edges[MEDIA_AMPLIFICATION]
3. Wie brengt hem politiek binnen? → parliamentary_claim_links + edges[PARLIAMENTARY_QUESTION]
4. Welke actoren hebben toegang tot besluitvorming? → tier T0-T1 met edges naar DUTCH_GOV/TWEEDE_KAMER
5. Welke impact volgt? → outcomes + edges[RESULTED_IN]
6. Wat is de timing? → timeline_events
"""

(V5 / "METHODOLOGY_V5.md").write_text(methodology, encoding="utf-8")
print("METHODOLOGY_V5.md rewritten with capture-aware epistemic model")

print("\nDone. Run generate_graphml.py to rebuild the graph with updated fields.")
