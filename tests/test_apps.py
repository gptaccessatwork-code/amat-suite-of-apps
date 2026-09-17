"""Tests for registry validation and failure isolation."""

from __future__ import annotations

import unittest

from asa_launcher.registry import AppStatus, load_applications, parse_application


class ApplicationRegistryTests(unittest.TestCase):
    def test_parses_available_application(self) -> None:
        application = parse_application(
            {
                "id": "test_app",
                "name": "Test App",
                "description": "A test application.",
                "url": "http://example.test:8102",
                "status": "available",
                "icon": "science",
            }
        )

        self.assertEqual(application.status, AppStatus.AVAILABLE)
        self.assertEqual(application.icon, "science")

    def test_non_available_application_may_omit_url(self) -> None:
        application = parse_application(
            {
                "id": "future_app",
                "name": "Future App",
                "description": "Not released yet.",
                "status": "coming_soon",
            }
        )

        self.assertIsNone(application.url)
        self.assertEqual(application.icon, "apps")

    def test_invalid_entry_does_not_hide_valid_entries(self) -> None:
        applications = load_applications(
            (
                {"id": "broken"},
                {
                    "id": "valid_app",
                    "name": "Valid App",
                    "description": "Still loads.",
                    "url": "https://apps.example.test/valid",
                    "status": "available",
                },
            )
        )

        self.assertEqual([app.id for app in applications], ["valid_app"])

    def test_non_object_entry_does_not_hide_valid_entries(self) -> None:
        applications = load_applications(
            (
                "not an object",
                {
                    "id": "valid_app",
                    "name": "Valid App",
                    "description": "Still loads.",
                    "url": "https://apps.example.test/valid",
                    "status": "available",
                },
            )
        )

        self.assertEqual([app.id for app in applications], ["valid_app"])

    def test_duplicate_ids_are_skipped(self) -> None:
        entry = {
            "id": "same_app",
            "name": "Same App",
            "description": "Duplicate test.",
            "url": "https://apps.example.test/same",
            "status": "available",
        }

        self.assertEqual(len(load_applications((entry, entry))), 1)


if __name__ == "__main__":
    unittest.main()
