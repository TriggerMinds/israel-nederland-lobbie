# v5 — claim-level provenance graph

## Overzicht

v5 is een multi-layer directed graph die inzet, transmissie en institutionele impact
van pro-Israël advocacy in Nederland modelleert. Het netwerk bestaat uit 166 nodes
en 118 edges over 12 laagtypen: actoren, claims, artikelen, parlementaire items,
events, reizen, financiering, juridische acties, outcomes, cases, bronnen en edges.

Het datamodel scheidt entity type (actor, claim, artikel, etc.) van het domein (lobby,
media, politiek, juridisch, financieel), zodat je per analysevraag de relevante laag
kunt isoleren of combineren.

## Niveaus

Het netwerk kent 5 analytische niveaus, van grof naar fijn:

1. **Netwerkstructuur** (`actors.csv`, `edges.csv`) — wie is verbonden met wie,
   welke rollen en tiers, wat is de dichtheid en centraliteit van hubs als CIDI, IAF,
   SGP, Telegraaf, NGO Monitor.

2. **Transmissieketens** (`cases.csv`, `article_claim_links.csv`,
   `parliamentary_claim_links.csv`) — welke claim reist via welke media-actoren naar
   welke parlementaire vragen, ministeriële reacties of beleidsuitkomsten.

3. **Temporele patronen** (`timeline_events.csv`) — timing van publicaties,
   Kamervragen, events en outcomes per case. Zichtbaar: publicatie → mediagolf →
   politieke reactie → outcome.

4. **Sociale en financiële laag** (`social_posts.csv`, `event_participants.csv`,
   `funding.csv`, `travel.csv`) — podiumgebruik, netwerkevenementen, gesponsorde
   reizen, personele draaideuren.

5. **Tekstuele laag** (`copy_overlap.csv`) — tekstoverlap tussen bronrapporten,
   media-artikelen en Kamervragen. Te vullen met difflib of alignment tools.

## Tabelstructuur (19 tabellen)

| Tabel | Nodes/Edges | Inhoud |
|-------|-------------|--------|
| actors.csv | 81 nodes | Organisaties, personen, media, partijen met type en tier |
| articles.csv | 23 nodes | Artikelen, rapporten, podcasts met publisher en datum |
| claims.csv | 15 nodes | Retorische strategieën, frames, aantijgingen met type en status |
| parliamentary_items.csv | 11 nodes | Kamervragen, moties, reisregistraties met actor en datum |
| events.csv | 7 nodes | Panels, lezingen, conferenties, podcasts |
| travel.csv | 2 nodes | Israël-reizen met reiziger, organizer en jaar |
| funding.csv | 7 nodes | Subsidies, donaties, reisbekostiging |
| legal_actions.csv | 2 nodes | Aangiftes, klachten, sommaties |
| outcomes.csv | 8 nodes | Outcome events (annulering, Kamervraag, beleidseffect) |
| cases.csv | 10 nodes | Casusdefinities met claim-herkomst, transmissie en outcome |
| edges.csv | 118 edges | Alle relaties tussen nodes uit alle lagen |
| sources.csv | 38 nodes | Bronregister met URLs |
| article_claim_links.csv | 14 edges | Koppelt artikelen aan claims |
| parliamentary_claim_links.csv | 8 edges | Koppelt Kamervragen aan claims |
| timeline_events.csv | 97 events | Chronologische gebeurtenissen per case |
| copy_overlap.csv | — | Structuur voor tekstoverlapmeting |
| social_posts.csv | 5 posts | Publieke uitingen (X, Instagram, media-statements) |
| event_participants.csv | 12 deelnemers | Wie deed mee aan welk event |
| organization_people_roles.csv | 10 relaties | Personele verbanden (founder, editor, employee, oud-medewerker) |

## Analysevolgorde

1. Begin bij `cases.csv`: elke case is een claim-transmissie-impact keten.
2. Traceer via `article_claim_links.csv` en `parliamentary_claim_links.csv`
   welke media en politieke actoren de claim droegen.
3. Gebruik `timeline_events.csv` voor de volgorde: wie publiceerde wanneer,
   wie reageerde wanneer, wat was de uitkomst.
4. Voeg `organization_people_roles.csv` toe om draaideurconstructie zichtbaar
   te maken — welke personen zitten in zowel media als advocacy organen.
5. `social_posts.csv` + `event_participants.csv` geven de informele
   netwerklaag: wie deelt een podium, wie reist samen, wie versterkt wie.

## Tier-classificatie voor actoren

| Tier | Type | Voorbeelden |
|------|------|-------------|
| T0 | Kernhubs — formele lobby/advocacy rol | CIDI, IAF, SGP, NGO Monitor |
| T1 | Structurele brokers — herhaalde verbinding lobby-media-politiek | CVI, ELNET, TRF, Telegraaf, ELSC |
| T2 | Institutionele transmitters — Kamervragen, moties, reizen | Dilan Yesilgöz, Chris Stoffer, PVV-Kamerleden |
| T3 | Media amplifiers — publicatie of framing | GeenStijl, Wierd Duk, Leon de Winter |
| T4 | Episodische amplifiers — losse publieke interventie | Koningin Máxima |
| T5 | Context nodes — verwijzingen en clusters | DUTCH_MEDIA_CLUSTER |

## Roltypologie per actor

| Rol | Betekenis | Voorbeeld |
|-----|-----------|-----------|
| ORIGINATOR | Produceert claim/frame | NGO Monitor, CIDI |
| AMPLIFIER | Verspreidt claim/frame via media/publiek | Telegraaf, GeenStijl |
| TRANSMITTER | Brengt claim naar politiek/institutie | VVD, PVV, BBB |
| GATEKEEPER | Beslist over subsidie, event, publicatie | DUTCH_GOV |
| PRESSURE_ACTOR | Zet publieke/juridische/politieke druk | CIDI, BBB |
| TARGET | Wordt aangevallen of onder druk gezet | AL_MEZAN, UAWC, HU |
| COUNTER_ACTOR | Documenteert, weerlegt, verzet zich | ELSC, TRF |
| BROKER | Verbindt netwerken (persoonlijk) | Esther Voet (CIDI → NIW) |
| FUNDER | Financiert actor/event/campagne | ELNET, CVI, DUTCH_GOV |
| HOST | Organiseert event/panel/reis | HU, CVI, IAF |

## De vragen die de graaf beantwoordt

1. **Wie produceert een claim?** → `claims.originator_actor_id` + `edges[source_type=claim]`
2. **Wie versterkt de claim?** → `article_claim_links` + `edges[edge_type=MEDIA_AMPLIFICATION]`
3. **Wie brengt hem institutioneel binnen?** → `parliamentary_claim_links` + `edges[edge_type=PARLIAMENTARY_QUESTION]`
4. **Welke actoren hebben toegang tot besluitvorming?** → tier T0–T1 actoren met edges naar DUTCH_GOV of TWEEDE_KAMER
5. **Welke impact volgt?** → `outcomes` + `edges[edge_type=RESULTED_IN]`
6. **Wat is de timing?** → `timeline_events` gesorteerd op datum

## Dataformaat

Alle tabellen zijn UTF-8 CSV met `QUOTE_MINIMAL`. Datumformaat: YYYY of YYYY-MM-DD.
Bronverwijzingen in `source_ids` kolommen zijn `;`-gescheiden ID's die verwijzen naar `sources.csv`.
