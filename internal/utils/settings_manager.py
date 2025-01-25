import json
from pathlib import Path


class SettingsManager:
    def __init__(self):
        self.settings_dir = Path.home() / ".unity_log_viewer"
        self.settings_file = self.settings_dir / "settings.json"
        self.ensure_settings_dir()
        self.settings = self.load_settings()

    def ensure_settings_dir(self):
        self.settings_dir.mkdir(exist_ok=True)
        if not self.settings_file.exists():
            self.save_settings({"recent_files": {"player": "", "editor": ""}})

    def load_settings(self):
        try:
            with open(self.settings_file, "r") as f:
                return json.load(f)
        except:
            return {"recent_files": {"player": "", "editor": ""}}

    def save_settings(self, settings):
        with open(self.settings_file, "w") as f:
            json.dump(settings, f, indent=4)

    def get_recent_file(self, log_type):
        return self.settings["recent_files"].get(log_type, "")

    def save_recent_file(self, log_type, file_path):
        self.settings["recent_files"][log_type] = file_path
        self.save_settings(self.settings)
