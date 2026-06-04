#!/usr/bin/env pwsh
# stop-docs.ps1 - zatrzymuje serwery MkDocs.

param(
  [int]$PortAI = 8001,
  [int]$PortUser = 8002
)

Write-Host "Zatrzymuje serwery MkDocs na portach $PortAI i $PortUser..." -ForegroundColor Yellow

foreach ($port in @($PortAI, $PortUser)) {
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
