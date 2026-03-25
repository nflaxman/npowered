/**
 * ZachmanOrchestrator — 6×6 Zero Trust × Zachman visual grid (React).
 *
 * Pass artifacts from DuckDB `zachman_cells` (or your API). Optional `onCellSelect`
 * fires when the user clicks a cell.
 *
 * @example
 * import ZachmanOrchestrator from './ZachmanOrchestrator.jsx';
 *
 * const artifacts = [
 *   { perspective: 'Row1_Planner', interrogative: 'What', zt_pillar: 'Data',
 *     artifact_name: 'Scope', artifact_content: '…' },
 * ];
 * <ZachmanOrchestrator artifacts={artifacts} />
 */

import { useCallback, useMemo, useState } from "react";

const PERSPECTIVES = [
  ["Row1_Planner", "Planner / Scope"],
  ["Row2_Owner", "Owner / Business Model"],
  ["Row3_Designer", "Designer / System Model"],
  ["Row4_Builder", "Builder / Technology Model"],
  ["Row5_Implementer", "Implementer / Detailed Representations"],
  ["Row6_Operator", "Operator / Functioning Enterprise"],
];

const INTERROGATIVES = [
  ["What", "What (Data)"],
  ["How", "How (Function)"],
  ["Where", "Where (Network)"],
  ["Who", "Who (Identity)"],
  ["When", "When (Time)"],
  ["Why", "Why (Motivation)"],
];

const ZT_PILLARS = ["All", "Identity", "Device", "Network", "Application", "Data"];

function hasCell(artifacts, perspective, interrogative, pillar) {
  return artifacts.some((a) => {
    if (a.perspective !== perspective || a.interrogative !== interrogative) return false;
    if (pillar != null && a.zt_pillar !== pillar) return false;
    return true;
  });
}

/** Mirrors `src/validation/rules.py` default registry (client-side preview). */
function validateCell(artifacts, perspective, interrogative) {
  const existsAny = hasCell(artifacts, perspective, interrogative);
  if (!existsAny) {
    return { status: "Unverified", issues: [] };
  }
  const issues = [];
  if (
    interrogative === "Where" &&
    hasCell(artifacts, perspective, "Where", "Network") &&
    !hasCell(artifacts, perspective, "Why")
  ) {
    issues.push({
      code: "ZT_WHERE_REQUIRES_WHY",
      message:
        "Network path/route exists without a corresponding Why (policy intent/governance) artifact.",
    });
  }
  if (issues.length) {
    return { status: "Invalid", issues };
  }
  return { status: "Valid", issues: [] };
}

function cellVisibleUnderPillar(artifacts, perspective, interrogative, pillar) {
  if (pillar === "All") {
    return hasCell(artifacts, perspective, interrogative);
  }
  return hasCell(artifacts, perspective, interrogative, pillar);
}

function artifactsForCell(artifacts, perspective, interrogative, pillar, searchQuery) {
  const q = (searchQuery || "").trim().toLowerCase();
  const out = [];
  for (const a of artifacts) {
    if (a.perspective !== perspective || a.interrogative !== interrogative) continue;
    if (pillar !== "All" && a.zt_pillar !== pillar) continue;
    if (q) {
      const hay = `${a.zt_pillar} ${a.artifact_name} ${a.artifact_content || ""}`.toLowerCase();
      if (!hay.includes(q)) continue;
    }
    out.push(a);
  }
  out.sort((x, y) =>
    `${x.zt_pillar}:${x.artifact_name}`.localeCompare(`${y.zt_pillar}:${y.artifact_name}`)
  );
  return out;
}

