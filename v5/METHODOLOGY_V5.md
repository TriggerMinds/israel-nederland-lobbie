# v5 — claim-level provenance graph

## What changed from v4

v5 is v4 + claim-level provenance expansion. The schema is unchanged (same 12 base tables),
but 7 new tables add explicit claim-linkage, temporal ordering, and social/event layers.

## v5 tables

| tabel | rijen | functie |
|-------|-------|---------|
| actors.csv | 81 | Actoren: organisaties, personen, media, partijen (T0–T5) |
| claims.csv | 15 | Retorische strategieën, frames, aantijgingen |
| articles.csv | 23 | Media-artikelen, rapporten, podcasts |
| parliamentary_items.csv | 11 | Kamervragen, moties, reisregistraties |
| events.csv | 7 | Conferenties, panels, lezingen |
| travel.csv | 2 | Israël-reizen, delegaties |
| funding.csv | 7 | Subsidies, donaties, reisbekostiging |
| legal_actions.csv | 2 | Aangiftes, klachten, sommaties |
| outcomes.csv | 8 | Zichtbare impact |
| cases.csv | 10 | Centrale casustabel: claim → transmissie → outcome |
| edges.csv | 118 | Alle relaties tussen nodes (multi-type) |
| sources.csv | 38 | Bronregister met URLs en betrouwbaarheid |
| article_claim_links.csv | 14 | Koppelt media-artikelen aan claims |
| parliamentary_claim_links.csv | 8 | Koppelt Kamervragen/moties aan claims |
| timeline_events.csv | 97 | Chronologische events per case |
| copy_overlap.csv | 0 | Tekstoverlap-paren (te vullen) |
| social_posts.csv | 5 | Social media / publieke uitingen |
| event_participants.csv | 12 | Deelnemers aan events met rol |
| organization_people_roles.csv | 10 | Personele relaties |

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
