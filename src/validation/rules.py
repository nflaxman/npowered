from __future__ import annotations

from src.validation.rule_registry import Rule, RuleContext, RuleRegistry, RuleViolation

INTERROGATIVE_PREDICATES = {
    "What": "defines",
    "How": "performs",
    "Where": "routes_through",
    "Who": "is_responsible_for",
    "When": "triggers",
    "Why": "justifies",
}


def _has_cell(
    artifacts: list[dict],
    perspective: str,
    interrogative: str,
    pillar: str | None = None,
) -> bool:
    for a in artifacts:
        if a["perspective"] != perspective:
            continue
        if a["interrogative"] != interrogative:
            continue
        if pillar is not None and a["zt_pillar"] != pillar:
            continue
        return True
    return False


def codify_triplet(artifact: dict) -> tuple[str, str | None]:
    perspective = artifact.get("perspective") or "UnknownPerspective"
    interrogative = artifact.get("interrogative") or "UnknownInterrogative"
    pillar = artifact.get("zt_pillar") or "UnknownPillar"
    name = artifact.get("artifact_name") or ""
    content = artifact.get("artifact_content") or ""

    subject = f"{perspective}.{interrogative}.{name}".strip(".")
    predicate = INTERROGATIVE_PREDICATES.get(interrogative, "relates_to")
    obj = content.strip()

    if not name.strip() or not obj:
        return (
            f"{subject or perspective} {predicate} <missing object>",
            "Add artifact_name and artifact_content so the Zachman cell can be expressed as Subject Predicate Object.",
        )

    if not pillar.strip():
        return (
            f"{subject} {predicate} {obj}",
            "Set zt_pillar to Identity, Device, Network, Application, or Data.",
        )

    return (f"{subject} {predicate} {obj}", None)


def build_default_registry() -> RuleRegistry:
    registry = RuleRegistry()

    def where_network_requires_why(ctx: RuleContext):
        if ctx.interrogative != "Where":
            return []
        if not _has_cell(ctx.artifacts, ctx.perspective, "Where", pillar="Network"):
            return []
        if _has_cell(ctx.artifacts, ctx.perspective, "Why"):
            return []
        return [
            RuleViolation(
                code="ZT_WHERE_REQUIRES_WHY",
                message="Network path/route exists without a corresponding Why (policy intent/governance) artifact.",
                remediation="Create a Why artifact for the same Zachman perspective that states policy intent, governance rationale, and approval authority for the network path.",
                triplet=f"{ctx.perspective}.Where.Network routes_through <network path> requires {ctx.perspective}.Why.<policy intent>",
            )
        ]

    registry.register(
        Rule(
            code="ZT_WHERE_REQUIRES_WHY",
            description="If a perspective defines a Network Where artifact, it must also define a Why policy-intent artifact.",
            fn=where_network_requires_why,
        )
    )

    def artifact_requires_triplet(ctx: RuleContext):
        out = []
        for artifact in ctx.artifacts:
            if artifact.get("perspective") != ctx.perspective:
                continue
            if artifact.get("interrogative") != ctx.interrogative:
                continue
            triplet, remediation = codify_triplet(artifact)
            if remediation:
                out.append(
                    RuleViolation(
                        code="ZACHMAN_TRIPLET_INCOMPLETE",
                        message="Artifact cannot be expressed as a complete Zachman subject-predicate-object triplet.",
                        remediation=remediation,
                        triplet=triplet,
                    )
                )
        return out

    registry.register(
        Rule(
            code="ZACHMAN_TRIPLET_INCOMPLETE",
            description="Each Zachman cell artifact must have enough metadata to form a subject-predicate-object triplet.",
            fn=artifact_requires_triplet,
        )
    )

    return registry

