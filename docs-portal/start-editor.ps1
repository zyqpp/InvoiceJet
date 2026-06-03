#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Uruchamia serwer edycji plików (port 8010).

.PARAMETER Port
    Port serwera. Domyślnie: 8010.

.PARAMETER Editor
    Ścieżka do edytora. Domyślnie: Windows "Otwórz za pomocą".
    Przykłady: "notepad++", "code", "C:\Program Files\Notepad++\notepad++.exe"

.EXAMPLE
    .\start-editor.ps1
    .\start-editor.ps1 -Editor "notepad++"
    .\start-editor.ps1 -Editor "code" -Port 8011
#>

param(
    [int]$Port = 8010,
    [string]$Editor = ""
)

$python = $null
foreach ($cmd in @("python", "python3", "py")) {
    try { & $cmd --version 2>$null | Out-Null; $python = $cmd; break } catch {}
}
if (-not $python) { Write-Host "❌ Python nie znaleziony!" -ForegroundColor Red; exit 1 }

$script = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "editor-server.py"
$args_ = "--port $Port"
if ($Editor) { $args_ += " --editor `"$Editor`"" }

Write-Host "✏️  Uruchamiam serwer edycji na porcie $Port..." -ForegroundColor Green
& $python $script --port $Port $(if ($Editor) { "--editor"; $Editor })
