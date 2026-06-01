<#
.SYNOPSIS
  Wyszukuje wszystkie pliki .md zawierające sequenceDiagram poza 09_procesy_biznesowe/
  — do audytu przed migracją diagramów do katalogu procesów biznesowych.

.PRZYKŁAD
  ./znajdz_sekwencje.ps1
  ./znajdz_sekwencje.ps1 -DocRoot "../../"
#>
param(
  [string]$DocRoot = (Join-Path $PSScriptRoot "../../..")
)

$docAI = Join-Path $DocRoot "doc_AI"
$biz   = Join-Path $docAI "09_procesy_biznesowe"

Write-Host "=== Diagramy sequenceDiagram poza 09_procesy_biznesowe ===" -ForegroundColor Cyan

$all = Get-ChildItem -Path $docAI -Recurse -Filter "*.md" |
  Where-Object { $_.FullName -notlike "$biz*" } |
  Where-Object { (Get-Content $_.FullName -Raw) -match "sequenceDiagram" }

if (-not $all) { Write-Host "Brak — wszystkie sekwencje już przeniesione." -ForegroundColor Green; return }

$all | ForEach-Object {
  $rel = $_.FullName.Replace($docAI + "\", "")
  Write-Host "  $rel" -ForegroundColor Yellow
}

Write-Host "`nLiczba plików do migracji: $($all.Count)" -ForegroundColor Cyan
Write-Host "Uruchom skill doc-biz-process aby przenieść diagramy do 09_procesy_biznesowe/" -ForegroundColor DarkYellow
