from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from src.db.duckdb.db import DuckDbPaths, connect, default_paths, ensure_db
from src.validation.cell_validation import CellStatus, validate_cell


PERSPECTIVES = [
    ("Row1_Planner", "Planner / Scope"),
    ("Row2_Owner", "Owner / Business Model"),
    ("Row3_Designer", "Designer / System Model"),
    ("Row4_Builder", "Builder / Technology Model"),
    ("Row5_Implementer", "Implementer / Detailed Representations"),
    ("Row6_Operator", "Operator / Functioning Enterprise"),
]

INTERROGATIVES = [
    ("What", "What (Data)"),
    ("How", "How (Function)"),
    ("Where", "Where (Network)"),
    ("Who", "Who (Identity)"),
    ("When", "When (Time)"),
    ("Why", "Why (Motivation)"),
]

ZT_PILLARS = ["All", "Identity", "Device", "Network", "Application", "Data"]


def repo_root() -> Path:
    # This file lives at src/web/streamlit_app.py -> repo root is three parents up.
    return Path(__file__).resolve().parents[2]


def get_paths() -> DuckDbPaths:
    root = repo_root()
    paths = default_paths(root)

    override = os.getenv("VERIDM_DUCKDB_PATH")
    if override:
        paths = DuckDbPaths(
            db_path=Path(override),
            schema_sql_path=paths.schema_sql_path,
            seed_sql_path=paths.seed_sql_path,
        )

    return paths


@st.cache_data(show_spinner=False)
def load_artifacts(db_path: str) -> list[dict]:
    paths = get_paths()
    with connect(paths) as conn:
        rows = conn.execute(
            """
            SELECT
              perspective,
              interrogative,
              zt_pillar,
              artifact_name,
              artifact_content
            FROM zachman_cells
            """
        ).fetchall()

    return [
        {
            "perspective": r[0],
            "interrogative": r[1],
            "zt_pillar": r[2],
            "artifact_name": r[3],
            "artifact_content": r[4],
        }
        for r in rows
    ]


def cell_has_pillar(artifacts: list[dict], perspective: str, interrogative: str, pillar: str) -> bool:
    if pillar == "All":
        return any(
            a["perspective"] == perspective and a["interrogative"] == interrogative for a in artifacts
        )
    return any(
        a["perspective"] == perspective
        and a["interrogative"] == interrogative
        and a["zt_pillar"] == pillar
        for a in artifacts
    )


def artifacts_for_cell(
    artifacts: list[dict],
    perspective: str,
    interrogative: str,
    pillar: str,
    query: str,
) -> list[dict]:
    q = query.strip().lower()
    out: list[dict] = []
    for a in artifacts:
        if a["perspective"] != perspective or a["interrogative"] != interrogative:
            continue
        if pillar != "All" and a["zt_pillar"] != pillar:
            continue
        if q:
            hay = f"{a['zt_pillar']} {a['artifact_name']} {a['artifact_content'] or ''}".lower()
            if q not in hay:
                continue
        out.append(a)

    out.sort(key=lambda x: (x["zt_pillar"], x["artifact_name"]))
    return out


def main() -> None:
    st.set_page_config(page_title="VERIDM Zachman Matrix (Zero Trust)", layout="wide")
    st.title("VERIDM — Zachman Matrix (6×6) for Zero Trust")

    paths = get_paths()
    ensure_db(paths)

    st.sidebar.header("Filters")
    pillar = st.sidebar.selectbox("Zero Trust pillar", ZT_PILLARS, index=0)
    search = st.sidebar.text_input("Search artifacts", placeholder="artifact name/content…")

    artifacts = load_artifacts(str(paths.db_path))

    st.caption(
        "Click a cell to view its Zero Trust artifacts. "
        "Cells can be filtered by Zero Trust pillar and searched by artifact text."
    )

    st.sidebar.divider()
    st.sidebar.subheader("Legend")
    st.sidebar.write("**Valid**: artifacts exist and pass ontology checks.")
    st.sidebar.write("**Unverified**: no artifacts yet for the cell.")
    st.sidebar.write("**Invalid**: artifacts exist but violate a consistency rule.")

    # Column headers
    header_cols = st.columns([1.3] + [1] * 6)
    header_cols[0].markdown("**Perspective \\ Interrogative**")
    for i, (_, label) in enumerate(INTERROGATIVES, start=1):
        header_cols[i].markdown(f"**{label}**")

    # Grid
    for persp_key, persp_label in PERSPECTIVES:
        row_cols = st.columns([1.3] + [1] * 6)
        row_cols[0].markdown(f"**{persp_label}**  \n`{persp_key}`")

        for col_idx, (inter_key, _) in enumerate(INTERROGATIVES, start=1):
            enabled = cell_has_pillar(artifacts, persp_key, inter_key, pillar)
            validation = validate_cell(artifacts, persp_key, inter_key)
            status = validation.status

            if not enabled:
                label = "—"
            else:
                if status == CellStatus.VALID:
                    label = "View (Valid)"
                elif status == CellStatus.INVALID:
                    label = "View (Invalid)"
                else:
                    label = "View (Unverified)"

            if row_cols[col_idx].button(
                label,
                key=f"cell:{persp_key}:{inter_key}",
                use_container_width=True,
                disabled=not enabled,
            ):
                st.session_state["selected_cell"] = (persp_key, inter_key)

    # Sidebar selection output
    st.sidebar.divider()
    st.sidebar.subheader("Selected cell")

    selected = st.session_state.get("selected_cell")
    if not selected:
        st.sidebar.info("Click any cell to load its artifacts.")
        return

    selected_persp, selected_inter = selected
    st.sidebar.write(f"**Perspective:** `{selected_persp}`")
    st.sidebar.write(f"**Interrogative:** `{selected_inter}`")

    selected_validation = validate_cell(artifacts, selected_persp, selected_inter)
    st.sidebar.write(f"**Status:** {selected_validation.status.value}")
    if selected_validation.issues:
        st.sidebar.markdown("**Issues:**")
        for issue in selected_validation.issues:
            st.sidebar.write(f"- `{issue.code}`: {issue.message}")

    items = artifacts_for_cell(
        artifacts=artifacts,
        perspective=selected_persp,
        interrogative=selected_inter,
        pillar=pillar,
        query=search,
    )

    if not items:
        st.sidebar.warning("No artifacts match the current filter/search for this cell.")
        return

    for a in items:
        st.sidebar.markdown(f"**{a['zt_pillar']} — {a['artifact_name']}**")
        st.sidebar.write(a["artifact_content"] or "")


if __name__ == "__main__":
    main()

