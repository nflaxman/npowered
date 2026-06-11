from __future__ import annotations

import os
import struct
from dataclasses import dataclass
from pathlib import Path


SQL_COPT_SS_ACCESS_TOKEN = 1256


@dataclass(frozen=True)
class AzureSqlConfig:
    server: str
    database: str
    schema_sql_path: Path
    seed_sql_path: Path


class AzureSqlRepository:
    def __init__(self, config: AzureSqlConfig) -> None:
        self.config = config

    @classmethod
    def from_environment(cls, repo_root: Path) -> "AzureSqlRepository":
        server = os.getenv("TRUDY_SQL_SERVER", "").strip()
        database = os.getenv("TRUDY_SQL_DATABASE", "").strip()
        if not server or not database:
            raise ValueError("TRUDY_SQL_SERVER and TRUDY_SQL_DATABASE are required for Azure SQL mode.")
        return cls(
            AzureSqlConfig(
                server=server,
                database=database,
                schema_sql_path=repo_root / "src" / "db" / "sql" / "schema.sql",
                seed_sql_path=repo_root / "src" / "db" / "sql" / "seed_row1_row2_protect_surface.sql",
            )
        )

    def ensure(self) -> None:
        if os.getenv("TRUDY_SQL_AUTO_MIGRATE", "").strip().lower() not in {"1", "true", "yes"}:
            return
        self.migrate()

    def migrate(self) -> None:
        with self.connect() as conn:
            for batch in _split_batches(self.config.schema_sql_path.read_text(encoding="utf-8")):
                conn.execute(batch)
            for batch in _split_batches(self.config.seed_sql_path.read_text(encoding="utf-8")):
                conn.execute(batch)
            conn.commit()

    def load_artifacts(self) -> list[dict]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT
                  perspective,
                  interrogative,
                  zt_pillar,
                  artifact_name,
                  artifact_content
                FROM dbo.zachman_cells
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

    def upsert_artifacts(self, artifacts: list[dict], source: str = "") -> int:
        if not artifacts:
            return 0
        self.ensure()
        with self.connect() as conn:
            for artifact in artifacts:
                conn.execute(
                    """
                    MERGE dbo.zachman_cells AS target
                    USING (
                      SELECT
                        ? AS perspective,
                        ? AS interrogative,
                        ? AS zt_pillar,
                        ? AS artifact_name,
                        ? AS artifact_content
                    ) AS source
                    ON target.perspective = source.perspective
                       AND target.interrogative = source.interrogative
                       AND target.zt_pillar = source.zt_pillar
                       AND target.artifact_name = source.artifact_name
                    WHEN MATCHED THEN
                      UPDATE SET artifact_content = source.artifact_content, updated_at = SYSUTCDATETIME()
                    WHEN NOT MATCHED THEN
                      INSERT (perspective, interrogative, zt_pillar, artifact_name, artifact_content)
                      VALUES (source.perspective, source.interrogative, source.zt_pillar, source.artifact_name, source.artifact_content);
                    """,
                    (
                        artifact.get("perspective") or "",
                        artifact.get("interrogative") or "",
                        artifact.get("zt_pillar") or "",
                        artifact.get("artifact_name") or "",
                        artifact.get("artifact_content") or "",
                    ),
                )
            conn.commit()
        return len(artifacts)

    def insert_evidence(self, evidence: list[dict]) -> int:
        if not evidence:
            return 0
        self.ensure()
        with self.connect() as conn:
            for item in evidence:
                conn.execute(
                    """
                    INSERT INTO dbo.graph_evidence(
                      source_name,
                      source_endpoint,
                      evidence_key,
                      evidence_json,
                      ingestion_status
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        item.get("source_name") or "",
                        item.get("source_endpoint") or "",
                        item.get("evidence_key") or "",
                        item.get("evidence_json") or "{}",
                        item.get("ingestion_status") or "Succeeded",
                    ),
                )
            conn.commit()
        return len(evidence)

    def connect(self):
        import pyodbc

        token = _access_token()
        connection_string = (
            "Driver={ODBC Driver 18 for SQL Server};"
            f"Server=tcp:{self.config.server},1433;"
            f"Database={self.config.database};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        return pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token})


def _access_token() -> bytes:
    from azure.identity import DefaultAzureCredential

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=True)
    raw = credential.get_token("https://database.windows.net/.default").token.encode("utf-16-le")
    return struct.pack(f"<I{len(raw)}s", len(raw), raw)


def _split_batches(sql: str) -> list[str]:
    batches: list[str] = []
    current: list[str] = []
    for line in sql.splitlines():
        if line.strip().upper() == "GO":
            batch = "\n".join(current).strip()
            if batch:
                batches.append(batch)
            current = []
        else:
            current.append(line)
    batch = "\n".join(current).strip()
    if batch:
        batches.append(batch)
    return batches
