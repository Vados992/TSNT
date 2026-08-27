# Data model

## Core records

| Record | Required identity | Time fields | Quantitative controls |
|---|---|---|---|
| NodeRecord | node_id, name, layer | valid_from, valid_to, transaction_time | optional bounded SNII components |
| EdgeRecord | edge_id, source, target, layer, commodity | same bitemporal fields | capacity, unit, cost, transit time |
| CapacityShock | target type/id | starts_at, ends_at | capacity factor in [0,1] |
| ScenarioContract | scenario_id | as_of, analysis_cutoff | horizon and random seed |
| ProvenanceRecord | provenance_id, URI, licence | effective/retrieval time | SHA-256 and lineage |
| ScenarioRun | run_id, scenario_id | creation time | code/input hashes and output JSON |

Unknown is represented by null or absence, never zero.

## Identity

- edge_id identifies one analytical edge version family;
- version_id hashes kind, identity and transaction time;
- canonical_flow_id identifies the underlying physical/economic flow and is used
  to prevent cross-table double counting;
- provenance_id binds a batch to a content hash and source licence.

Changing the meaning of an identifier requires a new identifier.

## Units

Values are stored with an explicit unit. The reference registry contains a small
reviewed set and refuses cross-dimensional conversion. Production systems should
use a controlled vocabulary based on official source metadata and add
commodity, currency basis, price basis, seasonal adjustment and denominator.

A valid conversion does not make unlike commodities additive.

## Evidence classes

primary, official, commercial, peer_reviewed, secondary, expert_judgment and
synthetic are controlled classes. Evidence class describes provenance, not
truth. Conflicting official sources remain separate versions until adjudicated.

## Provenance chain

A lineage step stores operation, code version, execution time and parameters.
The recommended manifest is:

~~~json
{
  "source_checksum": "sha256",
  "licence_id": "source-specific",
  "retrieved_at": "UTC timestamp",
  "effective_time": "UTC timestamp",
  "transformations": ["normalise-unit", "map-entity", "aggregate-window"],
  "schema_version": "1",
  "code_commit": "git SHA"
}
~~~

Raw licensed data should live outside Git. Store only permitted aggregates,
schemas, synthetic fixtures and hashes in this repository.

## Bitemporal corrections

Do not overwrite a historical row. Close its transaction-time version in the
persistence layer or append a corrected payload with a later transaction time.
A backtest using an earlier cutoff will continue seeing only the earlier
knowledge state.
