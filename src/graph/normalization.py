from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GraphRecord:
    source_name: str
    source_endpoint: str
    key: str
    payload: Any


def artifacts_from_records(records: list[GraphRecord]) -> list[dict]:
    artifacts: list[dict] = []
    for record in records:
        artifacts.extend(_artifact_for_record(record))
    return artifacts


def evidence_from_records(records: list[GraphRecord]) -> list[dict]:
    return [
        {
            "source_name": r.source_name,
            "source_endpoint": r.source_endpoint,
            "evidence_key": r.key,
            "evidence_json": json.dumps(r.payload, sort_keys=True, default=str),
            "ingestion_status": "Succeeded",
        }
        for r in records
    ]


def _artifact_for_record(record: GraphRecord) -> list[dict]:
    payload = record.payload if isinstance(record.payload, dict) else {"value": record.payload}
    summary = _summary(payload)

    if record.source_name == "applications":
        return [
            {
                "perspective": "Row4_Builder",
                "interrogative": "Who",
                "zt_pillar": "Identity",
                "artifact_name": f"GraphApplication:{record.key}",
                "artifact_content": f"App registration evidence from Microsoft Graph: {summary}",
            }
        ]

    if record.source_name == "users":
        return [
            {
                "perspective": "Row6_Operator",
                "interrogative": "Who",
                "zt_pillar": "Identity",
                "artifact_name": f"GraphUser:{record.key}",
                "artifact_content": f"Directory user evidence from Microsoft Graph: {summary}",
            }
        ]

    if record.source_name == "devices":
        return [
            {
                "perspective": "Row6_Operator",
                "interrogative": "What",
                "zt_pillar": "Device",
                "artifact_name": f"GraphDevice:{record.key}",
                "artifact_content": f"Device inventory evidence from Microsoft Graph: {summary}",
            }
        ]

    if record.source_name == "signIns":
        return [
            {
                "perspective": "Row6_Operator",
                "interrogative": "When",
                "zt_pillar": "Identity",
                "artifact_name": f"GraphSignIn:{record.key}",
                "artifact_content": f"Sign-in telemetry evidence from Microsoft Graph: {summary}",
            }
        ]

    if record.source_name == "reports":
        return [
            {
                "perspective": "Row6_Operator",
                "interrogative": "When",
                "zt_pillar": "Application",
                "artifact_name": "GraphReports:Office365ActiveUsers",
                "artifact_content": f"Microsoft 365 usage report evidence from Microsoft Graph: {summary}",
            }
        ]

    if record.source_name == "sites":
        return [
            {
                "perspective": "Row6_Operator",
                "interrogative": "Where",
                "zt_pillar": "Data",
                "artifact_name": f"GraphSite:{record.key}",
                "artifact_content": f"SharePoint/OneDrive location evidence from Microsoft Graph: {summary}",
            }
        ]

    if record.source_name == "conditionalAccess":
        return [
            {
                "perspective": "Row4_Builder",
                "interrogative": "Why",
                "zt_pillar": "Identity",
                "artifact_name": f"GraphConditionalAccess:{record.key}",
                "artifact_content": f"Conditional Access policy evidence from Microsoft Graph: {summary}",
            }
        ]

    return [
        {
            "perspective": "Row6_Operator",
            "interrogative": "What",
            "zt_pillar": "Application",
            "artifact_name": f"GraphEvidence:{record.source_name}:{record.key}",
            "artifact_content": f"Microsoft Graph governance evidence: {summary}",
        }
    ]


def _summary(payload: dict) -> str:
    interesting_keys = [
        "id",
        "displayName",
        "appId",
        "userPrincipalName",
        "deviceId",
        "createdDateTime",
        "signInAudience",
        "state",
        "webUrl",
        "value",
    ]
    parts = []
    for key in interesting_keys:
        value = payload.get(key)
        if value is None:
            continue
        text = str(value).replace("\n", " ").strip()
        if len(text) > 240:
            text = f"{text[:237]}..."
        parts.append(f"{key}={text}")
    if parts:
        return "; ".join(parts)
    compact = json.dumps(payload, sort_keys=True, default=str)
    return compact[:500]
