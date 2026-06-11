# Trudy

## Run the Zachman Matrix UI (Streamlit)

1. Create/activate a Python virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Start the app:
   - `streamlit run src/web/streamlit_app.py`

The app will auto-initialize a local DuckDB database at `data/trudy.duckdb` using:
- `src/db/duckdb/schema.sql`
- `src/db/duckdb/seed_row1_row2_protect_surface.sql`

Optional override:
- Set `TRUDY_DUCKDB_PATH` to point at another DuckDB file.
- Legacy `VERIDM_DUCKDB_PATH` is still accepted as a fallback during the rebrand.

## Azure Hosting

Trudy is prepared for Azure Developer CLI deployment to private Azure Container Apps:

1. Copy `.env.example` values into your azd environment.
2. Set `TRUDY_SQL_ADMIN_OBJECT_ID`, `TRUDY_SQL_ADMIN_LOGIN`, and `TRUDY_SQL_ADMIN_PRINCIPAL_TYPE` to the Entra user or group that will bootstrap Azure SQL.
3. Run `azd provision` to create infrastructure and post-provision Entra/Graph/SQL configuration.
4. Run `azd deploy web` to build and publish the Streamlit container image.

Azure mode uses:
- `TRUDY_DB_PROVIDER=azure_sql`
- `TRUDY_SQL_SERVER=<server>.database.windows.net`
- `TRUDY_SQL_DATABASE=sqldb-trudy`

The Graph ingestion job runs as a scheduled Container Apps Job and uses managed identity app-only permissions.


