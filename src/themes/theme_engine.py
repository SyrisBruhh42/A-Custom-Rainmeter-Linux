"""
Theme & Circadian Light Dynamics Engine.
Theme: "Campfire by a Forest Lake in the Mountains"
Color Palette: Sage Greens, Deep Lake Blues, Mountain Mist Gray, Warm Campfire Ember.
Includes f.lux-style solar/time-of-day dynamics and audio-reactive glass reflection variables.
"""

import time
import math
from typing import Dict, Any


class ThemeEngine:
    PALETTES = {
        "sage_green": "#8A9A86",
        "forest_deep": "#1B2A26",
        "lake_blue_deep": "#0F1C2E",
        "lake_blue_accent": "#2B4C6F",
        "mountain_mist": "#9BA8B0",
        "campfire_ember": "#E06D44",
        "campfire_glow": "#F4A261",
        "glass_overlay": "rgba(27, 42, 38, 0.45)",
        "glass_border": "rgba(138, 154, 134, 0.25)"
    }

    def __init__(self, mode: str = "circadian"):
        self.mode = mode  # 'circadian', 'sage_lake', 'campfire_night'

    def get_circadian_factor(self, hour: float = None) -> float:
        """Calculates daylight solar curve between 0.0 (midnight) and 1.0 (noon)."""
        if hour is None:
            t = time.localtime()
            hour = t.tm_hour + t.tm_min / 60.0

        # Sine wave peaked at 12.0 PM
        factor = (math.sin(math.pi * (hour - 6.0) / 12.0) + 1.0) / 2.0
        return max(0.0, min(1.0, factor))

    def get_dynamic_theme(self, audio_level: float = 0.0, hour: float = None) -> Dict[str, Any]:
        c_factor = self.get_circadian_factor(hour)

        # Blend lake blue (day) and campfire ember (night)
        ember_intensity = (1.0 - c_factor) * 0.8 + (audio_level * 0.2)

        # Audio reactivity on glass border pulse
        glass_glow = min(1.0, 0.25 + (audio_level * 0.5))

        return {
            "mode": self.mode,
            "circadian_daylight_factor": round(c_factor, 3),
            "colors": {
                "background_primary": self.PALETTES["forest_deep"] if c_factor < 0.5 else self.PALETTES["lake_blue_deep"],
                "accent_primary": self.PALETTES["sage_green"] if c_factor > 0.3 else self.PALETTES["campfire_glow"],
                "ember_highlight": self.PALETTES["campfire_ember"],
                "text_primary": "#EAF0EC",
                "text_secondary": self.PALETTES["mountain_mist"],
                "glass_bg": f"rgba(15, 28, 46, {0.35 + (1.0 - c_factor) * 0.25:.2f})",
                "glass_border": f"rgba(138, 154, 134, {glass_glow:.2f})",
                "ember_glow_intensity": round(ember_intensity, 3)
            },
            "glass_effects": {
                "backdrop_blur_px": 20,
                "border_radius_px": 12,
                "box_shadow": f"0 8px 32px 0 rgba(0, 0, 0, {0.37 + ember_intensity * 0.15:.2f})"
            }
        }


def main():
    engine = ThemeEngine()
    print("--- Daylight Theme (12:00 PM) ---")
    print(ThemeEngine().get_dynamic_theme(audio_level=0.1, hour=12.0))
    print("\n--- Campfire Night Theme (10:00 PM) ---")
    print(ThemeEngine().get_dynamic_theme(audio_level=0.4, hour=22.0))


if __name__ == "__main__":
    main()
