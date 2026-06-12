# v4 repair + audit + v5 rapport

Generated: 2026-06-12

## Phase 1: CSV-repair

| bestand | probleem | herstel |
|---|---|---|
| actors.csv | 7 ontbrekende referentie-nodes toegevoegd | hersteld |
| cases.csv | 1 rij (CASE_CESTMOCRO_BAN_2024) had extra leeg amplifier-veld → kolomverschuiving | hersteld |
| claims.csv | 3 rijen (C5, C7, C11) hadden ongequote komma's in notes | hersteld |
| outcomes.csv | 1 rij (OUTC_HU_POLITICAL_PRESSURE_2024) had ongequote komma's in description en notes | hersteld |
| sources.csv | 1 rij (S_ELSC_2021) had ongequote komma in reliability_note | hersteld |

## Phase 2: Audit

Missing refs in edges.csv: 0
Missing refs in other tables: 0
Missing source refs: 0

### Tabel telling na repair

| bestand | rijen |
|---|---|
| actors.csv | 79 |
| articles.csv | 23 |
| cases.csv | 10 |
| claims.csv | 15 |
| edges.csv | 111 |
| events.csv | 7 |
| funding.csv | 7 |
| legal_actions.csv | 2 |
| outcomes.csv | 8 |
| parliamentary_items.csv | 11 |
| sources.csv | 38 |
| travel.csv | 2 |

## Phase 3: V5 - Claim-level provenance expansion

| tabel | rijen | functie |
|---|---|---|
| article_claim_links.csv | 14 | Koppelt media-artikelen aan claims via edges, case chains en originator-relaties |
| copy_overlap.csv | 0 | Voorbereiding voor tekstoverlapmeting tussen rapporten en artikelen |
| event_participants.csv | 12 | Deelnemers aan events met rol |
| organization_people_roles.csv | 10 | Personele relaties (oud-medewerker, founder, editor, etc.) |
| parliamentary_claim_links.csv | 8 | Koppelt Kamervragen/moties/reisregistraties aan claims |
| social_posts.csv | 5 | Social media / publieke uitingen van actoren (X, Instagram, media-statements) |
| timeline_events.csv | 97 | Tijdlijn van gebeurtenissen per case, gesorteerd op datum |

## Volgende stappen

1. Per case 5-20 media-items toevoegen aan articles.csv met exacte datums
2. social_posts.csv uitbreiden met systematische X/YouTube/podcast-verzameling
3. copy_overlap.csv vullen via tekstoverlap-analyse (bijv. diff/Python difflib)
4. Datumvelden verbeteren naar ISO-formaat (YYYY-MM-DD) voor temporale sequencing
