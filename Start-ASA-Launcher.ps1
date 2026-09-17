[CmdletBinding()]
param(
    [string]$ConfigPath,
    [Nullable[int]]$Port
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (-not $ConfigPath) {
    $ConfigPath = Join-Path $ProjectRoot 'launcher.json'
}

if (-not (Test-Path -LiteralPath $Python)) {
    throw 'The launcher is not installed. Run .\Setup-ASA-Launcher.ps1 first.'
}
if (-not (Test-Path -LiteralPath $ConfigPath)) {
    throw "Configuration file not found: $ConfigPath"
}

Set-Location -LiteralPath $ProjectRoot
$Arguments = @('-m', 'asa_launcher', '--config', $ConfigPath)
if ($null -ne $Port) {
    $Arguments += @('--port', $Port.ToString())
}

Write-Host 'Starting ASA Launcher. Press Ctrl+C to stop.' -ForegroundColor Cyan
& $Python @Arguments
exit $LASTEXITCODE

