from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from multi_region_dr.orchestrator import DRManager  # noqa: E402


class DRManagerTests(unittest.TestCase):
    def _write_config(self, payload: dict) -> pathlib.Path:
        tmpdir = pathlib.Path(tempfile.mkdtemp())
        path = tmpdir / "config.json"
        path.write_text(json.dumps(payload))
        return path

    def test_status_reflects_rpo_budget(self) -> None:
        path = self._write_config(
            {
                "primary_region": "us-east-1",
                "secondary_region": "us-west-2",
                "rpo_minutes": 5,
                "rto_minutes": 15,
                "traffic_region": "us-east-1",
                "replication": {"dynamodb_seconds": 60, "s3_seconds": 120},
                "regions": {
                    "us-east-1": {"role": "primary", "healthy": True, "warm": True},
                    "us-west-2": {"role": "secondary", "healthy": True, "warm": True},
                },
            }
        )
        manager = DRManager.from_file(path)
        status = manager.status()
        self.assertTrue(status["rpo_within_target"])
        self.assertEqual(status["traffic_region"], "us-east-1")

    def test_failover_moves_traffic_to_secondary(self) -> None:
        path = ROOT / "config" / "example.json"
        manager = DRManager.from_file(path)
        result = manager.failover("region outage")
        self.assertEqual(result["traffic_region"], "us-west-2")
        self.assertEqual(manager.status()["traffic_region"], "us-west-2")

    def test_recovery_restores_primary(self) -> None:
        path = ROOT / "config" / "example.json"
        manager = DRManager.from_file(path)
        manager.failover("drill")
        result = manager.recover_primary()
        self.assertEqual(result["traffic_region"], "us-east-1")


if __name__ == "__main__":
    unittest.main()
