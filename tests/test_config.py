"""Tests for launcher-level JSON configuration."""

from __future__ import annotations

import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from asa_launcher.config import ConfigurationError, load_configuration


class ConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config_path = Path(__file__).with_name("_test_launcher.json")

    def tearDown(self) -> None:
        self.config_path.unlink(missing_ok=True)

    def _write_config(self, data: object) -> Path:
        self.config_path.write_text(json.dumps(data), encoding="utf-8")
        return self.config_path

    def test_loads_settings_and_resolves_relative_log_path(self) -> None:
        path = self._write_config(
            {
                "launcher": {
                    "host": "0.0.0.0",
                    "port": 8123,
                    "log_level": "warning",
                    "log_file": "logs/test.log",
                },
                "applications": [],
            }
        )
        with patch.dict(os.environ, {}, clear=True):
            configuration = load_configuration(path)

        self.assertEqual(configuration.settings.port, 8123)
        self.assertEqual(configuration.settings.log_level, "WARNING")
        self.assertEqual(
            configuration.settings.log_file,
            path.parent / "logs" / "test.log",
        )

    def test_environment_can_override_port(self) -> None:
        path = self._write_config(
            {"launcher": {"port": 8000}, "applications": []}
        )
        with patch.dict(os.environ, {"ASA_LAUNCHER_PORT": "9000"}, clear=True):
            configuration = load_configuration(path)

        self.assertEqual(configuration.settings.port, 9000)

    def test_rejects_invalid_json(self) -> None:
        self.config_path.write_text("{invalid", encoding="utf-8")
        with self.assertRaisesRegex(ConfigurationError, "invalid JSON"):
            load_configuration(self.config_path)

    def test_rejects_missing_applications_array(self) -> None:
        path = self._write_config({"launcher": {"port": 8000}})
        with self.assertRaisesRegex(ConfigurationError, "applications"):
            load_configuration(path)


if __name__ == "__main__":
    unittest.main()
