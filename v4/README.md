# Israel-advocacy SNA NL — v4 multi-layer influence graph

Generated: 2026-06-12

## Structuur

v4 breidt v3 uit van een actor-netwerk naar een multi-layer influence graph met
gescheiden tabellen voor elke analytische laag:

| Laag | Bestand | Inhoud |
|------|---------|--------|
| Actoren | actors.csv | organisaties, personen, media, partijen (T0–T5) |
| Claims | claims.csv | retorische strategieën, frames, aantijgingen |
| Artikelen | articles.csv | media-artikelen, rapporten, podcasts |
| Parlementaire items | parliamentary_items.csv | Kamervragen, moties, reisregistraties, ministeriele reacties |
| Events | events.csv | conferenties, panels, lezingen, podia |
| Reizen | travel.csv | Israël-reizen, delegaties, gesponsorde bezoeken |
| Financiering | funding.csv | subsidies, donaties, reisbekostiging |
| Juridische acties | legal_actions.csv | aangiftes, klachten, sommaties |
| Outcomes | outcomes.csv | zichtbare impact: annulering, Kamervraag, beleidsreactie |
| Cases | cases.csv | centrale casustabel: claim -> transmissie -> outcome |
| Edges | edges.csv | alle relaties tussen nodes uit alle lagen |
| Bronnen | sources.csv | bronregister met URLs en betrouwbaarheidsnotities |

## Belangrijkste wijzigingen tov v3

1. **Abstracte concepten verplaatst naar claims.csv**: voormalige abstracte nodes (ANTIZIONISM_FRAME, SMEAR_CAMPAIGN, CHILLING_EFFECT, etc.) zijn nu claims met claim_type, adjudication_status en evidence_status.

2. **Bronketens als edges**: waar v3 `NGO_MONITOR -> TELEGRAAF` had als FRAME_SUPPLY, voegt v4 artikel-level edges toe zoals `ART_ELSC_2021 -> CIDI` en parlementaire edges zoals `PQ_RAJKOWSKI_NGO_2026 -> DUTCH_GOV`.

3. **Rolscheiding**: actors.csv heeft `tier`-kolom om kernactoren (T0), structurele brokers (T1) en incidentele deelnemers (T3–T5) te scheiden. `actor_type` vervangt `entity_kind`/`actor_class` met vaste typologie: ADVOCACY_ORG, PR_FIRM, COUNTER_ACTOR, TRANSNATIONAL_HUB, etc.

4. **Multi-type edges**: edge_type omvat nu AUTHORED_BY, CITES_SOURCE, FUNDED_BY, RESULTED_IN, TRIGGERED_BY, SPONSORED_BY, etc. — niet alleen lobby-relaties.

5. **Casus-centraal model**: cases.csv koppelt claims aan actoren, transmissie, institutionele targets en outcomes. Elke case heeft een eigen adjudication_status.

6. **Bronkritiek expliciet**: nested_source, primary_source_independent en reliability_note in sources.csv maken zichtbaar welke edges van ELSC/TRF afhankelijk zijn vs onafhankelijk geverifieerd.

## Edge types per laag

De `source_type` en `target_type` kolommen in edges.csv geven aan welk type node betrokken is:
- `actor` -> `actor`: directe actor-relatie
- `article` -> `actor`: artikel relateert aan actor
- `parliamentary_item` -> `actor`: Kamervraag/motie relateert aan actor
- `claim` -> `actor`: claim wordt geuit over actor
- `event` -> `actor`: event relateert aan actor
- `travel` -> `actor`: reis relateert aan actor
- `funding` -> `actor`: financiering naar actor
- `legal_action` -> `actor`: rechtszaak/klacht naar actor
- `outcome` -> `event/parliamentary_item`: outcome volgt uit eerdere node

## Filteradvies per analysevraag

| Vraag | Filter |
|-------|--------|
| Publieke lobby-map | `source_type=actor AND target_type=actor AND tier IN (T0,T1) AND confidence IN (high,medium_high)` |
| Transmissieketen per case | Filter op `case_id` + alle edges met die case_id |
| Claim-provenance | `source_type IN (article,claim,report) AND edge_type IN (AUTHORED_BY,REPLICATES_FRAME,CITES_SOURCE)` |
| Institutionele druk | `edge_type IN (PARLIAMENTARY_QUESTION,OFFICIAL_NONCONFIRMATION,POLICY_INPUT)` |
| Geld/sponsoring | `edge_type IN (FUNDED_BY,SPONSORED_BY) OF source_type IN (funding,travel)` |
| Rol-gebaseerd (geen lobby-label) | Gebruik `actor_type` i.p.v. enkel `actor_class` |
| Conservative view | `risk_flags NOT LIKE '%contested_claim%' AND confidence IN (high,medium_high)` |

## Epistemische regels (v4 aangescherpt)

1. Een officiële bron bewijst dat een institutie iets zegt of doet. **Niet** dat het inhoudelijk waar is.

2. `confidence` beschrijft vertrouwen dat de publieke relatie/handeling bestaat, niet vertrouwen dat de inhoudelijke claim waar is.

3. **Overheidsreacties zijn politieke posities, geen onafhankelijke waarheidsvinding.** Alle overheidsreacties hebben `epistemic_role = political_position_not_investigation` en `risk_flags = institutional_self_interest;potential_non_transparency`. Non-confirmation ≠ falsification. Due-diligence assertions ≠ externe audit. De overheid is donor, beleidsverantwoordelijke en politieke actor in dit dossier — geen neutrale arbiter.

4. **Analytisch onderscheid Israëlisch/pro-Israël/zionistisch/christelijk-zionistisch**: Deze categorieën worden niet samengevoegd. `sub_type` in actors.csv geeft de categorisering.

5. **BN'ers, journalisten en influencers zijn standaard AMPLIFIER, niet LOBBY_ACTOR.** Alleen bij bewijs van formele rol, betaling of gecoördineerde campagne wordt het lobby-label gebruikt.

6. Gebruik minimaal drie lagen: claim-origin, transmission, adjudication. Alleen laag 3 (onafhankelijke rechterlijke uitspraak, openbaar bewijsdossier, reproduceerbare primaire brondocumentatie) kan inhoudelijke validiteit benaderen.

## Uitbreidingsrichtingen

- Social media edge data (X, LinkedIn, YouTube, Instagram)
- Volledige subsidy dataset (BuZa, RVO, NGO-jaarverslagen)
- PR- en communicatiebureau-opdrachten en facturen
- Rechtersuitspraken en klachten bij CvdM/Raad voor Journalistiek
- DNA/tekstoverlap-analyse van media-artikelen
- Internationale contextnodes (VS-organisaties, EU-instellingen)
