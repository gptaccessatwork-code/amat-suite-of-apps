"""Compatibility entry point for ``py main.py``."""

from __future__ import annotations

from asa_launcher.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