const styles = {
  root: {
    display: "flex",
    flexWrap: "wrap",
    gap: "1.5rem",
    fontFamily: "system-ui, Segoe UI, sans-serif",
    maxWidth: "1200px",
  },
  main: { flex: "1 1 560px", minWidth: 0 },
  panel: {
    flex: "0 0 320px",
    border: "1px solid #ccc",
    borderRadius: "8px",
    padding: "1rem",
    background: "#fafafa",
    alignSelf: "flex-start",
    position: "sticky",
    top: "1rem",
  },
  caption: { color: "#444", fontSize: "0.9rem", marginBottom: "1rem" },
  filters: { marginBottom: "1rem", display: "flex", flexDirection: "column", gap: "0.5rem" },
  label: { fontWeight: 600, fontSize: "0.85rem" },
  select: { padding: "0.35rem", borderRadius: "4px", border: "1px solid #aaa" },
  input: { padding: "0.35rem", borderRadius: "4px", border: "1px solid #aaa" },
  legend: { fontSize: "0.85rem", marginBottom: "0.75rem", lineHeight: 1.5 },
  table: { width: "100%", borderCollapse: "collapse", fontSize: "0.8rem" },
  thCorner: {
    border: "1px solid #ddd",
    padding: "0.35rem",
    background: "#e8e8e8",
    textAlign: "left",
    minWidth: "100px",
  },
  th: {
    border: "1px solid #ddd",
    padding: "0.35rem",
    background: "#e8e8e8",
    textAlign: "center",
    verticalAlign: "bottom",
    maxWidth: "88px",
  },
  rowLabel: {
    border: "1px solid #ddd",
    padding: "0.35rem",
    background: "#f5f5f5",
    fontSize: "0.75rem",
    verticalAlign: "middle",
  },
  cell: {
    border: "1px solid #ddd",
    padding: "0.25rem",
    textAlign: "center",
    verticalAlign: "middle",
  },
  btn: {
    width: "100%",
    padding: "0.4rem 0.2rem",
    fontSize: "0.72rem",
    cursor: "pointer",
    borderRadius: "4px",
    border: "1px solid #888",
    background: "#fff",
  },
  btnDisabled: {
    cursor: "not-allowed",
    opacity: 0.45,
    background: "#eee",
  },
  issue: { fontSize: "0.8rem", marginTop: "0.25rem" },
  artifactBlock: { marginTop: "0.75rem", paddingTop: "0.75rem", borderTop: "1px solid #ddd" },
};

