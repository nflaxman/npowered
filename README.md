# VERIDM

## Run the Zachman Matrix UI (Streamlit)

1. Create/activate a Python virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Start the app:
   - `streamlit run src/web/streamlit_app.py`

The app will auto-initialize a local DuckDB database at `data/veridm.duckdb` using:
- `src/db/duckdb/schema.sql`
- `src/db/duckdb/seed_row1_row2_protect_surface.sql`

Optional override:
- Set `VERIDM_DUCKDB_PATH` to point at another DuckDB file.

