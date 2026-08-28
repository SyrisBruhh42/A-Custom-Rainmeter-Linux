# Lumina-Forest Custom Desktop Suite (Linux Rainmeter-Equivalent)

A high-performance, window-aware, dynamic desktop suite designed for Linux desktops (GNOME/X11 & Wayland), optimized for multi-monitor PLP (Portrait-Landscape-Portrait) setups, hardware telemetry, and real-time glass/light dynamics.

## Key Features
- **Window-Aware Occlusion Engine**: Automatically detects open windows, calculating desktop visibility to pause, fade, or reflow widgets dynamically.
- **Hardware Telemetry**: Deep monitoring for AMD Ryzen 7 5800X (8C/16T), NVIDIA RTX 4070 SUPER, 128GB RAM, Samsung NVMe, and Sound BlasterX G6 audio.
- **Circadian & Audio Light Dynamics**: Sage Green, Deep Lake Blue, and Warm Campfire Ember color palettes with f.lux-style solar shifts and audio-reactive glass reflections.
- **PLP Triple Monitor Ready**: Pre-configured layout targeting 1080x1920 (Left), 1920x1080 (Center Main @ 180Hz), and 1080x1920 (Right).
- **Crucible Protocol Validated**: Includes deterministic verification tools, test suite, and automated health diagnostics.

## Directory Structure
- `src/daemons/`: Window occlusion tracker and IPC daemons.
- `src/telemetry/`: Hardware sensor collection (CPU, GPU, RAM, NVMe, Audio).
- `src/themes/`: Theme engine for colors, circadian flux shifts, and CSS glass styling.
- `src/widgets/`: Modular widget configurations and HTML/CSS/GTK render specs.
- `src/cli/`: `lumina` CLI tool for system management, layout switching, and debugging.
- `tests/`: Pytest suite for sensor validation, geometry calculations, and crucible verification.
