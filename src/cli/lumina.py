#!/usr/bin/env python3
"""
Lumina CLI Manager Tool.
Provides command-line commands for suite orchestration, daemon control,
geometry inspection, theme testing, and health checks.
"""

import sys
import json
import argparse
from src.telemetry.sensor_daemon import SensorDaemon
from src.daemons.window_tracker import WindowTrackerDaemon
from src.themes.theme_engine import ThemeEngine


def cmd_status(args):
    print("=== Lumina Desktop Suite Status ===")
    sensors = SensorDaemon().collect_all()
    tracker = WindowTrackerDaemon().calculate_occlusion()
    theme = ThemeEngine().get_dynamic_theme()

    print(f"CPU Load: {sensors['cpu']['overall_load']}% | Temp: {sensors['cpu']['temperature_c']}°C")
    print(f"GPU Utilization: {sensors['gpu']['utilization_percent']}% | Temp: {sensors['gpu']['temperature_c']}°C")
    print(f"RAM Used: {sensors['memory']['used_gb']} GB / {sensors['memory']['total_gb']} GB")
    print("\n--- Monitor Occlusion Directives ---")
    for mon, data in tracker['monitors'].items():
        print(f"[{mon.upper()}] Mode: {data['render_mode']} | Target FPS: {data['target_fps']} | Occlusion: {data['occlusion_ratio']*100:.1f}%")
    print(f"\nActive Theme Colors: Primary BG={theme['colors']['background_primary']}, Accent={theme['colors']['accent_primary']}")


def cmd_telemetry(args):
    sensors = SensorDaemon().collect_all()
    print(json.dumps(sensors, indent=2))


def cmd_occlusion(args):
    tracker = WindowTrackerDaemon().calculate_occlusion()
    print(json.dumps(tracker, indent=2))


def cmd_theme(args):
    theme = ThemeEngine().get_dynamic_theme(hour=args.hour if args.hour is not None else 12.0)
    print(json.dumps(theme, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Lumina Suite CLI Control Tool")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Display suite status summary")
    subparsers.add_parser("telemetry", help="Print telemetry JSON feed")
    subparsers.add_parser("occlusion", help="Print current monitor occlusion directives")

    theme_p = subparsers.add_parser("theme", help="Print current dynamic theme specs")
    theme_p.add_argument("--hour", type=float, help="Simulate hour of day (0.0 to 24.0)")

    args = parser.parse_args()

    if args.command == "status" or not args.command:
        cmd_status(args)
    elif args.command == "telemetry":
        cmd_telemetry(args)
    elif args.command == "occlusion":
        cmd_occlusion(args)
    elif args.command == "theme":
        cmd_theme(args)


if __name__ == "__main__":
    main()
