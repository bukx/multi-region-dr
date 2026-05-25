"""Failover orchestration logic for the DR simulator."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import RegionState, ReplicationStatus


class DRManager:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.primary_region = config["primary_region"]
        self.secondary_region = config["secondary_region"]
        self.rpo_minutes = int(config["rpo_minutes"])
        self.rto_minutes = int(config["rto_minutes"])

    @classmethod
    def from_file(cls, path: str | Path) -> "DRManager":
        return cls(json.loads(Path(path).read_text()))

    def region(self, name: str) -> RegionState:
        data = self.config["regions"][name]
        return RegionState(
            name=name,
            role=data["role"],
            healthy=bool(data["healthy"]),
            warm=bool(data["warm"]),
        )

    def replication_status(self) -> ReplicationStatus:
        data = self.config["replication"]
        return ReplicationStatus(
            dynamodb_seconds=int(data["dynamodb_seconds"]),
            s3_seconds=int(data["s3_seconds"]),
        )

    def status(self) -> dict:
        primary = self.region(self.primary_region)
        secondary = self.region(self.secondary_region)
        replication = self.replication_status()
        return {
            "traffic_region": self.config["traffic_region"],
            "rpo_minutes": self.rpo_minutes,
            "rto_minutes": self.rto_minutes,
            "rpo_within_target": replication.within_rpo(self.rpo_minutes),
            "replication": asdict(replication),
            "regions": [asdict(primary), asdict(secondary)],
        }

    def failover(self, reason: str) -> dict:
        primary = self.config["regions"][self.primary_region]
        secondary = self.config["regions"][self.secondary_region]
        primary["healthy"] = False
        secondary["role"] = "primary"
        self.config["traffic_region"] = self.secondary_region
        return {
            "action": "failover",
            "reason": reason,
            "traffic_region": self.secondary_region,
            "message": f"Traffic moved to {self.secondary_region}",
        }

    def recover_primary(self) -> dict:
        primary = self.config["regions"][self.primary_region]
        secondary = self.config["regions"][self.secondary_region]
        primary["healthy"] = True
        primary["role"] = "primary"
        secondary["role"] = "secondary"
        self.config["traffic_region"] = self.primary_region
        return {
            "action": "recovery",
            "traffic_region": self.primary_region,
            "message": f"Traffic restored to {self.primary_region}",
        }
