# Database / Ingestion

## DuckDB (Primary)

Schema + seeds live in:
- `src/db/duckdb/schema.sql`
- `src/db/duckdb/seed_row1_row2_protect_surface.sql`

These create:
- `zachman_cells(perspective, interrogative, zt_pillar, artifact_name, artifact_content, ...)`
- supporting tables: `assets`, `identities`, `access_policies` (+ join tables)

The Streamlit app auto-initializes `data/trudy.duckdb` through `src/db/duckdb/db.py` when `TRUDY_DB_PROVIDER=duckdb`.

## Azure SQL

Azure SQL mode is selected with:

- `TRUDY_DB_PROVIDER=azure_sql`
- `TRUDY_SQL_SERVER=<server>.database.windows.net`
- `TRUDY_SQL_DATABASE=sqldb-trudy`

The SQL schema and seed files live in `src/db/sql/`. The Azure post-provision script runs `python -m src.db.sql.bootstrap` with an Entra SQL administrator, then grants:

- web managed identity: `db_datareader`
- Graph ingestion managed identity: `db_datareader`, `db_datawriter`

## Legacy CSV Ingestion

Initial ingestion target:
- `data/zachman/zachman_matrix_cells.csv`

Legacy implementation:
- `ingest_zachman_matrix.py` loads the CSV into a local SQLite database.

Example:
- `python src/db/ingest_zachman_matrix.py --csv data/zachman/zachman_matrix_cells.csv --db data/zachman/zachman.sqlite`

After running, the SQLite file will be created or updated. Prefer the DuckDB path for the Trudy app.

