[CmdletBinding()]
param(
    [string]$Version = '1.0.0'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ReleaseDirectory = Join-Path $ProjectRoot 'release'
$ArchivePath = Join-Path $ReleaseDirectory "ASA-Launcher-$Version.zip"
$ArchiveRoot = "ASA-Launcher-$Version"

$Files = @(
    'asa_launcher',
    'tests',
    '.gitignore',
    'launcher.json',
    'main.py',
    'pyproject.toml',
    'requirements.txt',
    'README.md',
    'Setup-ASA-Launcher.ps1',
    'Start-ASA-Launcher.ps1',
    'Build-Release.ps1'
)

New-Item -ItemType Directory -Path $ReleaseDirectory -Force | Out-Null
if (Test-Path -LiteralPath $ArchivePath) {
    Remove-Item -LiteralPath $ArchivePath -Force
}

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$Archive = [System.IO.Compression.ZipFile]::Open(
    $ArchivePath,
    [System.IO.Compression.ZipArchiveMode]::Create
)

try {
    foreach ($Item in $Files) {
        $SourcePath = Join-Path $ProjectRoot $Item
        if (-not (Test-Path -LiteralPath $SourcePath)) {
            throw "Release input not found: $SourcePath"
        }

        $SourceItem = Get-Item -LiteralPath $SourcePath
        $SourceFiles = if ($SourceItem.PSIsContainer) {
            Get-ChildItem -LiteralPath $SourcePath -File -Recurse
        }
        else {
            @($SourceItem)
        }

        foreach ($SourceFile in $SourceFiles) {
            if ($SourceFile.FullName -match '[\\/]__pycache__[\\/]' -or
                $SourceFile.Extension -in @('.pyc', '.log')) {
                continue
            }

            $RelativePath = $SourceFile.FullName.Substring($ProjectRoot.Length).TrimStart('\', '/')
            $EntryName = ($ArchiveRoot + '/' + $RelativePath).Replace('\', '/')
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                $Archive,
                $SourceFile.FullName,
                $EntryName,
                [System.IO.Compression.CompressionLevel]::Optimal
            ) | Out-Null
        }
    }
}
finally {
    $Archive.Dispose()
}

Write-Host "Release created: $ArchivePath" -ForegroundColor Green
