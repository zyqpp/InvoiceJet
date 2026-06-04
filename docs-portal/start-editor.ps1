#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Uruchamia webowy edytor plikow Markdown dla portali MkDocs.

.PARAMETER Port
    Port serwera edycji. Domyslnie: 8010.

.PARAMETER Editor
    Opcjonalny zewnetrzny edytor dla endpointu /open-external.
    Zwykle nie jest potrzebny, bo klikniecie w MkDocs otwiera edytor webowy.

.EXAMPLE
    .\start-editor.ps1
    .\start-editor.ps1 -Port 8011
    .\start-editor.ps1 -Editor "code"
#>

param(
    [int]$Port = 8010,
    [string]$Editor = ""
)

$ErrorActionPreference = "Stop"

$python = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        & $cmd --version 2>$null | Out-Null
        $python = $cmd
        break
    } catch {}
}

if (-not $python) {
    Write-Host "Python nie znaleziony." -ForegroundColor Red
    exit 1
}

$script = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "editor-server.py"

Write-Host "Uruchamiam webowy edytor MkDocs: http://127.0.0.1:$Port" -ForegroundColor Green
if ($Editor) {
    & $python $script --port $Port --editor $Editor
} else {
    & $python $script --port $Port
}
