# Trudy Azure Deployment Plan

Status: Ready for Validation

## Objective
Prepare Trudy for Azure hosting on private Azure Container Apps with Azure SQL, Microsoft Entra authentication, and app-only Microsoft Graph ingestion through managed identity.

## Decisions
- Hosting: Azure Container Apps, internal/private environment.
- Database: Azure SQL Database with Microsoft Entra-only authentication.
- Infrastructure: Bicep + Azure Developer CLI.
- Web auth: Microsoft Entra authentication, restricted to a Trudy web users group.
- Graph: App-only Microsoft Graph using managed identity; no client secret.

## Implementation Checklist
- Add Azure Developer CLI project configuration.
- Add Bicep infrastructure for Container Apps, Azure SQL, private networking, identities, ACR, Key Vault, and monitoring.
- Add Streamlit container image build.
- Add database provider abstraction for local DuckDB and Azure SQL.
- Add Azure SQL schema and seed scripts.
- Add Graph ingestion job and normalization path.
- Add post-provision scripts for Entra app auth and Graph app-role assignment.
- Verify local DuckDB fallback and static Python checks.

## Notes
- Azure region defaults to `eastus2` unless overridden by azd.
- Existing private network access is assumed for users.
- Tenant-level Entra and Graph grants may require Privileged Role Administrator, Cloud Application Administrator, or equivalent administrator consent.

## Implemented Artifacts
- `azure.yaml`, `Dockerfile`, `.dockerignore`, `.env.example`
- `infra/main.bicep`, `infra/main.parameters.json`, `infra/scripts/postprovision.ps1`
- `src/db/repository.py`, `src/db/sql/*`
- `src/graph/ingest.py`, `src/graph/normalization.py`

## Validation Proof
- Passed: `python -m compileall -q src`
- Passed: local DuckDB repository smoke test loaded 12 seeded artifacts and accepted a Row 6 artifact.
- Passed: Graph normalization smoke test produced Zachman artifacts and evidence rows.
- Passed: Azure SQL provider fails fast when `TRUDY_SQL_SERVER` and `TRUDY_SQL_DATABASE` are not configured.
- Blocked locally: Azure CLI is not installed, so `az version`, `az bicep version`, `az bicep build`, and `azd` validation could not be run in this workspace.
- Status remains `Ready for Validation` until Azure CLI/AZD validation commands run successfully.
