import argparse
import csv
import os
import sqlite3
from typing import Iterable, Tuple


def iter_cells(csv_path: str) -> Iterable[Tuple[str, str, str]]:
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"row", "column", "cell"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError(
                f"CSV header must include {sorted(required)}; got {reader.fieldnames}"
            )

        for i, row in enumerate(reader, start=2):  # start=2 accounts for header line
            row_label = (row.get("row") or "").strip()
            column_label = (row.get("column") or "").strip()
            cell = (row.get("cell") or "").strip()
            if not row_label or not column_label:
                # Ignore incomplete rows (keeps ingestion tolerant of placeholder content).
                continue
            yield row_label, column_label, cell


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS zachman_cells (
            row_label TEXT NOT NULL,
            column_label TEXT NOT NULL,
            cell TEXT,
            PRIMARY KEY (row_label, column_label)
        );
        """
    )
    conn.commit()


def ingest(csv_path: str, db_path: str) -> None:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)

    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        ensure_schema(conn)

        # SQLite >= 3.24 supports ON CONFLICT ... DO UPDATE.
        conn.execute("PRAGMA journal_mode=WAL;")

        rows = list(iter_cells(csv_path))
        conn.executemany(
            """
            INSERT INTO zachman_cells(row_label, column_label, cell)
            VALUES (?, ?, ?)
            ON CONFLICT(row_label, column_label) DO UPDATE SET
                cell = excluded.cell;
            """,
            rows,
        )
        conn.commit()
    finally:
        conn.close()

    print(
        f"Ingested {len(rows)} cell(s) from {csv_path} into {db_path}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest Zachman matrix CSV into SQLite.")
    parser.add_argument(
        "--csv",
        default="data/zachman/zachman_matrix_cells.csv",
        help="Path to zachman_matrix_cells.csv",
    )
    parser.add_argument(
        "--db",
        default="data/zachman/zachman.sqlite",
        help="SQLite database output path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ingest(args.csv, args.db)


if __name__ == "__main__":
    main()

