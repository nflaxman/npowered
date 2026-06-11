IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = N'dbo')
BEGIN
  EXEC(N'CREATE SCHEMA dbo');
END
GO

IF OBJECT_ID(N'dbo.zachman_perspectives', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.zachman_perspectives (
    perspective NVARCHAR(64) NOT NULL CONSTRAINT PK_zachman_perspectives PRIMARY KEY,
    perspective_order INT NOT NULL,
    label NVARCHAR(128) NOT NULL
  );
END
GO

IF OBJECT_ID(N'dbo.zachman_interrogatives', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.zachman_interrogatives (
    interrogative NVARCHAR(32) NOT NULL CONSTRAINT PK_zachman_interrogatives PRIMARY KEY,
    interrogative_order INT NOT NULL,
    label NVARCHAR(128) NOT NULL
  );
END
GO

IF OBJECT_ID(N'dbo.zt_pillars', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.zt_pillars (
    zt_pillar NVARCHAR(64) NOT NULL CONSTRAINT PK_zt_pillars PRIMARY KEY,
    label NVARCHAR(128) NOT NULL
  );
END
GO

IF OBJECT_ID(N'dbo.zachman_cells', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.zachman_cells (
    perspective NVARCHAR(64) NOT NULL,
    interrogative NVARCHAR(32) NOT NULL,
    zt_pillar NVARCHAR(64) NOT NULL,
    artifact_name NVARCHAR(256) NOT NULL,
    artifact_content NVARCHAR(MAX) NULL,
    created_at DATETIME2 NOT NULL CONSTRAINT DF_zachman_cells_created_at DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NOT NULL CONSTRAINT DF_zachman_cells_updated_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_zachman_cells PRIMARY KEY (perspective, interrogative, zt_pillar, artifact_name),
    CONSTRAINT FK_zachman_cells_perspective FOREIGN KEY (perspective) REFERENCES dbo.zachman_perspectives(perspective),
    CONSTRAINT FK_zachman_cells_interrogative FOREIGN KEY (interrogative) REFERENCES dbo.zachman_interrogatives(interrogative),
    CONSTRAINT FK_zachman_cells_zt_pillar FOREIGN KEY (zt_pillar) REFERENCES dbo.zt_pillars(zt_pillar)
  );
END
GO

IF OBJECT_ID(N'dbo.assets', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.assets (
    asset_id NVARCHAR(128) NOT NULL CONSTRAINT PK_assets PRIMARY KEY,
    asset_name NVARCHAR(256) NOT NULL,
    asset_type NVARCHAR(64) NOT NULL,
    sensitivity NVARCHAR(64) NULL,
    description NVARCHAR(MAX) NULL
  );
END
GO

IF OBJECT_ID(N'dbo.identities', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.identities (
    identity_id NVARCHAR(128) NOT NULL CONSTRAINT PK_identities PRIMARY KEY,
    identity_name NVARCHAR(256) NOT NULL,
    identity_type NVARCHAR(64) NOT NULL,
    assurance_level NVARCHAR(64) NULL,
    description NVARCHAR(MAX) NULL
  );
END
GO

IF OBJECT_ID(N'dbo.access_policies', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.access_policies (
    policy_id NVARCHAR(128) NOT NULL CONSTRAINT PK_access_policies PRIMARY KEY,
    policy_name NVARCHAR(256) NOT NULL,
    description NVARCHAR(MAX) NULL,
    effect NVARCHAR(16) NOT NULL CONSTRAINT CK_access_policies_effect CHECK (effect IN (N'ALLOW', N'DENY')),
    conditions_json NVARCHAR(MAX) NULL,
    enforcement_point NVARCHAR(256) NULL
  );
END
GO

IF OBJECT_ID(N'dbo.policy_assets', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.policy_assets (
    policy_id NVARCHAR(128) NOT NULL,
    asset_id NVARCHAR(128) NOT NULL,
    CONSTRAINT PK_policy_assets PRIMARY KEY (policy_id, asset_id),
    CONSTRAINT FK_policy_assets_policy FOREIGN KEY (policy_id) REFERENCES dbo.access_policies(policy_id),
    CONSTRAINT FK_policy_assets_asset FOREIGN KEY (asset_id) REFERENCES dbo.assets(asset_id)
  );
END
GO

IF OBJECT_ID(N'dbo.policy_identities', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.policy_identities (
    policy_id NVARCHAR(128) NOT NULL,
    identity_id NVARCHAR(128) NOT NULL,
    CONSTRAINT PK_policy_identities PRIMARY KEY (policy_id, identity_id),
    CONSTRAINT FK_policy_identities_policy FOREIGN KEY (policy_id) REFERENCES dbo.access_policies(policy_id),
    CONSTRAINT FK_policy_identities_identity FOREIGN KEY (identity_id) REFERENCES dbo.identities(identity_id)
  );
END
GO

IF OBJECT_ID(N'dbo.graph_evidence', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.graph_evidence (
    evidence_id BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_graph_evidence PRIMARY KEY,
    source_name NVARCHAR(128) NOT NULL,
    source_endpoint NVARCHAR(1024) NOT NULL,
    evidence_key NVARCHAR(512) NOT NULL,
    evidence_json NVARCHAR(MAX) NOT NULL,
    ingestion_status NVARCHAR(32) NOT NULL,
    observed_at DATETIME2 NOT NULL CONSTRAINT DF_graph_evidence_observed_at DEFAULT SYSUTCDATETIME()
  );
END
GO
