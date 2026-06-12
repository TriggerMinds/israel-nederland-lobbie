# Epistemische correctie v2

Deze dataset gebruikt géén enkele actor als waarheidsanker.

## Kernregel

Een bron bewijst primair dat een publieke handeling, claim, publicatie, reis, klacht, Kamervraag of institutionele reactie heeft plaatsgevonden.

Een bron bewijst niet automatisch dat de inhoudelijke claim waar is.

## Correctie op regeringsbronnen

Officiële Nederlandse regeringsreacties worden behandeld als:

- `OFFICIAL_NONCONFIRMATION`
- `official_position`
- `institutional_position_not_truth_anchor`

Niet als:

- onafhankelijke waarheidsvinding
- objectieve weerlegging
- bewijs dat NGO Monitor ongelijk heeft
- bewijs dat Oxfam/DRA vrij zijn van elk probleem

## Correcte interpretatie

Voorbeeld NGO Monitor -> Oxfam/DRA:

1. NGO Monitor brengt of voedt een aantijging.
2. De aantijging wordt via media/parlementaire vragen het Nederlandse beleidsveld binnengebracht.
3. De Nederlandse regering zegt publiekelijk dat zij geen ondersteunende informatie heeft of vertrouwen heeft in haar procedures.
4. Dat is een institutionele positie, geen onafhankelijke adjudicatie.

## Analyse-implicatie

Gebruik minimaal drie gescheiden lagen:

1. Claim-origin layer: wie produceert de aantijging?
2. Transmission layer: wie versterkt of verplaatst de aantijging naar media/politiek?
3. Adjudication layer: wie onderzoekt, bevestigt, ontkent of ontwijkt de aantijging?

Alleen laag 3 kan inhoudelijke validiteit benaderen, en dan alleen bij onafhankelijke, controleerbare audit, rechterlijke uitspraak, openbaar bewijsdossier of reproduceerbare primaire documentatie.

## Praktische filter

Voor strikte analyse:
- gebruik `epistemic_role`
- gebruik `adjudication_status`
- behandel `official_position` als actor-data, niet als waarheid-data


## v3 toevoeging: retorische strategieën als aparte laag

De v3-dataset maakt onderscheid tussen:

1. Actoren
2. Transmissieroutes
3. Retorische strategieën
4. Institutionele reacties
5. Impactmechanismen

Hierdoor worden personen, media en partijen niet automatisch als 'lobby' gelabeld. Zij kunnen verschillende rollen hebben:
- bron
- amplifier
- beleidsinvoer
- commentator
- target
- institutionele actor
- counter-documentation actor

Voor claims zoals 'media controle' gebruikt v3 strengere taal:
- media visibility
- frame supply
- media amplification
- source dependency
- campaign reproduction

Alleen met direct redactioneel bewijs wordt 'control' als edge toegestaan.
