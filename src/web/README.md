# Web

- **Standalone HTML**: `index.html` — dynamic query-first operational loop with a Microsoft Graph list hook, Zachman 6x6 population, triplet checks, and codified remediation.
- **Streamlit (primary local app)**: `streamlit_app.py` — 6x6 grid backed by DuckDB; see repo `README.md`.
- **React (optional)**: `ZachmanOrchestrator.jsx` — same matrix UX for embedding in a React app.

## Artifact Shape

All web surfaces expect artifacts shaped like DuckDB `zachman_cells` rows. The operational loop can also carry query/digest and Who/How/What fields used to create the triplet:

```json
{
  "perspective": "Row1_Planner",
  "interrogative": "What",
  "zt_pillar": "Data",
  "artifact_name": "ProtectSurfaceScope",
  "artifact_content": "CRM customer records and PII dataset.",
  "query": "GET /identity/conditionalAccess/policies",
  "digest": "Agent normalized the evidence into Zachman ontology fields.",
  "who": "Identity owner",
  "how": "defines protected surface",
  "what": "customer PII dataset"
}
```

## Operational Loop

The standalone page models the loop in this order:

1. Query Microsoft Graph, SharePoint, or the local corpus for evidence.
2. Digest the returned row into ontology fields: perspective, interrogative, Zero Trust pillar, artifact name, and artifact content.
3. Create a Zachman triplet from the ontology, plus a human-readable Who / How / What view.
4. Validate the target 6x6 cell for completeness and consistency.
5. Codify remediation when the triplet is incomplete or the cell violates a rule.

## Microsoft Graph Hook

`index.html` can fetch SharePoint list items from Microsoft Graph when supplied:

- A Graph list endpoint, for example `https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items?expand=fields`
- A bearer token for the current browser session

The token is not stored by the page. The expected Graph response is a list item payload with a `value` array and each row's metadata under `fields`.

Supported field names:

- Native: `perspective`, `interrogative`, `zt_pillar`, `artifact_name`, `artifact_content`
- SharePoint-style: `SNY_Perspective`, `SNY_Interrogative`, `SNY_ZTPillar`, `SNY_ArtifactName`, `SNY_ArtifactContent`
- Optional loop fields: `query` / `SNY_Query`, `digest` / `SNY_Digest`, `who` / `SNY_Who`, `how` / `SNY_How`, `what` / `SNY_What`, `remediation` / `SNY_Remediation`

For React embedding, pass `graphEndpoint` and `graphAccessToken` props to `ZachmanOrchestrator`.

## Azure Graph Ingestion

The Azure deployment uses `python -m src.graph.ingest` as a Container Apps Job. It calls Microsoft Graph with the job's managed identity, stores raw evidence in Azure SQL, and upserts normalized Zachman artifacts for the Streamlit UI to display.

## Triplets and Remediation

Each artifact is codified as a Zachman triplet:

```text
<Perspective>.<Interrogative>.<ArtifactName> <Predicate> <ArtifactContent>
```

Predicate mapping:

- `What` -> `defines`
- `How` -> `performs`
- `Where` -> `routes_through`
- `Who` -> `is_responsible_for`
- `When` -> `triggers`
- `Why` -> `justifies`

Current remediation checks:

- A `Where` / `Network` artifact requires a matching `Why` artifact for the same perspective.
- Every artifact must include enough metadata to form a subject-predicate-object triplet.


