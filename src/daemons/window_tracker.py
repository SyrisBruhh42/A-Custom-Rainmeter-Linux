"""
Active Window Occlusion & Desktop Geometry Tracker Daemon.
Inspects active open window boundaries on the PLP multi-monitor workspace:
- Left Screen (Portrait): 1080 x 1920 (Offset: 0, 0)
- Center Screen (Landscape): 1920 x 1080 (Offset: 1080, 840)
- Right Screen (Portrait): 1080 x 1920 (Offset: 3000, 0)

Calculates screen area coverage / occlusion ratios and emits visibility directives:
- Fully visible: render high-refresh visualizers & detailed telemetry
- Partially occluded: reflow / morph into compact status mode
- Fully covered / hidden: pause heavy rendering & lower refresh rate
"""

import json
import subprocess
from typing import Dict, List, Any


class MonitorSpec:
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, wx: int, wy: int, ww: int, wh: int) -> float:
        """Returns intersection area with a given window rectangle."""
        ix1 = max(self.x, wx)
        iy1 = max(self.y, wy)
        ix2 = min(self.x + self.width, wx + ww)
        iy2 = min(self.y + self.height, wy + wh)

        if ix2 > ix1 and iy2 > iy1:
            return float((ix2 - ix1) * (iy2 - iy1))
        return 0.0

    @property
    def area(self) -> float:
        return float(self.width * self.height)


class WindowTrackerDaemon:
    def __init__(self):
        # PLP 3-Monitor Virtual Geometry Setup
        self.monitors = {
            "left": MonitorSpec("left", 0, 0, 1080, 1920),
            "center": MonitorSpec("center", 1080, 840, 1920, 1080),
            "right": MonitorSpec("right", 3000, 0, 1080, 1920)
        }

    def get_open_windows_x11(self) -> List[Dict[str, Any]]:
        """Queries xdotool / wmctrl for active window geometries."""
        windows = []
        try:
            output = subprocess.check_output(["wmctrl", "-lG"], timeout=1).decode('utf-8')
            for line in output.strip().splitlines():
                parts = line.split(maxsplit=7)
                if len(parts) >= 8:
                    x, y, w, h = int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])
                    title = parts[7]
                    windows.append({"x": x, "y": y, "w": w, "h": h, "title": title})
        except Exception:
            pass
        return windows

    def calculate_occlusion(self, open_windows: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        if open_windows is None:
            open_windows = self.get_open_windows_x11()

        mon_covered = {name: 0.0 for name in self.monitors}

        for mon_name, mon in self.monitors.items():
            total_overlap = 0.0
            for win in open_windows:
                overlap = mon.intersects(win["x"], win["y"], win["w"], win["h"])
                total_overlap += overlap
            # Cap occlusion ratio at 1.0 (100%)
            mon_covered[mon_name] = min(1.0, total_overlap / mon.area)

        # Derive dynamic render mode per monitor
        directives = {}
        for mon_name, ratio in mon_covered.items():
            if ratio >= 0.85:
                state = "hidden_pause"
                fps = 1
                mode = "paused"
            elif ratio >= 0.30:
                state = "partially_occluded"
                fps = 15
                mode = "compact"
            else:
                state = "fully_visible"
                fps = 60
                mode = "full_fidelity"

            directives[mon_name] = {
                "occlusion_ratio": round(ratio, 4),
                "state": state,
                "target_fps": fps,
                "render_mode": mode
            }

        return {
            "total_windows_active": len(open_windows),
            "monitors": directives
        }


def main():
    daemon = WindowTrackerDaemon()
    # Test sample with simulated centered fullscreen window
    sample_windows = [
        {"x": 1080, "y": 840, "w": 1920, "h": 1080, "title": "Chrome / Game - Center Screen"}
    ]
    report = daemon.calculate_occlusion(sample_windows)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
