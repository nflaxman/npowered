# Decisions

## Current Decisions

1. **Separate documentation, code, and data**
   - `docs/` contains design/decision documents.
   - `src/` contains web page and database/ingestion logic.
   - `data/` contains initial CSV ingestion data.

2. **Represent the Zachman matrix as cell-level rows**
   - Store matrix content as CSV rows with `row`, `column`, and `cell`.
   - Rationale: makes it easy to ingest, filter, and display by any axis.

3. **Use a local-first ingestion script**
   - Provide a simple ingestion script in `src/db/` that loads `data/zachman/*.csv` into a database.
   - Rationale: lets you validate the data model before wiring a production DB.

## Deferred / TBD

- Choosing the primary database technology for production deployment.
- Defining the full Zachman ontology (row/column labels, normalization, constraints).
- Wiring the web UI to query the database (API layer, auth, pagination, etc.).

