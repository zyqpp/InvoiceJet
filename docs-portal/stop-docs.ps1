#!/usr/bin/env pwsh
# stop-docs.ps1 - zatrzymuje serwery MkDocs.

param(
  [int]$PortAI = 8001,
  [int]$PortUser = 8002,
  [int]$EditorPort = 8010,
  [switch]$NoEditor
)

$ports = @($PortAI, $PortUser)
if (-not $NoEditor) {
  $ports += $EditorPort
}

Write-Host "Zatrzymuje serwery MkDocs/edytor na portach $($ports -join ', ')..." -ForegroundColor Yellow

foreach ($port in $ports) {
  $pids = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING" |
    ForEach-Object { ($_ -split '\s+')[-1] } | Sort-Object -Unique

  foreach ($pid in $pids) {
    if ($pid -match '^\d+$') {
      try {
        Stop-Process -Id $pid -Force -ErrorAction Stop
        Write-Host "Zatrzymano PID $pid (port $port)" -ForegroundColor Green
      } catch {
        Write-Host "PID $pid juz nieaktywny" -ForegroundColor Gray
      }
    }
  }
}

Write-Host "Gotowe." -ForegroundColor Green
