# Decisions

## Current Decisions

1. **Canonical Zachman × ZT ontology in-repo**
   - The narrative ontology document is maintained at `docs/ZACHMAN_ONTOLOGY_FOR_AI_ARCHITECTURE.md` and is the primary semantic reference for rows/columns, ZT pillars, and Trudy workflow language.

2. **Separate documentation, code, and data**
   - `docs/` contains design/decision documents.
   - `src/` contains web page and database/ingestion logic.
   - `data/` contains initial CSV ingestion data.

3. **Represent the Zachman matrix as cell-level rows**
   - Store matrix content as CSV rows with `row`, `column`, and `cell`.
   - Rationale: makes it easy to ingest, filter, and display by any axis.

4. **Use a local-first ingestion script**
   - Provide a simple ingestion script in `src/db/` that loads `data/zachman/*.csv` into a database.
   - Rationale: lets you validate the data model before wiring a production DB.

## Deferred / TBD

- Choosing the primary database technology for production deployment.
- Defining the full Zachman ontology (row/column labels, normalization, constraints).
- Wiring the web UI to query the database (API layer, auth, pagination, etc.).


