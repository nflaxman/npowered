from __future__ import annotations

import argparse
import os
from typing import Any

import requests
from azure.identity import DefaultAzureCredential

from src.db.repository import get_repository
from src.graph.normalization import GraphRecord, artifacts_from_records, evidence_from_records


GRAPH_ROOT = "https://graph.microsoft.com/v1.0"

GRAPH_SOURCES = {
    "applications": "/applications?$select=id,appId,displayName,signInAudience,createdDateTime&$top=50",
    "users": "/users?$select=id,displayName,userPrincipalName,accountEnabled,createdDateTime&$top=50",
    "devices": "/devices?$select=id,displayName,deviceId,operatingSystem,trustType,accountEnabled&$top=50",
    "signIns": "/auditLogs/signIns?$top=50",
    "reports": "/reports/getOffice365ActiveUserCounts(period='D30')",
    "sites": "/sites?$search=*&$top=50",
    "conditionalAccess": "/identity/conditionalAccess/policies?$top=50",
}


def acquire_graph_token() -> str:
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=True)
    return credential.get_token("https://graph.microsoft.com/.default").token


def fetch_graph_records(source_names: list[str] | None = None) -> list[GraphRecord]:
    token = acquire_graph_token()
    names = source_names or list(GRAPH_SOURCES)
    records: list[GraphRecord] = []
    for name in names:
        path = GRAPH_SOURCES[name]
        try:
            records.extend(_fetch_source(name, path, token))
        except requests.HTTPError as exc:
            records.append(
                GraphRecord(
                    name,
                    path,
                    f"{name}:error",
                    {
                        "error": str(exc),
                        "statusCode": exc.response.status_code if exc.response is not None else None,
                    },
                )
            )
        except requests.RequestException as exc:
            records.append(GraphRecord(name, path, f"{name}:error", {"error": str(exc)}))
    return records


def ingest(source_names: list[str] | None = None) -> tuple[int, int]:
    records = fetch_graph_records(source_names)
    repo = get_repository()
    inserted_artifacts = repo.upsert_artifacts(artifacts_from_records(records), source="microsoft_graph")

    insert_evidence = getattr(repo, "insert_evidence", None)
    inserted_evidence = 0
    if callable(insert_evidence):
        inserted_evidence = insert_evidence(evidence_from_records(records))

    return inserted_artifacts, inserted_evidence


def _fetch_source(name: str, path: str, token: str) -> list[GraphRecord]:
    url = f"{GRAPH_ROOT}{path}"
    headers = {"Authorization": f"Bearer {token}"}
    records: list[GraphRecord] = []
    while url:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            payload = {"value": response.text[:4000], "contentType": content_type}
            records.append(GraphRecord(name, path, name, payload))
            return records

        payload = response.json()
        rows = payload.get("value")
        if isinstance(rows, list):
            for row in rows:
                key = _record_key(row, fallback=f"{name}:{len(records) + 1}")
                records.append(GraphRecord(name, path, key, row))
        else:
            key = _record_key(payload, fallback=name)
            records.append(GraphRecord(name, path, key, payload))

        url = payload.get("@odata.nextLink")
    return records


def _record_key(payload: Any, fallback: str) -> str:
    if isinstance(payload, dict):
        for key in ("id", "appId", "deviceId", "userPrincipalName", "displayName"):
            value = payload.get(key)
            if value:
                return str(value)
    return fallback


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest Microsoft Graph governance evidence into Trudy.")
    parser.add_argument(
        "--source",
        action="append",
        choices=sorted(GRAPH_SOURCES),
        help="Graph source to ingest. Repeat to select multiple. Defaults to all sources.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if os.getenv("TRUDY_DB_PROVIDER", "").lower() not in {"azure_sql", "azuresql", "sql", "mssql"}:
        print("Warning: TRUDY_DB_PROVIDER is not Azure SQL; graph_evidence rows are only stored in SQL mode.")
    artifacts, evidence = ingest(args.source)
    print(f"Ingested {artifacts} artifact(s) and {evidence} evidence row(s).")


if __name__ == "__main__":
    main()
