from __future__ import annotations

import argparse
import os

from src.db.repository import repo_root
from src.db.sql.db import AzureSqlRepository


def bootstrap(web_identity_name: str, graph_identity_name: str) -> None:
    repo = AzureSqlRepository.from_environment(repo_root())
    repo.migrate()

    with repo.connect() as conn:
        _ensure_external_user(conn, web_identity_name)
        _ensure_external_user(conn, graph_identity_name)
        _ensure_role(conn, "db_datareader", web_identity_name)
        _ensure_role(conn, "db_datareader", graph_identity_name)
        _ensure_role(conn, "db_datawriter", graph_identity_name)
        conn.commit()


def _ensure_external_user(conn, name: str) -> None:
    if not name:
        raise ValueError("Managed identity user name cannot be empty.")
    escaped = name.replace("]", "]]")
    conn.execute(
        f"""
        IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'{name.replace("'", "''")}')
        BEGIN
          CREATE USER [{escaped}] FROM EXTERNAL PROVIDER;
        END
        """
    )


def _ensure_role(conn, role: str, member: str) -> None:
    escaped_member = member.replace("]", "]]")
    conn.execute(
        f"""
        IF IS_ROLEMEMBER(N'{role}', N'{member.replace("'", "''")}') = 0
        BEGIN
          ALTER ROLE [{role}] ADD MEMBER [{escaped_member}];
        END
        """
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap Trudy Azure SQL schema and managed identity users.")
    parser.add_argument("--web-identity-name", default=os.getenv("TRUDY_WEB_IDENTITY_NAME", ""))
    parser.add_argument("--graph-identity-name", default=os.getenv("TRUDY_GRAPH_IDENTITY_NAME", ""))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bootstrap(args.web_identity_name, args.graph_identity_name)
    print("Azure SQL schema, seed data, and managed identity users are ready.")


if __name__ == "__main__":
    main()
