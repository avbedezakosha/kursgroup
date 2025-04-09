import json
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from typing import Dict, Any


class StyleManager:
    _instance = None
    _current_theme: Dict[str, str] = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._themes = {}
            cls._instance._load_themes()
        return cls._instance

    def _load_themes(self):
        themes_dir = Path(__file__).parent / "themes"
        for theme_file in themes_dir.glob("*.json"):
            with open(theme_file, "r") as f:
                self._themes[theme_file.stem] = json.load(f)

    def set_theme(self, theme_name: str):
        theme = self._themes.get(theme_name, self._themes["dark"])
        self._current_theme = theme
        self._apply_styles()

    def get_color(self, color_name: str) -> str:
        return self._current_theme.get(color_name, "#000000")

    def _apply_styles(self):
        app = QApplication.instance()
        with open(Path(__file__).parent / "main.qss", "r") as f:
            styles = f.read()
            for key, value in self._current_theme.items():
                styles = styles.replace(f"{{{{{key}}}}}", value)
            app.setStyleSheet(styles)