# Web

- **Streamlit (primary)**: `streamlit_app.py` — 6×6 grid backed by DuckDB; see repo `README.md`.
- **React (optional)**: `ZachmanOrchestrator.jsx` — same matrix UX for embedding in a React app; pass `artifacts` shaped like DuckDB `zachman_cells` rows (`perspective`, `interrogative`, `zt_pillar`, `artifact_name`, `artifact_content`).

Next steps (typical):
- Wire `ZachmanOrchestrator` to a small API that returns `zachman_cells` JSON from DuckDB.
- Add a UI for filtering by Zachman `row` and `column`.
- Add an API layer (or local querying approach) to read ingested data from the database.

