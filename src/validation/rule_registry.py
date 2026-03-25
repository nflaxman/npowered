from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class RuleContext:
    artifacts: list[dict]
    perspective: str
    interrogative: str


@dataclass(frozen=True)
class RuleViolation:
    code: str
    message: str


RuleFn = Callable[[RuleContext], Iterable[RuleViolation]]


@dataclass(frozen=True)
class Rule:
    code: str
    description: str
    fn: RuleFn


class RuleRegistry:
    def __init__(self) -> None:
        self._rules: list[Rule] = []

    def register(self, rule: Rule) -> None:
        if any(r.code == rule.code for r in self._rules):
            raise ValueError(f"Duplicate rule code: {rule.code}")
        self._rules.append(rule)

    def rules(self) -> tuple[Rule, ...]:
        return tuple(self._rules)

