-- Seed metadata for Row 1 (Planner) and Row 2 (Owner) perspectives
-- of a Zero Trust protect surface.

BEGIN TRANSACTION;

-- Reference data
INSERT OR IGNORE INTO zachman_perspectives(perspective, perspective_order, label) VALUES
  ('Row1_Planner', 1, 'Planner / Scope'),
  ('Row2_Owner',   2, 'Owner / Business Model');

INSERT OR IGNORE INTO zachman_interrogatives(interrogative, interrogative_order, label) VALUES
  ('What',  1, 'Data / Things'),
  ('How',   2, 'Function / Process'),
  ('Where', 3, 'Network / Location'),
  ('Who',   4, 'People / Identity'),
  ('When',  5, 'Time / Events'),
  ('Why',   6, 'Motivation / Intent');

INSERT OR IGNORE INTO zt_pillars(zt_pillar, label) VALUES
  ('Identity', 'Identity'),
  ('Device', 'Device'),
  ('Network', 'Network'),
  ('Application', 'Application'),
  ('Data', 'Data');

-- Protect surface starter set (intentionally small, extensible)
INSERT OR IGNORE INTO assets(asset_id, asset_name, asset_type, sensitivity, description) VALUES
  ('asset:crm-app', 'CRM Application', 'Application', 'Confidential', 'Primary customer relationship management app in protect surface.'),
  ('asset:customer-pii', 'Customer PII Dataset', 'DataStore', 'Restricted', 'Protected dataset containing customer personally identifiable information.');

INSERT OR IGNORE INTO identities(identity_id, identity_name, identity_type, assurance_level, description) VALUES
  ('id:sales-rep', 'Sales Representative (role)', 'Human', 'AAL2', 'Business user role accessing CRM and customer records.'),
  ('id:crm-service', 'CRM Service Account', 'Workload', 'AAL3', 'Non-human identity used by CRM workloads for backend calls.');

INSERT OR IGNORE INTO access_policies(policy_id, policy_name, description, effect, conditions_json, enforcement_point) VALUES
  (
    'policy:ps:crm:pii:read',
    'Read PII via CRM (ZT)',
    'Allow read access to customer PII only via approved CRM path with strong authentication, device posture, and least privilege.',
    'ALLOW',
    '{"requirements":{"authn":"mfa","device_posture":"compliant","network":"approved","risk":"low"},"constraints":{"time_window":"business_hours","geo":"allowed_regions"}}',
    'API Gateway'
  ),
  (
    'policy:ps:crm:pii:deny-direct',
    'Deny direct PII access (ZT)',
    'Deny direct access to the PII datastore except via explicitly authorized services and paths.',
    'DENY',
    '{"reason":"protect_surface","enforcement":"default_deny"}',
    'DB Proxy'
  );

INSERT OR IGNORE INTO policy_assets(policy_id, asset_id) VALUES
  ('policy:ps:crm:pii:read', 'asset:customer-pii'),
  ('policy:ps:crm:pii:read', 'asset:crm-app'),
  ('policy:ps:crm:pii:deny-direct', 'asset:customer-pii');

INSERT OR IGNORE INTO policy_identities(policy_id, identity_id) VALUES
  ('policy:ps:crm:pii:read', 'id:sales-rep'),
  ('policy:ps:crm:pii:read', 'id:crm-service');

-- Row 1 (Planner): define the scope primitives (rule-based placeholders)
INSERT OR IGNORE INTO zachman_cells(perspective, interrogative, zt_pillar, artifact_name, artifact_content) VALUES
  ('Row1_Planner','What','Data','ProtectSurfaceScope','Define the protect surface data scope: CRM customer records and PII dataset.'),
  ('Row1_Planner','Who','Identity','IdentityScope','Define identity scope: sales reps (human) and CRM workloads (service/workload identities).'),
  ('Row1_Planner','Where','Network','PathScope','Define approved access paths: user -> API gateway -> CRM -> DB proxy -> PII store.'),
  ('Row1_Planner','How','Application','ControlObjectives','Define control objectives: least privilege, strong authn, continuous verification, encrypted channels.'),
  ('Row1_Planner','When','Device','VerificationCadence','Define verification cadence: continuous session evaluation and device posture checks.'),
  ('Row1_Planner','Why','Identity','ZeroTrustPrinciple','Never Trust, Always Verify; default deny; assume breach; explicit verification.');

-- Row 2 (Owner): business model and governance artifacts for protect surface
INSERT OR IGNORE INTO zachman_cells(perspective, interrogative, zt_pillar, artifact_name, artifact_content) VALUES
  ('Row2_Owner','What','Data','BusinessDataDefinition','Business definition of protected data (PII) and ownership/stewardship expectations.'),
  ('Row2_Owner','Who','Identity','RoleModel','Role model: sales rep role, CRM service role, and their responsibilities for handling customer data.'),
  ('Row2_Owner','How','Application','BusinessProcess','Business process: view/update customer records through CRM with auditable actions.'),
  ('Row2_Owner','Where','Network','BusinessLocations','Business locations/contexts allowed for access (regions, networks, remote access constraints).'),
  ('Row2_Owner','When','Device','BusinessEvents','Business events that trigger re-verification (login, privilege elevation, risk change).'),
  ('Row2_Owner','Why','Data','PolicyIntent','Policy intent: minimize exposure of PII and enable customer service while managing risk.');

COMMIT;

