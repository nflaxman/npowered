from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.validation.rule_registry import RuleContext
from src.validation.rules import build_default_registry

class CellStatus(str, Enum):
    VALID = "Valid"
    UNVERIFIED = "Unverified"
    INVALID = "Invalid"


@dataclass(frozen=True)
class CellIssue:
    code: str
    message: str
    remediation: str = ""
    triplet: str = ""


@dataclass(frozen=True)
class CellValidation:
    status: CellStatus
    issues: tuple[CellIssue, ...] = ()


def _has_cell(artifacts: list[dict], perspective: str, interrogative: str, pillar: str | None = None) -> bool:
    for a in artifacts:
        if a["perspective"] != perspective:
            continue
        if a["interrogative"] != interrogative:
            continue
        if pillar is not None and a["zt_pillar"] != pillar:
            continue
        return True
    return False


def validate_cell(artifacts: list[dict], perspective: str, interrogative: str) -> CellValidation:
    """
    Rule-based validation for AI-mediated reification.

    The point is not to "execute code blindly", but to detect ontology inconsistencies
    across cells and flag them in the UI.

    Current minimal rules (extensible):
    - If a 'Where' cell has Network artifacts, the corresponding 'Why' cell must exist
      (policy intent / governance) for the same perspective.
    """

    exists_any = _has_cell(artifacts, perspective, interrogative)
    if not exists_any:
        return CellValidation(status=CellStatus.UNVERIFIED)

    registry = build_default_registry()
    ctx = RuleContext(artifacts=artifacts, perspective=perspective, interrogative=interrogative)

    issues: list[CellIssue] = []
    for rule in registry.rules():
        for v in rule.fn(ctx):
            issues.append(
                CellIssue(
                    code=v.code,
                    message=v.message,
                    remediation=v.remediation,
                    triplet=v.triplet,
                )
            )

    if issues:
        return CellValidation(status=CellStatus.INVALID, issues=tuple(issues))

    return CellValidation(status=CellStatus.VALID)

