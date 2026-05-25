"""Shared data structures for the DR simulator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RegionState:
    name: str
    role: str
    healthy: bool
    warm: bool


@dataclass(slots=True)
class ReplicationStatus:
    dynamodb_seconds: int
    s3_seconds: int

    def within_rpo(self, rpo_minutes: int) -> bool:
        budget = rpo_minutes * 60
        return self.dynamodb_seconds <= budget and self.s3_seconds <= budget
