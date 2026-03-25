-- DuckDB schema for the Zero Trust × Zachman Matrix.
-- Designed to store 36 cells (6 perspectives × 6 interrogatives)
-- and link each cell to Zero Trust artifacts in a modular, rule-based way.

BEGIN TRANSACTION;

-- -----------------------------
-- Core reference tables
-- -----------------------------

CREATE TABLE IF NOT EXISTS zachman_perspectives (
  perspective TEXT PRIMARY KEY,              -- e.g., 'Row1_Planner', 'Row2_Owner', ...
  perspective_order INTEGER NOT NULL,        -- 1..6
  label TEXT NOT NULL                        -- human-friendly label
);

CREATE TABLE IF NOT EXISTS zachman_interrogatives (
  interrogative TEXT PRIMARY KEY,            -- 'What','How','Where','Who','When','Why'
  interrogative_order INTEGER NOT NULL,      -- 1..6
  label TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS zt_pillars (
  zt_pillar TEXT PRIMARY KEY,                -- 'Identity','Device','Network','Application','Data'
  label TEXT NOT NULL
);

-- -----------------------------
-- Zachman cells (artifacts live here)
-- -----------------------------

CREATE TABLE IF NOT EXISTS zachman_cells (
  perspective TEXT NOT NULL,
  interrogative TEXT NOT NULL,
  zt_pillar TEXT NOT NULL,
  artifact_name TEXT NOT NULL,
  artifact_content TEXT,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (perspective, interrogative, zt_pillar, artifact_name),

  FOREIGN KEY (perspective) REFERENCES zachman_perspectives(perspective),
  FOREIGN KEY (interrogative) REFERENCES zachman_interrogatives(interrogative),
  FOREIGN KEY (zt_pillar) REFERENCES zt_pillars(zt_pillar)
);

-- -----------------------------
-- Supporting tables (protect surface primitives)
-- -----------------------------

CREATE TABLE IF NOT EXISTS assets (
  asset_id TEXT PRIMARY KEY,                 -- stable identifier (e.g., 'asset:crm')
  asset_name TEXT NOT NULL,
  asset_type TEXT NOT NULL,                  -- e.g., 'Application','DataStore','Service'
  sensitivity TEXT,                          -- e.g., 'Public','Internal','Confidential','Restricted'
  description TEXT
);

CREATE TABLE IF NOT EXISTS identities (
  identity_id TEXT PRIMARY KEY,              -- stable identifier (e.g., 'id:alice')
  identity_name TEXT NOT NULL,
  identity_type TEXT NOT NULL,               -- 'Human','Service','Workload','Device'
  assurance_level TEXT,                      -- e.g., 'IAL2/AAL2' (free-form for now)
  description TEXT
);

CREATE TABLE IF NOT EXISTS access_policies (
  policy_id TEXT PRIMARY KEY,                -- stable identifier (e.g., 'policy:ps:crm:read')
  policy_name TEXT NOT NULL,
  description TEXT,
  effect TEXT NOT NULL CHECK (effect IN ('ALLOW','DENY')),
  conditions_json TEXT,                      -- JSON string; keep flexible and validate at app layer
  enforcement_point TEXT                      -- e.g., 'API Gateway', 'DB Proxy'
);

-- Join tables to keep policies modular and rule-based.
CREATE TABLE IF NOT EXISTS policy_assets (
  policy_id TEXT NOT NULL,
  asset_id TEXT NOT NULL,
  PRIMARY KEY (policy_id, asset_id),
  FOREIGN KEY (policy_id) REFERENCES access_policies(policy_id),
  FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS policy_identities (
  policy_id TEXT NOT NULL,
  identity_id TEXT NOT NULL,
  PRIMARY KEY (policy_id, identity_id),
  FOREIGN KEY (policy_id) REFERENCES access_policies(policy_id),
  FOREIGN KEY (identity_id) REFERENCES identities(identity_id)
);

COMMIT;

