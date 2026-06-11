MERGE dbo.zachman_perspectives AS target
USING (VALUES
  (N'Row1_Planner', 1, N'Planner / Scope'),
  (N'Row2_Owner', 2, N'Owner / Business Model'),
  (N'Row3_Designer', 3, N'Designer / System Model'),
  (N'Row4_Builder', 4, N'Builder / Technology Model'),
  (N'Row5_Implementer', 5, N'Implementer / Detailed Representations'),
  (N'Row6_Operator', 6, N'Operator / Functioning Enterprise')
) AS source(perspective, perspective_order, label)
ON target.perspective = source.perspective
WHEN NOT MATCHED THEN
  INSERT (perspective, perspective_order, label)
  VALUES (source.perspective, source.perspective_order, source.label);
GO

MERGE dbo.zachman_interrogatives AS target
USING (VALUES
  (N'What', 1, N'Data / Things'),
  (N'How', 2, N'Function / Process'),
  (N'Where', 3, N'Network / Location'),
  (N'Who', 4, N'People / Identity'),
  (N'When', 5, N'Time / Events'),
  (N'Why', 6, N'Motivation / Intent')
) AS source(interrogative, interrogative_order, label)
ON target.interrogative = source.interrogative
WHEN NOT MATCHED THEN
  INSERT (interrogative, interrogative_order, label)
  VALUES (source.interrogative, source.interrogative_order, source.label);
GO

MERGE dbo.zt_pillars AS target
USING (VALUES
  (N'Identity', N'Identity'),
  (N'Device', N'Device'),
  (N'Network', N'Network'),
  (N'Application', N'Application'),
  (N'Data', N'Data')
) AS source(zt_pillar, label)
ON target.zt_pillar = source.zt_pillar
WHEN NOT MATCHED THEN
  INSERT (zt_pillar, label)
  VALUES (source.zt_pillar, source.label);
GO

MERGE dbo.assets AS target
USING (VALUES
  (N'asset:crm-app', N'CRM Application', N'Application', N'Confidential', N'Primary customer relationship management app in protect surface.'),
  (N'asset:customer-pii', N'Customer PII Dataset', N'DataStore', N'Restricted', N'Protected dataset containing customer personally identifiable information.')
) AS source(asset_id, asset_name, asset_type, sensitivity, description)
ON target.asset_id = source.asset_id
WHEN NOT MATCHED THEN
  INSERT (asset_id, asset_name, asset_type, sensitivity, description)
  VALUES (source.asset_id, source.asset_name, source.asset_type, source.sensitivity, source.description);
GO

MERGE dbo.identities AS target
USING (VALUES
  (N'id:sales-rep', N'Sales Representative (role)', N'Human', N'AAL2', N'Business user role accessing CRM and customer records.'),
  (N'id:crm-service', N'CRM Service Account', N'Workload', N'AAL3', N'Non-human identity used by CRM workloads for backend calls.')
) AS source(identity_id, identity_name, identity_type, assurance_level, description)
ON target.identity_id = source.identity_id
WHEN NOT MATCHED THEN
  INSERT (identity_id, identity_name, identity_type, assurance_level, description)
  VALUES (source.identity_id, source.identity_name, source.identity_type, source.assurance_level, source.description);
GO

MERGE dbo.access_policies AS target
USING (VALUES
  (
    N'policy:ps:crm:pii:read',
    N'Read PII via CRM (ZT)',
    N'Allow read access to customer PII only via approved CRM path with strong authentication, device posture, and least privilege.',
    N'ALLOW',
    N'{"requirements":{"authn":"mfa","device_posture":"compliant","network":"approved","risk":"low"},"constraints":{"time_window":"business_hours","geo":"allowed_regions"}}',
    N'API Gateway'
  ),
  (
    N'policy:ps:crm:pii:deny-direct',
    N'Deny direct PII access (ZT)',
    N'Deny direct access to the PII datastore except via explicitly authorized services and paths.',
    N'DENY',
    N'{"reason":"protect_surface","enforcement":"default_deny"}',
    N'DB Proxy'
  )
) AS source(policy_id, policy_name, description, effect, conditions_json, enforcement_point)
ON target.policy_id = source.policy_id
WHEN NOT MATCHED THEN
  INSERT (policy_id, policy_name, description, effect, conditions_json, enforcement_point)
  VALUES (source.policy_id, source.policy_name, source.description, source.effect, source.conditions_json, source.enforcement_point);
