from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import duckdb


@dataclass(frozen=True)
class DuckDbPaths:
    db_path: Path
    schema_sql_path: Path
    seed_sql_path: Path


def default_paths(repo_root: Path) -> DuckDbPaths:
    return DuckDbPaths(
        db_path=repo_root / "data" / "veridm.duckdb",
        schema_sql_path=repo_root / "src" / "db" / "duckdb" / "schema.sql",
        seed_sql_path=repo_root / "src" / "db" / "duckdb" / "seed_row1_row2_protect_surface.sql",
    )


def ensure_db(paths: DuckDbPaths) -> None:
    paths.db_path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(paths.db_path)) as conn:
        schema_sql = paths.schema_sql_path.read_text(encoding="utf-8")
        conn.execute(schema_sql)

        seed_sql = paths.seed_sql_path.read_text(encoding="utf-8")
        conn.execute(seed_sql)


def connect(paths: DuckDbPaths) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(paths.db_path))

