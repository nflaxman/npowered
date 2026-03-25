# Database / Ingestion

Initial ingestion target:
- `data/zachman/zachman_matrix_cells.csv`

Starter implementation:
- `ingest_zachman_matrix.py` loads the CSV into a local SQLite database.

## Run

Example:
- `python src/db/ingest_zachman_matrix.py --csv data/zachman/zachman_matrix_cells.csv --db data/zachman/zachman.sqlite`

After running, the SQLite file will be created (or updated).

