# v5 — capture-aware influence provenance graph

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
