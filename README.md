# Israel-advocacy SNA NL dataset

Generated: 2026-06-12

Files:
- nodes.csv: node table for Gephi/Maltego/custom Python
- edges.csv: directed edge list
- sources.csv: source register
- israel_advocacy_sna_nl.graphml: direct GraphML import
- sna_dataset.json: full dataset

Interpretation rules:
1. This is an evidence-graded public-actor network, not a guilt-by-association map.
2. edge_type is the analytic unit. Do not collapse all edges into "lobby".
3. `confidence` describes confidence that the public relation/action exists, not agreement with the actor's substantive claim.
4. `evidence_status=contested_claim` means the claim is reported or used publicly but disputed or rejected by another source.
5. `risk_flags=defamation_sensitive` requires explicit wording that allegations are allegations and may have been rejected by government/counterparties.
6. Private persons are excluded. Public individuals are included only for public role, article, parliamentary action, public statement, travel registration, platforming, or organizational role.
7. For visualization: filter out abstract nodes first if you want actor-only topology. Keep abstract nodes if you want discourse/frame topology.

Recommended Gephi import:
- Import nodes.csv as nodes.
- Import edges.csv as edges.
- Use `weight` as edge weight.
- Partition by `actor_class` or `entity_kind`.
- Filter edges where `confidence` in [high, medium_high] for conservative view.
- Filter out `risk_flags=contested_claim` for strict verified-action view.


## v2 epistemische correctie

Naar aanleiding van methodologische kritiek is de dataset aangescherpt:

- Nederlandse regeringsreacties zijn niet langer als impliciete waarheidsankers gemodelleerd.
- Regeringsuitspraken rond NGO Monitor/Oxfam/DRA zijn hercodeerd als `OFFICIAL_NONCONFIRMATION` en `official_position`.
- Nieuwe edgevelden: `epistemic_role` en `adjudication_status`.
- `confidence` betekent: vertrouwen dat de publieke relatie/handeling bestaat, niet vertrouwen dat de inhoudelijke claim waar is.
- Institutionele bronnen, lobbybronnen, media en NGO-bronnen krijgen allemaal bronrolscheiding: actor-data ≠ waarheid-data.

Belangrijkste regel:
Een officiële bron bewijst dat een institutie iets zegt of doet. Niet dat het inhoudelijk waar is.


## v3 uitbreiding

Toegevoegd:
- rhetorical_strategies.csv
- claims_to_verify.csv
- Joods.nl-node
- MSA/Israeli Ministry of Strategic Affairs als transnationale contextnode
- European Coalition for Israel als EU-lobbynode
- CIDI media-presence edge op basis van Activiteitenoverzicht 2024
- Jan Tervoort / The Rights Forum karaktermoordcase
- Al Mezan-route: NGO Monitor -> Joods.nl/De Telegraaf -> PVV/Kamervragen -> CIDI-publicatie volgens ELSC
- UAWC/defunding-route als contested claim-transmission layer

Belangrijk:
v3 maakt retorische tactieken zichtbaar zonder ze automatisch als bewijs van coördinatie te behandelen.
