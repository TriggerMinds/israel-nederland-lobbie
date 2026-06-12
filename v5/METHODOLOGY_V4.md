# v4 methodologie: multi-layer influence graph

## Waarom v4?

v3 was een solide actor-netwerk met retorische strategieën en bronkritiek, maar miste
de diepere infrastructuurlagen die invloed operationeel maken:

- Geldstromen
- Personele draaideuren
- Events en reizen
- Article-level provenance
- Parlementaire transmissieketens
- Meetbare outcomes

v4 voegt deze lagen toe als aparte tabellen, niet als extra kolommen in één platte graaf.

## Kernprincipe: edge-events

Waar v3 een edge `NGO_MONITOR -> TELEGRAAF (FRAME_SUPPLY)` had, vereist v4
splitsing in concrete events:

```
NGO_MONITOR_REPORT_2025 -> TELEGRAAF_ARTICLE_2026_XX
TELEGRAAF_ARTICLE_2026_XX -> PQ_RAJKOWSKI_NGO_2026
PQ_RAJKOWSKI_NGO_2026 -> GOV_RESPONSE_NGO_2026
```

Dit transformeert de graaf van een meningenkaart naar een causal-provenance graph.

## Nieuwe node typen

| node_type | voorbeelden |
|-----------|-------------|
| ADVOCACY_ORG | CIDI, Likoed Nederland |
| TRANSNATIONAL_HUB | IAF, ELNET, ECI |
| WATCHDOG_ORG | NGO Monitor |
| PR_FIRM | Castro |
| COUNTER_ACTOR | ELSC, TRF, NPK, New Neighbours |
| STATE_ACTOR | DUTCH_GOV, TWEEDE_KAMER, MSA_ISRAEL |
| MEDIA_OUTLET | TELEGRAAF, NOS, NIW, JONET, JOODS_NL |
| POLITICAL_PARTY | SGP, VVD, PVV, BBB, CU |
| POLITICIAN | CHRIS_STOFFER, QUEENY_RAJKOWSKI |
| JOURNALIST | WIERD_DUK, LEON_DE_WINTER, ESTHER_VOET |
| PUBLIC_FIGURE | NAOMI_MESTRUM, FRITS_HUFFNAGEL, QUEEN_MAXIMA |
| NGO | OXFAM_NOVIB, UAWC, AL_MEZAN |
| EDUCATION_ACTOR | HU, THIEMEMEULENHOFF, NOORDHOFF |
| SOCIAL_MEDIA | CESTMOCRO |
| RELIGIOUS_NETWORK | CVI |
| INTERNATIONAL_ORG | UNRWA |

## Nieuwe edge typen

| edge_type | functie | voorbeeld |
|-----------|---------|----------|
| AUTHORED_BY | artikel/rapport gemaakt door | ART_NIW_CIDI_DATA_2025 -> BART_VAN_DIJK |
| CITES_SOURCE | bronvermelding | ART_NOS_CESTMOCRO_2023 -> CIDI |
| REPLICATES_FRAME | inhoudelijke frame-overname | JOODS_NL -> AL_MEZAN (TERROR_LINK) |
| TEXTUAL_OVERLAP | meetbare tekstoverlap | [nog toe te voegen] |
| PUBLISHED_AFTER | temporele volgorde | PQ_RAJKOWSKI_NGO_2026 -> GOV_RESPONSE_NGO_2026 |
| TRIGGERED_BY | causale volgorde | GOV_NGOMONITOR_UITSTEL_2025 -> PQ_RAJKOWSKI_NGO_2026 |
| FUNDED_BY | geldstroom | DUTCH_GOV -> OXFAM_NOVIB |
| HOSTED_BY | event georganiseerd | HU -> CIDI (EVENT_COLLABORATION) |
| ATTENDED_BY | aanwezig bij event | EV_ELNET_MISSION_2024 -> CHRIS_STOFFER |
| SPONSORED_BY | reis/event betaald | FUND_ELNET_MISSION -> CHRIS_STOFFER |
| PRESSURED_TARGET | institutionele druk | CIDI -> DUTCH_GOV |
| RESULTED_IN | zichtbaar effect | OUTC_HU_POSTPONEMENT_2024 -> EV_HU_CIDI_LECTURES_2024 |
| DENIED_BY | officiele ontkenning | DUTCH_GOV -> NGO_MONITOR (OFFICIAL_NONCONFIRMATION) |
| CONFIRMED_BY | onafhankelijke bevestiging | [nog in te vullen] |
| OFFICIAL_NONCONFIRMATION | institutionele positie | DUTCH_GOV -> NGO_MONITOR (kabinet weerlegt niet) |

