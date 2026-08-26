CREATE TABLE IF NOT EXISTS node_versions (
  version_id varchar(64) PRIMARY KEY,
  node_id varchar(200) NOT NULL,
  valid_from timestamptz NOT NULL,
  valid_to timestamptz,
  transaction_time timestamptz NOT NULL,
  payload jsonb NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_nodes_visible
  ON node_versions (node_id, valid_from, transaction_time);

CREATE TABLE IF NOT EXISTS edge_versions (
  version_id varchar(64) PRIMARY KEY,
  edge_id varchar(200) NOT NULL,
  source varchar(200) NOT NULL,
  target varchar(200) NOT NULL,
  capacity double precision NOT NULL CHECK (capacity >= 0),
  valid_from timestamptz NOT NULL,
  valid_to timestamptz,
  transaction_time timestamptz NOT NULL,
  payload jsonb NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_edges_visible
  ON edge_versions (edge_id, valid_from, transaction_time);

CREATE TABLE IF NOT EXISTS scenario_runs (
  run_id varchar(64) PRIMARY KEY,
  scenario_id varchar(200) NOT NULL,
  created_at timestamptz NOT NULL,
  code_version varchar(80) NOT NULL,
  input_manifest_hash varchar(64) NOT NULL,
  request_payload jsonb NOT NULL,
  result_payload jsonb NOT NULL,
  notes text
);
CREATE INDEX IF NOT EXISTS ix_scenario_manifest
  ON scenario_runs (scenario_id, input_manifest_hash);
