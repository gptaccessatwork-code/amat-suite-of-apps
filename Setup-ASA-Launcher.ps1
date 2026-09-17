[CmdletBinding()]
param(
    [switch]$OpenFirewall
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VirtualEnvironment = Join-Path $ProjectRoot '.venv'
$Python = Join-Path $VirtualEnvironment 'Scripts\python.exe'
$ConfigPath = Join-Path $ProjectRoot 'launcher.json'

Write-Host 'ASA Launcher setup' -ForegroundColor Cyan

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw 'Python Launcher (py.exe) was not found. Install Python 3.11-3.13, then rerun this script.'
}

$PythonVersion = & py -3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ($LASTEXITCODE -ne 0) {
    throw 'A supported Python 3 installation was not found.'
}

$VersionParts = $PythonVersion.Trim().Split('.')
$Major = [int]$VersionParts[0]
$Minor = [int]$VersionParts[1]
if ($Major -ne 3 -or $Minor -lt 11 -or $Minor -gt 13) {
    throw "Python $PythonVersion is unsupported. Install Python 3.11, 3.12, or 3.13."
}

if (-not (Test-Path -LiteralPath $VirtualEnvironment)) {
    Write-Host "Creating virtual environment with Python $PythonVersion..."
    & py -3 -m venv $VirtualEnvironment
    if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed.' }
}

Write-Host 'Installing the pinned launcher package and dependencies...'
& $Python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw 'pip upgrade failed.' }
& $Python -m pip install --upgrade $ProjectRoot
if ($LASTEXITCODE -ne 0) { throw 'Launcher installation failed.' }

Write-Host 'Validating launcher.json...'
& $Python -m asa_launcher --config $ConfigPath --validate-config
if ($LASTEXITCODE -ne 0) { throw 'Configuration validation failed.' }

if ($OpenFirewall) {
    $Identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $Principal = [Security.Principal.WindowsPrincipal]::new($Identity)
    $IsAdministrator = $Principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $IsAdministrator) {
        throw 'Opening the firewall requires an elevated PowerShell window.'
    }

    $Configuration = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
    $Port = [int]$Configuration.launcher.port
    $RuleName = 'ASA AMAT Suite Launcher'
    if (-not (Get-NetFirewallRule -DisplayName $RuleName -ErrorAction SilentlyContinue)) {
        New-NetFirewallRule `
            -DisplayName $RuleName `
            -Direction Inbound `
            -Action Allow `
            -Protocol TCP `
            -LocalPort $Port `
            -Profile Domain,Private | Out-Null
        Write-Host "Opened inbound TCP port $Port for Domain and Private networks."
    }
    else {
        Write-Host "Firewall rule '$RuleName' already exists."
    }
}

Write-Host ''
Write-Host 'Setup complete.' -ForegroundColor Green
Write-Host 'Start the launcher with: .\Start-ASA-Launcher.ps1'