## Roltypologie

Niet iedereen is "lobby". Personen krijgen een rol op basis van functie:

| rol | betekenis | voorbeeld |
|-----|-----------|-----------|
| ORIGINATOR | produceert claim/frame | NGO_MONITOR |
| AMPLIFIER | verspreidt claim/frame | TELEGRAAF, JOODS_NL |
| TRANSMITTER | brengt naar politiek/media/institutie | VVD, PVV |
| GATEKEEPER | beslist over subsidie, event, publicatie | DUTCH_GOV |
| PRESSURE_ACTOR | zet publieke/juridische/politieke druk | CIDI, BBB |
| TARGET | wordt aangevallen/framed/onder druk gezet | AL_MEZAN, UAWC, TRF |
| COUNTER_ACTOR | documenteert, weerlegt, verzet zich | ELSC, TRF |
| BROKER | verbindt netwerken | ESTHER_VOET |
| FUNDER | financiert actor/event/campagne | ELNET, CVI |
| HOST | organiseert event/panel/reis | HU, CVI |

## Tiers

Om overzicht te bewaren bij een groeiende dataset:

| Tier | Type actor | Opnamecriterium |
|------|-----------|-----------------|
| T0 | Kernhubs | Formele lobby/advocacy rol |
| T1 | Structurele brokers | Herhaalde verbinding tussen lobby, media en politiek |
| T2 | Institutionele transmitters | Kamervragen, moties, beleidsinterventies, reizen |
| T3 | Media amplifiers | Herhaalde publicatie of framing |
| T4 | Episodische amplifiers | Losse publieke interventie |
| T5 | Ambient supporters | Sympathie/mening, geen netwerkwaarde (niet opgenomen) |

## Gebruik van tiers in visualisatie

- T0–T1: Kerngraaf voor lobby-infrastructuur
- T0–T3: Volledige invloedsgraaf
- T4: Per case toevoegen
- T5: Niet opnemen

## Kernvraag per case

Voor elke case in cases.csv wordt gevraagd:

1. Wie produceerde de claim?
2. Wie versterkte de claim?
3. Wie bracht hem institutioneel binnen?
4. Welke actor had toegang tot besluitvorming?
5. Welke materiele of reputatie-impact volgde?
6. Is de inhoud onafhankelijk vastgesteld?

## Epistemische positie: overheid is geen waarheidsanker

Een kernpunt van kritiek op v3 was dat de Nederlandse regering impliciet als
waarheidsanker werd gebruikt — ook al stond er `institutional_position_not_truth_anchor`
bij. **Die correctie was onvoldoende.** De overheid is geen neutrale arbiter.

### Waarom overheidshandelingen geen weerlegging zijn

1. **Institutioneel eigenbelang**: De Nederlandse overheid is donor en beleidsverantwoordelijke voor dezelfde NGO's waarover NGO Monitor aantijgingen doet. Een non-confirmation kan politieke bescherming van donorrelaties en coalitiebelangen zijn, geen objectieve waarheidsvinding.

2. **Actieve non-transparantie**: Het feit dat een kabinet zegt "geen informatie te hebben" betekent niet dat die informatie niet bestaat. Het kan betekenen: niet gezocht, niet gevonden willen hebben, of politiek niet opportuun om te delen.

3. **Politiek gemotiveerd standpunt**: Een regeringsstandpunt over een betwiste kwestie is een politieke handeling, geen onafhankelijk onderzoek. Zeker in een dossier waar de overheid zelf (mede)financier en beleidsverantwoordelijke is.

### Regel voor v4

- Alle overheidsreacties krijgen `epistemic_role = political_position_not_investigation`.
- Alle overheidsreacties krijgen `risk_flags = institutional_self_interest;potential_non_transparency`.
- Non-confirmation door de overheid **weerlegt de aantijging niet**. Het bewijst alleen dat de overheid ervoor kiest (of gedwongen is) publiekelijk niet te bevestigen.
- Zelfs due-diligence beweringen zijn `political_position_not_investigation`: de overheid beoordeelt haar eigen processen — inherent belangenconflict.

## Analytisch onderscheid: Israëlisch / pro-Israël / zionistisch / christelijk-zionistisch

