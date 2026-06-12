# v2 data integration

v5 is the consolidated single source of truth. It includes all data from:
- v2 (actor-network graph): 88 nodes, 103 edges, 38 sources
- v4 (multi-layer influence graph): 12 tables, 111 edges, 79 actors
- v5 (claim-level provenance expansion): 7 new tables

## v2 content absorbed into v5

| v2 file | rows | v5 disposition |
|---------|------|----------------|
| nodes.csv | 88 | 79 in actors.csv, 9 abstract → claims.csv, 3 context nodes added |
| edges.csv | 103 | 85 → edges.csv, 18 abstract-concept edges not carried over |
| sources.csv | 38 | all → sources.csv |
| rhetorical_strategies.csv | 7 | → claims.csv (claim_type = rhetorical_strategy) |
| claims_to_verify.csv | 5 | → claims.csv notes field |

## Not carried over from v2
- 18 edges referencing abstract concept nodes (ANTIZIONISM_FRAME, CHILLING_EFFECT, etc.)
  These concepts now exist as claims with claim_id values (C1, C2, etc.)
- DUTCH_FOREIGN_POLICY_CONTEXT — context-only node, no edges reference it
