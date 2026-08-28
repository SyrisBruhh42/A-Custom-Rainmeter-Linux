"""
Automated Crucible Validation & Deterministic Verification Protocol.
Statically & dynamically verifies system architecture, telemetry bounds,
window occlusion logic, and theme consistency.
"""

import sys
import json
from typing import Dict, Any
from src.telemetry.sensor_daemon import SensorDaemon
from src.daemons.window_tracker import WindowTrackerDaemon
from src.themes.theme_engine import ThemeEngine


class CrucibleValidator:
    def __init__(self):
        self.findings = []

    def verify_telemetry(self) -> bool:
        daemon = SensorDaemon()
        data = daemon.collect_all()

        # Verify schema keys
        required_keys = ["timestamp", "cpu", "memory", "gpu", "storage"]
        for key in required_keys:
            if key not in data:
                self.findings.append(f"CRITICAL: Missing key '{key}' in sensor telemetry output.")
                return False

        # Verify CPU logical cores bounds
        if data["cpu"]["cores_logical"] <= 0:
            self.findings.append("CRITICAL: Invalid CPU core count <= 0.")
            return False

        # Verify Memory bounds
        if data["memory"]["total_gb"] <= 0:
            self.findings.append("CRITICAL: Total RAM reporting <= 0 GB.")
            return False

        return True

    def verify_window_occlusion(self) -> bool:
        daemon = WindowTrackerDaemon()

        # Test 100% occlusion on center monitor
        report = daemon.calculate_occlusion([
            {"x": 1080, "y": 840, "w": 1920, "h": 1080, "title": "Fullscreen Window"}
        ])

        center_mode = report["monitors"]["center"]["render_mode"]
        if center_mode != "paused":
            self.findings.append(f"FAIL: Expected center render_mode 'paused', got '{center_mode}'")
            return False

        return True

    def verify_theme_engine(self) -> bool:
        engine = ThemeEngine()
        day_theme = engine.get_dynamic_theme(hour=12.0)
        night_theme = engine.get_dynamic_theme(hour=22.0)

        if day_theme["colors"]["glass_bg"] == night_theme["colors"]["glass_bg"]:
            self.findings.append("FAIL: Glass translucency did not shift between solar daylight and night.")
            return False

        return True

    def run_crucible_autopsy(self) -> Dict[str, Any]:
        telemetry_ok = self.verify_telemetry()
        occlusion_ok = self.verify_window_occlusion()
        theme_ok = self.verify_theme_engine()

        passed = telemetry_ok and occlusion_ok and theme_ok

        report = {
            "status": "PASSED" if passed else "FAILED",
            "checks": {
                "telemetry_verification": telemetry_ok,
                "window_occlusion_verification": occlusion_ok,
                "theme_engine_verification": theme_ok
            },
            "findings": self.findings
        }
        return report


def main():
    validator = CrucibleValidator()
    report = validator.run_crucible_autopsy()
    print(json.dumps(report, indent=2))
    if report["status"] != "PASSED":
        sys.exit(1)


if __name__ == "__main__":
    main()