Deze categorieën worden **niet** samengevoegd in één "lobby"-label. Het overlap, maar
analytisch moeten ze gescheiden blijven om ideologische mistwolken te voorkomen.

| Categorie | Betekenis | Voorbeelden in dataset |
|-----------|-----------|----------------------|
| Israëlische staatsinvloed | Direct of indirect verbonden aan Israëlische staat, diplomatie, regeringsbeleid, public diplomacy | MSA_ISRAEL (`STATE_ACTOR/israeli_state_public_diplomacy`) |
| Pro-Israël advocacy | Verdedigt Israëlisch beleid of belangen, niet noodzakelijk staatsaangestuurd | CIDI, Likoed Nederland, ELNET (`ADVOCACY_ORG/pro_israel_advocacy`) |
| Zionistische ideologische netwerken | Ideologisch gemotiveerde steun voor zionisme/Joodse nationale zelfbeschikking, breder dan de staat Israël | IAF, IAF_EU, ECI (`TRANSNATIONAL_HUB/zionist_ideological_*`) |
| Christelijk-zionisme | Religieus-theologische steun aan Israël, sterk in SGP/CU-kringen | CVI (`RELIGIOUS_NETWORK/christian_zionist`) |
| Media-/opinie-amplificatie | Verspreidt, versterkt of normaliseert frames zonder formele lobbyrol | Journalisten, columnisten, talkshows (`AMPLIFIER` rol) |
| Politieke transmissie | Brengt frames binnen in parlement, moties, Kamervragen | Politici als `TRANSMITTER` of `QUESTION_ACTOR` |

### Regel

`sub_type` in actors.csv geeft deze categorisering. Geen actor krijgt automatisch
`actor_type = ADVOCACY_ORG` omdat hij/zij pro-Israël is. Een journalist is `JOURNALIST`
met `role = amplifier`, een politicus is `POLITICIAN` met `role = transmitter`.

## BN'ers en influencers: standaard AMPLIFIER, niet LOBBY_ACTOR

BN'ers en publieke figuren worden **niet** als lobbyactoren gelabeld tenzij er
bewijs is van:

- Formele rol bij lobbyorganisatie
- Betaalde campagnefunctie of consultancy
- Aantoonbare coördinatie met campagneplanning
- Herhaalde, gestructureerde frame-replicatie

Standaardrol is `amplifier` of `commentator`. Dit voorkomt dat iemands publieke
mening automatisch als lobbyactiviteit wordt geregistreerd.

## Analyse-lagen (gescheiden grafen)

| Graph | Doel |
|-------|------|
| G1_actor_network | Wie is verbonden met wie |
| G2_claim_transmission | Hoe frames reizen |
| G3_institutional_access | Hoe lobby toegang krijgt tot politiek/beleid |
| G4_pressure_outcomes | Welke campagnes effect hebben |
| G5_money_events_travel | Geld, reizen, conferenties, informele invloed |

## Data kwaliteitsindicatoren

- `confidence`: vertrouwen dat de publieke relatie/handeling bestaat
- `primary_source_independent`: edge blijft overeind zonder ELSC/TRF (kolom in edges.csv)
- `risk_flags`: defamation_sensitive, contested_claim, media_generalization, speech_restriction
- `adjudication_status`: not_adjudicated, unadjudicated_contested, independently_confirmed
- `epistemic_role`: evidence_of_public_relation, institutional_position_not_truth_anchor, allegation_origin, etc.

## v4 tov v3

| Aspect | v3 | v4 |
|--------|----|----|
| Node structuur | 1 tabel (nodes.csv) | 10 tabellen (actors, claims, articles, parliamentary_items, events, travel, funding, legal_actions, outcomes, cases) |
| Abstracte concepten | nodes met entity_kind=concept | claims.csv met eigenschappen |
| Edges | alleen actor->actor | multi-type: actor, article, parliamentary_item, claim, event, funding, legal_action, outcome |
| Roltypologie | actor_class | actor_type + tier + role |
| Transmissieketens | impliciet in edge_label | expliciet via case_id + article/parliamentary edges |
| Geld/reizen | niet gemodelleerd | aparte tabellen (funding.csv, travel.csv) |
| Outcomes | niet gemodelleerd | aparte tabel (outcomes.csv) + RESULTED_IN edges |
| Bronkritiek | sources.csv met reliability_note | sources.csv + `primary_source_independent` in edges |
