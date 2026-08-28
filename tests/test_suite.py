"""
Pytest unit tests for Lumina Desktop Suite modules.
"""

import pytest
from src.telemetry.sensor_daemon import SensorDaemon
from src.daemons.window_tracker import WindowTrackerDaemon, MonitorSpec
from src.themes.theme_engine import ThemeEngine


def test_sensor_daemon_keys():
    daemon = SensorDaemon()
    data = daemon.collect_all()
    assert "cpu" in data
    assert "memory" in data
    assert "gpu" in data
    assert "storage" in data


def test_monitor_spec_intersection():
    mon = MonitorSpec("center", 1080, 840, 1920, 1080)
    # Full coverage
    assert mon.intersects(1080, 840, 1920, 1080) == 1920 * 1080
    # No coverage
    assert mon.intersects(0, 0, 500, 500) == 0.0
    # Partial coverage (half left side)
    assert mon.intersects(1080, 840, 960, 1080) == 960 * 1080


def test_theme_circadian_factor():
    engine = ThemeEngine()
    assert engine.get_circadian_factor(12.0) == 1.0
    assert abs(engine.get_circadian_factor(6.0) - 0.5) < 0.05
    assert engine.get_circadian_factor(0.0) == 0.0


def test_occlusion_modes():
    daemon = WindowTrackerDaemon()
    # Test hidden pause threshold
    report = daemon.calculate_occlusion([
        {"x": 0, "y": 0, "w": 1080, "h": 1920, "title": "Left Fullscreen"}
    ])
    assert report["monitors"]["left"]["render_mode"] == "paused"
    assert report["monitors"]["left"]["target_fps"] == 1
