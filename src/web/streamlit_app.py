from __future__ import annotations

import streamlit as st

from src.db.repository import db_provider, get_repository
from src.validation.cell_validation import CellStatus, validate_cell
from src.validation.rules import codify_triplet


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


@st.cache_data(show_spinner=False)
def load_artifacts(provider: str) -> list[dict]:
    return get_repository().load_artifacts()


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
    st.set_page_config(page_title="Trudy Zachman Matrix (Zero Trust)", layout="wide")
    st.title("Trudy — Zachman Matrix (6×6) for Zero Trust")

    repo = get_repository()
    repo.ensure()

    st.sidebar.header("Filters")
    pillar = st.sidebar.selectbox("Zero Trust pillar", ZT_PILLARS, index=0)
    search = st.sidebar.text_input("Search artifacts", placeholder="artifact name/content…")

    artifacts = load_artifacts(db_provider())
    context = getattr(st, "context", None)
    headers = getattr(context, "headers", {}) if context else {}
    principal = headers.get("X-MS-CLIENT-PRINCIPAL-NAME")
    if principal:
        st.sidebar.caption(f"Signed in: {principal}")

    st.caption(
        "Operational loop: query evidence, digest it into ontology fields, create a Zachman "
        "triplet, then validate and remediate the 6x6 cell. Cells can be filtered by Zero "
        "Trust pillar and searched by artifact text."
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
            if issue.triplet:
                st.sidebar.code(issue.triplet, language="text")
            if issue.remediation:
                st.sidebar.info(f"Remediation: {issue.remediation}")

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
        triplet, remediation = codify_triplet(a)
        st.sidebar.caption("Codified Zachman triplet")
        st.sidebar.code(triplet, language="text")
        if remediation:
            st.sidebar.warning(f"Remediation: {remediation}")
        st.sidebar.write(a["artifact_content"] or "")


if __name__ == "__main__":
    main()


