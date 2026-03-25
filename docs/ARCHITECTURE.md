# Architecture

## Canonical ontology reference
The full narrative ontology (Zachman columns/rows, Zero Trust pillars, veridm discipline, Codex prompt workflow, and cited sources) lives in:

- [`docs/ZACHMAN_ONTOLOGY_FOR_AI_ARCHITECTURE.md`](ZACHMAN_ONTOLOGY_FOR_AI_ARCHITECTURE.md)

Use it as the **semantic source** when extending `zachman_cells`, validation rules, and the Streamlit grid. Implementation details in this repo should stay consistent with that document unless `docs/DECISIONS.md` records an explicit deviation.

## Overview
This project is organized into three layers:

1. `docs/` - design docs for how the system should work.
2. `data/` - initial CSV data representing the Zachman matrix.
3. `src/` - implementation code:
   - `src/web/` for the web page UI.
   - `src/db/` for database schema + ingestion logic.

## Data Flow (High Level)
1. Start with Zachman matrix CSV cells under `data/zachman/`.
2. Ingestion logic in `src/db/` loads those cells into a relational table.
3. The web page in `src/web/` can later query/display the ingested results.

## AI-mediated reification (ontology validation)
In a veridm-enabled system, the logic layer does not only execute changes; it **validates changes against the ontology**.

Conceptually:
- A developer (the “Sub-contractor”) proposes a change (often in lower rows like Row 5).
- veridm AI checks the proposal against:
  - `docs/AI_CONTRACT.md` (process + constraints)
  - Row 3 designer models (logical/architectural intent; represented as artifacts in `zachman_cells`)
- If the change introduces inconsistencies (e.g., a new **Where** network route without a corresponding **Why** access policy intent),
  the system flags the affected cell(s) as **Invalid** or **Unverified**.

This enables a “self-healing” architecture where inconsistencies are detected early and surfaced to stakeholders in the grid UI.

### Stakeholder views (same 6×6 language)
- **Planner (strategic view)**: track Zero Trust maturity progress across the protect surface.
- **Architect (system view)**: visualize logical flow of data between zones and layers.
- **Security analyst (operations view)**: map denials/threats to the organizational units and cells they impact.

## Initial Implementation Targets
- Database ingestion:
  - A simple, local-first ingestion script that can load CSV into a database.
- Web page:
  - A static page scaffold that documents where data will be surfaced.

## Folder Responsibilities
- `docs/AI_CONTRACT.md`: how AI should collaborate with this repo.
- `docs/DECISIONS.md`: record of architecture and implementation decisions.
- `src/web/`: UI scaffolding (static HTML + later JS).
- `src/db/`: schema + ingestion (CSV -> DB).
- `data/zachman/`: initial CSV ingestion data.