GO

MERGE dbo.policy_assets AS target
USING (VALUES
  (N'policy:ps:crm:pii:read', N'asset:customer-pii'),
  (N'policy:ps:crm:pii:read', N'asset:crm-app'),
  (N'policy:ps:crm:pii:deny-direct', N'asset:customer-pii')
) AS source(policy_id, asset_id)
ON target.policy_id = source.policy_id AND target.asset_id = source.asset_id
WHEN NOT MATCHED THEN
  INSERT (policy_id, asset_id)
  VALUES (source.policy_id, source.asset_id);
GO

MERGE dbo.policy_identities AS target
USING (VALUES
  (N'policy:ps:crm:pii:read', N'id:sales-rep'),
  (N'policy:ps:crm:pii:read', N'id:crm-service')
) AS source(policy_id, identity_id)
ON target.policy_id = source.policy_id AND target.identity_id = source.identity_id
WHEN NOT MATCHED THEN
  INSERT (policy_id, identity_id)
  VALUES (source.policy_id, source.identity_id);
GO

MERGE dbo.zachman_cells AS target
USING (VALUES
  (N'Row1_Planner', N'What', N'Data', N'ProtectSurfaceScope', N'Define the protect surface data scope: CRM customer records and PII dataset.'),
  (N'Row1_Planner', N'Who', N'Identity', N'IdentityScope', N'Define identity scope: sales reps (human) and CRM workloads (service/workload identities).'),
  (N'Row1_Planner', N'Where', N'Network', N'PathScope', N'Define approved access paths: user -> API gateway -> CRM -> DB proxy -> PII store.'),
  (N'Row1_Planner', N'How', N'Application', N'ControlObjectives', N'Define control objectives: least privilege, strong authn, continuous verification, encrypted channels.'),
  (N'Row1_Planner', N'When', N'Device', N'VerificationCadence', N'Define verification cadence: continuous session evaluation and device posture checks.'),
  (N'Row1_Planner', N'Why', N'Identity', N'ZeroTrustPrinciple', N'Never Trust, Always Verify; default deny; assume breach; explicit verification.'),
  (N'Row2_Owner', N'What', N'Data', N'BusinessDataDefinition', N'Business definition of protected data (PII) and ownership/stewardship expectations.'),
  (N'Row2_Owner', N'Who', N'Identity', N'RoleModel', N'Role model: sales rep role, CRM service role, and their responsibilities for handling customer data.'),
  (N'Row2_Owner', N'How', N'Application', N'BusinessProcess', N'Business process: view/update customer records through CRM with auditable actions.'),
  (N'Row2_Owner', N'Where', N'Network', N'BusinessLocations', N'Business locations/contexts allowed for access (regions, networks, remote access constraints).'),
  (N'Row2_Owner', N'When', N'Device', N'BusinessEvents', N'Business events that trigger re-verification (login, privilege elevation, risk change).'),
  (N'Row2_Owner', N'Why', N'Data', N'PolicyIntent', N'Policy intent: minimize exposure of PII and enable customer service while managing risk.')
) AS source(perspective, interrogative, zt_pillar, artifact_name, artifact_content)
ON target.perspective = source.perspective
   AND target.interrogative = source.interrogative
   AND target.zt_pillar = source.zt_pillar
   AND target.artifact_name = source.artifact_name
WHEN NOT MATCHED THEN
  INSERT (perspective, interrogative, zt_pillar, artifact_name, artifact_content)
  VALUES (source.perspective, source.interrogative, source.zt_pillar, source.artifact_name, source.artifact_content);
GO
