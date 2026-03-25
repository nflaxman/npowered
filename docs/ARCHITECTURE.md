# Architecture

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

