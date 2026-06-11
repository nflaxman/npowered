from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol

from src.db.duckdb.db import DuckDbPaths, connect as connect_duckdb
from src.db.duckdb.db import default_paths as default_duckdb_paths
from src.db.duckdb.db import ensure_db as ensure_duckdb


class TrudyRepository(Protocol):
    def ensure(self) -> None:
        ...

    def load_artifacts(self) -> list[dict]:
        ...

    def upsert_artifacts(self, artifacts: list[dict], source: str = "") -> int:
        ...


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def db_provider() -> str:
    return os.getenv("TRUDY_DB_PROVIDER", "duckdb").strip().lower()


def get_repository() -> TrudyRepository:
    provider = db_provider()
    if provider in {"duckdb", "local", ""}:
        return DuckDbRepository.from_environment(repo_root())
    if provider in {"azure_sql", "azuresql", "sql", "mssql"}:
        from src.db.sql.db import AzureSqlRepository

        return AzureSqlRepository.from_environment(repo_root())
    raise ValueError(f"Unsupported TRUDY_DB_PROVIDER: {provider}")


class DuckDbRepository:
    def __init__(self, paths: DuckDbPaths) -> None:
        self.paths = paths

    @classmethod
    def from_environment(cls, root: Path) -> "DuckDbRepository":
        paths = default_duckdb_paths(root)
        override = os.getenv("TRUDY_DUCKDB_PATH") or os.getenv("VERIDM_DUCKDB_PATH")
        if override:
            paths = DuckDbPaths(
                db_path=Path(override),
                schema_sql_path=paths.schema_sql_path,
                seed_sql_path=paths.seed_sql_path,
            )
        return cls(paths)

    def ensure(self) -> None:
        ensure_duckdb(self.paths)

    def load_artifacts(self) -> list[dict]:
        with connect_duckdb(self.paths) as conn:
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
        return [_artifact_from_row(r) for r in rows]

    def upsert_artifacts(self, artifacts: list[dict], source: str = "") -> int:
        if not artifacts:
            return 0
        self.ensure()
        with connect_duckdb(self.paths) as conn:
            conn.executemany(
                """
                INSERT OR REPLACE INTO zachman_cells(
                  perspective,
                  interrogative,
                  zt_pillar,
                  artifact_name,
                  artifact_content
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                [_artifact_params(a) for a in artifacts],
            )
        return len(artifacts)


def _artifact_from_row(row: tuple) -> dict:
    return {
        "perspective": row[0],
        "interrogative": row[1],
        "zt_pillar": row[2],
        "artifact_name": row[3],
        "artifact_content": row[4],
    }


def _artifact_params(artifact: dict) -> tuple[str, str, str, str, str]:
    return (
        str(artifact.get("perspective") or ""),
        str(artifact.get("interrogative") or ""),
        str(artifact.get("zt_pillar") or ""),
        str(artifact.get("artifact_name") or ""),
        str(artifact.get("artifact_content") or ""),
    )