export default function ZachmanOrchestrator({
  artifacts = [],
  onCellSelect,
}) {
  const [pillar, setPillar] = useState("All");
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);

  const handleCellClick = useCallback(
    (perspKey, interKey) => {
      const next = { perspective: perspKey, interrogative: interKey };
      setSelected(next);
      onCellSelect?.(next);
    },
    [onCellSelect]
  );

  const selectedItems = useMemo(() => {
    if (!selected) return [];
    return artifactsForCell(
      artifacts,
      selected.perspective,
      selected.interrogative,
      pillar,
      search
    );
  }, [artifacts, selected, pillar, search]);

  const selectedValidation = useMemo(() => {
    if (!selected) return null;
    return validateCell(artifacts, selected.perspective, selected.interrogative);
  }, [artifacts, selected]);

  return (
    <div style={styles.root}>
      <div style={styles.main}>
        <h1 style={{ marginTop: 0, fontSize: "1.35rem" }}>
          VERIDM — Zachman Matrix (6×6) for Zero Trust
        </h1>
        <p style={styles.caption}>
          Perspectives (rows) × interrogatives (columns). Click a cell to inspect Zero Trust
          artifacts. Cells respect the pillar filter and search in the sidebar.
        </p>

        <div style={styles.filters}>
          <label style={styles.label}>
            Zero Trust pillar
            <select
              style={{ ...styles.select, display: "block", marginTop: "0.25rem", width: "100%", maxWidth: "280px" }}
              value={pillar}
              onChange={(e) => setPillar(e.target.value)}
            >
              {ZT_PILLARS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </label>
          <label style={styles.label}>
            Search artifacts
            <input
              type="search"
              style={{ ...styles.input, display: "block", marginTop: "0.25rem", width: "100%", maxWidth: "280px" }}
              placeholder="artifact name or content…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </label>
        </div>

        <div style={styles.legend}>
          <strong>Legend:</strong> Valid — passes ontology checks; Unverified — no artifacts yet;
          Invalid — rule violation (e.g. Where/Network without Why).
        </div>

        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.thCorner}>Perspective \ Interrogative</th>
              {INTERROGATIVES.map(([key, label]) => (
                <th key={key} style={styles.th}>
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {PERSPECTIVES.map(([perspKey, perspLabel]) => (
              <tr key={perspKey}>
                <td style={styles.rowLabel}>
                  <strong>{perspLabel}</strong>
                  <br />
                  <code style={{ fontSize: "0.65rem" }}>{perspKey}</code>
                </td>
                {INTERROGATIVES.map(([interKey]) => {
                  const enabled = cellVisibleUnderPillar(artifacts, perspKey, interKey, pillar);
                  const validation = validateCell(artifacts, perspKey, interKey);
                  let btnLabel = "—";
                  if (enabled) {
                    if (validation.status === "Valid") btnLabel = "View (Valid)";
                    else if (validation.status === "Invalid") btnLabel = "View (Invalid)";
                    else btnLabel = "View (Unverified)";
                  }
                  const isSelected =
                    selected?.perspective === perspKey && selected?.interrogative === interKey;
                  return (
                    <td key={`${perspKey}:${interKey}`} style={styles.cell}>
                      <button
                        type="button"
                        style={{
                          ...styles.btn,
                          ...(enabled ? {} : styles.btnDisabled),
                          ...(isSelected ? { borderColor: "#06c", boxShadow: "0 0 0 1px #06c" } : {}),
                        }}
                        disabled={!enabled}
                        onClick={() => enabled && handleCellClick(perspKey, interKey)}
                      >
                        {btnLabel}
                      </button>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <aside style={styles.panel} aria-label="Selected cell details">
        <h2 style={{ marginTop: 0, fontSize: "1rem" }}>Selected cell</h2>
        {!selected && <p style={{ margin: 0, color: "#666" }}>Click a cell to load artifacts.</p>}
        {selected && (
          <>
            <p style={{ margin: "0 0 0.5rem", fontSize: "0.9rem" }}>
              <strong>Perspective:</strong> <code>{selected.perspective}</code>
            </p>
            <p style={{ margin: "0 0 0.5rem", fontSize: "0.9rem" }}>
              <strong>Interrogative:</strong> <code>{selected.interrogative}</code>
            </p>
            {selectedValidation && (
              <p style={{ margin: "0 0 0.75rem", fontSize: "0.9rem" }}>
                <strong>Status:</strong> {selectedValidation.status}
              </p>
            )}
            {selectedValidation?.issues?.length > 0 && (
              <div role="alert">
                <strong>Issues:</strong>
                <ul style={{ margin: "0.25rem 0 0 1rem", padding: 0 }}>
                  {selectedValidation.issues.map((issue) => (
                    <li key={issue.code} style={styles.issue}>
                      <code>{issue.code}</code>: {issue.message}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {selectedItems.length === 0 ? (
              <p style={{ color: "#a60", fontSize: "0.9rem", marginTop: "0.75rem" }}>
                No artifacts match the current filter/search for this cell.
              </p>
            ) : (
              selectedItems.map((a) => (
                <div key={`${a.zt_pillar}:${a.artifact_name}`} style={styles.artifactBlock}>
                  <strong>
                    {a.zt_pillar} — {a.artifact_name}
                  </strong>
                  <p style={{ margin: "0.35rem 0 0", whiteSpace: "pre-wrap", fontSize: "0.88rem" }}>
                    {a.artifact_content || ""}
                  </p>
                </div>
              ))
            )}
          </>
        )}
      </aside>
    </div>
  );
}
