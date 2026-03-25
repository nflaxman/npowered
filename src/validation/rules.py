from __future__ import annotations

from src.validation.rule_registry import Rule, RuleContext, RuleRegistry, RuleViolation


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
            )
        ]

    registry.register(
        Rule(
            code="ZT_WHERE_REQUIRES_WHY",
            description="If a perspective defines a Network Where artifact, it must also define a Why policy-intent artifact.",
            fn=where_network_requires_why,
        )
    )

    return registry

