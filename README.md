# ASA - AMAT Suite of Apps

Version 1.0.0

A production-oriented NiceGUI portal for launching internally hosted engineering
applications. Each linked application remains an independent process and opens in a
new browser tab.

## Release contents

- `launcher.json` - server settings and application registry
- `Setup-ASA-Launcher.ps1` - creates an isolated Python environment and installs the app
- `Start-ASA-Launcher.ps1` - validates paths and hosts the portal
- `Build-Release.ps1` - creates a clean deployment ZIP
- `asa_launcher/` - Python package
- `tests/` - configuration and registry tests

## Deploy to a second Windows PC

1. Install 64-bit Python 3.11, 3.12, or 3.13 from your approved company source.
   During installation, include the Python Launcher (`py.exe`).
2. Extract the release ZIP to a stable local path such as `C:\ASA\Launcher`.
3. Edit `launcher.json` and confirm the application URLs are reachable from user PCs.
4. Open PowerShell in the extracted directory.
5. Run setup:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Setup-ASA-Launcher.ps1
```

6. Start the portal:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Start-ASA-Launcher.ps1
```

The terminal remains attached to the server. Press `Ctrl+C` to stop it. Users can
browse to `http://SECOND-PC-HOSTNAME:8000` while the process is running.

Setup requires internet or internal package-index access to download Python packages.
Later starts use the local `.venv` and do not reinstall anything.

### Windows Firewall

If company policy permits the setup script to create the inbound rule, open an
elevated PowerShell window and use:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Setup-ASA-Launcher.ps1 -OpenFirewall
```

The switch opens the configured TCP port for Domain and Private profiles only. If
firewall rules are centrally managed, ask IT to allow inbound TCP port `8000` instead.

## Configuration

All routine deployment settings are in `launcher.json`:

```json
{
  "launcher": {
    "host": "0.0.0.0",
    "port": 8000,
    "log_level": "INFO",
    "log_file": "logs/asa_launcher.log"
  },
  "applications": [
    {
      "id": "delta_bom",
      "name": "Delta BOM Generator",
      "description": "Compare BOM revisions and generate structured delta reports.",
      "url": "http://sg1wgm0nkfwa-1:8099/",
      "status": "available",
      "icon": "description"
    }
  ]
}
```

Changes require a launcher restart because production mode intentionally disables
automatic reload.

The checked-in registry also includes **Excel Scraper for Quotes**, hosted on the
OneDrive PC at `http://SG1WPF5LM0PD:8101/`. Start that project's
`Start-LAN-Server.ps1` separately; ASA opens it in a new tab and does not launch its
server. If the quote host changes, update its URL in `launcher.json`. For an ASA
deployment using a copied release, copy the updated registry and restart that
launcher. The existing Delta BOM entry is preserved.

**AMAT System Type Identifier** is registered at
`http://sg1wgm0nkfwa-1:8100/`, assuming the same host as Delta BOM and the
identifier's source default port. Confirm this URL against the deployed server:
its deployment examples use port `8080`, which may be set through
`AMAT_MATCHER_PORT` in `.env`. ASA does not start the identifier server.

**Production Issues Tracker (PIT)** is registered as
`production_issues_tracker` at `http://sg1wgm0nkfwa-1:8102/`.
PIT runs independently; configure its `pit_settings.json` port as `8102` and
start its `PIT Server.exe` on the hosting PC. ASA opens
the tracker in a new tab, where PIT's own admin lock controls database editing.
If the host or port changes, update this URL in `launcher.json` and restart ASA.

### Add an application

Add one object to the `applications` array. Supported statuses are:

- `available` - enabled blue button; requires an HTTP or HTTPS URL
- `unavailable` - unavailable badge and disabled button
- `coming_soon` - coming-soon badge and disabled button

`icon` accepts a Material icon name. Invalid application entries are logged and
skipped individually; they do not take down the portal.

### Environment overrides

These optional variables override launcher-level JSON settings:

- `ASA_CONFIG_FILE`
- `ASA_LAUNCHER_HOST`
- `ASA_LAUNCHER_PORT`
- `ASA_LOG_LEVEL`

## Operations

Validate configuration without starting the server:

```powershell
.\.venv\Scripts\python.exe -m asa_launcher --config .\launcher.json --validate-config
```

Check server health:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Logs rotate automatically at approximately 2 MB, retaining five backups under
`logs\` by default.

Only one process can listen on port `8000`. A WinError 10048 means another launcher
instance is already running.

## Start automatically with Windows Task Scheduler

Create a task that runs whether a user is logged on or not, using an approved service
account. Configure:

- Program: `powershell.exe`
- Arguments: `-NoProfile -ExecutionPolicy Bypass -File "C:\ASA\Launcher\Start-ASA-Launcher.ps1"`
- Start in: `C:\ASA\Launcher`
- Trigger: At startup

Do not store credentials in `launcher.json` or the PowerShell scripts.

## Development and validation

Install locally with `Setup-ASA-Launcher.ps1`, then run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m asa_launcher --config .\launcher.json --validate-config
```

Build a distributable ZIP:

```powershell
.\Build-Release.ps1
```

The archive is written to `release\ASA-Launcher-1.0.0.zip`.
