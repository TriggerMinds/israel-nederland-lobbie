# Israel advocacy SNA NL — v5 claim-level provenance graph

Multi-layer influence graph dataset: inzet, transmissie en institutionele impact
van pro-Israël advocacy in Nederland.

## Structuur (19 tabellen)

| Laag | Bestand | Rijen |
|------|---------|-------|
| Actoren | actors.csv | 81 |
| Claims | claims.csv | 15 |
| Artikelen | articles.csv | 23 |
| Parlementaire items | parliamentary_items.csv | 11 |
| Events | events.csv | 7 |
| Reizen | travel.csv | 2 |
| Financiering | funding.csv | 7 |
| Juridische acties | legal_actions.csv | 2 |
| Outcomes | outcomes.csv | 8 |
| Cases | cases.csv | 10 |
| Edges | edges.csv | 118 |
| Bronnen | sources.csv | 38 |
| Article–claim links | article_claim_links.csv | 14 |
| Parliamentary–claim links | parliamentary_claim_links.csv | 8 |
| Timeline events | timeline_events.csv | 97 |
| Text overlap (voorbereid) | copy_overlap.csv | 0 |
| Social posts | social_posts.csv | 5 |
| Event participants | event_participants.csv | 12 |
| Organisatie-personeel | organization_people_roles.csv | 10 |

## Methodologie

Zie `METHODOLOGY_V5.md` voor de volledige methodologische verantwoording.

## Kernregel

Een bron bewijst dat een publieke handeling, claim, publicatie, reis, klacht,
Kamervraag of institutionele reactie heeft plaatsgevonden.
Een bron bewijst NIET automatisch dat de inhoudelijke claim waar is.

## v5 scripts

`scripts/repair_and_v5.py` — pipeline: v4-repair → audit → v5 tabellen
`scripts/consolidate_v5.py` — consolidatie van v2 + v4 + v5 naar enkel v5/

## Dataset opbouw

v5 = v2 (actor-network) + v4 (multi-layer graph) + v5 (claim-level provenance expansion)

Zie `V2_INTEGRATION.md` voor details over wat uit eerdere versies is overgenomen.
