# Database / Ingestion

Initial ingestion target:
- `data/zachman/zachman_matrix_cells.csv`

Starter implementation:
- `ingest_zachman_matrix.py` loads the CSV into a local SQLite database.

## DuckDB (ZT-Zachman-Matrix)

Schema + seeds live in:
- `src/db/duckdb/schema.sql`
- `src/db/duckdb/seed_row1_row2_protect_surface.sql`

These create:
- `zachman_cells(perspective, interrogative, zt_pillar, artifact_name, artifact_content, ...)`
- supporting tables: `assets`, `identities`, `access_policies` (+ join tables)

## Run

Example:
- `python src/db/ingest_zachman_matrix.py --csv data/zachman/zachman_matrix_cells.csv --db data/zachman/zachman.sqlite`

After running, the SQLite file will be created (or updated).

